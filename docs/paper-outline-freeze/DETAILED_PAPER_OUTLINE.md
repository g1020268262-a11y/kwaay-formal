# 《K-Waay 接收端安全边界的形式化分析与组合加固》详细大纲冻结稿

## 0. 冻结说明

- 研究恢复基线与本文件编制时的仓库 `HEAD`：`112667a69c95dae4e9abc5781a6ddb8df6a10fdd`。
- 目标期刊：《计算机应用研究》。
- 本大纲只组织仓库中已经完成的 M0–M5 与 RQ-v2 研究，不新增模型、性质或实验。
- 证据标签：`[已证明]` 表示保存的机器结果为 `true/verified`；`[已证伪/见证可达]` 表示全称性质被反例否定或存在性见证被验证；`[条件化证明]` 表示结论依赖显式 `C_install-v2`；`[协议解释]` 表示由协议/模型语义进行的解释；`[设计建议]` 不属于机器证明。
- ProVerif 与 Tamarin 的事件词汇和抽象层次保持分离；不得把两个模型中的攻击拼接成一条未经验证的执行。
- 下列每节的“证据”项只列写作时必须直接核对的核心证据；完整逐节索引见 `SECTION_EVIDENCE_MAPPING.md`。

## 0 引言

1. **研究目的**：提出接收端的两层问题：完整参数对应关系是否成立，以及合法消息在同一批次中是否至多接受一次；说明第二问不是第一问的同义改写。
2. **核心论点**：K-Waay 的 symbolic key secrecy、完整转录本对应关系、批内 occurrence injectivity 和上层安装唯一性是不同性质；本文按“core 缺口—HMAC—批内重复接受—条件化影响—dedup—组合验证—party-level 边界”展开。
3. **机制/定义**：简要定义 `m=<ct_l,ct_k,ct_s>`、`sid`、`k=KDF(K_l,K_k,K_s,sid)`、`BatchReceive`、P0-S/P0-O/P1/P2/P3、`DistinctPartyPerBatch`。
4. **必须展示的过程**：用一段因果链概述原始 ProVerif 反例、HMAC 无泄露基线修复、HMAC-only 双重接受、`C_install-v2` 条件化双安装、M3/M4 修复；不在引言展开 trace 细节。
5. **真实源码路径**：`proverif/kwaay_core_final.cpp.pv`；`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`；`tamarin/replay/`；`tamarin/impact/`；`tamarin/rq-v2-minimal/`。
6. **query/lemma 与结果**：提要式列出 `RecvDone ==> SendDone`（原始 `false`，HMAC baseline `true`）、`one_confirmed_send_two_accepts_exists`（verified）、`one_send_two_accepts_two_installs_exists`（verified，条件化）、修复模型中对应攻击见证（falsified），以及 `same_party_different_messages_batch_exists`（verified）。
7. **stdout/trace/证明日志**：`logs/final/proverif/summary.txt`；`logs/variants/hmac-confirmation/proverif/summary.txt`；`logs/tamarin-replay-hmac-only/attack-trace.out`；`logs/tamarin-impact-original/attack-trace.out`；`logs/tamarin-m3-closeout/composite-result-vector.tsv`；`logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv`；`reviews/2026-09-16-evidence/result-comparison.tsv`。
8. **衔接**：从研究动机过渡到 §1 的协议对象；末段给出四项贡献并预告 §6 的适用边界。
9. **图/表/公式**：不放独立核心图；引用表1概括性质分层。可使用一条不编号的总路线公式，但不得将它画成跨模型攻击 trace。
10. **保留/合并/补充材料**：正文必须保留两问题分层、工具分工、四项贡献和三类边界；版本、哈希、完整结果计数移至 Artifact/附录。引言不得宣称 deployed exploit、计算安全或完整协议安全。

## 1 K-Waay 协议及安全问题

### 1.1 K-Waay 核心密钥交换流程

1. **研究目的**：给出理解 ProVerif 对应关系反例和 HMAC 修复所需的最小 Figure 7 core。
2. **核心论点**：接收端分别处理长时 KEM、临时 KEM 与 split-KEM 分量，并把三份共享秘密及转录本 `sid` 输入 KDF；分量合法或密钥保密不自动推出完整元组匹配。
3. **机制/定义**：`m=<ct_l,ct_k,ct_s>`；`sid=session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)`；`k=KDF(K_l,K_k,K_s,sid)`；`SendDone/RecvDone`、`SenderKey/ReceiverKey`、`SplitKemAccepted/SenderSplitKemComponent`。
4. **必须展示的过程**：诚实发送与接收计算的参数对齐；暂不展示攻击，只指出攻击者可控制公共网络并重新组合公开可构造分量。
5. **真实源码路径**：`proverif/kwaay_core_final.cpp.pv`（事件、query、发送/接收过程）；`docs/model-mapping.md`（协议对象到模型对象映射）。
6. **query/lemma 与结果**：本节只预告 baseline 中 sender/receiver secrecy 为 `true`、component-origin 为 `true`；详细结果留到 §3.1。
7. **stdout/trace/证明日志**：`logs/final/proverif/summary.txt`；正文不引用攻击 trace 细节，以免提前泄露 §3.2 的论证。
8. **衔接**：承接引言的 core 问题；下一节从单次接收转向 `BatchReceive` 的共享状态和批次生命周期。
9. **图/表/公式**：保留三分量消息、`sid`、KDF 三个公式；图1中显示 core send 到批量接收入口的关系。
10. **保留/合并/补充材料**：必须保留完整 `sid` 绑定与三个密文分量；具体 ProVerif 构造子/reduction 可移附录。内容充足，不建议合并。

### 1.2 BatchReceive 批量接收机制

1. **研究目的**：说明批次、槽位、共享 receiver state、seal/process/complete/fail 的状态语义，以及原协议的参与方互异前置条件。
2. **核心论点**：批量接收不是多个无关单次接收的简单集合；同一批次内槽位共享 `B,bid,rst`，因此准入、处理次序和终止状态会影响 occurrence-level 安全。
3. **机制/定义**：`ReceiverState(B,rst)`、`bid`、`idx`、Add/Seal/Process/Complete/Fail；`DistinctPartyPerBatch: i != j => A_i != A_j`。说明一般定义与固定槽位模型的区别。
4. **必须展示的过程**：展示正常的 AddSlot→SealBatch→ProcessSlot→BatchComplete，以及失败路径消耗终止 token；不在本节展示重复接受反例。
5. **真实源码路径**：`tamarin/kwaay_splitkem_batch_dynamic_v6.spthy`；`tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`；`docs/rq-v2/g2-admission-semantics.md`。
6. **query/lemma 与结果**：V7 的 `executable_four_slots_added`、`executable_seal_batch`、`executable_four_slots_processed`、`executable_batch_complete`、`executable_batch_fail`、`no_slot_accept_after_close`、`receiver_state_single_batch_end` 均 VERIFIED。
7. **stdout/trace/证明日志**：`logs/tamarin-v7/summary.txt`；结果解释见 `docs/tamarin/tamarin-v7-results.md`。
8. **衔接**：从 §1.1 的单次 core 扩展到批处理；下一节把两种接收问题和论文研究范围并列冻结。
9. **图/表/公式**：图1置于本节；公式给出 `DistinctPartyPerBatch`。表1在 §2.4 统一呈现，不在此重复结果表。
10. **保留/合并/补充材料**：正文保留状态机主干、共享坐标和参与方互异；V6/V7 全部 lemma 清单、四槽实现细节移附录。内容充足，不建议合并。

### 1.3 接收端安全问题与研究范围

1. **研究目的**：把 full-parameter correspondence 与 same-batch occurrence injectivity 明确拆成两个研究问题，并限定两者的逻辑关系。
2. **核心论点**：HMAC 可修复 P1，但不能自动给出 P2；重复接受只有经 `C_install-v2` 才能推出条件化 P3；exact-message dedup 也不能替代 party-level admission。
3. **机制/定义**：P0-S、P0-O、P1、P2、P3 under `C_install-v2`；“same message”“same sender occurrence”“same party”三种 identity coordinate。
4. **必须展示的过程**：给出性质依赖图的文字版：secrecy/component origin ≠ correspondence ≠ occurrence injectivity ≠ installation uniqueness；另列 party uniqueness 为正交准入约束。
5. **真实源码路径**：`docs/claim-hierarchy.md`；`docs/model-mapping.md`；`artifact/manifest/property-semantics.tsv`；`docs/rq-v2/rq-v2-complete-argument-map.md`。
6. **query/lemma 与结果**：本节不新增结果；引用后文的代表性 query/lemma 作为性质定义锚点。
7. **stdout/trace/证明日志**：以 `artifact/results/claim-matrix.tsv`、`artifact/results/claim-evidence.tsv` 为索引；具体 stdout 留在 §3–§6。
8. **衔接**：总结 §1 的协议背景；引向 §2 的攻击者、模型与性质定义。
9. **图/表/公式**：建议一组编号公式定义 P1/P2/P3；不增加核心图。表1承担性质—事件—模型—证据映射。
10. **保留/合并/补充材料**：必须保留研究范围和禁止推断；M0 的历史提交细节移 Artifact。内容不能与 §2.4 完全合并：本节回答“研究什么”，§2.4 回答“怎样形式化并分工具”。

## 2 形式化建模与安全性质

### 2.1 攻击者模型与研究假设

1. **研究目的**：冻结不同模型中的攻击能力、妥协边界和抽象假设。
2. **核心论点**：Dolev–Yao 攻击者可控制公共网络、保存/重放公开消息、重组可公开生成的 `ct_l/ct_k`；批次模型中的 symbolic batch-composition adversary 是分析边界，不等同于 deployed 网络攻击者控制真实 batch builder。
3. **机制/定义**：no-compromise baseline；HMAC 的 private `confirm_key(k)` 抽象；Tamarin 的 `HonestSession`；固定两槽 `B,bid,rst`；`C_install-v2` C1–C8；RQ-v2 的 party coordinate `A`。
4. **必须展示的过程**：分别列出 core 重组、同批重放、条件化消费所需能力；明确均不需要在相应 baseline witness 中发生 sender/receiver state compromise。
5. **真实源码路径**：两个 ProVerif 模型；`tamarin/replay/*.spthy`；`tamarin/impact/*.spthy`；`docs/rq-v2/rq-v2-threat-model.md`。
6. **query/lemma 与结果**：baseline secrecy queries `true`；HMAC-only 与 original replay 的见证排除 compromise；M2 witness 排除 compromise。不能把这些结果推广为完整 compromise theorem。
7. **stdout/trace/证明日志**：`logs/final/proverif/summary.txt`；`logs/tamarin-replay-hmac-only/attack-trace.out`；`logs/tamarin-impact-original/attack-trace.out`。
8. **衔接**：承接 §1.3 的范围；下一节进入 ProVerif 的事件和查询建模。
9. **图/表/公式**：表1中设置“攻击者/妥协边界”列；无需独立图。
10. **保留/合并/补充材料**：正文必须保留 batch-composition adversary 与部署攻击者的区别；全部 compromise target 矩阵可移附录。不得将 `HMAC_LEAK_SIGSK_A` 单项结果概括为所有泄露场景。

### 2.2 ProVerif 核心模型

1. **研究目的**：解释为什么 ProVerif 适合分析 Figure 7 core 的 secrecy、component origin 和 non-injective correspondence。
2. **核心论点**：该模型是 no-batch/single-receive abstraction；它对完整消息与 `sid/k` 参数建模，但不承担 `BatchReceive` slot/lifecycle 证明。
3. **机制/定义**：free constructors/reductions、public channel、签名检查、KEM/shared-secret 抽象、事件插桩；原始模型与 HMAC variant 的唯一关键差别是 tag 生成/验证门。
4. **必须展示的过程**：原始 receiver 在 `RecvDone` 前的检查链；HMAC variant 在 `ReceiverKey/RecvDone` 前匹配 `hmac(confirm_key(kRecv),sidBA)`。
5. **真实源码路径**：`proverif/kwaay_core_final.cpp.pv`；`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`。
6. **query/lemma 与结果**：定义 `HonestRun` reachability、两项 secrecy、`RecvDone ==> SendDone`、两项 prekey correspondence、component-origin query；结果集中在 §3。
7. **stdout/trace/证明日志**：`logs/final/proverif/out/BASELINE.out`；`logs/final/proverif/out/COMPONENT.out`；HMAC 对应输出目录。
8. **衔接**：从攻击者假设进入 core 建模；下一节说明为什么状态化批处理需要 Tamarin。
9. **图/表/公式**：可用一个事件—query 公式块；不单独成图。表1列出查询语义。
10. **保留/合并/补充材料**：正文保留模型边界和关键事件；所有 C-preprocessor target、泄露宏和构造子定义移附录/Artifact。

### 2.3 Tamarin 批次处理模型

1. **研究目的**：说明 Tamarin 如何表达线性状态、slot occurrence、批次终止、去重决定与条件化消费。
2. **核心论点**：Tamarin 模型分层复用生命周期语义，但 original/HMAC-only/fixed/combined/impact/RQ-v2 是不同 theory，不能因事件名字近似而合并为一个大模型。
3. **机制/定义**：线性 `ReceiverState`、stage/token、persistent source fact、`ReceiverAccept`/`ConfirmedReceiverAccept`、`aid`、`h`、`ConsumerComplete`、R/M/P admission semantics。
4. **必须展示的过程**：V7 生命周期主干；historical fixed-two-slot replay；impact consumer；RQ-v2 two-slot admission。明确 fixed four-slot lifecycle 与 fixed two-slot replay/RQ-v2 各自范围。
5. **真实源码路径**：`tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`；`tamarin/replay/`；`tamarin/impact/`；`tamarin/rq-v2-minimal/`。
6. **query/lemma 与结果**：V7 24 项 selected lemma 均 VERIFIED；其余结果按 §4–§6 分层报告。
7. **stdout/trace/证明日志**：`logs/tamarin-v7/summary.txt`；各 replay/impact evidence 目录；`reviews/2026-09-16-evidence/`。
8. **衔接**：解释工具选择；下一节统一给出性质公式和 ProVerif/Tamarin 的职责边界。
9. **图/表/公式**：图1引用生命周期；表1给出事件签名与模型。无需新增模型架构图。
10. **保留/合并/补充材料**：正文必须保留事件词汇分离和槽位边界；rule 全文、完整 lemma inventory 移 Artifact。不得把 RQ-v2 `ReceiverAccept(A,sid,m,bid,rst)` 当成历史 replay 的同一事件签名。

### 2.4 安全性质定义与工具分工

1. **研究目的**：给出可直接引用的性质公式、证据类型和工具分工。
2. **核心论点**：P0–P3 不是强弱线性阶梯；existence witness、all-traces proof、falsified property、conditional composition 分别回答不同问题。
3. **机制/定义**：P1 为 non-injective correspondence；P2 为同一 `(B,bid,rst)` 内 exact-message acceptance at-most-once/injectivity；P3 为 completed consumer 内安装唯一性；另定义 party-level invariant。
4. **必须展示的过程**：用公式并列 `RecvDone ==> SendDone`、`same_message_accepted_at_most_once`、`unique_install_within_completed_consumer`、`accepted_batch_has_distinct_parties`。
5. **真实源码路径**：`docs/claim-hierarchy.md`；`artifact/manifest/property-semantics.tsv`；各 query/lemma 所在模型。
6. **query/lemma 与结果**：表1逐项给出实际状态，并标识“verified exists-trace”不等于普遍安全、“falsified attack witness”不等于工具失败。
7. **stdout/trace/证明日志**：`artifact/results/actual-results.tsv`；`artifact/results/raw-to-summary.tsv`；核心结果回链至各原始输出。
8. **衔接**：完成方法章节；下一节首先回答 ProVerif core 的 P0/P1 结果。
9. **图/表/公式**：表1放在本节；保留 4 组性质公式。无需图。
10. **保留/合并/补充材料**：必须保留存在性/全称性质解释与条件化标签；405 行完整结果表移 Artifact。内容不能并入 §2.2/§2.3，否则性质定义会被工具细节割裂。

## 3 接收方对应关系缺口及 HMAC 加固

### 3.1 原始 Core 的形式化验证

1. **研究目的**：回答原始 Figure 7 core 中 secrecy、component origin 和完整参数对应关系分别是否成立。
2. **核心论点**：在 `BASELINE` 无泄露抽象中，sender/receiver symbolic key secrecy 成立、正常执行可达，但 `RecvDone ==> SendDone` 被反例否定；`COMPONENT` 的分量来源成立不能替代完整元组对应。
3. **机制/定义**：`HonestRun`、`SenderKey/ReceiverKey`、`SendDone/RecvDone`、`SplitKemAccepted/SenderSplitKemComponent`。
4. **必须展示的过程**：先报告 query 组和非空性，再以同一表展示正负结果；不要在本节提前展开密文重组细节。
5. **真实源码路径**：`proverif/kwaay_core_final.cpp.pv`。
6. **query/lemma 与结果**：`not event(HonestRun(k))` 为 `false`（即 HonestRun 可达）；`RecvDone ==> SendDone` 为 `false`；两项 prekey correspondence 为 `true`；sender/receiver secrecy 为 `true`；component origin 为 `true`。
7. **stdout/trace/证明日志**：`logs/final/proverif/summary.txt`；`logs/final/proverif/out/BASELINE.out`；`logs/final/proverif/out/COMPONENT.out`。
8. **衔接**：从方法进入首个结果；下一节解释为何 correspondence 失败而 secrecy 仍成立。
9. **图/表/公式**：表2的 original 行；P1 与 secrecy 公式。图2的左半部分由下一节引出。
10. **保留/合并/补充材料**：正文必须保留 `HonestRun` 非空性与正负结果并列；泄露变体矩阵移附录。不可只写“认证失败”，必须写清精确事件参数。

### 3.2 密文重组攻击路径与原因分析

1. **研究目的**：解释 `RecvDone ==> SendDone` 的真实反例，以及它为何不导致 attacker 得到接收方会话密钥。
2. **核心论点**：攻击者复用诚实发送的认证 split-KEM 分量 `ct_s`，以接收方公开材料生成新的 `ct_l/ct_k`，使接收方完成一个没有完整匹配 `SendDone(A,B,sid,k)` 的转录本；baseline receiver secrecy query 仍为 `true`。
3. **机制/定义**：消息完整元组、`sid` 对消息的绑定、component origin 与 full-parameter correspondence 的区别、non-injective correspondence 的语义。
4. **必须展示的过程**：诚实 `ct_s` 来源→攻击者构造新 `ct_l/ct_k`→组合新 `m'`→接收方计算 `sid'/k'`→`RecvDone`→不存在同参数 `SendDone`；单独标注“attacker(k') 未被证明可达”。
5. **真实源码路径**：`proverif/kwaay_core_final.cpp.pv` 的发送/接收过程和查询。
6. **query/lemma 与结果**：P1 `false`；sender/receiver secrecy 均 `true`；component origin `true`。这是 correspondence counterexample，不是 secrecy counterexample。
7. **stdout/trace/证明日志**：`logs/final/proverif/out/BASELINE.out`（实际 Horn-clause trace）；`logs/final/proverif/summary.txt`（结果汇总）。
8. **衔接**：解释 §3.1 的负结果；下一节引出用已导出会话密钥对 `sid` 做显式确认。
9. **图/表/公式**：图2左半；正文必须在图前说明“符号重组”，图后解释“缺失 matching SendDone，但 secrecy query 为真”。
10. **保留/合并/补充材料**：攻击的五步投影必须正文保留；冗长 ProVerif term 可放附录。不得写成 KEM break、key recovery 或 deployed exploit。

### 3.3 基于 HMAC 的密钥确认机制

1. **研究目的**：说明 HMAC confirmation 如何把 `sid` 与双方计算出的 `k` 显式绑定，并在接收完成前设置验证门。
2. **核心论点**：tag `hmac(confirm_key(k),sid)` 恢复当前无泄露 ProVerif baseline 上的完整参数 non-injective correspondence；它不携带 `bid/idx/rst`，因此不承担批内 freshness/dedup。
3. **机制/定义**：`confirm_key/1`、`hmac/2`、`msg_confirm(m,tag)`；sender 生成 tag，receiver 使用本地 `kRecv/sidBA` 匹配后才触发 `ReceiverKey/RecvDone`。
4. **必须展示的过程**：原始接收路径与 HMAC-gated 路径并列；指出 adversary 不能为重组后不同 `k'/sid'` 生成匹配 tag，但可以原样重放已见合法 confirmed message。
5. **真实源码路径**：`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`；`proverif/variants/hmac-confirmation/README.md`。
6. **query/lemma 与结果**：`HMAC_BASELINE` 中 `RecvDone ==> SendDone` 为 `true`；sender/receiver secrecy 为 `true`；component origin 为 `true`；`HonestRun` 可达。
7. **stdout/trace/证明日志**：`logs/variants/hmac-confirmation/proverif/summary.txt`；`logs/variants/hmac-confirmation/proverif/out/HMAC_BASELINE.out`。
8. **衔接**：从重组根因导出修复；下一节给出原始/HMAC 结果对照及泄露边界。
9. **图/表/公式**：图2右半；公式 `tag=HMAC_{confirm_key(k)}(sid)`。表2列 HMAC baseline。
10. **保留/合并/补充材料**：正文必须保留 tag 输入和验证时点；symbolic HMAC 构造细节移附录。不能称为计算 HMAC 证明或 replay protection。

### 3.4 修复前后的形式化验证结果

1. **研究目的**：用受控对照确认 HMAC 修复了什么，并说明无泄露/泄露条件边界。
2. **核心论点**：从 original baseline 到 `HMAC_BASELINE`，P1 由 `false` 变 `true`，baseline secrecy 与 component origin 保持；但 `HMAC_LEAK_SIGSK_A` 中 P1 为 `false`、receiver secrecy 为 `false`，因此正面结论限定在无该泄露的 baseline。
3. **机制/定义**：target 级比较：`BASELINE/COMPONENT` 对 `HMAC_BASELINE/HMAC_COMPONENT`；单独列 `HMAC_LEAK_SIGSK_A`，不外推到未执行的 compromise 组合。
4. **必须展示的过程**：表2逐行对照；正文解释 M4 是 Tamarin-only，未重跑这些 ProVerif query。
5. **真实源码路径**：两个 ProVerif 模型；M4 模型仅作为后文组合验证，不作为本节 ProVerif 证据。
6. **query/lemma 与结果**：原始 P1 `false`→HMAC baseline `true`；baseline 两项 secrecy 始终 `true`；HMAC component origin `true`；`HMAC_LEAK_SIGSK_A` P1 `false`、sender secrecy `true`、receiver secrecy `false`。
7. **stdout/trace/证明日志**：两份 ProVerif summary 及相应 `out/*.out`。
8. **衔接**：收束第一部分；下一章提出“合法性确认后，是否仍可在同批重复接受”。
9. **图/表/公式**：表2放本节；回引图2，不新增图。
10. **保留/合并/补充材料**：必须保留 baseline/泄露边界与 inherited evidence 说明；完整历史 leak target 表移附录。小节内容独立，不建议合并。

## 4 批内重复接受与安全影响分析

### 4.1 BatchReceive 前置条件与放宽输入模型

1. **研究目的**：明确重复输入模型相对 K-Waay 已声明参与方互异前置条件的地位。
2. **核心论点**：original replay/HMAC-only 模型故意允许同一 modeled party 和同一完整消息进入同一 `(B,bid,rst)` 的两个 slot；它研究准入/集成边界未维持条件时的行为，不是满足原前置条件的 K-Waay 执行反例。
3. **机制/定义**：fixed two-slot、same `B,bid,rst`、distinct `idx`；`SenderSession`/`ConfirmedSend` 与 `ReceiverAccept`/`ConfirmedReceiverAccept`；party identity 与 message identity 分离。
4. **必须展示的过程**：先写规范前置条件，再写 relaxed input；说明 Dolev–Yao 网络保留并向两个槽位投递相同 public message。
5. **真实源码路径**：`tamarin/replay/kwaay_replay_original.spthy`；`tamarin/replay/kwaay_replay_hmac_only.spthy`；`docs/rq-v2/g2-admission-semantics.md`。
6. **query/lemma 与结果**：original `one_send_two_accepts_exists` verified 15 steps、`same_message_accepted_at_most_once` falsified 13 steps、`injective_receiver_accept` falsified 16 steps；matching/source 与 normal path verified。
7. **stdout/trace/证明日志**：`logs/tamarin-m3-closeout/source-run2/aggregate-original-replay.tsv`；对应 `proofs/original-replay/*.out`；`tamarin/replay/README.md`。
8. **衔接**：从 §3.4 的 confirmation 成功转向 admission/occurrence 问题；下一节展示 HMAC-confirmed message 的实际双重接受。
9. **图/表/公式**：表3先列 original replay 与 HMAC-only；本节不放新图，图3留给条件化影响。
10. **保留/合并/补充材料**：前置条件边界必须正文重点保留；历史 original replay 完整 18-lemma 表可移附录。不得称为“原规范内攻击”。

### 4.2 HMAC 确认后的批内重复接受反例

1. **研究目的**：回答通过 HMAC 合法性/密钥确认的消息是否仍可在同一批次被接受两次。
2. **核心论点**：一个 matching `ConfirmedSend` 的完全相同 `<m,hmac(confirm_key(k),sid)>` 可进入两个 slot、通过相同 HMAC gate 并产生两个不同 `ConfirmedReceiverAccept`；没有 HMAC forgery。
3. **机制/定义**：matching coordinates `(A,B,m,sid,k,tag)`；receiver context `(bid,idx,rst)`；`HonestSession` 是成功会话重构抽象。
4. **必须展示的过程**：one confirmed send→同一 public confirmed message 两次投递→slot1/slot2 validation→两个 accept→正常 `BatchComplete`；trace 排除 sender/receiver compromise。
5. **真实源码路径**：`tamarin/replay/kwaay_replay_hmac_only.spthy`。
6. **query/lemma 与结果**：`one_confirmed_send_two_accepts_exists` verified 17 steps；`confirmed_message_accepted_at_most_once` falsified 15 steps；`injective_confirmed_receiver_accept` falsified 15 steps；matching、send uniqueness、normal single accept、normal completion 均 verified。
7. **stdout/trace/证明日志**：`logs/tamarin-replay-hmac-only/summary.txt`；`raw.out`；`attack-trace.out/json/dot`。
8. **衔接**：把 §3 的 P1 修复与 P2 缺口分开；下一节只在显式 consumer 假设下分析上层影响。
9. **图/表/公式**：表3列核心结果；不新增图，图3从该双 accept 作为输入边界开始，但要标明跨 theory 的“接口关系”而非一条联合机器 trace。
10. **保留/合并/补充材料**：核心 17/15-step 结果与无 forgery 解释必须正文保留；11 项 lifecycle lemma 可压缩后移附录。不得使用“HMAC 被绕过/攻破”。

### 4.3 C_install-v2 条件化安全影响

1. **研究目的**：在不把 `ReceiverAccept` 直接等同于真实会话安装的前提下，分析重复 accepted outputs 的条件化消费结果。
2. **核心论点**：在固定两输出、逐 output 独立安装且不按 `sid/message/peer/key` 合并的 `C_install-v2` 中，一个 matching send 可导致两个 accept、两个 fresh `aid` 和两个相同 `A,B,sid,k` 但不同 fresh handle 的 `InstallSession`；C7/C8 是假设，不是部署事实。
3. **机制/定义**：C1–C8；`AcceptOutputCreated(aid,...)`、linear `AcceptedOutput`、`InstallFromAccept(aid,h,...)`、`InstallSession(B,h,A,sid,k)`、`ConsumerComplete`；区分 `sid/aid/h`。
4. **必须展示的过程**：ReceiverAccept→accepted-output source→BatchComplete→两个独立安装→ConsumerComplete；说明两次安装均在 batch 完成后、consumer 完成前。
5. **真实源码路径**：`tamarin/impact/kwaay_impact_original.spthy`；`tamarin/impact/README.md`。
6. **query/lemma 与结果**：`one_send_two_accepts_two_installs_exists` verified 28 steps；`unique_install_within_completed_consumer` falsified 28 steps；`normal_one_accept_one_install` verified 22 steps；`normal_consumer_complete` verified 25 steps；19 个 composition lemmas 为 18 verified/1 falsified。
7. **stdout/trace/证明日志**：`logs/tamarin-impact-original/aggregate-results.tsv`；`attack-trace.out/json/dot`；`unique-install-trace.out/json/dot`；`summary.txt`。
8. **衔接**：从 §4.2 的下层输出进入条件化上层；下一节汇总攻击与失败性质，并为原子去重的放置点提供依据。
9. **图/表/公式**：图3放本节；表3同时列 duplicate acceptance 与 conditional installation，表头必须明确“模型条件”。
10. **保留/合并/补充材料**：C7/C8、`sid/aid/h` 区分及 28-step 正负结果必须正文保留；C1–C6 细节可压缩并移附录。不得写“两个真实会话”“session cloning”或 deployed impact。

### 4.4 攻击路径与失败性质验证

1. **研究目的**：用支撑性质排除伪解释，确认反例发生在可执行、状态受控的正常生命周期中。
2. **核心论点**：重复接受/条件化双安装不是由多次 send、close 后继续处理、receiver state 跨批复用或工具未终止造成；同时，失败路径和正常路径均需证明可达以避免真空结论。
3. **机制/定义**：send uniqueness、matching existence/order、slot distinctness、seal/process ordering、state consumption、batch/consumer completion。
4. **必须展示的过程**：对 original/HMAC-only/M2 各给一行“攻击见证 + supporting lemmas”；明确 M2 lower-layer 18/18 formula/result MATCH 只是选定回归保持，不是 trace equivalence。
5. **真实源码路径**：三个历史 replay/impact theory；V7 lifecycle theory。
6. **query/lemma 与结果**：`full_message_unique_send`、`receiver_accept_has_sender`、`confirmed_message_unique_send`、`confirmed_receiver_accept_has_sender`、`batch_end_token_single_use`、`receiver_state_single_batch_end`、M2 provenance/handle/consumer lemmas均为 verified；具体反例状态保持不变。
7. **stdout/trace/证明日志**：original replay proof outputs；HMAC-only `raw.out`；M2 `proofs/`、`frozen-formula-comparison.txt`、`lower-layer-result-comparison.txt`；V7 summary。
8. **衔接**：收束攻击和影响分析；下一章根据“必须在任何 ProcessSlot 前阻断 duplicate”提出 M3 原子去重。
9. **图/表/公式**：回引图3和表3；不新增核心图表。
10. **保留/合并/补充材料**：正文保留非空性、唯一发送和状态边界；逐 lemma provenance 表移 Artifact。若期刊篇幅紧，可与 §4.3 合并为末段，但必须保留本节全部边界句。

## 5 批内去重与组合加固验证

### 5.1 批内原子消息去重机制

1. **研究目的**：给出能在处理前阻断同一完整消息两次进入接受路径的最小修复。
2. **核心论点**：在同一 `B,bid,rst` 内，于两槽收集并 seal 后、任何 `ProcessSlot` 前，以 exact complete base message `m` 做一次线性原子决定；重复分支关闭 batch，distinct 分支继续。
3. **机制/定义**：`DedupPending`、`DedupDecisionToken`、`DuplicateDetected`、`DedupPassed`、`CheckedSlot1/2`、`BatchFail/BatchClosed/ConsumeReceiverState`。
4. **必须展示的过程**：duplicate `m1=m2`→无 accept/output/install；distinct `m1!=m2`→两个 slot 可处理并完成；强调 dedup identity 不是 `sid`、tag 或 party。
5. **真实源码路径**：`tamarin/replay/kwaay_replay_fixed.spthy`；`tamarin/impact/kwaay_impact_fixed.spthy`。
6. **query/lemma 与结果**：本节以机制为主，预告 `duplicate_batch_fail_exists` verified、`duplicate_detected_before_any_accept` verified、`dedup_outcomes_exclusive` verified。
7. **stdout/trace/证明日志**：`logs/tamarin-m3-closeout/source-run2/aggregate-fixed-replay.tsv`；`traces/duplicate-fail/trace.out/json/dot`。
8. **衔接**：回应 §4.4 的失败点；下一节用 original/fixed 机器结果验证修复有效且不真空。
9. **图/表/公式**：图4置于本节；公式给出 scope、identity、decision point。
10. **保留/合并/补充材料**：原子决定位置、duplicate/distinct 两分支必须正文保留；Tamarin search-control annotation 移附录。不得扩展为 global/cross-batch replay cache。

### 5.2 去重修复的形式化验证

1. **研究目的**：对照 original 与 fixed replay/impact，验证重复攻击被阻断且不同消息与失败路径仍可达。
2. **核心论点**：M3 将 original P2/P3 的负结果翻转为 scoped 正面结果，同时保留 normal distinct batch/consumer 和 slot failure 路径；修复不是靠禁止所有执行获得。
3. **机制/定义**：fixed replay 与 fixed impact 的相同 lower-layer dedup；impact 继续保留 `C_install-v2`，变化发生在 processing 前的 admission boundary。
4. **必须展示的过程**：original→fixed 的 attack witness、at-most-once、injectivity、duplicate failure、no accept/output/install、normal distinct completion 成对对照。
5. **真实源码路径**：M3 两个模型与 `tamarin/milestones/run-m3-dedup.sh`（只作为历史复现入口，本任务不执行）。
6. **query/lemma 与结果**：fixed replay：`one_send_two_accepts_exists` falsified 21 steps，`same_message_accepted_at_most_once` verified 34，`injective_receiver_accept` verified 70，`duplicate_batch_fail_exists` verified 19，`normal_distinct_batch_complete` verified 23；fixed impact：双安装 witness falsified 172，unique install verified 259，no output/install verified，`normal_distinct_consumer_complete` verified 35。
7. **stdout/trace/证明日志**：`logs/tamarin-m3-closeout/source-run2/aggregate-fixed-replay.tsv`；`aggregate-fixed-impact.tsv`；相应 `proofs/` 与五组 trace；顶层 composite vector/summary。
8. **衔接**：验证 dedup-only；下一节把它与 §3 的 HMAC confirmation 合并，检查两类性质能否同时维持。
9. **图/表/公式**：表4列 original、HMAC-only、M3、M4；回引图4。
10. **保留/合并/补充材料**：正文必须保留攻击被阻断与正常 distinct path 可达；M3 196/196 transparent composite 的运行细节可放 Artifact，但必须注明没有单次 source run 达到 196/196 terminal。

### 5.3 HMAC 与去重组合方案

1. **研究目的**：验证完整参数确认与批内 exact-message occurrence uniqueness 能在同一 fixed-two-slot 模型中组合。
2. **核心论点**：HMAC gate 负责 confirmed origin/agreement，dedup 以 base message `m` 在 processing 前拒绝重复；去重不能按 `<m,tag>`，否则同 base/different tag 可能逃逸设计意图。
3. **机制/定义**：`ConfirmedSend`、`HmacValidated`、`ConfirmedReceiverAccept`；base `m` 与 confirmed tuple `<m,tag>`；combined replay 与 tag-free consumer interface。
4. **必须展示的过程**：valid tag+distinct base messages→两个接受/完成；same base+same/different tag→duplicate failure；invalid tag slot1/slot2 mismatch；impact 中 output/install 仅在完成 batch 后发生。
5. **真实源码路径**：`tamarin/replay/kwaay_replay_hmac_dedup.spthy`；`tamarin/impact/kwaay_impact_hmac_dedup.spthy`。
6. **query/lemma 与结果**：`confirmed_accept_requires_hmac_validated`、`confirmed_accept_requires_valid_tag`、两个 at-most-once、injectivity、`duplicate_same_base_different_tag_fail_exists` 均 verified；two-accept witness falsified；impact 的 two-install witness falsified、unique install/no output/no install/normal distinct consumer 均 verified。
7. **stdout/trace/证明日志**：`logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv`；`source-run1/` 与 `source-run2/` 对应 proofs；五组 `traces/`。
8. **衔接**：组合 §3 与 §5.2 的修复；下一节用完整前后矩阵与正常/失败路径边界作收束。
9. **图/表/公式**：图4右侧显示组合流程；表4给组合结果。
10. **保留/合并/补充材料**：same-base/different-tag、distinct valid completion 与 tag-free consumer 边界必须保留；62 条 impact lemma 清单移 Artifact。不得把 `HonestSession` 结构性来源证明写成 computational HMAC theorem。

### 5.4 修复前后性质及正常执行对照

1. **研究目的**：给出论文最核心的前后矩阵，证明两种修复各自解决目标性质且未破坏必要正常路径。
2. **核心论点**：original/HMAC-only 可达的 duplicate witness 在 M3/M4 中不可达；P1 由独立 ProVerif HMAC evidence 支持；M4 同时保留 two-distinct-valid confirmed batch/consumer；部分失败 batch 仍可能已有 slot1 lower-layer output。
3. **机制/定义**：attack witness vs universal safety；normal reachability vs failure reachability；ProVerif inherited evidence vs M4 Tamarin-only composite。
4. **必须展示的过程**：按 P1/P2/P3/normal/failure 五组行比较 original core、HMAC baseline、HMAC-only replay、M3、M4；标注不可跨层比较的单元格。
5. **真实源码路径**：全部 core/replay/impact 修复模型；`artifact/results/claim-matrix.tsv` 作为索引。
6. **query/lemma 与结果**：M4 296/296 terminal、296/296 MATCH、281 verified、15 falsified、0 conflict/unresolved/mismatch；关键 normal lemmas verified；`hmac_failure_slot2_after_prior_accept_exists`/`...replay_exists` verified，故不能声称每个失败 batch 都无 partial lower-layer output。
7. **stdout/trace/证明日志**：M4 `composite-summary.txt`、`composite-selection.tsv`、`composite-result-vector.tsv`；normal-replay、normal-consumer、slot1/slot2-mismatch traces。
8. **衔接**：结束修复验证；下一章解释 confirmation、dedup、party admission 三者为何仍不能互相替代。
9. **图/表/公式**：表4置于本节；回引图4。无需额外图。
10. **保留/合并/补充材料**：必须保留 M4 composite 的透明性、正常路径和 partial-output 边界；资源限制、fallback 行细节移 Artifact。不能把 composite 说成一次 296/296 source run，也不能说 M4 重跑了 ProVerif。

## 6 讨论与适用边界

### 6.1 接收确认、消息去重与参与方互异的不同作用

1. **研究目的**：综合解释三种机制保护的 identity coordinate 与失效模式。
2. **核心论点**：HMAC confirmation 绑定 `k/sid/full message`；exact-message dedup 约束同批相同 `m` 的 occurrence；`DistinctPartyPerBatch` 约束不同槽位的 party coordinate。三者互补而非替代。
3. **机制/定义**：confirmed-message identity、base-message identity、party identity；correspondence、occurrence injectivity、batch identity semantics。
4. **必须展示的过程**：分别给出“无 HMAC 的重组”“有 HMAC 无 dedup 的双接受”“有 dedup 无 party guard 的 same-party/different-message”三个反例类别；明确来自不同 theory，不拼接。
5. **真实源码路径**：HMAC ProVerif；HMAC-only/M4 replay；RQ-v2 message-dedup/party-admission models。
6. **query/lemma 与结果**：P1 original false/HMAC true；HMAC-only duplicate witness verified；M4 duplicate witness falsified；RQ-v2 `same_party_different_messages_batch_exists` verified。
7. **stdout/trace/证明日志**：相应 ProVerif summaries、HMAC-only trace、M4 vector、RQ-v2 result comparison/trace JSON。
8. **衔接**：从修复结果上升到机制职责；下一节用 R/M/P 对照正式证明 message-level 条件不能替代 party-level 条件。
9. **图/表/公式**：不新增图；可用三行职责对照框，引用表1与表4。
10. **保留/合并/补充材料**：职责三分必须正文保留。若篇幅极紧，可与 §6.2 合并，但应先保留本节概念区分、再给 RQ-v2 机器证据。

### 6.2 RQ-v2 的消息级和参与方级约束比较

1. **研究目的**：用 R/M/P 三个最小原型回答 exact-message dedup 是否足以维护 `DistinctPartyPerBatch`。
2. **核心论点**：R-semantics 允许同 party/exact entry 重复并产生 duplicate accept；M-semantics 拒绝 exact message 且恢复 scoped occurrence injectivity，却仍允许同 party 的两个不同消息；P-semantics 拒绝 same-party 并保留 distinct-party 正常 batch。
3. **机制/定义**：R=relaxed admission；M=message inequality；P=party inequality；party coordinate `A` 不等于 message、sid、prekey 或 deployed identity object。
4. **必须展示的过程**：R 的 one-send/two-accept；M 的 `A,m1`/`A,m2` 两发送两接受；P 的 same-party rejection 与 `A1!=A2` 正常 batch。
5. **真实源码路径**：三个 `tamarin/rq-v2-minimal/rqv2_*.spthy`；`docs/rq-v2/prototype-execution-report.md`。
6. **query/lemma 与结果**：R：3 verified/1 falsified；M：5 verified，包括 `same_party_different_messages_batch_exists` 16 steps；P：5 verified，包括 `same_party_rejection_exists` 5、`distinct_party_batch_exists` 17、`accepted_batch_has_distinct_parties` 31。
7. **stdout/trace/证明日志**：`reviews/2026-09-16-evidence/*-prove.stdout.txt`；三个 `*-traces.json`；`result-comparison.tsv`（14/14 MATCH，13 verified/1 falsified）；`trace-audit-summary.txt`。
8. **衔接**：给 §6.1 的职责区分提供机器证据；下一节集中列举模型假设和不能外推的范围。
9. **图/表/公式**：不增加第五张核心表；将 R/M/P 精简比较作为表4的“修复边界”分区或正文小矩阵。可给 `i!=j => A_i!=A_j` 公式。
10. **保留/合并/补充材料**：same-party/different-message 与 P positive control 必须正文保留；14 项完整表可移附录/Artifact。不得把 RQ-v2 accept trace与 M2 install trace拼成同一攻击。

### 6.3 模型假设、研究局限与适用范围

1. **研究目的**：集中声明论文所有结果的外推边界，避免符号证据被误读为完整协议或部署结论。
2. **核心论点**：现有证据足以支撑“符号安全边界、条件化影响与组合修复”定位；它不支撑规范内通用攻击、部署会话克隆、全局 replay protection、计算安全或 source-to-model refinement。
3. **机制/定义**：free-constructor/Dolev–Yao；fixed two-slot（V7 为 fixed four-slot lifecycle）；same-batch/same-state；batch-local exact-message；no rollback/restart/cross-batch；`HonestSession`；`C_install-v2`；RQ-v2 minimal party abstraction。
4. **必须展示的过程**：以“已证明—未建模—条件化—概念解释”四列表述每个边界；把真实实现的 party admission enforcement location 标为未确定。
5. **真实源码路径**：各 README、milestone completion、`docs/claim-hierarchy.md`、`artifact/results/claim-matrix.tsv`。
6. **query/lemma 与结果**：不新增 query；引用前文结果并明确其量化范围。`HMAC_LEAK_SIGSK_A` 是已观察负面边界，不是完整 compromise matrix。
7. **stdout/trace/证明日志**：M5 的 `actual-results.tsv`、`raw-to-summary.tsv`、`validation/summary.tsv` 用于证明结果可追踪；不作为新安全性质。
8. **衔接**：收束讨论；下一节只总结已证实结论与条件化边界，不提出新结果。
9. **图/表/公式**：不新增图；可在正文用紧凑边界表，但不计入四张核心表。
10. **保留/合并/补充材料**：fixed-slot、C7、无部署映射、无计算证明、不可跨模型拼接必须正文保留；工具版本/哈希/完整清单移 Artifact。内容独立，不建议删除。

## 7 结束语

1. **研究目的**：用最短闭环回答全文问题并给出严格结论强度。
2. **核心论点**：原始 core 的 baseline secrecy 成立而 P1 失败；HMAC 在无泄露 baseline 修复 P1；合法 confirmed message 仍可在 relaxed 同批模型中重复接受；该行为在 `C_install-v2` 下具有条件化双安装影响；M3/M4 阻断 scoped witness 并保持正常路径；party-level invariant 仍需独立维护。
3. **机制/定义**：只复用 P1/P2/P3 和 `DistinctPartyPerBatch`，不引入新概念。
4. **必须展示的过程**：按上述六句因果链总结，但明确 ProVerif、historical replay/impact、RQ-v2 是相互约束的独立证据层，而非一条联合 trace。
5. **真实源码路径**：不新增；回指各节模型与 M5 artifact。
6. **query/lemma 与结果**：只引用表2–表4的代表结果；不得新增“总体安全”结论。
7. **stdout/trace/证明日志**：回指四表的证据来源与 `artifact/validation/summary.tsv`。
8. **衔接**：承接 §6.3；以“适用边界内研究闭环已经完成”结束，不启动新研究任务。
9. **图/表/公式**：无新图表公式。
10. **保留/合并/补充材料**：正文必须保留 conditional 与 relaxed-input 限定；可省略数值型运行统计。结束语不能声称所有 replay、任意 batch、真实实现或计算安全均已解决。

## 大纲冻结判断

按上述结构正式重写，能够完整、准确地展示原项目已经完成的安全分析、攻击发现和加固研究，前提是写作中持续保持三条证据边界：

1. 原始 ProVerif 密文重组反例、historical Tamarin 批内重复接受、M2 条件化安装和 RQ-v2 party-admission 分析不得拼成一条未经机器验证的攻击；
2. `C_install-v2` 尤其 C7/C8 必须始终标为条件化 consumer 假设；
3. M3/M4 exact-message dedup 的正面结论不得替代 `DistinctPartyPerBatch`。

当前不存在阻止该论文定位成立的科学证据缺口。尚缺的是更强主张所需的外部证据：真实上层逐 output 安装行为、任意长度/跨批/回滚性质、实现或部署验证、计算安全证明以及 source-to-model refinement。它们属于主张扩展缺口，不是本论文既定范围内尚未完成的工作。M0 缺少单独的 `M0-completion.md` 是文档可追溯性债务，也不是科学结果缺口。
