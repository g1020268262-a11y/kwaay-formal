"""Stage 6 scientific synchronization, preserving Stage 5 package furniture."""
from pathlib import Path
import copy, importlib.util, json, re, zipfile
from lxml import etree

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stage4',HERE/'build_word_stage4.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
BASE=s.OUT/'stage5-submission-package/K-Waay-AROCMAG-submission-stage5-author-confirmation.docx'
FINAL=s.OUT/'K-Waay-AROCMAG-submission-stage6.docx'
QA=s.OUT/'qa/stage6'
s.BASE_DOCX=BASE;s.FINAL_DOCX=FINAL
s.TABLES.update(json.loads((HERE/'stage6-evidence-tables.json').read_text(encoding='utf-8')))
s.TABLES['full-verification-results']['widths']=[0.9,5.85,2.0,1.4,0.95,4.7]
original_add_table=s.add_table_block
def add_table(doc,name,cite_map):
 original_add_table(doc,name,cite_map)
 if name=='full-verification-results':
  for p in doc.paragraphs:
   if p.text==s.TABLES[name]['caption']:p.paragraph_format.page_break_before=True
  # Keep the compact 14-result checklist on one page without shrinking it.
  for row in doc.tables[-1].rows[:-1]:
   for cell in row.cells:
    for p in cell.paragraphs:p.paragraph_format.keep_with_next=True
s.add_table_block=add_table
for name,num in [('identity-coordinate-map',1),('source-to-abstraction',2),('admission-configurations',3),('verification-property-semantics',4),('key-verification-results',5),('full-verification-results',6)]:
 s.REF_MAP['tab:'+name]=str(num)
 s.TABLES[name]['caption']=re.sub(r'^表 \d+',f'表 {num}',s.TABLES[name]['caption'])
# Existing frozen 360dpi assets: no new rasterization or figure design.
s.render_figure_pdf=lambda number:s.FIGURES/f'fig{number}-word-stage4.png'
# Remove the Stage 4 six-page-specific forced reference column break.
def refs(doc,order,bib):
 heading=doc.add_paragraph(style=s.h.style_by_id(doc,'82'))
 heading.paragraph_format.keep_with_next=True
 s.h.add_text_run(heading,'参考文献',bold=True,size=10.5)
 records=[]
 for number,key in enumerate(order,1):
  if number==4:
   p=doc.add_paragraph(style=s.h.style_by_id(doc,'71'))
   p.paragraph_format.space_before=p.paragraph_format.space_after=s.Pt(0)
   p.add_run().add_break(s.WD_BREAK.COLUMN)
  v=s.REFERENCE_OVERRIDES[key]
  p=doc.add_paragraph(style=s.h.style_by_id(doc,'84'))
  p.alignment=s.WD_ALIGN_PARAGRAPH.LEFT
  p.paragraph_format.left_indent=s.Pt(18);p.paragraph_format.first_line_indent=s.Pt(-18)
  p.paragraph_format.space_before=p.paragraph_format.space_after=s.Pt(0)
  p.paragraph_format.line_spacing_rule=s.WD_LINE_SPACING.EXACTLY;p.paragraph_format.line_spacing=s.Pt(9.5)
  s.h.add_text_run(p,v['reference'],size=8)
  records.append(dict(number=number,key=key,reference=f'[{number}] '+v['reference'],verified_source=v['source']))
 return records
s.add_references=refs
def records(order,references,formulas):
 (s.FORMULAS/'formulas-stage6.json').write_text(json.dumps(formulas,ensure_ascii=False,indent=2),encoding='utf-8')
 (HERE/'citation-order-stage6.json').write_text(json.dumps(references,ensure_ascii=False,indent=2),encoding='utf-8')
s.write_source_records=records
s.build()

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
ns={'w':W,'r':R,'m':M}
def text(el):return ''.join(el.xpath('.//w:t/text()|.//m:t/text()',namespaces=ns))
with zipfile.ZipFile(BASE) as z: base={i.filename:z.read(i.filename) for i in z.infolist()}
with zipfile.ZipFile(FINAL) as z: new={i.filename:z.read(i.filename) for i in z.infolist()}
oldroot=etree.fromstring(base['word/document.xml']); root=etree.fromstring(new['word/document.xml'])
oldbody=oldroot.find('w:body',ns); body=root.find('w:body',ns)
# Reuse the original first-section header/footer references; later sections
# inherit them. The helper's newly allocated duplicate stories are discarded.
original_sections=oldroot.xpath('.//w:sectPr',namespaces=ns)
new_sections=root.xpath('.//w:sectPr',namespaces=ns)
for sect in new_sections:
 for child in list(sect):
  if child.tag in ('{'+W+'}headerReference','{'+W+'}footerReference'):sect.remove(child)
for child in original_sections[0]:
 if child.tag in ('{'+W+'}headerReference','{'+W+'}footerReference'):new_sections[0].insert(0,copy.deepcopy(child))
# Reuse unchanged source paragraphs/tables, retaining original run and math objects.
lookup={}
for el in oldbody:
 if text(el) and not el.xpath('.//w:sectPr',namespaces=ns):lookup.setdefault((el.tag,text(el)),[]).append(el)
reused=0
for el in list(body):
 candidates=lookup.get((el.tag,text(el)),[])
 if candidates and not el.xpath('.//w:sectPr',namespaces=ns):
  body.replace(el,copy.deepcopy(candidates.pop(0)));reused+=1
# All existing media/furniture relationships must remain valid in the patched body.
def relmap(data):
 t=etree.fromstring(data)
 return {el.get('Id'):(el.get('Type'),el.get('Target'),el.get('TargetMode')) for el in t}
oldrels=relmap(base['word/_rels/document.xml.rels']);newrels=relmap(new['word/_rels/document.xml.rels'])
for el in root.iter():
 for a,v in el.attrib.items():
  if a.startswith('{'+R+'}'):
   if oldrels.get(v)!=newrels.get(v):
    matches=[k for k,val in oldrels.items() if val==newrels.get(v)]
    if not matches:raise RuntimeError('New unsupported relationship: '+v)
    el.set(a,matches[0])
# Preserve every Stage 5 package part except body and provenance metadata.
core=etree.fromstring(base['docProps/core.xml'])
for el in core:
 if el.tag.endswith('}subject'):el.text='AROCMAG Stage 6 contribution-restoration manuscript'
 if el.tag.endswith('}description'):el.text='Scientific source synchronized with reviewed Stage 6 LaTeX; author details and MathType remain pending.'
base['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
base['docProps/core.xml']=etree.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(FINAL,'w',zipfile.ZIP_DEFLATED) as z:
 for name,data in base.items():z.writestr(name,data)
manifest={'stage5_sha256':s.sha256(BASE),'stage6_sha256':s.sha256(FINAL),'reused_unchanged_body_blocks':reused,'changed_package_parts':['word/document.xml','docProps/core.xml'],'unchanged_parts':len(base)-2,'tables':6,'figures':2,'source_hashes':{str(p.relative_to(s.ROOT)).replace('\\','/'):s.sha256(p) for p in sorted((s.LATEX/'sections').glob('*.tex'))}}
(QA/'build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
