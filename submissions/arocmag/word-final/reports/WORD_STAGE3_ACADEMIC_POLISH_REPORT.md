# K-Waay《计算机应用研究》Word Stage 3 学术润色报告

## 1. 执行范围与基线

- 任务：`AROCMAG_WORD_STAGE3_ACADEMIC_POLISH`
- 执行日期：2026-10-09
- 分支：`main`
- 起始 HEAD：`7c2b8a0184cf858f5a3d468bdd9f71bff8863b01`
- 科学内容权威源：`submissions/arocmag/latex-v2/`
- Word 回退基线：`K-Waay-AROCMAG-submission-stage2.docx`
- Stage 3 交付：`K-Waay-AROCMAG-submission-stage3-polished.docx`

本轮先完成全文审查，再在不改变科学主张的前提下润色 LaTeX，最后从当前 LaTeX 重新生成独立 Stage 3 Word。Stage 2 文件未被覆盖，其 SHA-256 仍为 `440DCA6E07E1E6292FD04F0AD535A15F00B709FFBC9BC5FB2D90D34E8BFA6CFC`。官方投稿模板的 SHA-256 仍为 `BAF9FCE8B2BC56F2320C8BF4541546E43F48A8F3A1C773B40667D7B2A7B872CB`。

润色前已创建独立备份：`submissions/arocmag/word-final/backups/latex-v2-stage3-pre-polish-7c2b8a0/`，其中保存七个章节源文件、`main.tex`、`paper-content.tex`、`main.pdf` 和校验清单。润色前问题分级记录见 `qa/WORD_STAGE3_PRE_POLISH_AUDIT.md`；未发现要求停止处理的 P0 科学或逻辑问题。

## 2. 实际修改文件

### 2.1 LaTeX 学术行文

仅修改以下七个章节文件及重新生成的 `main.pdf`：

- `sections/00-abstract.tex`：重组中英文摘要的问题—方法—结果—结论链条，英文改为第三人称表述。
- `sections/01-introduction.tex`：强化批次组合问题、完整生命周期见证的价值及递进式贡献表述。
- `sections/02-problem.tex`：理顺协议事实、分析抽象、比较维度和研究问题之间的衔接。
- `sections/03-formal-modeling.tex`：澄清攻击者能力、匹配发送来源、事件边界和规则/性质分工。
- `sections/04-formal-analysis.tex`：按结果—见证—解释—RQ 回答组织结果，减少重复并收紧证据边界。
- `sections/05-discussion.tex`：突出机器证据与人工迹语义推导的区别，并集中讨论接口维护义务与适用边界。
- `sections/06-conclusion.tex`：按研究对象—方法—主要结果—有限启示收束。

未修改 `main.tex`、表格源、图形源、参考文献库、Tamarin 模型、lemma、证明记录或复核证据。

### 2.2 Word 生成与核验产物

- `K-Waay-AROCMAG-submission-stage3-polished.docx`
- `figures/fig1-word-stage3.png`
- `figures/fig2-word-stage3.png`
- `formulas/formulas-stage3.json`
- `source/build_word_stage3.py`
- `source/run_content_audit_stage3.py`
- `source/run_layout_audit_stage3.py`
- `source/export_stage3_with_wps.ps1`
- `source/build-manifest-stage3.json`
- `source/citation-order-stage3.json`
- `qa/stage3-content-audit.json`
- `qa/stage3-layout-audit.json`
- `qa/stage3-render-final/`

Stage 3 Word 由润色后的当前 LaTeX 动态提取内容后独立生成，没有复制 Stage 2 正文冒充同步结果。

## 3. 分章修改统计

统计口径为：以空行分隔的正文段落和列表项分别计为一个行文单元；公式、表格、图形、标题和纯标签行不计入。该统计表示被改写的行文单元数量，不表示科学内容增删。

| 部分 | 修改行文单元数 |
|---|---:|
| 中英文摘要 | 2 |
| 引言 | 8 |
| 第 1 章：问题定义 | 10 |
| 第 2 章：形式化建模 | 11 |
| 第 3 章：形式化验证与结果分析 | 18 |
| 第 4 章：结果讨论与适用范围 | 10 |
| 第 5 章：结束语 | 2 |
| 合计 | 61 |

源文件差异为 75 行新增、74 行删除，属于等范围的学术行文替换；章节结构未改变。

## 4. 代表性修改前后对照

以下对照只展示有实质作用的代表性修改；省略处不改变原句的科学限定。

1. **中文摘要的研究问题**
   - 修改前：直接从“K-Waay 已要求不同参与方”进入三模型结果。
   - 修改后：先明确“消息级限制能否替代该条件仍需验证”，再给出共同生命周期、三种模型、关键见证和两槽边界，使目的—方法—结果—结论完整闭合。

2. **英文摘要的人称与方法表达**
   - 修改前：`We construct three fixed-two-slot Tamarin models ...`
   - 修改后：`Three fixed-two-slot Tamarin admission models ... were therefore constructed over a common lifecycle.`
   - 作用：符合官方模板偏好的第三人称行文，同时保留三模型和共同生命周期。

3. **引言中的分析对象**
   - 修改前：“批次准入中的条目关系需要单独建模。”
   - 修改后：“批次准入中的条目关系需要作为单独的分析对象。”
   - 作用：从建模动作前移到研究对象，避免把贡献缩减为技术实现。

4. **原协议条件与本文问题的关系**
   - 修改前：“研究对象不是协议是否遗漏这一条件……”
   - 修改后：“分析并非寻找协议规范遗漏的条件，而是考察该条件维护的批内关系……”
   - 作用：更直接排除“发现原协议漏检”的误读。

5. **静态区别与机器见证的价值**
   - 修改前：只列出三个比较对象及研究问题。
   - 修改后：增加“静态地指出这些对象不同，并不能说明相应条目能否经过来源匹配、批次准入和顺序处理并产生接受事件”。
   - 作用：说明贡献不等于“不同消息不等于不同参与方”这一静态常识，而在于完整生命周期的可达性证据。

6. **问题定义中的条目向量**
   - 修改前：“一次调用的输入可概括为未编号向量”。
   - 修改后：“一次调用的输入可概括为”。
   - 作用：删除编辑性说明，改为期刊正文的自然叙述。

7. **攻击者能力与匹配发送来源**
   - 修改前：“也可选择同一参与方产生的两个不同合法元组”。
   - 修改后：“也可以选择由同一参与方产生、分别具有匹配发送来源的两个不同元组”。
   - 作用：消除“合法”可能暗示完整密码学认证的风险，只陈述模型内来源事实。

8. **`ReceiverAccept` 的事件边界**
   - 修改前：“表示来源匹配后到达抽象接受边界”。
   - 修改后：“表示条目完成来源匹配并到达抽象接受边界”。
   - 作用：明确事件针对条目处理，仍不等同于完整会话接受或密钥安装。

9. **图 2 附近的额外发送限定**
   - 修改前：“执行中可能存在与该元组不匹配的其他发送。”
   - 修改后：正文与 Word 图注统一为“该元组的匹配 Send 唯一，执行中可能存在与其不匹配的其他 Send”。
   - 作用：只断言所示完整元组的匹配来源唯一，不声称整个执行只有一个 Send。

10. **无互异约束模型的 RQ 回答**
    - 修改前：把重复条目见证与 RQ1、RQ2 合并为较长的结果句。
    - 修改后：先交代同一条目占据两槽及两个处理步骤读取同一持久来源事实，再分别回答 RQ1 和 RQ2。
    - 作用：保持一个匹配发送来源对应两个接受事件的准确事件语义。

11. **消息互异模型的决定性证据**
    - 修改前：强调 $m_1\neq m_2$、$A_1=A_2$ 和两项全称结果。
    - 修改后：明确机器见证把该静态关系落实到“来源匹配—准入—顺序处理—接受”的完整共同生命周期，并说明两项全称结果不构成相互独立的增量证据。
    - 作用：保持 $M_\tau\nRightarrow P_\tau$ 的机器证据基础，同时避免累计证据夸大。

12. **机器证据与人工推导的层级**
    - 修改前：在同一段中并列机器非蕴含和规则语义关系。
    - 修改后：明确 $M_\tau\nRightarrow P_\tau$ 由 `same_party_different_messages_batch_exists` 的完整可达执行支持，而 $P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$ 是当前新鲜消息和精确来源匹配规则下的人工迹语义推导，并非新增 Tamarin lemma。
    - 作用：防止把人工推导误报为机器证明或一般协议定理。

13. **适用边界与后续组件**
    - 修改前：“接受事件后的 consumer、状态安装和会话使用过程同样未被建模……”
    - 修改后：“接受事件后的消费组件、状态安装和会话使用过程同样未被建模……”
    - 作用：减少不必要的中英混用，并继续明确重复接受不等于状态破坏或部署攻击。

14. **结束语的收束顺序**
    - 修改前：一个长段连续汇总三模型及关系。
    - 修改后：依次给出研究对象和方法、无互异见证、消息互异非替代性、参与方目标对照、模型内逻辑依赖和两槽边界。
    - 作用：提高结论可读性，没有扩大协议级含义。

## 5. 科学一致性检查

### 5.1 保持不变的对象

- RQ1—RQ3 的三个问题句逐字保持不变。
- 三个固定两槽准入模型、所有 Tamarin 规则、lemma 和证明记录未修改。
- 三个编号公式和三个未编号公式的 LaTeX 内容与 Stage 2 公式清单完全一致；两个公式清单的 SHA-256 均为 `6BC9FA3B7024B99A4F273D5F83ADCAF5A9C6BD65DA68049227B0DDD599388A68`。
- 14 项机器结果仍为 13 项 verified、1 项 falsified；结果状态和证明步数未改变。
- `same_party_different_messages_batch_exists` 及其作为 $M_\tau\nRightarrow P_\tau$ 的机器可达见证完整保留。
- 图 1、图 2 的冻结科学含义、TikZ 源和表格源均未修改。
- 8 条参考文献的顺序和记录完整保留，K-Waay USENIX 会议版与 ePrint full version 仍分别列出。

### 5.2 证据边界

- $P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$ 仍被解释为当前模型的新鲜消息生成与完整元组精确来源匹配规则下的人工迹语义推导。
- $M_\tau\nRightarrow P_\tau$ 仍由既有机器可达见证支持。
- `ReceiverAccept` 仍只表示条目完成来源匹配并到达抽象接受边界，不表示完整协议会话完成、密钥安装或认证密钥交换成功。
- `!Sent` 仍是理想化的模型内来源事实，不表示真实签名验证或完整密码学认证证明。
- 参与方互异模型仍被定位为直接施加目标条件的目标对照（positive control）。
- 两项 rejection witness 仍只证明相应分支可达，不推出所有相关无效输入最终都会被拒绝。
- 未新增实际协议攻击、密钥泄露、机密性失败、部署漏洞、任意批长定理或实现精化结论。

内容审计文件 `qa/stage3-content-audit.json` 的全部检查通过，包括标题、双语摘要、科学锚点、六个公式、四张表、两幅图、八条参考文献、标题层级、匿名元数据和禁止表述检查。

## 6. LaTeX 编译结果

本地执行 `latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex` 成功，生成 11 页 A4 `main.pdf`：

- undefined references：0
- undefined citations：0
- missing glyphs：0
- overfull boxes：0
- LaTeX errors：0
- underfull hbox：1（不影响内容、引用或页面溢出）

内置 LaTeX 编辑器编译器也被调用，但其在开始编译前返回 `Unable to find standard directories for platform`，因此内置工具没有形成第二份编译确认。本报告的编译结论来自本机 XeLaTeX/latexmk 的实际成功构建。

## 7. Word 内容与版式结果

### 7.1 结构与对象

WPS 实际打开并导出 Stage 3 Word，统计为：

- 6 页 A4
- 9530 words（WPS 统计口径）
- 258 个段落
- 4 张表
- 2 幅图
- 99 个 OMath 数学对象
- 10 个版式分节
- 8 条顺序编码参考文献

Word 结构审计 `qa/stage3-layout-audit.json` 全部通过：A4、页边距、首页单栏与正文双栏、通栏表格分节、表格形状、两幅 7.9 cm 单栏图、六个显示公式、OMML、最终分栏符、无外部包关系、匿名核心元数据及 6 页 A4 PDF 均符合预期。

### 7.2 公式状态

- 三个编号公式和三个未编号公式均以可编辑 OMML 生成。
- Word 包中共有 99 个 OMML 对象，包括行间公式和正文内数学对象。
- 未发现公式图片、OLE 公式对象或 MathType 嵌入对象。
- 当前环境没有经过验证的 MathType 转换链，未将 OMML 虚报为 MathType。

状态：`MATH_TYPE_CONVERSION_PENDING`。只有投稿端明确强制 MathType 时，才应在具备 MathType 6.9d 或可靠转换环境后逐式转换并复核。

### 7.3 图片状态

- 图 1 和图 2 均来自已冻结的当前图源，以 360 dpi PNG 插入 Word，单栏宽度 7.9 cm。
- 已逐页检查文字、箭头、虚线、事件顺序、图题和灰度可读性，未见裁切或变形。
- 当前 Word 包中仍保留模板自带 WMF/EMF 媒体，但论文图 1、图 2 实际为 PNG。
- 未在缺少可靠可视验证的情况下声称完成 EMF/vector 转换。

状态：`FIGURE_VECTOR_CONVERSION_PENDING`。若投稿端强制矢量图，需在 Word/WPS 目标环境中转换并再次逐图核对。

### 7.4 三处重点版式问题

1. **第 4 页异常中文字距**：已修复。含长英文 lemma 标识符的段落改用左对齐，普通中文正文保持两端对齐，避免 WPS 对英文长串附近的中文进行异常拉伸。
2. **第 5 页表 4 lemma 换行**：已修复。设置明确列宽，只在下划线边界为三个最长 lemma 名称加入可控换行；忽略换行空白后，标识符文本与科学含义均未改变。
3. **第 6 页双栏与留白**：结论位于左栏、参考文献位于右栏，阅读顺序完整；参考文献字号调整为可读的 8 pt。页面下部仍有由全文篇幅造成的留白，没有通过删文或不可读缩放强行填满。

### 7.5 实际渲染与视觉检查

- WPS COM 导出成功，生成 `qa/stage3-render-final/K-Waay-AROCMAG-submission-stage3-polished-verified.pdf`。
- PDF 为 6 页 A4，所有页面重新转为 PNG 并逐页查看。
- 检查了首页字段、双栏正文、六个公式、四张表、两幅图、页眉、图表标题、长 lemma、参考文献和最终分栏。
- 未发现文字或公式遮挡、对象裁切、图片失真、表格越界、错误分页或空白页。
- 标准 `render_docx.py` 也已实际执行，但本机缺少 LibreOffice `soffice.exe`，该工具在转换阶段失败。此环境限制没有被记作通过；最终视觉结论来自成功的 WPS 实际导出和逐页检查。

## 8. 参考文献状态

- Word 中 8 条参考文献与当前 LaTeX 权威源逐条一致，正文引用序号为 `[1]`—`[8]`。
- 作者、题名、载体类型、出版信息、页码/文章编号、DOI 或公开 URL 沿用已核验的当前记录。
- K-Waay USENIX Security 2024 会议版与 Cryptology ePrint full version 未混淆。
- 未猜测或补造缺失出版元数据。
- 参考文献继续按仓库中官方模板核对所得的 GB/T 7714—2005 顺序编码体例排版。

## 9. 保护范围与完整性

- `tamarin/`：无修改。
- `reviews/`：无修改。
- `submissions/arocmag/latex-v2/figures/`：无修改。
- `submissions/arocmag/latex-v2/tables/`：无修改。
- 参考文献源：无修改。
- `submissions/arocmag/official/`：无修改。
- Stage 2 Word：未覆盖，哈希不变。
- 未运行新的 Tamarin 实验。
- 未 commit，未 push。
- `git diff --check` 未发现空白错误；仅显示 Windows 工作区的 LF/CRLF 提示。

## 10. 待人工处理事项

以下信息或工具能力无法在不编造、不虚报的前提下自动完成：

1. 填写真实作者姓名、单位、城市、邮编、基金、作者简介、通信作者和电子邮箱。
2. 确认匿名投稿阶段是否应继续保留全部身份占位；若转为实名稿，再统一更新中英文作者与元数据。
3. 填写中图分类号、文献标志码、文章编号等由作者或编辑部确认的字段。
4. 若投稿系统强制 MathType，执行并逐式验证 MathType 6.9d 转换；当前为 `MATH_TYPE_CONVERSION_PENDING`。
5. 若投稿系统强制 EMF 或其他矢量格式，转换图 1、图 2 并在目标 Word/WPS 环境复核；当前为 `FIGURE_VECTOR_CONVERSION_PENDING`。
6. 用投稿所用的 Microsoft Word 版本进行一次最终打开、域更新、打印预览和 PDF 对照；本轮已完成 WPS 实际渲染。
7. 提交前在投稿系统预览首页字段、双栏、公式、图表、参考文献和匿名信息。
8. 若需要公开匿名复核材料，补充经确认的匿名 artifact URL；当前不得编造链接。

## 11. 最终判定

科学内容已经与当前 LaTeX 权威源同步，全文学术润色、Word 独立生成、公式/图表/参考文献核对、6 页实际渲染和逐页视觉检查均已完成。章节结构、研究问题、模型、lemma、公式和 14 项机器结果均未改变。

由于真实作者与基金等元数据尚待提供，且 MathType 和矢量图是否为投稿系统硬性要求仍需在目标环境确认，当前不标记 `READY_FOR_SUBMISSION`。

**最终状态：`WORD_STAGE3_ACADEMIC_POLISH_COMPLETE_WITH_PENDING_ITEMS`**
