# K-Waay 论文 Stage 5 最终投稿准备与交付验收报告

## 1. 基线、范围与判定

- 任务：`AROCMAG_STAGE5_FINAL_SUBMISSION_PREPARATION`
- 执行日期：2026-10-10（Asia/Shanghai）
- 分支：`main`
- 起始 HEAD：`b4b484f20f7b2670490725e8b0653e6ca6de360b`
- Word 基线：`submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage4.docx`
- 科学基线：`submissions/arocmag/latex-v2/`
- Stage 5 交付目录：`submissions/arocmag/word-final/stage5-submission-package/`

本轮没有润色或改写论文，没有运行 Tamarin，没有修改研究问题、模型、lemma、机器结果、公式语义、图表科学内容、参考文献事实或结论边界，也没有 commit、push 或提交论文。Stage 5 Word 的 `word/document.xml` 与 Stage 4 逐字节相同；两份 DOCX 仅 `docProps/core.xml` 不同，用于明确匿名占位和 Stage 5 交付属性。

最终判定：

`SUBMISSION_PACKAGE_PREPARED_WITH_BLOCKERS`

仓库内能够完成的交付准备和验收已经完成。真实作者信息、真正的 MathType 转换、Microsoft Word 终检以及登录后投稿系统规则确认仍依赖外部条件，不能标记为 `READY_FOR_SUBMISSION`。

## 2. 当前官方要求核对

2026-10-10 核对的公开官方页面包括：

- [投稿须知](https://www.arocmag.cn/info/instruction/instructions)：优先上传 doc/docx；作者、单位、作者简介和署名顺序必须真实且无争议。
- [投稿模板](https://www.arocmag.cn/info/instruction/template)：公式要求使用 MathType；模板说明推荐 MathType 6.9d。图表措辞为“尽可能”使用矢量图，并非公开页面规定的绝对强制条件。
- [注册页面](https://www.arocmag.cn/signup)：账号注册要求真实姓名、常用邮箱和电话。
- [摘要要求](https://www.arocmag.cn/info/instruction/abstract-instruction)：继续沿用 Stage 4 已满足的摘要长度和写作规则。
- [中图分类号 TP 类表](https://www.arocmag.cn/info/instruction/clc)：用于作者最终确认分类号。
- [投稿流程](https://www.arocmag.cn/info/instruction/procedure)及[常见问题](https://www.arocmag.cn/info/instruction/faq)：用于作者登录后的流程复核。

公开页面没有说明初投稿必须匿名、采用双盲审稿，或同时上传实名和匿名两套 Word。当前官方模板包含中英文作者、单位、城市、邮编、基金、作者简介、通信作者邮箱和中图分类号；未发现“文献标志码”和“文章编号”是作者必填字段的公开证据。因此：

- 本包保留匿名占位，不猜测作者身份。
- 是否上传实名稿、匿名稿或两套文件，必须登录实际投稿表单确认。
- 文献标志码和文章编号仅在系统或编辑部明确要求时处理。
- 基金并非所有论文都必须填写；有基金时必须使用真实名称和编号，无基金时按系统规则填写。

## 3. 已经完成

### 3.1 独立 Stage 5 Word 和投稿包

已建立不覆盖 Stage 4 的独立 Word：

`stage5-submission-package/K-Waay-AROCMAG-submission-stage5-author-confirmation.docx`

结构审计结果：

- DOCX ZIP 完整，可由 WPS Writer 实际打开；
- 正文、样式、页眉页脚、分节、表格、公式和图片部件均保留；
- 与 Stage 4 的部件名称完全相同；
- 除 `docProps/core.xml` 外，所有部件逐字节一致；
- 核心作者和最后修改者均为 `Anonymous Author(s)`；
- 无批注、人员部件、修订记录、隐藏文本、宏、外部关系、本地路径或真实个人信息。

Stage 5 包含：

1. 待作者确认 Word；
2. WPS 实际导出的 PDF 预览；
3. 99 项公式核对清单和 MathType 操作指南；
4. 未填写的作者信息私下收集表；
5. 投稿规范检查报告；
6. 投稿系统操作检查表；
7. 包说明和 SHA-256 清单。

### 3.2 公式清点

当前 Word 的真实状态为：

- OMML 数学对象：99；
- 行内对象：86；
- 展示公式成员：13；
- 展示公式段落：6，其中编号式 3 项、未编号式 3 项；
- OLE/MathType 对象：0；
- `word/embeddings/`：0；
- 公式图片替代物：0。

`FORMULA_VERIFICATION_CHECKLIST.csv` 含连续的 1—99 项，每项记录对象类型、段落位置、展示编号、数学文本和上下文，并预留 MathType 转换、可编辑性、符号和视觉核对栏。人工指南已明确 `Convert Equations` 的来源、范围和目标设置，以及转换后 OMML=0、MathType OLE/embedding=99 的结构验收目标。

### 3.3 图片核验

冻结源与当前 Word 图片均未修改：

| 图 | 冻结源状态 | Stage 5 Word 图片 | 验收 |
|---|---|---|---|
| 图1 | TikZ + 单页纯矢量 PDF | 1182×1799，约360 dpi PNG | 哈希与 Stage 4 完全相同；WPS 页面完整可读 |
| 图2 | TikZ + 单页纯矢量 PDF | 1182×1454，约360 dpi PNG | 哈希与 Stage 4 完全相同；WPS 页面完整可读 |

现有 PDF→SVG→WPS 实测路径会丢失全部文字；当前环境没有可靠 EMF 写出链，也没有 Microsoft Word 回读环境，因此没有用未经验证的矢量产物替换正确 PNG。官网措辞是“尽可能”采用矢量图；只有投稿系统或编辑部明确强制矢量格式时，该项才成为上传阻塞。

### 3.4 实际渲染和逐页检查

本机 WPS Writer 12.1.0.28505 实际打开 Stage 5 DOCX、重新分页并导出 PDF。结果为：

- 6 页 A4；
- 9548 words；
- 258 个段落；
- 4 张表；
- 2 幅内嵌图；
- 99 个 OMath；
- 10 个版式分节。

PDF 已渲染为 6 张 1241×1754、150 dpi 页面图并逐页实际查看。检查结果：

- 首页题名、匿名占位、中英文摘要和关键词完整；
- 单栏首页和双栏正文正常；
- RQ1—RQ3、式(1)—(3)和 3 个未编号展示公式完整；
- 4 张表和 2 幅图没有裁切；
- 图中文字、数学符号、箭头、虚线和框线清楚；
- 第4页中文字距、第5页长 lemma 换行和第6页参考文献排版没有回退；
- 8 条参考文献内容和阅读顺序完整；
- 未发现新增重叠、缺字、黑框、异常分页或意外断行。

Stage 5 PDF 的标准化提取文本与 Stage 4 WPS PDF 完全相同。该结果只证明 WPS 实际渲染通过，不能替代 Microsoft Word 验收。

### 3.5 自动一致性审计

`qa/stage5-package-audit.json` 的全部内部检查为 `true`，包括：

- Stage 4/Stage 5 正文部件逐字节一致；
- 99 个 OMML、4 张表、2 幅图保持；
- 两幅冻结图片哈希保持；
- 公式清单恰好 99 行且索引为 1—99；
- PDF 为 6 页 A4，文本与 Stage 4 相同；
- PDF 作者元数据为 `Anonymous Author(s)`，未包含本地路径；
- 6 张页面图存在且尺寸正确；
- 匿名性、隐藏信息、外部链接、本地路径和宏检查通过。

## 4. 仍需作者提供

作者应在不受 Git 跟踪的私有目录复制并填写 `AUTHOR_INFORMATION_COLLECTION_FORM.md`，至少确认：

- 中英文作者姓名及顺序；
- 中英文单位、院系、城市、邮编、国家/地区及作者映射；
- 第一作者和通信作者；
- 真实邮箱和手机号；
- 基金名称、编号和英文名称，或明确无基金；
- 投稿系统要求时的作者简介；
- 中图分类号；
- CCF 会员信息、ORCID、栏目等仅在真实适用或系统要求时填写。

填妥文件不得提交到公开 GitHub 仓库。本轮没有根据 GitHub 用户名或其他线索猜测任何身份信息。

## 5. 需要本地软件完成

### 5.1 MathType

环境实测结果：

- `Word.Application` 未注册，未发现 `WINWORD.EXE`；
- 仅存在 OfficeHub，不是 Microsoft Word 桌面版；
- 未发现 MathType/WIRIS/Design Science 安装、可执行文件或 ProgID；
- WPS 可用，但没有 MathType COM 加载项。

因此：

`MATHTYPE_CONVERSION_BLOCKED`

作者需在安装 Microsoft Word 桌面版和真正 MathType 6.9d、且位数兼容的私有环境中：

1. 复制本包到私有目录，保留原 OMML 基线；
2. 用 Word 打开并另存为 `*-mathtype-private.docx`；
3. 在 **MathType → Convert Equations** 中选择来源 `Word 2007 and later (OMML) equations`、范围 `Whole document`、目标 `MathType equations (OLE objects)`；
4. 确认转换对话框报告 99 项；
5. 保存、关闭、重新打开，确认剩余 OMML=0、MathType OLE/embedding=99；
6. 按清单逐项双击验证可由 MathType 编辑，并核对 `⇏`、`⇒`、`⇔`、`≜`、关系符、逻辑连接符、`τ`、Unicode 上下标、正体算子、多行布局和式(1)—(3)编号；
7. 特别检查段落133的4个对象和段落142（式(3)）的5个对象；
8. 用 Microsoft Word 更新域、重新分页并导出 PDF，逐页检查全部 6 页。

只要数量、可编辑性、符号或视觉任一项未通过，就不得解除阻塞。

### 5.2 Microsoft Word 终检

必须在目标 Microsoft Word 桌面版完成：打开、域更新、重新分页、打印预览、PDF 导出和逐页对照。WPS 通过不等同于 Microsoft Word 已验证。

### 5.3 可选矢量转换

如投稿端明确强制 EMF，应从冻结 TikZ/PDF 源在 Inkscape、Illustrator、CorelDRAW 或等效可靠环境中生成真正矢量文件，并在 Microsoft Word 中回读、导出 PDF 后逐图核对。不得把 PNG 套壳为 EMF。

## 6. 需要投稿系统确认

作者登录实际投稿系统后应确认并记录：

- 初投稿是实名稿、匿名稿还是两套文件；
- 是否另需上传 PDF；
- 作者简介、基金、中图分类号、通信作者和手机号的必填状态；
- 匿名稿是否需移除基金、致谢、自引线索或复核材料链接；
- MathType 是否存在上传端硬性检测；
- 图形是否存在强制 EMF/矢量检测；
- 系统生成 PDF 的分页、公式、图表和参考文献是否与本地 Word PDF 一致。

最终点击“提交”必须由获授权的作者本人完成。本任务未自动登录或提交。

## 7. 科学内容保护

文件级证据表明 Stage 5 正文与 Stage 4 完全一致，因此：

- 3 种固定两槽模型未变；
- RQ1—RQ3 未变；
- 14 项机器结果仍为 13 项 verified、1 项 falsified；
- lemma、证明步数和机器见证未变；
- `same_party_different_messages_batch_exists` 保留；
- $P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$ 仍是当前模型规则下的人工迹语义推导；
- $M_\tau\nRightarrow P_\tau$ 仍由既有机器可达见证支持；
- `ReceiverAccept` 和 `!Sent` 的模型内语义边界未扩大；
- 图1、图2、4张表、6项展示公式和8条参考文献内容未变；
- `tamarin/` 和 `submissions/arocmag/latex-v2/` 未修改；
- 未运行新的 Tamarin 实验。

## 8. 交付文件与哈希

主要文件：

| 文件 | SHA-256 |
|---|---|
| Stage 5 Word | `FBE2E7C8CA1F5BFE2B55F06BAE4B1EFA81340FD8CCA35DD5958EE6CF747BC0FC` |
| Stage 5 PDF 预览 | `4D9A150AF19771ED49D2E220AD846C483F59F90F7CBFEC84391855F39FCFFF49` |
| 公式核对清单 | `B7A79188FC10291462B92CB321F454B9F23D53DA82492083EE1F6AC4A6082A32` |
| 作者信息收集表 | `2E5F644800790E0F3CCBF9226AC893704C078B05CFAD3D50947349A70CBB203A` |

完整文件清单、字节数和哈希见 `stage5-submission-package/PACKAGE_MANIFEST.json`。

## 9. 人工交接顺序

1. 在私有目录复制整个 Stage 5 包。
2. 登录投稿系统确认实名/匿名、必填字段、MathType和图形规则。
3. 私下填写真实作者和单位信息；不要把填妥文件提交公开仓库。
4. 如需 MathType，完成99项转换和逐式核对。
5. 生成所需实名/匿名最终副本，保持两者元数据与正文要求一致。
6. 在 Microsoft Word 中完成终检并导出 PDF。
7. 上传后下载系统生成 PDF，按操作检查表逐页核对。
8. 由获授权作者完成最终提交并保存稿件编号、回执和最终文件哈希。

## 10. 最终状态

`SUBMISSION_PACKAGE_PREPARED_WITH_BLOCKERS`
