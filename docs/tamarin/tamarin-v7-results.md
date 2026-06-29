# Tamarin V7 验证结果

## 1. 模型定位

`tamarin/kwaay_splitkem_batch_dynamic_v7.spthy` 是一个固定 4 slot 的 batch lifecycle 模型。它不是 `v6` 的替代品，也不是任意长度 `BatchReceive` 模型，而是专门用来补齐 `v6` 中不适合硬塞进去的 terminal lifecycle 证明目标。

`v7` 的核心建模选择是：

```text
OpenStage0 -> AddSlot1 -> OpenStage1 -> AddSlot2 -> OpenStage2
           -> AddSlot3 -> OpenStage3 -> AddSlot4 -> OpenStage4
           -> SealBatch -> SealedStage0
           -> ProcessSlot1 -> SealedStage1
           -> ProcessSlot2 -> SealedStage2
           -> ProcessSlot3 -> SealedStage3
           -> ProcessSlot4 -> SealedStage4
           -> CompleteBatch
```

`FailSlotN` 消耗当前 sealed stage 和 `BatchEndToken`，直接进入 closed 状态，不再产生后继 sealed stage。因此 close 之后没有规则可以继续 accept slot。

## 2. 本轮验证环境

```text
tamarin-prover 1.12.0
Maude 3.5.1
WSL Ubuntu-24.04
```

复现命令：

```bash
bash scripts/prove-v7-selected.sh
```

日志目录：

```text
logs/tamarin-v7/
```

## 3. 验证摘要

`scripts/prove-v7-selected.sh` 已对以下 selected lemmas 完成验证，结果均为 `VERIFIED`：

```text
executable_four_slots_added
executable_seal_batch
executable_four_slots_processed
executable_batch_complete
executable_batch_fail
seal_requires_all_slots_added
process_requires_slot_added
process_requires_seal
complete_requires_seal
fail_requires_seal
complete_requires_all_slots_done
complete_requires_all_added_slots_processed
no_add_after_seal
no_add_after_complete
no_add_after_fail
no_slot_accept_after_complete
no_slot_accept_after_fail
no_slot_accept_after_close
batch_complete_consumes_state
batch_fail_consumes_state
batch_end_token_single_use
batch_fail_complete_exclusive
receiver_state_single_batch_end
slot_origin
```

## 4. 解决了 review 中哪些问题

### 4.1 `SealBatch` 后 slot 集合冻结

`v6` 中 `AddSlot` 依赖剩余的 `AddSlotToken`，不依赖 open phase fact。因此在 `v6` 中，seal 后如果仍有 token，理论上还可能 add slot。

`v7` 改为线性 stage：

```text
OpenStage0 -> OpenStage1 -> OpenStage2 -> OpenStage3 -> OpenStage4 -> SealedStage0
```

`SealBatch` 消耗 `OpenStage4`，之后系统中不再存在任何 `OpenStageN`，所以 `AddSlot1..4` 都无法再次触发。这个语义由以下 lemma 支撑：

```text
seal_requires_all_slots_added
no_add_after_seal
no_add_after_complete
no_add_after_fail
```

### 4.2 close 后不能继续处理 pending slot

`v6` 中 `ProcessPendingSlot` 依赖 persistent `!BatchSealedFact`，而 complete/fail 不会消耗 persistent fact，所以不适合证明 close 后不能继续 process。

`v7` 改为线性 sealed stage：

```text
SealedStage0 -> SealedStage1 -> SealedStage2 -> SealedStage3 -> SealedStage4
```

`CompleteBatch` 和 `FailSlotN` 都不会产生新的 sealed stage，因此 close 后没有规则能继续产生 `BatchSlotAccept`。这个语义由以下 lemma 支撑：

```text
no_slot_accept_after_complete
no_slot_accept_after_fail
no_slot_accept_after_close
```

### 4.3 complete 必须等待所有建模 slot processed

`v6` 依赖 `strict_batch_completion` restriction 裁剪掉未完成就 complete 的轨迹，因此不能把该性质表述成纯规则层证明。

`v7` 让 `CompleteBatch` 同时消耗：

```text
SealedStage4
Slot1DoneFact
Slot2DoneFact
Slot3DoneFact
Slot4DoneFact
BatchEndToken
```

因此 complete 的前提由规则本身保证，而不是由 restriction 保证。这个语义由以下 lemma 支撑：

```text
complete_requires_all_slots_done
complete_requires_all_added_slots_processed
```

## 5. 仍然不能夸大的地方

`v7` 是 fixed 4 slot lifecycle model，不是 arbitrary-length batch proof。

`v7` 不替代 `v6` 的 compromise/exception 建模。`v6` 仍负责 receiver/sender compromise、attacker-known key exception、partnered slot key 等性质；`v7` 只负责把 `v6` 中不收敛的 terminal lifecycle 目标拆出来证明。

论文中建议表述为：

```text
We additionally provide a fixed four-slot Tamarin lifecycle model that
proves seal-time slot freezing, complete-after-all-slots, and terminal
close properties that are intentionally separated from the bounded dynamic
batch skeleton.
```
