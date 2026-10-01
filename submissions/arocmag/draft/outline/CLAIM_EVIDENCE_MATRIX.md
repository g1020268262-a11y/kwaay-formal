# 主张—证据矩阵

本文件约束后续中文稿的正式研究主张。模型源文件和独立复核原始输出高于英文母稿中的概括性文字；任何超出本矩阵“允许的中文表述”的句子都应回到证据层重新审查。

## 1. 分类和共同假设

| 分类 | 含义 |
|---|---|
| `SOURCE_FACT` | K-Waay 原始论文直接写出的接口、算法或安全游戏事实。 |
| `MODEL_RESULT` | 当前 Tamarin 模型中已有 lemma 的机器结果。 |
| `DERIVED_RELATION` | 从当前模型规则和已验证 witness 作出的人工逻辑推导；不是新增 lemma。 |
| `DESIGN_IMPLICATION` | 在指定接口解释和信任边界下的条件性设计启示。 |
| `PROVENANCE_FACT` | 有关模型输入、工具、运行和留存证据的可核对事实。 |
| `UNSUPPORTED` | 当前证据不能支持，正文不得作为结论。 |

下文使用这些共同建模假设：

- `H1`：每次 `SendMessage` 产生 fresh model-local `sid` 和 `m`；中文叙述建议把该 `sid` 称为 `oid`，避免与原协议 transcript `sid` 混淆。
- `H2`：持久事实 `!Sent(A,sid,m)` 提供理想化的精确 origin 匹配并可复用。
- `H3`：Dolev–Yao 网络可交付、重放和组合公开 tuple；这不等于已证明真实 batch builder 可被攻击者控制。
- `H4`：每个被观察 batch 固定两个 slot，按 `ProcessSlot1/2` 顺序处理。
- `H5`：性质以同一 `(bid,rst)` 为作用域，直接终点是 `ReceiverAccept`。
- `H6`：模型没有签名、KEM、KDF、recipient/prekey/context binding、keys、`KEY/TEST`、consumer 或部署状态。

## 2. 索引矩阵

| ID | 类型 | 核心主张 | 主要证据 | 可写入正文 |
|---|---|---|---|---|
| C1 | `SOURCE_FACT` | K-Waay 明确要求一次 `BatchReceive` 的不同元素对应不同 party | K-Waay full version Sec. 5.1, p.21 | 是 |
| C2 | `SOURCE_FACT` | `BatchReceive` 按输入索引 `j` 处理并返回 `{k_j}_j`，安全游戏以 party/component 坐标选择接收结果 | K-Waay Fig. 10 与游戏定义 | 是，限接口动机 |
| C3 | `MODEL_RESULT` | 三模型中的每个 `ReceiverAccept` 都有先前精确匹配的 `Send` | 三模型 `receiver_accept_has_send` | 是，限理想 origin correspondence |
| C4 | `MODEL_RESULT` | R 中一个精确 sender origin 可支持同 context 两次接受 | R `one_send_two_accepts_exists` | 是 |
| C5 | `MODEL_RESULT` | R 的作用域内 exact-origin injectivity 被反例否定 | R `receiver_accept_injective` | 是 |
| C6 | `MODEL_RESULT` | M 中 accepted message distinction 与 scoped injectivity 都成立 | M 两条 safety lemma | 是，但不得算作两项独立发现 |
| C7 | `MODEL_RESULT` | M 中同一 party 的两条不同 message 可在同一 batch 中接受 | M `same_party_different_messages_batch_exists` | 是，核心 separation witness |
| C8 | `MODEL_RESULT` | P 中接受端 party distinction 成立 | P `accepted_batch_has_distinct_parties` | 是，明示正控制性质 |
| C9 | `MODEL_RESULT` | P 中有效的不同 party 批次仍可达 | P `distinct_party_batch_exists` | 是，non-vacuity |
| C10 | `MODEL_RESULT` | M/P 的 rejection branch 可达 | 两条 rejection existence lemma | 是，仅附带、弱表述 |
| C11 | `DERIVED_RELATION` | 当前规则下 `P_tau => M_tau <=> I_tau`，且 `M_tau !=> P_tau` | 规则推导 + C7 witness | 是，必须标注人工推导 |
| C12 | `DESIGN_IMPLICATION` | 需要 party-indexed batch 解释的接口应明确维护 participant relation | C1、C2、C7–C11 | 是，条件性表述 |
| C13 | `PROVENANCE_FACT` | 独立复核使 14/14 状态与步数得到重现 | reviewer rerun 原始证据 | 是 |
| U1 | `UNSUPPORTED` | 完整 K-Waay 被攻破、密钥泄露或 `KEY/TEST` 失效 | 无 | 否 |
| U2 | `UNSUPPORTED` | 已证明实际实现漏查、部署漏洞、misbinding、UKS 或完整身份绑定失败 | 无 | 否 |
| U3 | `UNSUPPORTED` | 已证明任意 batch 大小或 source-to-model refinement | 无 | 否 |

## 3. 逐项证据卡

### C1 — K-Waay原文的不同参与方条件

- **Claim**：K-Waay 原文明确假设，同一次 `BatchReceive(sk_i,st_i,S)` 调用中，`S` 的每个元素对应不同 party。
- **Evidence Source**：`reviews/2026-09-16-evidence/kwaay-full-2024-120.pdf`，Sec. 5.1、Fig. 10 后文字，PDF p.21；SHA-256 `476f28594806f15f4baab6ce7d3785143db0a013f21fbcf590ac1666161660a8`。
- **Tamarin Model / Corresponding Lemma / Verification Result**：不适用；这是协议来源事实。
- **Original K-Waay Support**：直接、明确。
- **Modeling Assumptions**：无；后续如何投影到模型受 H1–H6 约束。
- **Limitations**：原文条件存在，不等于说明具体 caller、builder 或 receiver 实现如何检查它。
- **Proposed Chinese Wording**：`K-Waay在BatchReceive定义中明确假定，同一次调用的不同输入元素对应不同参与方。本文不把该条件视为协议遗漏，而考察其在受控接纳抽象中所维持的参与方关系。`

### C2 — party-indexed接口动机

- **Claim**：K-Waay 的 `BatchReceive` 遍历 `(pk_j,prek_j,m_j)` 并形成 `k_j`，正常返回 `{k_j}_j`；安全游戏对 receiver session 的测试/查询使用 party/component 索引。
- **Evidence Source**：同一 K-Waay full version，Fig. 10 与相关游戏/证明文字；adversarial review M4 对接口依赖的审计。
- **Tamarin Model / Corresponding Lemma / Verification Result**：不适用。
- **Original K-Waay Support**：算法层直接支持 `{k_j}_j`；游戏中的 `TEST(i,s,j*)` 等给出 party/component 选择动机。
- **Modeling Assumptions**：中文稿仅用其解释 party coordinate 为何值得区分。
- **Limitations**：当前模型没有 `k_j`、output selection、`KEY/TEST` 或 game；不能据此声称 cryptographic necessity 或接口失效。
- **Proposed Chinese Wording**：`原算法按索引j处理输入并返回相应分量，这为批内party投影提供了协议特定动机；本文模型尚未覆盖这些密钥分量及其查询语义。`

### C3 — 模型内精确origin correspondence

- **Claim**：三个模型中每个 `ReceiverAccept(A,sid,m,bid,rst)` 都存在更早的精确匹配 `Send(A,sid,m)`。
- **Evidence Source**：三个 `.spthy` 文件；独立复核 stdout 与 `result-comparison.tsv`。
- **Tamarin Model**：R、M、P。
- **Corresponding Lemma**：`receiver_accept_has_send`。
- **Verification Result**：三次均 `verified`，各 8 steps，独立复核 `MATCH`。
- **Original K-Waay Support**：没有直接等价物；原协议通过密码运算和 session/game 定义建立更丰富关系。
- **Modeling Assumptions**：H1–H6，尤其 H2。
- **Limitations**：该结果主要由 processing rule 的 `!Sent` 前提保证；不是完整 authentication、agreement 或 recipient binding。
- **Proposed Chinese Wording**：`在三个接纳模型中，接受事件均具有先前的精确符号origin；这一结果只表达模型内对应关系，不等同于K-Waay的完整认证性质。`

### C4 — 宽松模型的精确origin重复接受witness

- **Claim**：在 R 中，一个匹配的 sender origin 可在同一 `(bid,rst)` 下支持两个不同时间点的接受事件。
- **Evidence Source**：`rqv2_relaxed.spthy`、独立 prove stdout、`rqv2_relaxed-traces.json`。
- **Tamarin Model**：`rqv2_relaxed`。
- **Corresponding Lemma**：`one_send_two_accepts_exists`。
- **Verification Result**：`verified`，13 steps，独立复核 `MATCH`；exported graph 存在且可能包含无关 Send。
- **Original K-Waay Support**：该执行违反 C1 的输入域，不能作为合规 K-Waay attack。
- **Modeling Assumptions**：H1–H6；两个 slot 可收集同一公开 tuple；`!Sent` 可复用。
- **Limitations**：只到两个 `ReceiverAccept`；无 key、state installation 或应用结果。
- **Proposed Chinese Wording**：`在取消坐标不等约束的固定两槽模型中，存在一个精确匹配的sender origin在同一batch context内支持两次ReceiverAccept的执行。`

### C5 — 宽松模型的scoped injectivity反例

- **Claim**：R 中“同一 exact origin 在同一 context 至多接受一次”的性质不成立。
- **Evidence Source**：同 C4。
- **Tamarin Model**：`rqv2_relaxed`。
- **Corresponding Lemma**：`receiver_accept_injective`。
- **Verification Result**：`falsified`，13 steps，独立复核 `MATCH` 并保留 counterexample graph。
- **Original K-Waay Support**：无；性质是本文的 batch-local diagnostic。
- **Modeling Assumptions**：H1–H6。
- **Limitations**：不是标准 AKE injective agreement，也不证明全局 replay-resistance 失败。
- **Proposed Chinese Wording**：`相应的batch-local exact-origin injectivity在宽松模型中被反例否定；该性质仅用于区分事件重复与参与方重复。`

### C6 — 消息级模型的两个safety结果

- **Claim**：M 中同一 context 的不同接受事件具有不同 `m`，且同一 exact origin 不会在该 context 被接受两次。
- **Evidence Source**：`rqv2_message_dedup.spthy` 与独立复核输出。
- **Tamarin Model**：`rqv2_message_dedup`。
- **Corresponding Lemma**：`accepted_batch_has_distinct_messages`；`receiver_accept_injective`。
- **Verification Result**：分别 `verified` 31 steps、`verified` 33 steps；均独立复核 `MATCH`。
- **Original K-Waay Support**：K-Waay 的目标 condition 比较 party，不是 message。
- **Modeling Assumptions**：H1–H6。
- **Limitations**：在当前 fresh-message 与 exact-origin 规则下二者满足 C11 的等价关系，不是两项独立研究发现；不表示跨 batch replay protection。
- **Proposed Chinese Wording**：`消息级模型验证了接受消息区分和当前作用域内的精确origin单次接受；在本模型规则下，这两个结论并非独立。`

### C7 — 同party/不同message的机器witness

- **Claim**：M 中存在同一 party 的两个不同 `sid/m` origin 在同一 batch 内各接受一次的执行。
- **Evidence Source**：`rqv2_message_dedup.spthy`、独立 prove stdout 与 `rqv2_message_dedup-traces.json`。
- **Tamarin Model**：`rqv2_message_dedup`。
- **Corresponding Lemma**：`same_party_different_messages_batch_exists`。
- **Verification Result**：`verified`，16 steps，独立复核 `MATCH`。
- **Original K-Waay Support**：该 composition 不满足 C1；用于分析替代谓词，不是原协议有效域攻击。
- **Modeling Assumptions**：H1–H6；同一 party 可执行多次 Send。
- **Limitations**：两个 entry 都有明确 origin；不证明 attribution ambiguity、wrong peer、misbinding 或 key confusion。
- **Proposed Chinese Wording**：`消息不等能够排除当前模型中的精确origin重复接受，但仍存在同一参与方产生两条不同消息并在同一批次中各被接受一次的执行，因此消息区分不蕴含批内参与方区分。`

### C8 — party-level safety

- **Claim**：P 中同一 context 的两个不同接受事件具有不同 party 坐标。
- **Evidence Source**：`rqv2_party_admission.spthy` 与独立复核输出。
- **Tamarin Model**：`rqv2_party_admission`。
- **Corresponding Lemma**：`accepted_batch_has_distinct_parties`。
- **Verification Result**：`verified`，31 steps，独立复核 `MATCH`。
- **Original K-Waay Support**：建模目标来自 C1，但模型实现不是原算法的 refinement。
- **Modeling Assumptions**：H1–H6；P 的 admission rule 直接产生 `Neq(A1,A2)` 并受 inequality restriction 约束。
- **Limitations**：这是公开 guard 在抽象生命周期中的保持，不是从密码学推导出的新条件，也不规定真实 enforcement placement。
- **Proposed Chinese Wording**：`在直接约束参与方坐标的模型中，接受端的批内参与方区分性质得到验证。该结果是接纳guard的正控制，而非对完整K-Waay的新安全定理。`

### C9 — party-level non-vacuity

- **Claim**：P 仍允许两个不同 party 的合法 origin 在同一 batch 中接受。
- **Evidence Source**：P 模型、独立 prove stdout 与 `rqv2_party_admission-traces.json`。
- **Tamarin Model**：`rqv2_party_admission`。
- **Corresponding Lemma**：`distinct_party_batch_exists`。
- **Verification Result**：`verified`，17 steps，独立复核 `MATCH`。
- **Original K-Waay Support**：与 C1 的允许输入形状一致，但不覆盖真实密码处理。
- **Modeling Assumptions**：H1–H6。
- **Limitations**：只证明至少一个有效执行；不证明所有合规输入都完成。
- **Proposed Chinese Wording**：`参与方级接纳并未使模型空真：至少一个由不同参与方origin组成并完成两次接受的批次仍然可达。`

### C10 — 两条弱rejection可达性

- **Claim**：M 和 P 的抽象 rejection branch 均可达。
- **Evidence Source**：M/P 模型、独立输出和两个 rejection graph。
- **Tamarin Model**：`rqv2_message_dedup`、`rqv2_party_admission`。
- **Corresponding Lemma**：`repeated_message_rejection_exists`；`same_party_rejection_exists`。
- **Verification Result**：分别 `verified` 4 steps、`verified` 5 steps，均 `MATCH`。
- **Original K-Waay Support**：无直接对应；这是模型设计的拒绝分支。
- **Modeling Assumptions**：H1–H6。
- **Limitations**：lemma 中的前置 Send 没有和 rejected pair 绑定；只能说 branch non-empty，不能说展示的 honest Sends 被拒，也不能推出 eventual rejection/liveness。
- **Proposed Chinese Wording**：`两种受限模型的拒绝分支均可达；现有存在性性质未把前置Send与被拒条目绑定，因此本文不据此主张特定合法输入被拒绝。`

### C11 — 当前规则下的P/M/I关系

- **Claim**：令 `P_tau`、`M_tau`、`I_tau` 分别表示同一 `(bid,rst)` 中接受事件的 party distinction、message distinction、exact-origin scoped injectivity，则当前规则下 `P_tau => M_tau <=> I_tau`，并且 `M_tau !=> P_tau`。
- **Evidence Source**：adversarial review M3 对共同规则的人工推导；C7 提供最后一个非蕴含的机器 witness。
- **Tamarin Model**：跨 R/M/P 的规则层关系。
- **Corresponding Lemma**：无单一对应 lemma；`M_tau !=> P_tau` 由 `same_party_different_messages_batch_exists` 见证。
- **Verification Result**：`DERIVED_RELATION`，不是新增 Tamarin result。
- **Original K-Waay Support**：无；关系依赖当前 abstraction。
- **Modeling Assumptions**：H1–H5，尤其 `m` 全局 fresh、每个接受需精确 `!Sent`、两槽顺序事件。
- **Limitations**：消息和 injectivity 在更忠实消息构造、不同 freshness 或不同事件定义下未必等价；不能推广为一般协议定理。
- **Proposed Chinese Wording**：`依据当前freshness和origin规则可人工推出 P_tau=>M_tau<=>I_tau；M模型的可达执行进一步给出M_tau不蕴含P_tau。该关系不是新增Tamarin引理。`

### C12 — 条件性设计启示

- **Claim**：当批处理接口的语义要求不同位置代表不同 party 时，负责构造或接纳批次的组件必须维护相应 participant relation，不能仅凭 message/origin/slot 的区分推定该关系。
- **Evidence Source**：C1、C2、C7–C11；英文 Section 6 的 invariant/enforcement 分析。
- **Tamarin Model / Corresponding Lemma / Verification Result**：由已有结果支持的解释，不是额外验证性质。
- **Original K-Waay Support**：原文给出 condition 和 party-indexed interface；没有规定本文列举的唯一 enforcement location。
- **Modeling Assumptions**：需要一个可论证的 concrete identity 到模型 party 坐标的映射。
- **Limitations**：caller、batch builder、receiver admission 都只是可能责任位置；本文未审计部署，也不提出必须新增某一具体 check。
- **Proposed Chinese Wording**：`对按参与方解释批内位置的接口，应显式规定由哪个组件、依据何种参与方归属维护批内关系；其他坐标上的不等约束只有在给出映射论证后才能作为替代。`

### C13 — 独立复核的可重复性事实

- **Claim**：2026-09-16 的独立 reviewer rerun 对三个未改模型完成 parse/prove，14/14 结果状态和 steps 与稿件记录一致，并保存 raw stdout/stderr、manifest、hash 和 7 个 JSON graphs。
- **Evidence Source**：`reviews/2026-09-16-evidence/README.md`、`independent-rerun-manifest.json`、`result-comparison.tsv`、`SHA256SUMS.txt` 及输出文件。
- **Tamarin Model**：R、M、P，输入 SHA-256 与记录相符。
- **Corresponding Lemma / Verification Result**：14 个实例，13 verified、1 falsified；全部 `MATCH`。
- **Original K-Waay Support**：不适用。
- **Modeling Assumptions**：reviewed commit `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57`，clean pre/post；Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu 24.04。
- **Limitations**：新证据不是历史运行日志恢复；复现抽象结果不证明协议连接、攻击有效性或发表新颖性。
- **Proposed Chinese Wording**：`独立复核在明确的代码版本和工具环境下重跑了三个未改模型，14个model–lemma实例的状态与步数均与原记录一致；该复核确认抽象结果可重复，但不补足source-to-model refinement。`

### U1–U3 — 禁止升级的主张

| Claim | Evidence Source | Tamarin Model | Corresponding Lemma | Verification Result | Original K-Waay Support | Modeling Assumptions | Limitations | Proposed Chinese Wording |
|---|---|---|---|---|---|---|---|---|
| 完整 K-Waay 被攻破、密钥泄露、`KEY/TEST` 失效 | 无 | 当前模型无 key/queries | 无 | `UNSUPPORTED` | 原论文的 different-party 条件排除所示 composition | H6 明确省略 | 不得作为结论、暗示或题名 | `本文不对完整K-Waay的密钥安全性或KEY/TEST接口作出结论。` |
| 实际实现漏查、部署漏洞、完整 identity binding 失败、misbinding/UKS | 无 | 无实现/peer-key relation | 无 | `UNSUPPORTED` | 无部署证据 | H3/H6 | 不得写成“攻击路径”“真实漏洞” | `本文未分析具体实现或部署，也未建模错误peer/identity到密钥的绑定。` |
| 任意 batch 大小性质、完整 source-to-model refinement | 无 | 仅固定两槽 | 无 | `UNSUPPORTED` | 原接口可处理一般集合，但模型没有一般化证明 | H4/H6 | 两槽只给最小违反对；抽象可多也可少允许真实行为 | `机器证据固定为两槽，且不存在从原协议到该抽象的精化定理。` |

## 4. 第一轮审稿问题的落地判断

| 问题 | 可由定位/表述处理 | 必须保留为局限 | 若要变成更强贡献所需的新研究 |
|---|---|---|---|
| M1 研究非平凡性 | 将论文定位为窄的 formal semantic case study；P 明示为正控制；14 条结果不拆成 14 项发现 | message-level substitute 的现实来源和研究增量仍弱，改写不能自动解决发表价值 | 找到独立结果谓词或真实实现/规范中的 message-level substitute，并验证其协议相关性 |
| M2 协议抽象差距 | 用 source-to-abstraction mapping 明示保留/省略项；所有结论加 `ReceiverAccept` 边界 | `!Sent` 缺 recipient/prekey/context，不能称保守 over-approximation 或协议反例 | 保留相关接收上下文与密码操作，建立 simulation/refinement 或可审计投影 |
| M3 M 与 I 依赖 | 明写 `P_tau=>M_tau<=>I_tau` 为人工推导，避免独立贡献计数 | 关系只在当前 freshness/origin 规则下成立 | 使用更忠实的 message/sid 构造后重新建模与验证 |
| M4 K-Waay-specific interface | 增加 `{k_j}_j`、party/component-indexed query 的接口动机 | 当前模型没有输出选择与 game，不能主张 cryptographic necessity | 形式化 slot-to-party-to-output 关系及扩展域语义，再定义相应安全目标 |
| M5 rejection witness | 将结论降为 rejection branch reachability，正文弱化 | 现有 lemma 不绑定被拒 tuple，不给 liveness | 增加 entry-bearing rejection event 或绑定输入的精确 witness 后重跑 |
| M6 authority 分叉 | 统一为“party relation 的 non-substitutability”；重复 party 表示投影非单射，不写 attribution ambiguous | 历史文档的强措辞不能借作当前证据 | 如需反向 party-to-slot 选择歧义，必须先建模该接口 |
| M7 provenance | 中文稿引用独立 rerun，列出 commit、工具、raw outputs 和 match | 这不是原运行日志的恢复，也不提升 protocol validity | 发布可由输出生成的结果表和完整证据包；必要时另做作者侧复现 |

