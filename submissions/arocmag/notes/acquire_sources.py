import urllib.request, urllib.parse, pathlib, json, hashlib, re, datetime, csv, sys
from lxml import html
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[1]
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
DB=ROOT/'notes/source_records.json'
records=json.loads(DB.read_text('utf-8')) if DB.exists() else []
def save(url, sid, category='page'):
    old=next((r for r in records if r['source_id']==sid),None)
    if old: return old
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=60) as r:
        data=r.read(); headers=dict(r.headers); final=r.url
    if category=='page':
        p=ROOT/'snapshots'/f'{sid}.html'; p.write_bytes(data)
        tree=html.fromstring(data.decode('utf-8-sig'))
        for e in tree.xpath('//script|//style'): e.drop_tree()
        title=' '.join(tree.xpath('//title/text()'))
        lines=[re.sub(r'\s+',' ',s).strip() for s in tree.xpath('//body//text()') if s.strip()]
        content='\n'.join(lines)
        links=[{'text':a.text_content().strip(),'url':urllib.parse.urljoin(final,a.get('href'))} for a in tree.xpath('//a[@href]')]
        dates=re.findall(r'20\d{2}[-/]\d{1,2}[-/]\d{1,2}(?: \d{1,2}:\d{2}:\d{2})?',content)
        txt=ROOT/'snapshots'/f'{sid}.txt'
        txt.write_text(f'Title: {title}\nURL: {url}\nAccessed: {NOW}\n\n{content}\n\nLINKS\n'+json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
        filename=''; updated='; '.join(dict.fromkeys(dates)) or 'NOT OFFICIALLY SPECIFIED'
    else:
        disposition=headers.get('Content-Disposition','')
        match=re.search(r"filename\*=UTF-8''([^;]+)",disposition,re.I)
        filename=urllib.parse.unquote(match.group(1)) if match else ''
        if not filename:
            match=re.search(r'filename="?([^";]+)',disposition)
            filename=match.group(1) if match else url.rsplit('/',1)[-1]
        p=ROOT/'official'/category/filename
        if p.exists(): raise RuntimeError('Collision: '+str(p))
        p.write_bytes(data); title=filename; updated='NOT OFFICIALLY SPECIFIED'; links=[]
    rec=dict(source_id=sid,title=title,official_url=url,final_url=final,page_updated_date=updated,accessed_date=NOW,source_type=category,download_filename=filename,local_path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),headers=headers,links=links)
    records.append(rec); DB.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(sid,title,len(data),rec['local_path'])
    return rec
if __name__=='__main__':
    if len(sys.argv)>1:
        save(sys.argv[2],sys.argv[1],sys.argv[3] if len(sys.argv)>3 else 'page')
    else:
        for sid,path in [('P01','info/instruction/instructions'),('P02','info/instruction/template'),('P03','download'),('P04','info/instruction/abstract-instruction'),('P05','info/instruction/faq'),('P06',''),('P07','info/instruction/procedure'),('P08','info/instruction/clc')]:
            save('https://www.arocmag.cn/'+path,sid)
        for sid,name,cat in [('F01','template','templates'),('F02','cite-regulations','guidelines'),('F03','cite-tutorial','guidelines'),('F04','agreement','forms'),('F05','requisition','forms')]:
            save('https://www.arocmag.cn/download/'+name,sid,cat)
