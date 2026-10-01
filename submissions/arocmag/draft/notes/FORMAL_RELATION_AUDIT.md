# P/M/I形式关系审查

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_2`

## 1. 审查结论

Stage 2 采用无歧义写法

$$
(P_\tau\Rightarrow M_\tau)\land(M_\tau\Leftrightarrow I_\tau),
$$

并单独写出

$$
M_\tau\not\Rightarrow P_\tau.
$$

前三个蕴含方向是对当前共同规则、新鲜性和来源对应性的人工推导。非蕴含由 M 模型的机器验证见证支持。它们不是新增 Tamarin lemma，也不是适用于所有密码协议的一般定理。

## 2. 作用域和精确定义

考虑由三个 `rq-v2-minimal` theory 的共同生命周期产生的一条 trace $\tau$。论文使用 $oid\equiv sid_{model}$；以下 $\mathsf{RA}(A,oid,m,bid,rst)@r$ 缩写动作 `ReceiverAccept(A,sid,m,bid,rst)@r`。

### 2.1 参与方区分 $P_\tau$

$$
\begin{aligned}
P_\tau\triangleq \forall A_1,A_2,oid_1,oid_2,m_1,m_2,bid,rst,r_1,r_2.\;&
\mathsf{RA}(A_1,oid_1,m_1,bid,rst)@r_1 \\
&\land \mathsf{RA}(A_2,oid_2,m_2,bid,rst)@r_2 \\
&\land r_1\ne r_2
\Rightarrow A_1\ne A_2.
\end{aligned}
$$

它与 P theory 的 `accepted_batch_has_distinct_parties` 公式一致，只替换了论文记号。

### 2.2 消息区分 $M_\tau$

$$
\begin{aligned}
M_\tau\triangleq \forall A_1,A_2,oid_1,oid_2,m_1,m_2,bid,rst,r_1,r_2.\;&
\mathsf{RA}(A_1,oid_1,m_1,bid,rst)@r_1 \\
&\land \mathsf{RA}(A_2,oid_2,m_2,bid,rst)@r_2 \\
&\land r_1\ne r_2
\Rightarrow m_1\ne m_2.
\end{aligned}
$$

它与 M theory 的 `accepted_batch_has_distinct_messages` 公式一致。

### 2.3 作用域内精确来源单射性 $I_\tau$

$$
\begin{aligned}
I_\tau\triangleq \forall A,oid,m,bid,rst,s,r_1,r_2.\;&
Send(A,oid,m)@s \\
&\land \mathsf{RA}(A,oid,m,bid,rst)@r_1
\land \mathsf{RA}(A,oid,m,bid,rst)@r_2 \\
&\land s<r_1\land s<r_2
\Rightarrow r_1=r_2.
\end{aligned}
$$

它是三个 theory 中同名 `receiver_accept_injective` 的论文记号版本。作用域由共同的 $bid,rst$ 固定；性质没有禁止同一来源跨批次或跨接收方上下文再次使用。

## 3. 所需假设

推导使用以下模型事实：

1. **消息新鲜性**：每次 `SendMessage` 用 `Fr(~m)` 生成消息原子。在 Tamarin 的符号语义中，同一 fresh 原子不能由两个不同规则实例独立生成。
2. **发送实例新鲜性**：每次 `SendMessage` 同时用 `Fr(~sid)` 生成模型发送实例标识；论文记为 $oid$。
3. **精确来源处理**：`ProcessSlot1/2` 产生 `ReceiverAccept(A,oid,m,...)` 时要求完整匹配的持久事实 $!Sent(A,oid,m)$。
4. **来源对应性**：三个模型的 `receiver_accept_has_send` 均已机器验证；每个接受事件存在更早的精确匹配 `Send(A,oid,m)`。
5. **事件作用域**：$P_\tau$、$M_\tau$ 和 $I_\tau$ 比较同一 $(bid,rst)$ 内的接受事件，且 $r_1\ne r_2$ 表示两个不同事件发生时间点。

不使用以下未建模假设：真实消息碰撞规则、K-Waay transcript `sid` 的构造、recipient/prekey binding、密钥输出、`KEY/TEST` 或任意批大小归纳。

## 4. 各蕴含方向

### 4.1 $M_\tau\Rightarrow I_\tau$

假设 $M_\tau$ 成立，并取 $I_\tau$ 前件中的一个 `Send(A,oid,m)@s` 和两个接受事件。若 $r_1\ne r_2$，这两个事件共享同一 $(bid,rst)$，且消息坐标同为 $m$。$M_\tau$ 要求不同接受事件的消息不同，与 $m=m$ 矛盾。因此只能有 $r_1=r_2$，故 $I_\tau$ 成立。

该方向主要由两个谓词的事件参数关系得到，不需要把消息解释为真实密文。

### 4.2 $I_\tau\Rightarrow M_\tau$

假设 $I_\tau$ 成立，反设同一 $(bid,rst)$ 中存在 $r_1\ne r_2$ 的两个接受事件且 $m_1=m_2=m$。由已验证的来源对应性，两个接受分别有更早的精确匹配 Send。由于 $m$ 在每次 `SendMessage` 中由 `Fr` 新鲜生成，同一 $m$ 不能来自两个不同发送规则实例；两个来源必须是同一 `Send(A,oid,m)@s`，因而相应的 $A$ 和 $oid$ 也相同。此时满足 $I_\tau$ 的完整前件，却有 $r_1\ne r_2$，产生矛盾。因此不同接受事件必有 $m_1\ne m_2$，即 $M_\tau$ 成立。

该方向依赖当前模型的 fresh-message 和 exact-origin 规则。若真实协议允许内容相同的不同发送，或采用不同消息等价关系，该推导不能直接沿用。

### 4.3 $P_\tau\Rightarrow M_\tau$

假设 $P_\tau$ 成立，反设同一 $(bid,rst)$ 中存在两个不同接受事件且 $m_1=m_2=m$。同样利用来源对应性与消息新鲜性，可知两个接受对应同一个 `Send(A,oid,m)`，因此它们的参与方坐标相同。这与 $P_\tau$ 要求不同接受事件具有不同 $A$ 矛盾，故 $m_1\ne m_2$，即 $M_\tau$ 成立。

该方向不是“party inequality 在一般协议中必然推出消息 inequality”；它只是在当前 fresh-message 模型中成立。

## 5. $M_\tau\not\Rightarrow P_\tau$的机器见证

M theory 提供两项互补的机器结果：

- `accepted_batch_has_distinct_messages`：verified，31 steps；保证 M theory 的所有 trace 满足 $M_\tau$。
- `same_party_different_messages_batch_exists`：verified，16 steps；存在同一 $A$ 的两个不同 `sid/m` 发送来源在同一 $(bid,rst)$ 内各产生一次 `ReceiverAccept` 的 trace。

在第二项见证 trace 中，$m_1\ne m_2$ 且两个接受事件不同，因此 $M_\tau$ 成立；两个事件的参与方坐标均为 $A$，所以 $P_\tau$ 不成立。由此得到 $M_\tau\not\Rightarrow P_\tau$。独立复核的 `rqv2_message_dedup-traces.json` 保留了该见证图，同时也显示导出图可包含与公式无关的其他 Send；这些无关事件不改变见证所绑定的两个来源。

## 6. 机器结果与人工推导分界

| 项目 | 证据层次 | 当前状态 |
|---|---|---|
| M 的 $M_\tau$ | Tamarin lemma `accepted_batch_has_distinct_messages` | verified 31，独立复核 MATCH |
| M 的 $I_\tau$ | Tamarin lemma `receiver_accept_injective` | verified 33，独立复核 MATCH |
| P 的 $P_\tau$ | Tamarin lemma `accepted_batch_has_distinct_parties` | verified 31，独立复核 MATCH |
| R 的 $I_\tau$ | Tamarin lemma `receiver_accept_injective` | falsified 13，独立复核 MATCH |
| $M_\tau\not\Rightarrow P_\tau$见证 | Tamarin existence lemma `same_party_different_messages_batch_exists` + M safety | verified 16 + verified 31 |
| $P_\tau\Rightarrow M_\tau$ | 人工规则推导 | 不是 lemma |
| $M_\tau\Rightarrow I_\tau$ | 人工规则推导 | 不是 lemma |
| $I_\tau\Rightarrow M_\tau$ | 人工规则推导 | 不是 lemma |

## 7. 表述限制

- 正文不得把 $M_\tau$ 与 $I_\tau$ 写成两项逻辑独立的研究发现。
- 不得把上述关系推广到真实消息编码、其他协议或任意 batch 大小。
- P guard 直接记录 $Neq(A_1,A_2)$；P safety 是正控制结果，不能写成密码学运算推出的 hidden theorem。
- 现有 rejection existence lemma 与 P/M/I 关系无关，且不绑定具体被拒输入。
- 如果后续改变 freshness、origin matching、事件参数或处理生命周期，必须重新审查全部蕴含方向。

