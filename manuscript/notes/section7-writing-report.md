# 第七章写作报告

状态：`SECTION_7_READY_FOR_REVIEW`。

## 本次交付与范围

- 完成 `manuscript/sections/07-related-work.tex`，替换全部占位内容。
- 新增本写作报告。
- 使用现有 verified literature corpus 和 bibliography；未联网扩充文献。
- 未修改 `manuscript/bibliography/references.bib`、Sections 1–6、Tamarin 模型、结果或证据文件。
- 未运行 prover，未 commit/push。

## 章节结构

1. K-Waay and Post-Quantum Asynchronous Key Exchange
2. Formal Analysis of Secure-Messaging Composition
3. Identity Semantics and Misbinding
4. Injectivity, Replay, and Coordinate-Level Controls
5. Positioning of This Work

结构按研究主题组织，而不是逐篇论文罗列。Signal、PQXDH、Tamarin、MLS 和 misbinding 均被纳入相应主题，没有拆成独立 survey 小节。

## 文献使用

正文引用 18 项 verified works：`L1–L7`、`L9–L11`、`L13`、`L15–L21`。这些条目在 `docs/paper/literature/citation-verification.tsv` 中均为 `source_verified=yes`，相应 18 个 citation key 均存在于 `manuscript/bibliography/references.bib`。

未引用 `L8`、`L12` 和 `L14`：其 CGKA、MLS 标准与 PQXDH specification 背景已经由正文中更直接的 verified sources 覆盖。省略用于避免 citation stacking，不表示对其质量或相关性的否定。

- citation keys used：18
- missing bibliography keys：0
- unverified citations：0
- invented metadata：0
- bibliography modifications：0

## Prior-Art Credit Audit

- K-Waay 已提出 BatchReceive 和 different-party condition：明确归于 Collins et al.
- identity/name uniqueness：明确说明为既有研究主题。
- injective agreement 和 replay-sensitive correspondence：明确说明为既有概念。
- composition-layer security reasoning：明确说明为既有方法论。
- Tamarin：仅作为继承的分析工具与方法，不作为创新。

## Novelty and Collision Audit

正文将定位严格限制在：

- K-Waay 已声明条件的 fixed-two-slot、symbolic、batch-admission analysis；
- removal/message-level/party-level controlled comparison；
- scoped occurrence injectivity 可成立而 party distinction 仍失败的协议特定分离。

“未发现直接碰撞”只表述为 `within the verified literature corpus and search scope`，并紧接非穷尽性限定。最近邻 K-Waay、Session Handling、Names in Cryptographic Protocols、Injective Agreement Analysis 和 TreeSync 均说明了相近点与具体差异。

一般性的 message/identity distinction、identity binding、injectivity、composition reasoning 和 invariant/enforcement distinction 均未宣称为新概念。

## Overclaim Audit

以下不受支持的表述或推论均为 0：

- first-ever、unprecedented 或穷尽性 literature-priority claim；
- K-Waay 遗漏条件、原计算证明错误或本文修复 K-Waay；
- deployed vulnerability；
- cryptographic break、misbinding/UKS result 或 application-level consequence；
- arbitrary-size theorem；
- 将本文结论外推到 MLS、Signal 或所有 batch protocols。

正文明确将 repeated-party witness 与 misbinding、device pairing 和 unknown key-share failure 区分开。

## 篇幅与构建

- `texcount`：正文 1,194 English words；标题 24 words；总计数 1,218。
- subsection 数量：5。
- 编译：`latexmk -pdf -interaction=nonstopmode -halt-on-error -silent main.tex`。
- 构建结果：PASS。
- 完整 PDF：20 页；第七章位于第 16–18 页；第八章和 References 从第 19 页开始。
- fatal error、undefined citation/reference、overfull/underfull box：均为 0。
- 已逐页检查 PDF 第 16–20 页；章节衔接、参考文献和附录入口无裁切、重叠或不可读断行。
- 构建启动器仅报告非致命 Perl locale fallback；最终 LaTeX 日志没有匹配到编译或版面警告。

## 证据边界

本章没有新增 formal result，也没有重述 14 个 lemma outcome 或 step count。模型结果仅用于与既有 injectivity、composition 和 identity 文献进行受限比较。直接证据仍止于 fixed-two-slot symbolic `ReceiverAccept` boundary。

## Remaining TODOs

- Introduction、Conclusion 和附录仍包含占位内容，不属于本次第七章写作范围。
- `sethi2019misbinding` 沿用 bibliography 中已核实但合并 conference/journal 版本的现有条目；如投稿格式要求只保留一个版本，可在整稿 bibliography cleanup 阶段统一处理。
- 原始 prover transcripts 仍未加入；本次没有重新运行 prover。

## Verdict

`SECTION_7_READY_FOR_REVIEW`

该结论表示第七章已按 verified literature 和聊天中的 novelty boundary 写成并通过构建与版面检查，不表示整篇论文已经定稿。
