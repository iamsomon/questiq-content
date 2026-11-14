#!/usr/bin/env python3
"""Select a reproducible RU/EN review batch from the pinned Global-MMLU intake."""
import argparse
from collections import Counter, defaultdict, deque
import json
from pathlib import Path
import re

from content import ROOT, digest, encoded, inventory, normalized, require

SUBJECT_GROUPS = {
    'mathematics': 'elementary_mathematics high_school_mathematics high_school_statistics',
    'physics': 'conceptual_physics high_school_physics',
    'chemistry': 'high_school_chemistry',
    'biology': 'high_school_biology',
    'human_body': 'anatomy',
    'astronomy': 'astronomy',
    'economics': 'high_school_microeconomics high_school_macroeconomics',
    'ancient_world': 'prehistory',
    'modern_history': 'high_school_european_history high_school_us_history',
    'information_technology': 'high_school_computer_science',
    'artificial_intelligence': 'machine_learning',
    'civilizations': 'high_school_world_history',
    'countries': 'high_school_geography',
    'world_religions': 'world_religions',
}
CATEGORY_BY_SUBJECT = {
    subject: category
    for category, subjects in SUBJECT_GROUPS.items()
    for subject in subjects.split()
}
SOURCE_FIELDS = (
    'sourceId', 'sourceCommit', 'sourceUrls', 'sourceSha256', 'license',
    'attribution', 'translationProvenance',
)
AMBIGUOUS_OPTION = re.compile(
    r'^(?:all|none|both) (?:of the above|of these|of them|a and b)|'
    r'^(?:все|ничего|ни один) (?:из перечисленного|из указанных|из вариантов|вышеперечисленное)',
    re.IGNORECASE,
)


def select_rows(root, count, already_queued):
    categories, existing, _, revoked = inventory(root)
    known_categories = {category['id'] for category in categories}
    published_counts = Counter(
        q['categoryId'] for stage, q in existing if stage == 'questions'
    )
    used_ids = {q['id'] for _, q in existing} | set(revoked)
    used_text = {
        (locale, normalized(q['localizations'][locale]['question']))
        for _, q in existing for locale in ('ru', 'en')
    }
    previous_rows = list(already_queued)
    used_ids.update(row['candidateId'] for row in previous_rows)
    used_text.update(
        (locale, normalized(row['questions'][locale]))
        for row in previous_rows for locale in ('ru', 'en')
    )
    adapted = root / 'credits/global_mmlu_20261023.mapping.json'
    if adapted.exists():
        for row in json.loads(adapted.read_text()):
            if isinstance(row, dict) and row.get('sourceId'):
                used_ids.add('gmmlu_' + row['sourceId'].replace('/', '_'))

    by_category = defaultdict(deque)
    rejected = Counter()
    source = root / 'imports/global-mmlu/questions-ru-en.jsonl'
    with source.open(encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            category = CATEGORY_BY_SUBJECT.get(row['sourceSubject'])
            if category not in known_categories:
                rejected['outside_selected_subjects'] += 1
                continue
            if row['riskFlags'] or any(
                row['sourceAnnotations'][locale]['time_sensitive'] not in ('[]', '', None, [])
                for locale in ('ru', 'en')
            ):
                rejected['source_risk_flag'] += 1
                continue
            if any(AMBIGUOUS_OPTION.search(o[locale].strip())
                   for o in row['options'] for locale in ('ru', 'en')):
                rejected['context_dependent_option'] += 1
                continue
            keys = {(locale, normalized(row['questions'][locale]))
                    for locale in ('ru', 'en')}
            if row['id'] in used_ids or keys & used_text:
                rejected['duplicate_or_previously_queued'] += 1
                continue
            require(len(row['options']) == 4 and sum(
                o['id'] == row['sourceCorrectOptionId'] for o in row['options']
            ) == 1, f"Invalid source answer in {row['id']}")
            used_ids.add(row['id'])
            used_text.update(keys)
            by_category[category].append({
                'candidateId': row['id'],
                'categorySuggestion': category,
                'status': 'needs_editorial_review',
                'questions': row['questions'],
                'options': row['options'],
                'sourceCorrectOptionId': row['sourceCorrectOptionId'],
                'source': {key: row[key] for key in SOURCE_FIELDS},
                'needs': ['fact_check', 'distractor_review', 'ru_en_review', 'ru_en_explanations'],
            })

    selected = []
    order = sorted(by_category, key=lambda category: (published_counts[category], category))
    while len(selected) < count and any(by_category.values()):
        for category in order:
            if by_category[category]:
                selected.append(by_category[category].popleft())
            if len(selected) == count:
                break
    require(len(selected) == count, f'Found {len(selected)} eligible candidates for {count} requested')
    return selected, rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count', type=int, default=2000)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--exclude', type=Path, action='append', default=[])
    args = parser.parse_args()
    if not 1 <= args.count <= 10000:
        parser.error('count must be 1..10000')
    output = args.output.resolve()
    for folder in ('questions', 'reviews', 'dist', 'drafts', 'catalog'):
        require(not output.is_relative_to(ROOT / folder), 'Choose a separate review output directory')
    report_file = output.with_suffix('.report.json')
    require(not output.exists() and not report_file.exists(), 'Choose a new batch output path')
    previous = [json.loads(line) for file in args.exclude
                for line in file.read_text(encoding='utf-8').splitlines() if line.strip()]
    rows, rejected = select_rows(ROOT, args.count, previous)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b''.join(encoded(row) + b'\n' for row in rows))
    report = {
        'candidates': len(rows),
        'editoriallyReviewed': 0,
        'published': 0,
        'categorySuggestions': dict(sorted(Counter(r['categorySuggestion'] for r in rows).items())),
        'excludedSourceRows': dict(sorted(rejected.items())),
        'batchSha256': digest(rows),
        'output': output.name,
    }
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
