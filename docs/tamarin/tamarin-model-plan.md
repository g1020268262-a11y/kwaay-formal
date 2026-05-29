# Tamarin Model Plan

## 目的

这个文件记录 K-Waay Tamarin 阶段的建模与分析计划。

当前主线状态：

```text
ProVerif core symbolic stage completed.
Tamarin state / partnering stage starts here.
```

ProVerif 阶段已经覆盖：

```text
K-Waay Figure 7 core
public-channel symbolic model
single receive approximation
baseline secrecy
compromise experiments
sender-side exception sanity check
split-KEM component authenticity
```

Tamarin 阶段不重复 ProVerif 的工作。Tamarin 的目标是补充 ProVerif 不自然表达的内容：

```text
state consumption
compromise ordering
partnered / unpartnered session
BatchReceive slot
receiver-side exception
```

## 1. Tamarin 阶段的核心问题

当前 ProVerif 已经发现：

```text
RecvDone ==> SendDone: false
SenderKey secrecy: true
ReceiverKey secrecy: true
SplitKemAccepted ==> SenderSplitKemComponent: true
receiver_skem_sk compromise: sender true, receiver false
sender_skem_sk compromise: sender true, receiver false
```

这些结果说明：

1. Figure 7 core 不满足 full-message exact agreement；
2. baseline secrecy 仍然成立；
3. split-KEM component authenticity 在 symbolic model 下成立；
4. receiver-side false 需要更精细地区分 partnered / unpartnered 和 state compromise；
5. ProVerif 不适合自然表达 state consumption 和 compromise ordering。

因此，Tamarin 阶段要回答：

```text
receiver state 是什么时候生成、使用、消耗的？
compromise 是发生在 accept 前还是 accept 后？
receiver accept 是否有 sender partner？
receiver-side key leakage 是否属于 unpartnered bad case？
BatchReceive 的每个 slot 如何对应 sender component？
```

## 2. 当前不做什么

Tamarin 第一阶段暂时不做：

```text
完整 KEM IND-CCA
完整 KDF 3PRF
完整签名证明
完整 computational KIND
real-or-random TEST oracle
UNF-1KMA computational proof
IND-1BatchCCA computational proof
Theorem 1 advantage bound
```

这些内容后续更适合 CryptoVerif 或手工 computational proof。

Tamarin 阶段先处理：

```text
状态
顺序
配对
批处理组件
例外条件
```

## 3. V0 模型: split-KEM component + state lifecycle

第一版 Tamarin 模型只建最小骨架：

```text
A 生成 split-KEM component
B 接受 split-KEM component
B 的 receiver state 被使用
state 可以被 compromise
state 使用后被消费
```

暂时不建完整 K-Waay。

建议模型文件：

```text
tamarin/kwaay_splitkem_state_v0.spthy
```

### V0 主要对象

抽象对象：

```text
A
B
receiver state
sender state
component
key
```

可以先不建真实 KEM，只用抽象 term 表达：

```text
ct_s
K_s
state
```

### V0 主要事件

建议 action facts：

```text
SenderComponent(A,B,cts,Ks)
ReceiverAcceptsComponent(B,A,cts,Ks)
CompromiseReceiverState(B,st)
CompromiseSenderState(A,st)
UseReceiverState(B,st)
ConsumeReceiverState(B,st)
```

### V0 主要状态 facts

建议区分：

```text
!PublicKey(A,pk)
ReceiverState(B,st)
SenderState(A,st)
UsedReceiverState(B,st)
```

其中：

```text
ReceiverState(B,st)
```

应优先设计为 linear fact，用来表达 state consumption。

### V0 目标 lemma

V0 目标不是证明完整 secrecy，而是证明事件关系和状态生命周期。

建议第一批 lemmas：

1. executability：

```text
存在 honest sender component 和 receiver accept 的 trace。
```

2. state single-use：

```text
同一个 receiver state 不能被消费两次。
```

3. compromise ordering：

```text
如果 forged receiver accept 没有 sender origin，那么必须存在 accept 前的相关 state compromise。
```

4. component origin：

```text
如果 receiver 接受某个 component，且相关 state 没有在 accept 前 compromise，那么该 component 必须来自 sender origin。
```

## 4. V1 模型: receiver-side exception candidate

V1 在 V0 基础上研究 receiver-side false。

ProVerif 中已有结果：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false

sender_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

Tamarin 要进一步区分：

```text
compromise before accept
compromise after accept
partnered receiver session
unpartnered receiver session
```

### V1 目标

尝试形成 receiver-side exception theorem candidate：

```text
如果 receiver-side key 被 attacker 知道，
那么原因应属于以下之一：

1. receiver session 是 unpartnered bad case；
2. receiver_skem_sk 在 accept 前泄露；
3. sender_skem_sk 在 accept 前泄露；
4. full receiver decapsulation secrets 在关键事件前泄露；
5. session 不 fresh。
```

当前这只是 theorem candidate，不是最终 theorem。

### V1 需要新增的概念

```text
Partnered(A,B,s,k)
UnpartneredReceiver(B,A,s,k)
ReceiverKey(B,A,s,k)
AttackerKnowsKey(k)
```

但不要一开始就把 `Partnered` 写死成一对一 exact agreement。

要优先考虑：

```text
sender session <-> receiver component
```

而不是：

```text
entire receiver session <-> one sender session
```

## 5. V2 模型: BatchReceive slot model

V2 再进入 BatchReceive。

不要一开始建真实向量，可以用 batch slot facts 近似：

```text
Batch(B,bid)
BatchSlot(bid,index,A,msg)
BatchOutput(bid,index,k)
BatchFail(bid)
```

### V2 目标

表达：

```text
一个 receiver batch 可以包含多个 sender component。
每个 sender session 只对应 receiver batch 中的某个 slot。
```

核心关系：

```text
sender session <-> receiver batch component
```

而不是：

```text
entire receiver session <-> one sender session
```

### V2 需要表达的语义

```text
batch input slots
batch output slots
batch abort behavior
receiver vector partner identifiers
receiver vector key identifiers
state reuse within one batch
state consumption after batch
```

特别是：

```text
如果 batch 中任意 component decapsulation 失败，
整个 batch 返回 bottom。
```

## 6. V3 模型: compromise ordering and freshness approximation

V3 研究更细的 compromise ordering。

需要表达：

```text
compromise before Send
compromise after Send
compromise before Receive
compromise after Receive
compromise after state consumption
```

目标是区分：

```text
能够解释攻击的 compromise
不能解释过去攻击的 late compromise
```

这一步接近 freshness，但仍是 symbolic / trace-level approximation，不是 computational KIND。

## 7. 推荐执行顺序

推荐顺序：

```text
Step 1: 写 V0 split-KEM component + state lifecycle
Step 2: 证明 state single-use 和 component origin lemmas
Step 3: 加入 compromise before / after accept
Step 4: 形成 receiver-side exception candidate
Step 5: 建 BatchReceive slot model
Step 6: 再考虑更完整 freshness approximation
```

不要直接从完整 K-Waay BatchReceive 开始。

## 8. 第一版 `.spthy` 文件计划

建议新建：

```text
tamarin/kwaay_splitkem_state_v0.spthy
```

第一版只包含：

```text
builtins
abstract function symbols
state generation rule
sender component rule
receiver accept rule
receiver state compromise rule
sender state compromise rule
state consumption rule
executability lemma
state single-use lemma
component origin lemma
```

第一版不包含：

```text
完整 KDF
完整 KEM
完整签名
完整 BatchReceive
完整 receiver-side exception theorem
```

## 9. 成功标准

V0 成功标准：

1. 模型能被 Tamarin 打开；
2. honest execution trace 存在；
3. receiver state 不能重复消费；
4. 没有 early compromise 时，receiver accepted component 有 sender origin；
5. 有 early compromise 时，可以出现 forged / unpartnered receiver accept trace。

V0 不是最终安全证明，而是 Tamarin 建模语义验证。

## 10. 当前总判断

当前阶段路线是：

```text
ProVerif:
已完成 Figure 7 core symbolic analysis。

Tamarin:
从 split-KEM component + state lifecycle 开始，
逐步进入 receiver-side exception 和 BatchReceive。

CryptoVerif / hand proof:
后续再处理 computational KIND、UNF-1KMA、IND-1BatchCCA 和 advantage bound。
```
