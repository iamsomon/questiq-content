#!/usr/bin/env python3
"""Preserve aligned RU/EN four-choice source records, without game approval.
CLI conversion requires pyarrow; validation/tests of saved JSONL use stdlib only.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '0e619dbeb34206cd48705a1a0ea7fb21cae09993'
BASE = f'https://huggingface.co/datasets/CohereLabs/Global-MMLU/resolve/{COMMIT}'
PINS = {
    'en-dev': '86e985fb70b49130d751c7c5b255767348a8590793dc794ff0f34f1b8bd2d16f',
    'en-test': '5baec81ba97243728cc9557b2cba2f03aaeedf8232473db9f20cf995c6b0a1a9',
    'ru-dev': '9d9dd57996698aeaaca28d58e6f7df9945dedf275cc9d4951a994f0b8c40c8f9',
    'ru-test': '9037e1aaca6aed1856fe1e427e5b3d4e3bb6563861b760a3360ef077df301bd6',
}


def encoded(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def normal(value):
    return unicodedata.normalize('NFKC', value).strip().casefold()


def source_url(lang, split):
    return f'{BASE}/{lang}/{split}-00000-of-00001.parquet'


def align(en_rows, ru_rows, split):
    localized = {}
    for lang, rows in [('en', en_rows), ('ru', ru_rows)]:
        localized[lang] = {}
        for row in rows:
            if row['sample_id'] in localized[lang]:
                raise ValueError(f'Duplicate {lang} source ID: {row["sample_id"]}')
            localized[lang][row['sample_id']] = row
    if localized['en'].keys() != localized['ru'].keys():
        raise ValueError('RU/EN source ID sets differ')
    for key in sorted(localized['en']):
        en, ru = localized['en'][key], localized['ru'][key]
        if en['answer'] != ru['answer'] or en['answer'] not in 'ABCD' or len(en['answer']) != 1:
            raise ValueError(f'{key}: answer alignment mismatch')
        if en['subject'] != ru['subject']:
            raise ValueError(f'{key}: subject alignment mismatch')
        flags = []
        for lang, row in [('en', en), ('ru', ru)]:
            if not isinstance(row['question'], str) or not row['question'].strip():
                raise ValueError(f'{key}: missing {lang} question')
            choices = [row['option_'+letter] for letter in 'abcd']
            if not all(isinstance(s, str) and s.strip() for s in choices):
                flags.append(lang+'_empty_option')
            if len({normal(s) for s in choices if isinstance(s, str)}) != 4:
                flags.append(lang+'_duplicate_options')
            if len(row['question']) > 280:
                flags.append(lang+'_question_exceeds_mobile_limit')
            if any(isinstance(s, str) and len(s) > 140 for s in choices):
                flags.append(lang+'_option_exceeds_mobile_limit')
            if any(s in row['question'].lower() for s in ('following diagram', 'following figure',
                    'shown below', 'figure above', 'диаграмм', 'рисунк', 'изображен')):
                flags.append(lang+'_possible_missing_visual_context')
        if any(s in en['subject'] for s in ('medicine', 'clinical', 'law', 'virology', 'medical', 'nutrition')):
            flags.append('specialist_medical_or_legal_material')
        yield {
            'id': 'gmmlu_'+key.replace('/', '_'), 'sourceId': key, 'sourceSplit': split,
            'status': 'imported_not_game_ready', 'sourceDataset': 'Global-MMLU',
            'sourceSubject': en['subject'], 'sourceSubjectCategory': en['subject_category'],
            'questions': {'en': en['question'], 'ru': ru['question']},
            'options': [dict(id=a, en=en['option_'+a], ru=ru['option_'+a]) for a in 'abcd'],
            'sourceCorrectOptionId': en['answer'].lower(),
            'sourceAnnotations': {lang: {k: row.get(k) for k in ('required_knowledge', 'time_sensitive',
                'reference', 'culture', 'region', 'country', 'cultural_sensitivity_label', 'is_annotated')}
                for lang, row in [('en', en), ('ru', ru)]},
            'sourceCommit': COMMIT,
            'sourceUrls': {lang: source_url(lang, split) for lang in ('en', 'ru')},
            'sourceSha256': {lang: PINS[f'{lang}-{split}'] for lang in ('en', 'ru')},
            'license': 'Apache-2.0', 'attribution': 'Cohere Labs / Shivalika Singh et al., Global-MMLU (2024); based on MMLU by Dan Hendrycks et al.',
            'translationProvenance': 'Publisher combines machine translations, professional translations and post-edits; row-level human translation review is not established by is_annotated.',
            'missingForGame': ['explanation_ru_en', 'primary_fact_and_distractor_check',
                               'language_review', 'category_mapping', 'difficulty', 'editorial_acceptance'],
            'riskFlags': sorted(set(flags)),
        }


def read_source(cache, lang, split):
    path = cache/f'{lang}-{split}.parquet'
    if not path.exists():
        temp = path.with_suffix('.download')
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error', '--max-time', '60',
                        '--max-filesize', '16777216', source_url(lang, split), '-o', str(temp)], check=True)
        if hashlib.sha256(temp.read_bytes()).hexdigest() != PINS[f'{lang}-{split}']:
            raise ValueError('Source checksum mismatch')
        temp.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINS[f'{lang}-{split}']:
        raise ValueError('Source checksum mismatch')
    import pyarrow.parquet as pq
    return pq.read_table(path).to_pylist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', required=True, type=Path)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    rows = []
    for split in ('dev', 'test'):
        rows.extend(align(read_source(args.cache, 'en', split), read_source(args.cache, 'ru', split), split))
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate source IDs across splits')
    folder = ROOT/'imports/global-mmlu'
    folder.mkdir(parents=True, exist_ok=True)
    output = folder/'questions-ru-en.jsonl'
    output.write_bytes(b''.join(encoded(row)+b'\n' for row in rows))
    structural = ('empty_option', 'duplicate_options')
    report = {'schemaVersion': 1, 'sourceCommit': COMMIT, 'sourcePairs': len(rows),
              'distinctNormalizedQuestionPairs': len({tuple(normal(r['questions'][lang]) for lang in ('ru','en')) for r in rows}),
              'fourDistinctNonemptyOptionsBothLocales': sum(not any(any(s in f for s in structural) for f in r['riskFlags']) for r in rows),
              'withinMobileTextLimitsAndFourDistinctOptions': sum(not any(any(s in f for s in structural+('exceeds_mobile_limit',)) for f in r['riskFlags']) for r in rows),
              'subjects': dict(sorted(Counter(r['sourceSubject'] for r in rows).items())),
              'riskFlagCounts': dict(sorted(Counter(f for r in rows for f in r['riskFlags']).items())),
              'sourceReceipts': {f'{lang}-{split}': {'url': source_url(lang, split), 'sha256': PINS[f'{lang}-{split}'],
                    'bytes': (args.cache/f'{lang}-{split}.parquet').stat().st_size} for lang in ('en','ru') for split in ('dev','test')},
              'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'countIsDistinctFacts': False,
              'gameReadyQuestionsAdded': 0, 'humanTranslationReviewInferredFromAnnotations': False}
    (folder/'report.json').write_bytes(encoded(report)+b'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('subjects','sourceReceipts')}, indent=2))


if __name__ == '__main__':
    main()
