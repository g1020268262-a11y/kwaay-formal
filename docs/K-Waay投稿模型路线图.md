# K-Waay：从当前仓库到可投稿模型的路线图

更新时间：2026-07-27

## 1. 总判断

当前项目已经完成了“基础模型与若干独立结果”，但还没有完成“单一、闭环、可投稿的安全故事”。

最适合把现有成果收束起来的主线如下。这里的 P0-S、P0-O、P1 与 P2
是性质与依赖结构，不是全局线性安全等级；actual M2 的 P3 under
`C_install-v2` 属于独立的 impact/composition 层。

```text
当前 original artifacts
  ├─ actual P0-S symbolic secrecy：成立
  ├─ actual P0-O component origin：成立
  ├─ actual P1 full-parameter non-injective correspondence：falsified
  └─ actual Tamarin replay P2 BatchReceive one-send → many-accepts：falsified

HMAC confirmation
  ├─ actual ProVerif P1 no-compromise baseline：established
  ├─ actual Tamarin matching existence/order：verified，但在 `HonestSession` 下主要是结构性结果
  └─ actual Tamarin P2：同一 confirmed message 在同一 batch/state 的两个 slot 重复接受可达；occurrence injectivity falsified

P3 under C_install-v2
  ├─ actual conditional one-send → two-accepts → two-installs witness：verified
  ├─ actual distinct symbolic local handles：verified witness
  └─ actual unique_install_within_completed_consumer：falsified

Batch-local atomic dedup（fixed two-slot）
  ├─ actual P2 same-B/bid/rst exact-message at-most-once：established
  ├─ actual duplicate batch：fail before ReceiverAccept / AcceptedOutput / InstallSession
  └─ actual P3 under C_install-v2：unique installation established；normal distinct consumer reachable

HMAC confirmation + batch-local duplicate rejection
  ├─ actual M4 Tamarin-only：恢复 fixed two-slot、batch-local P2 one-send-one-accept
  ├─ actual M4 Tamarin-only：在 C_install-v2 下阻断 duplicate accepted output / duplicate installation
  ├─ actual M4 Tamarin-only：保留 distinct-message batch / consumer reachability
  └─ ProVerif P0-S/P0-O/P1：引用既有 original core 与 HMAC confirmation evidence，本轮未重跑
```

这条主线能把已经做完的 ProVerif core、HMAC 变体、Tamarin batch lifecycle 和新 replay 反例串成一个贡献，而不需要继续扩展“通用 Q1 检测器”。

## 2. 状态图例

- ✅：已有模型、运行结果和可引用证据。
- 🟡：已有部分材料，但还不能作为论文定稿证据。
- ⬜：尚未完成，是后续任务。
- ⛔：有意冻结或移出论文主贡献，不再继续扩展。

当前冻结快照（2026-07-19）：M0/M0.1 已合并至 `main`（commit `b196fda`）；
M1 HMAC-only replay bridge 的 evidence commit 为
`aeb66939af5e4b229f14f1444e19b559a4f98181`，最终合并后的 `main` 快照为
`0858252d787b4c61956be583ffdade58e01655f2`。M1 模型、脚本、summary、raw logs、
attack trace 和两组 regression 均已提交，Chat 最终审查通过。M2 model/runner
baseline Commit A2 为 `841feabd908a01bdc68669ad99253a6755820389`，正式
evidence Commit B 为 `e216a86e1ac7113013e58b17cb0217374ea95ca2`；M2 已通过
Chat 审查。M3 model/runner baseline A3 为
`282532fd922f3a7f7928f3772b3325fe06785730`，transparent composite evidence
Commit B 为 `b0ff0b23977614deea8375cb95c0909be71e5c71`。M3 已完成。M4
model/runner baseline Commit A 为 `96010c72e71defc775c7c2ee99c937ff700a3227`，
Tamarin-only composite evidence Commit B 为
`740666a3abd6937b52818d0f4acaf8ea0d023c58`。M4 已完成：two complete
source runs were VALID, and the transparent composite result is 296/296
terminal, 296/296 MATCH, with 0 terminal conflicts, 0 unresolved rows, and 0
mismatches. ProVerif 的 5 个 full-mode targets 本轮明确
`not_run_out_of_scope`，只引用此前已提交和审查的 original core/HMAC
confirmation evidence。

当前唯一下一步是 M5：冻结最终可复现 artifact/result table。M5 尚未开始。

## 3. 模型总表

| 阶段 | 任务 | 状态 | 当前证据 / 缺口 | 之后怎么做 | 完成判据 | 投稿作用 |
|---|---|---:|---|---|---|---|
| 0 | 冻结论文主问题 | ✅ | `docs/claim-hierarchy.md` 已冻结性质图、P2 matching relation、same-batch/same-state 反例范围与 P3 under `C_install`；`full_message_unique_send` 和 `normal_single_accept` 的证据角色已校准 | 后续只在实际 artifact/result 变化时同步 | 不存在全局线性强度链；每个 claim 指向唯一 artifact/query/lemma；sender-occurrence disambiguation、injectivity 与 non-vacuity 不混写；局部 negative 与 global negative 的关系明确 | 防止继续无限补模型 |
| 0 | 通用 Q1 模型作为主贡献 | ⛔ | 已有通用模板，但参数依赖协议映射，不能宣称适用所有协议 | 只保留为内部诊断器 / artifact 辅助材料 | 正文最多一段说明，不再扩展协议族 | 避免稀释论文贡献 |
| 1 | ProVerif final core | ✅ | `proverif/kwaay_core_final.cpp.pv` 已运行；baseline secrecy true、component authenticity true、`RecvDone ==> SendDone` false | 不再新增功能，只做回归与文档同步 | 固定 commit、版本、命令和结果表 | 论文 baseline |
| 1 | Tamarin receiver/batch lifecycle | ✅ | V6/V7 已覆盖 compromise、slot、abort、state consumption、fixed 4-slot terminal lifecycle | 将 V6 与 V7 的职责写清，不再追求任意长度 batch | 所有选定 lemma 一键复现，论文不夸称 arbitrary-length | 状态语义支撑 |
| 1 | Paper ↔ model mapping | ✅ | 已纳入 ProVerif final core、HMAC confirmation、Tamarin V6/V7、replay original、HMAC-only replay bridge、M2 original impact/composition、M3 fixed replay/impact、M4 HMAC+dedup replay/impact 和 preliminary deniability artifacts；M4 映射记录 confirmed base message、accepted output 与 conditional install 边界 | 后续只随新增 artifact/result 同步 | 每个 claim 指向唯一模型和 lemma/query；不同 Tamarin artifact 不共用错误的对象映射；ProVerif inherited evidence 与 M4 Tamarin-only evidence 不混写 | 审稿可信度 |
| 1 | Threat / compromise matrix | ✅ | material 与 timing 已拆为正交维度；实验 ledger 记录 exact target、方向和 baseline；M4 只新增 no-compromise combined baseline 与 state/timing 边界，不扩写 material compromise | 后续里程碑只更新实际新增的 artifact/result | 每个 theorem 有明确前提；experiment 不被推广为 theorem | 防止过度声称 |
| 1 | 清理 model drift | 🟡 | `LEAK_SIGSK` 当前实际结果已按 `LEAK_SIGSK_AB` alias 记录；根 README 仍描述为早期 no-batch 模型 | M0 文档以 committed summary 为准；README 同步另行确认 | M0 无未解释结果漂移；README 更新仍为独立文档任务 | artifact 基线质量 |
| 2 | K-Waay 专用 Q1 诊断 | ✅ | `KWAAY_LIKE / ATTACKER_KEY_BAD / AUTHZ_BAD / CONFIRMED_FIX` 已运行 | 仅作为理解和回归材料；主论文使用 final core/HMAC 的真实查询 | 不再依赖模板结果支撑 K-Waay 主 claim | 辅助解释危害边界 |
| 2 | 原始 core 的 non-injective agreement gap | ✅ | final core 中带 A/B/sid/key 的 `RecvDone ==> SendDone` 为 false | 导出并人工解释最小 trace，确认事件位置和会话绑定 | trace 中每个攻击步骤都能对应 Figure 7 对象 | 既有安全边界 |
| 2 | HMAC confirmation 修复 non-injective correspondence | ✅ | HMAC baseline 中 correspondence、secrecy、component authenticity 为 true | 保留为“confirmation 修复 Q1”，不要称为 replay 修复 | baseline 与至少必要 compromise case 可复现 | 第一层修复 |
| 2 | HMAC 下的 duplicate acceptance / injectivity | ✅ | `tamarin/replay/kwaay_replay_hmac_only.spthy` 与 `logs/tamarin-replay-hmac-only/` 已提交；`confirmed_receiver_accept_has_sender`、`confirmed_message_unique_send`、正常路径和 lifecycle 均 verified；`one_confirmed_send_two_accepts_exists` verified；`confirmed_message_accepted_at_most_once` 与 `injective_confirmed_receiver_accept` 均 falsified | 冻结 M1；后续不得把 duplicate accept 写成 duplicate installation，也不得把 HMAC confirmation 写成 replay prevention | 完整 proof 终止；非空正常路径存在；同一 batch/state 的 two-accept witness 排除 sender/receiver state compromise；raw logs 与复现脚本齐全 | 把 ProVerif HMAC P1 与 Tamarin replay/occurrence 主线接起来 |
| 3 | 原始 BatchReceive 重复接受 | ✅ | `tamarin/replay/kwaay_replay_original.spthy` 已证明 same message 在同一 state/batch 的两个不同 slot 被接受；无 compromise；batch 正常 complete | 冻结 original 模型，不在其中加入 impact 或 repair | 攻击存在性、唯一 send、distinct slots、lifecycle sanity 全部自动完成 | 新问题的协议层证据 |
| 3 | 跨 batch / close 后 replay 边界 | ✅ | 当前模型已证明 receiver state 单 batch、close 后无 accept；反例限定为同一 batch duplicate input | 在论文中明确这不是 rollback、cross-batch replay 或 state reuse | attack scope 一句话可准确复述 | 避免夸大 |
| 4 | P3 under `C_install-v2` composition interface | ✅ | `tamarin/impact/kwaay_impact_original.spthy`、`tamarin/impact/README.md`、`tamarin/impact/run-impact-original.sh`、`logs/tamarin-impact-original/`、`docs/milestones/M2-completion.md` | 冻结 conditional interface；M3 复用同一边界检查 fixed impact | 19 条 composition lemmas 全部终态：18 verified / 1 falsified；provenance、fresh handle、接口封闭性、completion-gated totality 与正常路径均实际检查 | 条件化影响证据 |
| 4 | P3 conditional duplicate-install trace | ✅ | `one_send_two_accepts_two_installs_exists` verified；`unique_install_within_completed_consumer` falsified；同一 sid/key、不同 symbolic local handles | 只按 `C_install-v2` 条件化引用，不提升为 deployed/session-cloning claim | positive witness 和 negative counterexample 均为 28 steps；37/37 lemma terminal；18/18 formula/result regression MATCH | 论文条件化影响证据 |
| 4 | 影响与 K-Waay 规范的对应 | 🟡 | conditional consumer 已建模并有正式结果，但尚无仓库内规范或实现证据证明 deployed upper layer 会按 C7 独立安装每个 `BatchReceive` output | 继续寻找规范、接口或实现映射；找不到时始终保留 conditional composition 前提 | 每个影响 claim 要么有规范引用，要么明确以 `C_install-v2` 为条件 | 决定能否提升实际影响主张 |
| 5 | 修复语义选择 | ✅ | 已冻结 processing 前对同一 `B,bid,rst` 内 exact complete message `m` 的原子 pre-scan；duplicate 整 batch fail | 保持 batch-local/fixed-two-slot 边界，不推广为 global replay cache | `duplicate_batch_fail_exists` verified；duplicate 分支无 accept/output/install；distinct fail paths 仍可达 | 最小协议修复 |
| 5 | Fixed Tamarin replay model | ✅ | `tamarin/replay/kwaay_replay_fixed.spthy`、`README-fixed.md`、A3 与 closeout evidence 已提交 | 冻结模型；M4 仅在独立 combined artifact 复用 | `one_send_two_accepts_exists` falsified；`same_message_accepted_at_most_once`、`injective_receiver_accept`、`normal_distinct_batch_complete` verified | 修复实现 |
| 5 | 修复 one-send-many-accepts | ✅ | fixed replay 30/30 目标取得预期终态；transparent composite vector 196/196 MATCH | 只按 same-B/bid/rst、exact complete `m` 引用 | duplicate failure 与 distinct success/FailSlot1/FailSlot2 均有非空 trace | 核心修复结论 |
| 5 | Fixed impact under `C_install-v2` | ✅ | `tamarin/impact/kwaay_impact_fixed.spthy` 53/53 目标取得预期终态 | 保持 consumer rules 3/3 与 conditional composition 边界 | duplicate-install witness falsified；unique installation、normal distinct consumer、no duplicate output/install verified | 条件化修复影响 |
| 5 | Combined fix：HMAC + dedup | ✅ | `tamarin/replay/kwaay_replay_hmac_dedup.spthy`、`tamarin/impact/kwaay_impact_hmac_dedup.spthy`、`docs/milestones/M4-completion.md`、`logs/tamarin-m4-hmac-dedup/` | 冻结 M4；M5 只做 final artifact/result table，不重新解释为 full 301-target run | actual Tamarin-only composite：296/296 terminal、296/296 MATCH；Run 1 两个 OOM nonterminal 由 Run 2 verified fallback 补齐；Run 2 五个 timeout 目标由 Run 1 terminal 结果覆盖；ProVerif 5 targets 本轮 out of scope | combined HMAC+dedup 的 Tamarin 主证据 |
| 5 | M3 regression/composite evidence | ✅ | 两次同 A3/inputs/tools 的完整 manifest-valid 运行各有一个不同 intermittent `<<loop>>`；机械 composite 196/196 MATCH、无冲突、无 mismatch | 明确称为 transparent composite evidence；不得称为一次 clean 196/196 run | 55/55 formulas、constructors、consumer rules 3/3、Original/HMAC/M2/V6/V7/ProVerif regressions 与 5 traces 全部 MATCH/valid | 证明修复没有破坏冻结性质 |
| 5 | 修复 compromise assumptions | ⬜ | HMAC 只有一个 leak case，dedup 尚无 compromise 分析 | 只选择与论文 claim 有关的最小 compromise 集；区分认证密钥泄露与 receiver state 泄露 | 每个修复 theorem 的例外条件明确且能复现 | 防止“只在理想模型有效”质疑 |
| 6 | Symbolic deniability core diff | ✅ | core equivalence VERIFIED；negative sanity 为 EXPECTED_NON_EQUIV | 保留为强化贡献，不让它阻塞 replay 主线 | core/negative 两个结果可复现 | 可选第二贡献 |
| 6 | Malicious PoK deniability | 🟡 | executability/witness lemmas verified，但 observational equivalence TIMEOUT | replay 闭环完成后再缩减 proof search 或拆小模型 | equivalence VERIFIED，或明确降级为 limitation | 高目标强化项 |
| 6 | Big Brother / full deniability | ⬜ | 尚未完成 | 仅在主线冻结后继续 | 明确 game、opening data、simulator 与 result | 不作为当前模型冻结前置条件 |
| 7 | Computational proof sketch | ⬜ | 尚无 CryptoVerif / game proof | 对 AsiaCCS/ACNS 可先放 future work；若冲 USENIX/密码方向，再补最小 KDF hybrid / KIND sketch | 假设、game hop、symbolic↔computational边界成文 | 高目标加分，不替代影响闭环 |
| 8 | 一键复现 artifact | 🟡 | 各分支有脚本和日志，但缺一个统一入口与总结果清单 | 新增 `scripts/run-paper-artifact.sh`，固定工具版本、timeout、预期 true/false/trace | 干净环境一条命令得到完整表；失败有非零退出码 | 投稿硬要求 |
| 8 | Artifact README / claim matrix | ⬜ | 根 README 过时，结果散在多个 docs/logs | 写 installation、模型索引、预计时间、结果表、限制、论文 claim 对应 | 陌生审稿人 15 分钟内能运行一个核心结果 | Open Science / 复现性 |
| 8 | 最终模型冻结 | ⬜ | 仍有新增分支和陈旧文档 | 打 tag/commit；主模型只保留 original、hmac-only、impact、fixed/combined；历史实验归档 | 冻结后只修 bug，不再改变事件定义/安全目标 | 开始写论文的门槛 |

## 4. 必须按顺序执行的里程碑

### M0：冻结性质、主张与证据命名

产物：

```text
docs/claim-hierarchy.md
docs/threat-compromise-matrix.md
```

M0 冻结的是性质图，不是严格线性安全层级：

```text
P0-S: symbolic session-key secrecy（独立性质）
P0-O: split-KEM component origin（独立性质）
P1: 指定 artifact/event tuple 的 non-injective correspondence
P2: 同一 event vocabulary 下的 matching existence/order + occurrence injectivity
P3 under C_install: impact/composition layer；M0 快照中仅命名、当时 not modeled，
M2 已以 `C_install-v2` 条件化实例完成
```

正常路径 executability/non-vacuity 是 P2 的证据要求，不是 P2 安全公式本身。
只有相同 artifact instantiation、事件语义与参数元组下才允许写 `P2 => P1`。

当前 `injective_receiver_accept` 量化同一 `bid`、同一 `rst` 和可能不同的
`idx1/idx2`。它是 same-batch/same-receiver-state lemma；该子范围反例足以
否定更强 global one-send-one-accept，但未来同范围的 positive lemma 不能自动
提升为 arbitrary-batch/arbitrary-state injectivity。

当前 replay evidence bundle 的角色冻结如下：

- `receiver_accept_has_sender`：matching existence/order；
- `injective_receiver_accept`：same-batch/same-receiver-state occurrence injectivity，当前 falsified；
- `normal_single_accept`：至少一条 matching accept 路径可达，不排除同一 trace 中还有额外 accept；
- `normal_batch_complete`：lifecycle sanity；
- `full_message_unique_send`：在 tuple-based matching 中消除 sender occurrence 歧义，不是 P2 injectivity，也不是 replay prevention；
- `one_send_two_accepts_exists`：现有 P2 negative result 的攻击存在性 witness。

未来正向 P2 模型若沿用 tuple-based matching，必须保持 sender occurrence 可消歧；
也可以采用其他显式 occurrence-level encoding。不能把 tuple equality 自动当作
occurrence equality。

M0.1 文档已冻结；M1 已按实际 artifact 和日志完成。仓库当前仍缺少单独的
`docs/milestones/M0-completion.md` 历史记录，这一文档缺口不改变 M0 的既有
artifact 状态，也不阻塞 M1 登记。

### M1：建立 HMAC-only replay bridge ✅

目的：检查“key confirmation 修复 ProVerif P1，但本身是否提供 replay prevention /
occurrence injectivity”。以下全部来自实际 lemma 和提交日志，不是路线图预期。

| 检查项 | actual lemma / evidence | 实际结果 |
|---|---|---|
| matching existence/order | `confirmed_receiver_accept_has_sender` | `verified` |
| one-send-two-accepts reachability | `one_confirmed_send_two_accepts_exists` | `verified`，17 steps |
| same-batch/same-state occurrence injectivity | `injective_confirmed_receiver_accept` | `falsified - found trace`，15 steps |
| confirmed message at-most-once | `confirmed_message_accepted_at_most_once` | `falsified - found trace`，15 steps |
| normal-path executability / non-vacuity | `normal_confirmed_single_accept`；`normal_confirmed_batch_complete` | `verified`，12 / 18 steps |
| sender occurrence 消歧 | `confirmed_message_unique_send` | `verified`；相同完整 confirmed tuple 唯一确定 send timepoint |
| lifecycle regressions | 11 个 selected lifecycle/state lemmas | 全部 `verified` |
| compromise scope | attack witness + trace condition | 无 `CompromiseReceiverState` 或 `CompromiseSenderState`；未建立 compromise-conditioned HMAC theorem |

事件匹配坐标为 `(A,B,m,sid,k,tag)`，receiver occurrence context 为
`(bid,idx,rst)`。同一 public confirmed message
`<m,hmac(confirm_key(k),sid)>` 被放入两个不同 slot。fresh ciphertext
randomness 与 `confirmed_message_unique_send` 用于消除 sender occurrence 歧义；
该 lemma 不是 P2 injectivity，也不是 replay prevention。

`!HonestSession(A,B,rst,m,sid,k)` 是接收规则的持久来源关系，因此 Tamarin
bridge 中 matching existence/order 主要是结构性结果。这个 bridge 的独立贡献是
replay/receiver-occurrence 分析，而不是重新证明具体 KEM/KDF/HMAC origin 或
computational security。HMAC P1 的主要独立正面证据仍是 ProVerif
`HMAC_BASELINE` 的 `RecvDone ==> SendDone`。

M1 自身的结论只到 duplicate `ConfirmedReceiverAccept`，不包含
`InstallSession`，因此不能仅凭 M1 写成 duplicate installation。后续 M2 已在
独立的显式 `C_install-v2` composition model 中建立条件化 impact witness；该结果
不追溯改变 M1 的证据边界。

### M2：实现 P3 under C_install-v2 的 impact/composition 模型 ✅

M2 已用独立 theory 实现固定两输出 `C_install-v2` consumer，并从 clean Commit
A2 生成正式 evidence Commit B。以下为 committed actual results，不是路线图预期：

| 检查项 | actual lemma / evidence | 实际结果 |
|---|---|---|
| conditional one-send → two-accepts → two-installs witness | `one_send_two_accepts_two_installs_exists` | verified，28 steps |
| unique installation under completed consumer | `unique_install_within_completed_consumer` | falsified - found trace，28 steps |
| normal matching accept/install path | `normal_one_accept_one_install` | verified，22 steps |
| normal accept/install/complete path | `normal_consumer_complete` | verified，25 steps |
| composition profile | 19 composition lemmas | 18 verified / 1 falsified |
| full impact proof | 37 total lemmas | 34 verified / 3 falsified / 0 incomplete |
| frozen lower-layer formulas | `frozen-formula-comparison.txt` | 18/18 MATCH |
| lower-layer actual result vector | `lower-layer-result-comparison.txt` | 18/18 MATCH |

模型入口与证据：

```text
tamarin/impact/kwaay_impact_original.spthy
tamarin/impact/README.md
tamarin/impact/run-impact-original.sh
logs/tamarin-impact-original/
docs/milestones/M2-completion.md
```

结果只在 `C_install-v2` 下成立：consumer 在 successful `BatchComplete` 后独立
消费两个 accepted-output tokens，不按 `sid/message/peer/key` 合并或去重。仓库
没有证据证明 deployed K-Waay upper layer 必然遵循 C7，因此这里证明的是两个
不同 symbolic local handles，不是两个真实会话、Double Ratchet duplication 或
application exploit。

### M3：建立 batch-local atomic dedup 修复 ✅

M3 已在 A3 冻结以下修复语义：

```text
fixed two-slot BatchReceive 在产生任何输出前，
检查同一 B/bid/rst 中两个 exact complete message m 是否不同；
若发现重复，整个 batch 失败且不产生 ReceiverAccept、AcceptedOutput 或 InstallSession。
```

实际结果：

| 检查项 | actual lemma / evidence | 实际结果 |
|---|---|---|
| original duplicate witness | `one_send_two_accepts_exists` | falsified |
| exact-message at-most-once | `same_message_accepted_at_most_once` | verified |
| same-batch/same-state injectivity | `injective_receiver_accept` | verified |
| duplicate failure/non-vacuity | `duplicate_batch_fail_exists`; `duplicate_batch_has_no_accept` | verified |
| distinct normal completion | `normal_distinct_batch_complete` | verified |
| distinct abstract failures | `normal_distinct_fail_slot1_exists`; `normal_distinct_fail_slot2_exists` | verified |
| fixed impact witness | `one_send_two_accepts_two_installs_exists` | falsified |
| fixed conditional unique installation | `unique_install_within_completed_consumer` | verified |
| distinct consumer non-vacuity | `normal_distinct_consumer_complete` | verified |

证据为 `logs/tamarin-m3-closeout/` 中的 transparent composite evidence：两次
同一 A3/inputs/tool versions 的完整、manifest-valid 运行各在不同目标出现一次
intermittent source-saturation `<<loop>>`；机械选择得到 196/196 expected terminal，
0 conflicts、0 mismatches。没有一次单独 invocation 达到 196/196 terminal。

M3 positive lemmas 只覆盖 fixed two-slot、同一 `B,bid,rst` 和 exact complete
message `m`。不得改写为 global、cross-batch 或 rollback replay theorem。

### M4：完成 combined fix 与统一回归 ✅

用同一组性质比较：

以下表格严格区分 actual result 与 inherited evidence：

| 性质 | Original | HMAC only | Dedup only | HMAC + dedup |
|---|---:|---:|---:|---:|
| P0-S symbolic secrecy | actual: true | actual ProVerif baseline: true；Tamarin bridge 未建模 secrecy | fixed replay 未建模 secrecy；M3 ProVerif regression MATCH | inherited ProVerif evidence only；M4 Tamarin-only run 未重跑 ProVerif |
| P0-O component origin | actual: true | actual ProVerif component target: true；Tamarin bridge 未独立建模 concrete origin | fixed replay 未独立建模 concrete origin；M3 ProVerif regression MATCH | inherited ProVerif evidence only；M4 Tamarin-only run 未重跑 ProVerif |
| P1 non-injective exact-parameter correspondence | actual: false | actual ProVerif baseline: true；Tamarin matching existence/order verified 但在 `HonestSession` 下主要为结构性结果 | dedup-only 不恢复 original ProVerif P1 | inherited ProVerif HMAC evidence；M4 Tamarin records confirmed-send/confirmed-accept matching, not a new ProVerif run |
| P2 one-send-one-accept / injectivity | actual replay: false | actual HMAC-only replay: false（same-batch/same-state） | actual fixed two-slot same-B/bid/rst exact-message result: true | actual M4 Tamarin-only：fixed two-slot same-B/bid/rst exact base-message result true |
| P3 under `C_install` unique installation | actual M2: falsified under `C_install-v2`; conditional duplicate-install witness verified | not modeled | actual fixed impact under `C_install-v2`: verified；duplicate-install witness falsified | actual M4 Tamarin-only：duplicate accepted output/install blocked under `C_install-v2`；distinct consumer reachable |
| batch lifecycle / atomic close | actual selected lifecycle lemmas: true | actual selected HMAC-bridge lifecycle lemmas: true | actual selected fixed lifecycle/dedup lemmas: true | actual M4 Tamarin-only：duplicate rejection atomic；slot-2 mismatch after slot-1 accept reachable |

M4 的 positive 结果只覆盖 fixed two-slot、同一 `B,bid,rst` 和 exact complete
base message `m`。same-batch/same-state positive lemma 不能自动作为 global
injectivity theorem。M4 also records the important negative boundary: slot 2
can fail after slot 1 has produced a confirmed accept, so the artifact must not
be summarized as “all failed batches have no partial output.”

M4 evidence is `logs/tamarin-m4-hmac-dedup/`, with `evidence_scope=tamarin-only`.
The canonical Tamarin-only matrix has 296 targets. Source Run 1 and Source Run 2
are both `VALID` complete invocations, and the transparent composite result is
296/296 terminal and 296/296 MATCH. The five ProVerif full-mode targets were not
run in this evidence round; the ProVerif story continues to cite the previously
committed original core and HMAC confirmation summaries.

### M5：Artifact freeze

必须具备：

```text
一个总入口脚本
一个工具版本文件
一个 expected-results 表
original/impact/fixed 的自动 trace 或 lemma 结果
paper ↔ model ↔ query 映射
所有 known timeout / limitation 的显式记录
```

达到 M5 后，模型才算“可以开始写投稿论文”。

## 5. 投稿门槛

### AsiaCCS / ACNS / Journal of Computer Security 等现实目标

不可缺少：

```text
M0 + M1 + M2 + M3 + M4 + M5
```

即：原问题、条件化影响、最小修复、修复证明、回归和可复现 artifact 必须闭环。Deniability 与 computational proof 可作为强化或 future work。

### USENIX Security / 更高目标

除上述全部内容外，还应至少补强一项：

```text
1. 用 K-Waay 规范或实际集成方式支撑 session-install impact；或
2. 更完整的 malicious deniability；或
3. computational proof sketch；或
4. 对相邻协议/实现进行系统性对照，说明该 batch injectivity 问题不是纯 toy artifact。
```

仅有 symbolic counterexample 和简单去重修复，通常不足以支撑高水平系统安全投稿。

## 6. 每次工作的停止规则

为避免做到一半忘记后续，每次只做一个里程碑，并在结束时更新这四项：

```text
状态：⬜ / 🟡 / ✅
证据：模型路径 + query/lemma + 日志路径
结论：能声称什么 / 不能声称什么
下一步：唯一的后继任务
```

任何任务只有同时满足以下条件才能打 ✅：

```text
模型存在
查询定义正确
工具实际运行完成
结果符合或明确修正研究判断
非空性 / executability 检查通过
文档记录假设和限制
可由脚本复现
```

## 7. 当前唯一下一步

M4 已完成并登记 Tamarin-only transparent composite evidence。当前不要把
`C_install-v2` 条件化结果提升为 deployed behavior，也不要把本轮 evidence 写成
full 301-target run 或 ProVerif rerun。

当前唯一下一步是 M5：

```text
冻结最终可复现 artifact/result table 与 paper-facing artifact bundle。
```

M5 尚未开始。M4 的 Tamarin-only 296-target evidence 已完成；ProVerif 5 个
targets 本轮未运行，仍引用既有 original core/HMAC confirmation evidence。

## 8. Venue 规格依据

- USENIX Security 2027 要求 finished, complete papers，正文上限 13 页，并要求 Open Science appendix 与投稿 artifact；范围包括安全协议和已部署密码协议分析：<https://www.usenix.org/conference/usenixsecurity27/call-for-papers>
- ACM AsiaCCS 2027 包含 Formal Methods 与 Applied Cryptography track，要求结果对一般安全研究者可理解且有实际安全联系；正文上限 12 页，并要求 Open Science appendix：<https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html>
- ACM TOPS 强调对安全/隐私系统的构造、评估、应用或运行具有实际相关性：<https://dl.acm.org/journal/tops/author-guidelines>
