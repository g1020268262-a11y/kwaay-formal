"""Read-only scientific-content and artifact checks; never invokes Tamarin."""
import csv,hashlib,json,re,unicodedata,zipfile
from collections import Counter
from pathlib import Path
from lxml import etree
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[4]
WROOT=ROOT/'submissions/arocmag/word-final';LROOT=ROOT/'submissions/arocmag/latex-v2';QA=WROOT/'qa/stage6'
BASE=WROOT/'stage5-submission-package/K-Waay-AROCMAG-submission-stage5-author-confirmation.docx'
FINAL=WROOT/'K-Waay-AROCMAG-submission-stage6.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def package(p):
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  return {n:z.read(n) for n in z.namelist()}
def txt(x):return ''.join(x.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS))
def norm(s):return re.sub(r'[\s\u200b\u00ad]','',unicodedata.normalize('NFKC',s))
def han(s):return ''.join(re.findall(r'[\u4e00-\u9fff]',s))
base,new=package(BASE),package(FINAL)
old=etree.fromstring(base['word/document.xml']);doc=etree.fromstring(new['word/document.xml'])
body=doc.find('w:body',NS)
pars=body.findall('w:p',NS);oldpars=old.find('w:body',NS).findall('w:p',NS)
check={}
check['package_parts_unchanged_except_body_metadata']=sorted(n for n in base if base[n]!=new[n])==['docProps/core.xml','word/document.xml'] and set(base)==set(new)
check['old_four_tables_preserved']=all(any(etree.tostring(t)==etree.tostring(n) for n in body.findall('w:tbl',NS)) for t in old.xpath('.//w:body/w:tbl',namespaces=NS))
def style(p):return p.xpath('string(./w:pPr/w:pStyle/@w:val)',namespaces=NS)
oldformula=[p for p in oldpars if style(p)=='74']
formulas=[p for p in pars if style(p)=='74']
check['six_old_display_formulas_preserved']=len(oldformula)==6 and all(any(etree.tostring(p)==etree.tostring(n) for n in formulas) for p in oldformula)
check['seven_displays']=len(formulas)==7
check['eight_references_unchanged']=[txt(p) for p in oldpars if style(p)=='84']==[txt(p) for p in pars if style(p)=='84']
check['six_chapters_13_subsections']=[sum(style(p)==st for p in pars) for st in ['65','66']]==[6,13]
check['rq_text_unchanged']=[txt(p) for p in oldpars if txt(p).startswith(('RQ1','RQ2','RQ3'))]==[txt(p) for p in pars if txt(p).startswith(('RQ1','RQ2','RQ3'))]
check['abstract_discussion_conclusion_sources_unchanged']=all((QA/('baseline-'+f)).read_bytes()==(LROOT/'sections'/f).read_bytes() for f in ['00-abstract.tex','05-discussion.tex','06-conclusion.tex'])
old_body_text=[txt(p) for p in oldpars]
check['front_matter_unchanged']=[txt(p) for p in pars[:13]]==old_body_text[:13]
check['figures_unchanged']=all(new[n]==base[n] for n in base if n.startswith('word/media/')) and len(doc.xpath('.//w:drawing',namespaces=NS))==2
allhan='\n'.join(han(txt(p)) for p in pars)
coverage=[]
for path in sorted((LROOT/'sections').glob('*.tex')):
 if path.name=='00-abstract.tex':continue
 src=path.read_text(encoding='utf-8')
 src=re.sub(r'\%[^\n]*','',src)
 src=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}','',src,flags=re.S)
 src=re.sub(r'\\begin\{equation\}.*?\\end\{equation\}|\\\[.*?\\\]','',src,flags=re.S)
 src=re.sub(r'\\(?:begin|end)\{enumerate\}(?:\[[^\]]*\])?','',src)
 src=src.replace('\\item','\n\n')
 for part in re.split(r'\n\s*\n',src):
  h=han(part)
  if h:coverage.append({'source':path.name,'text':h,'present':h in allhan})
check['all_scientific_prose_chinese_sequence_covered']=all(x['present'] for x in coverage)
bindings=json.loads((QA/'result-bindings.json').read_text(encoding='utf-8'))
actual=body.findall('w:tbl',NS)[-1]
result_rows=[[norm(txt(c)) for c in row.findall('w:tc',NS)] for row in actual.findall('w:tr',NS)][1:]
status_matches=[]
for row,record in zip(result_rows,bindings):
 stdout=(ROOT/'reviews/2026-09-16-evidence'/f"{record['model']}-prove.stdout.txt").read_text(encoding='utf-8')
 pattern=re.escape(record['lemma'])+r' \('+re.escape(record['type'])+r'\): '+record['status']+r'(?: - found trace)? \('+record['steps']+r' steps\)'
 status_matches.append(bool(re.search(pattern,stdout)) and row[1:5]==[record['lemma'],record['type'],record['status'],record['steps']])
check['all14_rows_bound_to_independent_stdout']=len(result_rows)==14 and all(status_matches)
check['13_verified_1_falsified']=Counter(row[3] for row in result_rows)=={'verified':13,'falsified':1}
newformula=[p for p in formulas if not any(etree.tostring(p)==etree.tostring(o) for o in oldformula)][0]
expected='Send(A,oid₁,m₁)@s₁,Send(A,oid₂,m₂)@s₂,oid₁≠oid₂,m₁≠m₂,A₁=A₂=A,BatchReceive(bid,rst)@b,ReceiverAccept(A,oid₁,m₁,bid,rst)@r₁,ReceiverAccept(A,oid₂,m₂,bid,rst)@r₂,s₁<b,s₂<b,b<r₁<r₂.'
check['M_witness_full_event_formula']=norm(txt(newformula))==norm(expected)
baseline=json.loads((QA/'baseline.json').read_text(encoding='utf-8'))
changed=[p for p,h in baseline['protected_sha256'].items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
check['protected_inputs_unchanged']=not changed
logpath=LROOT/'main.log'
if not logpath.exists():logpath=QA/'latex-compile.log'
log=logpath.read_text(encoding='utf-8',errors='replace')
compileqa={name:len(re.findall(pattern,log,re.I)) for name,pattern in {'undefined_references':r'Reference .+ undefined','undefined_citations':r'Citation .+ undefined','missing_glyphs':r'Missing character','overfull_boxes':r'Overfull \\[hv]box','underfull_boxes':r'Underfull \\[hv]box'}.items()}
check['latex_compile_qa']=all(compileqa[k]==0 for k in ['undefined_references','undefined_citations','missing_glyphs','overfull_boxes'])
pages={}
for label,path in [('word',WROOT/'K-Waay-AROCMAG-submission-stage6-preview.pdf'),('latex',LROOT/'main.pdf')]:
 pdf=pdfium.PdfDocument(str(path));pages[label]=len(pdf)
 folder=QA/(label+'-render');folder.mkdir(exist_ok=True)
 texts=[]
 for i,page in enumerate(pdf):
  page.render(scale=1.7).to_pil().save(folder/f'page-{i+1}.png')
  texts.append(page.get_textpage().get_text_range())
 (QA/(label+'-extracted.txt')).write_text('\n\n'.join(f'PAGE {i+1}\n'+t for i,t in enumerate(texts)),encoding='utf-8')
 if label=='word':check['complete14_table_on_one_page']=any(all(r['lemma'] in norm(t) for r in bindings) for t in texts)
formula_list=[]
for i,m in enumerate(doc.xpath('.//m:oMath',namespaces=NS),1):formula_list.append([i,txt(m),'OMML','MathType pending'])
with (QA/'FORMULA_CHECKLIST_STAGE6.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['index','visible_math','format','external_status']);writer.writerows(formula_list)
report={'checks':check,'all_pass':all(check.values()),'pages':pages,'OMML':len(formula_list),'tables':6,'figures':2,'display_formulas':7,'numbered_formulas':3,'references':8,'protected_files':len(baseline['protected_sha256']),'changed_protected':changed,'compile':compileqa,'prose_paragraphs_checked':len(coverage),'missing_prose':[x for x in coverage if not x['present']],'new_M_formula':txt(newformula),'expected_M_formula':expected,'visual_review':'separate human-visible page-image review required; automatic pass is not visual acceptance'}
(QA/'content-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'prose-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
