#!/usr/bin/env python3
"""Collect a pinned, licensed research queue. Never writes playable questions/reviews.

Network reads use curl's verified system TLS store. The source is a historical
community collection: its answers are NOT accepted as factual evidence.
"""
import argparse
from collections import Counter, deque
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'dcc1cdf36c2985ed5c849d1f2265c5041ffcdfb9'
BASE = f'https://raw.githubusercontent.com/uberspot/OpenTriviaQA/{COMMIT}'
CATEGORIES = ('animals brain-teasers celebrities entertainment for-kids general geography '
              'history hobbies humanities literature movies music newest people rated '
              'religion-faith science-technology sports television video-games world').split()


def normal(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def parse(text, category):
    """Reject malformed / ambiguous option matching; keep source line provenance."""
    blocks = re.split(r'(?m)^#Q ', text)
    offset = 1 + blocks[0].count('\n')
    for block in blocks[1:]:
        lines = block.splitlines()
        line = offset
        offset += block.count('\n')
        if not lines:
            continue
        question = html.unescape(lines[0]).strip()
        answers = [html.unescape(s[2:]).strip() for s in lines[1:] if s.startswith('^ ')]
        options = [html.unescape(s[2:]).strip() for s in lines[1:] if re.match(r'^[A-Z] ', s)]
        if len(answers) != 1 or len(options) != 4:
            continue
        if any(unicodedata.category(c) == 'Cc' for s in [question, *options] for c in s):
            continue
        if len({normal(s) for s in options}) != 4 or not all(normal(s) for s in options):
            continue
        matches = [i for i, s in enumerate(options) if normal(s) == normal(answers[0])]
        if len(matches) != 1 or not 5 <= len(question) <= 280 or any(len(s) > 140 for s in options):
            continue
        if any(s in question.casefold() for s in ('currently', 'this year', 'how old is', 'as of today')):
            continue
        fingerprint = hashlib.sha256(normal(question).encode()).hexdigest()
        yield {
            'candidateId': 'otqa_' + fingerprint[:24],
            'status': 'unverified_source_candidate',
            'sourceCategory': category,
            'questionEn': question,
            'optionsEn': options,
            'sourceCorrectIndex': matches[0],
            'source': f'{BASE}/categories/{category}',
            'sourceLine': line,
            'sourceCommit': COMMIT,
            'license': 'CC-BY-SA-4.0',
            'attribution': 'OpenTriviaQA contributors / uberspot',
            'missing': ['primary_fact_check', 'category_assignment', 'ru_translation',
                        'explanation_ru_en', 'distractor_check', 'editorial_review'],
        }


def collect(count, cache, output):
    cache.mkdir(parents=True, exist_ok=True)
    queues = []
    sources = []
    for category in CATEGORIES:
        path = cache / category
        if not path.exists():
            subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                            '--max-time', '30', '--max-filesize', '2097152',
                            f'{BASE}/categories/{category}', '-o', str(path)], check=True)
            time.sleep(.5)
        raw = path.read_bytes()
        try:
            text, encoding = raw.decode('utf-8-sig'), 'utf-8'
        except UnicodeDecodeError:
            # Historical files mix UTF-8 and legacy lines. Do not mojibake an
            # entire file because one line contains a Windows-1252 character.
            decoded = []
            for line in raw.splitlines(keepends=True):
                try:
                    decoded.append(line.decode('utf-8-sig'))
                except UnicodeDecodeError:
                    decoded.append(line.decode('cp1252'))
            text, encoding = ''.join(decoded), 'utf-8-with-per-line-cp1252-fallback'
        sources.append({'category': category, 'sha256': hashlib.sha256(raw).hexdigest(),
                        'bytes': len(raw), 'decodedAs': encoding})
        queues.append(deque(parse(text, category)))
    chosen = []
    seen = set()
    while len(chosen) < count and any(queues):
        for queue in queues:
            while queue:
                row = queue.popleft()
                key = normal(row['questionEn'])
                if key in seen:
                    continue
                seen.add(key)
                chosen.append(row)
                break
            if len(chosen) == count:
                break
    if len(chosen) < count:
        raise ValueError(f'Only {len(chosen)} eligible unique candidates, requested {count}')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in chosen))
    report = {'sourceCommit': COMMIT, 'candidateCount': len(chosen),
              'playableQuestionsAdded': 0, 'factChecked': False, 'ruTranslated': False,
              'sourceCategoryCounts': dict(sorted(Counter(r['sourceCategory'] for r in chosen).items())),
              'queueSha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'sources': sources}
    output.with_suffix('.report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'sources'}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count', type=int, default=10000)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--output', type=Path, default=ROOT / 'research/candidates/open-trivia-qa.jsonl')
    a = p.parse_args()
    if not 1 <= a.count <= 20000:
        p.error('count must be 1..20000')
    collect(a.count, a.cache, a.output)
