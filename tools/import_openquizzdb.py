#!/usr/bin/env python3
"""Import licensed English multiple-choice source records; never approve content."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'a16819964d171e40e6652368fc562f3bd27d0c5b'
ARCHIVE_URL = f'https://codeload.github.com/Zeuh/OpenQuizzDB/tar.gz/{COMMIT}'
ARCHIVE_SHA = '7ac8efd32ce0d410b29a94db21a495151efb831d41bd764922167b342fd545bc'
BASE = f'https://raw.githubusercontent.com/Zeuh/OpenQuizzDB/{COMMIT}'


def encoded(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def normal(value):
    return unicodedata.normalize('NFKC', value).strip().casefold()


def walk(value, level=''):
    if isinstance(value, list):
        for item in value:
            yield from walk(item, level)
    elif isinstance(value, dict):
        if 'question' in value:
            yield level, value
        else:
            for key, item in value.items():
                yield from walk(item, key)


def records(data, name, sha):
    for level, row in walk(data.get('quizz', {}).get('en', {})):
        choices = row.get('propositions')
        answer = row.get('réponse')
        if not (isinstance(row.get('question'), str) and row['question'].strip()
                and isinstance(choices, list) and len(choices) == 4
                and all(isinstance(s, str) and s.strip() for s in choices)
                and len({normal(s) for s in choices}) == 4 and choices.count(answer) == 1
                and isinstance(row.get('anecdote'), str) and row['anecdote'].strip()):
            continue
        yield {
            'id': f"oqdb_{name.split('_')[-1]}_{row['id']}",
            'status': 'unverified_source_candidate', 'sourceDataset': 'OpenQuizzDB',
            'questionEn': row['question'], 'optionsEn': choices,
            'sourceCorrectIndex': choices.index(answer), 'explanationEn': row['anecdote'],
            'sourceLevel': level, 'sourceTopic': data.get('thème'),
            'sourceAuthor': data.get('rédacteur'), 'sourceId': row['id'],
            'sourceUrl': f'{BASE}/data/{name}.json', 'sourceCommit': COMMIT,
            'sourceSha256': sha, 'license': 'CC-BY-SA-4.0',
            'attribution': f"OpenQuizzDB / {data.get('rédacteur', 'contributors')} (mirror: Zeuh)",
            'missingForGame': ['ru_translation', 'primary_fact_check', 'distractor_review',
                               'explanation_review', 'language_review', 'category_mapping', 'editorial_acceptance'],
        }


def import_archive(path, destination):
    if hashlib.sha256(path.read_bytes()).hexdigest() != ARCHIVE_SHA:
        raise ValueError('OpenQuizzDB archive checksum mismatch')
    destination.mkdir(parents=True, exist_ok=True)
    rows, rejected_files, file_receipts = [], [], []
    seen = set()
    total_en = 0
    with tarfile.open(path) as archive:
        for member in sorted(archive.getmembers(), key=lambda x: x.name):
            parts = Path(member.name).parts
            if not member.isfile():
                continue
            if len(parts) == 2 and parts[-1] == 'LICENCE':
                (destination/'LICENSE-CC-BY-SA-4.0.txt').write_bytes(archive.extractfile(member).read())
            if len(parts) != 3 or parts[-2] != 'data' or not parts[-1].endswith('.json'):
                continue
            raw = archive.extractfile(member).read()
            sha = hashlib.sha256(raw).hexdigest()
            name = Path(parts[-1]).stem
            try:
                data = json.loads(raw.decode('utf-8-sig'))
            except (ValueError, UnicodeError) as error:
                rejected_files.append({'file': parts[-1], 'reason': str(error), 'sha256': sha})
                continue
            en_count = sum(1 for _ in walk(data.get('quizz', {}).get('en', {})))
            if not en_count:
                continue
            total_en += en_count
            candidates = list(records(data, name, sha))
            for row in candidates:
                if row['id'] in seen:
                    raise ValueError(f"Duplicate source ID: {row['id']}")
                seen.add(row['id'])
            rows.extend(candidates)
            file_receipts.append({'file': parts[-1], 'sha256': sha, 'sourceEnRows': en_count,
                                  'acceptedStructuralRows': len(candidates)})
    output = destination/'questions-en.jsonl'
    output.write_bytes(b''.join(encoded(row)+b'\n' for row in rows))
    report = {'schemaVersion': 1, 'sourceArchiveUrl': ARCHIVE_URL, 'sourceArchiveSha256': ARCHIVE_SHA,
              'sourceCommit': COMMIT, 'sourceEnRows': total_en, 'importedSourceRows': len(rows),
              'structurallyRejectedRows': total_en-len(rows), 'rejectedFiles': rejected_files,
              'fileReceipts': file_receipts, 'topics': dict(sorted(Counter(r['sourceTopic'] for r in rows).items())),
              'distinctNormalizedQuestions': len({normal(r['questionEn']) for r in rows}),
              'countIsDistinctFacts': False, 'gameReadyQuestionsAdded': 0,
              'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
    (destination/'report.json').write_bytes(encoded(report)+b'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, required=True)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    path = args.cache/'openquizzdb.tar.gz'
    if not path.exists():
        temp = path.with_suffix('.download')
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error', '--max-time', '90',
                        '--max-filesize', '104857600', ARCHIVE_URL, '-o', str(temp)], check=True)
        if hashlib.sha256(temp.read_bytes()).hexdigest() != ARCHIVE_SHA:
            raise ValueError('OpenQuizzDB archive checksum mismatch')
        temp.replace(path)
    report = import_archive(path, ROOT/'imports/openquizzdb')
    print(json.dumps({k: report[k] for k in ('sourceEnRows', 'importedSourceRows',
                     'structurallyRejectedRows', 'distinctNormalizedQuestions', 'gameReadyQuestionsAdded', 'sha256')}, indent=2))


if __name__ == '__main__':
    main()
