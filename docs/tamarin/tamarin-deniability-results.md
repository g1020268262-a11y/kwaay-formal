# Tamarin Deniability Diff 验证结果

## 1. 模型定位

本轮新增三份 `--diff` 模型：

```text
tamarin/kwaay_deniability_core_diff.spthy
tamarin/kwaay_deniability_malicious_pok_diff.spthy
tamarin/kwaay_deniability_negative_sender_secret_diff.spthy
```

它们用于把旧的 toy deniability sketch 推进到可复现的 Tamarin observational-equivalence artifact。当前结果仍是 symbolic transcript-level abstraction，不是完整 computational deniability proof，也不是 Big Brother 完整 opening-data game。

## 2. 复现命令

```bash
bash scripts/prove-deniability-diff.sh
```

本轮验证环境：

```text
tamarin-prover 1.12.0
Maude 3.5.1
WSL Ubuntu-24.04
```

日志目录：

```text
logs/tamarin-deniability/
```

脚本已清理旧问题：不再使用 `--prove=Observational_equivalence` 指定自动生成的 diff lemma 名称，而是使用 `tamarin-prover --diff --prove <file>`。因此新日志中不再出现 “Observational_equivalence from arguments does not correspond to a specified lemma” warning。

## 3. 当前结果

```text
core_parse                                                             OK
malicious_pok_parse                                                    OK
negative_parse                                                         OK
core_executable_real                                                   VERIFIED
core_executable_simulated                                              VERIFIED
malicious_executable_real                                              VERIFIED
malicious_executable_simulated                                         VERIFIED
malicious_registered_witness                                           VERIFIED
malicious_simulator_witness                                            VERIFIED
negative_executable_real                                               VERIFIED
negative_executable_simulated                                          VERIFIED
core_observational_equivalence                                         VERIFIED
malicious_observational_equivalence                                    TIMEOUT
negative_observational_equivalence                                     EXPECTED_NON_EQUIV
```

## 4. 已经清理的问题

### 4.1 core diff warning

旧脚本使用：

```bash
tamarin-prover --diff --prove=Observational_equivalence ...
```

Tamarin 会证明自动生成的 diff lemma，但同时报告该 lemma 名称不是显式声明 lemma。新脚本改为：

```bash
tamarin-prover --diff --prove ...
```

新日志中 `core_observational_equivalence.out` 显示：

```text
All wellformedness checks were successful.
DiffLemma: Observational_equivalence : verified
```

### 4.2 malicious PoK wellformedness

旧模型在 `RegisterMaliciousReceiverWithPoK` 中通过 `pok(receiverSkB)` 反向模式匹配 witness，Tamarin 报告变量无法从 premise 推导。新模型把 malicious witness 显式作为 extractor input：

```tamarin
In(<$B, receiverSkB, pok(receiverSkB)>)
```

这表达的是 symbolic extractor assumption：注册阶段接受 PoK 后，模型记录 `ExtractedWitness` 和 `!ExtractedReceiverSk`。新 parse 日志不再有 message derivation warning。

### 4.3 negative sanity

旧 negative 模型没有真正让攻击者看到可区分 marker，导致坏扩展也被证明等价。新模型直接输出：

```tamarin
Out(diff(sender_tag_marker, simulated_tag_marker))
```

因此 `negative_observational_equivalence.out` 中出现预期攻击轨迹：

```text
DiffLemma: Observational_equivalence : falsified - found trace
```

脚本将这个预期结果记为 `EXPECTED_NON_EQUIV`。

## 5. 当前还能声称什么

可以谨慎声称：

```text
We provide a symbolic Tamarin observational-equivalence model for the
public core transcript abstraction, and a negative sanity check showing that
the framework detects a sender-secret-bound public tag as non-deniable.
```

也可以声称：

```text
The malicious-registration model includes explicit witness extraction events,
and the registered-witness / simulator-witness trace properties are verified.
```

## 6. 仍然不能声称什么

暂时不能声称：

```text
malicious PoK deniability equivalence 已完成证明。
Big Brother 1-out-of-2 deniability 已完成证明。
完整 K-Waay deniability 已完成证明。
computational deniability 已完成证明。
```

原因是 `malicious_observational_equivalence` 在 300 秒内仍为 `TIMEOUT`。它已经没有 wellformedness warning，但还没有自动证明完成。

## 7. 下一步建议

优先顺序：

```text
1. 缩小 malicious PoK equivalence 的 proof search 空间。
2. 如果仍不收敛，把 malicious PoK equivalence 拆成更小的 receiver-open / public-transcript 子模型。
3. 再推进 Big Brother OD 矩阵，不要直接从最强 opening-data claim 开始。
```
