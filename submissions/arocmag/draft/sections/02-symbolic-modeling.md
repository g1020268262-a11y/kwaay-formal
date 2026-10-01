# 2 批处理接纳机制的符号建模

## 2.1 源接口到符号模型的映射

本文模型不重建完整 K-Waay，而是隔离两个发送方相关条目在同一接收方上下文中被组合和接纳时的参与方关系。建模目标是让参与方、发送实例、消息、批次和接收方上下文保持可观察，同时在共同生命周期上只改变接纳谓词。省略密码运算有助于控制比较变量，但不能据此断言被省略的运算不会影响真实接收行为。

原协议和模型使用了同名但含义不同的 `sid`。K-Waay 图 10 中的 `sid` 由双方身份、公钥、预密钥包和协议消息拼接得到，并进入 KDF\cite[Sec. 5.1, Fig. 10]{collins2024kwaayfull}；三个 Tamarin 模型中的 `sid` 则由 `Fr(~sid)` 直接生成，只标识一次模型发送实例。本文统一采用

$$
oid \equiv sid_{\mathrm{model}},
$$

并在论文公式中写 $oid$。模型源码、lemma 名称和原始运行输出仍保留 `sid`，这一记号替换不表示新增变量或模型修改。因此，源码事实 `!Sent(A,sid,m)` 在本文叙述中写作 $!Sent(A,oid,m)$。

表 1 给出源接口到符号模型的映射。表中的“保留”只说明本文观察了相应关系，不表示已经证明二者之间的 simulation 或 refinement。

**表1  K-Waay源接口到接纳模型的映射**  
**Table 1  Mapping from the K-Waay Interface to the Admission Model**

| K-Waay对象 | 模型表示 | 保留的关系 | 未建模或未经证明的部分 |
|---|---|---|---|
| 输入分量 $(pk_j,prek_j,m_j)$ | $E=(A,oid,m)$ | 一个条目的参与方投影、发送实例和消息坐标 | 公钥/参与方解析、预密钥内容、线上消息结构 |
| 一次 `Send` | `Send(A,oid,m)` 与公开三元组 | 一次模型发送来源及其公开可组合输入 | `Send` 的签名、封装、接收方公钥和预密钥绑定 |
| 同一 `BatchReceive` 调用 | 共享 $(bid,rst)$ | 两槽属于同一模型批次和接收方上下文 | 真实 $st_i$ 的密码状态、预密钥生命周期和调度 |
| 原文不同参与方条件 | $A_1\ne A_2$ | 两槽目标关系 | 任意批大小的机器证明、具体执行组件 |
| 逐分量处理和 $k_j$ | `ReceiverAccept(A,oid,m,bid,rst)` | 一个精确来源支持一次模型内处理事件 | $k_j$、会话状态、`KEY/TEST`、应用安装 |
| 批次失败和分量 $\bot$ | M/P 的抽象 `Reject(bid,rst)` 分支 | 受限谓词下的模型拒绝可达性 | K-Waay 的签名失败、split-KEM batch-wide failure 及返回向量 |

模型中的持久事实 $!Sent(A,oid,m)$ 是理想化的精确发送来源事实。`SendMessage` 产生该事实，后续处理规则只有在完整三元组 $(A,oid,m)$ 一致时才能触发 `ReceiverAccept`。它由规则直接提供来源对应性，不是 K-Waay 签名验证、解封装或认证过程的实现。特别地，模型没有编码 signature、KEM、KDF、receiver/prekey binding、原协议 `sid` 的构造、密钥输出、`KEY/TEST` 查询或应用安装。

这种抽象既可能允许不能提升为真实协议执行的符号组合，也可能排除完整协议中的其他行为。被接纳的条目如果缺少精确 $!Sent$ 事实，处理路径可以停滞；模型不会把停滞自动转换成 K-Waay 的某个失败返回。因此，本文不把该抽象称为原协议的天然保守近似，也不声称已经建立从 K-Waay 到 Tamarin 模型的完整精化定理。其结论只适用于下述接纳规则、来源假设和观察事件。

## 2.2 共同生命周期和两槽范围

三个模型共享相同的参与方创建、发送、批次创建、输入收集和顺序处理规则。共同生命周期可概括为

$$
\text{创建参与方}
\rightarrow \text{产生发送实例并公开条目}
\rightarrow \text{收集两槽输入}
\rightarrow \text{接纳或拒绝}
\rightarrow \text{顺序处理}
\rightarrow \texttt{ReceiverAccept}.
$$

首先，`CreateParty` 生成新鲜参与方原子 $A$ 并保存持久事实 $!Party(A)$。该事实可重复使用，因此同一参与方能够触发多个 `SendMessage`。每次发送规则从 `Fr` 分别生成新鲜 $oid$ 和 $m$，记录动作

$$
\operatorname{Send}(A,oid,m),
$$

向网络公开 $\langle A,oid,m\rangle$，并保存精确来源事实 $!Sent(A,oid,m)$。这里的新鲜性是模型构造：不同发送规则实例产生不同的 $oid$ 和 $m$。它不是关于真实消息编码、碰撞概率、重传或原协议 transcript `sid` 的结论。

随后，`CreateBatch` 生成新鲜批次标识 $bid$ 和接收方上下文标识 $rst$，并打开第一个槽位。`CollectSlot1` 从网络接收 $E_1=(A_1,oid_1,m_1)$，线性状态推进到第二槽；`CollectSlot2` 接收 $E_2=(A_2,oid_2,m_2)$，形成

$$
\operatorname{Collected}
(bid,rst,A_1,oid_1,m_1,A_2,oid_2,m_2).
$$

$bid$ 仅标识本次模型批次，$rst$ 仅把两个槽位置于同一抽象接收方上下文。二者均由 `Fr` 生成，但 $rst$ 不包含 K-Waay 的 receiver state、长期密钥、临时秘密或预密钥。模型也没有显式接收方参与方对象。

收集完成后，所选模型执行相应接纳规则。接纳路径记录 `BatchReceive(bid,rst)` 并进入第一槽处理状态。`ProcessSlot1` 只有在存在 $!Sent(A_1,oid_1,m_1)$ 时才产生

$$
\operatorname{ReceiverAccept}
(A_1,oid_1,m_1,bid,rst)
$$

并打开第二槽处理状态；`ProcessSlot2` 以相同方式检查第二个精确来源，产生第二个 `ReceiverAccept` 后到达 `BatchComplete(bid,rst)`。两个处理状态是线性的，因而处理顺序固定；$!Sent$ 是持久事实，若同一精确条目被收集两次，它可以被两个处理规则重复读取。`ReceiverAccept` 不显式携带槽位编号，两个事件由不同时间点和线性处理阶段区分。

模型把批次大小固定为两个槽位。`DistinctPartyPerBatch` 是成对关系，较大批次中的任何违反都至少包含一对参与方投影相同的位置，因此两槽足以表达最小违反形状。然而，较大批次可能具有额外的处理、失败和组合交互；当前模型没有验证这些行为，也没有给出从两槽结果归纳到任意批次大小的证明。

## 2.3 三种接纳语义

三个模型文件在共同生命周期上采用不同的收集后接纳谓词。M 和 P 还分别增加对应的拒绝规则与 `Neq` 动作；因此，“主要比较变量是接纳谓词”不等于三个源文件只相差一行。

**表2  三种两槽接纳模型的语义比较**  
**Table 2  Admission Semantics of the Three Two-Slot Models**

| 模型 | 接纳条件 | 拒绝分支 | 分析角色 |
|---|---|---|---|
| R：宽松接纳（relaxed admission） | 不要求 $A_1\ne A_2$ 或 $m_1\ne m_2$ | 无收集后拒绝分支 | 移除目标不等关系的基线 |
| M：消息级接纳（message-level admission） | 记录 $Neq(m_1,m_2)$，全局限制排除 $Neq(x,x)$ | 消息相同时可触发 `RejectRepeatedMessage` | 比较消息坐标的辅助控制 |
| P：参与方级接纳（party-level admission） | 记录 $Neq(A_1,A_2)$，全局限制排除 $Neq(x,x)$ | 参与方相同时可触发 `RejectRepeatedParty` | 直接维护两槽目标关系的正控制 |

R 的 `AdmitRelaxedBatch` 对参与方和消息均无不等判断，因而接纳规则本身不排除精确重复条目或同参与方不同消息条目。是否存在完成后续处理并满足特定事件约束的执行，仍需由存在性性质验证，不能仅从“没有限制条件”推定完整执行轨迹。

M 的接纳分支比较 $m_1$ 和 $m_2$，但不比较 $A_1$ 和 $A_2$。在当前模型中，每次发送产生 fresh $m$，因此消息比较对精确来源重复具有较强区分能力；真实消息的规范化、重复内容、碰撞和跨批去重均未建模。M 是为检验坐标替代关系而设置的辅助模型，不代表已发现 K-Waay 的实际去重实现或提出具体修复方案。

P 的接纳分支直接比较 $A_1$ 和 $A_2$，是 `DistinctPartyPerBatch` 在两槽抽象中的一个可执行实现。该模型用于验证目标关系在共同处理路径上的保持以及有效批次的非空性（non-vacuity）。直接比较写入接纳条件后，相关安全性质具有正控制性质；它不能被描述为从完整密码运算中自动发现的定理。真实系统也可以由调用方、批次构造器或其他可信组件预先维持同一关系，P 并不规定唯一实现位置。

## 2.4 验证性质与证据口径

模型通过动作事实区分安全性质、存在性见证和拒绝分支可达性。以下公式均使用本文记号 $oid$；`.spthy` 源文件中的对应变量名仍为 `sid`。记 $X@t$ 表示动作 $X$ 在执行轨迹（trace）的时间点 $t$ 发生。

**1）发送来源对应性（sender-origin correspondence）。** 对任意接受事件，要求存在更早的完整三元组匹配发送：

$$
\forall A,oid,m,bid,rst,r.
\operatorname{ReceiverAccept}(A,oid,m,bid,rst)@r
\Rightarrow
\exists s.
\operatorname{Send}(A,oid,m)@s \land s<r.
$$

该性质对应三个模型中的 `receiver_accept_has_send`。由于处理规则直接要求 $!Sent(A,oid,m)$，它表达的是理想来源事实在处理事件中的保持，不是完整协议认证或双方 agreement。

**2）接受事件上的参与方区分与消息区分。** 对一条 trace $\tau$，定义

$$
P_\tau \triangleq
\forall r_1\ne r_2,
\bigl(
\mathsf{RA}(A_1,oid_1,m_1,bid,rst)@r_1
\land
\mathsf{RA}(A_2,oid_2,m_2,bid,rst)@r_2
\bigr)
\Rightarrow A_1\ne A_2,
$$

$$
M_\tau \triangleq
\forall r_1\ne r_2,
\bigl(
\mathsf{RA}(A_1,oid_1,m_1,bid,rst)@r_1
\land
\mathsf{RA}(A_2,oid_2,m_2,bid,rst)@r_2
\bigr)
\Rightarrow m_1\ne m_2,
$$

其中 $\mathsf{RA}(\cdot)$ 是 `ReceiverAccept` 的缩写，两个事件共享同一 $(bid,rst)$。$P_\tau$ 对应 P 的 `accepted_batch_has_distinct_parties`，$M_\tau$ 对应 M 的 `accepted_batch_has_distinct_messages`。

**3）作用域内精确来源单射性（scoped exact-origin injectivity）。** 记 $I_\tau$ 为

$$
\begin{aligned}
\forall A,oid,m,bid,rst,s,r_1,r_2.;&
\operatorname{Send}(A,oid,m)@s \\
&\land \mathsf{RA}(A,oid,m,bid,rst)@r_1
\land \mathsf{RA}(A,oid,m,bid,rst)@r_2 \\
&\land s<r_1 \land s<r_2
\Rightarrow r_1=r_2.
\end{aligned}
$$

它只约束同一批次和接收方上下文中的同一精确来源，不排除跨批次使用，也不是标准 AKE 的全局 injective agreement。

在共同的消息新鲜性、精确来源对应和两槽处理规则下，三个执行轨迹谓词之间满足人工推导关系

$$
(P_\tau\Rightarrow M_\tau)\ \land\ (M_\tau\Leftrightarrow I_\tau),
$$

而消息级模型中的机器见证给出

$$
M_\tau\not\Rightarrow P_\tau.
$$

这些关系只适用于当前模型规则和假设。$P_\tau\Rightarrow M_\tau$ 及 $M_\tau\Leftrightarrow I_\tau$ 是对规则、新鲜性和来源性质的人工推导，不是新增 Tamarin 引理；$M_\tau\not\Rightarrow P_\tau$ 的反例由 M 模型的 `same_party_different_messages_batch_exists` 见证。详细推导和机器/人工证据分界将在第 3 章分析，审计依据另行记录。

**4）存在性与拒绝可达性。** `one_send_two_accepts_exists`、`same_party_different_messages_batch_exists` 和 `distinct_party_batch_exists` 等存在性性质用于确认代表性组合能够形成完整观察轨迹，并为相应安全结论提供反例或非空性依据。M/P 的拒绝存在性只证明抽象拒绝分支存在某条可达轨迹。当前引理中的前置 `Send` 没有与 `Reject(bid,rst)` 所对应的被拒条目绑定，因而不能写成“特定合法发送输入已被证明遭到拒绝”，也不能推出所有无效批次最终都会拒绝的活性结论。

三个未修改模型已有独立复核：在 Tamarin 1.12.0、Maude 3.5.1 环境中重新完成解析与证明，14 个模型—引理实例的状态和证明步数均与原记录一致，其中 13 个得到验证、1 个被反例否定；原始标准输出、错误输出和导出图已经保留。该复核确认当前抽象结果可重复，但不恢复早期历史运行的来源记录，也不补足从 K-Waay 源协议到模型的精化关系。完整结果表和各见证的解释留到第 3 章。

