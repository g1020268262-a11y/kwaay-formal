# Stage 6 Word 版式执行与保留合同

参考文件：`D:/kwaay-formal/submissions/arocmag/word-final/stage5-submission-package/K-Waay-AROCMAG-submission-stage5-author-confirmation.docx`。

SHA-256：`FBE2E7C8CA1F5BFE2B55F06BAE4B1EFA81340FD8CCA35DD5958EE6CF747BC0FC`。参考6页、10节、4表、2图、99个OMML；底层版式继承官方模板。部件清单见`template-package-inventory.json`。

## 版式与槽位

- A4纵向，21×29.7cm；上2cm，下/左/右1.5cm；页眉页脚距离0.7cm。
- 首页中英文元数据单栏，正文双栏，栏距360twips；表格通过连续分节切换为单栏，表后返回双栏。
- 中文标题黑体16pt；英文标题12pt；一级标题10.5pt，二级9pt；正文宋体/Times New Roman 9pt，12pt固定行距；英文摘要左对齐8.5pt、11pt行距。
- 行内及展示公式保留可编辑OMML；独行公式样式74，9pt，编号右对齐。原6个展示公式必须逐字节保留；新增M见证公式按同样式。
- 三线表，无竖线；7–7.5pt，9.5pt行距；标题8pt居中；行不拆分，表头重复。新增映射表6行、结果表14行。完整结果表单页呈现，必要的分页只改变Word流。
- 图1/2保留既有360dpi PNG及7.9cm宽度，不重新裁切或设计；标题和图2说明仍可编辑。
- 8条参考文献8pt左对齐，9.5pt行距，18pt悬挂缩进；编号定义、事实与顺序保留。允许按新篇幅重新选择末栏分栏点。
- 作者、机构、分类号、基金等仍保留占位；页眉页脚及日期字段原样保留。

## 部件保留

可编辑部件仅`word/document.xml`和`docProps/core.xml`。其余23个部件（styles、numbering、settings、所有页眉页脚、媒体、关系、主题等）从Stage5按字节复制。新增内容沿用同一组样式及图片关系。原正文中内容完全相同的112个块复用原XML；四张旧表和六个旧展示公式逐字节保留。文档仍无MathType OLE对象，不能把OMML或模板残留图片误认成MathType/本文矢量图。

定位以正文XML中的样式、文本及表格结构为依据，不按页码定位编辑。标题/摘要/RQ/Discussion/Conclusion是保留槽位；引言相关工作和贡献、第1章映射、第2章共同资源、第3.2和3.4是本轮授权内容槽位。分节由10增至14，只为新增2张跨栏表，不改章节体系。

## 验收

标准render_docx尝试因缺少LibreOffice而失败；改用真实WPS的只读打开、重新分页与PDF导出，并将7页全部渲染为PNG检查。此结果不是Microsoft Word验收。最终页图、结构审计、保护哈希和逐式清单均在本目录。允许篇幅从6页增加至7页，不因模板槽位容量删正文或缩小字号。
