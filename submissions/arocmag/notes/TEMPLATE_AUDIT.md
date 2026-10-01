# Official Template Audit

状态：`DOWNLOADED_AND_AUDITED`。日期：2026-10-01。审查对象为官网原始 Word 二进制文件；未改写模板，未将 K-Waay 论文转成 Word。

## File

- 原文件名：`投稿编辑模板-计算机应用研究.doc`。
- 格式：Word 97–2003 `.doc`，OLE Compound File；保持原字节与原后缀。
- 来源：https://www.arocmag.cn/download/template 。发现页面：https://www.arocmag.cn/download 及 https://www.arocmag.cn/info/instruction/template 。未使用页面中旧 `go.arocmag.com` 跳转下载。
- 页面日期：模板介绍页2024-06-26；下载列表2023/10/13 16:41:40；原件首页修改日期域缓存2021/07/27。这三个日期不混用。
- SHA-256：见下方“Integrity”，同时登记在 `SOURCE_MANIFEST.tsv`。

## Inspection Method

通过 **WPS 的 `kwps.Application` COM 接口**实际以 `ReadOnly=True` 打开原件，关闭时不保存；读取原件样式、节、对象、字段、页眉页脚和正文。COM 兼容接口自报 `Microsoft Word / 12.0`，但实际调用的是 WPS，不能据此写“已用 Microsoft Word 验证”。本环境无可用的 bundled LibreOffice，故未使用该渲染器。

原件只读导出为审查用 `snapshots/F01-render.pdf`，Poppler 渲染3页后逐页视觉查看，确认中英文首部、页脚、分栏、公式、图和表可读。未测试 MathType 软件中的双击编辑行为；已确认其对象类型及预览内容。另存 `F01-audit-copy.docx` 仅用于 XML 交叉检查，**不是官方模板，也不是后续制稿底稿**。

原件 COM 记录 `F01-original-com-audit.json` 为字段数量和样式的首要证据；转换件 `F01-xml-audit.txt` 仅作辅助。转换后部分字段被展开，因此不可只靠 DOCX 说原模板没有域。

## Structure

按阅读顺序：

1. 首页页眉：投稿、计算机应用研究、修改日期。
2. 中文标题（示例上标 `*`）。
3. 中文作者（单位上标，通信作者示例 `†`）。
4. 中文单位/部门、省市、邮编。
5. 中文摘要。
6. 中文关键词。
7. 中图分类号。
8. 英文标题。
9. 英文作者。
10. 英文单位/部门、地点、邮编、国家。
11. 英文摘要。
12. 英文关键词。
13. 连续分节进入双栏正文。模板章节依次为：0 引言；1 样式；2 章节标题、编号及列项；3 引文标注；4 分栏；5 公式；6 图；7 表；8 代码/伪代码；9 文字；10 结束语；11 致谢；12 参考文献；13 文档格式。
14. 首页页脚为基金项目、作者简介，视觉上在首页正文下方；**不是正文章节序列，也不是 Word footnote**。

模板的章节1—13大多是编写指导，不是要求研究论文采用这些章节名。第6/7/9/10/11章等有待补充标记；“MathType安装程序见第14章”在当前实际文件中没有对应第14章，未补造内容。

## Style Information

以下来自原件 COM 样式，pt 为磅；样式字号不等于所有局部字符无覆盖。完整72条以 `@` 开头的样式（含字符/CharProp变体）保存在机器记录。

| 样式/用途 | 中文字体 / 西文字体 | 大小 | 段落与备注 |
|---|---|---|---|
| 中文题目 | 黑体 / Arial | 16 pt | 居中，双倍行距，段前16 pt，左右各22.7 pt缩进 |
| 中文作者 | 宋体 / Times New Roman | 12 pt | 居中，双倍行距，单位标记上标 |
| 英文题目 | 宋体（东亚默认）/ Times New Roman | 12 pt | 居中，单倍行距，段前后各16 pt |
| 英文作者 | 宋体 / Times New Roman | 10.5 pt | 居中，单倍行距 |
| 单位单行/多行 | 楷体 / Times New Roman | 9 pt | 单行居中；多行两端对齐；左右各22.7 pt |
| 摘要与关键词文本 | 楷体 / Times New Roman | 9 pt | 两端对齐，左右各22.7 pt；中文标签黑体、英文标签加粗 |
| 一级标题 | 黑体 / Arial | 10.5 pt | 固定16 pt行距，自动编号，悬挂关系 |
| 二级标题 | 黑体 / Arial | 9 pt | 单倍行距，自动编号 |
| 三级标题 | 楷体 / Times New Roman | 9 pt | 单倍行距，自动编号 |
| 正文 | 宋体 / Times New Roman | 9 pt | 两端对齐，单倍行距，字符单位首行缩进（XML为2字符）；COM换算32.2 pt，不宜当成通用固定缩进 |
| 独行公式 | 宋体 / Times New Roman | 9 pt | 使用制表位定位公式与右侧编号 |
| 表格/图表单列标题 | 宋体 / Times New Roman | 8 pt | 居中；图题在图下，表题在表上 |
| 代码 | 宋体 / Consolas | 7.5 pt | 单倍行距，左缩进9.1 pt，正文可编辑文字 |
| 参考文献标题 | 黑体 / Arial | 10.5 pt | 固定16 pt行距；预置样式，实际第12章为规则说明 |
| 参考文献条目 | 楷体 / Times New Roman | 7.5 pt | 两端对齐，悬挂缩进2字符；COM换算32.2 pt |
| 页眉/首页页脚 | 楷体 / Times New Roman | 7.5 pt | 固定12 pt行距；“基金项目/作者简介”标签为黑体 |

公式/图/表内容实际观察：第2页两个MathType公式，编号(1)/(2)；第3页一幅EMF图，有中文和英文图题；示例表无竖线，带表头分组辅助横线，不能称为“仅三条横线”。未把模板示例补写成缺失的通用图表规则。

## Formula Handling

原件 `InlineShapes` 有3个对象：2个 `Type=1` 的嵌入对象，ProgID 均为 **Equation.DSMT4**；另1个 `Type=3` 图片。原件正文有2个 `EMBED Equation.DSMT4` 域，转换件包中对应两个 `word/embeddings/oleObject*.bin`，同时有 WMF 预览。第3个图片在转换包中为 `image3.emf`。

据此模板确实含MathType示例，不是只有“建议使用”文字。公式不是普通Word OMML；未安装或调用MathType，也未执行批量公式转换。MathType具体版本无法仅从 `DSMT4` 推断，6.9d 是模板建议版本。

网页要求 MathType；模板又说明OMML转换、AxMath转换，以及禁止公式图片化。公式变量正斜体的一般规范没有明确文字规定。

## Hidden / Special Fields

| 项目 | 原件检查结果与后续注意 |
|---|---|
| Word styles | COM 检出72个 `@` 样式，含字符变体；DOCX转换会规范化/合并名称，不能比较数量后就认定原件丢样式 |
| 主文域 | 2个EMBED公式域（Type58），不可把它们当成可随意删除的隐藏代码 |
| 页眉域 | 首页1个 `SAVEDATE \\@ "yyyy/MM/dd" \\* MERGEFORMAT`（Type22），缓存2021/07/27；未更新它 |
| 页眉/页脚 | 首页不同；首页“投稿/刊名/修改日期”，其他页“投稿/刊名/投稿”；首页页脚存基金与作者简介 |
| Textbox / floating shapes | 原件 Shapes=0，各读取 Story 中 ShapeRange=0；未见文本框，正文图为inline |
| Bookmarks | 原件14个；存在书签不等于参考文献允许书签式编码，后者官方明确不建议 |
| Comments / revisions | 均0 |
| Footnotes / endnotes | 均0；基金作者块不是脚注 |
| Section break | 3节，连续分节；第1节单栏、第2节双栏、第3节单栏（尾部空节） |
| Page setup | 595.3×841.9 pt，约A4；上56.7 pt（约20 mm），左右/下42.5 pt（约15 mm）；页眉/页脚距28.35 pt（约10 mm） |
| 双栏间距 | 第2节18.15 pt（约6.40 mm）；模板文字另表述27字符/栏、2字符栏间距；两者应结合网格理解 |
| 页面网格 | XML派生件有linesAndChars网格；不宜重建一个只抄页边距的空Word文档 |

WPS生成的检查用DOCX中未保留原件SAVEDATE域代码，而是存了显示文本；这正是后续转换必须检查域的原因。不得以审查副本取代下载原件。

## Content Conflicts and Unspecified Items

- 中文摘要：模板200字以内，摘要专页200～300字，`NEEDS_CONFIRMATION`。
- 模板首页页脚是实际作者/基金字段来源，单读 `Document.Content.Text` 会漏掉它们；本次补读 StoryRanges 并查阅首页图像。
- 模板无总字数/页数上限、图像DPI、全面变量正斜体规则、ORCID、附录/补充材料政策。
- 图表章节仍未写完整说明；双语题注与三线表式结构仅作为实际模板示例。
- 版权表是 `.dotx`，不是`.docx`；原格式保留。

## Integrity

完整散列由资料索引脚本附于此节；下载原件会在交付前与下载时散列再次比对。

<!-- GENERATED HASH -->

F01 SHA-256：`baf9fce8b2bc56f2320c8bf4541546e43f48a8f3a1c773b40667d7b2a7b872cb`。
