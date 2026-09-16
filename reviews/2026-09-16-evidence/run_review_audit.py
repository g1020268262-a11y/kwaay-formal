from pathlib import Path
import subprocess, hashlib, json, datetime, time

ROOT = Path(r'D:\kwaay-formal')
OUT = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()
base = ['wsl', '-d', 'Ubuntu-24.04', '--cd', '/mnt/d/kwaay-formal', '--', 'env', 'PATH=/home/linuxbrew/.linuxbrew/bin:/usr/bin:/bin', '/home/linuxbrew/.linuxbrew/bin/tamarin-prover']
record = {'audit_kind':'independent-review-rerun; not recovery of original run', 'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'commit':git('rev-parse','HEAD'), 'branch':git('branch','--show-current'), 'pre_status':git('status','--porcelain=v1'), 'runner_sha256':sha(Path(__file__)), 'runs':[]}
for name,args in [('version',['--version'])] + [(variant+'-'+mode, [flag,'tamarin/rq-v2-minimal/'+variant+'.spthy'] + (['--output-json=/mnt/c/Users/10202/.codex/visualizations/2026/09/16/01a0a96b-d0fd-72f0-adcd-7cd964edcdf4/review-evidence/'+variant+'-traces.json'] if mode=='prove' else [])) for variant in ['rqv2_relaxed','rqv2_message_dedup','rqv2_party_admission'] for mode,flag in [('parse','--parse-only'),('prove','--prove')]]:
    cmd=base+args
    item={'id':name,'command':cmd}
    model=next((a for a in args if a.endswith('.spthy')),None)
    if model: item['model_sha256']=sha(ROOT/model)
    t=time.monotonic()
    with (OUT/(name+'.stdout.txt')).open('wb') as so, (OUT/(name+'.stderr.txt')).open('wb') as se:
        try:
            result=subprocess.run(cmd,stdout=so,stderr=se,timeout=180)
            item['exit_code']=result.returncode
        except subprocess.TimeoutExpired:
            item['timeout_seconds']=180
    item['elapsed_seconds']=round(time.monotonic()-t,3)
    item['stdout_sha256']=sha(OUT/(name+'.stdout.txt'))
    item['stderr_sha256']=sha(OUT/(name+'.stderr.txt'))
    record['runs'].append(item)
    (OUT/'independent-rerun-manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name, item.get('exit_code','TIMEOUT'), item['elapsed_seconds'],flush=True)
record['post_status']=git('status','--porcelain=v1')
record['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(OUT/'independent-rerun-manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
