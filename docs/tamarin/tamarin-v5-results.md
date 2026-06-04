# Tamarin V5 Results

## 结论

`tamarin/kwaay_splitkem_batch_lifecycle_v5.spthy` 已完成 selected lemma verification。

V5 在 V4 的 batch-level state consumption 基础上，加入固定两槽 lifecycle refinement。

一句话：

```text
V4: batch complete / fail 统一消费 receiver state
V5: BatchComplete 必须等待两个 slot 都处理完成，且 close 后不再有 slot accept
V5 和 V4 的区别
V4 解决的问题

V4 关注 batch-level state consumption：

一个 batch 内多个 slot 共享 receiver state。
batch complete / fail 时统一消费 receiver state。

V4 仍有边界：

ClosedBatch 后没有完全禁止继续 slot accept。
V5 新增的问题

V5 关注 batch lifecycle ordering：

BatchComplete / BatchFail 之后不能再出现新的 slot accept。

V5 使用固定两槽模型：

Slot1Token
Slot2Token
Slot1DoneFact
Slot2DoneFact

注意：

固定两槽只是 bounded lifecycle toy model。
它不表示 K-Waay batch 只能有两个 slot。
V5 核心设计

V5 将 V4 的 generic SlotToken 改成固定两槽：

Slot1Token(B,bid,rst,idx1)
Slot2Token(B,bid,rst,idx2)

slot accept 后产生：

Slot1DoneFact(B,bid,rst)
Slot2DoneFact(B,bid,rst)

BatchComplete 必须消耗：

BatchEndToken(B,bid,rst)
Slot1DoneFact(B,bid,rst)
Slot2DoneFact(B,bid,rst)

因此：

两个 slot 都处理完成后，batch 才能 complete。

BatchFail 消耗：

BatchEndToken(B,bid,rst)
Slot1Token 或 Slot2Token

因此：

slot fail 会直接关闭 batch。
验证策略

V5 不使用 full --prove 作为成功标准。

原因：

单条关键 lemma 可以 verified；
全量 --prove 可能因为 proof search 组合爆炸而不终止。

Tamarin 的自动证明可能返回 proof、counterexample，也可能无法终止；复杂协议的 Tamarin proof search 需要人工拆分 lemma 或调整策略是常见情况。

因此 V5 的成功标准是 selected lifecycle lemmas verified。

Selected lemma 结果
lemma	result	meaning
executable_two_slots_same_batch	verified	同一个 batch/rst 下两个 slot accept 可达
executable_batch_complete	verified	batch complete trace 可达
complete_requires_both_slots_done	verified	BatchComplete 必须在 Slot1 / Slot2 都 done 后发生
no_slot_accept_after_complete	verified	BatchComplete 后不会再有 slot accept
no_slot_accept_after_fail	verified	BatchFail 后不会再有 slot accept
核心 lemma 含义
complete_requires_both_slots_done

含义：

如果 BatchComplete(B,bid,rst) 发生，
那么 Slot1Done(B,bid,rst) 和 Slot2Done(B,bid,rst) 都已经发生。

这是 V5 的核心 lifecycle 条件。

no_slot_accept_after_complete

含义：

同一个 batch complete 后，不会再出现新的 BatchSlotAccept。
no_slot_accept_after_fail

含义：

同一个 batch fail 后，不会再出现新的 BatchSlotAccept。
当前意义

V5 证明了：

固定两槽模型中，batch complete 必须等待所有 slot 成功处理；
batch complete / fail 后不会继续处理 slot；
batch lifecycle ordering 可以在 Tamarin 中表达。

这比 V4 多了一层：

V4: batch-level state consumption
V5: batch close 后禁止 slot accept
边界

V5 不是完整 BatchReceive。

V5 不建模：

任意长度 batch
真实 counter +1 / -1
PendingSlot 不存在性判断
完整 vector traversal
真实 KEM decapsulation fail
完整 KEM
完整 KDF
签名
computational KIND
UNF-1KMA / IND-1BatchCCA computational proof

V5 是 bounded lifecycle toy model，不是最终完整 batch semantics。

下一步

进入 V6：更一般的 finite slot-set / pending-done batch model 设计。

V6 目标：

从固定两槽推广到有限 slot set 的抽象表达。

但 V6 不应直接使用整数 counter。

优先考虑：

PendingSlot
DoneSlot
SealBatch

再决定是否需要进入 list / vector encoding。