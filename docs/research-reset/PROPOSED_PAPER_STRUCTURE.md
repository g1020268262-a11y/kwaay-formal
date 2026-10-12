# 基于 M0--M5 的建议论文结构

## 1. 论文题目与定位

建议题目：

> **K-Waay 中认证确认与批内重放的符号分析及组合修复**

可选英文题目：

> **Symbolic Analysis and Composed Hardening of Confirmation and Batch Replay in K-Waay**

题目避免声称完整协议被攻破，也不把 `C_install-v2` 的条件化结果写成真实会话
克隆。

## 2. 建议研究问题

### RQ1：原始 core 的符号安全目标边界是什么？

在 Figure 7 core 的 no-compromise ProVerif 抽象中，session-key secrecy、
split-KEM component origin 和 full-parameter non-injective correspondence
分别是否成立？原始 correspondence counterexample 是否在不泄露 session key 的
情况下可达？

### RQ2：显式 HMAC confirmation 修复了什么，仍遗漏什么？

`hmac(confirm_key(k),sid)` 是否恢复 `RecvDone ==> SendDone`；同一诚实构造的
confirmed message 是否仍能在同一 batch/state 的两个 slot 中产生两个 accept
occurrences？

### RQ3：重复接受的安全影响到哪里？

在不把 `ReceiverAccept` 直接等同于 session installation 的前提下，显式
`C_install-v2` consumer 是否允许 one send -> two accepts -> two symbolic local
installations，并使 unique installation 失败？

### RQ4：最小修复及组合修复是否有效且非真空？

处理前的 batch-local atomic exact-message dedup 是否阻断重复 accept/output/
install，同时保留 distinct-message 正常路径；与 HMAC confirmation 组合后，
P1、batch-local P2 和 conditional P3 是否同时达到预期结果？

### 边界问题：exact-message dedup 是否等于 party admission？

RQ-v2 的回答为否。该问题用于界定修复职责，而不是重新命名 RQ2 的 replay
attack，也不扩展 M2 impact。

## 3. 建议章节结构

### 1 引言

按以下因果顺序组织：

1. K-Waay 将多种 KEM/split-KEM 组件组合到异步接收和 `BatchReceive` 中；
2. 组件机密性、消息确认、同批 occurrence uniqueness 和上层消费是不同安全层；
3. 原始 core 的 symbolic secrecy 可以成立，同时 exact correspondence 失败；
4. HMAC confirmation 修复 correspondence，但不能阻止相同 confirmed message
   被同一批次重复处理；
5. 本文给出重复接受、条件化 impact、dedup 修复和组合验证的完整证据链。

引言贡献建议列为四项：

1. ProVerif/Tamarin 分层性质与协议映射；
2. 原始 correspondence counterexample、HMAC 修复及 HMAC 后重复接受见证；
3. `C_install-v2` 下的条件化影响分析；
4. batch-local atomic dedup 及 HMAC+dedup 组合验证和可复现 artifact。

RQ-v2 的 party/message distinction 放在第四项的修复边界中，不单独取代主贡献。

### 2 K-Waay 背景与安全接口

内容：

- Figure 7 core 的 `m=(ct_l,ct_k,ct_s)`；
- `sid` 和 `k=KDF(K_l,K_k,K_s,sid)` 的符号表示；
- `BatchReceive` 的共享 receiver state、slot 与 batch lifecycle；
- 原论文安全目标与本文 symbolic events 的映射；
- distinct-party input discipline 的来源和作用边界。

本节必须明确：ProVerif 是 no-batch/single-receive abstraction；Tamarin
replay/impact 是固定两槽；两者没有一个覆盖完整 K-Waay computational game。

### 3 性质体系、攻击者与方法

#### 3.1 P0--P3 性质体系

定义 P0-S、P0-O、P1、P2 和 P3 under `C_install-v2`，说明它们不是线性安全
等级。给出各事件参数，不把不同 artifact 的事件合并。

#### 3.2 Dolev--Yao 攻击者

攻击者控制公共网络，能读取公开预密钥、重组公开可构造的 KEM 分量、重复投递
已见有效消息并安排两个 slot 的输入。各模型中未建模或被排除的 compromise 必须
逐项说明。

#### 3.3 工具分工

- ProVerif：symbolic secrecy、component origin、non-injective correspondence；
- Tamarin：state/lifecycle、same-batch replay occurrence、条件化 consumer；
- M5 artifact：结果与原始证据的机械绑定。

### 4 原始 core 的 ProVerif 分析

#### 4.1 模型与查询

介绍 `SenderKey`、`ReceiverKey`、`SendDone`、`RecvDone`、
`SplitKemAccepted` 和 `SenderSplitKemComponent`。

#### 4.2 Baseline 结果

同一张表报告：

- sender/receiver secrecy true；
- component origin true；
- `RecvDone ==> SendDone` false；
- `HonestRun` reachable。

#### 4.3 反例解释

按 `BASELINE.out` 解释 `ct_s` 复用与 `ct_l/ct_k` 重组。结论止于 exact
correspondence failure；同时明确 attacker 不得到 baseline session key。

#### 4.4 HMAC confirmation 对照

报告 `HMAC_BASELINE` correspondence/secrecy/component 结果，并说明
`HMAC_LEAK_SIGSK_A` 的负面边界。不要把 M4 Tamarin run 写成重跑这些
ProVerif targets。

### 5 Tamarin BatchReceive 与重复接受

#### 5.1 状态和生命周期建模

从 V6/V7 抽取 add/seal/process/complete/fail、state consumption、slot origin 和
close 后行为，用作 replay theory 的状态语义基础。

#### 5.2 原始 replay 反例

报告 `one_send_two_accepts_exists` verified、at-most-once/injectivity falsified、
matching/source/non-vacuity/lifecycle verified。展示 same `B,bid,rst,m,sid,k`、
distinct slot/timepoint 的事件投影。

#### 5.3 HMAC-only replay bridge

报告同一 `<m,hmac(confirm_key(k),sid)>` 通过两个 slot 的见证。强调攻击是
replay of a valid confirmed message，不是 HMAC forgery。

#### 5.4 与原规范前置条件的关系

明确 same-message 两槽 witness 不满足 distinct-party discipline。论文分析的是
该 integration/admission condition 未被维护时的行为，不能写成符合该条件的执行。

### 6 条件化 impact/composition 分析

#### 6.1 `C_install-v2`

逐项说明 C1--C8，重点突出 C7/C8：每个 successful output 独立消费是模型假设，
不是部署事实。

#### 6.2 Provenance 与安装对象

给出：

```text
ReceiverAccept
  -> AcceptOutputCreated(aid,...)
  -> InstallFromAccept(aid,h,...)
  -> InstallSession(B,h,A,sid,k)
  -> ConsumerComplete
```

区分 `sid`、`aid`、`h`。

#### 6.3 机器结果

报告 19 条 composition lemma、positive witness 与 falsified unique-install
property，引用两个 28-step trace。正文使用“conditional duplicate installation”
而不是“session cloning”。

### 7 修复设计与验证

#### 7.1 Batch-local atomic exact-message dedup

说明修复作用域、identity、decision point 和 duplicate/distinct 分支。解释为何
必须在任何 `ProcessSlot` 前作原子决定。

#### 7.2 M3 修复前后结果

以成对表格对比 original/fixed replay 与 original/fixed impact。必须同时报告
blocked witness 和 normal distinct path，防止全称性质的真空解释。

#### 7.3 HMAC + dedup 组合

说明 HMAC 修复 P1、dedup 修复 scoped P2/P3，两者职责不同。报告
same-base/different-tag rejection、distinct confirmed completion、slot-2 mismatch
after slot-1 accept 的边界。

#### 7.4 RQ-v2 边界检查

用 `same_party_different_messages_batch_exists` verified 说明 exact-message dedup
不维护 distinct-party invariant。该小节只得出“还需独立 party admission
obligation”，不得引用 M2 installation trace作为同方不同消息后果。

### 8 实验与可复现性

建议分开报告：

- ProVerif 原始/HMAC summaries；
- M1 单次完整 Tamarin proof 与 selected trace；
- M2 sequential-per-lemma 37/37 terminal；
- M3 196-target transparent composite；
- M4 296-target Tamarin-only transparent composite；
- M5 405-row result contract、claim matrix 和 checksum validation。

对 M3/M4 必须写清：composite terminal 结果不是任何一次 source run 单独完成的
全终态结果。

### 9 讨论

建议围绕四个边界展开：

1. secrecy/component origin 与 complete correspondence 的区别；
2. confirmation 与 replay prevention 的区别；
3. duplicate accept 与 conditional installation 的区别；
4. exact-message dedup 与 distinct-party admission 的区别。

本节适合讨论修复放置点，但不能声称某个真实实现遗漏检查。

### 10 局限

集中列出：

- symbolic/free-constructor abstraction；
- fixed two-slot；
- same-batch/same-state、batch-local exact-message scope；
- no rollback/restart/cross-batch/global theorem；
- HMAC compromise coverage 不完整；
- `C_install-v2` 与部署缺少映射；
- 没有真实 session database、Double Ratchet/application action；
- M0--M5 与 RQ-v2 的事件语义不可拼接；
- 不证明 computational KIND、UNF-1KMA、IND-1BatchCCA。

### 11 相关工作

围绕 symbolic AKE verification、explicit key confirmation、replay and
injective agreement、batch/group admission、protocol composition 和
post-quantum messaging 展开。避免把一般 authentication hierarchy 或 message
dedup 概念本身声称为新贡献。

### 12 结论

结论按四句话收束：

1. 原始 symbolic core 的 secrecy 与 component origin 成立，但 exact
   correspondence 失败；
2. HMAC confirmation 修复 correspondence，却不阻止同批 confirmed-message
   replay；
3. 该 replay 在 `C_install-v2` 下有条件化重复安装影响；
4. processing 前的 batch-local atomic dedup 与 HMAC 组合后阻断相应 witness，
   但仍需独立维护 distinct-party invariant。

## 4. 当前 Stage 6 内容的迁移方式

| Stage 6 内容 | 新论文位置 | 处理方式 |
| --- | --- | --- |
| K-Waay `BatchReceive` 和 distinct-party 来源 | §2 | 保留并与原始 core 背景合并 |
| R/M/P 模型 | §7.4 | 从论文主线降为修复边界对照 |
| relaxed one-send/two-accept 图 | §5 或 §7.4 | 必须标明它属于当前 RQ-v2 事件语义；不得替代 original replay trace |
| same-party/different-message witness | §7.4 | 保留为 dedup 非替代性证据 |
| party admission positive control | §7.4 | 保留为 distinct-party invariant 的单独 restoration control |
| 当前 14 项 RQ-v2 结果 | 附表或 §7.4 精简表 | 保留原状态，不与 M0--M5 结果计数合并 |
| 当前 discussion/limitations | §9--§10 | 复用身份层次与边界表述 |

不能直接把 Stage 6 的 `ReceiverAccept(A,oid,m,bid,rst)` 与历史 replay 的
`ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` 视为同一事件，也不能把 Stage 6 的
13 verified / 1 falsified 合并进 M4 的 296-target 统计。

## 5. 建议核心表格

1. 协议对象到 ProVerif/Tamarin 事件映射表；
2. P0--P3 性质和依赖边界表；
3. original / HMAC-only / dedup-only / HMAC+dedup 结果矩阵；
4. M2/M3/M4 impact 对照表；
5. RQ-v2 message-vs-party boundary 小表；
6. artifact 与 trace 索引表。

完整 405-row actual table 放 artifact，不应塞入正文。

## 6. 投稿定位是否被证据缺口阻止

### 可以成立的定位

“K-Waay 的符号安全边界、批内重复接受、条件化 impact 和互补修复”已有完整证据
支持。其研究增量来自跨层性质分离、实际 counterexample、HMAC 后 replay 见证、
显式 composition impact、修复前后机器对照和透明 artifact，而非单独重述某个
前置条件。

### 不能成立的定位

以下定位会被现有证据缺口阻止：

- “K-Waay 规范本身存在可利用的 duplicate-batch 漏洞”；
- “真实实现会从一个发送建立两个会话”；
- “M3/M4 解决所有 replay”；
- “组合模型证明完整 K-Waay 或计算安全”。

最关键的外部缺口是 `C_install-v2` C7 与真实规范/实现消费行为之间的映射。
若后续能得到可靠规范或实现证据，impact 叙述可进一步加强；若得不到，保留
conditional 即可，当前论文仍然成立。

## 7. 写作启动条件

恢复论文写作前只需要人工确认本文定位和章节顺序。模型、lemma、trace、结果和
artifact 均已冻结，不应因本次结构恢复而重跑或修改。

