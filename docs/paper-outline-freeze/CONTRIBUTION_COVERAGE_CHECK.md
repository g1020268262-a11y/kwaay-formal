# M0–M5 与 RQ-v2 研究贡献覆盖检查

## 0. 审查结论先行

新大纲已经覆盖原项目完成的主研究闭环，没有因当前 Stage 6 研究范围调整而遗漏
原始 ProVerif、HMAC confirmation、Tamarin receiver/batch、HMAC-only replay、M2、
M3、M4、正常执行、RQ-v2 或 M5。

建议的篇章处理标签为：

- **正文重点展示**：构成论文因果链或关键边界，必须给模型结果和解释。
- **正文简述**：需要让读者理解方法/可信度，但不展开全部结果。
- **附录或 Artifact 保留**：必须可追踪，不占用正文主叙事。
- **不纳入当前论文**：与冻结题目正交，需给出明确理由，不代表结果无效。

## 1. M0–M5 覆盖总表

| 工作包 | 已完成成果 | 新大纲位置 | 处理级别 | 必须写出的机器证据 | 覆盖风险与控制 |
| --- | --- | --- | --- | --- | --- |
| M0 性质/映射冻结 | P0-S/P0-O/P1/P2/P3 分层；事件、模型、禁止推断；claim hierarchy | §1.3、§2.4、§6.3 | 正文简述；完整语义与矩阵放 Artifact | `artifact/manifest/property-semantics.tsv`、`artifact/results/claim-matrix.tsv` | 风险：把性质当线性强弱等级。控制：表1按保护对象和证据类型分行 |
| 原始 ProVerif core（M0 主线前置证据） | baseline secrecy/component origin 成立，`RecvDone ==> SendDone` 失败；真实密文分量重组 trace | §3.1–§3.2 | 正文重点展示 | original P1 false；sender/receiver secrecy true；component origin true；HonestRun reachable | 风险：Stage 6 只保留 admission 主线而遗漏 core。新大纲已恢复为第一结果部分 |
| HMAC ProVerif 修复 | `hmac(confirm_key(k),sid)`；no-compromise P1/secrecy/component 正面；`HMAC_LEAK_SIGSK_A` 边界 | §3.3–§3.4 | 正文重点展示 | HMAC baseline P1/secrecy true；leak target P1/receiver secrecy false | 风险：只写“加 HMAC”不写条件。表2强制 baseline/leak 并列 |
| M1 HMAC-only replay bridge | matching/source、normal path、one confirmed send/two accepts、at-most-once/injectivity 反例 | §4.2，§4.4 | 正文重点展示 | 17-step witness verified；两个 15-step properties falsified；matching/normal verified | 风险：误称“HMAC 被攻破”。控制：正文写有效 confirmed message 被重放，无 forgery |
| M2 `C_install-v2` impact | accept-output provenance、fresh aid/handle、条件化 two installs、unique-install 反例、normal consumer | §4.3–§4.4 | 正文重点展示 | two-install witness verified 28；unique install falsified 28；18/19 composition verified | 风险：写成 deployed session cloning。控制：C7/C8、`sid/aid/h` 和 conditional 标签必须正文保留 |
| M3 atomic exact-message dedup | processing 前线性决定；duplicate close；fixed replay/impact；normal distinct/failure paths | §5.1–§5.2 | 正文重点展示 | attack witnesses falsified；at-most-once/injectivity/unique/no-output/no-install verified；normal distinct verified | 风险：只报安全不报非空性，或写 global replay。表4同时列 normal/failure 与 scoped boundary |
| M4 HMAC+dedup | base-message dedup、valid-tag gate、same-base/different-tag rejection、combined replay/impact、partial-failure 边界 | §5.3–§5.4 | 正文重点展示 | combined two-accept/two-install witnesses falsified；safety/normal/mismatch verified；296/296 composite | 风险：声称 M4 重跑 ProVerif或单次296/296。正文必须写 Tamarin-only transparent composite 和 inherited P1 |
| M5 reproducible freeze | expected/actual/semantics/provenance/checksum/validation；无新性质 | §2.4、§6.3；附录/Artifact | 正文简述；附录或 Artifact 保留 | 405 expected/actual；296 Tamarin；89 inherited PV；20 out-of-scope；checksum/validation PASS | 风险：固定结构无独立实验章导致 M5 消失。控制：方法末与局限节各有一段，并在证据表脚注回指 |

### M0 文档状态说明

仓库没有独立的 `docs/milestones/M0-completion.md`，但 M0 所承担的性质定义、模型
映射和 claim boundary 已由 `docs/claim-hierarchy.md`、`docs/model-mapping.md`、
`artifact/manifest/property-semantics.tsv` 和 `artifact/results/claim-matrix.tsv` 保存。
这是一项历史文档可追溯性债务，不是尚未完成的科学研究，也不应在论文中标为
future work。

## 2. 用户指定重点逐项核查

| 指定成果 | 当前状态 | 正文位置 | 主要证据 | 处理判定 |
| --- | --- | --- | --- | --- |
| 原始 ProVerif 攻击分析 | 已完成 | §3.1–§3.2 | `kwaay_core_final.cpp.pv`；`BASELINE.out`；original summary | 正文重点展示 |
| HMAC 确认方案及验证 | 已完成 | §3.3–§3.4 | HMAC model；HMAC summary/out | 正文重点展示 |
| Tamarin receiver/batch 生命周期 | 已完成 | §1.2、§2.3、§4.4 | V6/V7 models；V7 24 项 selected verified | 正文简述；完整 lemma 表放附录 |
| 原始 relaxed two-slot replay | 已完成 | §4.1、§4.4 | original replay model；M3 regression proof outputs | 正文重点展示，但置于前置条件边界内 |
| HMAC-only 批内重放 | 已完成 | §4.2 | M1 model、summary、attack trace | 正文重点展示 |
| `C_install-v2` 条件化安装 | 已完成 | §4.3 | M2 model、aggregate、两组 trace | 正文重点展示 |
| M3 原子消息去重 | 已完成 | §5.1–§5.2 | fixed replay/impact、M3 composite、五组 trace | 正文重点展示 |
| M4 组合加固 | 已完成 | §5.3–§5.4 | combined models、M4 composite、五组 trace | 正文重点展示 |
| 正常执行可达性 | 已完成 | §3.1、§4.2–§4.4、§5.2–§5.4 | HonestRun；normal accept/batch/consumer；normal distinct traces | 正文重点展示，防止真空性 |
| RQ-v2 参与方互异 | 已完成 | §6.1–§6.2 | R/M/P models；14/14 MATCH；trace audit | 正文重点展示，作为修复职责边界 |
| M5 可复现性 | 已完成 | §2.4、§6.3、附录/Artifact | result contract、raw provenance、checksums、validation | 正文简述；Artifact 重点保留 |

所有上述条目都已有历史机器结果，不得在正式论文中写为“计划验证”“有待证明”或
“未来将运行”。

## 3. 正常执行与失败处理覆盖

安全修复必须同时显示 attack blocked、normal path reachable 和 failure behavior。
新大纲的覆盖如下：

| 语义目标 | 机器结果 | 新大纲位置 | 保留理由 |
| --- | --- | --- | --- |
| ProVerif HonestRun | original/HMAC baseline 可达 | §3.1、§3.4 | 排除 correspondence/secrecy 的明显真空解释 |
| original normal single accept/batch | verified | §4.1、§4.4 | 证明 relaxed theory 可执行 |
| HMAC-only normal confirmed accept/batch | verified | §4.2 | 证明 HMAC gate 并未阻断正常 confirmed path |
| M2 normal one accept/install 与 consumer | verified | §4.3 | 证明条件化 consumer 非空 |
| M3 duplicate failure | verified | §5.1–§5.2 | 证明 duplicate 输入进入明确失败分支，而非从模型消失 |
| M3 distinct batch/consumer | verified | §5.2 | 证明 dedup 不拒绝所有 batch |
| M3 distinct slot1/slot2 failure | verified | §5.2、§6.3 | 限定“duplicate branch atomicity”而非所有 failure 无 partial output |
| M4 two-distinct-valid confirmed batch/consumer | verified | §5.3–§5.4 | 证明组合修复非真空且保持目标功能 |
| M4 slot1/slot2 HMAC mismatch | verified | §5.3–§5.4 | 说明 slot2 failure 可晚于 slot1 accept |
| RQ-v2 P-semantics distinct-party batch | verified | §6.2 | 证明 party admission 的正面结果不是拒绝全部 batch |

结论：正常执行可达性没有被 Stage 6 范围调整遗漏，并已被安排为正文解释的一部分，
而不是仅留在日志中。

## 4. RQ-v2 与主线的整合完整性

RQ-v2 在本文中承担“修复边界检查”，不替代 M0–M5 主线：

| 机制 | 它实际约束的坐标 | 已验证作用 | 仍不保证 |
| --- | --- | --- | --- |
| HMAC confirmation | `k,sid,m,tag` 的完整确认 | no-compromise P1；combined model 中 valid-tag gate | same-batch occurrence uniqueness、party uniqueness |
| exact-message atomic dedup | 同一 `(B,bid,rst)` 内 exact base message `m` | 阻断相同消息双 accept/条件化双 install | same party 的不同消息、跨批/global replay |
| `DistinctPartyPerBatch` | 同一 batch 不同 slot 的 party `A` | P-semantics 拒绝 same-party 并保留 distinct-party batch | HMAC agreement、消息内容唯一、上层 installation |

必须保留的 RQ-v2 结果包括：

- R-semantics：one-send/two-accept reachable、injectivity falsified；
- M-semantics：exact-message rejection 与 scoped injectivity verified，但
  `same_party_different_messages_batch_exists` verified；
- P-semantics：same-party rejection、accepted-party distinctness 与正常
  distinct-party batch均 verified。

不允许的整合方式：

- 把 RQ-v2 的 `ReceiverAccept(A,sid,m,bid,rst)` 与历史 replay 的
  `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` 当成同一事件签名；
- 把 RQ-v2 的 13 verified/1 falsified 计入 M4 296-target 统计；
- 把 RQ-v2 repeated-party trace 接到 M2 `InstallSession` 后面形成一条未验证攻击；
- 把 P-semantics 说成唯一可能的实现算法；它是 invariant restoration control。

## 5. M5 证据与论文可复现性覆盖

固定章节没有单独“实验与可复现性”章，因此采用双重落点：

1. §2.4 用一段说明性质定义、机器结果、raw output 和 claim matrix 由 M5 账本绑定；
2. §6.3 用一段说明 M3/M4 transparent composite、inherited ProVerif 和
   `not_run_out_of_scope` 的区别。

附录/Artifact 必须保留：

- `artifact/results/expected-results.tsv` 与 `actual-results.tsv` 的 405-row contract；
- `claim-evidence.tsv`、`claim-matrix.tsv`、`raw-to-summary.tsv`；
- Git-blob checksum、tool version、inventory 与 validation summary；
- M3/M4 source-run/composite selection provenance；
- 所有原始 stdout、proof 与 trace。

这能保留 M5 的可复现性贡献，又不会把“打包/校验”误写成新安全性质。

## 6. 建议放入附录或 Artifact 的内容

| 内容 | 处理 | 理由 |
| --- | --- | --- |
| 405-row expected/actual table | Artifact | 正文只需 claim-oriented 4 表 |
| 完整 ProVerif leak target 矩阵 | 附录/Artifact | 保留 compromise 证据，不打断主线 |
| V6/V7 全部 selected lemma | 附录 | 正文仅需状态语义和代表性质 |
| original/HMAC-only/M2 的全部 lifecycle/provenance lemma | 附录/Artifact | 核心 witness/safety 在正文 |
| M3 196-target 与 M4 296-target 完整向量 | Artifact | 正文报告透明 composite 统计和关键行 |
| M3/M4 source-run OOM/timeout/fallback 行 | Artifact，正文脚注 | 影响证据透明性，但不是协议主论点 |
| RQ-v2 14 项完整表与三个 trace JSON | 附录/Artifact | §6.2 正文保留关键 R/M/P 行 |
| tool versions、commands、hashes | Artifact | 支撑复核，不作为安全结论 |

## 7. 不纳入当前论文的现有工作

| 仓库内容 | 判定 | 理由 |
| --- | --- | --- |
| Tamarin deniability theories/results | 不纳入当前论文；Artifact 可继续保存 | peer deniability/observational equivalence 与冻结的接收端 correspondence、batch replay、dedup 主线正交；纳入会改变题目和研究问题 |
| q1 generic/analysis models | 不纳入当前论文 | 属于更一般的 confirmation/context 设计空间，不是本文 K-Waay Figure 7 + BatchReceive 的直接证据；核心 HMAC ProVerif 结果已有专用模型 |
| archived AEAD-confirmation experiment | 不纳入当前论文 | 当前冻结修复明确是 HMAC confirmation，不应混入另一修复路线 |
| FormaliSE/AROCMAG 投稿排版与图形资产 | 不纳入当前研究内容；仅可复用经核对的文字证据 | 属于历史投稿载体/版式，不是新科学结果；本任务禁止修改论文和图片 |
| 真实实现/部署推断 | 不纳入当前论文结论 | 仓库没有 implementation/refinement/deployment 证据 |

以上排除不会删除或否认这些结果，只是维持当前论文的固定题目与贡献边界。

## 8. Stage 6 范围调整后的遗漏风险

| 风险 | 若遗漏会造成的问题 | 当前大纲中的恢复措施 | 状态 |
| --- | --- | --- | --- |
| 只保留 RQ-v2，丢失 original ProVerif/HMAC | 论文退化为单一 precondition 分析 | §3 完整恢复 original/HMAC | 已消除 |
| 只写 duplicate accept，丢失 M2 conditional impact | 无法说明安全影响边界 | §4.3 单列 C_install-v2 | 已消除 |
| 只写修复，不写 M3 normal/failure | 修复可能显得真空或过度拒绝 | §5.2 强制 normal distinct/failure | 已消除 |
| 只写 HMAC+dedup 正面结论，丢失 partial-output 边界 | 夸大失败原子性 | §5.3–§5.4 保留 slot2-after-slot1 trace | 已消除 |
| 只写 message dedup，丢失 party-level constraint | 错误声称修复已满足原协议全部 admission semantics | §6.1–§6.2 保留 R/M/P | 已消除 |
| 固定结构无复现章导致 M5 消失 | 证据可信度和复核入口不足 | §2.4+§6.3+附录/Artifact 双重落点 | 已消除 |
| 把不同 `ReceiverAccept` 事件拼接 | 形成未经验证的攻击链 | 图3分层、表3条件列、§6.2 禁止拼接 | 已消除 |

## 9. 科学证据缺口与表达缺口区分

### 9.1 不属于科学缺口

- 现有论文没有按新题目和章节重写；
- M0 没有独立 completion 文件；
- 旧 Stage 6 文本偏向 RQ-v2；
- 核心图表尚未按新结构重绘；
- 完整 result vector 未进入正文。

这些都是写作、组织或可追溯性问题，不应把已经完成的验证标为 future work。

### 9.2 真正限制更强主张的证据缺口

- 缺少 `C_install-v2` C7 与真实上层消费行为的规范/实现证据；
- 缺少任意长度、跨 batch、rollback/restart/global replay theorem；
- 缺少完整 HMAC compromise material/timing 分析；
- 缺少真实 session database、Double Ratchet、application action 和部署利用证据；
- 缺少 computational proof 和 source-to-model refinement theorem；
- RQ-v2 不建模 key/output/consumer，因此不能直接证明 output-key/security-interface
  failure。

这些缺口要求限制结论强度，但不阻止当前论文定位成立。

## 10. 最终判断

**是。按冻结大纲正式重写论文，能够完整、准确地展示原项目已经完成的安全分析、
攻击发现和组合加固研究。**

成立条件是：正文坚持原始 ProVerif、historical replay/impact、M3/M4 和 RQ-v2 的
模型边界；把 M2/M3/M4 的 installation 结论保持为 `C_install-v2` 条件化；把
same-message dedup 与 distinct-party admission 分开；并在攻击被阻断的同时报告正常
与失败路径的可达性。

当前没有需要在正式重写前补做的阻断性形式化实验。更强的部署、任意长度、全局
replay、计算安全或 refinement 主张仍缺证据，但它们不属于本论文已冻结的科学主张。
