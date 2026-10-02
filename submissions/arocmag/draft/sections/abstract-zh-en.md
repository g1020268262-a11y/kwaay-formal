# 中文题目

K-Waay批处理接纳中参与方区分条件的形式化分析

## 中文摘要

K-Waay的BatchReceive规定同一调用中的输入应对应不同参与方。为分析该条件在批处理接纳边界上的语义作用，构建共享生命周期的三种固定两槽Tamarin模型。验证表明：放宽条件时，一个精确发送来源可在同一批次支持两次接收事件；消息级限制虽可保证消息区分和作用域内来源单射性，仍允许同一参与方的不同消息共同被接受；参与方级限制保持目标关系且存在有效双接受执行。结果说明，当前符号抽象中的消息区分不能替代批内参与方区分；结论限于理想来源匹配和固定两槽模型。

**关键词：** K-Waay；BatchReceive；形式化验证；Tamarin；批处理接纳

# English Title

Formal Analysis of the Distinct-Party Condition in K-Waay Batch Admission

## Abstract

K-Waay specifies that the inputs of one BatchReceive call correspond to different parties. To examine the semantic role of this condition at the batch-admission boundary, three fixed two-slot Tamarin models with a shared lifecycle are constructed. Verification shows that, after the condition is relaxed, one exact sender origin can support two receiver-acceptance events in the same batch. A message-level restriction ensures message distinction and scoped exact-origin injectivity, but still admits two different messages from the same party. The party-level restriction preserves the target relation while retaining a reachable valid double-acceptance execution. Thus, under the current symbolic abstraction, message distinction cannot substitute for within-batch party distinction. The conclusion is limited to idealized exact-origin matching and fixed two-slot models.

**Key words:** K-Waay; BatchReceive; formal verification; Tamarin; batch admission
