"""Original quiz drafts from explicitly selected, checkable catalog facts.

Requires local primary-source snapshots. Produces drafts/evidence only, never
reviews or approval. No source descriptions, images, books or program code are
republished. Each factual assertion is tied to the actual source record hash.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from babel import Locale
from babel.numbers import get_currency_name
from bs4 import BeautifulSoup
import beta1000_choices as C

ROOT = Path(__file__).resolve().parents[1]
OUT, EVIDENCE = [], {}


def pairs(text):
    return [line.split('|') for line in text.strip().splitlines()]


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def add(cat, key, difficulty, ru, en, answer, alternatives, fr, fe, url, record, location):
    qid = f'{cat}_catalog_{key}_0001'
    opts = [answer]+alternatives
    assert len(opts) == 4 and len({x[0] for x in opts}) == len({x[1] for x in opts}) == 4
    q = dict(id=qid, categoryId=cat, difficulty=difficulty, type='single_choice', revision=1,
             localizations={'ru': dict(question=ru, explanation=fr), 'en': dict(question=en, explanation=fe)},
             options=[dict(id=f'o{i}', ru=x[0], en=x[1]) for i, x in enumerate(opts)],
             correctOptionId='o0', sources=[url], image=None)
    OUT.append(q)
    EVIDENCE[qid] = dict(url=url, location=location, sourceRecord=record, sourceRecordSha256=sha(record),
                         claim=f'{en} Answer: {answer[1]}. {fe}')


def wrong(answer, pool, key):
    options = sorted(set(pool)-{answer})
    return random.Random(key).sample(options, 3)


def level(i, total):
    return 'easy' if i < total*.4 else 'medium' if i < total*.8 else 'hard'


def currency_label(code, locale):
    s=get_currency_name(code,locale=locale)
    s={'KGS':'кыргызский сом','KZT':'казахстанский тенге'}.get(code,s) if locale=='ru' else {'KGS':'Kyrgyzstani Som'}.get(code,s)
    return s[:1].upper()+s[1:]


def main(cache):
    # One named entity per question; reverse questions and alternative editions
    # are not used as additional items. Existing source entities are excluded.
    source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in cache.iterdir()
                     if p.name in ['unesco.json', 'art-selected.json', 'pg_catalog.csv', 'jpl.html', 'iau.html', 'elements.html', 'currencies.xml', 'services.csv']}
    existing = json.loads((ROOT/'authoring/beta1000.baseline.json').read_text())['questions'].values()
    used_whc = {int(n) for q in existing for u in q['sources'] for n in re.findall(r'whc.unesco.org/en/list/(\d+)', u)}
    heritage = json.loads((cache/'unesco.json').read_text())
    quota = dict(natural_wonders=100, cities=100, architecture=100, civilizations=20, countries=20)
    counts, countries = Counter(), Counter()
    selected = []
    country_labels = {}
    for r in heritage:
        for code in json.loads(r['iso_codes']):
            country_labels[code] = (Locale('ru').territories.get(code, code), Locale('en').territories.get(code, code))
    country_labels.update(US=('США', 'United States'), GB=('Великобритания', 'United Kingdom'),
                          CD=('ДР Конго', 'Democratic Republic of the Congo'), CG=('Республика Конго', 'Republic of the Congo'), SC=('Сейшелы', 'Seychelles'))
    for r in sorted(heritage, key=lambda r: (int(r['date_inscribed'][:4]), int(r['id_no']))):
        codes = json.loads(r['iso_codes'])
        if len(codes) != 1 or codes[0] in ['IL','PS','RU','UA','XK','SY','YE','AF']: continue
        code = codes[0]
        if int(r['id_no']) in used_whc or countries[code] >= 12 or r['category'] == 'Mixed': continue
        ru, en = r.get('name_ru', ''), r.get('name_en', '')
        if not ru or not en or max(len(ru), len(en)) > 125 or int(r['id_no']) in [31, 266, 355, 369, 487, 577, 740, 983]: continue
        if any(ru.count(a) != ru.count(b) for a,b in [('(',')'),('«','»')]): continue
        # A country embedded verbatim in a title gives away the answer.
        if any(c.casefold() in name.casefold() for c, name in zip(country_labels[code], [ru,en]) if len(c)>3): continue
        s = en.lower()
        if r['category'] == 'Natural': cat = 'natural_wonders'
        elif re.search(r'historic (centre|center|city|town)|city of|old town|medina|historic quarter|town of',s): cat='cities'
        elif re.search(r'archaeolog|prehistor|ancient|rock art|rock-art|petroglyph|neolithic',s): cat='civilizations'
        elif re.search(r'palace|cathedral|church|monastery|castle|abbey|temple|mosque|fort|bridge|sanctuar|basilica|convent|viaduct|tower',s): cat='architecture'
        else: cat='countries'
        if counts[cat] >= quota[cat]: continue
        counts[cat] += 1; countries[code] += 1
        selected.append((r,cat))
    assert dict(counts) == quota, counts
    local_index = Counter()
    for r,cat in selected:
        code = json.loads(r['iso_codes'])[0]; correct = country_labels[code]
        pool = [country_labels[c] for x in heritage if x['region']==r['region'] for c in json.loads(x['iso_codes']) if c in country_labels]
        record = {k:r[k] for k in ['id_no','name_ru','name_en','date_inscribed','category','iso_codes']}
        local_index[cat] += 1
        ru = r['name_ru'].replace('Ройал-Читаван','Читван').replace('окружающие его храмы','окружающие её храмы')
        ru = {'598':'Церкви Молдавии (исторической области)','630':'Остров Кгари (Фрейзер)'}.get(r['id_no'],ru)
        ru = re.sub('[«»“”]', '', ru)
        year = r['date_inscribed'][:4]
        kind_ru,kind_en = ('природный','natural') if r['category']=='Natural' else ('культурный','cultural')
        add(cat, f'whc_{r["id_no"]}', level(local_index[cat]-1, quota[cat]),
            f'В какой стране находится объект всемирного наследия «{ru}»?', f'Which country is home to the World Heritage property {r["name_en"]}?', correct,
            wrong(correct,pool,r['id_no']), f'В Список всемирного наследия этот {kind_ru} объект включили в {year} году.',
            f'This {kind_en} property was inscribed on the World Heritage List in {year}.',
            f'https://whc.unesco.org/en/list/{r["id_no"]}/',record,'Property ID; State Party (single-country property); initial inscription year and category')

    # A museum is the primary authority for its own collection attribution.
    art = {str(r['id']):r for r in json.loads((cache/'art-selected.json').read_text())['data']}
    artist_ru = dict(pairs(C.ARTISTS)); art_pool = [(ru,en) for en,ru in artist_ru.items()]
    for i,(key,title_ru) in enumerate(pairs(C.ART)):
        r=art[key]; assert len(r['artist_ids'])==1 and r['artwork_type_title']=='Painting'
        en=r['artist_title']; answer=(artist_ru[en],en)
        date=str(r['date_start']) if r['date_start']==r['date_end'] else f'{r["date_start"]}–{r["date_end"]}'
        medium=r['medium_display'].lower()
        if 'oil' in medium: mr,me='масляная живопись','oil paint'
        elif 'acrylic' in medium: mr,me='акриловая живопись','acrylic paint'
        elif 'tempera' in medium: mr,me='темпера','tempera'
        else: raise ValueError((key,r['medium_display']))
        title_ru=re.sub('[«»“”]', '', title_ru)
        add('painting',f'art_{key}',level(i,60),f'Кто написал картину «{title_ru}» ({date}) из Чикагского института искусств?',
            f'Who painted {r["title"]} ({date}) in the Art Institute of Chicago?',answer,wrong(answer,art_pool,key),
            f'В музейной записи указана техника: {mr}.',f'The museum records the medium as {me}.',
            f'https://api.artic.edu/api/v1/artworks/{key}',r,'Artwork ID; sole artist attribution; date_start/date_end; medium_display')

    books={r['Text#']:r for r in csv.DictReader((cache/'pg_catalog.csv').open())}
    chosen=[]
    for key,title_ru,author_ru in pairs(C.BOOKS):
        r=books[key]; first=r['Authors'].split(';')[0].strip()
        assert '[' not in first and r['Type']=='Text', (key,first)
        name=re.split(r', (?:-?\d|\?)',first)[0].replace(', graf','').replace(', Sir','')
        if ',' in name:
            surname,given=name.split(',',1); name=f'{given.strip()} {surname}'
        name=re.sub(r'\s*\([^)]*\)','',name).strip()
        name=name.replace('Elizabeth Von Arnim','Elizabeth von Arnim')
        if key=='55':name='L. Frank Baum'
        if key=='60':name='Baroness Orczy'
        chosen.append((key,title_ru,author_ru,name,r,first))
    book_pool=[(x[2],x[3]) for x in chosen]
    for i,(key,title_ru,author_ru,name,r,first) in enumerate(chosen):
        title_en=r['Title'].split('\n')[0].split(';')[0]
        title_en={'3600':'Essais','1232':'The Prince','25717':'The History of the Decline and Fall of the Roman Empire','3800':'Ethics','205':'Walden'}.get(key,title_en)
        answer=(author_ru,name)
        # Birth dates marked uncertain are never asserted as exact.
        dates=re.search(r'(\d{4})-(\d{4})$',first)
        if dates:
            fr=f'Годы жизни автора: {dates[1]}–{dates[2]}.';fe=f'The author lived from {dates[1]} to {dates[2]}.'
        elif key=='1251':fr='Это произведение относится к циклу преданий о короле Артуре.';fe='This work belongs to the cycle of legends about King Arthur.'
        elif key=='521':fr='Роман рассказывает о выживании после кораблекрушения.';fe='The novel follows survival after a shipwreck.'
        else:raise ValueError((key,first))
        add('literature',f'pg_{key}',level(i,90),f'Кто автор произведения «{title_ru}»?',f'Who wrote {title_en}?',answer,
            wrong(answer,book_pool,key),fr,fe,f'https://www.gutenberg.org/ebooks/{key}',
            {k:r[k] for k in ['Text#','Title','Authors','Subjects']},'Catalog ID; primary author, not translator/editor; author dates or subject headings (not ebook upload date)')

    jpl={}
    table=BeautifulSoup((cache/'jpl.html').read_text(),'lxml').find('table')
    for tr in table.find_all('tr'):
        t=tr.find_all('td',recursive=False)
        if len(t)!=12:continue
        name=t[1].get_text(strip=True)
        jpl[name]=dict(parent=t[0].get_text(strip=True),name=name,radius=float(t[6].get_text(strip=True)))
    planets=dict(Mars='Марс',Jupiter='Юпитер',Saturn='Сатурн',Uranus='Уран',Neptune='Нептун',Pluto='Плутон')
    planet_pool=[(ru,en) for en,ru in planets.items()]
    for i,(key,ru) in enumerate(pairs(C.MOONS)):
        r=jpl[key]; answer=(planets[r['parent']],r['parent']);radius=round(r['radius'])
        add('astronomy',f'moon_{key.lower()}',level(i,30),f'Вокруг какого небесного тела обращается спутник {ru}?',
            f'Which celestial body does the moon {key} orbit?',answer,wrong(answer,planet_pool,key),
            f'Средний радиус этого спутника составляет примерно {radius} км.',f'This moon has a mean radius of approximately {radius} km.',
            'https://ssd.jpl.nasa.gov/sats/phys_par/',r,'Planet/satellite row; mean radius, not diameter; parent can be a dwarf planet')

    iau={}
    for tr in BeautifulSoup((cache/'iau.html').read_text(),'html.parser').find('table').find_all('tr')[1:]:
        t=tr.find_all('td',recursive=False)
        for span in t[4].select('.pronunciation'):span.decompose()
        iau[t[2].get_text(strip=True)]=dict(name=t[1].find('strong').get_text(' ',strip=True),genitive=t[4].get_text(' ',strip=True))
    constellation_pool=[(ru,iau[abbr]['name']) for abbr,ru in pairs(C.CONSTELLATIONS)]
    for i,(abbr,ru) in enumerate(pairs(C.CONSTELLATIONS)):
        r=iau[abbr];answer=(ru,r['name'])
        add('astronomy',f'iau_{abbr.lower()}',level(i,30),f'Какому созвездию соответствует официальное сокращение {abbr}?',
            f'Which constellation has the official abbreviation {abbr}?',answer,wrong(answer,constellation_pool,abbr),
            f'Его латинское название в родительном падеже — {r["genitive"]}; эта форма используется в обозначениях звёзд.',
            f'Its Latin genitive is {r["genitive"]}; this form is used in star designations.',
            'https://www.iau.org/IAU/Astronomy-FAQs/Constellations.aspx',dict(abbreviation=abbr,**r),'Constellation Names table: nominative, exact three-letter abbreviation and genitive')

    elements={}
    for tr in BeautifulSoup((cache/'elements.html').read_text(),'html.parser').find_all('tr'):
        t=[x.get_text(' ',strip=True) for x in tr.find_all('td',recursive=False)]
        if len(t)>=4 and t[0].isdigit() and re.fullmatch('[A-Z][a-z]?',t[1]):
            elements[t[1]]=dict(number=int(t[0]),symbol=t[1],name=t[2])
    element_pool=[(ru,elements[symbol]['name']) for symbol,ru in pairs(C.ELEMENTS)]
    for i,(symbol,ru) in enumerate(pairs(C.ELEMENTS)):
        r=elements[symbol];answer=(ru,r['name'])
        add('chemistry',f'element_{symbol.lower()}',level(i,50),f'Какой химический элемент обозначается символом {symbol}?',
            f'Which chemical element has the symbol {symbol}?',answer,wrong(answer,element_pool,symbol),
            f'Атомный номер этого элемента — {r["number"]}: столько протонов в ядре его атома.',
            f'Its atomic number is {r["number"]}, the number of protons in its atomic nucleus.',
            'https://iupac.qmul.ac.uk/AtWt/',r,'Element row: atomic number, symbol, name; atomic weights deliberately not used')

    currencies={}
    for row in ET.parse(cache/'currencies.xml').findall('.//CcyNtry'):
        code=row.findtext('Ccy')
        if code and code not in currencies:
            currencies[code]=dict(code=code,name=row.findtext('CcyNm'),number=row.findtext('CcyNbr'))
    currency_pool=[(currency_label(code,'ru'),currency_label(code,'en')) for code,_ in pairs(C.CURRENCIES)]
    for i,(code,country_ru) in enumerate(pairs(C.CURRENCIES)):
        r=currencies[code];answer=(currency_label(code,'ru'),currency_label(code,'en'))
        add('economics',f'currency_{code.lower()}',level(i,40),f'Какой валюте соответствует код {code} в стандарте ISO 4217?',
            f'Which currency has the ISO 4217 code {code}?',answer,wrong(answer,currency_pool,code),
            f'Её цифровой код — {r["number"]}. Буквенные и цифровые коды позволяют однозначно обозначать валюты.',
            f'Its numeric code is {r["number"]}. Alphabetic and numeric codes identify currencies unambiguously.',
            'https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html',r,'ISO 4217 List One XML: alphabetic code, currency name and numeric code; snapshot 23 October 2026')

    services=list(csv.DictReader((cache/'services.csv').open()))
    all_ports=[int(row[2]) for row in pairs(C.SERVICES)]
    en_labels={'ftp':'FTP control','bootps':'BOOTP server','bootpc':'BOOTP client','netbios-ns':'NetBIOS Name Service','netbios-dgm':'NetBIOS Datagram Service','netbios-ssn':'NetBIOS Session Service','printer':'LPD printing','ftps':'FTPS control'}
    for i,(name,transport,port,label_ru) in enumerate(pairs(C.SERVICES)):
        source=next(r for r in services if r['Service Name']==name and r['Transport Protocol']==transport and r['Port Number']==port)
        en_label=en_labels.get(name,label_ru)
        assert not re.search('[А-Яа-я]',en_label)
        answer=(port,port); pool=[(str(x),str(x)) for x in all_ports]
        range_ru,range_en=('системных портов 0–1023','system ports 0–1023') if int(port)<1024 else ('пользовательских портов 1024–49151','user ports 1024–49151')
        add('information_technology',f'port_{name.replace("-","_")}',level(i,50),f'Какой порт {transport.upper()} зарегистрирован для сервиса {label_ru}?',
            f'Which {transport.upper()} port is registered for {en_label}?',answer,wrong(answer,pool,name),
            f'Этот номер относится к диапазону {range_ru}. Регистрация порта не гарантирует, какой трафик фактически через него проходит.',
            f'This number is in the range of {range_en}. A registration does not guarantee what traffic actually uses a port.',
            'https://www.iana.org/assignments/service-names-port-numbers/',
            {k:source[k] for k in ['Service Name','Port Number','Transport Protocol','Description']},'Exact service + transport row; port range definitions and registry warning about actual traffic')

    assert len(OUT)==690, len(OUT)
    (ROOT/'authoring/beta1000.source-hashes.json').write_text(json.dumps(source_hashes,indent=2)+'\n')
    (ROOT/'authoring/beta1000.evidence.json').write_text(json.dumps(EVIDENCE,ensure_ascii=False,indent=2)+'\n')
    for cat in sorted({q['categoryId'] for q in OUT}):
        (ROOT/'drafts'/f'beta1000_{cat}.json').write_text(json.dumps([q for q in OUT if q['categoryId']==cat],ensure_ascii=False,indent=2)+'\n')
    print('690 drafts written. No approvals or published questions changed.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cache',type=Path,required=True)
    main(parser.parse_args().cache)
