# M1 Completion Record — HMAC-only replay bridge

完成日期：2026-07-15

状态：✅ complete

## 1. 冻结版本

- M1 evidence commit：`aeb66939af5e4b229f14f1444e19b559a4f98181`
- 最终合并后的 main 快照：`0858252d787b4c61956be583ffdade58e01655f2`
- 模型 SHA-256：`d46ead8564b8cc8410f9f3a655c72be440e5fce3f2455022e0b00155508873f6`
- runner SHA-256：`2828cc0029adf5c441ce56893f10244cb3488315d3f3e4ec30b770451cf24294`

日志绑定的是 evidence commit 与上述 model/runner hash；最终 main 快照包含该
evidence bundle。文档更新 commit 不改变 M1 模型或原始运行结果。

## 2. Artifact 路径

核心模型与说明：

- `tamarin/replay/kwaay_replay_hmac_only.spthy`
- `tamarin/replay/README-hmac-only.md`
- `tamarin/replay/run-hmac-only.sh`
- `tamarin/replay/README.md`（original replay 对照）

M1 evidence bundle：

- `logs/tamarin-replay-hmac-only/summary.txt`
- `logs/tamarin-replay-hmac-only/raw.out`
- `logs/tamarin-replay-hmac-only/parse.out`
- `logs/tamarin-replay-hmac-only/command.txt`
- `logs/tamarin-replay-hmac-only/versions.txt`
- `logs/tamarin-replay-hmac-only/attack-trace.out`
- `logs/tamarin-replay-hmac-only/attack-trace.json`
- `logs/tamarin-replay-hmac-only/attack-trace.dot`
- `logs/tamarin-replay-hmac-only/original-regression.out`
- `logs/tamarin-replay-hmac-only/original-regression-summary.txt`
- `logs/tamarin-replay-hmac-only/hmac-baseline-regression.out`
- `logs/tamarin-replay-hmac-only/hmac-baseline-regression-summary.txt`
- `logs/tamarin-replay-hmac-only/hmac-baseline-runner.out`

## 3. 事件与 matching relation

Sender event：

```text
ConfirmedSend(A,B,m,sid,k,tag) @ s
```

Receiver event：

```text
ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag) @ r
```

Matching protocol coordinates：

```text
(A,B,m,sid,k,tag)
```

Receiver occurrence context：

```text
(bid,idx,rst)
```

matching existence/order 要求每个 `ConfirmedReceiverAccept @ r` 都存在更早
的 `ConfirmedSend @ s`，角色顺序反转且完整 matching coordinates 相同。

## 4. Sender occurrence 消歧

sender 规则为 ciphertext constructors 使用 fresh randomness，构造唯一完整
message tuple；`confirmed_message_unique_send` 实际验证：

```text
同一 (A,B,m,sid,k,tag) 出现于两个 ConfirmedSend 时，两个 timepoint 相同。
```

因此本 artifact 中相同完整 tuple 可以用来识别同一 sender occurrence。该结果
只负责 matching disambiguation，不是 receiver occurrence injectivity，不是
replay prevention，也不是 batch-local dedup。

## 5. HonestSession abstraction 的证据角色

模型建立持久关系：

```text
!HonestSession(A,B,rst,m,sid,k)
```

receiver slot processing 只有在存在该关系且输入恰为
`<m,hmac(confirm_key(k),sid)>` 时才产生 `ConfirmedReceiverAccept`。因此：

- `confirmed_receiver_accept_has_sender` 的 matching existence/order 在该
  abstraction 下主要是结构性 source-event mapping；
- Tamarin bridge 的主要独立证据角色是 confirmed-message replay 与 receiver
  occurrence/injectivity 分析；
- 它不独立建模 concrete KEM decapsulation、KDF security、HMAC unforgeability
  或 computational security；
- HMAC P1 的主要独立正面证据仍是 ProVerif `HMAC_BASELINE` 的
  `RecvDone ==> SendDone`。

## 6. 核心 lemma 与实际结果

数据源：`logs/tamarin-replay-hmac-only/summary.txt` 和完整
`raw.out`。

| 证据角色 | Lemma | 类型 | 实际结果 |
|---|---|---|---|
| matching-accept non-vacuity | `normal_confirmed_single_accept` | exists-trace | verified，12 steps |
| normal batch executability | `normal_confirmed_batch_complete` | exists-trace | verified，18 steps |
| matching existence/order | `confirmed_receiver_accept_has_sender` | all-traces | verified，16 steps |
| sender occurrence 消歧 | `confirmed_message_unique_send` | all-traces | verified，2 steps |
| duplicate-accept witness | `one_confirmed_send_two_accepts_exists` | exists-trace | verified，17 steps |
| confirmed message at-most-once | `confirmed_message_accepted_at_most_once` | all-traces | falsified - found trace，15 steps |
| same-batch/same-state injectivity | `injective_confirmed_receiver_accept` | all-traces | falsified - found trace，15 steps |

Lifecycle/state regressions：

| Lemma | 实际结果 |
|---|---|
| `slot_indices_distinct` | verified |
| `process_requires_slot_added` | verified |
| `process_requires_seal` | verified |
| `complete_requires_all_slots_processed` | verified |
| `no_add_after_seal` | verified |
| `no_accept_after_close` | verified |
| `batch_complete_consumes_state` | verified |
| `batch_fail_consumes_state` | verified |
| `batch_end_token_single_use` | verified |
| `receiver_state_single_batch` | verified |
| `receiver_state_single_batch_end` | verified |

完整 proof 的 parse、proof 和 selected attack-trace commands 均 exit 0；
52.75 秒的完整运行没有 timeout 或 incomplete lemma。selected-lemma
`attack-trace.out` 中其他 lemma 显示 analysis incomplete 是因为该命令只要求
一个 lemma；完整结果以 `raw.out` 为准。

## 7. 工具版本与命令

工具：

- Tamarin Prover 1.12.0
- Maude 3.5.1
- ProVerif 2.05（该版本不支持 `-version`，banner 已保存在
  `versions.txt`）

复现入口：

```bash
bash tamarin/replay/run-hmac-only.sh
```

记录的核心命令：

```bash
tamarin-prover --parse-only tamarin/replay/kwaay_replay_hmac_only.spthy
tamarin-prover --prove tamarin/replay/kwaay_replay_hmac_only.spthy
tamarin-prover --prove=one_confirmed_send_two_accepts_exists \
  --output-json=logs/tamarin-replay-hmac-only/attack-trace.json \
  --output-dot=logs/tamarin-replay-hmac-only/attack-trace.dot \
  tamarin/replay/kwaay_replay_hmac_only.spthy
tamarin-prover --prove tamarin/replay/kwaay_replay_original.spthy
bash proverif/variants/hmac-confirmation/run-hmac-confirmation.sh HMAC_BASELINE
```

runner 在正式运行前要求 clean worktree。`versions.txt` 记录
`pre_run_git_status_empty: true`；post-run 变化仅为被重新生成的 M1 log files。

## 8. 非空性与 attack trace 关键条件

非空性：

- matching send/accept 正常路径可达；
- two-slot normal batch completion 可达；
- ProVerif HMAC regression 中 `not event(HonestRun(k)) is false`，即
  `HonestRun` 可达。

positive proof / attack witness 的关键条件：

- 恰有一个 matching `ConfirmedSend` occurrence；
- 存在两个不同 receiver accept timepoints；
- 两个 slot indices 不同；
- 两个 accepts 使用相同 `A,B,bid,rst,m,sid,k,tag`；
- 两个 slot 都收到完全相同的 public
  `<m,hmac(confirm_key(k),sid)>`；
- 两个 accepts 都早于 `BatchComplete`；
- 整个 witness 中没有 `CompromiseReceiverState` 或
  `CompromiseSenderState`。

## 9. Regressions

Original replay regression：exit 0，重新得到已记录的 original profile，包括
one-send-two-accept witness verified、at-most-once/injectivity falsified，以及
selected lifecycle results。

ProVerif HMAC baseline regression：exit 0，实际结果包括：

- `HonestRun` reachable；
- `RecvDone ==> SendDone` true；
- 两个 prekey correspondences true；
- sender/receiver symbolic key secrecy true。

该 regression 才是 HMAC P1 的主要独立正面证据；Tamarin bridge 不替代它。

## 10. Assumptions

- Dolev–Yao symbolic attacker。
- fixed two-slot batch；不是 arbitrary-length vector theorem。
- symbolic `hmac/2` 与 private `confirm_key/1`；没有 computational HMAC game。
- `HonestSession` 抽象 successful honest session reconstruction。
- 两个 slots 可以接收同一 exact public confirmed message。
- matching 以完整 `(A,B,m,sid,k,tag)` tuple 加 sender uniqueness lemma 消歧。
- witness 限定同一 `bid`、同一 `rst`、不同 `idx`。
- witness 排除 sender/receiver state compromise。
- 没有 duplicate cache、`SeenSid`、rollback、cross-batch state reuse、
  `InstallSession`、application/Double Ratchet state。

## 11. Limitations

- matching existence 在 `HonestSession` 下主要是结构性结果，不能宣传成
  独立的 concrete HMAC-origin theorem。
- 只证明 same-batch/same-receiver-state negative；没有 positive global
  injectivity theorem，也没有专门 cross-batch attack。
- 没有 compromise-conditioned HMAC theorem；只知道当前 witness 不需要两类
  state compromise。
- 模型没有 P3 under `C_install`，所以 duplicate acceptance 不推出 duplicate
  installed sessions。
- 没有 batch-local dedup 或 combined repair。
- 没有 concrete KEM/KDF/HMAC、implementation 或 computational-security proof。

## 12. Allowed claims

可以声称：

> In the fixed two-slot symbolic HMAC-only bridge, one honestly constructed
> confirmed message can be supplied to two distinct slots of the same batch and
> receiver state, pass the same symbolic HMAC confirmation gate twice, and
> produce two distinct receiver accept occurrences before normal batch
> completion, without modeled sender/receiver state compromise.

还可以分别声称：

- ProVerif HMAC no-compromise baseline establishes its exact non-injective P1
  correspondence and symbolic secrecy targets；
- Tamarin HMAC-only matching existence/order is verified under its
  `HonestSession` abstraction；
- batch lifecycle/state-consumption selected lemmas regress successfully；
- HMAC confirmation 与 replay prevention、batch-local dedup、P3 under
  `C_install`、computational security 是不同性质。

## 13. Prohibited claims

不能声称：

- HMAC 被伪造、HMAC computational security 被攻破；
- HMAC confirmation 提供 freshness、replay prevention 或 batch-local dedup；
- 已证明 arbitrary/global/cross-batch replay；
- duplicate accept 等于 duplicate installation 或 concrete session cloning；
- 已证明 P3 under `C_install`；
- 已证明 deployed K-Waay exploit、full protocol security 或 computational KIND；
- 结果覆盖 `HonestSession` abstraction 之外的 concrete session reconstruction；
- 结果在任意 compromise material/timing 下成立；
- 已完成 M3 dedup 或 HMAC+dedup combined fix。

## 14. Chat 最终审查结论

Chat 最终审查结论：M1 已修正并可以通过/合并。最终审查要求的证据绑定
（commit、model hash、runner hash）、clean pre-run 状态和
`HonestSession` README 表述均已在 evidence bundle 中落实。最终审查同时确认：
正常路径和 batch completion 可达；matching 与 sender disambiguation verified；
one-send-two-accept witness verified；at-most-once/injectivity falsified；完整运行
无 timeout。由此 M1 可以登记为 ✅。

## 15. M0 completion 文件状态

截至最终 main 快照
`0858252d787b4c61956be583ffdade58e01655f2`，
`docs/milestones/M0-completion.md` 不存在（GitHub contents API 返回 404）。
本记录没有假装读取该文件，也不回填未经单独核实的历史内容。

建议日后基于 M0 commit `b196fdad`、对应 docs 和当时日志补一份独立的历史
M0 completion record。它是文档可追溯性债务，不阻塞 M1 结果登记，也不是当前
唯一研究下一步。

## 16. 唯一后继任务

M2：`C_install` impact/composition 调查与建模。

具体只做：

1. 从规范/接口/集成证据确认 receiver output 到 session installation 的消费方式；
2. 冻结 `ReceiverAccept -> InstallSession` 接口与五项 `C_install` 假设；
3. 在显式 `C_install` 下检查 one send → two accepts 是否产生 same sid/key、
   distinct local handles；
4. 若规范证据不足，如实保留 conditional/unknown impact。

M2 完成前不开始 M3 dedup，不把 duplicate accept 写成 duplicate installation。
