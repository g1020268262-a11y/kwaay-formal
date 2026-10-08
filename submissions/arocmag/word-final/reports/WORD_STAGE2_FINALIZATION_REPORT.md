# K-Waay《计算机应用研究》Word Stage 2 最终化报告

- 任务：`AROCMAG_WORD_STAGE2_FINALIZATION`
- 项目根目录：`D:/kwaay-formal`
- 执行日期：2026-10-08
- 分支：`main`
- 执行前 HEAD：`4c6dab68ca619faa7877361a1c3baa26fed338df`
- 科学内容权威源：`submissions/arocmag/latex-v2/`
- Stage 2 交付稿：`submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage2.docx`
- 实际渲染 PDF：`submissions/arocmag/word-final/qa/stage2-render-final/K-Waay-AROCMAG-submission-stage2-verified.pdf`

## A. 实际修改

### A.1 LaTeX 最后一项 P2 措辞清理

本轮只收紧“合法来源”一类可能被误读为完整密码学认证的措辞，没有改写章节结构或扩展科学结论。

| 文件 | 修改前 | 修改后 |
|---|---|---|
| `sections/00-abstract.tex` | “各有合法来源” | “各有模型内匹配发送来源” |
| `sections/00-abstract.tex` | “legitimate matching origin” | “matching sender origin” |
| `sections/01-introduction.tex` | “条目各自具有合法来源” | “条目各自具有模型内匹配发送来源” |
| `sections/01-introduction.tex` | “各有合法匹配来源” | “各有匹配发送来源” |
| `sections/04-formal-analysis.tex` | “合法来源条目” | “具有模型内匹配发送来源的条目” |
| `sections/04-formal-analysis.tex` | “合法匹配 Send 来源” | “匹配 Send 来源” |

中文摘要同时删除一个非必要修饰词“决定性”，使摘要保持在官方建议的 200 个汉字以内；按汉字计数为 175 字。LaTeX 全文已确认不再含“合法来源”“合法匹配来源”或 `legitimate matching origin`。

### A.2 Word 交付物及构建检查文件

新建独立 Stage 2 文件，未覆盖 Stage 1 工作稿：

- `K-Waay-AROCMAG-submission-stage2.docx`
- `backups/K-Waay-AROCMAG-submission-working-stage1-backup.docx`
- `source/build_word_stage2.py`
- `source/run_content_audit_stage2.py`
- `source/run_layout_audit_stage2.py`
- `source/build-manifest-stage2.json`
- `source/citation-order-stage2.json`
- `formulas/formulas-stage2.json`
- `figures/fig1-word-stage2.png`
- `figures/fig2-word-stage2.png`
- `qa/stage2-content-audit.json`
- `qa/stage2-layout-audit.json`
- `qa/stage2-render-final/`
- `qa/stage2-vector-test/`

Stage 1 工作稿与备份的 SHA-256 均为：

`03AA990783C22BC30706EBDDA66EDC1024D322974698046D072A6A802507FCCD`

这确认了原 Stage 1 文件未被覆盖。官方原始模板的 SHA-256 仍为：

`BAF9FCE8B2BC56F2320C8BF4541546E43F48A8F3A1C773B40667D7B2A7B872CB`

Stage 2 Word 的 SHA-256 为：

`440DCA6E07E1E6292FD04F0AD535A15F00B709FFBC9BC5FB2D90D34E8BFA6CFC`

## B. 科学同步

逐节对照当前 `latex-v2` 后，Word Stage 2 已同步：中英文标题、中英文摘要与关键词、引言及第 1—5 章正文、RQ1—RQ3、三项编号公式、三项未编号展示公式、四张表、图 1、图 2、正文引用和八条参考文献。

自动内容审计结果为 `all_pass: true`，包括：

- 一级标题 6 个、二级标题 13 个；
- 四张表结构分别为 `6×5`、`4×5`、`5×3`、`8×5`；
- 图 1、图 2 均存在且来自当前冻结图源；
- 三项编号公式与三项未编号公式逐式匹配 LaTeX；
- 八个正文引用编号和八条参考文献完整且顺序一致；
- `same_party_different_messages_batch_exists` 保留；
- 14 项机器结果保持为 13 项 `verified`、1 项 `falsified`。

论证边界保持不变：

- `P_τ ⇒ M_τ ⇔ I_τ` 仍被明确说明为当前模型假设下的人工迹语义推导，不是新增的 Tamarin lemma 或证明器结果；
- `M_τ ⇏ P_τ` 仍由 `same_party_different_messages_batch_exists` 的现有机器可达见证支持；
- `ReceiverAccept` 只表示两槽抽象中的接收事件，不表示完整协议会话完成、密钥安装或部署攻击成功；
- `!Sent` 只承担模型内匹配发送来源的作用，不构成真实密码学认证证明；
- 参与方级模型仍作为正控制；两项 rejection witness 仍只说明对应拒绝分支可达；
- 未新增实际协议攻击、密钥泄露或部署漏洞结论。

未修改 `tamarin/`、冻结模型、lemma、证明状态、复核证据或图示的科学含义，也未运行新的 Tamarin 实验。

## C. 公式状态

Stage 2 Word 中共有 99 个可编辑 OMML 数学对象，覆盖三项编号公式和三项未编号展示公式；量词、上下标、关系符、蕴含关系、多行公式和公式编号均已逐式核对。公式未转成图片。

官方模板使用“推荐采用 MathType 6.9d”的表述。当前环境没有可验证的 MathType 转换链，文件内也没有 MathType/OLE 嵌入对象。为避免把 WPS 公式对象或图片公式误报为 MathType，本轮保留已验证的可编辑 OMML：

`MATH_TYPE_CONVERSION_PENDING`

若编辑部在实际投稿环节强制要求 MathType，应在具备 MathType 的环境中转换，并再次逐式核对。

## D. 图片状态

图 1、图 2 使用当前冻结预览 PDF 生成的 360 dpi PNG，均按单栏宽度 7.9 cm 插入。正文中图题未重复，箭头、线条、灰度层级和文字在 WPS 导出的实际页面中可读。

本轮测试了 PDF 转 SVG 的矢量链，并在 WPS 中实际插入、导出和查看。该路径出现中文及部分动作标签丢失，只保留框线和箭头，因此被判定为不可靠，没有替换正式稿中的图片，也没有虚报矢量化完成。当前状态为：

`FIGURE_VECTOR_CONVERSION_PENDING`

如投稿系统强制要求 EMF 或其他矢量格式，需要使用能保留中文字体的可靠转换链，并在 Word/WPS 中重新验证。

## E. 参考文献

Word 中八条参考文献已按官方模板采用的 GB/T 7714—2005 顺序编码格式整理，正文引用顺序为 `[1]`—`[8]`。已逐项核对作者、题名、载体、年份、卷期、页码或文章编号、DOI/URL及访问日期；未猜测缺失字段。

本轮重点修正和确认：

- K-Waay USENIX Security 2024 会议版与 IACR ePrint 2024/120 full version 分列，未混淆；
- Signal 论文卷期确认为 `33(4)`；
- Tamarin、Names 和 Lowe 文献的会议、页码及 DOI 信息按出版方记录整理；
- ePrint 文献保留公开 URL 和访问日期 `2026-10-08`。

精确引用顺序、最终文本与核对来源保存在 `source/citation-order-stage2.json`。本轮没有剩余的书目元数据阻塞项。

## F. 版式结果

结构化版式审计为 `all_pass: true`：

- A4 纸张；
- 上边距 2.0 cm，下、左、右边距约 1.5 cm；
- 首页前置信息为单栏，正文为双栏；跨栏表格使用独立单栏节，并随后恢复双栏；
- 四张表、两幅图和六项展示公式均存在；
- 最后一页含一个人工分栏点，使讨论、结论与参考文献分布保持可读；
- 文档包内无外部关系、无 OLE/MathType 对象；
- 核心属性保持匿名：作者和最后修改者均为 `Anonymous Author(s)`。

`render_docx.py` 已实际执行，但由于环境中没有 LibreOffice `soffice.exe`，该工具不能完成渲染。随后使用本机 WPS COM 打开、重新分页并导出 PDF；导出成功，得到 6 页 A4 文档。六页均已渲染为 PNG 并逐页视觉检查，未发现文字或图表重叠、裁切、溢出、断页异常、空白参考文献编号或不可读公式。清理文档包后再次导出，六页图像与已检查版本逐页像素一致。

实际渲染 PDF 的 SHA-256 为：

`68A28B1B019801B88B2B0A8FFA773B2ABF65C60CC38C10329C66DB87E5D51B57`

LaTeX 使用以下命令强制重建成功：

`latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex`

结果为 11 页，undefined references = 0、undefined citations = 0、missing glyphs = 0、overfull boxes = 0。内置 LaTeX 编译器也已调用，但在进入编译前报告 `Unable to find standard directories for platform`；因此本报告以成功完成的本地 `latexmk` 构建为编译依据。

## G. 待人工处理事项

以下信息或软件条件无法从项目证据中可靠补齐，均保留明确占位：

1. 真实作者姓名、单位、城市、邮编；
2. 基金项目名称及编号；
3. 作者简介、通信作者、邮箱和电话；
4. 中图分类号、文献标志码、文章编号等编辑部字段；
5. 若编辑部强制要求 MathType，需在具备该软件的环境中执行并复核公式转换；
6. 若投稿系统强制要求 EMF/矢量图，需完成可靠的中文字体保留转换并在目标环境中复核；
7. 正式上传前应在目标 Microsoft Word/投稿系统中做一次最终打开与预览，确认其分页引擎与 WPS 一致。

## H. 最终判定

科学正文同步、P2 措辞清理、公式逐式核对、图表与引用对照、Word 结构审计、WPS 实际渲染、逐页视觉检查、Git 差异和受保护文件检查均已完成。科学主张、模型、lemma 和 14 项机器结果没有改变。

由于真实投稿元数据尚未提供，且 MathType/矢量图是否为投稿系统硬性要求仍需在目标环境确认，本稿不能标记为 `READY_FOR_SUBMISSION`。

**最终状态：`WORD_STAGE2_COMPLETE_WITH_PENDING_ITEMS`**

本任务未执行 commit 或 push。
