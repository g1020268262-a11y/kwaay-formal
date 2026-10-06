# WORD REPAIR REPORT

**状态：AROCMAG_WORD_REPAIR_INCOMPLETE**

## 1. 页眉修复情况

- 已从 SHA-256 为 `baf9fce8b2bc56f2320c8bf4541546e43f48a8f3a1c773b40667d7b2a7b872cb` 的官方模板恢复真实 Word header story，而非正文伪造文本。
- 首页启用 `different first page`，首页页眉为“投稿 / 计算机应用研究 / 修改日期：2026/10/06”；默认页眉为“投稿 / 计算机应用研究 / 投稿”。
- 官方页眉横线、制表位、字体、字号和段落格式随 header XML 一并复制。
- 第 1 节持有独立的首页与默认页眉；第 2～8 节均为连续分节，关闭各自的 `different first page`，页眉和页脚均链接到第 1 节。9 页渲染中页眉连续且未因单栏转双栏或通栏表格消失。

## 2. 首页页脚修复情况

- 已删除中文单位与摘要之间的普通正文占位段落。
- 首页 first-page footer story 已恢复官方横线和字体/段落格式，内容为：
  - 基金项目：待作者确认
  - 作者简介：待作者确认
  - 通信作者及电子邮箱：待作者确认
- 该区域是首页页脚，不是脚注；后续页未重复显示这些占位。

## 3. 中图分类号栏情况

- 已在中文关键词后加入“中图分类号：待确认”。未擅自填写分类号。

## 4. 英文单位栏情况

- 已在英文作者后加入 `(Department / Institution / City / Postal Code / China — to be completed and verified)`。
- 首页顺序已核对为：中文题目、中文作者、中文单位、中文摘要、中文关键词、中图分类号、英文题目、英文作者、英文单位、英文摘要、英文关键词、双栏正文。

## 5. 19 条参考文献转换结果

- 19 条参考文献均已按期刊附件转换：外文作者姓在前、名字首字母大写且无点，超过三人列前三人后加 `et al`；题名改为句首大写并保留专名/缩略语；会议文献采用 `[C]// Proc of ... 出版地: 出版者, 年: 页码`。
- USENIX 会议出版地按 USENIX Association 所在地 Berkeley 著录，未使用 Philadelphia、Anaheim 等会议举办地；SciTePress 使用 Setúbal；ACM 使用 New York；Springer LNCS 使用 Berlin。
- 正文引用顺序和 19 个 BibTeX key 未改变；映射已同步写入 `references/citation-order.tsv` 与 `references/citation-order.json`。
- 逐条来源与最终格式见 `REFERENCE_AUDIT_V2.md`。

## 6. 仍然 NEEDS_CONFIRMATION 的参考文献

- `[14] unger2015sok`：作者、题名、会议、年份、页码、DOI 和出版者已由 IEEE/Crossref 确认；会议录出版地未在直接出版项中找到，按规则写为 `[S. l. ]`。
- `[18] thomson2021uks`：标准号、题名、作者、日期、DOI、URL 和 RFC Editor 已确认；在线标准未给出可直接采用的出版地，按规则写为 `[S. l. ]`。
- 其余 17 条标记为完全确认。由于仍有两项出版地待确认，总体状态不能标记为就绪。

## 7. MathType 转换真实状态

- `MATH_TYPE_CONVERSION_BLOCKED`。
- 常见安装目录、ProgramData、用户 AppData、卸载注册表、Word Add-ins 注册表、命令入口和相关进程均未发现 MathType、Design Science 或 WIRIS。
- 未伪造 MathType/OLE 对象，未把公式转成图片。详细记录见 `FORMULA_AUDIT_V2.md`。

## 8. OMML 对象数量

- v1 与 v2 均为 197 个 OMML 对象，按顺序提取的 197 组数学文本完全相同。
- 27 个编号行间公式、公式编号和 `source/formulas.json`（27 条）保持不变。

## 9. 图 1、图 2 状态

- Word 包内仍为 2 个 EMF 矢量对象，并与制图目录中的源 EMF 哈希完全相同：
  - 图 1：`2855659de102cc14cf5d4d0f66a725a92633995cfc3c01136690c53bef572496`
  - 图 2：`15736b1f41c529fa0730f7c8e3d23ef356f60ca2a3fa25454e30520baf0c96c6`
- SVG 设计源保留，未重新设计图义；第 2、5 页渲染清晰，无裁切或失真。

## 10. 表 1～表 3 状态

- 仍为 3 张原生 Word 表格，行数分别为 7、4、15。
- v1/v2 表格全部单元格文本逐项相等；14 项 Tamarin 结果及状态、步数、独立复核匹配列未改变。
- 三张表未定义竖向表格边框；第 3、4、6～7 页渲染无竖线、无重叠、无数据丢失。

## 11. 最终页数

- 最终 PDF 为 A4、9 页，与 v1 页数相同。

## 12. 逐页视觉检查结论

- 已生成 `qa/final-render-v4/page-1.png` 至 `page-9.png` 并逐页按原始分辨率检查。
- 已生成首页和后续页页眉的官方模板/v2 并排图，核对页眉、横线、首页字段顺序和首页页脚。
- 第 1 页首页元数据与双栏起始正常；第 2～9 页页眉连续；通栏表、双栏正文、2 幅图、27 个编号公式和第 9 页参考文献均无裁切、重叠、缺字或异常空白。
- 文档技能标准渲染器已执行，但该 Windows 环境没有 `soffice.exe`，因此使用 WPS 对实际 DOCX 重新分页并导出最终 PDF，再用工作区 Poppler 以 180 DPI 生成 PNG；WPS 统计与 PDF 均为 9 页。

## 13. 作者/基金等待补充的信息

- 中文作者、中文单位、基金项目、作者简介、通信作者与电子邮箱仍需作者确认。
- 英文作者与英文单位仍需补充并核验。
- 中图分类号仍需作者或编辑确认。

## 14. 是否达到投稿格式要求

- 页眉、首页页脚、首页缺失字段、19 条参考文献格式、图表和逐页视觉版式已完成本轮修复。
- 正文完整性检查通过：从“引言”到“参考文献”前共 194 个段落与 v1 逐段相等；题目、摘要、R/M/P 含义、14 项结果、公式语义、图义、表格数据和研究限制未改变；未发现 Markdown 标题、代码围栏、LaTeX 命令、图占位符或大面积异常空白。
- v1 保持原哈希 `a328ea4775287b64151362fe6db32770ec9e45addca2e6c63ca8a88e101bb57f`；`source/__pycache__/` 已删除，未再次生成 `.pyc`。
- MathType 转换尚未完成，且参考文献 `[14]`、`[18]` 的出版地仍需确认，因此未达到完整投稿格式要求。

## 最终文件与哈希

- DOCX：`kwaay-arocmag-draft-v2.docx`  
  SHA-256：`3fdbca305b43eaaee66f4ad9cd06a5c3c5941601bbf0985fcbf998ade9900348`
- PDF：`kwaay-arocmag-review-v2.pdf`  
  SHA-256：`4fac66b21463d32cd41781ffa7337761dabd3acaae4b3fa97df87d65361139a2`

本轮未提交、未推送、未投稿。
