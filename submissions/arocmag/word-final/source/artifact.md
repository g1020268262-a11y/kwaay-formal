# Official template execution contract

## Reference

- Authoritative template: `D:/kwaay-formal/submissions/arocmag/official/templates/投稿编辑模板-计算机应用研究.doc`
- Authoritative template SHA-256: `BAF9FCE8B2BC56F2320C8BF4541546E43F48A8F3A1C773B40667D7B2A7B872CB`
- Editable conversion base: `official-template-converted.docx`
- The conversion base was produced from a byte-identical copy of the authoritative `.doc`; the `.doc` remains unchanged.
- Reference render inspected: three pages, covering first-page metadata, two-column body, equations, figures, tables, references, headers and footers.

## Page system

- A4 portrait, 21.0 cm × 29.7 cm.
- Top margin 2.0 cm; bottom, left and right margins 1.5 cm.
- Header and footer distances approximately 0.7 cm.
- Front matter uses one column; the body uses two columns with approximately 0.64 cm spacing.
- Wide editable tables use temporary continuous one-column sections, followed by a continuous return to two columns.
- The first page uses a distinct header/footer. Later sections link to the preceding header/footer.

## Typography

| Role | Official style | Formatting used |
|---|---|---|
| Chinese title | `@头部|标题|中文` | 黑体/Arial, 16 pt, centered |
| Chinese author | `@头部|作者|中文` | 宋体/Times New Roman, 12 pt, centered |
| Institution | `@头部|机构|多行` | 楷体/Times New Roman, 9 pt, centered/justified |
| Abstract and keywords | `@头部|摘要|文本` | 楷体/Times New Roman, 9 pt, justified, fixed 12 pt line |
| English title | `@头部|标题|英文` | Times New Roman, 12 pt, centered |
| English author | `@头部|作者|英文` | Times New Roman, 10.5 pt, centered |
| Level-1 heading | `@正文|标题1` | 黑体/Arial, 10.5 pt, automatic official numbering |
| Level-2 heading | `@正文|标题2` | 黑体/Arial, 9 pt, automatic official numbering |
| Body | `@正文|段落文本` | 宋体/Times New Roman, 9 pt, justified, two-character first-line indent, fixed 12 pt line |
| Display equation | `@正文|独行公式` | Cambria Math/宋体, 9 pt, editable OMML, right-side number |
| Figure/table caption | `@正文|图表|1列` | 宋体/Times New Roman, 8 pt, centered |
| Reference heading | `@正文|标题参考文献` | 黑体/Arial, 10.5 pt |
| Reference entry | `@正文|参考文献` | 楷体/Times New Roman, 7.5 pt, hanging indent |

## Slot map

1. Chinese and English titles: exact frozen values.
2. Chinese/English author and institution slots: explicit pending placeholders only.
3. Chinese/English abstracts and keywords: exact text from `latex-v2/sections/00-abstract.tex`.
4. Classification, document code and article-number slots: pending placeholders.
5. Body: sections 0–5 and all second-level headings from the frozen LaTeX source.
6. Equations: three numbered and two unnumbered displays as editable OMML; inline mathematics is also OMML.
7. Tables: four native Word tables with no vertical rules and editable text.
8. Figures: current frozen preview PDFs retained as vector sources; Stage 1 inserts 360 dpi inline PNG placeholders with editable Word captions.
9. References: eight cited entries in first-citation order from the frozen BibTeX database.
10. First-page footer: fund, author biography and correspondence fields remain explicit pending placeholders.

## Fidelity gates

- The official `.doc` hash remains unchanged.
- No sample instructions, sample authors, sample figures, sample tables or example equations remain.
- No real author, institution, email, fund or receipt-date information is invented.
- Every rendered page must be inspected for clipping, overlap, missing glyphs, broken formulas, broken tables, duplicate captions and unreadable figures.
- Scientific text, four tables, three numbered formulas, two figures and eight references must remain traceable to the frozen LaTeX source.

