# Baseline Q1 false trace

## 1. Trace 核心

攻击者重用 honest sender 的 `ctS`，但替换 `ctL` 和 `ctE`。B 对篡改后的 `m'` 导出新的 `sid'` 和 `k'`。baseline 中 B 在没有 key confirmation 的情况下直接触发 `RecvDone`。

## 2. 原始 honest 消息

```text
ctL = lkem_enc(kpk(kskB[]), rL_1)
ctE = ekem_enc(ekpk(ekskB[]), rE_1)
ctS = skem_enc(senderSkA[], pk_skem_receiver(receiverSkB[]), rS_1)

m = msg(ctL, ctE, ctS)
```

A 的 `SendDone` 只对应这个原始 `m`、`sid_original` 和 `k_original`。

## 3. 攻击者构造的消息

```text
ctL' = lkem_enc(kpk(kskB[]), r_1)
ctE' = ekem_enc(ekpk(ekskB[]), r)
ctS  = skem_enc(senderSkA[], pk_skem_receiver(receiverSkB[]), rS_1)

m' = msg(ctL', ctE', ctS)
```

`ctL'` 和 `ctE'` 是攻击者使用公开接收方公钥和自己知道的 randomness 构造的；`ctS` 是从 honest sender 原始消息中提取并复用的。

## 4. B 的错误接受流程

1. B 接收 `m'`。
2. B 从 `m'` 中取出 `ctL'`、`ctE'`、`ctS`。
3. B 解封装得到 `KL'`、`KE'`、`KS`。
4. B 基于 `m'` 计算 `sid'`。
5. B 计算 `k' = kdf(KL', KE', KS, sid')`。
6. baseline 中 B 直接触发 `RecvDone(B,A,sid',k')`。
7. 但 A 没有触发 `SendDone(A,B,sid',k')`。

## 5. 一句话结论

该 trace 说明 baseline 中攻击者可以制造 unpartnered receiver session；攻击者不需要知道 `k'`，只需要让 B 接受一个没有 matching `SendDone` 的会话。
