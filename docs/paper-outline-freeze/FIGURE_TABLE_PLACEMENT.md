# 四张核心图与四张核心表的规划冻结

## 0. 使用边界

本文件只冻结图表的学术目的、信息构成、证据来源和正文引用方式，不生成 TikZ、
PNG、SVG、流程图或其他图片。任何后续绘制都必须以这里列出的事件和 trace 为准，
不得为了视觉连贯把不同 theory 的执行拼成一条机器 trace。

## 1. 核心图规划

### 图1：K-Waay 核心发送与 BatchReceive 交互流程

- **放置位置**：§1.2，在介绍 `BatchReceive` 状态坐标和
  `DistinctPartyPerBatch` 之后。
- **学术目的**：建立全文共同的协议对象词汇，显示 Figure 7 core 的消息如何进入
  接收端批次生命周期，并把“单次 core”与“批次状态”两个模型层分开。
- **必须表现的实体**：发送方 `A`、接收方 `B`、公共网络、`BatchReceive`、slot 1/
  slot 2、共享 receiver state `rst`、batch id `bid`、slot index `idx`。
- **必须表现的信息**：
  - `m=<ct_l,ct_k,ct_s>`；
  - `sid=session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)`；
  - `k=KDF(K_l,K_k,K_s,sid)`；
  - core 的 send/receive 边界；
  - AddSlot→SealBatch→ProcessSlot→BatchComplete/BatchFail；
  - 同一 batch 内 `i != j => A_i != A_j` 的 specification-level 前置条件。
- **必须表现的事件**：ProVerif 一侧标 `SendDone/RecvDone`；Tamarin 一侧标
  `BatchCreated/SlotAdded/BatchSealed/ReceiverAccept/BatchComplete/BatchFail`。用视觉
  分区明确这些不是同一模型中的一条事件序列。
- **对应模型**：`proverif/kwaay_core_final.cpp.pv`；
  `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`；historical replay theory 的两槽
  lifecycle 只作为后续实例。
- **对应证据**：`logs/tamarin-v7/summary.txt` 中 executability、seal/process/order、
  close/state-consumption lemmas；本图不表示攻击 trace。
- **图前正文**：先解释 core message/sid/key，再定义 batch/state/slot 和参与方互异。
- **图后正文**：指出 ProVerif 负责 no-batch core，Tamarin 负责状态化批次；这张图
  是跨层协议映射，不是 source-to-model refinement theorem。
- **不得表现**：M2 installation、RQ-v2 output-key 概念、任意长度已证明、部署组件。

### 图2：原始消息重组攻击与 HMAC 确认对照

- **放置位置**：跨 §3.2–§3.3；建议在 §3.3 HMAC 机制定义后放置，使左右两部分
  都已有正文铺垫。
- **学术目的**：解释为什么原始模型可以“secrecy true 但 correspondence false”，
  以及 HMAC gate 为什么阻断同类完整参数不匹配完成。
- **左侧必须表现的实体/信息**：诚实发送方、网络攻击者、接收方；诚实 `ct_s`；
  攻击者基于公开接收方材料构造的新 `ct_l'`、`ct_k'`；重组消息 `m'`；接收方的
  `sid'`、`k'`、`RecvDone(B,A,sid',k')`；不存在相同参数的 `SendDone`。
- **右侧必须表现的实体/信息**：sender 计算
  `tag=hmac(confirm_key(k),sid)`；receiver 用本地 `kRecv/sidBA` 检查 tag 后才允许
  `ReceiverKey/RecvDone`；重组后的不同 `k'/sid'` 无匹配 tag。
- **必须显式标注**：左侧 baseline 的 receiver secrecy query 为 `true`；该图不是
  attacker key recovery。右侧结论限于 `HMAC_BASELINE` 无泄露目标。
- **对应模型**：原始与 HMAC variant 两个 ProVerif 模型。
- **对应 stdout**：`logs/final/proverif/out/BASELINE.out`；
  `logs/variants/hmac-confirmation/proverif/out/HMAC_BASELINE.out`。
- **对应结果**：原始 P1 `false`，两项 secrecy `true`；HMAC baseline P1 与两项
  secrecy均 `true`；`HMAC_LEAK_SIGSK_A` 作为图注边界而非主流程。
- **图前正文**：先报告表2并解释 component origin 不等于完整 correspondence。
- **图后正文**：说明 HMAC 修复 P1，但 tag 不含 `bid/idx/rst`，由此自然转入 §4
  的批内 occurrence 问题。
- **不得表现**：把 HMAC-only Tamarin replay 直接画在本图右侧作为 ProVerif
  counterexample continuation；它是后续独立模型。

### 图3：批内重复接受及 C_install-v2 条件化影响

- **放置位置**：§4.3，在 C1–C8 和 `sid/aid/h` 定义之后。
- **学术目的**：同时展示下层 duplicate accept 的事件投影和独立 impact theory
  中的条件化消费，但通过明显的“模型接口/条件化扩展”分隔线避免伪造联合 trace。
- **上半部分实体/事件**：一个 `ConfirmedSend(A,B,m,sid,k,tag)`；公共 confirmed
  message `<m,tag>`；同一 `B,bid,rst` 的两个不同 `idx`；两个
  `ConfirmedReceiverAccept`；`BatchComplete`。
- **上半部分信息**：matching coordinates 相同、accept timepoint/slot 不同、无
  compromise、无 HMAC forgery。对应 M1 HMAC-only trace。
- **下半部分实体/事件**：两个 `ReceiverAccept`；两个 fresh
  `AcceptOutputCreated(aid1/aid2,...)`；`BatchComplete`；两个
  `InstallFromAccept`；两个 `InstallSession(B,h1/h2,A,sid,k)`；
  `ConsumerComplete`。
- **下半部分信息**：`h1 != h2`，但 `A,B,sid,k` 相同；明确标注“仅在
  `C_install-v2`，尤其 C7 下”。对应 M2 impact theory。
- **对应模型/trace**：
  - 上半：`tamarin/replay/kwaay_replay_hmac_only.spthy` 与
    `logs/tamarin-replay-hmac-only/attack-trace.*`；
  - 下半：`tamarin/impact/kwaay_impact_original.spthy` 与
    `logs/tamarin-impact-original/attack-trace.*`、`unique-install-trace.*`。
- **图前正文**：先分别给 HMAC-only result 和 `C_install-v2` 定义；声明图由两个
  已验证模型的“相邻证据层”组成，不是一条单模型 trace。
- **图后正文**：解释 duplicate accepted output 到 installation 的推论是条件化的；
  不使用“真实会话克隆”措辞。
- **不得表现**：把 `ConfirmedReceiverAccept` 无说明地直接重命名为 M2 的
  `ReceiverAccept`；不得加入 Double Ratchet、数据库或 deployed session。

### 图4：批内原子消息去重及组合加固流程

- **放置位置**：§5.1，在修复 scope/identity/decision point 三项定义之后。
- **学术目的**：说明为什么去重必须在 processing 前作一次原子决定，并展示 HMAC
  与 dedup 的互补放置位置。
- **必须表现的状态/事件**：AddSlot1/2→SealBatch→`DedupPending`+
  `DedupDecisionToken`；duplicate 分支→`DuplicateDetected`→`BatchFail`/
  `BatchClosed`/state consumption；distinct 分支→`DedupPassed`→CheckedSlot1/2→
  HMAC validation→accept→BatchComplete。
- **必须表现的 identity**：比较 exact base message `m`，而不是 `<m,tag>`、tag、
  `sid` 或 party。same base/different tag 仍进入 duplicate branch。
- **必须表现的边界**：duplicate 分支无 accept/output/install；distinct valid
  confirmed messages 可完成 batch/consumer；slot2 HMAC mismatch 可发生在 slot1
  accept 后，所以并非所有失败 batch 都无 partial lower-layer output。
- **对应模型**：M3 fixed replay/impact 与 M4 combined replay/impact。
- **对应 trace**：M3 `duplicate-fail`、`distinct-complete`、`distinct-consumer`；M4
  `duplicate`、`normal-replay`、`normal-consumer`、`slot1-mismatch`、
  `slot2-mismatch`。
- **对应结果**：M3 two-accept/two-install witness falsified，normal distinct paths
  verified；M4 confirmed two-accept/two-install witness falsified，same-base/different-
  tag failure与 normal distinct confirmed paths verified。
- **图前正文**：先说明原子决定点和 exact base-message identity。
- **图后正文**：以表4给出完整机器对照，再在 §6 说明该修复仍不等于 party
  admission。
- **不得表现**：全局 replay cache、跨 batch 共享 seen set、rollback/restart
  恢复、任意长度结论。

## 2. 核心表规划

### 表1：安全性质、定义及对应模型

- **放置位置**：§2.4。
- **学术目的**：让读者先理解性质语义、证据类型与模型边界，再阅读结果。
- **列名**：
  1. `性质层/名称`；
  2. `形式化定义或事件关系`；
  3. `保护的 identity/对象`；
  4. `证据类型`；
  5. `主模型/工具`；
  6. `攻击者与范围`；
  7. `本论文中的作用`；
  8. `不得推出的结论`。
- **行内容**：
  - P0-S：`not(attacker(k) && SenderKey/ReceiverKey)`；session key；ProVerif F+；
    不推出 agreement。
  - P0-O：`SplitKemAccepted ==> SenderSplitKemComponent`；split-KEM component；
    ProVerif F+；不推出完整消息来源。
  - P1：`RecvDone(B,A,sid,k) ==> SendDone(A,B,sid,k)`；完整参数；ProVerif；
    原始 F−/HMAC F+；non-injective，非 replay uniqueness。
  - P2-source：`ReceiverAccept ==> earlier SenderSession`；matching existence/order；
    Tamarin F+；不等于 occurrence injectivity。
  - P2-injective：same batch/state/message 的两个 accept 必须同一 occurrence；
    Tamarin original/HMAC-only F−，M3/M4 F+。
  - P3：completed consumer 内同一 source/session 的 installation uniqueness；
    Tamarin C；M2 F−，M3/M4 F+；不等于 deployed behavior。
  - `DistinctPartyPerBatch`：`i!=j => A_i!=A_j`；party identity；RQ-v2 P-semantics
    F+/W+；不由 message dedup/HMAC 推出。
- **证据来源**：两个 ProVerif summaries、replay/impact aggregates、RQ-v2 result
  comparison、`artifact/manifest/property-semantics.tsv`。
- **阅读价值**：避免把 lemma 清单当贡献，直接展示每层保护什么、没保护什么。

### 表2：原始 ProVerif 与 HMAC 修复结果

- **放置位置**：§3.4；§3.1 可先预告表中 original 行。
- **学术目的**：证明 HMAC 修复 P1 时没有牺牲 baseline secrecy/component origin，
  同时暴露 compromise 边界。
- **列名**：
  1. `验证目标`；
  2. `安全含义`；
  3. `Original BASELINE/COMPONENT`；
  4. `HMAC_BASELINE/HMAC_COMPONENT`；
  5. `HMAC_LEAK_SIGSK_A`；
  6. `非空性/反例说明`；
  7. `证据文件`；
  8. `允许结论`。
- **行内容**：
  - HonestRun：original 与 HMAC baseline reachable；泄露 target 亦 reachable；防止
    正面结果真空。
  - P1 `RecvDone ==> SendDone`：false / true / false；主修复对照。
  - sender secrecy：true / true / true。
  - receiver secrecy：true / true / false。
  - sender prekey correspondence：true / true / true。
  - receiver local prekey correspondence：true / true / true。
  - component origin：true / true / 未在该泄露 target 中单列；不可误填。
  - trace interpretation：original 为 `ct_s` 复用+`ct_l/ct_k` 重组；HMAC baseline
    阻断完整参数不匹配；泄露 target 显示正面结论不是无条件 compromise theorem。
- **证据来源**：`logs/final/proverif/summary.txt`、`out/BASELINE.out`；HMAC summary
  与三个 out 文件。
- **阅读价值**：读者能同时看到“修复了什么”“保持了什么”“在哪个已测试泄露
  条件下失效”，而非只看到 query 名称。

### 表3：批内重复接受与条件化安全影响

- **放置位置**：§4.3，紧邻图3。
- **学术目的**：把下层 occurrence 结果与上层条件化 impact 分栏，阻止
  `ReceiverAccept == InstallSession` 的错误推断。
- **列名**：
  1. `证据层`；
  2. `模型条件`；
  3. `关键事件链`；
  4. `正向见证`；
  5. `被否定的安全性质`；
  6. `正常路径/支撑性质`；
  7. `安全含义`；
  8. `禁止外推`；
  9. `原始证据`。
- **行内容**：
  - original replay：relaxed two-slot、same `B,bid,rst,m,sid,k`；one send→two
    accepts W+；at-most-once/injectivity F−；normal complete W+；duplicate successful
    output，不是 key leak。
  - HMAC-only replay：same confirmed message；17-step witness W+；两个 15-step
    properties F−；matching/send uniqueness/normal complete F+/W+；有效消息重放，
    不是 HMAC forgery。
  - M2 impact：`C_install-v2`；one send→two accepts→two aids→two handles/installs；
    28-step witness W+；28-step unique install F−；normal consumer W+；conditional
    local-handle duplication，不是 real session cloning。
  - lower-layer regression row：18/18 formula/result MATCH；只说明选定 lower layer
    保持，不是 trace equivalence。
- **证据来源**：E-R0、E-RH、E-I0 的 aggregate/proof/trace。
- **阅读价值**：通过“模型条件”和“禁止外推”两列把攻击可达性与影响强度分离。

### 表4：去重及组合加固前后的验证对照

- **放置位置**：§5.4；§6.2 复用其中“party-level 边界”分区。
- **学术目的**：以问题而非 lemma 数量为行，展示 original/HMAC-only/M3/M4 和
  RQ-v2 boundary 的差异。
- **列名**：
  1. `研究问题/判定标准`；
  2. `Original`；
  3. `HMAC-only`；
  4. `M3 dedup-only`；
  5. `M4 HMAC+dedup`；
  6. `RQ-v2 party-boundary`；
  7. `正常/失败路径证据`；
  8. `解释`；
  9. `证据来源`。
- **主行内容**：
  - P1 full-parameter correspondence：original false；HMAC baseline true；M3 不负责；
    M4 从既有 ProVerif 证据继承，不是 M4 rerun；RQ-v2 不建模。
  - same exact message two accepts：original W+；HMAC-only W+；M3 W−且 safety F+；
    M4 W−且 confirmed/base safety F+；RQ-v2 R 模型 W+。
  - same-base/different-tag：仅 M4 有专门 rejection witness W+；其余 N/A。
  - duplicate accepted output/install：M2 conditional W+/unique F−；M3/M4 conditional
    witness W−、no output/install 与 unique F+。
  - normal distinct batch：M3/M4 W+；不得只呈现攻击被阻断。
  - normal distinct consumer：M3/M4 C/W+。
  - duplicate failure：M3/M4 W+，且 duplicate branch 无 accept/output/install。
  - HMAC mismatch failure：M4 slot1 和 slot2 paths W+；slot2 可在 slot1 accept 后失败，
    故不能声称所有 failed batch 无 partial lower-layer output。
  - same-party/different-message：M-semantics W+，说明 exact-message dedup 不等于
    party uniqueness。
  - party-level restoration：P-semantics same-party rejection、distinct-party normal
    batch与 admitted-party distinctness均 verified；HMAC/M3/M4 不替代该约束。
- **汇总脚注**：M3 为 196-target transparent composite；M4 为 Tamarin-only
  296-target transparent composite；两者都不能写成单次 source run 全终态。RQ-v2
  14 项结果计数不得并入 M4 296 项。
- **证据来源**：E-M3、E-M4、E-RQ；P1 单元格来自 E-PV-O/E-PV-H。
- **阅读价值**：读者可沿“问题—修复—正常性—剩余边界”阅读，而不是在孤立
  lemma 名称和步数间推断安全含义。

## 3. 正文引用约定

1. 每张图首次出现前先给出模型范围，图后再解释允许结论。
2. 表中 `verified` 必须区分 F+ 与 W+；`falsified` 必须说明是 found trace 还是
   no trace found 的 exists-trace。
3. 图3的两个证据层必须使用分隔线和“conditional composition”标识。
4. 表4中不可比较的格子写 `N/A（该模型不建模此性质）`，不得写“安全”。
5. 图表标题中使用“符号模型”“固定两槽”“条件化”中的必要限定词。
