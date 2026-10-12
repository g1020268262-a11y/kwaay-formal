# K-Waay 原始论文贡献恢复

## 1. 建议论文定位

建议恢复为一篇关于 K-Waay 符号安全边界及互补修复的论文：

> 对 K-Waay Figure 7 core 与 `BatchReceive` 接收生命周期进行 ProVerif/Tamarin
> 分层分析，揭示“密钥机密性与分量来源成立，但完整参数对应关系和批内
> occurrence injectivity 仍可能失败”的性质差异；验证 HMAC confirmation 与
> batch-local atomic exact-message dedup 分别修复认证确认和批内重复接受，并在
> 显式 `C_install-v2` 下评估重复接受的条件化安装影响及组合修复效果。

该定位不把批内重复输入描述为满足 K-Waay 已声明 distinct-party 前置条件的
协议攻击，也不把条件化 installation 描述为已部署漏洞。

## 2. 已完成的实质贡献

### 贡献一：建立 K-Waay 的分层符号性质体系

**贡献。** 将 K-Waay 的安全分析拆分为 P0-S symbolic secrecy、P0-O
split-KEM component origin、P1 full-parameter non-injective correspondence、
P2 matching/order 与 occurrence injectivity，以及 P3 under `C_install-v2`
conditional installation uniqueness。

**实质增量。** 该体系避免把“密钥未泄露”“一个分量有来源”“接收完成有完整
匹配发送”“同一发送只对应一次接受”“一个接受输出只安装一次”混成一个认证
结论，并为两个工具和多个事件词汇给出明确映射。

**证据。** `docs/claim-hierarchy.md`、`docs/model-mapping.md`、
`artifact/manifest/property-semantics.tsv`、`artifact/results/claim-matrix.tsv`。

### 贡献二：发现原始 core 的完整参数对应关系缺口并验证 HMAC 修复

**原始结果。** 在 `proverif/kwaay_core_final.cpp.pv` 的 no-compromise
`BASELINE` 中，sender/receiver key secrecy 均为 `true`，component origin 为
`true`，但 `RecvDone(B,A,sid,k) ==> SendDone(A,B,sid,k)` 为 `false`。

**反例性质。** `logs/final/proverif/out/BASELINE.out` 给出符号网络攻击者重组
消息分量的执行：保留诚实 `ct_s`，用公开密钥构造新的 `ct_l`、`ct_k`，接收方
完成一个没有完整匹配 `SendDone` 的转录本。该结果是 exact correspondence
failure，不是 attacker key recovery。

**修复结果。** 在
`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv` 的
`HMAC_BASELINE` 中，显式 `hmac(confirm_key(k),sid)` 使同一对应关系变为
`true`，同时保持 baseline secrecy 和 component origin。`HMAC_LEAK_SIGSK_A`
中该对应关系仍为 `false`，因此 compromise 边界清楚。

**论文价值。** 这给出一个独立于 batch replay 的核心发现：KIND-style symbolic
secrecy 和 component authenticity 不自动提供完整转录本上的 explicit
agreement/key confirmation。

### 贡献三：证明 HMAC-confirmed 消息仍可在同一批次中重复接受

**模型。** `tamarin/replay/kwaay_replay_hmac_only.spthy`。

**攻击见证。** `one_confirmed_send_two_accepts_exists` verified（17 steps）；
对应 `attack-trace.out/json/dot` 显示一个 matching `ConfirmedSend`、两个不同
slot/timepoint 的 `ConfirmedReceiverAccept`、相同
`(A,B,bid,rst,m,sid,k,tag)`，且 batch 正常完成。

**失败性质。** `confirmed_message_accepted_at_most_once` 和
`injective_confirmed_receiver_accept` 均 falsified（15 steps）。

**支撑性质。** matching existence/order、sender occurrence 消歧、正常单次接受、
正常 batch completion 和 11 项 lifecycle/state lemma 均 verified；trace 不含
sender/receiver state compromise。

**论文价值。** 该结果以机器证据表明，confirmation/authentication 与
freshness/replay prevention 是两个独立安全维度。攻击复用有效 confirmed
message，不伪造 HMAC。

### 贡献四：证明原始重复接受在 `C_install-v2` 下具有条件化安装影响

**模型。** `tamarin/impact/kwaay_impact_original.spthy`。

**正向见证。** `one_send_two_accepts_two_installs_exists` verified（28 steps）。

**被否定性质。** `unique_install_within_completed_consumer` falsified（28 steps）。

**完整结构。** 一个 matching sender occurrence 对应两个 accepts、两个 fresh
accepted-output id 和两个 installations；两次 `InstallSession` 具有相同
`A,B,sid,k`，但 local handles 不同。19 条 composition lemma 为 18 verified / 1
falsified，正常 accept/install/complete 路径可达，18/18 lower-layer formula 与
result regression 均 MATCH。

**证明边界。** 该贡献只在 `C_install-v2` 成立：固定两输出 consumer 独立处理
每个成功输出且不按 `sid/message/peer/key` 合并。仓库没有证明真实上层采用该
行为。因此贡献是 conditional composition impact，不是 deployed session
cloning。

### 贡献五：提出并验证处理前的批内原子 exact-message 去重

**修复。** `tamarin/replay/kwaay_replay_fixed.spthy` 在同一 `B,bid,rst` 内，
于任何 `ProcessSlot` 之前比较两个 exact complete messages。重复分支原子关闭
batch；不同消息分支继续执行。

**修复前后对照。**

| 性质 | original | fixed |
| --- | --- | --- |
| `one_send_two_accepts_exists` | verified | falsified |
| `same_message_accepted_at_most_once` | falsified | verified |
| `injective_receiver_accept` | falsified | verified |
| duplicate failure reachable | 未作为修复目标 | verified |
| duplicate has no accept | 不成立 | verified |
| distinct batch completion | reachable | verified |

**条件化影响对照。** `tamarin/impact/kwaay_impact_fixed.spthy` 中
`one_send_two_accepts_two_installs_exists` falsified，
`unique_install_within_completed_consumer` verified，duplicate branch 无 accepted
output/install，`normal_distinct_consumer_complete` verified。

**论文价值。** 修复不是靠拒绝所有执行获得全称性质；它阻断 exact-message
duplicate，同时保留 distinct-message batch、failure 和 consumer 路径。

### 贡献六：组合验证 HMAC confirmation 与 dedup 的互补性

**模型。** `tamarin/replay/kwaay_replay_hmac_dedup.spthy` 和
`tamarin/impact/kwaay_impact_hmac_dedup.spthy`。

**核心结果。**

- matching confirmed sender、HMAC validation 与 normal distinct confirmed
  execution 保持可达；
- same-base duplicate 即使使用不同 tag 也在 processing 前被拒；
- `one_confirmed_send_two_accepts_exists` falsified；
- confirmed-message/base-message at-most-once 与 scoped injectivity verified；
- 在 `C_install-v2` 下 duplicate accepted output/install 被阻断，unique
  installation verified；
- 两个不同有效 confirmed messages 仍可完成 batch 和 consumer；
- slot 2 HMAC mismatch 可以发生在 slot 1 accept 之后，所以不能声称所有失败
  batch 都无 partial lower-layer output。

**证据质量。** M4 Tamarin-only transparent composite 为 296/296 terminal、
296/296 MATCH、0 conflicts、0 unresolved、0 mismatches；两个 source run 的
非终态由预先冻结的 transparent selection policy 互补。ProVerif 结果是 inherited
evidence，本轮未重跑。

### 贡献七：给出可机械审计的完整 artifact

M5 冻结 expected/actual/result semantics、raw provenance、claim matrix 和 Git
blob checksum。它不新增性质，但把上述贡献的模型、公式、结果和原始证据连接为
可复核集合。这是论文可复现性贡献，而不是形式化性质贡献。

## 3. 证据总表

| 层次 | 性质或见证 | 模型 | 实际结果 | 主要原始证据 | 最大允许解释 |
| --- | --- | --- | --- | --- | --- |
| P0-S | sender/receiver secrecy | original ProVerif `BASELINE` | true / true | `logs/final/proverif/summary.txt` | no-compromise symbolic secrecy |
| P0-O | component origin | original ProVerif `COMPONENT` | true | 同上 | accepted split-KEM component 有 matching origin |
| P1 | `RecvDone ==> SendDone` | original ProVerif | false | `logs/final/proverif/out/BASELINE.out` | exact correspondence counterexample |
| P1 repair | `RecvDone ==> SendDone` | HMAC ProVerif baseline | true | `logs/variants/hmac-confirmation/proverif/summary.txt` | no-compromise non-injective correspondence restored |
| P2 | `one_send_two_accepts_exists` | original replay | verified | M3/M4 aggregate and proof outputs | same-batch exact-message duplicate accept reachable |
| P2 | `one_confirmed_send_two_accepts_exists` | HMAC-only replay | verified | `logs/tamarin-replay-hmac-only/attack-trace.*` | same confirmed message passes twice |
| P3 conditional | `one_send_two_accepts_two_installs_exists` | original impact | verified | `logs/tamarin-impact-original/attack-trace.*` | conditional two-install witness |
| P3 conditional | `unique_install_within_completed_consumer` | original impact | falsified | `unique-install-trace.*` | conditional unique installation failure |
| P2 repair | legacy duplicate witness | fixed replay | falsified | M3 composite vector | exact-message duplicate blocked in scoped model |
| P3 repair | conditional unique installation | fixed impact | verified | M3 composite vector | repair blocks conditional duplicate install |
| combined | confirmed duplicate witness | combined replay | falsified | M4 composite vector | HMAC+dedup blocks scoped confirmed replay |
| combined | conditional unique installation | combined impact | verified | M4 composite vector | combined repair blocks conditional duplicate install |

## 4. RQ-v2 作为边界贡献，而非替代主线

RQ-v2 最有价值的补充结论是：

> M3/M4 的 exact-message dedup 是针对 same-message replay/occurrence
> duplication 的修复；它不是 `DistinctPartyPerBatch` 的实现。

`same_party_different_messages_batch_exists` 的 verified 见证证明，同一参与方的
不同有效消息可以避开 exact-message dedup 并同批接受。这个结果应当放在修复
讨论或 limitations 中，用来说明两项机制的职责边界：

```text
HMAC confirmation          -> 完整参数确认/对应关系
exact-message atomic dedup -> 同批同消息 occurrence uniqueness
party admission invariant -> 同批参与方互异
```

三者不应互相替代。RQ-v2 没有上层 installation 事件，因此不能与 M2 trace 拼成
“同方不同消息导致重复安装”的新攻击。

## 5. 论文可以主张与不能主张的内容

### 可以主张

1. 原始 symbolic core 在 baseline 中保持 session-key secrecy 和 component
   origin，但 full-parameter non-injective correspondence 被反例否定。
2. HMAC confirmation 在 no-compromise ProVerif baseline 中恢复该对应关系，
   但同一 confirmed message 在同批两个 slot 的重复接受仍可达。
3. 在 `C_install-v2` 下，原始重复接受可条件化传播为相同 peer/sid/key、不同
   symbolic handles 的两个 installations。
4. batch-local atomic exact-message dedup 在固定两槽、同一 `B,bid,rst` 范围内
   阻断重复接受及其条件化安装传播，并保留不同消息的有效执行。
5. HMAC 与 dedup 组合后同时维护各自的目标，M4 结果有完整透明复合证据。
6. exact-message dedup 不等于 distinct-party admission；RQ-v2 为此提供独立见证。

### 不能主张

1. 完整 K-Waay、KIND、UNF-1KMA 或 IND-1BatchCCA 已被证明或攻破。
2. 原始 P1 counterexample 是 key-recovery attack。
3. HMAC 被伪造，或 HMAC 单独提供 replay prevention。
4. 满足 K-Waay distinct-party input discipline 的执行仍能产生 same-message
   duplicate batch。
5. `ReceiverAccept` 自动等于 `InstallSession`。
6. `C_install-v2` 是 deployed K-Waay 的真实上层行为。
7. M2 证明真实 session cloning、Double Ratchet duplication 或应用动作重复。
8. M3/M4 证明 global、cross-batch、rollback、restart 或 arbitrary-length replay
   protection。
9. RQ-v2 的 same-party/different-message witness 是 M0--M5 的 same-message replay。

## 6. 是否存在阻止论文定位成立的关键证据缺口

### 对建议的“符号安全边界、条件化影响与组合修复”定位：不存在阻断性缺口

核心反例、修复前后对照、正常路径非空性、条件化 impact、组合回归和 artifact
provenance 都已有冻结机器证据。论文无需重新运行证明器即可恢复这一主线。

### 对更强定位：存在两个阻断性缺口

1. **不能定位为“符合原始规范的 BatchReceive 攻击”。** same-message 两槽输入
   违反原文已声明的 distinct-party discipline。现有证据研究的是该条件未被维护
   时的 relaxed/integration 行为，而不是保留前置条件的执行。
2. **不能定位为“已部署会话克隆漏洞”。** `C_install-v2` 的 C7 仍是研究者给出的
   composition assumption。缺少规范或实现证据证明真实上层逐输出独立安装且不按
   `sid/message/peer/key` 合并。

此外，arbitrary-length、rollback/restart、完整 compromise matrix 和
computational reduction 是增强项，不阻止当前受限符号论文成立，但限制投稿目标和
标题措辞。

## 7. 恢复判定

原始路线已经完成了实质性研究闭环。建议恢复的主贡献不是单一
`DistinctPartyPerBatch` 语义观察，而是：

```text
认证确认缺口及 HMAC 修复
        +
HMAC 后仍存在的批内重复接受
        +
C_install-v2 下的条件化影响
        +
batch-local atomic dedup 修复
        +
HMAC 与 dedup 组合验证
        +
RQ-v2 对 distinct-party 边界的补充
```

