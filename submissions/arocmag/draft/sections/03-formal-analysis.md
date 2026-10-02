# 3 形式化验证与结果分析

本章依据三个未修改的两槽 Tamarin 模型及 2026 年 9 月 16 日的独立复核证据分析接纳行为。存在性性质用于给出至少一条满足公式的可达执行，全称性质用于约束相应模型的全部执行轨迹；二者承担的证据作用不同。除特别说明外，正文继续使用 $oid\equiv sid_{\mathrm{model}}$，并把直接观察终点限定为 `ReceiverAccept`。

## 3.1 宽松接纳模型中的精确来源重复接受

宽松接纳模型 R 在收集两个条目后直接触发 `AdmitRelaxedBatch`，不比较参与方、发送实例或消息坐标。`normal_relaxed_batch_exists` 以 10 步得到验证，表明该生命周期至少可以到达一次 `BatchReceive` 和随后的 `ReceiverAccept`。这一结果只排除“模型完全不能完成接纳处理”的空模型解释，不提供参与方区分证据。

核心存在性性质 `one_send_two_accepts_exists` 以 13 步得到验证。其见证满足

$$
\begin{aligned}
&\operatorname{Send}(A,oid,m)@s,\\
&\operatorname{BatchReceive}(bid,rst)@b,\\
&\mathsf{RA}(A,oid,m,bid,rst)@r_1,\\
&\mathsf{RA}(A,oid,m,bid,rst)@r_2,\\
&s<b<r_1<r_2,
\end{aligned}
$$

并附加同一精确三元组的发送唯一性条件

$$
\forall s_2.\ 
\operatorname{Send}(A,oid,m)@s_2
\Rightarrow s_2=s.
$$

这里的唯一性只针对与 $(A,oid,m)$ 完全匹配的 `Send`。它不能被解释为整条执行中只有一次发送；独立复核导出的 graph 确实还包含与见证变量无关的其他 `Send`，但这些事件不改变公式所绑定的精确来源。见证中的同一公开三元组被 `CollectSlot1` 和 `CollectSlot2` 分别收集，随后两个处理规则在同一 $(bid,rst)$ 下复用持久事实 $!Sent(A,oid,m)$，因而在不同时间点产生两个参数完全相同的 `ReceiverAccept`。

与该存在性结果对应，R 中的全称性质 `receiver_accept_injective` 以 13 步被反例否定。该性质要求：如果同一 $(A,oid,m)$ 的发送来源先于同一批次和接收方上下文中的两个匹配接受事件，则两次接受必须发生在同一时间点。上述见证满足其前件，却有 $r_1<r_2$，因此给出直接反例。与此同时，`receiver_accept_has_send` 以 8 步得到验证，说明反例没有依赖无来源条目；两个接受事件共享的是一个理想化的精确来源。

被否定的性质是本文定义的作用域内精确来源单射性，而不是标准 AKE 中的 injective agreement。该执行也不属于 K-Waay 原文规定的不同参与方输入域：它只说明，在取消坐标不等限制的当前两槽抽象中，一个公开条目可以占据两个槽并到达两个模型接受事件，不能据此声称完整 K-Waay 存在真实重放攻击或认证失效。

> **图2  宽松接纳模型中的精确来源重复接受执行**  
> **Fig. 2  Exact-Origin Duplicate-Acceptance Execution in the Relaxed Model**  
> 注：根据 Tamarin 见证人工整理，不是 prover 直接导出的原始攻击图。

## 3.2 消息级接纳模型的限制与反例

消息级接纳模型 M 在接纳分支记录 $Neq(m_1,m_2)$，并由全局限制排除 $Neq(x,x)$，因而接纳条件为

$$
m_1\ne m_2.
$$

`repeated_message_rejection_exists` 以 4 步得到验证，只说明消息相等时抽象拒绝分支存在一条可达执行。该 lemma 中的前置 `Send` 没有与 `Reject(bid,rst)` 对应的被拒条目绑定，因此不能据此断言某个特定合法发送输入已被拒绝，也不能推出所有等消息批次最终都会进入拒绝分支。

对接受路径，`accepted_batch_has_distinct_messages` 以 31 步得到验证：同一 $(bid,rst)$ 中两个不同时间点的 `ReceiverAccept` 必须具有不同消息坐标。`receiver_accept_injective` 以 33 步得到验证，表明同一精确来源不能在该上下文中支持两个不同接受事件；`receiver_accept_has_send` 仍以 8 步得到验证。由此，R 中“同一三元组占据两个槽”的精确重复形状不能在 M 的接受路径上重现。

消息级限制并未维护参与方关系。`same_party_different_messages_batch_exists` 以 16 步得到验证，其见证由同一参与方 $A$ 的两个发送实例组成：

$$
E_1=(A,oid_1,m_1),qquad
E_2=(A,oid_2,m_2),
$$

其中

$$
oid_1\ne oid_2,qquad m_1\ne m_2.
$$

机器公式同时绑定两个发送和两个接受：

$$
\begin{aligned}
&\operatorname{Send}(A,oid_1,m_1)@s_1,
\quad \operatorname{Send}(A,oid_2,m_2)@s_2,\\
&\operatorname{BatchReceive}(bid,rst)@b,\\
&\mathsf{RA}(A,oid_1,m_1,bid,rst)@r_1,
\quad \mathsf{RA}(A,oid_2,m_2,bid,rst)@r_2,\\
&s_1<b,quad s_2<b,quad b<r_1<r_2.
\end{aligned}
$$

因此，两次接受分别具有自己的精确匹配来源，见证没有制造 origin mismatch，也没有把一个发送错误归属给另一参与方。它展示的是：在消息坐标已经区分、精确来源单射性已经成立的情况下，两个条目的参与方投影仍可相同。换言之，M 在其所约束的坐标上有效排除了精确消息重复，但实际模型行为仍给出 $M_\tau$ 不蕴含 $P_\tau$ 的反例。

这一结果不能扩展为身份错误归属、未知密钥共享（UKS）、misbinding 或密钥泄露。模型没有对端密钥、会话密钥、`KEY/TEST` 或应用安装事件；见证也不在 K-Waay 原文规定的不同参与方合法输入域内。它的证据价值在于说明，message-coordinate control 与批内参与方区分观察的是不同关系。

## 3.3 参与方级接纳模型的性质验证

参与方级接纳模型 P 把接纳条件直接设为

$$
A_1\ne A_2.
$$

`AdmitDistinctParties` 记录 $Neq(A_1,A_2)$，全局不等限制排除参与方相同的接纳分支。相应的全称性质 `accepted_batch_has_distinct_parties` 以 31 步得到验证：同一 $(bid,rst)$ 中两个不同 `ReceiverAccept` 的参与方坐标必不相同。这一结论说明目标关系在当前两槽处理路径上得到保持；由于接纳规则直接维护同一关系，它是正控制结果，而不是从完整密码运算中发现的新安全定理。

安全性质没有依靠拒绝全部输入获得空真。存在性性质 `distinct_party_batch_exists` 以 17 步得到验证，给出两个不同参与方及其各自精确来源在一个批次中完成双接受的执行：

$$
\begin{aligned}
&\operatorname{Send}(A_1,oid_1,m_1)@s_1,
\quad \operatorname{Send}(A_2,oid_2,m_2)@s_2,\\
&A_1\ne A_2,\\
&\operatorname{BatchReceive}(bid,rst)@b,\\
&\mathsf{RA}(A_1,oid_1,m_1,bid,rst)@r_1,
\quad \mathsf{RA}(A_2,oid_2,m_2,bid,rst)@r_2,\\
&s_1<b,quad s_2<b,quad b<r_1<r_2.
\end{aligned}
$$

该见证只建立非空性，即至少存在一个有效的双接受执行；它不证明所有满足参与方区分的候选批次最终都会完成。P 中 `receiver_accept_has_send` 和 `receiver_accept_injective` 分别以 8 步和 33 步得到验证，为同一处理路径提供模型内来源对应和精确来源单射性，但不增加协议层认证或活性结论。

`same_party_rejection_exists` 以 5 步得到验证，说明参与方相同时抽象拒绝分支可达。与 M 的拒绝性质相同，其公式虽然列出两个同参与方、不同发送实例和不同消息的前置 `Send`，却没有把这些三元组绑定到 `Reject(bid,rst)` 所对应的 `Collected`。因此，机器结果的最强表述仍是“拒绝分支非空”。规则层可以直接看出 `RejectRepeatedParty` 匹配参与方相同的已收集条目，但现有 existence lemma 不是特定被拒条目的机器见证。

P 仅给出直接维护目标关系的一种抽象实现。真实系统可以由调用方、批次构造器、接收方接纳层或其他具有可靠参与方归属信息的组件维持该关系；当前结果不规定唯一检查位置，也不证明某个部署应当新增相同规则。

## 3.4 综合结果与性质关系分析

表 3 汇总三个模型源文件中的全部 14 个 model–lemma 实例。独立复核直接解析并证明三个未修改模型，复核结果与历史记录逐项比较；`Steps` 仅用于对应本次运行记录，不作为工具性能指标。

**表3  三种批处理接纳模型的形式化验证及独立复核结果**  
**Table 3  Formal Verification and Independent Rerun Results for the Three Batch-Admission Models**

| Model | Lemma | Property Type | Outcome | Steps | Independent Rerun Match |
|---|---|---|---|---:|---|
| R | `normal_relaxed_batch_exists` | exists-trace / 基本可达性 | VERIFIED | 10 | MATCH |
| R | `one_send_two_accepts_exists` | exists-trace / 精确来源重复接受见证 | VERIFIED | 13 | MATCH |
| R | `receiver_accept_has_send` | all-traces / 来源对应性 | VERIFIED | 8 | MATCH |
| R | `receiver_accept_injective` | all-traces / 作用域内精确来源单射性 | FALSIFIED WITH COUNTEREXAMPLE | 13 | MATCH |
| M | `repeated_message_rejection_exists` | exists-trace / 拒绝分支可达性 | VERIFIED | 4 | MATCH |
| M | `same_party_different_messages_batch_exists` | exists-trace / 同参与方不同消息见证 | VERIFIED | 16 | MATCH |
| M | `accepted_batch_has_distinct_messages` | all-traces / 消息区分 | VERIFIED | 31 | MATCH |
| M | `receiver_accept_has_send` | all-traces / 来源对应性 | VERIFIED | 8 | MATCH |
| M | `receiver_accept_injective` | all-traces / 作用域内精确来源单射性 | VERIFIED | 33 | MATCH |
| P | `same_party_rejection_exists` | exists-trace / 拒绝分支可达性 | VERIFIED | 5 | MATCH |
| P | `distinct_party_batch_exists` | exists-trace / 不同参与方双接受见证 | VERIFIED | 17 | MATCH |
| P | `accepted_batch_has_distinct_parties` | all-traces / 参与方区分 | VERIFIED | 31 | MATCH |
| P | `receiver_accept_has_send` | all-traces / 来源对应性 | VERIFIED | 8 | MATCH |
| P | `receiver_accept_injective` | all-traces / 作用域内精确来源单射性 | VERIFIED | 33 | MATCH |

独立复核环境为 WSL Ubuntu 24.04、Tamarin 1.12.0 和 Maude 3.5.1。manifest 记录的三个模型 SHA-256 与当前权威源文件一致；7 次 version/parse/prove 调用均正常结束，三个 prove transcript 的 wellformedness checks 均成功。14 项状态和步数全部匹配，其中 13 项为 verified，1 项为 falsified with trace；证据包保留 raw stdout/stderr 以及 7 个 JSON graph。该证据是 2026 年 9 月 16 日针对明确代码版本完成的独立重跑，不是历史 freeze 日志的恢复。它确认当前抽象结果可重复，但不产生新的安全性质，也不补足从 K-Waay 到抽象模型的精化关系。

为比较三个坐标，沿用第 2.4 节在一条当前共同生命周期轨迹 $\tau$ 上定义的参与方区分 $P_\tau$、消息区分 $M_\tau$ 和作用域内精确来源单射性 $I_\tau$。在消息由每次 `SendMessage` 新鲜生成、每个接受具有更早的精确匹配来源、且事件固定在同一 $(bid,rst)$ 的条件下，有人工推导关系

$$
(P_\tau\Rightarrow M_\tau)
\land
(M_\tau\Leftrightarrow I_\tau).
$$

各方向的理由如下。若 $M_\tau$ 成立，同一 $(A,oid,m)$ 在两个不同时间点被接受会直接违反消息区分，因此 $M_\tau\Rightarrow I_\tau$。反之，若两个不同接受事件具有相同消息，则来源对应性和 fresh $m$ 迫使二者追溯到同一个 `Send(A,oid,m)`；$I_\tau$ 随即排除两个不同接受时间点，故 $I_\tau\Rightarrow M_\tau$。同样地，相同消息迫使精确来源及参与方坐标相同，因此 $P_\tau$ 排除这种情况，得到 $P_\tau\Rightarrow M_\tau$。这些方向依赖当前 freshness、origin matching 和事件作用域，是规则层人工推导，不是 Tamarin 单独验证的跨理论 lemma。

M 的机器见证进一步给出

$$
M_\tau\not\Rightarrow P_\tau.
$$

`accepted_batch_has_distinct_messages` 说明 M 的全部轨迹满足消息区分，`same_party_different_messages_batch_exists` 则给出一条消息不同而参与方相同的双接受轨迹；二者共同支持这一非蕴含判断。这里仍需区分三个证据层次：具体 theory 的 all-traces lemma 约束该 theory 的全部轨迹，exists-trace lemma 只给出一条见证，而 $P/M/I$ 的前三个蕴含方向是基于共同规则的人工逻辑推导。

综合来看，单个条目的来源对应性、接受消息之间的区分以及同一批次内的参与方区分是三个不同研究对象。当前模型中的消息级限制能够排除精确消息重复和相应的重复接受形状，却不能替代 K-Waay 接口所要求的批内参与方关系；参与方级模型则为该目标关系提供安全性与非空性的正控制。上述归纳止于固定两槽、理想精确来源和 `ReceiverAccept` 观察边界，不能升级为完整 K-Waay 协议的安全失效、密钥后果或任意批次大小结论。
