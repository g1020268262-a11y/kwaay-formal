# ProVerif Final Targets

`proverif/kwaay_core_final.cpp.pv` 是 K-Waay Figure 7 core 的 macro-based final model。它使用 C preprocessor 风格宏组织多个验证目标，普通 ProVerif 不直接读取这个文件，而是先由脚本执行：

```bash
cpp -P -D TARGET proverif/kwaay_core_final.cpp.pv
```

生成的普通 `.pv` 文件会放在 `logs/final/proverif/generated/`，ProVerif 输出放在 `logs/final/proverif/out/`，汇总文件是 `logs/final/proverif/summary.txt`。

运行方式：

```bash
bash scripts/run-proverif-final.sh
bash scripts/run-proverif-final.sh BASELINE
```

这个模型是 K-Waay Figure 7 core 的 no-batch / single-receive abstraction，不是 full `BatchReceive`。BatchReceive 的 state、slot、lifecycle 由 Tamarin final model 处理。该文件不证明 computational `KIND`、`UNF-1KMA`、`IND-1BatchCCA` 或 deniability。

## Target 说明

`BASELINE` 是 no-compromise baseline。它不启用任何 leak process，包含 executability sanity query、`RecvDone ==> SendDone` diagnostic query、prekey sanity queries、sender-side secrecy 和 receiver-side secrecy。

`COMPONENT` 是 split-KEM component authenticity target。核心 query 是：

```proverif
SplitKemAccepted ==> SenderSplitKemComponent
```

它只检查 receiver 接受的 split-KEM component 是否对应 honest sender 生成的 component，不要求完整消息或 session key exact agreement。`COMPONENT` 不启用任何 leak process。

`EXCEPTION_CHOICE` 是 optional compromise classification target。attacker 可以选择触发 B 侧 0 个、1 个、2 个或 3 个 decapsulation secret compromise。它用于 bad-case / exception classification，不是 baseline secrecy theorem。

`LEAK_SIGSK` 是 signature secret compromise experiment，泄露 `sskA` 和 `sskB`。

`LEAK_KEMSK` 是 receiver long-term KEM secret compromise experiment，泄露 `kskB`。

`LEAK_EKEMSK` 是 receiver ephemeral KEM state compromise experiment，泄露 `ekskB`。

`LEAK_RSKEMSK` 是 receiver split-KEM state compromise experiment，泄露 `receiverSkB`。

`LEAK_SSKEMSK` 是 sender split-KEM state compromise experiment，泄露 `senderSkA`。

`LEAK_KEMSK_EKEMSK` 是组合泄露实验，泄露 `kskB + ekskB`。

`LEAK_ALL_RECEIVER_SECRETS` 是 B 侧三个 decapsulation secrets compromise experiment，触发：

```text
CompromiseKemSk(B)
CompromiseReceiverEkemState(B)
CompromiseReceiverSkemState(B)
```

## Query 语义

`RecvDone ==> SendDone` 是 diagnostic query。它用于观察 public-channel core 中 full-message exact agreement 的缺口，不是最终认证定理。

`SplitKemAccepted ==> SenderSplitKemComponent` 是 component-level authenticity query。它是 split-KEM component 层面的 correspondence，不等价于完整 session agreement。

`LEAK_*` target 的结果是 compromise experiment 的结果，不是 baseline security theorem。Baseline 和 compromise target 不能混淆：`BASELINE` 中没有泄露进程；`EXCEPTION_CHOICE` 和 `LEAK_*` 中主动泄露 secret 或允许 attacker 选择泄露。

如果某个 leak target 中 secrecy query 为 false，只能说明该 compromise experiment 下 ProVerif 找到了对应攻击轨迹，不能把它解释为 no-compromise baseline 被破坏。
