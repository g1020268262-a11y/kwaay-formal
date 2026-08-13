# K-Waay Tamarin 与可否认性模型审稿式评审建议

## 0. 结论先行

当前 `tamarin/kwaay_splitkem_batch_dynamic_v6.spthy` 可以作为 `K-Waay` 的 `BatchReceive` 状态机骨架，已经有一组 selected lemmas 支撑 `AddSlot -> SealBatch -> ProcessSlot -> Complete/Fail` 的基本生命周期、slot 来源、receiver-side exception 和 batch close 互斥。

但是，从会议或期刊审稿标准看，它还不能被表述为完整的 `K-Waay` 形式化证明。它更准确的定位应是：

```text
K-Waay Figure 7 core 的 symbolic batch/state/lifecycle abstraction。
```

三份可否认性模型：

```text
tamarin/kwaay_deniability.spthy
tamarin/kwaay_deniability_with_proof
tamarin/kwaay_deniability_advanced_BigBrother
```

这三份旧模型更像是“可否认性直觉的 toy equivalence sketch”，不能直接作为论文中的 formal deniability proof。核心原因不是 `diff` 用错了，而是模型把最难的部分用方程直接假设掉了，没有把 `K-Waay` 的完整消息、状态、对手能力、注册/证明、泄露视图和 simulator game 结构建模出来。

本轮已新增独立的 `kwaay_deniability_core_diff.spthy` / `kwaay_deniability_malicious_pok_diff.spthy` / `kwaay_deniability_negative_sender_secret_diff.spthy`。其中 core public-transcript observational equivalence 已 verified，negative sanity 已按预期 falsified，malicious PoK 的 witness lemmas 已 verified，但 malicious observational equivalence 仍 timeout。

建议论文/投稿中现在只能谨慎声称：

```text
我们已经完成 K-Waay core 的 symbolic secrecy/agreement boundary 分析，
并用 Tamarin 验证了 receiver-side state、batch slot、batch close lifecycle 的若干 trace properties。
```

暂时不要声称：

```text
已经证明完整 K-Waay。
已经证明完整 deniability。
已经证明 Big Brother model 下的 1-out-of-2 deniability。
已经证明 computational KIND / UNF-1KMA / IND-1BatchCCA。
```

## 1. 本次评审依据

本次评审阅读了以下本地文件：

```text
tamarin/kwaay_splitkem_batch_dynamic_v6.spthy
tamarin/kwaay_splitkem_batch_dynamic_v7.spthy
tamarin/kwaay_deniability.spthy
tamarin/kwaay_deniability_with_proof
tamarin/kwaay_deniability_advanced_BigBrother
docs/model-mapping.md
docs/paper/threat-model.md
docs/tamarin/tamarin-v6-results.md
docs/tamarin/tamarin-v7-results.md
docs/tamarin/tamarin-deniability-results.md
archive/pre-rq-v2/docs/tamarin/tamarin-stage-summary.md
logs/tamarin-v6/summary.txt
logs/tamarin-v6/*.out
logs/tamarin-v7/summary.txt
logs/tamarin-v7/*.out
logs/tamarin-deniability/summary.txt
logs/tamarin-deniability/*.out
```

同时对照了 `Tamarin` 官方手册中与本任务直接相关的部分：

- [Property Specification](https://tamarin-prover.com/manual/master/book/007_property-specification.html)：`trace properties`、`exists-trace`、`all-traces`、`diff`、`observational equivalence`、`restriction`。
- [Protocol Specification using Rules](https://tamarin-prover.com/manual/master/book/005_protocol-specification-rules.html)：`In`、`Out`、`Fr`、linear facts、persistent facts、规则执行语义。

本轮后续已通过 WSL Ubuntu-24.04 现场调用 `tamarin-prover 1.12.0` 与 `maude 3.5.1`。恢复后的 `tamarin/kwaay_splitkem_batch_dynamic_v6.spthy` 可以通过 source saturation，`executable_add_slot` 在约 3 秒内 verified。对 `v6` 进行规则层 strict lifecycle 硬化的多个尝试均在 `[Saturating Sources] Step 1 (Max 5)` 阶段超过 75 到 90 秒未结束，因此本报告把这些尝试记录为不适合直接塞入 `v6` 的失败方向。作为替代，本轮新增 `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`，并用 `scripts/prove-v7-selected.sh` 验证了 24 个 fixed-slot lifecycle selected lemmas，结果均为 `VERIFIED`。

## 2. 对 `kwaay_splitkem_batch_dynamic_v6.spthy` 的审稿意见

### 2.1 已经做得比较好的地方

`v6` 的优点很明确：

```text
CreateBatch
AddSlot
SealBatch
ProcessPendingSlot
CompleteSealedBatch
FailSealedBatch
```

这些规则把 `BatchReceive` 从固定两个 slot 的 toy model 推进到 bounded dynamic skeleton。相比早期模型，`v6` 更接近论文中 batch lifecycle 的形式。

已有 selected lemmas 覆盖了：

```text
slot add 可达
seal 可达
process slot 可达
complete/fail 可达
process 必须来自已 add 的 slot
process 必须发生在 seal 后
complete/fail 必须发生在 seal 后
batch complete/fail 消费 receiver state
batch end token 单次使用
batch fail 与 complete 互斥
无 early compromise 时 slot 有 sender origin
attacker-known slot key 必须落入 exception
无 early compromise 时 partnered slot key 不被 attacker 知道
```

这些性质对论文有价值。它们证明了 `K-Waay` 中一个重要工程语义：receiver state 不是无约束重复使用的资源，batch close 是有生命周期约束的，receiver-side key leakage 需要被分类为 unpartnered 或 compromise bad case，而不是直接解读为 honest key recovery。

### 2.2 当前仍是 `v6` 边界：`SealBatch` 没有真正冻结 slot 集合

当前 `AddSlot` 只依赖：

```tamarin
AddSlotToken($B, bid, rst)
In(<$A,$B,cts_in>)
Fr(~idx)
```

它不依赖 `OpenBatch`，也不检查 batch 是否已经 sealed 或 closed。因此，只要 `CreateBatch` 生成的 4 个 `AddSlotToken` 没有用完，理论上可以出现：

```text
CreateBatch
SealBatch
CompleteSealedBatch
AddSlot
```

或者：

```text
CreateBatch
AddSlot
SealBatch
FailSealedBatch
AddSlot
```

这和 `AddSlot -> SealBatch -> ProcessSlot -> Complete/Fail` 的生命周期叙述不完全一致。审稿人会问：如果 seal 表示 batch input vector 已经固定，为什么 seal 之后还能 add slot？

本轮尝试过把该问题直接在 `v6` 中修掉，但实测不适合。尝试过的方案包括：

```text
OpenBatch / SealedBatch / ClosedBatch 线性 phase fact。
SealToken 在 AddSlot 中消耗并重放。
OpenCount0..4 -> SealedCount0..4 单向 bounded counter。
```

这些方案都能表达更严格的 seal 语义，但会让 Tamarin 在 source precomputation 阶段卡住。尤其是 `AddSlot` 中消耗并重放同一个线性 phase fact 的写法，会制造 source saturation 很难处理的自循环；而拆成 bounded count 后，规则数量和 pending/source 匹配仍会让 `v6` 在 `[Saturating Sources] Step 1` 不收敛。

因此，当前 `v6` 保持为可验证的 bounded dynamic skeleton，不再声称已经证明 “seal 后 slot 集合冻结”。如果论文需要这个 claim，不应继续压进 `v6`，而应引用本轮新增的 fixed-slot lifecycle 模型 `v7`。`v7` 通过线性 `OpenStage0..4 -> SealedStage0` 阶段建模，已经证明 `seal_requires_all_slots_added`、`no_add_after_seal`、`no_add_after_complete` 和 `no_add_after_fail`。

### 2.3 当前仍是 `v6` 边界：`FailSealedBatch` 后仍可能处理其他 pending slots

当前 `ProcessPendingSlot`、`ForgedProcessAfterReceiverStateCompromise` 和 `ForgedProcessAfterSenderStateCompromise` 只依赖 persistent fact：

```tamarin
!BatchSealedFact($B,bid,rst)
```

而 `FailSealedBatch` / `CompleteSealedBatch` 不会消耗该 persistent fact。因此，同一个 batch 在 close 后仍可能处理其他 pending slot。已有 `batch_end_token_single_use` 只能证明 close action 只发生一次，不能证明 close 后没有继续 accept/process。

本轮尝试过三类修复：

```text
1. OpenBatch / SealedBatch / ClosedBatch 线性 phase fact。
2. 固定 slot1..slot4，加 DoneSlotFact 并让 Complete/Fail 枚举所有 slot 状态。
3. OpenCount0..4 / SealedCount0..4 bounded counter。
```

实测结果一致：`--parse-only` 可以通过，但任意最小 lemma，例如 `executable_add_slot`，都会卡在 source saturation 第一阶段。因此没有把这些结构留在 `v6` 中。

审稿层面的处理方式应写成：

```text
v6 证明 batch close 的单次性和 selected lifecycle ordering。
v6 不证明 close 后同一 batch 不能继续 process pending slot。
该性质已由 fixed-slot lifecycle v7 补证。
```

`v7` 中 `ProcessSlot1..4` 依赖线性 `SealedStageN`，而 `CompleteBatch` 和 `FailSlotN` 都不再产生后继 sealed stage。因此 close 之后没有规则可以继续产生 `BatchSlotAccept`。对应已验证 lemma 是 `no_slot_accept_after_complete`、`no_slot_accept_after_fail` 和 `no_slot_accept_after_close`。

### 2.4 当前仍依赖 restriction：`strict_batch_completion` 不是协议规则证明

当前模型仍使用：

```tamarin
restriction strict_batch_completion
```

裁剪掉 “complete 时还有未处理 slot” 的轨迹。这种写法能帮助证明，但容易被审稿人理解为把待证明结论作为环境假设加入模型。

本轮尝试把它改成规则层 bounded-4 token / counter 机制，但这些机制都会使 `v6` 在 source saturation 阶段不收敛。结论是：`v6` 不应该同时承担 dynamic skeleton、strict completion、terminal close 三个目标。当前 `v6` 的成熟定位应是：

```text
在 strict completion trace restriction 下，验证 bounded dynamic batch skeleton 的 selected lifecycle properties。
```

如果论文要声称 “Tamarin 证明 complete 必须等待所有 added slots processed”，应该引用独立模型 `v7`，而不是引用当前 `v6`。`v7` 使用显式 `AddedSlot1..4`、线性 `SealedStage0..4` 和 `Slot1DoneFact..Slot4DoneFact` 建模，并已证明：

```text
complete_requires_all_added_slots_processed
complete_requires_all_slots_done
no_slot_accept_after_complete
no_slot_accept_after_fail
no_add_after_seal
```

需要注意的是，`v7` 只能支撑 fixed 4 slot lifecycle claim。若只引用 `v6` 而不引用 `v7`，论文中仍应明确写成：

```text
We assume strict batch completion as a trace restriction in the bounded dynamic skeleton.
```

### 2.5 最大问题四：bounded dynamic skeleton 不等于任意长度 `BatchReceive`

`CreateBatch` 产生 4 个 `AddSlotToken`。这意味着当前 `v6` 最多建模 4 个 slot。它是 bounded dynamic skeleton，不是 arbitrary-length vector。

这本身不是错误，但论文必须精确表述。

可以声称：

```text
bounded symbolic model with up to four dynamically added slots
```

不能声称：

```text
arbitrary-length BatchReceive
```

解决方式：

如果目标是会议 artifact，可以保留 bounded model，但要在文档和论文中给出理由：

```text
Tamarin 对 unbounded vectors 和全局“不存在 pending slot”判断不自然，
因此我们用 bounded symbolic skeleton 验证 batch lifecycle 的关键不变量。
```

如果目标是更强论文结果，则建议新增：

```text
tamarin/kwaay_splitkem_batch_dynamic_bounded4_final.spthy
tamarin/kwaay_splitkem_batch_dynamic_counter_experiment.spthy
```

第一个作为稳定 artifact，第二个作为探索 arbitrary-length/counter 的实验模型。

### 2.6 最大问题五：`K-Waay` 密码学对象仍然过于抽象

`v6` 当前用：

```tamarin
cts/4 [private]
ks/4 [private]
rkey/5 [private]
```

表达 split-KEM component 和 receiver key。它没有显式建模：

```text
ct_l
ct_k
ct_s
K_l
K_k
K_s
sid
KDF(K_l,K_k,K_s,sid)
signature
prekey bundle
真实 decapsulation fail
```

这与仓库已有 `docs/model-mapping.md` 的定位一致：`v6` 是 state/batch semantics，不是完整 cryptographic model。

解决方式：

为论文主线建立一个明确的模型分层：

```text
Layer 1: ProVerif core model
  负责 m=(ct_l,ct_k,ct_s)、secrecy、agreement boundary。

Layer 2: Tamarin v6 batch/state model
  负责 receiver state、BatchReceive slot、compromise ordering、batch lifecycle。

Layer 3: deniability diff model
  负责 transcript indistinguishability / simulator。

Layer 4: computational proof outline
  负责 KIND / UNF-1KMA / IND-1BatchCCA / advantage bound。
```

每一层只声称自己证明的内容，避免把 `v6` 的 batch skeleton 解释成完整 `K-Waay` 证明。

## 3. 对 `kwaay_deniability.spthy` 的审稿意见

### 3.1 当前模型做了什么

该文件包含两个场景：

```text
Deniable_Transcript_Core
Deniable_Transcript_HMAC
```

核心方程是：

```tamarin
skem_forge_ct(skR, pk(skS), r) = skem_enc(skS, pk(skR), r)
skem_forge_key(skR, pk(skS), r) = skem_key(skS, pk(skR), r)
```

然后输出：

```tamarin
Out(diff(real_transcript, fake_transcript))
```

这表达了一个非常强的建模假设：receiver 可以生成与 sender 真实 split-KEM component 语法上等价的 ciphertext/key。

### 3.2 为什么这还不是成熟 deniability proof

问题一：等价性几乎被方程直接假设。

如果 `fake_ct_s` 通过方程直接等于 `real_ct_s`，那么 `diff(real_transcript, fake_transcript)` 的不可区分性不是由协议流程和 attacker view 推出来的，而是由 equational theory 直接给出的。审稿人会问：这个方程对应哪一个 `K-Waay` primitive assumption？是 split-KEM 的定义？是可否认性 simulator 的构造？还是把要证明的性质当成公理？

问题二：只建模了 `ct_s`，没有建模完整 transcript。

`K-Waay` core transcript 至少应包含：

```text
ct_l
ct_k
ct_s
sender/receiver identities
public prekey bundle
sid
```

旧 core deniability 只比较 `ct_s`。这不足以说明完整 `K-Waay` transcript 可否认，因为攻击者或 judge 可能从 `ct_l`、`ct_k`、`sid`、prekey bundle 或状态泄露中区分 real/fake。本轮新增的 `kwaay_deniability_core_diff.spthy` 已把 public core transcript 扩展到 identities、prekey bundle、`m=(ct_l,ct_k,ct_s)` 和 `sid`。

问题三：旧模型没有证明 `Observational_equivalence`，新 core diff 模型已经补上初版证据。

在 `Tamarin` 中，`diff` 文件需要在 `--diff` 模式下证明自动生成的：

```text
Observational_equivalence
```

本轮已新增 `tamarin/kwaay_deniability_core_diff.spthy`，并生成 `logs/tamarin-deniability/core_observational_equivalence.out`。该日志显示 `All wellformedness checks were successful`，且 `DiffLemma: Observational_equivalence : verified`。因此 core public-transcript deniability 已有初版 symbolic evidence。

但这仍然不是完整 K-Waay deniability。它只覆盖 public core transcript abstraction，不覆盖完整 Big Brother opening-data game，也不覆盖 computational deniability。

问题四：HMAC 场景不清楚是不是 `K-Waay` 原协议。

`Deniable_Transcript_HMAC` 加了：

```text
mac(real_key, real_sid)
```

如果这是修复/扩展协议，需要明确它不是 Figure 7 core。否则审稿人会认为你把一个 hardening branch 混入原协议主张。

### 3.3 修复建议

建议把该文件拆成两个模型：

```text
tamarin/kwaay_deniability_core_diff.spthy
tamarin/kwaay_deniability_hmac_extension_diff.spthy
```

`core` 模型应该包含完整 transcript：

```tamarin
real_transcript = <pkA, pkB, ct_l_real, ct_k_real, ct_s_real, sid_real>
fake_transcript = <pkA, pkB, ct_l_fake, ct_k_fake, ct_s_fake, sid_fake>
```

如果 `ct_l` 和 `ct_k` 是 simulator 可重采样的未认证 component，应明确让 fake world 自己生成：

```text
ct_l_fake
ct_k_fake
```

如果 `ct_s` 是 deniable/authenticated component，应单独给出其 forge relation，并解释对应的 primitive assumption。

最重要的是新增证明脚本：

```text
scripts/prove-deniability-diff.sh
logs/tamarin-deniability/core_observational_equivalence.out
logs/tamarin-deniability/summary.txt
```

命令形态应包含：

```bash
tamarin-prover --diff --prove tamarin/kwaay_deniability_core_diff.spthy
```

不要使用 `--prove=Observational_equivalence`。该名称是 Tamarin 在 `--diff` 模式下自动生成的 diff lemma，不是源文件中的显式 lemma；把它作为参数传入会产生 wellformedness warning。

## 4. 对 `kwaay_deniability_with_proof` 的审稿意见

### 4.1 当前模型想表达什么

该文件试图建模 malicious adversary 下的 `PoK`：

```tamarin
In(< pk(malicious_skB), pok(malicious_skB) >)
```

直觉是：恶意 receiver 若注册公钥，就必须提供同一个 secret witness 的证明；simulator 可抽取该 witness，再用它伪造 transcript。

这个方向是对的。面对 maliciously generated public key，单纯假设 receiver 有合法 secret key 不够，必须建模 registration validity 或 knowledge extraction。

### 4.2 当前问题

问题一：`pok/1` 只是 public constructor，不是 proof system。

在 symbolic model 里，`pok(x)` 如果没有验证规则、抽取规则、不可伪造约束或注册事件，它只是一个普通 term。当前 `In(<pk(malicious_skB), pok(malicious_skB)>)` 只能让规则模式匹配同一个变量，不能充分表达：

```text
adversary actually knows malicious_skB
registration oracle accepted this key
extractor can recover malicious_skB
```

问题二：没有 `REGISTER` oracle / key registry。

可否认性游戏通常需要明确：

```text
who registers public keys
what proof must be attached
which keys are honest
which keys are adversarial
what the simulator can extract
```

旧模型中 malicious public key 是直接从输入 term 匹配出来的，没有全局注册状态，也没有 `ValidRegisteredKey`。本轮新增的 `tamarin/kwaay_deniability_malicious_pok_diff.spthy` 已经补了 `RegisterHonestSender`、`RegisterMaliciousReceiverWithPoK`、`ExtractedWitness` 和 `!ExtractedReceiverSk`。

同时，模型已避免从 `pok(receiverSkB)` 反向模式匹配 witness；现在把 malicious witness 作为 symbolic extractor input 显式建模，parse 日志不再有 message derivation warning。

问题三：仍然只比较一个单规则 transcript。

没有 sender role、receiver role、network attacker、state compromise、judge view，也没有和 `K-Waay` batch/state 主模型对接。

### 4.3 修复建议

建议新增 registration 层：

```tamarin
rule RegisterHonestReceiver:
  [ Fr(~skB) ]
  --[ HonestRegistered($B, pk(~skB)) ]->
  [ !Ltk($B, ~skB), !Pk($B, pk(~skB)), Out(pk(~skB)) ]

rule RegisterMaliciousReceiverWithPoK:
  [ In(<$B, pk(skB), pok(skB)>) ]
  --[ MaliciousRegistered($B, pk(skB)), ExtractedWitness($B, pk(skB), skB) ]->
  [ !Pk($B, pk(skB)), !ExtractedSk($B, pk(skB), skB), Out(pk(skB)) ]
```

然后让 simulator 只能在以下 premise 下伪造：

```tamarin
!ExtractedSk($B, pkB, skB)
```

新增 lemmas：

```text
registered_key_has_witness
simulator_uses_extracted_witness
malicious_deniability_diff_equivalence
```

对于 `PoK`，建议在论文中写成 symbolic abstraction：

```text
We model the proof of knowledge by an extractor event ExtractedWitness.
This abstracts the computational extractability of the registration proof.
```

不要写成：

```text
Tamarin proves the proof-of-knowledge scheme secure.
```

除非另有专门模型或手工证明。

## 5. 对 `kwaay_deniability_advanced_BigBrother` 的审稿意见

### 5.1 当前模型想表达什么

该文件试图表达：

```text
Big Brother Distinguisher
OD={SKS}
1-out-of-2 deniability against malicious adversaries
```

并在规则输出里泄露：

```tamarin
Out(~skA)
Out(~skB)
Out(diff(real_transcript, fake_transcript))
```

### 5.2 当前问题

问题一：`Big Brother` view 没有被精确定义。

如果 judge 拿到双方 long-term secret key，它能否拿到：

```text
sender local randomness
receiver local randomness
ephemeral KEM secret
registration witness
state after session
batch receiver state
message logs
```

这些必须明确定义。当前只泄露 `~skA` 和 `~skB`，不足以支撑 “Big Brother model” 的论文级主张。

问题二：泄露双方 secret 后仍等价，主要来自 forge equation。

如果 `skem_forge_ct(~skB, pkA, ~r)` 被方程设为 `skem_enc(~skA, pkB, ~r)`，那么 judge 即使看到 secret key 也分不出，更多是因为语法等式被强行加入，而不是因为协议 transcript 天然可模拟。

问题三：没有体现 `1-out-of-2` 的选择结构。

`1-out-of-2 deniability` 应该明确：

```text
哪一方可以否认？
哪一方负责模拟？
judge 拿到哪一方或双方的 opening data？
真实世界和模拟世界中哪个 participant 行为不同？
```

当前模型只有一个 rule，不能表达这些交互式选择。

### 5.3 修复建议

建议先写清楚 `OD` 矩阵：

| 模型 | Judge 获得的数据 | 目标 |
|---|---|---|
| outsider | public transcript | 普通 transcript deniability |
| receiver-opens | receiver long-term secret + transcript | receiver 可伪造 sender-like transcript |
| sender-opens | sender long-term secret + transcript | sender 可解释自己的行为 |
| both-open | both long-term secrets + transcript | stronger Big Brother claim |
| full-state-open | long-term secrets + ephemeral randomness + local state | 通常很难成立，需要谨慎 |

然后为每个 `OD` 单独建一个 `diff` model 或用 action fact 标记：

```text
JudgeViewPublic
JudgeViewReceiverSK
JudgeViewSenderSK
JudgeViewBothSK
JudgeViewFullState
```

不要直接把最强 claim 写成唯一模型。建议从较弱但可证明的版本开始：

```text
receiver-opens deniability for split-KEM component
```

然后再推进到：

```text
full K-Waay transcript deniability under specified OD
```

## 6. 与 `K-Waay` 的贴合度评估

### 6.1 `v6` 与 `K-Waay` 的贴合度

贴合的部分：

```text
receiver-side state
batch slot
batch complete/fail
state compromise ordering
partnered/unpartnered receiver slot
receiver-side exception
```

不贴合或尚未覆盖的部分：

```text
full K-Waay message m=(ct_l,ct_k,ct_s)
full KDF over K_l,K_k,K_s,sid
real KEM decapsulation success/failure
prekey bundle signature
BatchReceive arbitrary vector traversal
full transcript sid binding
computational KIND game
deniability game
```

评估：

```text
作为 K-Waay batch/state submodel：合理。
作为完整 K-Waay model：不够。
作为 deniability 证明基础：需要进一步和 diff model 对接。
```

### 6.2 三份 deniability 模型与 `K-Waay` 的贴合度

贴合的部分：

```text
抓住了 split-KEM 可伪造/可模拟的核心直觉。
尝试区分 core、HMAC extension、malicious/PoK、Big Brother。
使用了 Tamarin 的 diff operator。
```

不贴合的部分：

```text
没有完整 K-Waay transcript。
没有 BatchReceive。
没有 state lifecycle。
没有 REGISTER / KEY / STATE / TEST oracle。
没有 precise judge view。
没有 observed proof result。
没有 negative sanity checks。
```

评估：

```text
作为直觉草图：有价值。
作为 artifact proof：不成熟。
作为会议/期刊 formal deniability result：目前不够。
```

## 7. 投稿级别应该补齐的内容

### 7.1 Claim matrix

建议新增一个表，把每个安全声明和模型证据一一对应：

| Claim | 工具 | 文件 | 证据 | 当前状态 |
|---|---|---|---|---|
| sender/receiver secrecy | ProVerif | `kwaay_core_final.cpp.pv` | query true | 已有 |
| exact agreement boundary | ProVerif | `kwaay_core_final.cpp.pv` | counterexample | 已有 |
| receiver state lifecycle | Tamarin | `v6` | selected lemmas | 部分成熟 |
| batch close exclusivity | Tamarin | `v6` | `batch_fail_complete_exclusive` | 已有 |
| no process after close | Tamarin | `v7` | `no_slot_accept_after_complete`, `no_slot_accept_after_fail`, `no_slot_accept_after_close` | 已补 |
| arbitrary BatchReceive | Tamarin/hand proof | 待新增 | theorem | 缺失 |
| core deniability | Tamarin `--diff` | `kwaay_deniability_core_diff.spthy` | `Observational_equivalence` | 初版已补 |
| malicious PoK deniability | Tamarin `--diff` + assumption | `kwaay_deniability_malicious_pok_diff.spthy` | witness lemmas verified, equivalence timeout | 部分补齐 |
| Big Brother deniability | Tamarin `--diff` | 待重构 | specified OD equivalence | 缺失 |
| computational KIND | CryptoVerif/hand proof | 待新增 | reduction | 缺失 |

### 7.2 `v6` 未补、`v7` 已补的 terminal lifecycle lemmas

本轮确认不应把以下 lemmas 直接塞入当前 `v6`：

```text
complete_requires_all_added_slots_processed
no_slot_accept_after_complete
no_slot_accept_after_fail
no_add_after_seal
```

原因不是语法问题，而是规则层硬化会让 Tamarin 在 source saturation 阶段不收敛。已经尝试过 `OpenBatch / SealedBatch / ClosedBatch`、固定 `slot1..slot4 + DoneSlotFact`、`OpenCount0..4 / SealedCount0..4` 三类写法，均不适合当前 `v6`。

本轮已新增 `v7`，采用固定 4 slot lifecycle 模型，把这些 terminal lifecycle 性质放到更小、更专门的模型里证明。`v7` 已验证：

```text
no_add_after_seal
no_add_after_complete
no_add_after_fail
no_slot_accept_after_complete
no_slot_accept_after_fail
no_slot_accept_after_close
complete_requires_all_added_slots_processed
complete_requires_all_slots_done
batch_end_token_single_use
batch_fail_complete_exclusive
receiver_state_single_batch_end
```

其中 `fail_is_terminal` 和 `closed_batch_is_terminal` 在 `v7` 中分别由 `no_slot_accept_after_fail` 与 `no_slot_accept_after_close` 表达；`complete_requires_nonempty_batch` 在固定四槽模型中由 `seal_requires_all_slots_added` 和 `complete_requires_all_slots_done` 间接覆盖，不再单独列为核心 lemma。

### 7.3 deniability 必补 tests

对每个 `diff` 模型至少补三类测试：

1. Positive equivalence:

```text
Observational_equivalence verified
```

2. Executability on both sides:

```text
exists-trace real transcript generated
exists-trace fake transcript generated
```

3. Negative sanity checks:

```text
去掉 forge equation 后 equivalence 应失败。
把 MAC 绑定到 sender-only secret 后 equivalence 应失败。
泄露 sender randomness 后 Big Brother equivalence 应失败或降级。
```

第三类很重要。没有 negative sanity check，审稿人会担心模型过抽象，导致任何协议都“可否认”。

## 8. 建议的实施路线

### Phase A：已新增 `v7`，不要继续硬改 `v6`

目标：

```text
让 batch phase 和 terminal lifecycle 由规则保证，而不是只由注释和 restriction 保证。
```

动作：

```text
保留 v6 作为可验证的 bounded dynamic skeleton。
新增 v7，从 fixed-slot lifecycle 风格扩展到 4 slot。
避免在 v7 中使用 AddSlot 的 phase self-loop。
显式建模 OpenStage0..4、SealedStage0..4、AddedSlot1..4 和 Slot1DoneFact..Slot4DoneFact。
新增并验证 complete_requires_all_added_slots_processed。
新增并验证 no_slot_accept_after_complete / no_slot_accept_after_fail / no_slot_accept_after_close。
新增并验证 no_add_after_seal / no_add_after_complete / no_add_after_fail。
```

成功标准：

```text
v6 继续作为 bounded dynamic skeleton，不把 terminal lifecycle 硬塞回 v6。
v7 的 24 个 selected lifecycle lemmas 均 verified。
logs/tamarin-v7 中已保存可复现输出。
```

新增文件：

```text
tamarin/kwaay_splitkem_batch_dynamic_v7.spthy
scripts/prove-v7-selected.sh
docs/tamarin/tamarin-v7-results.md
```

### Phase B：已重构 core deniability diff model

目标：

```text
从 toy ct_s equivalence 推进到 full K-Waay core transcript equivalence。
```

动作：

```text
显式建模 ct_l / ct_k / ct_s。
显式建模 sid。
显式建模 public transcript。
保留 split-KEM forge abstraction，但写清楚它是 primitive assumption。
使用 --diff 证明 Observational_equivalence。
新增 negative sanity check，并确认坏扩展不等价。
```

成功标准：

```text
core diff 模型 wellformed。已完成。
Observational_equivalence verified。已完成。
有 negative sanity check。已完成，结果为 EXPECTED_NON_EQUIV。
```

### Phase C：已加入 malicious registration / PoK，但 equivalence 尚未收敛

目标：

```text
把 malicious public key 的 witness extraction 建模出来。
```

动作：

```text
新增 RegisterHonest / RegisterMaliciousWithPoK。已完成。
新增 ExtractedWitness action/fact。已完成。
simulator 只能使用 ExtractedWitness。已完成。
证明 registered malicious key has witness。已 verified。
证明 malicious deniability diff。当前 300 秒 TIMEOUT，尚未完成。
```

成功标准：

```text
没有 PoK/extractor 时 malicious equivalence 失败或无法证明。
有 PoK/extractor 时 witness 相关 trace lemmas 成立。
malicious observational equivalence 需要继续拆分或优化 proof search。
```

### Phase D：定义 Big Brother `OD`

目标：

```text
把 Big Brother claim 从口号变成可审查的 formal view。
```

动作：

```text
列出 OD={public transcript, sender sk, receiver sk, local randomness, state} 的组合。
从 receiver-opens 开始证明。
逐步增加 OD 强度。
每增强一次 OD，都跑 positive 和 negative sanity checks。
```

成功标准：

```text
每个 Big Brother theorem 都有清楚的 OD 定义。
每个 theorem 都有对应 --diff 日志。
论文不使用未证明的最强 claim。
```

## 9. 推荐的论文表述

当前成熟表述：

```text
We provide a symbolic formal analysis of the K-Waay core.
Our ProVerif model separates KIND-style secrecy from exact agreement.
Our Tamarin models verify receiver-state consumption, compromise ordering,
batch-slot origin, receiver-side exception classification, batch abort,
and selected lifecycle properties of a bounded dynamic batch skeleton.
We additionally give an initial symbolic observational-equivalence model
for the public core transcript, with a negative sanity check.
```

当前不建议表述：

```text
We prove full K-Waay deniability in Tamarin.
We prove 1-out-of-2 deniability in the Big Brother model.
We prove full computational security of K-Waay.
```

当前可谨慎升级为：

```text
We additionally give a symbolic observational-equivalence model for
the deniability intuition of the split-KEM component / full core transcript,
under an explicitly stated simulator and opening-data model.
```

注意这里仍然是 symbolic，不是 computational。

## 10. 最终审稿判断

如果现在投稿，审稿判断大概率是：

```text
Tamarin batch/state 部分有价值，但属于 partial symbolic model。
Deniability 部分目前过于简化，不能支撑标题级 claim。
```

如果按上面的 Phase A 到 Phase D 补齐，成熟度会明显提升：

```text
Phase A 完成后：Tamarin batch lifecycle 可以作为较稳的 symbolic artifact。
Phase B 完成后：可以开始谨慎声称 symbolic deniability。
Phase C 完成后：malicious-key deniability 才有可审查基础。
Phase D 完成后：Big Brother claim 才适合进入论文主结论。
```

最优投稿定位建议：

```text
不要把工作包装成“完整证明 K-Waay”。
把贡献定位为“对 K-Waay core 的 symbolic verification 和 security-goal boundary clarification”。
deniability 若未补齐，应作为 future work 或 preliminary model。
```

这样写更稳，也更像真正能经得住审稿的 formal methods artifact。
