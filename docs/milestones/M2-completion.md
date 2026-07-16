# M2 Completion Record — Original impact/composition model

完成日期：2026-07-16

状态：✅ complete

## 1. 冻结版本

Commit A2（固定模型、README 和逐 lemma runner）：

```text
commit: 841feabd908a01bdc68669ad99253a6755820389
tree:   7f68a46e0a19b40d5e94e40e050225b846932716
```

Commit B（只包含正式 evidence）：

```text
commit: e216a86e1ac7113013e58b17cb0217374ea95ca2
tree:   b74690a7d6267bea63d6c09c53f264eecfa2204e
```

冻结 artifact provenance：

```text
impact model blob:
c5cdc0d7233f3a415839b8f289182c0986d911a8

impact model SHA-256:
0c20e36137c27bd138101a91ef5ce1e16109fccf696f942eb98c3d855a11fa41

runner blob:
7dc5be4ac1972b6cbb949301aac90b66e999215b

runner worktree SHA-256:
1db2924b999ac9e68d40d047b3a012afd284f4961463723bb9b9e439226c15a5
```

A2 固定模型、README 和逐 lemma runner；B 只包含从 clean A2 生成的正式
evidence。本 completion record 只解释已提交证据，不改变模型、lemma、runner
或实际结果。本文件不预写自身 Commit C SHA，也不虚构最终 `main` merge SHA。

## 2. Artifact 与 evidence 路径

模型、runner 与边界说明：

- `tamarin/impact/kwaay_impact_original.spthy`
- `tamarin/impact/run-impact-original.sh`
- `tamarin/impact/README.md`

正式 evidence：

- `logs/tamarin-impact-original/aggregate-results.tsv`
- `logs/tamarin-impact-original/summary.txt`
- `logs/tamarin-impact-original/versions.txt`
- `logs/tamarin-impact-original/command.txt`
- `logs/tamarin-impact-original/parse.out`
- `logs/tamarin-impact-original/proofs/`
- `logs/tamarin-impact-original/attack-trace.out`
- `logs/tamarin-impact-original/attack-trace.json`
- `logs/tamarin-impact-original/attack-trace.dot`
- `logs/tamarin-impact-original/unique-install-trace.out`
- `logs/tamarin-impact-original/unique-install-trace.json`
- `logs/tamarin-impact-original/unique-install-trace.dot`
- `logs/tamarin-impact-original/original-regression.out`
- `logs/tamarin-impact-original/original-regression-summary.txt`
- `logs/tamarin-impact-original/frozen-formula-comparison.txt`
- `logs/tamarin-impact-original/lower-layer-result-comparison.txt`
- `logs/tamarin-impact-original/SHA256SUMS.txt`

## 3. 精确定义 `C_install-v2`

`C_install-v2` 是本模型显式采用的条件化组合边界：

```text
C1:
每个 installation 都有更早、完整参数匹配的 accept-output source。

C2a:
每个 accepted-output source 至多安装一次。

C2b:
若 ConsumerComplete 发生，则属于该 consumer 的每个成功输出都恰好安装一次。
该结论由 completion-gated totality 和 at-most-once 两部分共同组成，
不是用 future-install restriction 强制得到。

C2c:
正常的 accept → install → ConsumerComplete 路径可达。

C3:
每次 installation 都产生 fresh local handle。

C4:
InstallSession 只能由指定 installation interface rules 产生。

C5:
至少一个 matching accept/install pair 可达。
这不表示整条 trace 中只有一个 accept 或一个 install。

C6:
不同 accept-source occurrences 使用不同 local handles。

C7:
固定两输出 consumer 独立处理每个成功 batch output，
不按照 sid、message、peer 或 key 合并或去重。

C8:
C7 是显式 composition assumption，
不是已证明的 deployed K-Waay 行为。
```

`consumer_complete_requires_all_outputs_installed` 提供 C2b 的
completion-gated totality，`accept_output_installed_at_most_once` 提供
at-most-once；两者合起来才是 exactly-once。模型没有使用要求未来 install 的
restriction。

**`C_install-v2` 是条件化组合边界，不是协议规范事实、实现事实或部署事实。**
仓库没有证据证明 deployed upper layer 会独立安装每个 `BatchReceive` output；
因此所有 M2 installation 结论都以 `C_install-v2` 为前提。

## 4. 对象和事件

对象语义：

```text
sid = 协议 session identifier
aid = fresh accepted-output occurrence identifier
h   = fresh symbolic local installation handle
```

核心事件：

```text
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
AcceptOutputCreated(aid,B,A,bid,idx,rst,m,sid,k)
InstallFromAccept(aid,B,h,A,bid,idx,rst,m,sid,k)
InstallSession(B,h,A,sid,k)
ConsumerComplete(B,bid,rst)
```

- `aid` 不进入协议 message、`sid` 或 `k`；它只标识成功 output occurrence。
- `h` 是上层 symbolic local handle，不是协议 `sid`。
- `InstallFromAccept` 保存 `aid,B,h,A,bid,idx,rst,m,sid,k` 的完整来源。
- `InstallSession` 是 `C_install-v2` 下的条件化组合事件。
- `ConsumerComplete` 只表示固定两输出 consumer 完成，不是真实应用完成。

## 5. 19 条 composition lemma 实际结果

以下结果逐项来自 committed
`logs/tamarin-impact-original/aggregate-results.tsv`：

| Lemma | 实际结果 |
|---|---|
| `accept_output_has_same_time_accept` | verified，4 steps |
| `receiver_accept_has_output` | verified，4 steps |
| `receiver_accept_has_unique_output` | verified，20 steps |
| `accept_id_unique` | verified，193 steps |
| `install_has_prior_accept` | verified，18 steps |
| `install_session_has_interface_origin` | verified，4 steps |
| `install_from_accept_has_session` | verified，4 steps |
| `install_event_has_single_source` | verified，26 steps |
| `install_handle_unique` | verified，52 steps |
| `accept_output_installed_at_most_once` | verified，180 steps |
| `distinct_accept_sources_have_distinct_handles` | verified，26 steps |
| `install_requires_batch_complete` | verified，10 steps |
| `consumer_complete_requires_all_outputs_installed` | verified，30 steps |
| `consumer_complete_single_use` | verified，36 steps |
| `no_install_after_consumer_close` | verified，44 steps |
| `normal_one_accept_one_install` | verified，22 steps |
| `normal_consumer_complete` | verified，25 steps |
| `one_send_two_accepts_two_installs_exists` | verified，28 steps |
| `unique_install_within_completed_consumer` | falsified - found trace，28 steps |

汇总：

```text
composition:
18 verified
1 falsified

frozen lower layer:
16 verified
2 falsified

total:
37 terminal
34 verified
3 falsified
0 incomplete
0 failed invocation
0 wellformedness failure
0 <<loop>>
```

## 6. 核心 M2 结论

在固定两 slot、无 sender/receiver state compromise、并满足
`C_install-v2` 的条件化 consumer 模型中：

- 一个唯一 matching `SenderSession` 可以产生两个不同
  `ReceiverAccept` occurrences；
- 两个 accept 创建两个不同的 fresh `aid`；
- 两个 accept outputs 被分别安装；
- 两个 `InstallSession` 具有相同 `A`、`B`、`sid`、`k`，但具有不同的
  fresh symbolic local handles `h1` 和 `h2`；
- consumer 随后正常完成。

正向 witness：

```text
one_send_two_accepts_two_installs_exists
verified，28 steps
```

负性质：

```text
unique_install_within_completed_consumer
falsified - found trace，28 steps
```

> 这证明的是 conditional duplicate-install witness 和 conditional
> local-handle duplication，不是两个真实会话、session cloning、
> Double Ratchet state duplication 或 deployed exploit。

## 7. Trace 关键条件

- 一个唯一 matching `SenderSession`；
- 同一 `A,B,m,sid,k,bid,rst`；
- 两个不同 receiver timepoints；
- 两个不同 slot indices；
- 两个不同 fresh `aid`；
- 两个不同 installation timepoints；
- 两个不同 fresh handles；
- 两次 `InstallSession` 都发生在 `BatchComplete` 后、`ConsumerComplete` 前；
- 整条 witness 中不存在 `CompromiseReceiverState` 或
  `CompromiseSenderState`。

“唯一 send”只指完整 matching tuple 经 `full_message_unique_send` 消歧后的唯一
matching sender occurrence，不表示整条 trace 中不能存在无关 sender rule。

## 8. Regression

```text
18/18 frozen lower-layer formulas MATCH
18/18 lower-layer actual result vector MATCH
original regression exit = 0
```

impact model 保留 original 18 条 lower-layer lemma 的完整原公式；独立 original
regression 重新得到相同的 18 条 actual status。这证明选定公式和结果向量未回归，
不证明完整 trace equivalence，也不证明两个 theory 的全部语义完全等价。

## 9. Runner 与工具说明

```text
Tamarin Prover 1.12.0
Maude 3.5.1
execution_mode = sequential_per_lemma
37 independent selected-proof invocations
```

一次早期 single multi-lemma invocation 在当前模型和工具链上报告 `<<loop>>`；
随后 37 条 lemma 的逐项隔离诊断显示 37/37 单独正常终止。因此最终 runner 按
冻结顺序执行 37 次 `--prove=<exact-lemma-name>`，保存每条原始 output，并机械
聚合结果。

> 这是当前模型与已验证 Tamarin 1.12.0 工具链上的执行编排观察，
> 不是关于 Tamarin 的一般性 bug claim，也不是模型性质失败。

正式 successful evidence：

```text
runner final exit = 0
manifest entries = 52
evidence files including manifest = 53
sha256sum verification = 52/52 OK
```

所有 37 条 selected proof invocation 均 exit 0、wellformedness success、无
`<<loop>>`；positive/negative trace 和 original regression 的 wellformedness
检查也全部成功。

## 10. Assumptions 和 limitations

- Dolev–Yao symbolic attacker；
- fixed two-slot batch，不是 arbitrary-length vector theorem；
- KEM/KDF/message 使用 free symbolic constructors，不是 computational proof；
- successful reconstruction 使用 original `HonestSession` abstraction；
- core witness 中没有 sender/receiver state compromise；
- consumer 只有在 successful `BatchComplete` 后开始，failure path 不启动；
- 每个 successful output 有线性 token；
- consumer independently installs each output；
- 不按 `sid`、message、peer 或 key 去重或合并；
- 没有真实 session database；
- 没有 Double Ratchet；
- 没有 application action；
- 没有 concrete implementation mapping；
- 没有 arbitrary-length batch theorem；
- 没有 computational security；
- 没有 HMAC impact counterpart；
- 没有 dedup repair。

## 11. Allowed claims

允许的核心表述：

> Under the explicitly modeled `C_install-v2` consumer assumptions, the bounded
> original replay witness propagates from two receiver-accept outputs to two
> distinct symbolic local installation handles carrying the same peer,
> session identifier, and session key.

还可以分别说明：

- installation provenance 双向对应 verified；
- distinct accept sources 使用 distinct handles；
- normal accept/install/complete 路径可达；
- lower-layer formula 和结果向量未退化；
- unique installation under this consumer is falsified。

## 12. Prohibited claims

不能声称：

- deployed K-Waay 必然安装两个会话；
- Figure 7 规范已经要求逐项安装；
- 真实 implementation 存在 session-cloning exploit；
- 两个 `InstallSession` 等于两个完整真实会话；
- Double Ratchet 状态被复制；
- application、payment、authorization 等业务动作重复执行；
- arbitrary-length 或 cross-batch impact 已证明；
- HMAC-only 的 duplicate acceptance 已经证明 duplicate installation；
- M3 dedup 已完成；
- M4 combined fix 已完成；
- computational security 已证明。

## 13. Chat 最终审查

- Commit A2 的 model、README 和 runner 已通过审查；
- Commit B 的正式 evidence 已通过审查；
- 37 条结果与 expected result vector 一致；
- positive/negative trace artifacts 与指定公式及终态一致；
- 18/18 frozen formula comparison 通过；
- 18/18 lower-layer result comparison 通过；
- manifest 为 52 个 entries、53 个 committed evidence files，路径一致；
- Chat 已允许进入只解释 evidence 的 Commit C。

## 14. 唯一后继任务

M2 已完成。当前唯一下一步是 M3：建立 batch-local atomic dedup repair。

M3 尚未开始；本 completion record 不创建 fixed model，不提前实现 dedup，也不
开始 M4 combined work。
