# K-Waay：从当前仓库到可投稿模型的路线图

更新时间：2026-07-13

## 1. 总判断

当前项目已经完成了“基础模型与若干独立结果”，但还没有完成“单一、闭环、可投稿的安全故事”。

最适合把现有成果收束起来的主线是：

```text
原始 Figure 7 core
  ├─ symbolic secrecy / component origin 成立
  ├─ full-parameter non-injective correspondence 存在缺口（Q1）
  └─ BatchReceive 允许 one-send → many-accepts（injectivity / replay 缺口）

HMAC confirmation
  ├─ 修复 Q1，对 sid/key 的非单射 correspondence 恢复
  └─ 预计仍不能阻止同一已确认消息被多个 slot 重复接受

HMAC confirmation + batch-local duplicate rejection
  ├─ 恢复单射接受 / one-send-one-accept
  ├─ 阻止重复 session installation
  └─ 保持 secrecy、component origin、batch lifecycle 与 compromise 边界
```

这条主线能把已经做完的 ProVerif core、HMAC 变体、Tamarin batch lifecycle 和新 replay 反例串成一个贡献，而不需要继续扩展“通用 Q1 检测器”。

## 2. 状态图例

- ✅：已有模型、运行结果和可引用证据。
- 🟡：已有部分材料，但还不能作为论文定稿证据。
- ⬜：尚未完成，是后续任务。
- ⛔：有意冻结或移出论文主贡献，不再继续扩展。

## 3. 模型总表

| 阶段 | 任务 | 状态 | 当前证据 / 缺口 | 之后怎么做 | 完成判据 | 投稿作用 |
|---|---|---:|---|---|---|---|
| 0 | 冻结论文主问题 | 🟡 | 仓库中已有多条支线，但还没有一份正式的 claim hierarchy | 固定为“secrecy → non-injective agreement → injective agreement → composition impact → combined repair” | `docs/claim-hierarchy.md` 明确主张、非主张、模型与查询 | 防止继续无限补模型 |
| 0 | 通用 Q1 模型作为主贡献 | ⛔ | 已有通用模板，但参数依赖协议映射，不能宣称适用所有协议 | 只保留为内部诊断器 / artifact 辅助材料 | 正文最多一段说明，不再扩展协议族 | 避免稀释论文贡献 |
| 1 | ProVerif final core | ✅ | `proverif/kwaay_core_final.cpp.pv` 已运行；baseline secrecy true、component authenticity true、`RecvDone ==> SendDone` false | 不再新增功能，只做回归与文档同步 | 固定 commit、版本、命令和结果表 | 论文 baseline |
| 1 | Tamarin receiver/batch lifecycle | ✅ | V6/V7 已覆盖 compromise、slot、abort、state consumption、fixed 4-slot terminal lifecycle | 将 V6 与 V7 的职责写清，不再追求任意长度 batch | 所有选定 lemma 一键复现，论文不夸称 arbitrary-length | 状态语义支撑 |
| 1 | Paper ↔ model mapping | 🟡 | `docs/model-mapping.md` 已存在，但仍写着 deniability 未建模，且未纳入 replay/HMAC 新分支 | 更新协议对象、事件、查询、假设、结果、文件路径 | 每个论文 claim 都能指向唯一模型和 lemma/query | 审稿可信度 |
| 1 | Threat / compromise matrix | 🟡 | core 和 V6 有多种 compromise 实验；HMAC 仅跑 baseline/component/单一 sig-key leak | 建表区分 no-compromise、early/late compromise、sender/receiver state、长期密钥 | 每个 theorem 都有明确前提；不把 experiment 当 theorem | 防止过度声称 |
| 1 | 清理 model drift | ⬜ | `LEAK_SIGSK` 与旧 ledger 预期不一致；根 README 仍把项目描述为早期 no-batch 模型 | 先判断结果是建模变化还是 bug，再更新预期/模型；同步根 README | 无未解释的结果漂移；README 与当前仓库一致 | artifact 基线质量 |
| 2 | K-Waay 专用 Q1 诊断 | ✅ | `KWAAY_LIKE / ATTACKER_KEY_BAD / AUTHZ_BAD / CONFIRMED_FIX` 已运行 | 仅作为理解和回归材料；主论文使用 final core/HMAC 的真实查询 | 不再依赖模板结果支撑 K-Waay 主 claim | 辅助解释危害边界 |
| 2 | 原始 core 的 non-injective agreement gap | ✅ | final core 中带 A/B/sid/key 的 `RecvDone ==> SendDone` 为 false | 导出并人工解释最小 trace，确认事件位置和会话绑定 | trace 中每个攻击步骤都能对应 Figure 7 对象 | 既有安全边界 |
| 2 | HMAC confirmation 修复 non-injective correspondence | ✅ | HMAC baseline 中 correspondence、secrecy、component authenticity 为 true | 保留为“confirmation 修复 Q1”，不要称为 replay 修复 | baseline 与至少必要 compromise case 可复现 | 第一层修复 |
| 2 | HMAC 下的 duplicate acceptance / injectivity | ⬜ | 当前 HMAC 模型没有 batch slot，也没有 one-send-many-accept query | 建一个 `hmac-only` 两 slot Tamarin 变体：同一完整 confirmed message 输入两个 slot | `one_send_two_accepts_exists` verified；non-injective correspondence 仍成立；injective agreement falsified | 把现有 HMAC 与 replay 主线接起来 |
| 3 | 原始 BatchReceive 重复接受 | ✅ | `tamarin/replay/kwaay_replay_original.spthy` 已证明 same message 在同一 state/batch 的两个不同 slot 被接受；无 compromise；batch 正常 complete | 冻结 original 模型，不在其中加入 impact 或 repair | 攻击存在性、唯一 send、distinct slots、lifecycle sanity 全部自动完成 | 新问题的协议层证据 |
| 3 | 跨 batch / close 后 replay 边界 | ✅ | 当前模型已证明 receiver state 单 batch、close 后无 accept；反例限定为同一 batch duplicate input | 在论文中明确这不是 rollback、cross-batch replay 或 state reuse | attack scope 一句话可准确复述 | 避免夸大 |
| 4 | 组合接口定义 | ⬜ | 目前只证明“重复输出”，没有证明上层影响 | 单独建 `impact` 模型；定义 `ReceiverAccept -> InstallSession`，每个 accept 创建 fresh local handle | 接口假设写清楚，模型不假装是未知实现代码 | 将问题从异常行为提升为安全影响 |
| 4 | Session-clone / duplicate-install trace | ⬜ | 尚无 `InstallSession` / `Action` 事件 | 证明一个 send 导致两个不同 local session handles，二者共享 sid/key；可再加条件化 `Action` | `one_send_two_installs_exists` verified；`unique_install` falsified | 论文影响证据 |
| 4 | 影响与 K-Waay 规范的对应 | ⬜ | 尚未确认 Figure 7 输出列表之后如何被消费 | 从论文文字/接口说明中找 output list、session creation、Double Ratchet 或上层调用；找不到时明确写成 conditional composition result | 每个影响 claim 要么有规范引用，要么带显式“若上层逐项安装”前提 | 决定能否冲高水平安全会 |
| 5 | 修复语义选择 | ⬜ | 还未决定 duplicate 时整个 batch fail、跳过 slot，还是复用第一次结果 | 首选：处理前对完整 message 或 sid 做 batch-local distinctness 检查；重复则在输出任何 key 前原子地 `BatchFail` | 修复伪代码无 partial output，且与现有 fail/complete 语义一致 | 最小协议修复 |
| 5 | Fixed Tamarin model | ⬜ | 没有 `SeenMessage/SeenSid` 或 distinctness precheck | 建 `tamarin/replay/kwaay_replay_fixed.spthy`，保持 original 的其余规则与事件坐标不变 | normal distinct batch reachable；duplicate batch 不能产生两个 accept | 修复实现 |
| 5 | 修复 one-send-many-accepts | ⬜ | 尚无修复后证明 | 验证 `same_message_accepted_at_most_once` 和 injective sender/receiver correspondence | 两个安全 lemma VERIFIED，且有非空正常 trace | 核心修复结论 |
| 5 | Combined fix：HMAC + dedup | ⬜ | HMAC 与 replay 当前分离 | 建 combined 变体，证明 Q1 与 injectivity 同时恢复 | non-injective correspondence true；injective agreement true；duplicate install 不可达 | 最强、最完整的修复故事 |
| 5 | Regression matrix | ⬜ | 修复尚未对既有性质回归 | 在 original / HMAC-only / dedup-only / combined 四列运行统一查询 | secrecy、component origin、lifecycle、fail/complete、state consumption 不退化 | 证明修复没有破坏原性质 |
| 5 | 修复 compromise assumptions | ⬜ | HMAC 只有一个 leak case，dedup 尚无 compromise 分析 | 只选择与论文 claim 有关的最小 compromise 集；区分认证密钥泄露与 receiver state 泄露 | 每个修复 theorem 的例外条件明确且能复现 | 防止“只在理想模型有效”质疑 |
| 6 | Symbolic deniability core diff | ✅ | core equivalence VERIFIED；negative sanity 为 EXPECTED_NON_EQUIV | 保留为强化贡献，不让它阻塞 replay 主线 | core/negative 两个结果可复现 | 可选第二贡献 |
| 6 | Malicious PoK deniability | 🟡 | executability/witness lemmas verified，但 observational equivalence TIMEOUT | replay 闭环完成后再缩减 proof search 或拆小模型 | equivalence VERIFIED，或明确降级为 limitation | 高目标强化项 |
| 6 | Big Brother / full deniability | ⬜ | 尚未完成 | 仅在主线冻结后继续 | 明确 game、opening data、simulator 与 result | 不作为当前模型冻结前置条件 |
| 7 | Computational proof sketch | ⬜ | 尚无 CryptoVerif / game proof | 对 AsiaCCS/ACNS 可先放 future work；若冲 USENIX/密码方向，再补最小 KDF hybrid / KIND sketch | 假设、game hop、symbolic↔computational边界成文 | 高目标加分，不替代影响闭环 |
| 8 | 一键复现 artifact | 🟡 | 各分支有脚本和日志，但缺一个统一入口与总结果清单 | 新增 `scripts/run-paper-artifact.sh`，固定工具版本、timeout、预期 true/false/trace | 干净环境一条命令得到完整表；失败有非零退出码 | 投稿硬要求 |
| 8 | Artifact README / claim matrix | ⬜ | 根 README 过时，结果散在多个 docs/logs | 写 installation、模型索引、预计时间、结果表、限制、论文 claim 对应 | 陌生审稿人 15 分钟内能运行一个核心结果 | Open Science / 复现性 |
| 8 | 最终模型冻结 | ⬜ | 仍有新增分支和陈旧文档 | 打 tag/commit；主模型只保留 original、hmac-only、impact、fixed/combined；历史实验归档 | 冻结后只修 bug，不再改变事件定义/安全目标 | 开始写论文的门槛 |

## 4. 必须按顺序执行的里程碑

### M0：冻结主张与命名

产物：

```text
docs/claim-hierarchy.md
docs/threat-compromise-matrix.md
```

必须写清：

```text
P0 secrecy / component origin
P1 full-parameter non-injective correspondence
P2 injective one-send-one-accept
P3 unique session installation under an explicit composition interface
```

完成后才允许新增模型。

### M1：建立 HMAC-only replay bridge

目的：证明“key confirmation 修复 Q1，但本身不提供 freshness / replay prevention / injectivity”。

核心结果：

```text
HMAC-only:
  correspondence = true
  one-send-two-accepts = reachable
  injective agreement = false
```

这是把旧工作与新重复接受结果连接成一篇论文的关键步骤。

### M2：建立 impact/composition 模型

只加入最小接口：

```text
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
    -> InstallSession(B,handle,A,sid,k)
```

要求两个 `ReceiverAccept` 产生两个不同 `handle`。先证明 session clone，不必一开始模拟完整 Double Ratchet。

完成标准：

```text
one send -> two accepts -> two installs
same sid / same key / distinct local handles
```

### M3：建立 batch-local atomic dedup 修复

推荐修复语义：

```text
BatchReceive 在产生任何输出前检查输入完整消息（或其 sid）两两不同；
若发现重复，整个 batch 失败且不产生部分 key 输出。
```

优先选择 pre-scan，而不是“处理到第二个重复项才失败”，因为后者可能已经输出第一个 key，形成 partial-output 语义。

### M4：完成 combined fix 与统一回归

用同一组性质比较：

| 性质 | Original | HMAC only | Dedup only | HMAC + dedup |
|---|---:|---:|---:|---:|
| symbolic secrecy | 预期 true | 预期 true | 必须 true | 必须 true |
| component origin | 预期 true | 预期 true | 必须 true | 必须 true |
| non-injective exact-parameter correspondence | false | true | 预计仍 false | true |
| one-send-one-accept / injectivity | false | false | true | true |
| unique session install | false | false | true | true |
| batch lifecycle / atomic close | true | true | 必须 true | 必须 true |

实际模型结果如与“预期”不同，先解释原因，不能直接改查询去迎合表格。

### M5：Artifact freeze

必须具备：

```text
一个总入口脚本
一个工具版本文件
一个 expected-results 表
original/impact/fixed 的自动 trace 或 lemma 结果
paper ↔ model ↔ query 映射
所有 known timeout / limitation 的显式记录
```

达到 M5 后，模型才算“可以开始写投稿论文”。

## 5. 投稿门槛

### AsiaCCS / ACNS / Journal of Computer Security 等现实目标

不可缺少：

```text
M0 + M1 + M2 + M3 + M4 + M5
```

即：原问题、条件化影响、最小修复、修复证明、回归和可复现 artifact 必须闭环。Deniability 与 computational proof 可作为强化或 future work。

### USENIX Security / 更高目标

除上述全部内容外，还应至少补强一项：

```text
1. 用 K-Waay 规范或实际集成方式支撑 session-install impact；或
2. 更完整的 malicious deniability；或
3. computational proof sketch；或
4. 对相邻协议/实现进行系统性对照，说明该 batch injectivity 问题不是纯 toy artifact。
```

仅有 symbolic counterexample 和简单去重修复，通常不足以支撑高水平系统安全投稿。

## 6. 每次工作的停止规则

为避免做到一半忘记后续，每次只做一个里程碑，并在结束时更新这四项：

```text
状态：⬜ / 🟡 / ✅
证据：模型路径 + query/lemma + 日志路径
结论：能声称什么 / 不能声称什么
下一步：唯一的后继任务
```

任何任务只有同时满足以下条件才能打 ✅：

```text
模型存在
查询定义正确
工具实际运行完成
结果符合或明确修正研究判断
非空性 / executability 检查通过
文档记录假设和限制
可由脚本复现
```

## 7. 当前唯一下一步

当前不要先写论文正文，也不要继续扩通用 Q1 或 Big Brother 模型。

唯一下一步是 M0，然后立即做 M1：

```text
先冻结 claim hierarchy；
再建立 HMAC-only 两 slot replay 模型，验证 confirmation 是否仍允许 one-send-many-accepts。
```

只有完成 M1，才能确认现有 Q1/HMAC 工作与新 replay 结果是否能组成同一条论文主线。

## 8. Venue 规格依据

- USENIX Security 2027 要求 finished, complete papers，正文上限 13 页，并要求 Open Science appendix 与投稿 artifact；范围包括安全协议和已部署密码协议分析：<https://www.usenix.org/conference/usenixsecurity27/call-for-papers>
- ACM AsiaCCS 2027 包含 Formal Methods 与 Applied Cryptography track，要求结果对一般安全研究者可理解且有实际安全联系；正文上限 12 页，并要求 Open Science appendix：<https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html>
- ACM TOPS 强调对安全/隐私系统的构造、评估、应用或运行具有实际相关性：<https://dl.acm.org/journal/tops/author-guidelines>
