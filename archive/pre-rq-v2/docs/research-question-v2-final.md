# K-Waay RQ-v2 Research Question Freeze

**状态：** Stage 0 / Step 1 — Research Question Freeze  
**基线 commit：** `930820d8db1e101fb4cb377fb0887f6c004c02a9`  
**文档角色：** RQ-v2 的 active research authority  
**形式化状态：** 尚未创建新的 RQ-v2 `.spthy` / `.pv` 模型

---

## 1. 文档目的

本文档用于冻结 RQ-v2 在进入新一轮形式化建模之前的最高层研究约束，包括：

- 主研究问题；
- specification-level invariant；
- 目标安全性质；
- 对既有 M0–M5 证据的重新定位；
- 当前允许声称的内容；
- 当前禁止声称的内容；
- 尚未解决、且必须在新模型出现之前澄清的问题。

本文档**不冻结最终研究结论**。

它冻结的是：

> **下一阶段要研究什么，而不是下一阶段已经证明了什么。**

如果后续形式化结果与本文档中的 hypothesis 不一致，应当修改研究结论，而不是修改模型去迎合本文档。

M0–M5 的模型、日志、结果、manifest、claim mapping 和 reproducibility artifact 继续作为 frozen historical evidence 保留。本文档不修改它们的原始工具结果，只规定它们在 RQ-v2 中应如何被解释和引用。

---

## 2. 研究背景

### 2.1 K-Waay 的 `BatchReceive`

K-Waay 使用 receiver-side `BatchReceive` 来处理一组 sender inputs，并允许这些输入共享同一个 receiver-side state / reused prekey 语义。

在 specification 层，作者对一次：

```text
BatchReceive(sk_i, st_i, S)
```

给出了一个 distinct-party 输入条件：同一次 `BatchReceive` 中，不同输入元素应对应不同的 `party`。

本文档将这一条件称为：

```text
DistinctPartyPerBatch
```

或：

```text
distinct-party BatchReceive precondition
```

### 2.1.1 Specification source anchor

RQ-v2 中的 distinct-party 条件不是从当前 Tamarin 模型中推导出来的，而是直接来源于 K-Waay 的完整 specification。

主要证据锚点：

```text
K-Waay ePrint full version
Figure 10
Figure 10 之后、Theorem 1 之前的说明文字
PDF p.20
```

该处明确说明：对于给定的

```text
BatchReceive(sk_i, st_i, S)
```

调用，假设 `S` 中的各个元素对应不同的 `party`。

因此，本文后续定义的：

```text
I_spec = DistinctPartyPerBatch
```

来源于原 specification 的 natural-language precondition，而不是我们为了当前模型自行创造的假设。

### 2.2 既有 duplicate-input 证据

现有 frozen 模型：

```text
tamarin/replay/kwaay_replay_original.spthy
```

允许：

```text
同一个 modeled sender identity A
+
同一个 complete message m
+
同一个 receiver batch/state
+
两个不同 slot
```

并已经存在历史 witness：

```text
one modeled sender occurrence
        |
        +----> ReceiverAccept occurrence 1
        |
        +----> ReceiverAccept occurrence 2
```

因此，在 RQ-v2 中，这个模型被重新定位为：

```text
RELAXED-INPUT BASELINE
```

它研究的是：

> 当 specification 中的 distinct-party input discipline 没有被显式建模成 batch-admission condition 时，哪些 execution 会变得可达。

它**不是**：

```text
对满足 distinct-party precondition 的 K-Waay execution 的反例
```

也不应被描述为：

```text
K-Waay replay vulnerability
K-Waay theorem break
deployed implementation vulnerability
```

### 2.3 Integration 层的不确定性

当前仓库本身没有证据展示一个完整、公开可审计的：

```text
K-Waay caller
server batching layer
BatchReceive admission layer
upper-layer consumer
```

因此目前不能从仓库中确认：

```text
谁负责构造一次 BatchReceive 的输入；
谁决定哪些 input 属于同一个 batch；
真实 implementation 中什么对象代表 party；
谁负责检查 duplicate-party admission；
违反 distinct-party precondition 后应如何处理。
```

所以 RQ-v2 当前既不假设：

```text
真实 implementation 一定 enforce 该条件
```

也不假设：

```text
真实 implementation 一定没有 enforce 该条件
```

这个未知点本身就是 specification–integration boundary 的一部分。

---

## 3. Frozen main research question

### RQ-v2

> **How does K-Waay's stated distinct-party `BatchReceive` precondition affect occurrence-level receiver acceptance under an explicit modeled batch-admission semantics, and can an executable admission mechanism enforce that precondition while preserving valid batch behavior?**

中文解释：

> K-Waay 明确要求一次 `BatchReceive` 中的不同输入对应不同 `party`。RQ-v2 研究这个输入纪律在**显式建模的 batch-admission semantics** 中对 receiver-side occurrence-level acceptance / injectivity 起什么作用；当该 precondition 被放宽时哪些行为会变得可达；以及能否设计一个 executable admission mechanism 来实现这一 precondition，同时保留合法 batch 的正常行为。

这里故意不使用：

```text
we prove the invariant is necessary
```

因为目前新的 invariant-enforced model 尚未建立。

RQ-v2 当前研究的是：

```text
whether and how the invariant is security-critical
for the modeled occurrence-level property
```

而不是预先假定这一结论已经成立。

---

## 4. Specification-level invariant

定义：

```text
I_spec = DistinctPartyPerBatch
```

对于一次固定的：

```text
BatchReceive(sk_i, st_i, S)
```

如果：

```text
j != k
```

则要求：

```text
party(S[j]) != party(S[k])
```

写成规范化公式：

```text
forall j,k.
  j != k
  =>
  party(S[j]) != party(S[k])
```

注意：

> 这个公式是我们对论文 natural-language distinct-party precondition 的形式化 normalization，并不是声称 K-Waay 作者在原文中逐字使用了这一数学记号。

### 4.1 `I_spec` 当前只属于 specification 层

当前的：

```text
party(...)
```

只是 specification-level abstraction。

现阶段不允许直接把它定义成：

```text
message equality
session identifier equality
public-key equality
signature-key equality
account identity
server-side user identifier
modeled sender identity A
```

这些映射必须单独获得证据支持。

---

## 5. Identity-mapping boundary

这一节是 Stage 0 后续最重要的未解决问题。

现有 Tamarin 模型使用 symbolic sender identity：

```text
A
```

当前 RQ-v2 **不假设**：

```text
modeled A
=
specification-level party
=
real implementation identity
```

当前只知道：

```text
A
```

是 existing Tamarin artifacts 中用于表示 sender role / matching coordinates 的 symbolic identity。

当前关系保持为：

```text
specification-level party
          |
          |  尚未证明映射
          v
modeled sender identity A
          |
          |  implementation mapping unknown
          v
real integration identity
```

可能的 implementation-level identity 候选包括但不限于：

```text
account identity
authenticated peer identity
long-term identity key
signature-verification identity
public-key tuple
server-authenticated user identifier
other protocol-specific principal identifier
```

本文档不冻结任何一个候选作为最终答案。

### Identity-mapping rule

在 identity mapping 被正式论证之前：

> RQ-v2 必须始终区分 **specification-level party** 与 **modeled sender identity `A`**。

后续 active 文档和新模型说明不得在没有解释的情况下直接写：

```text
party = A
```

---

## 6. Target security property

RQ-v2 的主要 target property 定义为：

```text
P_accept-inj
```

即：

```text
same-batch / same-receiver-state
occurrence-level receiver injectivity
```

### 6.1 非正式含义

固定：

```text
receiver B
batch bid
receiver state rst
```

如果两个：

```text
ReceiverAccept
```

都匹配到同一个 sender occurrence，那么它们不应该是两个不同的 receiver acceptance occurrences。

概念上：

```text
SenderOccurrence S
        |
        +----match----> ReceiverAccept R1
        |
        +----match----> ReceiverAccept R2

desired:

R1 and R2 are not two distinct acceptance occurrences
```

抽象关系为：

```text
Match(S,R1) and Match(S,R2) => R1 = R2
```

但这一性质的最终 event tuple、matching coordinates 和 exact theorem syntax 尚未冻结。

### 6.2 与历史 lemma 的关系

历史 Tamarin lemma：

```text
injective_receiver_accept
```

是 bounded / same-batch / same-receiver-state occurrence-injectivity 的既有 evidence source。

但是 RQ-v2 不能直接把这个旧 lemma 当作未来 invariant-enforced model 的最终 theorem。

未来必须重新检查：

```text
sender occurrence definition
receiver occurrence definition
matching coordinates
batch/state scope
identity coordinate
non-vacuity
```

本文档目前不建立任何新的 positive theorem。

---

## 7. Current evidence classification

### 7.1 ProVerif core

角色：

```text
SECURITY-GOAL BASELINE
```

已有范围包括：

```text
symbolic session-key secrecy
split-KEM component origin
agreement / correspondence boundary
selected compromise experiments
```

这些结果在 RQ-v2 中属于 supporting background。

它们不是 distinct-party batch-admission 问题的主要 positive / negative evidence。

### 7.2 HMAC confirmation

角色：

```text
AGREEMENT / EXPLICIT KEY-CONFIRMATION EVIDENCE
```

冻结解释：

> HMAC confirmation addresses agreement/key confirmation; it is not an admission-uniqueness mechanism.

也就是说，HMAC 用于讨论 message modification / agreement / explicit confirmation 边界，而不作为：

```text
DistinctPartyPerBatch
```

的 enforcement candidate。

### 7.3 Frozen duplicate-input Tamarin model

角色：

```text
RELAXED-INPUT BASELINE
```

它研究：

```text
当 one bounded receiver batch/state
允许 repeated modeled sender/message entries
时，会有哪些 occurrence-level execution 可达
```

它不能被称为：

```text
original K-Waay vulnerability
deployed replay vulnerability
specification break
```

### 7.4 Exact-message dedup

角色：

```text
LEGACY MESSAGE-LEVEL HARDENING
```

现有 M3 建立的是：

```text
same exact complete message m
```

在其 frozen bounded scope 中被检测/拒绝。

它尚未建立：

```text
same modeled sender identity A
+
m1 != m2
```

情况下的 party-level uniqueness。

因此目前只能写：

```text
exact-message identity
!=
specification-level party identity
```

这里的 `!=` 表示“不能在没有额外论证时把二者视为同一个概念”，而不是一个已经形式化证明的数学不等式。

### 7.5 `C_install-v2`

角色：

```text
CONDITIONAL COMPOSITION / IMPACT EVIDENCE
```

所有 installation claim 都必须保持：

```text
under the modeled C_install-v2 consumer semantics
```

不能推广成：

```text
deployed K-Waay consumer
real session cloning
Double Ratchet duplication
application exploit
```

---

## 8. Hypotheses to test

以下均为待验证 hypothesis，不是 RQ-v2 已经建立的 claim。

### H1 — Relaxing the admission discipline

候选假设：

> Relaxing the specification-level distinct-party admission discipline may admit multiple receiver acceptance occurrences corresponding to one modeled sender occurrence within one receiver batch/state.

当前状态：

```text
PARTIALLY MOTIVATED BY HISTORICAL EVIDENCE
NOT YET ESTABLISHED AS A PARTY-LEVEL RQ-v2 THEOREM
```

现有 same-modeled-identity / same-message witness 只能作为一个较窄实例。

### H2 — Exact-message dedup may be insufficient

候选假设：

> Exact-message deduplication may be insufficient to implement the broader distinct-party admission condition, because two inputs may belong to the same specification-level party while carrying different complete messages.

当前状态：

```text
NOT YET ESTABLISHED
```

未来的重要 comparison case 是：

```text
same modeled sender identity A
m1 != m2
```

但这个 experiment 目前还没有作为 RQ-v2 结果运行。

### H3 — Explicit invariant enforcement

候选假设：

> A specification-faithful party-uniqueness admission mechanism may prevent the target duplicate-party acceptance behavior while preserving normal distinct-party batches and existing lifecycle/state properties.

当前状态：

```text
NOT YET ESTABLISHED
```

未来如果得到 positive result，必须同时包含：

```text
non-vacuity
normal distinct-party batch reachability
lifecycle regression
state-consumption regression
```

不能只证明 attack witness 不再出现。

---

## 9. Allowed current claims

### C0 — Specification condition

可以声称：

> K-Waay specification 对一次 `BatchReceive` 的 inputs 给出了 distinct-party precondition。

### C1 — Historical relaxed-input witness

可以声称：

> Frozen duplicate-input Tamarin artifact 允许 repeated modeled sender identity/message input 出现在同一个 bounded receiver batch/state 中，并存在 one modeled sender occurrence 对应 two receiver acceptance occurrences 的 witness。

### C2 — Interpretation boundary

可以声称：

> 因为该 frozen artifact 放宽了 specification 中的 distinct-party input discipline，所以这个 witness 应解释为 relaxed-input / integration-robustness result，而不是对满足该 precondition 的 execution 的反例。

### C3 — Exact-message dedup scope

可以声称：

> 现有 M3 dedup artifact 在其 frozen bounded scope 中实现了 exact complete-message duplicate rejection。

### C4 — No equivalence yet

可以声称：

> 当前仓库没有建立 exact-message dedup 与 specification-level party uniqueness 的等价关系。

### C5 — HMAC role

可以声称：

> HMAC confirmation addresses agreement/key confirmation; it is not a batch-admission uniqueness mechanism.

### C6 — Conditional impact

可以声称：

> `C_install-v2` 仅提供 conditional composition evidence。

---

## 10. Prohibited claims / non-claims

RQ-v2 当前不得声称：

1. K-Waay 的 security theorem 已被破坏。
2. K-Waay specification 被现有 duplicate-input trace 攻破。
3. 真实 deployed K-Waay implementation 会在一次 `BatchReceive` 中接受 duplicate parties。
4. 作者的 benchmark implementation 没有 enforce distinct-party input。
5. K-Waay server 已被证明存在漏洞。
6. 某个公开 K-Waay implementation 已被证明存在 concrete replay vulnerability。
7. 现有 exact-message dedup model 就是 specification-faithful final fix。
8. HMAC confirmation 是 replay-prevention 或 party-uniqueness fix。
9. `C_install-v2` 代表真实 deployed K-Waay consumer。
10. Duplicate `ReceiverAccept` events 已经意味着真实 Double Ratchet duplication 或真实 application exploitation。
11. Modeled sender identity `A` 已经被证明等价于 specification-level `party`。
12. `DistinctPartyPerBatch` 已经被证明 necessary、sufficient、minimal、unique 或者是唯一可能的 enforcement condition。
13. 一个 positive same-batch/same-receiver-state result 自动意味着 arbitrary cross-batch / global replay resistance。
14. Existing symbolic results 已经建立 computational KIND、IND-1BatchCCA、UNF-1KMA 或 concrete primitive security。
15. 当前仓库没有完整 implementation evidence，就等于外部不存在任何 implementation 或 enforcement。

---

## 11. Terminology discipline

### 推荐术语

后续优先使用：

```text
distinct-party BatchReceive precondition
specification-level party
modeled sender identity A
batch-admission invariant
security-critical invariant candidate
relaxed-input model
relaxed integration semantics
occurrence-level receiver acceptance
same-batch/same-receiver-state injectivity
explicit invariant enforcement
exact-message dedup hardening
conditional composition impact
```

### 在没有新证据前避免使用

```text
K-Waay replay vulnerability
protocol break
implementation vulnerability
server vulnerability
real session cloning
the fix
necessary invariant
sufficient invariant
minimal invariant
unique invariant
party = A
```

---

## 12. 什么样的结果才算 RQ-v2 有实质进展？

理想研究链条是：

```text
specification-level distinct-party condition
        |
        v
justified identity mapping
        |
        v
explicit modeled batch-admission semantics
        |
        +-----------------------------+
        |                             |
        v                             v
relaxed version                 enforced version
        |                             |
        v                             v
target bad occurrence          target property restored
reachable                      in the stated scope
                                      |
                                      v
                              normal valid batches remain reachable
```

未来有价值的 evidence 至少包括：

1. 明确并论证 specification-level `party` 与 modeled identity 之间的关系；
2. 给出 `DistinctPartyPerBatch` 的 executable admission semantics；
3. 在 relaxed model 中明确说明哪个 occurrence-level property 失败；
4. 在 invariant-enforced model 中检查该 property 是否恢复；
5. 用 exists-trace 证明 valid distinct-party batch 仍然可达；
6. 回归验证 lifecycle / state-consumption semantics 没有被新的 enforcement 破坏；
7. 证明 exact-message dedup 与 party-level admission 在语义上确实需要区分。

---

## 13. 什么结果会削弱、推翻或迫使我们修改 RQ-v2？

如果后续出现以下情况，必须修改、收窄甚至放弃当前 framing：

1. specification-level `party` 无法有意义地映射进 formal integration model；
2. 在 faithful executable encoding 的 distinct-party precondition 下，目标 duplicate behavior 仍然可达；
3. enforcement 之所以得到 positive property，只是因为它让 valid batch 也不可达；
4. 新实验只是机械地“删掉 assumption 得到反例、重新加回 assumption 得到安全”，却没有揭示任何独立的 security-property consequence；
5. matching relation 把 message identity、sender identity、sender occurrence 和 party identity 混在一起，使结果实际上只是 modeling artifact；
6. 未来 implementation evidence 表明当前 framing 错误描述了真实 `BatchReceive` integration contract；
7. 在 identity semantics 被正确冻结后，exact-message dedup 与 party-level uniqueness 的区分实际上不存在。

这一节必须保留，因为 RQ-v2 必须保持可证伪性，而不能形成：

```text
先决定结论
→
再让模型证明结论
```

---

## 14. Stage-0 freeze

### 当前已经冻结

```text
RQ-v2 main research question

I_spec = DistinctPartyPerBatch

P_accept-inj 的研究方向

frozen duplicate-input model
= relaxed-input baseline

HMAC confirmation
= agreement / key-confirmation evidence

exact-message dedup
= legacy message-level hardening

C_install-v2
= conditional composition evidence

allowed claims

prohibited claims / non-claims

terminology discipline
```

### 当前尚未冻结

```text
specification-level party 的精确定义

party -> modeled sender identity A 的映射

party -> real implementation identity 的映射

DistinctPartyPerBatch 的 exact Tamarin encoding

duplicate-party violation 的处理策略
(reject one item / fail whole batch / other)

final matching relation

final theorem syntax

same-A / different-message experiment result

final enforcement mechanism

implementation-level exploitability / impact
```

---

## 15. 新形式化模型之前的两个 Gate

在创建新的 RQ-v2 `.spthy` 之前，必须先解决以下两个问题。

### Gate G1 — Identity

> `specification-level party` 到底是什么？  
> 什么证据能够支持它与 symbolic/model identity 之间的映射？

在 G1 没有完成前，不允许直接把：

```text
party
```

写成：

```text
A
```

### Gate G2 — Executable invariant semantics

> 在 identity coordinate 被明确之后，什么样的 batch-admission rule 才能忠实表达 `DistinctPartyPerBatch`，同时又不会偷偷加入与原 precondition 无关的额外安全假设？

只有 G1 和 G2 都通过后，才进入：

```text
RELAXED
vs.
SPEC-FAITHFUL / INVARIANT-ENFORCED
```

的新 Tamarin comparison。

---

## 16. 当前一句话定位

Stage 0 / Step 1 结束时，RQ-v2 的项目定位冻结为：

> **RQ-v2 研究 K-Waay 已声明的 distinct-party `BatchReceive` input discipline 是否构成一个与 occurrence-level receiver acceptance 相关的 security-critical integration invariant candidate，并研究如何在显式建模的 batch-admission semantics 中实现该条件；这一问题与 deployed vulnerability、HMAC confirmation、exact-message dedup 以及 conditional upper-layer installation impact 明确分开。**
