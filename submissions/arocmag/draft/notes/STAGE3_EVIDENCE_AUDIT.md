# Stage 3证据审计

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_3`  
日期：2026-10-02（Asia/Shanghai）

## 1. 审计对象与方法

本审计以当前 `.spthy` 源文件为 lemma 和规则的权威依据，并逐项核对 2026-09-16 独立复核目录：

- `reviews/2026-09-16-evidence/README.md`；
- `independent-rerun-manifest.json`；
- `result-comparison.tsv`；
- 三组 parse/prove raw stdout/stderr；
- 三个 `*-traces.json`；
- `trace-audit-summary.txt`；
- `SHA256SUMS.txt`。

`SHA256SUMS.txt` 列出的 24 个证据文件全部重新计算并匹配。manifest 记录的三个模型哈希与当前源文件一致：

| 模型 | SHA-256 | 当前源文件匹配 |
|---|---|---|
| `rqv2_relaxed.spthy` | `e5129575720020aa3f509782c2052fbf2114a540d013126f5a75d316cbabaf9d` | 是 |
| `rqv2_message_dedup.spthy` | `90a196f5da5c244026596283d001376427880cd64c5bea3c6cfdfd4ccba99184` | 是 |
| `rqv2_party_admission.spthy` | `c35af64cac7f01182418cb999ea105214b8da4f2295b670a9b3733f0bd976bba` | 是 |

manifest 共记录 7 次 version/parse/prove 调用，exit code 均为 0，运行前后 worktree 状态均为空。三个 prove stdout 均报告 successful wellformedness checks。

## 2. 14项结果的来源核查

| 模型 | Lemma | 源公式类型 | Raw stdout结果 | Steps | `result-comparison.tsv` | JSON graph |
|---|---|---|---|---:|---|---|
| R | `normal_relaxed_batch_exists` | exists-trace | verified | 10 | MATCH | 有 |
| R | `one_send_two_accepts_exists` | exists-trace | verified | 13 | MATCH | 有 |
| R | `receiver_accept_has_send` | all-traces | verified | 8 | MATCH | 无需导出见证 |
| R | `receiver_accept_injective` | all-traces | falsified - found trace | 13 | MATCH | 有反例 |
| M | `repeated_message_rejection_exists` | exists-trace | verified | 4 | MATCH | 有 |
| M | `same_party_different_messages_batch_exists` | exists-trace | verified | 16 | MATCH | 有 |
| M | `accepted_batch_has_distinct_messages` | all-traces | verified | 31 | MATCH | 无需导出见证 |
| M | `receiver_accept_has_send` | all-traces | verified | 8 | MATCH | 无需导出见证 |
| M | `receiver_accept_injective` | all-traces | verified | 33 | MATCH | 无需导出见证 |
| P | `same_party_rejection_exists` | exists-trace | verified | 5 | MATCH | 有 |
| P | `distinct_party_batch_exists` | exists-trace | verified | 17 | MATCH | 有 |
| P | `accepted_batch_has_distinct_parties` | all-traces | verified | 31 | MATCH | 无需导出见证 |
| P | `receiver_accept_has_send` | all-traces | verified | 8 | MATCH | 无需导出见证 |
| P | `receiver_accept_injective` | all-traces | verified | 33 | MATCH | 无需导出见证 |

合计 14 个 model–lemma 实例：13 verified，1 falsified with trace；状态和 steps 均为 14/14 MATCH。三个 JSON 文件合计包含 7 个 graph，与两个 R 存在性见证、一个 R 反例、两个 M 存在性见证和两个 P 存在性见证对应。

## 3. 每个lemma与模型及正文的对应关系

| Lemma | 权威模型 | 正文位置 | 正文证据作用 |
|---|---|---|---|
| `normal_relaxed_batch_exists` | R | 3.1、表3 | R 基本生命周期非空，不支持目标 invariant |
| `one_send_two_accepts_exists` | R | 3.1、表3、图2 | 一个精确来源在同一 context 支持两个接受的存在性见证 |
| R `receiver_accept_has_send` | R | 3.1、表3 | 反例中的接受仍有先前精确来源 |
| R `receiver_accept_injective` | R | 3.1、表3 | batch-local exact-origin injectivity 反例 |
| `repeated_message_rejection_exists` | M | 3.2、表3 | 等消息拒绝分支可达；不绑定被拒 tuple |
| `same_party_different_messages_batch_exists` | M | 3.2、3.4、表3 | $M_\tau\not\Rightarrow P_\tau$ 的核心机器见证 |
| `accepted_batch_has_distinct_messages` | M | 3.2、3.4、表3 | M theory 的 all-traces 消息区分 |
| M `receiver_accept_has_send` | M | 3.2、表3 | 两个接受分别具有精确来源 |
| M `receiver_accept_injective` | M | 3.2、表3 | M theory 的 scoped exact-origin injectivity |
| `same_party_rejection_exists` | P | 3.3、表3 | 同参与方拒绝分支可达；不绑定被拒 tuple |
| `distinct_party_batch_exists` | P | 3.3、表3 | P 双接受路径非空 |
| `accepted_batch_has_distinct_parties` | P | 3.3、表3 | P theory 的 all-traces 参与方区分 |
| P `receiver_accept_has_send` | P | 3.3、表3 | P 接受具有精确来源 |
| P `receiver_accept_injective` | P | 3.3、表3 | P theory 的 scoped exact-origin injectivity |

## 4. R见证的关键事件

`one_send_two_accepts_exists` 的源公式绑定：

1. 一个 `Send(A,sid,m)@s`；
2. 一个 `BatchReceive(bid,rst)@b`；
3. 参数完全相同的两个 `ReceiverAccept(A,sid,m,bid,rst)@r_1/@r_2`；
4. 顺序 $s<b<r_1<r_2$；
5. 对同一 $(A,sid,m)$，任意匹配 Send 的时间点都等于 $s$。

JSON graph 显示 `CollectSlot1` 和 `CollectSlot2` 都接收 $\langle A,sid,m\rangle$，并显示一个额外的无关 `Send(~a,~sid.1,~m.1)`。因此，正文准确写为“一个唯一匹配该精确三元组的 Send”，而没有写成“整条 trace 只有一次 Send”。同一 JSON 中的 `receiver_accept_injective-case_1` graph 具有相同的两个接受事件，为 all-traces 性质提供反例。

## 5. M见证的关键事件

`same_party_different_messages_batch_exists` 的源公式和 JSON graph 共同绑定：

- `Send(A,sid_1,m_1)@s_1` 与 `Send(A,sid_2,m_2)@s_2`；
- $sid_1\ne sid_2$、$m_1\ne m_2$；
- 同一个 `BatchReceive(bid,rst)@b`；
- `ReceiverAccept(A,sid_1,m_1,bid,rst)@r_1` 与 `ReceiverAccept(A,sid_2,m_2,bid,rst)@r_2`；
- $s_1<b$、$s_2<b$、$b<r_1<r_2$。

两个接受分别绑定自己的精确发送来源，且 party 坐标均为同一个 $A$。graph 还包含一个与见证无关的额外 `Send`；正文没有把导出 graph 错写成最小 trace。该见证不支持 origin mismatch、wrong-party attribution、UKS、misbinding 或 key consequence。

## 6. P非空性见证的关键事件

`distinct_party_batch_exists` 绑定两个不同参与方 $A_1\ne A_2$、两个匹配发送、一个 batch/context 和两个有序接受事件。JSON graph 中 `AdmitDistinctParties` 记录 `Neq(~a,~a.1)`，两个 `ReceiverAccept` 分别使用这两个参与方及其对应 `sid/m`。graph 同样含有与公式无关的额外 Send，故只把 lemma 解释为“至少一个有效双接受执行可达”。它不证明所有参与方不同的批次都最终完成。

## 7. P/M/I推导依据

采用第 2 章定义的三个轨迹谓词：$P_\tau$ 为同 context 不同接受事件的 party distinction，$M_\tau$ 为 message distinction，$I_\tau$ 为同一 exact origin 的 batch-local injectivity。人工推导使用：

1. 每个 `SendMessage` 以 `Fr` 生成 fresh `sid/m`；
2. `ReceiverAccept(A,sid,m,...)` 只在完整匹配的持久事实 $!Sent(A,sid,m)$ 存在时产生；
3. `receiver_accept_has_send` 在三个模型中均经机器验证；
4. 三个谓词固定相同 $(bid,rst)$，并以 $r_1\ne r_2$ 区分两个接受事件。

在这些假设下，$M_\tau\Rightarrow I_\tau$、$I_\tau\Rightarrow M_\tau$ 和 $P_\tau\Rightarrow M_\tau$ 是人工规则推导；没有对应的单一跨理论 Tamarin lemma。$M_\tau\not\Rightarrow P_\tau$ 由 M 的 all-traces message safety 与 same-party/different-message exists-trace witness 联合支持。

## 8. 人工整理图与机器导出图的区别

机器 JSON graph 是 Tamarin constraint-system 导出，包含协议规则节点、网络推导节点以及与目标公式无关的其他 Send。图 2 设计说明只抽取公式绑定的 Send、两次收集、接纳和两个 ReceiverAccept，并用单个持久 $!Sent$ 节点解释规则复用。

因此：

- 图 2 必须标注“根据 Tamarin 见证人工整理”；
- 不得称为原始 attack graph 或最小 trace；
- 省略无关 Send 只用于可读性，不能据此改变唯一性条件的量词范围；
- 图示不增加机器结果中没有的 key、authentication 或 deployment 事件。

## 9. 证据一致性结论

未发现当前模型、raw stdout/stderr、manifest、result comparison、JSON graphs 与 Stage 3 正文之间的结果不一致。任务给出的 14 项预期状态和 steps 与原始 evidence 完全一致。

需要保留的 provenance 区分是：历史 freeze 记录与 2026-09-16 独立重跑属于不同证据来源。后者提供 raw transcripts 和 exported graphs，并确认当前抽象结果可重复；它不是历史日志恢复，也不建立 source-to-model refinement 或协议级安全结论。

**EVIDENCE_AUDIT_PASS**
