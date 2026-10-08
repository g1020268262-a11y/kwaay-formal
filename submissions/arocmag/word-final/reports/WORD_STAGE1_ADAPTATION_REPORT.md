# Word Stage 1 adaptation report

## 1. Official template actually inspected

官方模板：`submissions/arocmag/official/templates/投稿编辑模板-计算机应用研究.doc`

SHA-256：`BAF9FCE8B2BC56F2320C8BF4541546E43F48A8F3A1C773B40667D7B2A7B872CB`

模板与先前留存的官方原件副本逐字节一致。已实际检查其三页渲染，覆盖首页、后续双栏页、标题层级、公式、图、表、参考文献、页眉和首页页脚。

实际结构如下：

- A4纵向；上边距2.0 cm，其余边距1.5 cm；
- 首页题名、作者、单位、中英文摘要和关键词为单栏；
- 正文为双栏，栏间距约0.64 cm；
- 一级标题10.5 pt，二级标题9 pt，正文9 pt、固定12 pt行距；
- 图表文字8 pt，图题在图下，表题在表上；
- 独行公式居中并在右侧编号；模板允许Word OMML后续转换为MathType；
- 表格采用无竖线的三线表；
- 参考文献采用顺序编码，模板明确指向GB/T 7714—2005；
- 首页页眉右侧为修改日期字段，首页页脚保留基金、作者简介和通信作者信息区。

## 2. Word working file

`submissions/arocmag/word-final/K-Waay-AROCMAG-submission-working.docx`

当前稿由官方模板转换基底派生，没有修改或覆盖官方`.doc`。旧`word-draft/`只用于复用模板转换和排版工具经验，科学内容全部读取自`latex-v2/`基线`54ad3723d1c509693693c8b5984c3b1b8bc006e1`。

## 3. Migrated content

- 中英文标题、摘要、关键词；
- 0–5章全部正文；
- 6个一级标题、13个二级标题；
- 3个编号公式及2个未编号公式；
- 4张可编辑Word表格；
- 图1、图2、两处图题及图2证据说明；
- 8个正文引用与8条参考文献；
- M/I模型内依赖说明及其人工推导边界；
- 固定两槽、非完整K-Waay攻击和非部署漏洞等适用范围；
- 13 verified + 1 falsified结果。

映射细节见`LATEX_TO_WORD_MAPPING.md`。

## 4. Incomplete items

- `AUTHOR_METADATA_PENDING`：作者、单位、城市、邮编、基金、作者简介、通信作者、邮箱、中图分类号、文献标志码和文章编号均待权威信息；
- `MATH_TYPE_CONVERSION_PENDING`：公式当前为OMML，尚未转换并逐式核验为MathType对象；
- `EMF_VECTOR_CONVERSION_PENDING`：两图当前使用高分辨率PNG占位，矢量PDF已保留；
- `GBT_REFERENCE_FORMAT_FINALIZATION_PENDING`：引用闭合已完成，最终GB/T格式及缺失出版项尚待复核；
- 最后一页双栏未做栏平衡，右栏留白；留待正式版式QA处理，不删改正文；
- 模板的修改日期字段在WPS渲染中显示其缓存值，投稿前需在最终Word环境刷新字段。

## 5. Formula format

- 编号公式：式(1)、式(2)、式(3)，编号和正文引用一致；
- 未编号公式：输入向量、批内来源单射性前件，共2个；
- 全文共92个可编辑OMML数学对象，未使用公式截图；
- 原始LaTeX记录保存在`formulas/formulas.json`；
- 后续MathType转换必须保持量词、上下标、多行结构和编号不变。

## 6. Figure format

- 图1和图2均来自当前冻结的独立预览PDF；
- Word中暂用360 dpi单栏内联PNG；
- 独立预览自带图题/说明已从占位图裁去，Word中的图题和图2说明保持可编辑；
- 未修改TikZ、图中文字、结构、箭头或图义；
- 后续方案见`FIGURE_VECTOR_CONVERSION_PLAN.md`。

## 7. Reference format

- 正文采用`[1]`–`[8]`首次引用顺序；
- 8条文末条目均来自冻结`references.bib`；
- 当前使用官方参考文献段落样式，但不宣称已完成最终GB/T规范化；
- 缺失出版项没有猜测，详见`REFERENCE_FORMAT_AUDIT.md`。

## 8. Anonymous information status

- 首页仅保留“作者信息待补”等显式占位；
- 基金、作者简介、通信作者和邮箱均为待补；
- 核心属性`author`和`last_modified_by`均为`Anonymous Author(s)`；
- 未发现真实作者、单位、邮箱或本地路径泄露。

## 9. Word and LaTeX consistency

自动一致性检查全部通过：

- 中英文标题、摘要和关键词一致；
- RQ1–RQ3完整；
- 3个编号公式和2个未编号公式存在；
- 4张表形状分别为6×5、4×5、5×3、8×5；
- 图1/图2各1个；
- 8个引用编号连续闭合；
- `same_party_different_messages_batch_exists`、13 verified + 1 falsified、M/I依赖、人工推导不是机器证明、固定两槽边界和非具体协议攻击边界均存在；
- 未发现`\\cite`、`\\ref`、`\\begin`、项目宏、TODO、GitHub内部路径或本地盘符残留；
- `latex-v2/`、Tamarin模型和冻结图源均无修改。

## 10. Layout QA

最终WPS渲染为A4、6页。已逐页按原始分辨率检查：

| 页 | 内容 | 结果 |
|---:|---|---|
| 1 | 中英文题名、摘要、关键词、匿名字段、引言 | 无裁切、重叠或缺字；首页单栏和正文双栏切换正常 |
| 2 | 第1章、表1、式(1)(2)、第2章前部 | 标题编号、公式编号和全栏表格正常 |
| 3 | 图1、表2、表3、未编号公式 | 图题唯一；表格可读；无横向越界 |
| 4 | 第3章、式(3)、图2、3.2–3.3 | 图2及说明完整；无重复图题/说明；公式可读 |
| 5 | 3.4、表4、第4章 | 表4完整，7项核心结果及注释可读 |
| 6 | 局限、结束语、8条参考文献 | 内容完整；右栏留白列入下一阶段栏平衡处理 |

文档技能的标准LibreOffice渲染器在当前运行时未提供`soffice.exe`，因此使用项目此前验证可用的WPS COM接口完成分页和PDF导出，再用工作区Poppler生成逐页PNG。结构审计显示：4张表、2个内联图、92个OMML对象、10个连续分栏节。

## 11. MathType follow-up

在安装并确认MathType转换接口后，将全部OMML批量转换为MathType兼容对象，并逐项核对3个编号、2个未编号公式及所有行内数学。转换前后必须进行对象计数和逐页视觉比较。

## 12. EMF follow-up

按`FIGURE_VECTOR_CONVERSION_PLAN.md`将当前冻结PDF转换为EMF，替换PNG占位后复核单栏尺寸、字体、线条、灰度、图题邻接和图2证据说明。

## 13. GB/T follow-up

以官方模板的GB/T 7714—2005要求为基线，补充并核验出版地、出版者、期号、DOI/URL和在线访问日期，统一外文作者著录规则。不得编造缺失字段。

## Final status

`AROCMAG_WORD_STAGE1_READY_FOR_FORMAT_QA`

