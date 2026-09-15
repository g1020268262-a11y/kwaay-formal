# K-Waay RQ-v2 论文初次整体审查

审查日期：2026-09-15。

结论：`INITIAL_REVIEW_NEEDS_REVISION — TECHNICAL_CORE_REVIEWABLE, MANUSCRIPT_INCOMPLETE`。

第二至第七章已形成连贯的技术主体，未发现三模型结果被写反或模型版本漂移。当前仍不是完整论文，也不能因可以编译或单章通过审查就标记为可投稿。最优先补齐的是摘要、引言、结论和复现附录；同时修正文献版本与几处跨章语义表述。

本报告区分已确认的错误/缺项与论证说服力建议。P1 表示阻碍整稿完成，P2 表示下一轮应修订的准确性或证据呈现问题；没有发现要求立即改变既有模型或推翻 14 项记录的 P0 问题。

## 审查范围与快照

- 阅读当前 LaTeX 正文、前后置内容、图表、引用库，以及三个实际 RQ-v2 `.spthy` 模型。
- 对照现有 execution report、冻结包环境/命令/模型哈希；对关键文献回查原始来源。
- 按 PDF 审查流程渲染并逐页查看现有 20 页 PDF；未重新编译或覆盖它。
- Git HEAD：`4c0841f9afc7e5d546a54fe68ee2c20522328a88`。审查对象包含尚未提交的第七章与其写作报告，不是仅审查 HEAD。
- PDF SHA-256：`7678BD06186A10B8A43E52212D0EE299EF82451DCA3F9470F61600F1D9102534`。
- 本次只新增两份审查报告，未修改论文、参考文献、模型、结果、冻结材料；未运行 prover、未 commit/push。

“结果一致”指现有论文与现有执行记录一致，不代表本次独立重现证明。没有原始 prover transcripts 的限制在下文单独列出。

## 一、应优先修改的发现

### G1. [P1] 摘要、引言和结论实际为空，整篇论文的论证入口与收束尚未完成

位置：[摘要](D:/kwaay-formal/manuscript/sections/00-abstract.tex:2)、[引言](D:/kwaay-formal/manuscript/sections/01-introduction.tex:1)、[结论](D:/kwaay-formal/manuscript/sections/08-conclusion.tex:2)。

这些文件目前仅有 TODO/comment。PDF 第 1 页显示空 Abstract 和 Introduction，随后直接进入第二章；第 19 页的 Conclusion 标题后直接进入 References。

影响：读者尚未获得完整的问题重要性、贡献摘要、主要发现和收束结论；也无法审查摘要/引言承诺是否与后文证据匹配。RQ1–RQ3 实际已在第二章 2.5 定义，因此不是“全文缺少 RQ”，而是引言还没有形成导读。

建议：在技术正文的准确性修订之后补写上述三部分。引言应简要映射已有 RQ 和三模型证据，不另造一组问题；结论只收束现有受限结论，不能新添部署攻击或完整协议安全主张。该缺项是此前逐章写作阶段的遗留，不是第七章生成造成的回归。

### G2. [P2] 关键原论文的版本定位不一致，另有混合出版记录

位置：[第二章第 15 行](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:15)、[第二章第 32 行](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:32)、[第二章第 51 行](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:51)、[第七章第 17 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:17)、[引用库](D:/kwaay-formal/manuscript/bibliography/references.bib:6)。

`collins2024kwaay` 指向 USENIX 会议版，但正文定位采用 ePrint 全文版章节号和 Figure 10。核查确认：distinct-party 条件确实在[全文版第 5.1 节、第 21 页](https://eprint.iacr.org/2024/120.pdf)，而[会议版第 5.1 节](https://www.usenix.org/system/files/usenixsecurity24-collins.pdf)是 Benchmarks。这是关键论据的可追溯性问题，不是原文条件不存在。

此外，[`sethi2019misbinding`](D:/kwaay-formal/manuscript/bibliography/references.bib:85)混合会议版和期刊版；[期刊版的第一作者实际为 Peltonen](https://research.aalto.fi/en/publications/formal-verification-of-misbinding-attacks-on-secure-device-pairin/)，不能沿用会议版顺序后只改题目和年份。

建议：明确全文版引用；将 misbinding 版本选定或拆分。完整核查与最小修改说明见[第七章报告](D:/kwaay-formal/manuscript/notes/section7-review-report.md)。

### G3. [P2] 第五章把满足的 message-distinction 性质写成了 message equality

位置：[第五章第 213 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:213)、[第五章第 268 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:268)；PDF 第 11、13 页。

正文先列出 message equality、occurrence injectivity、party identity，随后说 satisfying/success for the first two 不蕴含第三个。这里第一项实际应是 message distinction，而不是 message equality。M 模型的 admission 和安全 lemma 要求的是 `m1 != m2`，并拒绝相等消息；其 witness 也明确包含不同消息。

建议：在“哪些性质成立”的句子中统一使用 message distinction、scoped occurrence injectivity、party distinction。只有讨论比较坐标/判等操作时才使用 message identity/equality。这是局部措辞反转，不是式 (10) 或结果表错误。

### G4. [P2] 第二章表 1 的非蕴含关系没有区分概念层和当前模型的 freshness 假设

位置：[第二章第 99 行](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:99)，对照[第四章第 75 行](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:75)和 [SendMessage 规则](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_message_dedup.spthy:20)。

表 1 的 Party 行说 party distinctness 不意味着 distinct message 或 occurrence，且该行将 A 定义为 modeled principal。作为跨协议的概念区分，其意图可以理解；但作为当前模型的性质，这个非蕴含说法不成立：每次 SendMessage 同时产生 fresh `sid` 和 fresh `m`，两个不同 A 的合法 sender-origin tuples 必须来自不同 Send，所以在当前模型中它们的 `sid`、`m` 也不同。ReceiverAccept 还要求匹配完整 origin tuple。

影响：读者可能误以为模型允许“不同合法 parties 共享同一 fresh message/occurrence”，与第四章、实际规则及第六章关于 freshness 影响性质关系的限定冲突。

建议：明确表 1 仅区分坐标的概念含义，不能据此宣称它们在当前模型里任意独立；调整 Party 行的绝对否定。保留论文真正展示的方向：不同 message/occurrence 不保证不同 party。不要为了让表格成立而修改模型或弱化 freshness。

### G5. [P2] 复现附录未完成，现有静态摘要不能替代原始证明与轨迹记录

位置：[附录 A](D:/kwaay-formal/manuscript/appendix/trace-details.tex:3)、[附录 B](D:/kwaay-formal/manuscript/appendix/model-properties.tex:3)、[附录 C](D:/kwaay-formal/manuscript/appendix/reproducibility.tex:3)、[第五章环境说明](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:259)。

PDF 第 20 页的 A/B/C 都只有标题。现有冻结包是 `existing-report-only`，有模型、命令、环境和转录结果，但无 raw prover transcripts。当前第五章和第六章已经如实披露这一限制，所以不把它定性为虚报实验；然而现阶段尚不足以声称整稿的详细 proof/trace 材料已齐全，亦不能凭哈希匹配将转录结果升级为本次独立验证。

建议分两层处理：

1. 先完成文档层工作：在附录写出精确 lemma 与 model 对应、记录命令/环境/哈希，并把示意图明确称为依据模型和执行报告重构的 abstract trace。
2. 若后续要宣称有独立复现或原始证明证据，再单独安排保留完整输出与 provenance 的重跑/归档。不能用本次静态检查代替那项工作，也不要编造目前不存在的原始 trace。

### G6. [P2，论证风险] “密码学细节与问题正交”强于当前已给出的抽象依据

位置：[第四章第 11 行](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:11)，尤其第 14 行的 orthogonal；对照[第二章具体接收语义](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:24)、[第四章 origin 机制](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:104)以及[第六章限制](D:/kwaay-formal/manuscript/sections/06-discussion.tex:177)。

原协议描述包含密码学验证、解封装和 batch-wide failure；最小模型以 persistent `!Sent` 与线性处理状态支持 acceptance，不编码这些成功/失败条件，也没有给出具体 K-Waay trace 到抽象 trace 的保持性或反向实现论证。因此，“我们选择不建模这些细节”是已知事实；“它们不会影响关心的接收行为”尚不能作为由本文证明的事实。

这不推翻已经限定在 admission abstraction 内的结果，但会影响 reviewer 对“为何这是 K-Waay 特定的有意义分析，而不只是一个一般性两槽过滤器实验”的判断。现有 non-claim 和 limitations 有必要保留，却不能完全替代正面的抽象依据。

最小修改：把 orthogonal 改成明确的建模取舍/条件性表述；增加一小段 source-to-abstraction 对照，说明哪些 party/entry/batch 关系来自原接口、哪些 `sid`/freshness/origin facts 是分析假设，以及 `ReceiverAccept` 不与原协议输出等价。若要进一步声称原协议层面后果，则需要新的模型或 refinement 证据；本次不建议自动扩展到该范围。

## 二、非阻塞但值得统一的表述

1. [第五章第 204 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:204)仍有 changes only the constrained identity dimension。与第四章明确承认 guarded models 还增加 rejection branches/Neq actions 的文字相比偏强。建议改为 uses the message coordinate as the controlled admission dimension；后文关于共享 processing 的解释可保留。
2. [第七章第 120 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:120)的 one-to-one 建议改为同一 `(bid,rst)` 内、对一个 exact sender-origin tuple 至多一次 acceptance；不是全局双射或每个 Send 的送达保证。
3. [第五章第 191 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:191)可把“admitted-entry invariant”与“accepted-occurrence lemma”之间的桥梁说清楚：所有 admitted pairs 的 A 不等来自 `AdmitDistinctParties` 加 Inequality restriction；被 machine-checked 的命名 lemma 直接量化的是两个 ReceiverAccept。有效完成路径 witness 提供非空性，而不是用存在性证明所有已准入 pair 都会完成。当前规则支持前者，不需要把它误报成结果无效。
4. 第七章可用一句定义级对比区分 participant-list view consistency 与 intra-batch party distinctness，见单章报告。
5. 第二至第七章多次重复“不是完整协议攻击/不是独有 enforcement”。整体编辑时可以压缩重复，但保留第三章的统一边界、第六章的 limitations 和容易越界处的局部限定。不要通过删光限定来制造更强贡献。

## 三、模型与证据核对结果

### 三模型结论没有发生结果漂移

| 模型 | 核对后的论证内容 | 当前判定 |
| --- | --- | --- |
| Relaxed | 一条 exact tuple 对应一个匹配 Send、同 batch 两个 ReceiverAccept；scoped injectivity 的记录为 falsified；origin correspondence 的记录为 verified | 正文主要解释与模型/记录一致 |
| Message-level | 不同 message/sid、同一 party 的两条 origin tuples 在同 batch 被接受；message distinction 与 scoped injectivity 的记录为 verified | 支持关键非蕴含，不是“一条 Send 被重复接受”的反例 |
| Party-level | accepted party distinction 的记录为 verified，且有 distinct-party 完整 batch witness | 支持模型内非空恢复，不支持唯一 enforcement 或全协议安全结论 |

14 项 lemma 名称、outcome 和 steps 已逐项对照[结果表](D:/kwaay-formal/manuscript/tables/verification-results.tex:11)与[现有执行报告](D:/kwaay-formal/docs/rq-v2/prototype-execution-report.md)。R/M/P 分别为 4/5/5 项；steps 仅是证明运行元数据，不能当性能评测或贡献强度。

当前模型 SHA-256 与 execution report 的记录均一致：

| 模型 | SHA-256 |
| --- | --- |
| Relaxed | `E5129575720020AA3F509782C2052FBF2114A540D013126F5A75D316CBABAF9D` |
| Message-level | `90A196F5DA5C244026596283D001376427880CD64C5BEA3C6CFDFD4CCBA99184` |
| Party-level | `C35AF64CAC7F01182418CB999EA105214B8DA4F2295B670A9B3733F0BD976BBA` |

模型语义层面，还确认了：

- origin 匹配是完整 `(A,sid,m)`，不是只比较 A；`!Sent` 的持久性允许重复使用同一 origin fact。
- `bid` 和 `rst` 每批新建，固定的是 batch size=2，不是总共只能发生一个 batch 或两个 Send。
- 攻击者可以重组网络值；admission 本身不要求 origin，但 processing 要求。因此不是所有 admitted pairs 都必然产生两个 acceptance events。
- rejection existence 不等于 liveness；party rejection lemma 没有将先前两个 Send 绑定到被拒绝 batch。第五章当前已明确说明这一点。
- 没有把 ReceiverAccept 等同于密钥输出、应用状态安装或部署漏洞，也没有把 n=2 的记录写成任意 batch size 的定理。

### 先前审查问题的当前状态

[旧第五章审查报告](D:/kwaay-formal/manuscript/notes/section5-review-report.md)保留历史记录，本次不覆盖它。当前复查发现：

- 将未绑定 Send 解释为特定被拒绝输入对的问题：正文已修正。
- 声称详细附录已交付的问题：当前第五章已改为指向模型文件和静态包，但附录本身仍未完成，见 G5。
- Table 3 漂到附录后的问题：当前 PDF 第 12 页、第五章内，已修正。

## 四、章节与版面初审

| 部分 | 当前状态 | 下一轮重点 |
| --- | --- | --- |
| Abstract / Section 1 | 空占位 | 补齐问题重要性、贡献、受限结论与导读 |
| Section 2 | 有完整问题背景与 RQ | 引用全文版本；澄清坐标表的概念/模型范围 |
| Section 3 | objective、adversary、boundary 齐全 | 保留 batch-local / ReceiverAccept 范围 |
| Section 4 | 与实际规则基本一致 | 收窄 orthogonal，补充抽象依据 |
| Section 5 | 主要结果及 14 项表格齐全 | equality/distinction、控制变量措辞和证据类别 |
| Section 6 | 解释与限制齐全 | 压缩重复，不扩大实施层含义 |
| Section 7 | 可保留结构，需小修 | 两项版本问题及局部 scope wording |
| Section 8 / Appendices | 空占位 | 完成结论与详细证据材料 |

现有 PDF 共 20 页，已全部查看。Figure 1 位于第 9 页，Figure 2 与 Table 3 位于第 12 页，第七章位于第 16–18 页。没有发现文字/图表裁切、重叠或漂出对应章节的问题；第 1、19、20 页的空标题是内容缺失，不是排版引擎错误。

静态检查：18 个实际 citation keys 均有定义；没有发现重复 BibTeX keys、重复 labels 或显式 `ref/eqref` 的缺失目标。现有构建日志未发现 LaTeX error、undefined citation/reference 或 overfull/underfull box 记录。本次没有启动新的构建，结论只针对上述现有 PDF 和当前已检查的源文件。

当前仍采用 venue-neutral、11pt 单栏 review format；README 已明确不是正式 submission template。尚未选择目标 venue，不应将当前 20 页直接与某会议双栏页数限制比较，也不能据此宣称格式合规。

## 五、建议推进顺序

1. 先修正 G2/G3/G4 和非阻塞的局部措辞，不改模型或已冻结结果。
2. 处理 G6 的抽象依据，让贡献表述更具体；保持“协议接口启发的受限语义分析”与“完整协议漏洞证明”分离。
3. 补写摘要、引言、结论，并按现有证据补齐附录；不得把缺失的原始日志写成已经拥有。
4. 整稿完成后做第二轮 claim-to-evidence、重复压缩和 PDF 检查；如需独立复现，另行安排和记录。

当前最准确的定位是：有可审查的技术核心和清楚的证据边界，但还需要完成整稿并修订上述准确性问题。它既不是“需要推倒重写”，也不是“已经可以直接投稿”。
