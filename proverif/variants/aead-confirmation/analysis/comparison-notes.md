# Baseline 与 AEAD 分支对比记录

本文件用于整理实验结果。

## baseline

文件：

  proverif/kwaay-core-public-channel.pv

预期：

  Q1 exact receiver agreement: false

## AEAD confirmation variant

文件：

  proverif/variants/aead-confirmation/kwaay-core-public-channel-aead.pv

预期：

  Q1 exact receiver agreement: true

## 对比结论

原始 K-Waay core 主要提供 KIND/secrecy-oriented 目标。
AEAD confirmation 分支提供额外的 explicit receiver agreement / key confirmation。
该分支应被表述为 extension / hardening layer，而不是原始协议本身。
