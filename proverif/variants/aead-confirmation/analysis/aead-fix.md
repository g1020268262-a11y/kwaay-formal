# AEAD confirmation 如何修复 Q1

AEAD 分支中，发送方在计算 kSend 后生成：

  kc = aead_tag(kSend, sidAB)

接收方在计算 kRecv 后必须验证：

  aead_verify(kRecv, sidBA, kcFromNet) = aead_ok

只有验证成功，接收方才触发：

  AeadConfirmed
  ReceiverKey
  RecvDone

因此攻击者即使修改 ctL, ctE 或 ctS，使接收方计算出新的 sidBA 和 kRecv，
也无法生成对应的 kc。

所以攻击者只能让接收方进入 RecvComputed，
不能让接收方进入 RecvDone。
