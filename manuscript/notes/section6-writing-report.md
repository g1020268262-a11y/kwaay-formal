# 第六章写作报告

状态：`SECTION_6_REVISED_AND_VALIDATED`。

## 本次交付与范围

- 完成 `manuscript/sections/06-discussion.tex`，替换原有占位内容。
- 新增本写作报告。
- 重新编译 `manuscript/main.pdf`，并检查第五章到第七章的页面衔接。
- 根据审查结论，对第六章的中心问题、non-vacuity 表述和 rejection failure interface 限制进行了定向修改。
- 将第五章末尾的强制分页替换为浮动体屏障，并在 preamble 中引入 `placeins`；除此之外未修改 Sections 2–5 的论证内容。
- 未修改第七章以后正文、图表内容、模型、结果、证据或研究权威文档；未运行 prover，未 commit/push。

## 聊天要求的读取边界

已读取“研究K-Waay语义可行性”中最新的第六章提示词。读取接口对单条消息限制为 20,000 字符，因此末尾存在截断。本次明确取得了六个 subsection 标题、各小节内容要求、五类主要 limitations，以及不得新增形式化结果或升级历史证据的约束，并按这些可读取要求完成正文；不宣称已读取被截断的尾部。

聊天对第五章 5.4 的一项可选措辞建议没有在本次顺带修改，以保持第六章写作范围。

## 章节结构

1. Why the Result Is More Than Guard Removal
2. Party Identity, Message Identity, and Occurrence Injectivity
3. Invariant and Enforcement
4. Relation to Authentication, Replay, and Deduplication
5. Design Implications
6. Limitations

旧骨架中的独立 Conditional Upper-Layer Interpretation 小节已取消。上层传播仅保留为需要额外 consumer model 的证据边界。没有新增 Security Impact、Mitigation 或 Future Work 小节。

## 论证与证据对应

| 内容 | 依据 | 写作边界 |
| --- | --- | --- |
| 不仅是删除不等式 | 第五章的 relaxed receiver-event witness、message-level 对照、party-level 安全性质与有效 batch 可达性 | 解释现有证据，不声称新方法或新 theorem |
| 三类性质的区分 | 完整 origin tuple、batch/state scope、第五章 Equation (10) | 明确特定非蕴含，不宣称三类性质全面逻辑独立 |
| Invariant 与 enforcement | 第三章目标、第四章规则、现有语义文档 | party 比较只是一个实现；caller、builder、admission layer 只是架构可能性 |
| Authentication / replay / deduplication | 精确 Send correspondence 与 message-level witness | 不把 origin correspondence 写成完整认证，也不称 deduplication 无用 |
| 三条设计启示 | composition boundary、目标坐标、责任归属 | 不声称部署遗漏检查，不规定唯一算法 |
| 五类限制 | 当前模型与第五章证据范围 | two-slot、admission abstraction、ReceiverAccept endpoint、rejection reachability 与具体 failure interface 未定、representation/enforcement |

## 重点措辞审查

- 以 message-level comparison 为核心，不重复列举 14 个 outcome 或 step counts。
- 将中心问题表述为必须保持哪一种 identity relation，不把结论误写成必须采用某个 identity-coordinate check。
- party-level 安全性质以“有效 distinct-party batch 仍可达”说明 non-vacuity，不再使用含糊的 successful/useful behavior 表述。
- 未将 occurrence injectivity 作为新概念或主要创新。
- “must” 和 necessity 仅指保持本文定义的 batch identity interpretation，不指全部 K-Waay 安全、secrecy 或 authentication。
- `same_party_rejection_exists` 的两个 Send tuple 不绑定被拒绝 batch；正文保留这一限制。
- 同 party、不同消息的拒绝说明归于规则语义，而非更强的已验证具体见证。
- Rejection reachability 不等于所有无效 batch 最终都被拒绝。
- 抽象 rejected state 不决定具体系统会丢弃单个 entry、拒绝整个 batch、返回错误或采用其他 failure behavior。
- KEY/TEST、installation、state corruption 和 application compromise 仅出现在明确的不支持结论说明中。
- 未引入历史 HMAC 或 C_install-v2 实验，也未引入 misbinding/UKS 定性。
- 未把 abstract party A 等同于账号、公钥字节、用户名或数据库标识。
- 明确模型含 fresh sid/m 与 persistent origin facts，不能静默扩大到完整协议。
- 保留原始 prover transcripts 缺失、未独立重跑的说明。

## 读取材料

已完整读取当前 Sections 2–5、三个实际 RQ-v2 模型，以及以下正文来源：

- `docs/paper/discussion-draft.md`
- `docs/paper/limitations-draft.md`
- `docs/paper/contribution-evidence-map.md`
- `docs/rq-v2/rq-v2-complete-argument-map.md`
- `docs/rq-v2/g2-admission-semantics.md`
- `docs/rq-v2/rq-v2-threat-model.md`

以下四份文件均存在且已读取，但仅作为概念性支持，不作为新增 formal result：

- `docs/rq-v2/invariant-necessity-analysis.md`
- `docs/rq-v2/invariant-vs-enforcement-analysis.md`
- `docs/rq-v2/party-output-binding-analysis-final.md`
- `docs/rq-v2/security-interface-dependency-analysis.md`

为保持主线简洁，未展开 party-indexed downstream-interface 的可选动机段，也未新增文献综述。文献比较仍留给第七章。

## 编译与页面检查

- 编译：`latexmk -pdf -interaction=nonstopmode -halt-on-error -silent main.tex`。
- 结果：PASS；完整 PDF 17 页，第六章位于第 13–16 页，第七章从第 16 页开始。
- 致命错误、未定义引用/文献、overfull/underfull box：均为 0。
- 已逐页查看第 12–17 页，正文、标题、浮动体及章节衔接无裁切、重叠或缺失。
- 第五章 Figure 2 和 Table 3 仍在第 12 页；`\FloatBarrier` 将第五章浮动体约束在章节边界之前，同时允许第六章自然接续于第 13 页。
- 构建启动器有非致命的 Perl locale fallback 提示，最终 LaTeX 日志无编译警告。
- `texcount`：正文 1,456 英文词；包括标题与行内数学计数的总量为 1,526 单位。六个 subsection 之外仅使用段落标题，未增加独立小节。
- 前后 SHA-256 核对：三个模型、执行报告、admission-semantics 文档与冻结环境记录均未变化。

## 待后续工作

本次状态表示第六章已按审查意见修改并通过构建、版面和范围核对，不代表整篇论文定稿。第七章及后续占位内容、附录补写和原始 prover transcript 补充均不在本次范围内。
