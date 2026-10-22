#!/usr/bin/env python3
"""Content-only validator and deterministic publisher. No credentials or network writes."""
import argparse, hashlib, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
def encoded(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(value):return hashlib.sha256(encoded(value)).hexdigest()
def load(path,default=None):return json.loads(path.read_text()) if path.exists() else default
def require(ok,message):
 if not ok:raise ValueError(message)
def normalized(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
def check_question(q,categories):
 require(set(q)=={'id','categoryId','difficulty','type','revision','localizations','options','correctOptionId','sources','image'},'Unexpected/missing question fields')
 name=q['id'];require(isinstance(name,str) and re.fullmatch(r'[a-z0-9_]{5,80}',name),f'Invalid ID: {name}')
 require(q['categoryId'] in categories,f'{name}: unknown category')
 require(q['type']=='single_choice' and q['difficulty'] in ['easy','medium','hard'],f'{name}: type/difficulty')
 require(type(q['revision']) is int and q['revision']>0,f'{name}: revision')
 require(set(q['localizations'])=={'ru','en'},f'{name}: both locales required')
 opts=q['options'];require(isinstance(opts,list) and len(opts)==4,f'{name}: exactly four options')
 ids=[o['id'] for o in opts];require(len(set(ids))==4 and ids.count(q['correctOptionId'])==1,f'{name}: answer IDs')
 for o in opts:require(set(o)=={'id','ru','en'} and re.fullmatch(r'[a-z0-9_]+',o['id']),f'{name}: option fields')
 for lang in ['ru','en']:
  loc=q['localizations'][lang];require(set(loc)=={'question','explanation'},f'{name}: locale fields')
  require(isinstance(loc['question'],str) and 5<=len(loc['question'].strip())<=280,f'{name}: question length')
  require(isinstance(loc['explanation'],str) and 10<=len(loc['explanation'].strip())<=600,f'{name}: explanation length')
  labels=[normalized(o[lang]) for o in opts];require(all(labels) and len(set(labels))==4,f'{name}: duplicate/empty option labels')
  require(all(isinstance(o[lang],str) and len(o[lang])<=140 for o in opts),f'{name}: option length')
  require(not any(x in loc['question'].lower() for x in ['lorem ipsum','todo','placeholder']),f'{name}: filler')
 require(isinstance(q['sources'],list) and q['sources'] and len(q['sources'])==len(set(q['sources'])),f'{name}: sources')
 for u in q['sources']:
  uri=urlsplit(u);require(uri.scheme=='https' and uri.hostname and not uri.username,f'{name}: HTTPS source required')
 image=q['image']
 if image is not None:
  require(set(image)=={'url','required','fit','aspectRatio','attribution','license'},f'{name}: image fields')
  require(image['url'].startswith('https://') and type(image['required']) is bool and image['fit'] in ['contain','cover'] and type(image['aspectRatio']) in [int,float] and 0<image['aspectRatio']<=4 and image['attribution'].strip() and image['license'].strip(),f'{name}: media rights/shape')
 return q

def inventory(root=ROOT):
 cats=load(root/'catalog/categories.json'); categories={c['id'] for c in cats}
 require(len(cats)==len(categories)==50,'Exactly fifty stable categories required')
 revoked=load(root/'revoked.json',[]);require(len(revoked)==len(set(revoked)) and all(re.fullmatch(r'[a-z0-9_]{5,80}',i) for i in revoked),'Revoked IDs')
 reviews={}
 for p in sorted((root/'reviews').glob('*.json')):
  for row in load(p,[]):
   require(row['id'] not in reviews,f"Duplicate review: {row['id']}");reviews[row['id']]=row
 items=[];ids=set();texts=set()
 for stage in ['questions','drafts']:
  for p in sorted((root/stage).glob('*.json')):
   data=load(p);require(isinstance(data,list),f'{p}: expected array')
   for q in data:
    check_question(q,categories);name=q['id']
    require(name not in ids,f'Duplicate ID across files/stages: {name}');ids.add(name)
    for lang in ['ru','en']:
     key=(lang,normalized(q['localizations'][lang]['question']))
     require(key not in texts,f'{name}: duplicate wording');texts.add(key)
    if stage=='questions':
     require(name not in revoked,f'{name}: revoked ID cannot be published')
     r=reviews.get(name,{});require(r.get('status')=='approved',f'{name}: no approval')
     require(r.get('sha256')==digest(q),f'{name}: stale review hash')
     require(all(isinstance(r.get(k),str) and r[k].strip() for k in ['author','factReviewer','languageReviewer','checkedAt','method']),f'{name}: incomplete review roles')
     require(type(r.get('humanApproved')) is bool,f'{name}: human approval must be explicit')
     require(r['method'] in ['human_editorial_review','agent_source_review'],f'{name}: unknown review method')
     require(not r['humanApproved'] or r['method']=='human_editorial_review',f'{name}: false human approval')
     checks=r.get('sourceChecks',[]);require(checks and all(c.get('url') in q['sources'] and c.get('claim','').strip() and c.get('location','').strip() for c in checks),f'{name}: missing source evidence')
    items.append((stage,q))
 return cats,items,reviews,revoked

def report(root=ROOT):
 cats,items,reviews,revoked=inventory(root)
 rows=[]
 for c in cats:
  approved=[q for stage,q in items if stage=='questions' and q['categoryId']==c['id']]
  draft=[q for stage,q in items if stage=='drafts' and q['categoryId']==c['id']]
  rows.append({'id':c['id'],'approved':len(approved),'draft':len(draft),'humanApproved':sum(reviews[q['id']]['humanApproved'] for q in approved),'difficulty':dict(Counter(q['difficulty'] for q in approved)),'playable':len(approved)>=10})
 return {'schemaVersion':1,'approvedQuestions':sum(r['approved'] for r in rows),'draftQuestions':sum(r['draft'] for r in rows),'playableCategories':sum(r['playable'] for r in rows),'humanApprovedQuestions':sum(r['humanApproved'] for r in rows),'targetQuestions':10000,'revokedCount':len(revoked),'categories':rows}

def build(root,base):
 uri=urlsplit(base);require(uri.scheme=='https' and uri.hostname and not uri.username and not uri.query and not uri.fragment,'HTTPS base URL required')
 cats,items,reviews,revoked=inventory(root);approved=sorted([q for stage,q in items if stage=='questions'],key=lambda q:q['id'])
 registry=load(root/'catalog/revisions.json',{})
 for q in approved:
  old=registry.get(q['id']);h=digest(q)
  if old:require(q['revision']>=old['revision'] and (h==old['sha256'] or q['revision']>old['revision']),f"{q['id']}: changing published content requires a higher revision")
  registry[q['id']]={'revision':q['revision'],'sha256':h}
 old_revoked=load(root/'dist/manifest.json',{}).get('revokedIds',[])
 require(set(old_revoked).issubset(revoked),'Revocations must be cumulative')
 dist=root/'dist';packs=dist/'packs';packs.mkdir(parents=True,exist_ok=True)
 manifest={'schemaVersion':1,'version':digest({'questions':approved,'revoked':sorted(revoked)}),'revokedIds':sorted(revoked),'packs':[]}
 keep=set()
 for c in sorted({q['categoryId'] for q in approved}):
  batch=[q for q in approved if q['categoryId']==c];require(len(batch)>=10,f'{c}: fewer than ten approved questions')
  payload=encoded(batch)+b'\n';require(len(payload)<=2097152,f'{c}: pack exceeds byte budget')
  sha=hashlib.sha256(payload).hexdigest();name=f'{c}-{sha[:16]}.json';keep.add(name);(packs/name).write_bytes(payload)
  for lang in ['ru','en']:manifest['packs'].append({'schemaVersion':1,'locale':lang,'category':c,'url':base.rstrip('/')+'/packs/'+name,'sha256':sha,'size':len(payload)})
 for p in packs.glob('*.json'):
  if p.name not in keep:p.unlink()
 (dist/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (root/'catalog/revisions.json').write_text(json.dumps(registry,indent=2,sort_keys=True)+'\n')
 (dist/'quality-report.json').write_text(json.dumps(report(root),ensure_ascii=False,indent=2)+'\n')
 return manifest

def main():
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['validate','report','build','hash']);parser.add_argument('--base-url');parser.add_argument('--file',type=Path);args=parser.parse_args()
 if args.action=='validate':
  inventory();print('Content structure, duplicate checks and publication review gates passed.')
 elif args.action=='report':print(json.dumps(report(),ensure_ascii=False,indent=2))
 elif args.action=='build':
  require(args.base_url,'--base-url required');m=build(ROOT,args.base_url);print(f"Built {len(m['packs'])//2} bilingual packs; version {m['version'][:12]}")
 else:
  require(args.file,'--file required');data=load(args.file);print(json.dumps({q['id']:digest(q) for q in data},indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,TypeError,AssertionError) as e:print(f'Content validation failed: {e}',file=sys.stderr);sys.exit(1)
