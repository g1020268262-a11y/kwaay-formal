# 原始 K-Waay core 的 Q1 gap

本文件用于记录原始 baseline 中 Q1 false 的原因。

Q1 查询：

  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))

该查询表达：
如果接收方 B 接受了一个声称来自 A 的 session key k，
那么发送方 A 应该已经完成过同一个 sid 和同一个 key 的发送会话。

原始 core 中的问题：
B 在计算出 kRecv 后直接触发 RecvDone。
攻击者可以修改核心 KEM ciphertext，使 B 接受一个没有 exact matching sender session 的 key。

该问题不是 key recovery。
baseline secrecy 仍然可以成立。
它表示的是 explicit receiver agreement / key confirmation 缺失。
