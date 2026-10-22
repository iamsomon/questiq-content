#!/usr/bin/env python3
"""Import existing RU/EN source banks, with original answers and provenance.

No generated translations, distractors, explanations, or publication approvals.
The intake format deliberately differs from the mobile question schema.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
MKQA_COMMIT = 'f964fe1bac4d580cee3d4928572df1f676f8e656'
RUBQ_COMMIT = 'fade3eae6a4807c35b19cfce20dfa805fc8c0cdf'
MKQA_URL = f'https://raw.githubusercontent.com/apple-aiml-research/ml-mkqa/{MKQA_COMMIT}/dataset/mkqa.jsonl.gz'
RUBQ_BASE = f'https://raw.githubusercontent.com/vladislavneon/RuBQ/{RUBQ_COMMIT}'
ATTRIBUTIONS = {
    'mkqa': 'Shayne Longpre, Yi Lu, Joachim Daiber / MKQA, Apple',
    'rubq': 'Ivan Rybin, Vladislav Korablinov, Pavel Efimov, Pavel Braslavski / RuBQ 2.0',
}
LICENSES = {'mkqa': 'CC-BY-SA-3.0', 'rubq': 'CC-BY-SA-4.0'}
SOURCE_HASHES = {
    'mkqa.jsonl.gz': 'f77ac6bf6306e98816c5c047880db71a3c67d2f1491b169896d63e9bb14ef3d3',
    'rubq-dev.json': '6cd20dcfad3404736691c5dcee271d19f579b6c5755a1aad4c4de644bc9dfd05',
    'rubq-test.json': '63d9e32a1bdefb2de713a9ccf3a0f9f0a4a48f2fdddd35b3908d6846b63dc85b',
}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def normal(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def risks(ru, en):
    flags = []
    both = ru.casefold() + ' ' + en.casefold()
    if any(s in both for s in ('currently', 'current president', 'last time', 'how many seasons',
                               'how many episodes', 'how old is', 'последний раз', 'сейчас',
                               'сколько сезонов', 'сколько серий', 'сколько лет', 'на данный момент')):
        flags.append('possibly_time_dependent_or_underspecified')
    if max(len(ru), len(en)) > 280:
        flags.append('question_exceeds_mobile_limit')
    return flags


def mkqa_rows(rows, source_sha):
    for line, row in enumerate(rows, 1):
        queries, answers = row.get('queries', {}), row.get('answers', {})
        if not all(isinstance(queries.get(lang), str) and queries[lang].strip()
                   and isinstance(answers.get(lang), list) and answers[lang] for lang in ('ru', 'en')):
            raise ValueError(f'MKQA line {line}: missing parallel question/answer annotations')
        flags = risks(queries['ru'], queries['en'])
        types = {a.get('type') for lang in ('ru', 'en') for a in answers[lang]}
        if types & {'unanswerable', 'long_answer'}:
            flags.append('source_has_no_short_answer')
        if types & {'binary'}:
            flags.append('binary_format')
        en_entities = {a['entity'] for a in answers['en'] if a.get('entity')}
        ru_entities = {a['entity'] for a in answers['ru'] if a.get('entity')}
        if en_entities != ru_entities:
            flags.append('entity_alignment_requires_review')
        canonical = {a.get('entity') or a.get('text') for a in answers['en']}
        if len(canonical - {None}) > 1:
            flags.append('multiple_source_answers')
        yield {
            'id': f"mkqa_{str(row['example_id']).replace('-', 'n')}",
            'status': 'imported_not_game_ready', 'sourceDataset': 'mkqa',
            'questions': {lang: queries[lang] for lang in ('ru', 'en')},
            'answers': {lang: answers[lang] for lang in ('ru', 'en')},
            'sourceId': str(row['example_id']), 'sourceLine': line,
            'sourceUrl': MKQA_URL, 'sourceCommit': MKQA_COMMIT, 'sourceSha256': source_sha,
            'license': LICENSES['mkqa'], 'attribution': ATTRIBUTIONS['mkqa'],
            'translationProvenance': {'ru': 'human_translation_reported_by_publisher', 'en': 'source_original'},
            'missingForGame': ['four_options', 'explanation_ru_en', 'category', 'difficulty', 'editorial_acceptance'],
            'riskFlags': sorted(flags),
        }


def rubq_rows(rows, split, source_sha):
    for index, row in enumerate(rows):
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in ('question_text', 'question_eng')):
            raise ValueError(f'RuBQ {split}/{index}: missing parallel question')
        translated = {'ru': [], 'en': []}
        flags = risks(row['question_text'], row['question_eng'])
        for answer in row['answers']:
            names = answer.get('wd_names') or {}
            for lang in ('ru', 'en'):
                aliases = list(names.get(lang) or [])
                if not aliases and lang == 'ru' and answer.get('label'):
                    aliases = [answer['label']]
                translated[lang].append({'value': answer.get('value'), 'type': answer.get('type'),
                                         'sourceLabel': answer.get('label'), 'aliases': aliases})
        if not row['answers']:
            flags.append('source_has_no_short_answer')
        if len(row['answers']) > 1:
            flags.append('multiple_source_answers')
        if any(not a['aliases'] for lang in ('ru', 'en') for a in translated[lang]):
            flags.append('localized_answer_label_missing')
        if 'no-answer' in row.get('tags', []):
            flags.append('source_query_not_answerable')
        yield {
            'id': f"rubq_{row['uid']}", 'status': 'imported_not_game_ready', 'sourceDataset': 'rubq',
            'questions': {'ru': row['question_text'], 'en': row['question_eng']},
            'answers': translated, 'sourceAnswerRu': row.get('answer_text'),
            'sourceId': str(row['uid']), 'sourceIndex': index, 'sourceSplit': split,
            'sourceUrl': f'{RUBQ_BASE}/RuBQ_2.0/RuBQ_2.0_{split}.json',
            'sourceCommit': RUBQ_COMMIT, 'sourceSha256': source_sha,
            'license': LICENSES['rubq'], 'attribution': ATTRIBUTIONS['rubq'],
            'translationProvenance': {'ru': 'source_original', 'en': 'source_machine_translation'},
            'query': row['query'], 'entities': row['question_uris'],
            'properties': row['question_props'], 'tags': row.get('tags', []),
            'paragraphIds': row.get('paragraphs_uids', {}).get('with_answer', []),
            'missingForGame': ['four_options', 'explanation_ru_en', 'category', 'difficulty',
                               'english_copy_review', 'editorial_acceptance'],
            'riskFlags': sorted(set(flags)),
        }


def write_bank(rows, output):
    ids = set()
    pairs = Counter()
    flags = Counter()
    count = 0
    unflagged = 0
    with output.open('wb') as stream:
        for row in rows:
            if row['id'] in ids:
                raise ValueError(f"Duplicate source ID: {row['id']}")
            ids.add(row['id'])
            pair = tuple(normal(row['questions'][lang]) for lang in ('ru', 'en'))
            pairs[pair] += 1
            flags.update(row['riskFlags'])
            unflagged += not row['riskFlags']
            stream.write(encoded(row) + b'\n')
            count += 1
    return {'sourceRows': count, 'uniqueSourceIds': len(ids), 'distinctNormalizedPairs': len(pairs),
            'duplicatePairRows': count-len(pairs), 'riskFlagCounts': dict(sorted(flags.items())),
            'rowsWithoutAutomaticRiskFlags': unflagged,
            'gameReadyQuestionsAdded': 0, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


def download(url, path):
    if path.exists():
        verify_source(path, path.name)
        return
    temp = path.with_suffix('.download')
    subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error', '--max-time', '60',
                    '--max-filesize', '25165824', url, '-o', str(temp)], check=True)
    verify_source(temp, path.name)
    temp.replace(path)


def verify_source(path, name):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SOURCE_HASHES[name]:
        raise ValueError(f'Source checksum mismatch: {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, required=True)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    destination = ROOT / 'imports/parallel-qa'
    destination.mkdir(parents=True, exist_ok=True)
    mkqa = args.cache / 'mkqa.jsonl.gz'
    download(MKQA_URL, mkqa)
    mkqa_hash = hashlib.sha256(mkqa.read_bytes()).hexdigest()
    with gzip.open(mkqa, 'rt', encoding='utf-8') as f:
        mkqa_report = write_bank(mkqa_rows((json.loads(line) for line in f), mkqa_hash), destination/'mkqa-ru-en.jsonl')
    all_rubq = []
    receipts = [{'url': MKQA_URL, 'sha256': mkqa_hash, 'bytes': mkqa.stat().st_size}]
    for split in ('dev', 'test'):
        path = args.cache / f'rubq-{split}.json'
        url = f'{RUBQ_BASE}/RuBQ_2.0/RuBQ_2.0_{split}.json'
        download(url, path)
        raw = path.read_bytes()
        h = hashlib.sha256(raw).hexdigest()
        receipts.append({'url': url, 'sha256': h, 'bytes': len(raw)})
        all_rubq.extend(rubq_rows(json.loads(raw), split, h))
    rubq_report = write_bank(all_rubq, destination/'rubq-ru-en.jsonl')
    report = {'schemaVersion': 1, 'sources': {'mkqa': mkqa_report, 'rubq': rubq_report},
              'sourceRows': mkqa_report['sourceRows'] + rubq_report['sourceRows'],
              'countIsDistinctFacts': False, 'gameReadyQuestionsAdded': 0,
              'sourceReceipts': receipts, 'publishedMobileContentUnchanged': True}
    (destination/'report.json').write_bytes(encoded(report)+b'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
