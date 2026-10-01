# Stage 2 记号一致性表

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_2`  
适用范围：中文稿第 0～2 章及后续章节

## 1. sid/oid最终决定

中文论文采用 $oid$ 表示模型内的发送实例标识，并规定

$$
oid \equiv sid_{\mathrm{model}}.
$$

采用该记号的原因是 K-Waay 原协议自身已经使用 `sid` 表示 transcript/session identifier。图 10 中的原协议 `sid` 由双方身份、公钥、预密钥包和协议消息拼接并输入 KDF；三个 `rq-v2-minimal` 模型中的 `sid` 则是 `SendMessage` 每次触发时由 `Fr(~sid)` 生成的独立新鲜原子。两者来源和语义均不同。

执行规则：

1. 中文论文的解释性公式统一写 $oid$。
2. 引用 `.spthy` 源码、lemma 原名、原始 stdout 或事实原文时保留 `sid`。
3. 首次出现源码事实时写明：`!Sent(A,sid,m)` 在本文记号中等价写作 $!Sent(A,oid,m)$。
4. 不修改任何 `.spthy` 文件，不把 $oid$ 描述为模型新增字段。
5. 提及 K-Waay 的 `sid` 时固定写作“原协议 transcript `sid`”或“原协议会话标识 `sid`”。

## 2. 原协议符号

| 符号 | 原始位置 | 含义 | 中文稿使用约束 |
|---|---|---|---|
| $P_i$ / $i$ | K-Waay Sec. 4.2、Fig. 10 | 当前执行算法的参与方；本文接口说明中通常为接收方 | 不等同于模型的显式 receiver principal；模型没有接收方参与方对象 |
| $P_j$ / $j$ | Sec. 4.1–4.2、Fig. 10 | 对端参与方索引；在接收方会话中索引输入和密钥分量 | 不称为“槽位编号”；重复 $j$ 的扩展语义未建立 |
| $sk_i$ | Sec. 4.1、Fig. 10 | 执行方长期秘密密钥 | 当前模型没有对应对象 |
| $st_i$ | Sec. 4.1、Fig. 10 | `Init` 输出并传给 `Send`/`BatchReceive` 的会话状态 | 不与模型 $rst$ 等同；$rst$ 只标识抽象上下文 |
| $pk_j$ | Sec. 4.1、Fig. 10 | 声称发送方 $P_j$ 的长期公钥 | 模型投影只保留参与方坐标 $A$，未验证 key-to-party 映射 |
| $prek_j$ | Sec. 4.1、Fig. 10 | 声称发送方的预密钥包 | 当前模型未编码 |
| $m_j$ | Sec. 4.1、Fig. 10 | 输入中的协议消息 | 模型 $m$ 是 fresh 原子，不重建密文三元组 |
| $k_j$ | Fig. 10、Sec. 4.2.3 | `BatchReceive` 对参与方索引 $j$ 的输出分量 | `ReceiverAccept` 不是 $k_j$，模型无密钥输出 |
| 原协议 `sid` | Fig. 10 lines 9/12；Sec. 4.2.1 | 由参与方、key/prekey 和消息形成的会话标识；接收方可持有向量 | 不用 $oid$ 替代其协议含义；只在 source 描述中写 `sid` |
| $\pi_i^s$ | Sec. 4.2.1 | $P_i$ 的第 $s$ 个安全游戏会话 | 当前模型没有一一对应对象 |
| `pid` | Sec. 4.2.1–4.2.3 | partner identifier；接收方时为对端参与方索引向量 | 只用于解释原游戏，不能写入当前模型结果 |
| `KEY(i,s,j)` | Sec. 4.2.3 p.17 | 接收方会话下取 $k_j$；发送方会话返回单个 $k$ | 当前模型不验证该查询 |
| `TEST(i,s,j)` | Sec. 4.2.3 pp.17–18 | 对接收方要求 $j\in pid$ 并选择 $k_j$ 作 real-or-random challenge | 只能作为 party-indexed 接口动机 |

## 3. 模型符号

| 论文记号 | 源码记号 | 含义 | 作用域/限制 |
|---|---|---|---|
| $A$ | `A` | 模型参与方坐标 | 不是账户、公钥编码或数据库身份 |
| $oid$ | `sid` | 一次 `SendMessage` 的新鲜发送实例标识 | 不是原协议 transcript `sid` |
| $m$ | `m` | 每次发送实例生成的 fresh 消息原子 | 不模拟真实内容相等、重传或碰撞 |
| $E=(A,oid,m)$ | `<A,sid,m>` | 候选接纳条目/公开三元组 | 不是 K-Waay wire tuple |
| $\ell\in\{1,2\}$ | `Slot1/Slot2` 状态 | 两槽模型中的位置 | 不等于原协议参与方索引 $j$ |
| $bid$ | `bid` | fresh 批次标识 | 只标识模型批次 |
| $rst$ | `rst` | fresh 接收方上下文标识 | 不重建 $st_i$ 或预密钥状态 |
| `Send(A,oid,m)` | `Send(A,sid,m)` | 一次模型发送来源动作 | action fact，不是完整 `Send` 算法 |
| $!Sent(A,oid,m)$ | `!Sent(A,sid,m)` | 可复用的精确发送来源事实 | 理想 origin，不是认证实现 |
| `BatchReceive(bid,rst)` | 同名 action | 通过模型接纳分支 | 不等于完整 K-Waay 算法执行 |
| `ReceiverAccept(A,oid,m,bid,rst)` | 源码 `ReceiverAccept(...sid...)` | 条目在精确来源支持下完成一次抽象处理 | 直接证据终点；不是协议会话接受或 key 输出 |
| `Reject(bid,rst)` | 同名 action | M/P 抽象拒绝分支动作 | 不携带被拒条目；现有 lemma 不能绑定前置 Send |
| `BatchComplete` / `BatchRejected` | 同名 state facts | 模型线性状态终点 | 不是应用安装或部署状态 |

## 4. 性质记号

| 记号/术语 | 固定中文 | 精确定义边界 |
|---|---|---|
| $P_\tau$ | trace $\tau$ 上的参与方区分 | 同一 $(bid,rst)$ 中不同 `ReceiverAccept` 事件的 $A$ 不同 |
| $M_\tau$ | trace $\tau$ 上的消息区分 | 同一 $(bid,rst)$ 中不同接受事件的 $m$ 不同 |
| $I_\tau$ | 作用域内精确来源单射性 | 同一 exact $(A,oid,m)$ 和 $(bid,rst)$ 不对应两个不同接受时间点 |
| sender-origin correspondence | 发送来源对应性 | 每个接受事件存在更早的精确匹配 `Send` |
| non-vacuity | 非空性 | 至少有一个满足目标条件并完成相关事件的执行 |
| reachability witness | 可达性见证 | 存在一条满足公式的 trace，不是全称安全性质 |
| rejection reachability | 拒绝分支可达性 | 存在 `Reject` trace；不等于特定 sender 输入被拒或最终必拒 |

正式关系固定写为

$$
(P_\tau\Rightarrow M_\tau)\land(M_\tau\Leftrightarrow I_\tau),
\qquad
M_\tau\not\Rightarrow P_\tau.
$$

不得恢复为可能产生结合歧义的 `Pτ ⇒ Mτ ⇔ Iτ`。

## 5. 固定术语

| 英文术语 | 首次出现写法 | 后续固定用语 |
|---|---|---|
| party | 参与方（party） | 参与方 |
| sender occurrence | 发送实例（sender occurrence） | 发送实例 |
| message | 消息（message） | 消息 |
| slot | 槽位（slot） | 槽位 |
| batch admission | 批处理接纳（batch admission） | 批处理接纳 |
| receiver context | 接收方上下文（receiver context） | 接收方上下文 |
| origin correspondence | 发送来源对应性（sender-origin correspondence） | 发送来源对应性 |
| scoped exact-origin injectivity | 作用域内精确来源单射性 | 作用域内精确来源单射性 |
| non-vacuity | 非空性（non-vacuity） | 非空性 |
| `ReceiverAccept` | 模型接受事件 `ReceiverAccept` | `ReceiverAccept`；不简称“协议接受” |

## 6. 禁止混同

- 参与方不同不能改写为消息不同、发送实例不同、槽位不同或公钥字节不同。
- $rst$ 不能称为已建模的 K-Waay receiver state。
- $!Sent$ 不能称为签名/KEM 验证结果或完整 authentication。
- `ReceiverAccept` 不能称为生成、安装或返回了 $k_j$。
- 原协议合法域内的 $j$ 关联不能扩展为重复 $j$ 时已定义的输出选择。
- batch-local exact-origin injectivity 不能简称为标准 AKE injective agreement 或全局 replay resistance。

