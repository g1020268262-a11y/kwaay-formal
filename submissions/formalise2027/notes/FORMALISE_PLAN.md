# FormaliSE 2027 内容适配计划

状态：仅计划；本阶段不执行正文压缩或研究扩展。下一阶段标识：`FORMALISE_CONTENT_ADAPTATION`。

## 1. 定位与证据边界

推荐定位：**a formal-methods case study of a source-motivated batch-admission semantic invariant**。

K-Waay 原文已经明确要求 BatchReceive 输入来自不同 party。本文把该条件形式化为 party-level batch invariant，并在受控抽象中检验其他坐标上的控制能否替代它。贡献重心应为 controlled formal analysis、semantic invariant、coordinate non-substitutability、bounded Tamarin case study、reproducible verification。

“bounded”须准确解释为每 batch 固定两槽；不能说 party、Send 和 batch 的总次数都已全局有界。不把结果包装为 K-Waay vulnerability、cryptographic break、AKE attack、KEY/TEST failure 或 implementation bug。R/M 的重复 party 输入在原构造明确规定的不同 party 输入域之外。

case study 定位本身不能解决研究增量不足。后续需要说明此 admission 契约的形式化对软件集成理解有何价值，并区分已观察的控制差异与尚无实现证据的工程动机；不可虚构真实实现采用 message-only 检查。

## 2. 已读取的 review 与待处理问题

依据：`../../../reviews/2026-09-16-adversarial-review.md`（尤其 §§1、4、6、9、12、13）以及 `../../../reviews/2026-09-16-evidence/` 的 README、manifest、result-comparison、原始输出和哈希清单。review 审查提交为 `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57`；本次复制源提交不同，不能混为一次运行。

| Issue | 后续正文处理 | 验收边界 |
| --- | --- | --- |
| Non-triviality（M1、§4） | 以 M-semantics 的 message-level control 不蕴含 party-level distinction 为最强结果，解释受控比较为何值得研究 | 14 个 model-property outcomes 不是 14 项独立发现；不能把 guard removal/guard restoration 本身宣传成协议级发现 |
| M/I dependency（M3） | 明示 fresh message 与精确 origin 假设下 `Pτ ⇒ Mτ ⇔ Iτ`，以及 `Mτ ⇏ Pτ` | 该依赖是基于现有规则的人工推导；不是新增机器检查 lemma。message distinction 与 scoped occurrence injectivity 不是两项完全独立的新保证 |
| R witness | 保留一个匹配 Send 对应同 batch 两次接受的精确 witness | model-level counterexample；不排除无关 Send，不是合规 K-Waay protocol attack |
| P positive control | 保留 distinct-party safety 与合法双接受 non-vacuity | positive control / direct realization；不是唯一修复、最小机制或所有合法输入最终完成的证明 |
| Abstraction boundary（M2、M4） | 集中说明理想 `!Sent`、fresh `sid/m`、缺失 receiver/prekey/context 绑定、按槽接受事件与真实 session status 的差别 | 当前没有完整 source-to-model protocol refinement theorem，不能提升 witness 到协议安全失败，也不强行补完整 K-Waay security consequence |
| Rejection queries（M5） | 只称拒绝分支可达；展示 Send 与被拒 pair 没有绑定 | 本阶段不改 lemma；后续写作也不能给已有 traces 补造关联或 liveness |
| Claim/evidence consistency（M6） | 明确当前 separation 定位与历史 necessity、conditional installation 材料的区别 | 不借用 archive/M4 的结果填补 RQ-v2 的证据缺口；如需改 authority 文档须另有授权 |
| Evidence integration（M7） | 正式引入带日期、commit、hash、command、exit code 的 independent rerun 包 | 新独立复核不是 recovered original logs，结果复现不是 protocol refinement |

## 3. 独立 rerun evidence 后续整合

现有 `reviews/2026-09-16-evidence/` 已记录 **14/14 outcomes 和步数 MATCH：13 verified、1 falsified with trace**。工具为 Tamarin 1.12.0、Maude 3.5.1；三个理论 parse/prove 成功，存在原始 stdout/stderr、manifest、哈希与七个导出 witness/counterexample graphs。本次只读核查这些记录，不重新运行 prover。

后续建立 submission artifact 的 claim → model → lemma → raw output → trace 对照，固定模型及原论文版本，保留运行环境、准确命令、时间、输入/输出 hash、exit status 与运行时 Git 状态。保留现有 evidence 原件，采用可追踪的发布副本；同时明确历史 freeze 与 2026-09-16 独立复核的不同 provenance。

最终论文不能继续笼统写 “raw prover transcripts are unavailable”。当前复制正文中的既有证据可用性表述**本阶段有意原样保留**；后续优先更新 §5.6 与 Appendix C，准确区分原 freeze 没有原始日志和现在已有独立 rerun transcripts。图中 reconstructed trace 与 raw exported graph 也须分清；不能把旧示意图改称机器导出反例。

artifact 可移植性：当前精确 listings 只读引用仓库中的权威模型。未来发布独立包时，才将经过 hash 核对的模型/证据副本纳入包，并检查文内路径、匿名性与复现入口；本阶段不搬动或复制模型、日志、PDF 原文和旧 artifact。

## 4. 目标结构（仅计划，不合并文件）

1. Introduction：问题、受控方法、限定贡献。
2. K-Waay Batch Admission Problem：source condition、identity coordinates、target invariant。
3. Formal Model：common abstraction、R/M/P variants、modeling boundary。
4. Formal Analysis：relaxed counterexample、message-level non-substitutability、party-level positive control、verification summary。
5. Discussion and Limitations：适用范围、缺失 refinement、软件集成启示的证据边界。
6. Related Work：针对研究对象与证据强度定位。
7. Conclusion：保持窄命题与主张一致。

当前 Section 1--8 文件及次序全部保留；上述七节方案不表示本次已落实。

## 5. 10-page compression strategy

| Priority | 内容 |
| --- | --- |
| KEEP | K-Waay source condition；DistinctPartyPerBatch 定义；R/M/P comparison；exact relaxed witness；same-party/different-message M witness；party-level non-vacuity；model assumptions；key limitations；related-work positioning |
| COMPRESS | long threat-model prose；重复 disclaimer；重复 authentication/replay 讨论；逐 lemma 长篇解释；过长 literature survey |
| MOVE TO ARTIFACT / SUPPLEMENT | 完整 Tamarin lemma listings；raw prover logs；详细 execution traces；hashes；准确命令；长复现说明；appendix-level model listings |

将 10 页用于内容，另留最多 2 页 references；附录不能当作额外免计页数。未来优先通过删重和重组达标，不通过缩小字号、压行距或改页边距绕过 IEEE 要求。当前仍保留全部附录，不为了页数删减研究内容。

## 6. 后续适配验收

对照 [官方 CFP](https://2027.formalise.org/track/Formalise-2027-papers) 核查 IEEE 格式、页数与匿名要求；按最终结构重新检查所有图表、公式、跨节引用及 bibliography。追踪本次仅为版式采用的宽浮动体/公式换行，避免误把页数变化当作内容压缩。References 本阶段字节保持一致、不新增文献；review 的直接后续工作覆盖问题只列为未来核查事项，未声称已完成。

本阶段的交付是工作区和计划，不是论文已满足 FormaliSE novelty/relevance 标准的判定。不运行模型、不新增 lemma、不修改原 authority、不提交或推送 Git，也不自动进入下一阶段。
