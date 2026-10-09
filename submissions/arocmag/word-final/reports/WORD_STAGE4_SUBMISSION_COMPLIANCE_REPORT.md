# K-Waay 论文 Stage 4 正式投稿文件最终合规化报告

## 1. 基线、范围与最终判定

- 任务：`AROCMAG_STAGE4_SUBMISSION_COMPLIANCE`
- 执行时间：2026-10-09 至 2026-10-10（Asia/Shanghai）
- 分支：`main`
- 起始 HEAD：`8118806da7dbf676177d0c392bb27750cc3fdb94`
- 受保护科学基线：`submissions/arocmag/latex-v2/`
- Word 基线：`K-Waay-AROCMAG-submission-stage3.1.docx`
- Stage 4 交付：`K-Waay-AROCMAG-submission-stage4.docx`
- WPS 导出预览：`qa/stage4-render-final/K-Waay-AROCMAG-submission-stage4-verified.pdf`

本轮只修改了中文摘要中两处指定表述，并修复了 LaTeX 到 Word 转换程序对英文长破折号的处理。未进行第二次全文润色，未修改章节结构、RQ1—RQ3、模型、lemma、机器执行轨迹、验证结果、公式科学含义、图表科学内容、Discussion、Conclusion 或参考文献事实。

当前最终判定：

`STAGE4_COMPLETE_WITH_EXTERNAL_BLOCKERS`

内部可自动完成的文本、Word 构建、结构审计、公式清点、匿名性审计、WPS 实际渲染、逐页视觉检查和科学一致性检查均已完成。真实作者信息、可靠 MathType 转换以及最终 Microsoft Word/投稿系统预览仍需外部条件。

## 2. 官方要求核对

### 2.1 当前官网与模板

2026-10-09 实际核对了《计算机应用研究》官方网站：

- [投稿模板](https://www.arocmag.cn/info/instruction/template)，页面日期 2024-06-26：要求公式通过 MathType 插入，说明 MathType 6.9d 可批量转换；图表“尽可能”使用矢量图，并建议在 Word 中选择性粘贴为增强型图元文件。该措辞表明 MathType 是当前明确格式要求，矢量图是强烈建议而非页面所述的绝对强制条件。
- [摘要编写要求](https://www.arocmag.cn/info/instruction/abstract-instruction)，页面日期 2022-07-24：中文摘要以 200～300 字为宜，采用第三人称、客观表述，一般不分段、不使用引文；英文摘要一般不超过 150 words。
- [投稿须知](https://www.arocmag.cn/info/instruction/instructions)，页面日期 2024-06-26：稿件应通过投稿系统提交，优先上传 doc/docx；要求作者署名和联系方式真实、无争议，但页面未说明初投稿件应采用匿名稿或双盲稿。

从官网当前“下载投稿模板”链接取得的 `.doc` 与仓库原始模板逐字节一致，SHA-256 均为：

`BAF9FCE8B2BC56F2320C8BF4541546E43F48A8F3A1C773B40667D7B2A7B872CB`

官网专门的摘要页面写明“200～300 字为宜”，当前模板正文仍含“200 字以内为宜”的较短提示，二者均是建议性措辞但范围不一致。本轮没有假定模板内短提示自动优先，而是采用官网专门摘要页面的 200～300 字规则，并在此记录来源差异。

### 2.2 摘要适用结果

- Stage 3.1 中文摘要：200 个 Unicode CJK 汉字。
- Stage 4 中文摘要：212 个 Unicode CJK 汉字，符合官网专门摘要页面的 200～300 字建议。
- 英文摘要：139 words，符合官网“一般不超过 150 words”的说明。
- 中英文摘要均保持研究问题、共同生命周期、三种固定两槽模型、人工语义推导、机器可达见证、消息级约束不能推出参与方级互异性以及固定两槽边界。

## 3. 实际修改

### 3.1 两处限定文字修正

中文摘要第一句：

- 修改前：`K-Waay的BatchReceive要求同次调用对应不同参与方……`
- 修改后：`K-Waay的BatchReceive要求同次调用中的输入元素分别对应不同参与方……`

参与方模型名称：

- 修改前：`参与方模型保持目标关系，有效批次可达。`
- 修改后：`参与方互异约束模型保持目标关系，有效批次可达。`

这些改动只澄清约束所作用的输入元素和模型名称，没有改变研究问题或结论。

### 3.2 英文长破折号

Stage 3.1 Word 中存在两处未转换的 LaTeX 标点：

- `models---unconstrained`
- `party-constrained---were`

`build_word_stage4.py` 现在统一把 LaTeX `---` 转换为英文长破折号 `—`，并把 `--` 转换为短破折号 `–`。Stage 4 Word 可见文本中 `---` 的剩余数量为 0；首页实际渲染显示为自然英文长破折号。修复位于可重复构建程序中，不是对单个 Word 文件的手工替换。

### 3.3 新增和更新文件

- `submissions/arocmag/latex-v2/sections/00-abstract.tex`：仅含上述中文摘要两处修正。
- `submissions/arocmag/latex-v2/main.pdf`：由当前 LaTeX 重新编译。
- `submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage4.docx`：独立 Stage 4 Word，未覆盖 Stage 3.1。
- `submissions/arocmag/word-final/source/build_word_stage4.py`：Stage 4 可重复构建和破折号转换。
- `submissions/arocmag/word-final/source/export_stage4_with_wps.ps1`：WPS 实际打开和 PDF 导出。
- `submissions/arocmag/word-final/source/run_content_audit_stage4.py`：内容与科学锚点审计。
- `submissions/arocmag/word-final/source/run_layout_audit_stage4.py`：页面、分栏、表格、图形和公式结构审计。
- `submissions/arocmag/word-final/source/run_submission_compliance_audit_stage4.py`：99 个公式对象、匿名性、图片、页面对照和包结构审计。
- `submissions/arocmag/word-final/formulas/formulas-stage4.json`：六项展示公式源记录。
- `submissions/arocmag/word-final/qa/stage4-formula-inventory.json`：全部 99 个 OMML 对象清单。
- `submissions/arocmag/word-final/qa/stage4-content-audit.json`、`stage4-layout-audit.json`、`stage4-submission-compliance-audit.json`：最终自动审计结果。
- `submissions/arocmag/word-final/qa/stage4-render-final/`：WPS PDF 与 6 页 150 dpi PNG 视觉核验产物。

## 4. 公式处理结果

### 4.1 实际对象清单

Stage 4 Word 共有 99 个可编辑 OMML 数学对象：

- 行内 OMML 对象：86；
- 六个展示公式段落内的 OMML 成员：13；
- 展示公式段落：6；
- 编号公式：3，编号顺序为 (1)、(2)、(3)；
- 未编号展示公式：3。

多行展示公式在 OOXML 中由同一展示段落内的多个 `m:oMath` 成员组成，因此 99 不表示 99 个独立展示公式。完整对象、段落位置、上下文、编号和数学文本记录在 `qa/stage4-formula-inventory.json`。

Stage 3.1 与 Stage 4 的六项展示公式源清单 SHA-256 完全相同：

`6BC9FA3B7024B99A4F273D5F83ADCAF5A9C6BD65DA68049227B0DDD599388A68`

`∀`、`∃`、`⇒`、`⇔`、`≠`、上下标、$P_\tau$、$M_\tau$、$I_\tau$、`ReceiverAccept`、`DistinctPartyPerBatch`、多行时间关系和公式编号均在内容审计及页面视觉检查中核对通过。

### 4.2 MathType 状态

当前环境未检测到 MathType 可执行程序或可验证的 MathType Word 插件。Stage 4 DOCX 中：

- OMML 对象：99；
- OLE/MathType 对象：0；
- `word/embeddings/` 对象：0；
- 公式图片：0。

未把 OMML、图片或扩展名伪装成 MathType，未进行不可验证的批量转换。

`MATHTYPE_CONVERSION_BLOCKED`

最小人工处理步骤：在安装 MathType 6.9d 且能由 Microsoft Word 调用的环境中，对副本批量转换；随后逐式核对 99 个对象、六项展示公式、(1)—(3) 编号、上下标和关系符，并重新导出 PDF 逐页检查。

## 5. 图形处理结果

图 1 和图 2 的科学内容、TikZ 源和冻结状态均未修改。Stage 4 Word 继续使用由冻结 PDF 预览生成的高分辨率 PNG：

| 图 | 像素 | DPI | SHA-256 | 与 Stage 3.1 |
|---|---:|---:|---|---|
| 图 1 | 1182 × 1799 | 360 | `AE6C5800ECFA64AB86200A6C73E25AA9248BA584825B9EEA8D0BC804E25C12AB` | 完全相同 |
| 图 2 | 1182 × 1454 | 360 | `8A4804F82DC382DE777B726D21827703DA84C7E7920311F703619EB48DA06992` | 完全相同 |

两图均以内嵌方式插入，单栏宽度 7.9 cm。WPS 页面检查确认中文、数学符号、箭头、时间线、虚线、框线、动作事实、图题和灰度层级完整可读。

当前环境有 `dvisvgm` 和 `pdftocairo`，但没有 Inkscape、pstoedit 或其他可验证的 EMF 写出和 Word/WPS 回读链。此前 PDF→SVG 路径曾出现中文和动作标签丢失；本轮没有用该不可靠路径替换正确 PNG，也没有把位图封装成 EMF 后声称为矢量图。

`VECTOR_GRAPHICS_PENDING`

官网使用“尽可能使用矢量图”的建议性措辞；如编辑部或投稿系统实际强制 EMF，应在可保留中文字体和数学符号的转换环境中从冻结 TikZ/PDF 矢量源生成，再在目标 Word/WPS 中逐图复核。

## 6. 投稿元数据与匿名性

官网投稿须知要求作者署名和联系方式真实且无争议，但未找到初投稿件必须匿名或双盲的明确说明。由于仓库没有经确认的真实作者信息，本轮没有编造作者、单位、基金、邮箱、电话或通信作者。

Stage 4 当前保留：

- 正文作者和单位显式待补；
- 基金、作者简介、通信作者及邮箱显式待补；
- 中图分类号、文献标志码、文章编号保持待确认；
- 核心属性 `author` 和 `last_modified_by` 均为 `Anonymous Author(s)`。

匿名性与隐私审计结果：

- 批注/人员部件：0；
- 修订插入、删除和移动记录：0；
- 隐藏文本：0；
- 外部包关系：0；
- 本地路径泄露：0；
- 两幅论文 PNG 仅含 DPI 元数据，无作者或路径元数据；
- 文件名不含真实作者信息。

该文件可作为匿名审阅稿，但官网没有确认它能替代实名投稿稿件。正式上传前必须由作者确认投稿系统是否接受匿名文件，并在要求实名时一次性补齐真实且一致的中英文作者信息和联系方式。

## 7. 实际排版与渲染结果

### 7.1 Word 结构

- 纸张：所有分节均为 A4；
- 页边距：上 2.0 cm、下 1.5 cm、左 1.5 cm、右 1.5 cm；
- 首页单栏，正文双栏，通栏表格分节保持正常；
- 一级标题 6 个，二级标题 13 个；
- 表格 4 张，形状分别为 6×5、4×5、5×3、8×5；
- 图形 2 幅，均为 7.9 cm 单栏内嵌图；
- 展示公式 6 项，OMML 对象 99 个；
- 参考文献 8 条，正文 `[1]`—`[8]` 引用完整；
- 末页保留 1 个受控分栏符。

`stage4-content-audit.json`、`stage4-layout-audit.json` 和 `stage4-submission-compliance-audit.json` 的内部检查均为 `all_pass: true`。这些自动结果只用于结构核对，未替代视觉审查。

### 7.2 WPS 实际打开与 PDF 导出

使用本机 WPS COM 实际打开 Stage 4 DOCX、重新分页并导出 PDF，结果为：

- 6 页 A4；
- 9548 words；
- 258 个段落；
- 4 张表；
- 2 个正文内嵌图形；
- 99 个 OMath；
- 10 个版式分节。

标准 `render_docx.py` 也已实际调用，但环境中没有 LibreOffice `soffice.exe`，不能生成第二套 LibreOffice 渲染。本报告只确认 WPS 实际渲染，不把 WPS 结果等同于 Microsoft Word 已验证。

### 7.3 六页视觉检查

- 第 1 页：212 字中文摘要完整；“同次调用中的输入元素”与“参与方互异约束模型”已生效；英文两处 `---` 均显示为自然长破折号；英文摘要继续左对齐，无异常词间距；匿名占位和元数据字段可见。
- 第 2 页：双栏、RQ1—RQ3、式 (1)、式 (2) 和表 1 完整，无裁切。
- 第 3 页：图 1、表 2、表 3 和未编号公式完整，图中文字和箭头清晰。
- 第 4 页：Stage 3 已修复的中文字距未回退；式 (3)、图 2、两条来源读取虚线和两个接受事件完整。
- 第 5 页：表 4 的长 lemma 名称保持按下划线边界换行，无标识符损坏或越界；正文双栏正常。
- 第 6 页：8 条参考文献内容和顺序完整，左对齐与悬挂缩进稳定；左栏结束语和第 1 条文献、右栏第 2—8 条的阅读顺序正确，保留自然下部留白。

与 Stage 3.1 PDF 的逐页文本对照显示：第 1 页仅发生本任务授权的摘要和标点变化，第 2—6 页提取文本逐页完全相同。六页均重新渲染为 1241×1754、150 dpi PNG 并实际查看，未发现重叠、裁切、缺字、黑框、图表失真或公式不可读。

## 8. LaTeX 编译与科学一致性

LaTeX 使用 XeLaTeX 完整重编译，生成 11 页 PDF。最终日志：

- undefined references：0；
- undefined citations：0；
- missing glyphs：0；
- overfull boxes：0；
- errors：0；
- underfull boxes：1（既有段落松散提示，不影响内容或裁切）。

科学一致性检查结果：

- 三种固定两槽准入模型未变；
- RQ1—RQ3 未变；
- 14 项机器结果仍为 13 项 verified、1 项 falsified，状态和证明步数未变；
- 所有 lemma 和机器执行轨迹未变；
- `same_party_different_messages_batch_exists` 完整保留；
- $P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$ 仍明确属于当前模型规则下的人工迹语义推导；
- $M_\tau\nRightarrow P_\tau$ 仍由既有机器可达见证支持；
- `ReceiverAccept` 仍是模型内接受事件，不被解释为完整会话、密钥安装或部署攻击；
- `!Sent` 仍是理想化来源事实，不被扩大为完整密码学认证；
- 4 张表、2 幅图、6 项展示公式和 8 条参考文献的科学内容未变；
- `tamarin/` 无修改，未运行新的 Tamarin 实验。

## 9. 文件哈希

- Stage 4 DOCX：`C5A9A26B036B1B6747DEF8279769038BB8C1D1F92C392BB1A002D2ED8B6F9A64`
- Stage 4 WPS PDF：`448FF3B1C60D0E4BB66528F9D44044EDF3F01EEAA6E7A33500CE9B9CEC498F28`
- Stage 4 LaTeX PDF：`A5B94B60C2B7E7F1A6D4180D05C58A11A4A7746842C9D0F6900A977B02FA0C02`
- 受保护的 Stage 3.1 DOCX：`71EB1C4B2F856D7CF63434861F96EB83BA4844F355A3D298EDF22984766A4556`

## 10. 剩余外部阻塞项

按优先级排列：

1. **真实投稿元数据**：作者姓名和顺序、单位、城市、邮编、通信作者、邮箱、电话、基金、作者简介、CCF 会员信息等必须由作者提供并确认；中图分类号需由作者依据官网 TP 类表确认，文献标志码和文章编号等编辑字段不得自行编造。
2. **MathType**：官网当前明确要求公式通过 MathType 插入；本机没有可靠转换链，当前为经过验证的可编辑 OMML。状态：`MATHTYPE_CONVERSION_BLOCKED`。
3. **匿名/实名文件选择**：官网未公开说明初投稿是否双盲；正式上传前需在实际投稿系统确认是否提交实名稿、匿名稿或两套文件。
4. **Microsoft Word 和投稿系统终检**：本轮完成 WPS 实际打开和 PDF 导出，未完成目标 Microsoft Word 版本的域更新、打印预览和投稿系统生成预览。
5. **矢量图**：官网为“尽可能”采用矢量图的建议；当前高分辨率 PNG 已通过 WPS 视觉核验。如投稿端强制 EMF，需使用可靠矢量链处理。状态：`VECTOR_GRAPHICS_PENDING`。
6. **摘要规则来源差异**：官网专门页面为 200～300 字，当前下载模板内部仍写 200 字以内。Stage 4 的 212 字符合专门页面；如投稿系统另有隐藏硬限制，需在上传界面确认。

上述事项依赖真实作者信息、专用软件或投稿端规则，不能通过当前仓库内的自动处理可靠补齐。因此本轮不标记 `READY_FOR_SUBMISSION`。

`STAGE4_COMPLETE_WITH_EXTERNAL_BLOCKERS`
