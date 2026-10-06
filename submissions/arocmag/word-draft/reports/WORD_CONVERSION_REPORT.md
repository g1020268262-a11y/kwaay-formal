# Word 转换报告

## 交付物

- `manuscript/kwaay-arocmag-draft.docx`
- `manuscript/kwaay-arocmag-review.pdf`
- `figures/figure-1.emf`、`figure-2.emf` 及对应 SVG/PNG 源
- `references/citation-order.tsv`、`citation-order.json`
- `source/formulas.json`、中文稿源文件副本和可回放构建脚本

## 模板与转换

稿件从官方模板 `投稿编辑模板-计算机应用研究.doc` 建立。官方文件和只读副本的 SHA-256 均为：

`baf9fce8b2bc56f2320c8bf4541546e43f48a8f3a1c773b40667d7b2a7b872cb`

官方 `.doc` 先由 WPS 转换为 `source/official-template-converted.docx`，正文生成继续使用模板中的版心、样式、编号、双栏和题注格式。标准 `render_docx.py` 路径因当前 Windows 环境没有 LibreOffice `soffice.exe` 而无法执行；最终采用 WPS 原生 PDF 导出，并用 Poppler 以 150 dpi 渲染全部页面审查。

## 内容结构审计

- A4，9 页，8 个连续分节。
- 7 个一级章节（0 引言至 6 结束语），22 个二级标题。
- 27 个编号行间公式，153 个行内公式源片段，最终共 197 个可编辑 OMML 对象。
- 2 幅 EMF 矢量图。
- 3 张原生 Word 表格，行数分别为 7、4、15；表 3 含表头及 14 项验证结果。
- 19 条参考文献，按正文首次引用顺序排列。
- OOXML 中无 `\cite`、`$$`、`**`、`[[FIGURE_...]]` 或 `$...$` 残留。
- WPS 复核：9 页、3 表、2 个 InlineShape、197 个 OMath、8 个分节。

最终文件 SHA-256：

- DOCX：`a328ea4775287b64151362fe6db32770ec9e45addca2e6c63ca8a88e101bb57f`
- PDF：`c30ac2e74dd8f2cd0b47cb625d22f5ffe02b765c2e410ff31644513970883b1b`

## 未完成项

1. 当前环境没有可复核的 MathType 批量转换接口，公式以可编辑 OMML 交付；投稿前仍需按编辑部要求完成 MathType 转换。
2. 作者、单位、基金、作者简介及通信作者信息待作者补充并核验。
3. 14 条会议论文、技术报告或在线规范的出版地、出版者或载体细节待按编辑部采用的 GB/T 7714 口径核验；稿件未猜测缺失字段。

## 状态

`AROCMAG_WORD_DRAFT_INCOMPLETE`
