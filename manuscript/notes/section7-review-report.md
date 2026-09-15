# 第七章审查报告

审查日期：2026-09-15。对象：当前工作区的 `07-related-work.tex`，不是旧 Markdown draft。

结论：`SECTION_7_READY_WITH_MINOR_EDITS`。

没有发现需要推翻第七章结构、三模型主线或现有 novelty boundary 的实质性错误，但不能给出“完全无问题”的结论。两项文献版本问题应在冻结前修正，另有两项非阻塞的表述建议。由于这些问题不阻断技术主体的整体评估，本次也继续完成了[整篇论文初次审查](D:/kwaay-formal/manuscript/notes/initial-manuscript-review-report.md)。

## 1. [P2] K-Waay 的定位使用全文版章节号，却引用会议版记录

位置：[第七章第 17 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:17)；[BibTeX 第 6 行](D:/kwaay-formal/manuscript/bibliography/references.bib:6)。当前 PDF 第 16 页可见 `[7, Sec. 5.1]`，而第 19 页的参考文献 [7] 只有 USENIX Security 2024 会议版信息。

本次直接对照了两个原始版本：

- [USENIX 会议版 PDF](https://www.usenix.org/system/files/usenixsecurity24-collins.pdf)：第 5.1 节为 Benchmarks，印刷页 444。
- [IACR ePrint 2024/120 全文版](https://eprint.iacr.org/2024/120.pdf)：第 5.1 节为 Construction，different-party 条件确实位于 Figure 10 后，全文版第 21 页。

所以问题不是条件不存在，也不是本文错误归功于原作者，而是引文不能把读者准确带到支持该主张的位置。现有 `collins2024kwaay` 记录没有全文版 URL 或版本说明；仅在 prose 写 full version 不足以解决 bibliography 的定位问题。

最小修改：为全文版提供可检索的独立记录，或在现有记录中明确附上全文版编号、链接和版本说明，并将对应 pinpoint citation 明确归于全文版。第二章第 15、32、51 行存在同一问题，应一起处理。不要把全文版第 5.1 节机械改成会议版的同号章节。

## 2. [P2] Misbinding 条目混合两个版本，且作者顺序并不相同

位置：[第七章第 99 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:99)；[BibTeX 第 85 行](D:/kwaay-formal/manuscript/bibliography/references.bib:85)。PDF 第 20 页的参考文献 [15] 已实际输出这个混合条目。

当前条目把两篇论文的标题、会议/期刊、2019–2020 年份、页码/文章编号和两个 DOI 拼在一起，不对应一个明确出版记录。更重要的是，两个版本的作者顺序不同：

- [AsiaCCS 2019 会议版](https://doi.org/10.1145/3321705.3329813)：Sethi、Peltonen、Aura，页码 453–464。
- [JISA 2020 期刊版的作者机构记录](https://research.aalto.fi/en/publications/formal-verification-of-misbinding-attacks-on-secure-device-pairin/)：Peltonen、Sethi、Aura，卷 51，文章 102461。

最小修改：根据正文实际采用的内容选择一个版本，或拆成两个正确条目分别引用。如果选择期刊版，必须同时修正作者顺序，不能只替换年份、标题和 venue。当前 misbinding 概念比较没有因此被推翻，但这不是仅当某个投稿格式要求时才需要处理的美观问题。

## 3. 非阻塞建议：把 one-to-one 收窄为准确的 batch-local 性质

位置：[第七章第 120 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:120)。

前句已经写了 scoped，结合第四章可以理解其意图；但下一句直接说 modeled sender 与 receiver occurrences 维持 one-to-one relation，容易被读成所有发送和接收之间的全局双射。

实际 [message-level injectivity lemma](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_message_dedup.spthy:121) 只比较同一完整 `(A,sid,m,bid,rst)` 下的两个 acceptance occurrences；不保证每个 Send 都被接受，也不限制同一 sender tuple 在不同 batch 中再次使用。

建议改为类似：

> Within one batch and receiver context, the message-level variant permits at most one acceptance occurrence for each exact sender-origin tuple, while still admitting two different messages from the same party.

这只是准确复述已有性质，不要求改 lemma 或重跑 prover。

## 4. 非阻塞建议：把 participant consistency 的差异说到定义层

位置：[第七章第 65 行](D:/kwaay-formal/manuscript/sections/07-related-work.tex:65)。

目前只是提到 taxonomy 中有 participant consistency。可增加一句直接对照：该性质比较不同诚实参与者对 participant list 的视图，而本文比较一个 batch 内不同位置的 party projection。二者不是同一谓词，也不应暗示一方的新名称自动构成新贡献。[SoK 原文第 V-A 节](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf)支持前一种定义。

## 已核对且可保留的部分

| 项目 | 审查判断 |
| --- | --- |
| 五个主题小节的组织 | 合理，未退化成逐篇文献摘要列表 |
| K-Waay 的优先权 | 正确承认原文已有条件，没有称本文发现遗漏检查 |
| PQXDH 的方法归属 | ProVerif/CryptoVerif 以及所分析的目标与[官方论文页](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan)一致 |
| Session-handling 的比较对象 | session-to-conversation 与本工作的同 batch 组成对象分开，与[官方论文页](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)吻合 |
| TreeSync 的比较对象 | group-management consistency/integrity 与本工作的 party distinctness 没有混同，参见[官方论文页](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez) |
| Replay 与 identity binding | [X3DH specification](https://signal.org/docs/specifications/x3dh/)确有对应安全讨论；正文没有把它们宣称为新问题 |
| Misbinding / UKS 的边界 | 没有把同一 A 的重复出现写成已证明的错误身份绑定或密钥共享攻击；[RFC 8844](https://www.rfc-editor.org/rfc/rfc8844.html)的比较用途恰当 |
| 贡献定位 | 明确限定于已检索 corpus、two-slot admission abstraction，没有 first-ever 或穷尽性优先权断言 |
| 与模型结果的衔接 | 保留了 M 模型 occurrence injectivity 成立而同 party 不同消息仍可达的关键区分 |

正文的 18 个 citation key 均存在，且对应本地 verification registry 的已核查条目。但是，“key 存在 / registry 标为 yes”不能代替出版版本、作者顺序和定位核对；上述两项问题正说明二者不同。本次对关键论断回查了原始来源，不是对全部相关文献重新开展穷尽性检索，也不据此重新认证全球优先权。

## 版面与交付边界

已检查现有 PDF 第 16–20 页：第七章位于第 16–18 页，未见裁切、重叠或引用问号。第八章和附录为空的现象属于整稿完整性问题，详见整体报告。

本次仅新增审查报告；没有修改正文、BibTeX、模型、证据或原写作报告，没有重新编译 PDF，没有运行 Tamarin，也没有 commit/push。

修复两项文献版本问题并收紧局部措辞后，可把第七章作为下一轮整稿修改的稳定基础；当前不建议标记为无条件冻结。
