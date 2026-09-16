# 两轮审查合并修改记录

日期：2026-09-16

依据：ChatGPT 对话「研究K-Waay语义可行性」中最新的第二次整体审查及其合并的第一次审查意见（conversation `6a7ab4f3-a7a0-83ea-a7ab-744db0f2812b`）。

结论：本轮要求的文稿修订与缺失章节补写已完成，形成可继续审查的完整稿；不等同于已完成独立复现或达到特定会议的投稿要求。

## 范围与基线

- 开始时工作树干净，基线提交为 `5eb05981971b20fb7248792037e64647f3b8a6fb`。
- 受版本管理的修改仅涉及 `manuscript/` 内正文、参考文献、图注、附录和支持其排版的文件；另生成了本报告与临时页面检查图。
- 未修改三个 Tamarin 模型、冻结材料、原执行报告或 14 行验证结果表；未执行 Tamarin，包括 parse-only；未提交或推送 Git。
- 先完成技术准确性与抽象说明修改，再按 Introduction → Conclusion → Abstract 的顺序补写首尾，最后完成附录与整体检查。
- 既有各章写作／审查报告保留为历史记录，本文件记录本次整改状态，不改写历史审查结论。

## 审查意见落实情况

| 审查点 | 本轮处理 | 位置 |
|---|---|---|
| K-Waay 会议版与 full version 混用 | 保留会议条目，新增独立 ePrint 2024/120 条目；章节、图号、页码定位引用 full version | Sections 1、2、4、7；BibTeX |
| Misbinding 元数据混合 | 改为 Peltonen、Sethi、Aura 的 JISA 2020 期刊论文，卷 51、文章号 102461 | Section 7；BibTeX |
| 身份坐标表与 fresh 假设冲突 | 第三列改为 interpretation boundary；明确概念区分并不表示所有坐标等式组合在 prototype 中可实现 | Section 2，Table 1 |
| 不恰当的 orthogonal 断言 | 删除不受证据支持的独立性断言，解释省略内容属于建模选择 | Section 4.1 |
| 原协议到抽象模型的映射缺失 | 增加六行 source-to-abstraction 表，区分来源语义、建模假设及 model-local 事件；明确无 refinement theorem、无抽象轨迹具体化证明 | Section 4.1，Table 2 |
| composition 控制似乎是现实协议事实 | 改为 symbolic batch-composition adversary，并明确它是分析能力假设，不证明部署网络攻击者控制 batch builder | Sections 1、3、6 |
| M-model 与真实 dedup 混淆 | 明确 fresh `sid/m` 下的辅助对照及 exact-origin 含义，不泛化到真实编码、碰撞、相同内容发送或跨 batch 缓存 | Sections 4.4、5.2、6.4 |
| message equality 误写 | 两处性质描述改为 message distinction；同时保留真正描述重复消息比较的 equality 用法 | Section 5 |
| changes only 过强 | 改为使用消息坐标作为受控 admission 维度，保留新增 rejection branches 和 inequality actions 的说明 | Sections 4、5.4 |
| admission 与 accept 证据混用 | 显式分为 admission-rule semantics、recorded all-traces safety、reachability/non-vacuity；说明不保证所有 admitted pair 完成 | Section 5.3 |
| necessity 贡献定位过强 | 主贡献调整为消息、发生次数与 party 属性的受控分离；necessity 只保留为相对于既定目标的窄结论 | Abstract、Sections 1、5、7、8 |
| one-to-one 范围过宽 | 本文性质限定为 exact sender-origin tuple 与同一 `(bid,rst)` 内至多一次接受，不承诺每个 Send 交付或跨 batch 禁止复用 | Section 7.4 |
| participant consistency 混淆 | 区分诚实参与者对参与者列表的视图一致性与单 batch 内各位置的 party 投影不同 | Section 7.2 |
| Related Work 内部报告语言 | 删除 verified literature corpus 一类措辞，不做全球优先权声明 | Section 7.5 |
| 术语漂移 | 描述本文目标时统一使用 same-batch party distinction；保留解释 global uniqueness、既有工作或原始 lemma 名称时必要的其他术语 | 全文 |
| 首尾空缺 | 完成引言、结论及摘要，使承诺与 Sections 3–5 的假设、模型和既有结果相对应 | Sections 0、1、8 |
| 三份附录占位 | 补齐重构轨迹与来源边界、精确 lemma、文件映射、命令、版本、模型及文档 SHA-256 | Appendices A–C |

## 引用核对说明

- [K-Waay ePrint 页面](https://eprint.iacr.org/2024/120)：本轮核对 full-version 条目与作者信息。章节和图号定位沿用此前已核实的 full-version 阅读记录；本轮再次获取 PDF 未成功，不将其描述为重新下载并独立逐页复核。会议版与 full-version 引用已分开。
- [Aalto 的期刊论文记录](https://research.aalto.fi/en/publications/formal-verification-of-misbinding-attacks-on-secure-device-pairin/)：核对 Misbinding 期刊版作者顺序、年份、期刊、卷号和文章号。
- [Signal PQXDH 规范](https://signal.org/docs/specifications/pqxdh/)：顺带消除已有但未引用条目中的年份 TODO，区分 Revision 3 的日期与页面最后更新日期；未因此新增正文引文。
- 保留已有文献范围，正文共有 19 个不同 citation keys。本轮没有新增一轮全面文献检索或宣称穷尽相关工作。

## 附录与证据处理

Appendix A 提供按模型规则与现有执行报告重构的抽象序列。它们明确不是原始 prover 图、原始输出或新增运行结果。两个 rejection existence lemma 没有将其 Send tuple 绑定到被拒绝的 batch；相关限制继续保留。

Appendix B 使用 `lstinputlisting` 直接引用冻结模型文件中的原始公式，不手工改写量词或事件参数。逐一核对了 10 段完整 lemma 的起止行；两项 common lemma 在三个模型中逐字一致，打印一次。两项 common × 三模型 + 八项特有性质 = 14 个 model–property instances。

Appendix C 区分三类来源：原执行报告记录的模型哈希；2026-09-16 测得的现有文档快照哈希；用于定位本次文稿基线的 Git 提交。后两者都没有冒充原始 proof-run provenance。复现命令仅列在论文中，没有在本轮执行。

## 检查结果

| 检查 | 结果 |
|---|---|
| 保护文件校验 | 三个模型、四份冻结文件、执行报告及结果表共 9 个文件，修改前后 SHA-256 全部一致 |
| 结果表 | 保留全部 14 行 outcome 与 step counts，无变更 |
| 附录公式 | 10 段完整原文公式；公共公式跨三个模型一致；覆盖全部 14 项结果 |
| 引用与标签 | 19 个不同正文引用键，无缺失键、重复标签或编译中的未定义引用 |
| 占位检查 | 正文与附录无 TODO、FIXME、TBD 或 placeholder |
| LaTeX 编译 | `latexmk -pdf -interaction=nonstopmode -halt-on-error -silent main.tex` 成功；最终 LaTeX/BibTeX 日志无文稿警告、overfull 或 underfull |
| 工具环境提示 | 构建外层 Perl 报本机 locale 回退提示，不影响成功编译；未改动系统设置 |
| PDF 视觉检查 | 共 29 页，全部检查；修正附录长路径溢出、单个 lemma 跨页断开及比较图中的不自然断词；变动页重新渲染复核 |
| 修改检查 | `git diff --check` 通过，受版本管理的修改范围限于论文目录 |

使用 PDF 技能完成了重新编译、页面渲染和可读性检查；它没有改变模型或验证结果。

临时页面检查图保留于 `tmp/pdfs/review-revision-20260916/`，不属于论文证据或最终交付内容。清理该专用目录的调用被环境策略拒绝，未换用其他方式删除；该目录当前未纳入版本管理。

## 仍然保留的限制与后续工作

1. 现有材料仍没有 raw prover transcripts、导出的精确 proof/trace 图或可确认的原始执行提交。本文继续明确报告 recorded executions；本轮检查不构成独立验证。
2. 投稿前建议另行进行冻结模型的完整重跑，保存命令、版本、运行提交与状态、退出码、原始输出、轨迹及输出哈希。该建议未在本轮自动执行。
3. source-to-abstraction mapping 是范围说明，不是 refinement theorem；没有据此扩展到完整 K-Waay、实际部署攻击或任意 batch 大小的结论。
4. 目前仍是 venue-neutral 完整稿。目标会议格式、页数限制、匿名 artifact 发布及进一步的行文压缩不在本轮修改范围内。

入口：[LaTeX 主文件](D:/kwaay-formal/manuscript/main.tex)。
