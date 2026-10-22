#!/usr/bin/env python3
"""Bounded, rate-limited source reachability report; not factual approval.
404/410 fail the check. Throttling, bot blocks and timeouts require review;
they never promote an unreviewed question or prove a factual claim.
"""
import argparse,json,subprocess,time
from pathlib import Path
import content

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=content.ROOT/'link-report.json');a=p.parse_args()
 _,items,_,_=content.inventory();urls=sorted({u for stage,q in items if stage=='questions' for u in q['sources']});rows=[]
 for url in urls:
  r=subprocess.run(['curl','--silent','--show-error','--location','--max-redirs','3','--max-time','15','--range','0-65535','--max-filesize','2097152','--output','/dev/null','--write-out','%{http_code}',url],capture_output=True,text=True)
  code=int(r.stdout) if r.stdout.isdecimal() else 0
  rows.append(dict(url=url,httpStatus=code,reachable=r.returncode==0 and 200<=code<400,needsManualCheck=r.returncode!=0 or not 200<=code<400))
  time.sleep(.5)
 report=dict(checkedAt=time.strftime('%Y-%m-%d',time.gmtime()),sourceCount=len(rows),reachable=sum(r['reachable'] for r in rows),factApproval=False,checks=rows)
 a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(f"Source links reachable: {report['reachable']}/{len(rows)}; see report for blocked/transient responses.")
 return 1 if any(r['httpStatus'] in (404,410) for r in rows) else 0
if __name__=='__main__':raise SystemExit(main())
