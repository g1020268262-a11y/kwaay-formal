# ProVerif final results

本页记录 `proverif/kwaay_core_final.cpp.pv` 在 2026-06-06 通过
`scripts/run-proverif-final.sh` 生成并运行后的结果。summary 路径：
`logs/final/proverif/summary.txt`。

## Target 分类

Theorem targets:

- `BASELINE`
- `COMPONENT`
- `EXCEPTION_CHOICE`

Classification / experiment targets:

- `RECEIVER_EXCEPTION_CLASSIFICATION`
- `LEAK_SIGSK`
- `LEAK_KEMSK`
- `LEAK_EKEMSK`
- `LEAK_RSKEMSK`
- `LEAK_SSKEMSK`
- `LEAK_KEMSK_EKEMSK`
- `LEAK_ALL_RECEIVER_SECRETS`

`LEAK_*` 和 `RECEIVER_EXCEPTION_CLASSIFICATION` 的结果用于 compromise /
bad-case 分类，不是 no-compromise baseline theorem。

## 结果摘要

| Target | ProVerif status | Actual result | Expected / interpretation |
| --- | --- | --- | --- |
| `BASELINE` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy true；`RecvDone ==> SendDone` false；prekey sanity true；`HonestRun` reachable | 符合预期。`RecvDone ==> SendDone` 是 exact agreement diagnostic false，不是 key-recovery break。 |
| `COMPONENT` | OK | `SplitKemAccepted ==> SenderSplitKemComponent` true | 符合预期，component-level authenticity 成立。 |
| `EXCEPTION_CHOICE` | OK | `SenderKey` secrecy false；`ReceiverKey` secrecy false；sender-side triple exception query true | 符合预期。该 target 只保留 sender-side exception theorem，不用于解释 receiver-side unpartnered bad case。 |
| `RECEIVER_EXCEPTION_CLASSIFICATION` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy false | 符合预期。receiver-side attacker-known key 属于 expected receiver-side bad case，不等同于 honest sender-side key 泄露。 |
| `LEAK_SIGSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy false | 与旧 ledger 的 expected `sender true / receiver true` 不一致，标记为 model-drift。生成文件的 final process 只启用 `LeakSigSk(sskA, sskB)`，没有启用 KEM / EKEM / receiver_skem / sender_skem / all receiver secrets leak process。 |
| `LEAK_KEMSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy true | 符合 expected `sender true / receiver true`。 |
| `LEAK_EKEMSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy true | 符合 expected `sender true / receiver true`。 |
| `LEAK_RSKEMSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy false | 符合 expected `sender true / receiver false`。 |
| `LEAK_SSKEMSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy false | 符合 expected `sender true / receiver false`。 |
| `LEAK_KEMSK_EKEMSK` | OK | `SenderKey` secrecy true；`ReceiverKey` secrecy true | 符合 expected `sender true / receiver true`。 |
| `LEAK_ALL_RECEIVER_SECRETS` | OK | `SenderKey` secrecy false；`ReceiverKey` secrecy false | 符合 expected `sender false / receiver false`，分类为 normal bad case。 |

## Exception / leak 分类说明

`EXCEPTION_CHOICE` 中保留的 exception theorem 是 sender-side theorem：
如果 attacker 知道 honest sender-side session key，则 B 侧
`kem_sk`、`receiver_ekem_state`、`receiver_skem_state` 三个 decapsulation
secrets 必须全部 compromise。

不加入 receiver-side 三重泄露 exception query。receiver-side secrecy false
可能由 `sender_skem_sk` 或 `receiver_skem_sk` 单独泄露导致，属于 expected
receiver-side unpartnered bad case。这个分类由
`RECEIVER_EXCEPTION_CLASSIFICATION`、`LEAK_RSKEMSK`、`LEAK_SSKEMSK` 和本页
说明。

因此 receiver-side exception 不能简单写成 sender-side exception 的三重泄露
条件。receiver-side 需要 partnered / unpartnered 语义，后续由 Tamarin 或更精细
的 ProVerif model 处理。
