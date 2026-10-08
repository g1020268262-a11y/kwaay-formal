# K-Waay 原接口到两槽符号模型的映射审查

## 1. 证据分层

本报告使用四类标记，避免把原文事实、模型编码和作者解释混为一谈。

- **S（source）**：K-Waay full version 明确陈述的事实。主要依据 `reviews/2026-09-16-evidence/kwaay-full-2024-120.pdf`：第4.1节第15页的接口语法，第4.2.1节第16页的会话字段与接收方向量，第5.1节第20--21页及图10的具体构造。
- **M（model）**：三个 `.spthy` 文件直接编码的规则、事实或动作。
- **A（author inference）**：为研究问题建立的作者抽象或条件性解释。
- **U（unestablished）**：当前没有 refinement、实现证据或机器证明支持的连接。

原文的关键事实为：`BatchReceive(ski,sti,{pkj,prekj,mj}j)` 接收大小 `d≥1` 的向量并输出 `d` 个密钥；接收会话的 `sid`、`pid` 和 `k` 是向量；K-Waay 图10以同一接收方状态逐项处理输入，任一 split-KEM 解封装失败时整批返回失败；原文第5.1节明确假设同一次 `BatchReceive` 调用中的每个元素对应不同参与方。

## 2. 严格 source-to-model 映射表

| 原协议对象 | 当前模型对象 | 保留的语义 | 省略的语义 | 有什么证据支持映射 | 可以得出什么结论 | 不能得出什么结论 |
|---|---|---|---|---|---|---|
| 参与方 `Pi/Pj` 及其长期公钥索引 | 条目首分量 `A`、持久事实 `!Party(A)` | 条目可投影到一个抽象协议主体；同一 `A` 可产生多次发送 | 公钥到主体的唯一解析、账户/设备/凭据关系、恶意注册、密钥轮换 | S：第4.2.1节把 `Pi` 与长期密钥对关联，输入以发送方 `pkj` 索引；M：`CreateParty`/`!Party(A)`；A：作者选择 `A` 作为 party projection | 在假定输入已有正确参与方投影时比较同批 `A1` 与 `A2` | 不能把账户、公钥字节串、预密钥记录和参与方视为天然等价，也不能证明实现中的身份解析正确 |
| 原协议 `Send(ski,pkj,sti,prekj)` | `SendMessage` 与动作 `Send(A,sid,m)` | 一个抽象参与方产生一次发送发生及消息，后续可按完整三元组追踪 | 签名检查、KEM/split-KEM 封装、目标接收方、预密钥、输出密钥、KDF 和具体线路编码 | S：第4.1节 `Send` 语法和图10第1--11行；M：三个模型的 `SendMessage` | 可讨论模型中发送来源和接受事件的对应 | 不能证明真实 `Send` 成功、密钥正确、发送方认证或 K-Waay 安全游戏性质 |
| 原协议消息 `mj=(ctℓ,ctk,cts)` | 符号原子 `m` | 不同发送规则实例可携带不同消息坐标；消息随条目进入批次 | 密文结构、相等语义、概率算法、重发时能否得到相同编码、解封装结果 | S：图10第4、8行；M：`Fr(~m)` 及 `Out(<A,sid,m>)`；A：以原子代表发送方产生的消息 | 可在当前新鲜消息抽象中验证同批消息互异 | 不能评价真实消息去重、碰撞、序列化相等、跨批缓存或同内容重发 |
| 原协议完整 `sid=Pi||Pj||pki||pkj||preki||prekj||m` | 论文记号 `oid`，Tamarin 变量 `sid` | 只保留“区分 `SendMessage` 规则实例”的发生坐标 | 双方身份、公钥、预密钥和消息拼接形成的原会话标识及 partnering 语义 | S：图10 `Send` 第9行、`BatchReceive` 第12行；M：`Fr(~sid)`；A：中文稿明确将其重命名为 `oid` 以避免混同 | 可区分两个模型发送发生，并与消息和主体共同构成精确来源元组 | 不能把 `oid` 等同于 K-Waay 完整 session identifier、transcript、时间戳或原安全游戏的 partnering 依据 |
| 发送方消息可被对手交付给接收接口 | `Out(<A,sid,m>)` 与 `In(<A,sid,m>)` | 条目暴露后可由 Dolev--Yao 网络保留、重放、选择和重排 | 真实传输通道、调用者权限、batch builder、API 参数来源及部署信任边界 | M：`SendMessage` 的 `Out`、两个收集规则的 `In`；A：批次组合控制是显式攻击者假设 | 可在模型内研究重复或重组已暴露条目 | 不能声称真实网络攻击者已经能控制合规实现的批次构造 |
| 一个发送来源及其合法密码计算 | 持久事实 `!Sent(A,sid,m)` | 接受前必须存在与完整 `(A,sid,m)` 相等的模型来源；同一持久事实可被两个槽位读取 | 签名、KEM 和 split-KEM 验证，目标接收方、密钥一致性、计算安全认证 | M：只有 `SendMessage` 产生 `!Sent`，`ProcessSlot1/2` 精确读取它；机器 lemma `receiver_accept_has_send` | 可得模型内“接受有更早完整元组匹配发送” | 不能解释成真实密码学认证、隐式认证、matching conversation 或 Lowe 单射一致性 |
| `BatchReceive` 的输入向量 `{pkj,prekj,mj}j` | `CollectSlot1`、`CollectSlot2` 收集两个 `(A,sid,m)` | 一次抽象调用内存在两个有序输入位置，可选择同一或不同来源条目 | 任意 `d≥1`、真实公钥/预密钥、向量索引、输入合法域检查、批量失败传播 | S：第4.1节输入向量；M：两槽线性收集状态；A：固定两槽是最小非平凡实例 | 可分析最小两位置的重复参与方关系 | 不能证明任意批次长度，也不能断言模型收集阶段与具体 API 调用逐步精化 |
| 同一接收方临时状态 `sti` 被一个 `BatchReceive` 调用中的多个条目共享 | 新鲜上下文坐标 `rst`，与 `bid` 一起在线性状态中传递 | 两个接受属于同一抽象接收上下文 | `sti=(esski,ekski,preki)` 的密码状态、状态泄露、状态生命周期和跨调用复用 | S：第4.1节语法、图10第1行及第5.1节共享同一 secret keys 的说明；M：`CreateBatch` 生成 `rst`，后续规则原样传递；A：`rst` 是坐标化抽象 | 可将两次接受限定到共同接收上下文 | 不能把 `rst` 当作完整 K-Waay 临时密码状态，或分析 state reveal、回滚和重启 |
| 一次 `BatchReceive` 调用及其批次边界 | 新鲜 `bid`、共享 `(bid,rst)`、动作 `BatchReceive(bid,rst)` | 把两个收集条目与一次准入/处理生命周期关联 | 原接口调用栈、调用次数、真实 session object、线程和错误返回 | S：第4.1节一次调用接收一个向量；M：`CreateBatch`、各准入规则和动作事实 | 可定义批内作用域，区分跨批事件 | 不能证明 `bid` 对应原协议已有字段，或给出跨批次/重启保证 |
| 原文“同次调用各元素对应不同参与方” | 目标 `A1≠A2`；P 模型 `AdmitDistinctParties`/`RejectRepeatedParty` | 保留两槽实例中的参与方投影互异关系 | 谁负责建立 party projection、谁执行检查、原算法在域外输入上的行为 | S：第5.1节第21页图10后明确句；M：P 模型的 `Neq(A1,A2)` 与目标 lemma；A：把 source condition 解释为 party projection relation | 可构造该关系的两槽正控制，并比较去除或换坐标后的模型行为 | 不能声称原协议遗漏条件、唯一实现必须显式比较 `A`，或真实实现没有维护该关系 |
| 放宽、消息互异、参与方互异三种准入语义 | `AdmitRelaxedBatch`、`AdmitDistinctMessages`、`AdmitDistinctParties` | 在相同模型生命周期上控制是否比较 `m` 或 `A` | 原 K-Waay 没有定义 relaxed 或 message-dedup 变体；真实域外调用语义未给出 | M：三条真实准入规则；A：受控比较设计 | 可回答“在该抽象中，消息条件能否替代目标 party relation” | 不能声称现实系统采用消息去重作为替代，也不能把 R/M 模型称为 K-Waay 实现 |
| 图10中的逐项接收处理 | `ProcessSlot1`、`ProcessSlot2` | 两个槽按顺序处理；每个接受保留条目与共同上下文坐标 | 验签、三次解封装、`fail` 标志、整批失败、KDF 和每项密钥 | S：图10第3--17行；M：两个顺序线性处理规则；A：只保留来源匹配端点 | 可检查两个槽是否都能到达模型接受事件 | 不能推出真实逐项密钥输出、批量失败语义或接收会话最终 status |
| 每个输入对应的输出密钥 `kj`；接收 session 的 `k/pid/sid` 向量；总体 accept/reject status | 动作 `ReceiverAccept(A,sid,m,bid,rst)` 和终态 `BatchComplete` | 提供一个来源匹配后的模型观察点，并区分两个事件发生 | 输出密钥、`⊥`、会话 status、partnering、`KEY/TEST`、密钥安装或应用消费 | S：第4.1节输出向量、第4.2.1节字段及 accept 条件；M：`ReceiverAccept`、`BatchComplete`；A：模型局部观察事件 | 可说抽象生命周期中两个来源匹配条目产生两个接受事件 | 不能等同于完整协议完成、会话接受、密钥安装、安全游戏成功或上层状态改变 |
| K-Waay 的整批失败与错误返回 | M/P 模型的 `Reject`、`BatchRejected` 分支 | 仅保留“某类候选对可进入抽象拒绝分支” | 图10只由 split-KEM 失败触发的 `fail` 语义；消息/参与方相等并非原算法的密码失败条件 | S：图10第13、16行；M：两个研究性拒绝规则；A：控制模型的分析分支 | 可确认研究性拒绝分支可达 | 不能把 `RejectRepeatedMessage/Party` 当作原 K-Waay 已定义的错误处理或实现修复 |

## 3. 五个重点对象的结论

### 3.1 `A` 能否表示原协议 party

可以作为**有条件的抽象投影**。原文确实以 `Pj`、`pkj`、receiver `pid` 向量和“different party”描述输入与参与方的关系，所以研究中保留 party coordinate 有来源依据。但是，当前模型直接把 `A` 放在公开条目中，没有验证公钥、预密钥或账户记录如何解析为同一主体。结论必须以前提“输入已带有正确、稳定的参与方投影”为限。

### 3.2 `oid` 与原协议 session identifier 的关系

仅有概念上的“发送发生坐标”关系，不是同一对象。原协议 `sid` 包含两方身份、公钥、预密钥和消息，并进入 KDF 与 partnering；当前 `sid` 是每次 `SendMessage` 新鲜生成的原子，中文稿称 `oid`。当前命名已避免直接混同，审查建议继续保持。

### 3.3 `!Sent` 能保证什么

它保证模型中存在一个更早、参数完全相同的发送来源，并允许精确分析一个来源是否被同批两个处理步骤读取。它不执行任何密码计算，不能提升为真实发送方认证、隐式认证、密钥一致性或完整协议 correspondence。

### 3.4 `(bid,rst)` 代表什么

它们是一次模型批次和共同接收上下文的坐标。`rst` 借用了原接口“多个输入共享接收方状态”的结构，但不包含该状态的密码材料或生命周期；`bid` 是模型新鲜标识，不是 K-Waay 原文给出的线路字段。

### 3.5 `ReceiverAccept` 代表什么

它只表示某槽在精确来源事实存在时到达模型的接受观察点。原 K-Waay 接收 session 的 status、输出密钥向量、partnering 和安全游戏对象均未建模，所以不能把一个或两个 `ReceiverAccept` 解释为一次或两次完整协议会话接受。

## 4. 三个层次的充分性判断

| 判断层次 | 结论 | 理由 |
|---|---|---|
| **模型内命题** | **足够** | 三模型共享发送、公开、两槽收集、精确来源匹配和顺序处理，只改变准入维度；现有机器结果足以说明 M 模型中同参与方异消息批次可达，而 P 模型保持目标关系且有效批次可达 |
| **K-Waay 接口层面的条件性解释** | **有条件地足够** | 原文确有同次 `BatchReceive` 的 different-party 假设，模型保留了批内 party projection；只要明确假设实现对象能正确映射到 `A`，可说明条目级消息/来源性质不自动承担该 party relation |
| **完整协议安全结论** | **不足** | 无 concrete-message semantics、密码计算、session status、key output、`KEY/TEST`、consumer、任意批长或 refinement/witness-lifting；不能据此得出 K-Waay 漏洞、认证失败、密钥泄露或部署缺陷 |

## 5. 已建立、推论和未建立连接

- **原文明确事实**：输入向量、共享接收状态、输出密钥向量、接收方会话的向量字段、不同参与方假设。
- **模型编码事实**：固定两槽、fresh `sid/m/bid/rst`、Dolev--Yao `Out/In`、精确 `!Sent`、三种准入规则、两个顺序处理步骤和模型局部事件。
- **作者推论**：把 claimed sender party 投影为 `A`，把一次模型生命周期解释为一次批次准入比较，把 `ReceiverAccept` 作为来源匹配后的分析端点。
- **尚未建立**：实现身份解析、原 `sid` 到 `oid` 的保持关系、具体 `BatchReceive` 执行到两槽迹的精化、真实域外输入行为、输出密钥/状态影响和攻击者对部署 batch builder 的控制。

**审计结论：当前 source-to-model 连接足以支撑一个边界明确的接口条件案例分析，不足以支撑完整协议或部署安全结论。**
