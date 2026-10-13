# 逐节研究内容与证据映射

## 1. 使用规则

本文件是 `DETAILED_PAPER_OUTLINE.md` 的证据账本。所有结果均来自基线
`112667a69c95dae4e9abc5781a6ddb8df6a10fdd` 中已保存的源码和日志；本次未重新运行
ProVerif 或 Tamarin。

证据等级：

| 标签 | 含义 | 论文写法 |
| --- | --- | --- |
| F+ | 已保存的全称性质为 `true/verified` | “在该模型和量化范围内得到验证” |
| F− | 全称性质为 `false/falsified` 且有反例 | “该性质在该模型中不成立” |
| W+ | `exists-trace` 为 `verified` | “存在机器见证/该路径可达” |
| W− | `exists-trace` 为 `falsified - no trace found` | “该命名见证在该模型中不可达”，不能泛化为更大范围 |
| C | 在 `C_install-v2` 下的条件化 F/W 结果 | 必须在句中显式写条件 |
| S | 协议/模型语义解释 | 不得写成机器证明 |
| D | 设计建议或写作选择 | 不得列入验证贡献 |

## 2. 核心证据包

### E-PV-O：原始 ProVerif core

- 模型：`proverif/kwaay_core_final.cpp.pv`。
- 原始结果：`logs/final/proverif/summary.txt`。
- 关键 stdout：`logs/final/proverif/out/BASELINE.out`、`COMPONENT.out`。
- `BASELINE`：
  - `not event(HonestRun(k)) is false`，即正常事件可达（W+）；
  - `event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)) is false`（F−）；
  - 两项 prekey correspondence 为 `true`（F+）；
  - sender/receiver key secrecy query 均为 `true`（F+）。
- `COMPONENT`：`SplitKemAccepted ==> SenderSplitKemComponent` 为 `true`（F+）。
- `BASELINE.out` 的反例投影：复用诚实 `ct_s`，以公开接收方材料生成新的
  `ct_l/ct_k`，接收方触发没有完整参数匹配 `SendDone` 的 `RecvDone`。同一 baseline
  的 receiver secrecy 为 `true`，所以该 trace 不是 attacker key recovery。

### E-PV-H：HMAC confirmation ProVerif variant

- 模型：`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`。
- 原始结果：`logs/variants/hmac-confirmation/proverif/summary.txt`。
- 关键 stdout：同目录 `out/HMAC_BASELINE.out`、`HMAC_COMPONENT.out`、
  `HMAC_LEAK_SIGSK_A.out`。
- `HMAC_BASELINE`：HonestRun 可达；P1、两项 prekey correspondence、两项 secrecy
  均为 `true`（W+/F+）。
- `HMAC_COMPONENT`：component origin 为 `true`（F+）。
- `HMAC_LEAK_SIGSK_A`：P1 为 `false`、receiver secrecy 为 `false`、sender secrecy
  为 `true`。这只界定已执行的 sender authentication-key 泄露目标，不能外推到完整
  compromise matrix。

### E-TV7：Tamarin receiver/batch lifecycle

- 模型：`tamarin/kwaay_splitkem_batch_dynamic_v6.spthy`、
  `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`。
- 结果：`logs/tamarin-v6/summary.txt`、`logs/tamarin-v7/summary.txt`。
- V7 selected lemmas 共 24 项均 VERIFIED，包括五项 executability、
  `seal_requires_all_slots_added`、`process_requires_slot_added`、
  `process_requires_seal`、`complete_requires_all_slots_done`、
  `no_slot_accept_after_close`、`batch_complete_consumes_state`、
  `batch_fail_consumes_state`、`batch_end_token_single_use`、
  `receiver_state_single_batch_end`、`slot_origin`。
- 边界：V7 是 fixed four-slot terminal lifecycle，不是任意长度模型；V6/V7 不替代
  historical fixed-two-slot replay/impact theory。

### E-R0：原始 fixed-two-slot replay

- 模型：`tamarin/replay/kwaay_replay_original.spthy`。
- 保存结果：`logs/tamarin-m3-closeout/source-run2/aggregate-original-replay.tsv`。
- 逐 lemma stdout：
  `logs/tamarin-m3-closeout/source-run2/proofs/original-replay/*.out`。
- 核心结果：
  - `normal_single_accept` verified 11 steps（W+）；
  - `normal_batch_complete` verified 16（W+）；
  - `one_send_two_accepts_exists` verified 15（W+）；
  - `same_message_accepted_at_most_once` falsified, found trace, 13（F−）；
  - `full_message_unique_send` verified 2（F+）；
  - `receiver_accept_has_sender` verified 16（F+）；
  - `injective_receiver_accept` falsified, found trace, 16（F−）；
  - lifecycle/state lemmas为 verified。
- 边界：模型故意放宽同批 distinct-party 输入纪律；结果是同批相同消息的 duplicate
  successful receiver output，不是规范内攻击、密钥泄露、跨批 replay 或部署漏洞。

### E-RH：M1 HMAC-only replay bridge

- 模型：`tamarin/replay/kwaay_replay_hmac_only.spthy`。
- 结果：`logs/tamarin-replay-hmac-only/summary.txt`、`raw.out`。
- trace：`logs/tamarin-replay-hmac-only/attack-trace.out/json/dot`。
- 核心结果：
  - `normal_confirmed_single_accept` verified 12（W+）；
  - `normal_confirmed_batch_complete` verified 18（W+）；
  - `confirmed_receiver_accept_has_sender` verified 16（F+）；
  - `confirmed_message_unique_send` verified 2（F+）；
  - `one_confirmed_send_two_accepts_exists` verified 17（W+）；
  - `confirmed_message_accepted_at_most_once` falsified 15（F−）；
  - `injective_confirmed_receiver_accept` falsified 15（F−）。
- trace 条件：相同 `(A,B,bid,rst,m,sid,k,tag)`、不同 slot/timepoint、一个 matching
  ConfirmedSend、无 sender/receiver state compromise、正常 BatchComplete。
- 边界：`HonestSession` 使 matching existence 主要是结构性映射；正面的 concrete P1
  证据仍是 E-PV-H。该 trace 重放有效 tag，不伪造 HMAC。

### E-I0：M2 原始 impact/composition

- 模型：`tamarin/impact/kwaay_impact_original.spthy`。
- 结果：`logs/tamarin-impact-original/aggregate-results.tsv`、`summary.txt`、`proofs/`。
- trace：`attack-trace.out/json/dot`、`unique-install-trace.out/json/dot`。
- 核心结果：
  - `normal_one_accept_one_install` verified 22（C/W+）；
  - `normal_consumer_complete` verified 25（C/W+）；
  - `one_send_two_accepts_two_installs_exists` verified 28（C/W+）；
  - `unique_install_within_completed_consumer` falsified 28（C/F−）；
  - composition 19 项为 18 verified/1 falsified；总计 37 terminal、34 verified/
    3 falsified。
- 回归：`frozen-formula-comparison.txt` 与 `lower-layer-result-comparison.txt` 均为
  18/18 MATCH。
- 边界：C7 假设 fixed consumer 独立安装每个成功 output 且不合并/去重；C8 明确
  C7 不是 deployed K-Waay 事实。两个不同 fresh handle 不是两个真实会话。

### E-M3：M3 batch-local atomic exact-message dedup

- 模型：`tamarin/replay/kwaay_replay_fixed.spthy`、
  `tamarin/impact/kwaay_impact_fixed.spthy`。
- 结果：`logs/tamarin-m3-closeout/composite-result-vector.tsv`；主要逐项结果在
  `source-run2/aggregate-fixed-replay.tsv`、`aggregate-fixed-impact.tsv` 及对应
  `proofs/`。
- trace：`source-run2/traces/duplicate-fail/`、`distinct-complete/`、
  `distinct-fail-slot1/`、`distinct-fail-slot2/`、`distinct-consumer/`。
- fixed replay 核心结果：two-accept witness falsified 21（W−）；at-most-once verified
  34（F+）；injectivity verified 70（F+）；duplicate failure verified 19（W+）；
  duplicate no accept verified 12（F+）；normal distinct completion verified 23（W+）。
- fixed impact 核心结果：two-install witness falsified 172（C/W−）；unique install
  verified 259（C/F+）；duplicate no output/install verified（C/F+）；normal distinct
  consumer verified 35（C/W+）。
- composite：196/196 expected terminal、0 conflict、0 mismatch；没有单次 source run
  达到 196/196 terminal。
- 边界：same `(B,bid,rst)`、exact complete message、fixed two-slot、processing 前；
  不是 global/cross-batch/rollback/restart replay protection。

### E-M4：M4 HMAC+dedup combined verification

- 模型：`tamarin/replay/kwaay_replay_hmac_dedup.spthy`、
  `tamarin/impact/kwaay_impact_hmac_dedup.spthy`。
- 结果：`logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv`、
  `composite-summary.txt`、`composite-selection.tsv`。
- 逐项 stdout/trace：`source-run1/proofs/`、`source-run2/proofs/` 和两处 `traces/`。
- replay 核心结果：matching/tag validation、confirmed/base-message at-most-once、
  scoped injectivity、same-base/different-tag duplicate failure、normal two-distinct-valid
  completion均 verified；`one_confirmed_send_two_accepts_exists` falsified。
- impact 核心结果：`one_confirmed_send_two_accepts_two_installs_exists` falsified；
  `unique_install_within_completed_consumer`、duplicate no output/install、normal
  two-distinct-valid consumer completion均 verified。
- 失败边界：`hmac_failure_slot2_after_prior_accept_exists` 与 replay variant verified，
  所以不能声称每个失败 batch 都没有 partial lower-layer output。
- composite：296/296 terminal、296/296 MATCH、281 verified、15 falsified、0 conflict、
  0 unresolved、0 mismatch。它由两个完整 manifest-valid Tamarin-only source run
  透明组合；不是一次单独的 296/296 run，也未重跑 ProVerif。

### E-RQ：RQ-v2 R/M/P 比较

- 模型：`tamarin/rq-v2-minimal/rqv2_relaxed.spthy`、
  `rqv2_message_dedup.spthy`、`rqv2_party_admission.spthy`。
- 权威说明：`docs/rq-v2/g2-admission-semantics.md`、
  `docs/rq-v2/prototype-execution-report.md`。
- 原始输出：`reviews/2026-09-16-evidence/*-prove.stdout.txt`；trace JSON；
  `result-comparison.tsv`、`trace-audit-summary.txt`。
- R：`normal_relaxed_batch_exists` verified 10；`one_send_two_accepts_exists`
  verified 13；`receiver_accept_has_send` verified 8；`receiver_accept_injective`
  falsified 13。
- M：`repeated_message_rejection_exists` verified 4；
  `same_party_different_messages_batch_exists` verified 16；
  `accepted_batch_has_distinct_messages` verified 31；matching 与 injectivity verified。
- P：`same_party_rejection_exists` verified 5；`distinct_party_batch_exists` verified 17；
  `accepted_batch_has_distinct_parties` verified 31；matching 与 injectivity verified。
- 总计：14/14 MATCH，13 verified/1 falsified。
- 边界：仅 two-slot identity-level abstraction；不建模 KEM/HMAC/key/output/consumer。
  RQ-v2 trace 不能与 E-I0 的 installation trace 拼接。

### E-M5：可复现实验冻结

- 入口：`scripts/run-paper-artifact.sh`（本任务未执行）。
- 结果账本：`artifact/results/expected-results.tsv`、`actual-results.tsv`、
  `claim-evidence.tsv`、`claim-matrix.tsv`、`raw-to-summary.tsv`。
- 验证摘要：`artifact/validation/summary.md`、`summary.tsv`。
- 冻结事实：405 expected/actual；296 Tamarin；89 inherited ProVerif；20 M4
  ProVerif `not_run_out_of_scope`；66 artifact inventory；92 Git-blob/infrastructure
  checksum；M5 没有运行证明器或新增安全性质。

## 3. 逐节证据分配矩阵

| 节 | 研究目的与核心论点 | 机制/必须展示的过程 | 源码与机器结果 | 原始日志/trace | 衔接 | 图表/公式 | 正文必须保留；可合并或移附录 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 引言 | 提出 P1 与 P2 两问及条件化 P3；给出完整研究闭环 | 只给总路线，不拼接跨模型 trace | E-PV-O、E-PV-H、E-RH、E-I0、E-M3、E-M4、E-RQ | 各 evidence summary/vector | →§1 协议对象 | 表1预告；无图 | 保留贡献与边界；统计细节移 Artifact |
| 1.1 | 解释 Figure 7 core 与三分量/KDF | `m`、`sid`、`k`，诚实 send/receive | E-PV-O 模型；结果仅预告 | ProVerif summary | →§1.2 batch | 三个公式；图1的一部分 | 保留完整参数；构造子细节移附录 |
| 1.2 | 解释 BatchReceive 生命周期与 distinct-party 前置条件 | Add→Seal→Process→Complete/Fail，共享 `B,bid,rst` | E-TV7；selected lifecycle 全 VERIFIED；E-RQ 语义 | V7 summary | →§1.3 问题范围 | 图1；互异公式 | 保留状态主干/互异；完整 lemma 表移附录 |
| 1.3 | 分离 P0/P1/P2/P3 与 party identity | 性质层次文字图 | M0 语义文档、E-M5 claim matrix | claim-evidence/raw-to-summary | →§2 形式化 | 表1 | 必须保留禁止推断；提交历史移 Artifact |
| 2.1 | 冻结 Dolev–Yao、compromise、composition 假设 | 重组、重放、batch composition、C_install-v2 | E-PV-O、E-RH、E-I0、E-RQ | baseline/HMAC-only/M2 traces | →§2.2 | 表1的假设列 | 保留 deployed adversary 区分；完整泄露矩阵移附录 |
| 2.2 | 定义 ProVerif query/事件 | receiver 检查链及 HMAC gate | E-PV-O、E-PV-H | BASELINE/HMAC stdout | →§2.3 | query 公式块 | 保留 no-batch 边界；宏/构造子移附录 |
| 2.3 | 定义 Tamarin 状态/事件层 | lifecycle、replay、impact、R/M/P 分 theory | E-TV7、E-R0、E-RH、E-I0、E-M3、E-M4、E-RQ | 各 Tamarin evidence | →§2.4 | 回引图1、表1 | 保留事件签名分离；rule 全文移 Artifact |
| 2.4 | 给出可引用的性质公式与证据语义 | P1/P2/P3/party invariant 并列 | E-M5 语义/结果索引 | actual-results/raw-to-summary | →§3 结果 | 表1+公式 | 保留 W/F/C 解释；405 行表移 Artifact |
| 3.1 | 报告原始 core 正负结果 | 先非空性，再 secrecy/component/P1 | E-PV-O：P1 F−；secrecy/component F+；HonestRun W+ | baseline/component stdout | →§3.2 解释反例 | 表2 original 行 | 正负结果必须同表；leak matrix 移附录 |
| 3.2 | 解释真实密文重组与无 key recovery | honest `ct_s` + 新 `ct_l/ct_k` → unmatched RecvDone | E-PV-O | `BASELINE.out` | →§3.3 HMAC | 图2左半 | 保留五步路径和 secrecy 对照；原始大 term 移附录 |
| 3.3 | 定义 HMAC confirmation | `tag=hmac(confirm_key(k),sid)`；RecvDone 前验证 | E-PV-H baseline P1/secrecy/component F+ | HMAC_BASELINE stdout | →§3.4 对照 | 图2右半；tag 公式 | 保留 tag 输入/时点；不称 replay fix |
| 3.4 | 比较修复前后与泄露边界 | BASELINE↔HMAC_BASELINE；单列 HMAC_LEAK_SIGSK_A | E-PV-O、E-PV-H | 两份 summary | →§4 合法消息仍可重复？ | 表2 | 保留 no-compromise 与 inherited evidence；全 target 细节移附录 |
| 4.1 | 定义 relaxed-input 边界 | 同 party/同 message 占两个 slot，违反原前置条件 | E-R0：W+/F−；E-RQ semantic contract | original proof logs | →§4.2 HMAC-only | 表3首组 | 必须写“非规范内反例”；完整 18 lemmas 移附录 |
| 4.2 | 展示合法 confirmed message 双重接受 | 一个 ConfirmedSend→两次 accept→complete，无 forgery/compromise | E-RH：17-step W+；两个 15-step F− | HMAC-only attack trace | →§4.3 conditional impact | 表3；图3仅作接口起点 | 核心 trace 正文；lifecycle 表移附录 |
| 4.3 | 分析 C_install-v2 条件化影响 | accept→aid→install h1/h2→ConsumerComplete | E-I0：28-step双安装 W+；28-step unique F−；正常路径 W+ | M2 两组 trace/aggregate | →§4.4 排除伪解释 | 图3+表3 | C7/C8、sid/aid/h 必须保留；C1–C6 可压缩 |
| 4.4 | 证明 trace 非真空且状态受控 | uniqueness/matching/lifecycle/regression 支撑 | E-R0、E-RH、E-I0、E-TV7 | proofs 与 18/18 comparisons | →§5 修复 | 回引图3/表3 | 保留唯一 send/state 边界；可并入§4.3末段但不能删 |
| 5.1 | 定义 processing 前原子 exact-message dedup | seal 后一次决定；duplicate close；distinct pass | E-M3 模型；duplicate decision lemmas F+/W+ | duplicate-fail trace | →§5.2 验证 | 图4；scope/identity/point 公式 | 必须保留决定时点；search annotation 移附录 |
| 5.2 | 验证 M3 修复有效且不真空 | original↔fixed replay/impact 成对对照 | E-M3：attack W−，safety F+，normal distinct W+ | aggregates/proofs/5 traces | →§5.3 组合 | 表4 | 保留正常/失败路径；196-run细节移 Artifact但注明 composite |
| 5.3 | 组合 HMAC 与 dedup | valid distinct、same-base/different-tag、mismatch、consumer | E-M4 关键 lemmas如上 | M4 proofs/5 traces | →§5.4 总对照 | 图4右半+表4 | 保留 base-vs-confirmed identity；62 lemmas 移 Artifact |
| 5.4 | 汇总 P1/P2/P3/normal/failure | 标注不可比较单元格与 partial output 边界 | E-PV-H（inherited）+E-M4（Tamarin-only 296 composite） | table/vector/trace | →§6 机制边界 | 表4 | 保留 composite透明性；资源/fallback细节移 Artifact |
| 6.1 | 区分 confirmation/dedup/party admission | 三类失效例来自三种独立模型 | E-PV-O/H、E-RH/M4、E-RQ | 各代表 trace | →§6.2 机器比较 | 三行职责框 | 必须保留“不拼 trace”；可与§6.2合并但不删概念层 |
| 6.2 | 用 R/M/P 证明 message≠party | R duplicate；M same-party/different-message；P rejection+positive control | E-RQ：14/14 MATCH，13 verified/1 falsified | RQ-v2 stdout/trace JSON | →§6.3 局限 | 表4边界分区；互异公式 | 保留 M/P 两个 witness；完整14项移附录 |
| 6.3 | 集中声明适用范围 | 已证明/未建模/条件化/概念解释四分 | E-M5 与所有模型 README/里程碑 | M5 validation 仅作追踪 | →§7 结论 | 可用非核心边界表 | fixed-slot、C7、no deployment/computational/refinement 必留 |
| 7 | 收束六句结论 | 不引入新性质或新攻击链 | 表2–表4及 E-M5 | 回指现有证据 | 论文结束 | 无新图表 | 保留 relaxed/conditional；不写总体安全 |

## 4. 重点核查结论

### 4.1 `RecvDone ==> SendDone` 的真实反例

- **确认存在**：E-PV-O 的 `BASELINE` query 为 `false`，`BASELINE.out` 有实际 trace。
- **反例内容**：复用诚实 `ct_s`，新建 `ct_l/ct_k`，得到无完整 matching
  `SendDone` 的 `RecvDone`。
- **同时成立**：baseline sender/receiver secrecy 都为 `true`；因此不能写 key
  recovery。

### 4.2 HMAC 修复的无泄露条件

- **确认完成**：E-PV-H 的 `HMAC_BASELINE` 中同一 P1 query 为 `true`，两项
  secrecy、两项 prekey correspondence 及 component origin 亦为 `true`，HonestRun
  可达。
- **边界**：`HMAC_LEAK_SIGSK_A` 中 P1 与 receiver secrecy 为 `false`；所以论文
  必须使用“no-compromise baseline”或等价限定。

### 4.3 HMAC-only 重复接受反例

- **确认完成**：E-RH 的 17-step `one_confirmed_send_two_accepts_exists` verified；
  两项 at-most-once/injectivity 性质各在 15 steps falsified。
- **解释**：相同有效 confirmed message 被投递两次，不涉及 HMAC forgery。

### 4.4 M2 条件化重复安装

- **确认完成**：E-I0 的 28-step 双安装见证 verified；28-step unique installation
  性质 falsified。
- **条件**：只在 `C_install-v2`，尤其 C7 的逐 output 独立安装假设下成立。

### 4.5 M3 消息去重修复

- **确认完成**：E-M3 中 two-accept/two-install witness 均 falsified；对应 safety、
  no-output/no-install 与 normal distinct execution 均 verified。
- **范围**：同 `(B,bid,rst)`、exact complete `m`、fixed two-slot、batch-local。

### 4.6 M4 HMAC+dedup 组合验证

- **确认完成**：E-M4 关键 combined replay/impact 结果均匹配冻结预期；296/296
  transparent composite terminal/MATCH。
- **来源说明**：ProVerif P1 结果继承 E-PV-H，M4 没有重跑 ProVerif。

### 4.7 RQ-v2 参与方互异补充结果

- **确认完成**：E-RQ 的 M-semantics 可恢复 exact-message occurrence injectivity，
  但 `same_party_different_messages_batch_exists` verified；P-semantics 的 same-party
  rejection、distinct-party normal batch 与 admitted-party distinctness 均 verified。
- **结论**：message dedup 不能替代 `DistinctPartyPerBatch`；该结论止于 identity-level
  admission/acceptance，不推出 M2 installation 结果。

## 5. 证据缺口判定

在本文冻结题目和符号分析定位内，以上七项重点均已有真实模型、命名 query/lemma、
终态结果及 stdout/trace/proof 支持，不应标为待完成。

真正缺少的证据只会阻止更强主张：

- `C_install-v2` C7 到真实规范/实现消费行为的映射；
- 任意长度、跨批、rollback/restart、global replay 性质；
- 完整 compromise matrix，尤其 HMAC 的材料/时序覆盖；
- 真实实现、部署利用、Double Ratchet/application 行为；
- computational security 与 source-to-model refinement theorem。

这些缺口不阻止按当前大纲写成“接收端符号安全边界、条件化影响与组合加固”论文。
