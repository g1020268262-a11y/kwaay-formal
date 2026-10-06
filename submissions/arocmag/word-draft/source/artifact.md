# Official template execution contract

## Reference

- Original retained template: `D:\kwaay-formal\submissions\arocmag\official\templates\投稿编辑模板-计算机应用研究.doc`
- Original SHA-256: `baf9fce8b2bc56f2320c8bf4541546e43f48a8f3a1c773b40667d7b2a7b872cb`
- Byte-identical working copy: `official-template-original.doc`
- WPS-converted DOCX base: `official-template-converted.docx`
- Reference render: `../qa/template-reference/page-1.png` through `page-3.png`
- Original/conversion page count: 3; section count: 3.
- Package inventory: `template-package-inventory.tsv`.
- Conversion authority: the official `.doc` remains authoritative; the DOCX is only the editable work base.

## Page system

- A4 portrait: 595.3 pt × 841.9 pt.
- Margins: top 56.7 pt; bottom, left and right 42.5 pt.
- Header/footer distance: approximately 28.35 pt.
- Section 1: continuous, one column, different first page enabled.
- Section 2: continuous, two columns, 18.15 pt column spacing.
- Section 3: continuous, one column, empty tail section in the reference.
- Header: three-part line with 投稿 / 计算机应用研究 / 投稿; first page right field is 修改日期.
- First-page footer retains fund and author-biography areas.

## Typography and paragraph roles

| Role | Template style | Required formatting |
|---|---|---|
| Chinese title | `@头部\|标题\|中文` | 黑体/Arial, 16 pt, centered, fixed 24 pt line, 22.7 pt side indents |
| Chinese author | `@头部\|作者\|中文` | 宋体/Times New Roman, 12 pt, centered, fixed 24 pt line |
| Institution | `@头部\|机构\|多行` | 楷体/Times New Roman, 9 pt, justified, fixed 12 pt line |
| Abstract/keywords/classification | `@头部\|摘要\|文本` | 楷体/Times New Roman, 9 pt, justified, fixed 12 pt line |
| English title | `@头部\|标题\|英文` | Times New Roman/宋体, 12 pt, centered |
| English author | `@头部\|作者\|英文` | Times New Roman/宋体, 10.5 pt, centered |
| Level-1 heading | `@正文\|标题1` | 黑体/Arial, 10.5 pt, fixed 16 pt, keep with next, automatic numbering |
| Level-2 heading | `@正文\|标题2` | 黑体/Arial, 9 pt, single/fixed 12 pt, keep with next, automatic numbering |
| Level-3 heading | `@正文\|标题3` | 楷体/Times New Roman, 9 pt, single/fixed 12 pt, keep with next |
| Body paragraph | `@正文\|段落文本` | 宋体/Times New Roman, 9 pt, justified, two-character first-line indent, fixed 12 pt |
| Display equation | `@正文\|独行公式` | 宋体/Times New Roman, 9 pt, tab-based equation and right-side number |
| Figure caption | `@正文\|图表\|1列` | 宋体/Times New Roman, 8 pt, centered, fixed 12 pt |
| Table content/caption | `@正文\|表格` | 宋体/Times New Roman, 8 pt, centered, fixed 12 pt |
| Reference heading | `@正文\|标题参考文献` | 黑体/Arial, 10.5 pt, fixed 16 pt, keep with next |
| Reference entry | `@正文\|参考文献` | 楷体/Times New Roman, 7.5 pt, justified, 2-character hanging indent |

## Components and slot map

1. Chinese title: replace the sample title in place.
2. Chinese authors: retain the slot and fill with a conspicuous待补占位 because no author data were supplied.
3. Chinese institution: retain and fill with a待补占位.
4. Chinese abstract, keywords and classification number: fill from the Chinese draft; classification number remains待确认.
5. English title: fill from the bilingual abstract source.
6. English authors and institution: retain as待补占位.
7. English abstract and key words: fill from the bilingual abstract source.
8. Body: replace all instructional sample content with sections 0–6, figures, tables and references; use the reference’s two-column section.
9. First-page footer: keep fund and biography fields and replace sample facts with待补占位 text.
10. Final single-column tail section: preserve only if needed for section/header stability; it must not create an extra blank page.

## Tables and figures

- Tables use no vertical borders, top/header/bottom horizontal rules, 8 pt text, and bilingual captions above.
- Figure images are inline, centered, followed immediately by Chinese and English captions.
- Figure 1 and Figure 2 use task-generated SVG as the editable vector source. Word insertion may use SVG directly when WPS accepts it; otherwise use a high-resolution PNG while retaining the SVG source and reporting the limitation.

## Equations

- The official template contains two `Equation.DSMT4` MathType examples and explicitly allows OMML as an intermediate that can later be batch-converted with MathType.
- The manuscript will use editable OMML, never formula screenshots.
- Raw LaTeX is retained only in the task’s `source/formulas.json` and must not remain visible in the Word manuscript.
- Because MathType is not installed, the final report must state that genuine MathType conversion is incomplete unless a MathType object can be verified.

## Package preservation

- Preserve `styles.xml`, `numbering.xml`, theme, settings, header/footer parts and template-derived page geometry.
- Removing sample text, example OLE equations, example image and example table is intentional.
- Opaque example OLE/media parts may become orphaned after body replacement; they must not appear in the final document.
- The official `.doc` and its byte-identical working copy must remain unchanged.

## Fidelity gates

- Final document retains A4 geometry, first-page single-column front matter, two-column body, header, first-page footer, official styles and numbering behavior.
- No instructional template prose remains.
- Every page is rendered to PNG from the final DOCX/PDF and inspected for clipping, overlap, missing glyphs, broken equations, broken tables, misplaced figures, large unexplained whitespace and orphan headings.
- Final PDF page count equals the number of reviewed PNG pages.
