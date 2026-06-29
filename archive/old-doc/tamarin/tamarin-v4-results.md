# Tamarin V4 Results

## 结论

`tamarin/kwaay_splitkem_batch_state_v4.spthy` 已跑通。

V4 在 V3 的 batch abort 模型基础上，修正 receiver state consumption 语义：

```text
V3: slot accept / fail 消耗 receiver state
V4: batch complete / fail 统一消费 receiver state

V4 使用 token 化状态建模，避免 OpenBatch -> OpenBatch 这类自循环规则导致 proof search 卡住。Tamarin 适合用 multiset rewriting 表达 stateful protocol，但这种低层状态编码需要谨慎设计，否则容易出现证明搜索困难。

V4 和 V3 的区别
V3 解决的问题

V3 关注 batch abort：

slot fail -> batch fail
BatchFail 和 BatchComplete 互斥

但 V3 仍然偏 slot-level state consumption。

V4 新增的问题

V4 关注 batch-level state consumption：

一个 batch 内多个 slot 共享同一个 receiver state。
receiver state 不在 slot accept 时消费。
receiver state 在 batch complete / fail 时统一消费。
V4 核心设计

V4 使用三个 token：

SlotToken
BatchEndToken
CompromiseToken

含义：

token	meaning
SlotToken	限制一个 batch 中可处理的 slot 数量
BatchEndToken	限制一个 batch 只能 complete 或 fail 一次
ReceiverCompromiseToken / SenderCompromiseToken / BatchCompromiseToken	限制 compromise 不无限重复

V4 删除了会导致循环的结构：

OpenBatch -> OpenBatch

改成：

slot accept 消耗 SlotToken
batch complete / fail 消耗 BatchEndToken
验证结果
lemma	result	meaning
executable_two_slots_same_batch	verified	同一个 batch/rst 下可以有多个 slot accept
executable_batch_complete	verified	batch complete trace 可达
executable_batch_fail	verified	batch fail trace 可达
batch_complete_consumes_state	verified	batch complete 会触发 receiver state consumption
batch_fail_consumes_state	verified	batch fail 会触发 receiver state consumption
batch_end_token_single_use	verified	同一个 batch 只能结束一次
batch_fail_complete_exclusive	verified	同一个 batch 不能既 fail 又 complete
receiver_state_single_batch_end	verified	同一个 receiver state 不能被最终消费两次
slot_origin_without_early_compromise	verified	无提前 compromise 时 accepted slot 有 sender origin
slot_key_known_requires_exception	verified	attacker-known slot key 必须有 exception 解释
partnered_slot_key_not_attacker_known_without_early_compromise	verified	无提前 compromise 时 partnered slot key 不会 attacker-known
核心 lemma 含义
executable_two_slots_same_batch

含义：

同一个 batch/rst 下可以出现多个 slot accept。

这是 V4 相比 V3 最关键的推进。

batch_complete_consumes_state

含义：

BatchComplete(B,bid,rst) 发生时，同步触发 ConsumeReceiverState(B,rst)。
batch_fail_consumes_state

含义：

BatchFail(B,bid,rst) 发生时，同步触发 ConsumeReceiverState(B,rst)。
batch_fail_complete_exclusive

含义：

同一个 batch 不能既 BatchFail 又 BatchComplete。
receiver_state_single_batch_end

含义：

同一个 receiver state 不能被两个 batch 结束事件重复消费。
当前意义

V4 证明了：

receiver state 可以被一个 batch 内多个 slot 共享；
receiver state 的最终消费发生在 batch complete / fail；
同一个 batch 只能结束一次；
slot-level origin / exception 性质在 batch-level state consumption 下仍然保持。

这比 V3 多了一层：

V3: batch abort / fail-complete 互斥
V4: batch-level receiver state consumption
边界

V4 不是完整 BatchReceive。

V4 不建模：

完整 batch vector traversal
所有 slot 成功才 complete
ClosedBatch 后禁止 slot accept
真实 KEM decapsulation fail
完整 KEM
完整 KDF
签名
computational KIND
UNF-1KMA / IND-1BatchCCA computational proof

尤其注意：

V4 仍未禁止 ClosedBatch 后继续 slot accept。

这是后续 lifecycle ordering refinement 的任务。

下一步

进入 V5：batch lifecycle ordering refinement。

V5 目标：

禁止 batch complete / fail 后继续出现新的 slot accept。

当前 V4 已经完成：

batch 内多个 slot 共享 receiver state
batch 结束时统一消费 receiver state

V5 将进一步处理：

slot accept 必须发生在 batch close 之前
ClosedBatch 后不能再处理 slot