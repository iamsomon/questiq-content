"""Original bilingual drafts. Running this file never grants approval."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT, EVIDENCE, SOURCES = [], {}, {}

def source(key, url):
    assert key not in SOURCES
    SOURCES[key] = url

def rows(category, text):
    for line in text.strip().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        slug, level, prompt, choices, explanation, src, location = line.split('§')
        ru, en = prompt.split('~')
        er, ee = explanation.split('~')
        options = [x.split('~') for x in choices.split(';')]
        assert len(options) == 4 and all(len(x) == 2 for x in options), slug
        q = dict(id=f'{category}_depth_{slug}', categoryId=category,
                 difficulty={'E':'easy','M':'medium','H':'hard'}[level],
                 type='single_choice', revision=1,
                 localizations={'ru':dict(question=ru, explanation=er),
                                'en':dict(question=en, explanation=ee)},
                 options=[dict(id=f'o{i}',ru=a,en=b) for i,(a,b) in enumerate(options)],
                 correctOptionId='o0', sources=[SOURCES[src]], image=None)
        OUT.append(q)
        EVIDENCE[q['id']] = dict(url=SOURCES[src], location=location, claim=ee)

def write():
    old = {q['id'] for p in (ROOT/'questions').glob('*.json') for q in json.loads(p.read_text())}
    assert not old.intersection(q['id'] for q in OUT), 'Already published; do not rerun historical drafts'
    assert len({q['id'] for q in OUT}) == len(OUT)
    grouped = {}
    for q in OUT:
        grouped.setdefault(q['categoryId'], []).append(q)
    for category, questions in grouped.items():
        (ROOT/'drafts'/f'{category}.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
    for suffix, data in [('evidence', EVIDENCE), ('sources', SOURCES)]:
        (ROOT/'authoring'/f'deepening_20261108.{suffix}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(f'Drafts only: {len(OUT)} questions in {len(grouped)} categories')

if __name__ == '__main__':
    for part in sorted((ROOT/'authoring/deepening_20261108_parts').glob('*.py')):
        exec(compile(part.read_text(), str(part), 'exec'), globals())
    write()
