# AROCMAG 中文 LaTeX 术语映射

本表以 `manuscript/` 英文 LaTeX 母稿和现有 Tamarin 模型的对象为准。旧中文稿只用于检查已有译法，没有作为段落或章节来源。

| 英文或源记号 | 中文稿用法 | 约束与说明 |
| --- | --- | --- |
| party / protocol principal | 参与方；需要强调抽象层次时写“建模协议主体” | 不等同于账户、公钥编码、预密钥或实现对象。 |
| `BatchReceive` | `BatchReceive` | 协议接口名保留英文和等宽体，不译成新的算法名。 |
| `Send` | `Send` | 协议接口或模型事件名保留英文。 |
| batch admission | 批处理接纳 | 本文的分析术语，不表示 K-Waay 规范另有独立算法。 |
| distinct-party condition | 不同参与方条件 | 明确为 K-Waay 原协议已经陈述的条件。 |
| `DistinctPartyPerBatch` | 批内参与方区分目标；公式和首次命名处保留 `DistinctPartyPerBatch` | 这是本文引入的分析性名称，不是声称源协议遗漏了条件。 |
| message `m` | 消息坐标 `m` | 消息不等不能推出参与方不等。 |
| occurrence / sender occurrence | 发送实例；必要时写“发送发生” | 表示分析中的一次发送方会话或出现，不赋予超出模型的会话语义。 |
| source-model `sid` | `oid` | 中文叙述统一采用 `oid ≡ sid_model`。英文母稿和 Tamarin 源模型仍使用 `sid`，此映射只为避免与 K-Waay transcript `sid` 混淆，不是模型修改。 |
| K-Waay transcript `sid` | transcript `sid` | 仅在解释冲突来源时使用；不改名为 `oid`。 |
| slot `i` | 槽位 `i` | 槽位不同不蕴含参与方或消息不同。 |
| batch `B` | 批次 `B` | 表示一次成组的接收方执行，不施加跨批次全局唯一性。 |
| receiver state / context | 接收方状态／接收方上下文 | 模型事件作用域使用 `(bid,rst)`；该坐标不能确定批内参与方数量。 |
| exact modeled origin | 精确建模来源／精确来源 | 按完整 `(A,oid,m)` 元组匹配，不按 `A` 单独匹配。 |
| `ReceiverAccept` | `ReceiverAccept` 接收事件 | 保留事件名，并明确它是批处理接纳抽象中的模型局部事件。 |
| batch-composition adversary | 批次组合对手 | 一项符号分析能力假设，不等于真实部署的 batch builder 已被网络攻击者控制。 |
| positive control | 正控制 | 指参与方级限制直接维护目标关系，不形成第四个研究问题。 |
| relaxed admission | 宽松接纳 | 首次出现写完整名称；内部宏 `R` 仅供后续章节需要时使用。 |
| message-level restriction | 消息级限制 | 约束消息坐标，不作为参与方关系的同义词。 |
| party-level restriction | 参与方级限制 | 直接约束参与方坐标；不主张这是唯一实现机制。 |
| split-KEM | split-KEM | 技术名称保留英文。 |
| refinement theorem | 精化定理 | 当前工作没有从完整 K-Waay 执行到模型的精化定理。 |

## 一致性规则

1. 除解释记号映射的首次出现外，中文正文的发送实例坐标统一写作 `oid`。
2. `party`、`message`、`occurrence`、`slot`、`batch` 和 receiver context 不合并为笼统的“身份唯一性”。
3. `ReceiverAccept` 不简写成协议级“认证成功”或完整会话“接受”。
4. 对手的批次组合能力只描述模型边界；没有实现证据时，不写成真实攻击者已控制批次构造器。
5. 现阶段没有阻塞后续翻译的待定术语。作者若希望全稿统一偏好，可在“参与方／协议主体”和“批处理接纳／批次接纳”之间作编辑性选择；本稿采用前一组。
