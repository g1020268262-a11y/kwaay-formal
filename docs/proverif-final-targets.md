# ProVerif Final Targets

`proverif/kwaay_core_final.pv` 是 K-Waay Figure 7 core 的 macro-based final symbolic model。它合并了 no-batch baseline、split-KEM component authenticity、optional compromise exception 和多个 single-leak experiments。

这个模型是 no-batch / single-receive abstraction，不是 full `BatchReceive`。BatchReceive 的 state、slot、lifecycle 由 Tamarin final model 处理。该 ProVerif 文件也不证明 computational `KIND`、`UNF-1KMA`、`IND-1BatchCCA` 或 deniability。

运行方式：

```bash
bash scripts/run-proverif-final.sh
bash scripts/run-proverif-final.sh BASELINE
```

脚本会用 `cpp -P -D TARGET` 预处理 `kwaay_core_final.pv`，再把生成的目标 `.pv` 文件交给 ProVerif。输出位于 `logs/final/proverif/`，汇总文件是 `logs/final/proverif/summary.txt`。

## Targets

`BASELINE` 是 no-compromise baseline。它不启用任何 leak process，保留 executability sanity query、`RecvDone ==> SendDone` diagnostic query、prekey verification queries、sender-side secrecy 和 receiver-side secrecy。

`COMPONENT` 用于 split-KEM component-level authenticity。核心 query 是 `SplitKemAccepted ==> SenderSplitKemComponent`。它不启用任何 leak process。

`EXCEPTION_CHOICE` 是 optional compromise model。attacker 可以通过公开命令选择触发 B 侧 0 个、1 个、2 个或 3 个 decapsulation secret compromise。它用于 exception classification，不代表 baseline secrecy。

`LEAK_SIGSK` 只启用 signature secret compromise experiment，泄露 `sskA` 和 `sskB`，复现 `kwaay-core-public-channel-leak-sigsk.pv` 的实验目的。

`LEAK_KEMSK` 只启用 receiver long-term KEM secret compromise，泄露 `kskB`。

`LEAK_EKEMSK` 只启用 receiver ephemeral KEM state compromise，泄露 `ekskB`。

`LEAK_RSKEMSK` 只启用 receiver split-KEM state compromise，泄露 `receiverSkB`。

`LEAK_SSKEMSK` 只启用 sender split-KEM state compromise，泄露 `senderSkA`。

`LEAK_KEMSK_EKEMSK` 启用 `kskB + ekskB` 组合泄露。

`LEAK_ALL_RECEIVER_SECRETS` 启用 B 侧三个 decapsulation secrets compromise：`CompromiseKemSk(B)`、`CompromiseReceiverEkemState(B)`、`CompromiseReceiverSkemState(B)`。

## Query Semantics

`RecvDone ==> SendDone` 是 diagnostic query。它用于观察 Figure 7 core public-channel abstraction 下的 full-message exact agreement 缺口，不应被解释为最终认证定理。

`SplitKemAccepted ==> SenderSplitKemComponent` 是 component-level authenticity query。它只检查 receiver 接受的 split-KEM component 是否对应 honest sender 生成的 component，不要求整条消息或 session key exact agreement。

`LEAK_*` targets 是 compromise experiments，不是 baseline security theorem。它们保留原始 leak 文件中的 secrecy / agreement query，是为了复现实验结果并观察不同 secret compromise 对结果的影响。

Baseline 和 compromise targets 不能混淆：`BASELINE` 中没有泄露进程；`EXCEPTION_CHOICE` 和 `LEAK_*` 中主动泄露 secret 或允许 attacker 选择泄露，因此它们的 query 结果只说明对应 compromise experiment 的行为。
