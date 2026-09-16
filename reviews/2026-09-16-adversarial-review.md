# K-Waay BatchReceive 论文匿名审稿报告

审查日期：2026-09-16。审查对象：**Party Identity in Batch Admission: A Formal Study of K-Waay BatchReceive**，当前 `main` 提交 `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57`，29 页成稿，包含全部正文、图表与附录。以 `manuscript/` 为论文正文；`docs/paper/` 为写作材料，RQ-v2 authority、历史模型和 archive 为辅助证据，不能倒过来替代当前论文。

审查方法：完整阅读成稿与 LaTeX 正文；逐条检查三个 RQ-v2 模型的规则、restriction 和全部 14 个 lemma 实例；核对原论文全文中的 §3.1、§4、§5.1–5.2、Fig. 5、Fig. 10；检查历史 replay/impact 模型、README、结果和 archive 的证据角色；独立运行当前三个未改动模型，保存原始输出与 JSON traces。不是对 M0–M5 全部历史目标的重新认证，也不是对所有引用文献的逐定理复核。本轮没有修改论文、模型、原日志、旧结果或 Git 历史。

**独立复核结果：14/14 个结果及步数与成稿一致，13 verified，1 falsified with trace；三模型 parse 与 wellformedness 均通过。** 这显著削弱了“结果可能只是手填且不能复现”的质疑，但没有弥补从抽象模型到协议安全意义的论证缺口。

新证据见 [独立复核包](D:/kwaay-formal/reviews/2026-09-16-evidence/README.md) 和 [运行清单](D:/kwaay-formal/reviews/2026-09-16-evidence/independent-rerun-manifest.json)。复核开始与结束时工作树均干净；随后仅新增本报告和审查证据目录。

---

## 1. Overall Verdict

**Reject。** 这是按密码学／协议安全／形式化验证研究论文的标准作出的判断；没有指定会议，不能据此预测某一 workshop、工具案例短文或教学栏目必然拒稿。

核心理由如下：

1. **已经正确识别的原文前置条件，没有被转化为足够有新意的研究问题。** “不同消息可能属于同一 party”及“检查 party 不等可保持 party 不等”成立，但本身是直接的关系性质。当前生命周期的增加还没有产生一个独立于这些定义的、K-Waay 特有的难点或安全后果。
2. **所谓 receiver-side consequence 仍主要由抽象接口决定。** 接收规则读取全局持久 `!Sent(A,sid,m)`，按每个槽发出一次 `ReceiverAccept`；省去了接收者身份、目标 prekey/state、密码检查、输出 key 和最终 vector 的解释。模型结果正确，不等于已经解释了原协议中的 receiver acceptance。
3. **最强核心结果是模型内的非蕴含，而不是 identity binding 或 AKE 安全失效。** M 模型中两次接受各有各的正确来源，没有 peer mismatch、密钥泄露、UKS 或错误的身份归属。R 模型的非单射是作者定义的同批次 occurrence property 失败；原文没有承诺这一同构事件性质。
4. **形式化结果之间的依赖比贡献叙述呈现得更紧。** 在当前 freshness／origin 假设下，accepted message distinction 与 scoped occurrence injectivity 等价；把二者并列为同时保持的两项保证，会放大中间对照的独立信息量。
5. **材料仍存在研究定位与证据发布问题。** 成稿把 M 模型的 separation 升为核心贡献，所谓 canonical authority 仍把它明确降为辅助、把 necessity 定为最终贡献。原提交只有结果转录，没有 raw transcripts；本次已补出独立复核证据，但作者仍需明确整合新证据和统一主张。

我不会以当前版本并未声称的“攻破 K-Waay”“发现漏写 uniqueness”“验证 full AKE”来拒稿。当前稿在限制性表述方面已经相当审慎。拒稿的主要依据是**研究贡献与协议关联不足，而非发现 Tamarin 给出了错误结果**。

## 2. Paper's Actual Contribution

### 2.1 核心逻辑链及每一步的证据

| 逻辑环节 | 当前可支持的内容 | 证据／缺口 |
| --- | --- | --- |
| 原协议／原规范 | 一次 `BatchReceive` 的元素应对应不同 party | 原全文 §5.1，p.21，Fig.10 后明确写出；不是本文发现的新条件 |
| batch semantics | 一个 receiver ephemeral state 对应一次批处理；输入、输出为向量 | 原文 §4.1；花括号记法不能推翻明确的 vector 类型 |
| party interpretation | 用符号 `A` 表示 protocol principal，区分 party、session、message、slot | 原文提供 principal 角色；具体 `party(pk,prek,m)` 解析关系在模型中假定存在 |
| same party 是否能多次出现 | 原协议合规同批次输入不允许；同一 party 可以有多个 session | 不能将多 session 的合法性偷换成同批次多 entry 的合规性 |
| 建模差异 | R 无不等式；M 检查消息；P 检查 party | sender、collect、process 共用；M/P 还增加拒绝分支和标准不等式 restriction |
| Tamarin witness | R 有单一匹配 origin 被接受两次；M 有同 party 的两条不同消息均被接受 | 本次独立复核确认，含机器导出 graph |
| 被破坏性质 | R 的 batch-local exact-origin injectivity；R/M 的目标 party-distinction | 不是原协议的计算安全性质，也不是完整的 Lowe injective agreement |
| 对 K-Waay 的实际含义 | 若一个集成边界承诺原文的不同 party 条件，仅凭消息不等不能推得该条件 | 尚无具体集成、可实现 identity projection、协议输出或 game refinement 支持更强结论 |
| 修复／建议 | 指定哪一层负责维护 party relation；P 为直接实现这一条件的正控制 | 不是修复原文漏写的要求，也未验证实际代码或部署策略 |

因此，目前真正完成的是：**对一个有原文动机的、固定两槽、具有理想来源关系的 admission 模型，验证三种规则的行为差异。** 它是一项正确但很小的形式语义案例分析。

### 2.2 A–E 分类

这些类别不是从弱到强的单一序列：规范是否明确、证明是否依赖、系统是否被攻破，是不同维度。

| 候选定位 | 结论 |
| --- | --- |
| A. K-Waay 存在安全漏洞 | **Unsupported**。没有合规执行中的密码学失败或真实集成攻击 |
| B. BatchReceive 存在 identity／party ambiguity | 对“是否要求 distinct parties”而言不成立；对“部署如何解析 party、谁执行检查”而言有未具体化之处，但尚未证明一个冲突解释导致安全后果 |
| C. 证明依赖未陈述的 distinct-party assumption | **不能成立为当前结论**：该条件已明确陈述。可以研究它在游戏索引和 proof 中的具体作用，但本文未完成这一研究 |
| D. 缺少 admission rule 破坏 security property | **仅支持限定的 D_model**：去掉目标 guard，在共同抽象中相应不变量或局部 occurrence property 可以失败；不能扩大到任意实现或原 AKE 安全 |
| E. 更强 identity-distinction property 在当前协议下不成立 | **只能支持“在 relaxed/M 抽象中不成立”**。它在 P 模型成立，而且与原文前置条件一致；不能写成合规 K-Waay 本身不满足 |

### 2.3 贡献评级

“评级”衡量可发表研究贡献，不是将 formal validity 和 novelty 混成一个布尔值。

| Contribution | 评级 | Formal evidence | Original-paper evidence | 新颖性及包装边界 |
| --- | --- | --- | --- | --- |
| C1. 精确定位原文的 distinct-party 条件 | Weak | 不需要 prover | 强，明文 | 是忠实阅读，不是发现缺失要求 |
| C2. 区分 party/message/occurrence/slot/batch | Weak | 类型与 tuple 编码清楚 | 原文 principal/session/vector 提供背景 | 概念本身已有；应用到本接口的教学价值不能自动变成新理论 |
| C3. M 保持消息区分和 scoped injectivity，但不能保持 party 区分 | Moderate（模型结论）；Weak（目前研究增量） | 独立复核确认 | 原文没有提出“消息去重可替代 party 条件” | 是最扎实结果，但对照方案为何值得反驳缺乏外部依据 |
| C4. R 的 one-origin/two-accept witness | Moderate（模型证据） | 存在性和否定性检查一致 | 不在原协议规定域内 | 不能包装为认证攻破；行为高度依赖 origin fact 和按槽事件定义 |
| C5. 明确集成层的 admission responsibility | Weak | 没有实现／refinement | 条件存在，具体责任层未给出 | 合理设计建议；不是已验证的新协议修复 |
| C6. P 的安全与非空执行 | Moderate（验证完整性）；Weak（新颖性） | safety＋有效两次接受 witness | 实现已陈述条件 | 正控制合格；不证明必要性、最小性或唯一机制 |
| C7. K-Waay 密码学漏洞／漏写假设／协议级修复 | Unsupported | 当前无相应对象和性质 | 明文条件反对“漏写”定位 | 当前成稿已否认，后续不得从旧材料重新引入 |

本轮有限的定向文献检索不能认证“首个”或穷尽性新颖性；报告不声称已有某篇论文逐字做过同样案例。研究增量不足的判断，首先来自当前结果可直接由建模定义推出，而非搜索未命中。

## 3. Strongest Part of the Paper

最强部分是 **M 模型的真实、可复现 separation witness**，以及作者对其边界的明确说明。

同一 `!Party(A)` 可支持两个 `SendMessage`；每次生成新的 `sid,m`；M 的 admission 条件允许 `m1 != m2`；两条 origin 都真实存在；两个接受各自匹配完整 tuple，却仍有相同 `A`。这不是假冒、不是 originless acceptance，也不是“无法证明便当作 falsified”。

此外，P 的 `distinct_party_batch_exists` 确实绑定了两个 distinct parties、两个 Send、同一 batch 和两个接受事件；没有靠拒绝所有输入获得 vacuous safety。R 的存在性反例与否定 injectivity 查询也相互吻合。

证据：[M 模型](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_message_dedup.spthy:92)、[P 非空查询](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_party_admission.spthy:96)、[新 M 原始输出](D:/kwaay-formal/reviews/2026-09-16-evidence/rqv2_message_dedup-prove.stdout.txt:451)。

## 4. Most Dangerous Claim

当前最危险的实际表述不是“协议被攻破”，而是 **§5.4 与 §6.1 将结果定位为超越 guard removal 的、protocol-specific 的实质分析**。

定位：[§5.4，219–257 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:219)、[§6.1，15–47 行](D:/kwaay-formal/manuscript/sections/06-discussion.tex:15)。

最强质疑是：

> 将两个 tuple 交给两个顺序处理规则，每条规则凭可复用的来源事实输出一次事件；再分别比较 tuple 的 message 或 party 字段。这样的完整 trace 并未引入 K-Waay 特有的密码学、状态或接口约束。为什么这不是一个关于投影函数和列表元素的基本示例？

“完整 trace”“非空性”“14 个 verified/falsified 结果”可以证明代码如定义运行，却不能单独回答这一贡献问题。尤其 `receiver_accept_has_send` 的来源关系直接由处理规则前提提供；它不是一项额外攻防分析得出的认证保证。

应将当前结果定位为**受限抽象中的坐标非替代性**，或者增加一个独立而非定义重述的对象：例如 party-indexed output 的定义性、原协议输出关系、可审计 caller contract。不能只增加“not a cryptographic break”之类免责声明来弥补研究增量。

## 5. Fatal Issues

**对当前已收缩的模型内结论，本轮没有发现可证实的数学致命错误。** 三个模型的结果可复现；restriction 使用公开；对应事件与量词的解释大体一致。为了达到“严格”而虚构 fatal bug，会误导后续修订。

但有一个**对更强论文定位具有致命影响的缺口 F1**：没有从模型事件到 K-Waay 安全对象的连接证据。

- **问题**：没有输出 key、peer agreement、真实 sid 构造、KIND 的 `KEY/TEST`、或实现级 admission。`!Sent` 不包含目标 receiver 或其 prekey/state，`rst` 只由 `CreateBatch` 新生成，Send 与该状态没有协议依赖。
- **位置**：[§4.1，43–68 行](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:43)、[R Send/CreateBatch，17–35 行](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_relaxed.spthy:17)、[R 接受，58–72 行](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_relaxed.spthy:58)。
- **影响**：凡是把结果升级为 K-Waay identity-binding weakness、原 proof assumption mismatch、真实 duplicate key installation 或 AKE failure 的主张，都无法成立。当前正文承认这一边界，所以 F1 **不是对现有窄命题的反驳**。
- **修改**：坚持窄命题并重新评估文章体量／类型；或先建立 source-to-model 的关系和独立安全目标，再验证更强主张。不能从 archive 的同名 lemma 直接借取这条连接。

**真正支撑本轮 Reject 的是下列 Major Issues 中的研究增量不足。** 一个命题正确并不保证其具有足够发表价值；这与证明不正确是两类拒稿理由。

## 6. Major Issues

### M1. 研究问题和正控制的答案过多地由定义决定

- **问题**：RQ1 移除 party 不等约束；RQ3 比较 message 不等能否推出 party 不等；P 再直接强制 party 不等。模型允许同一 party 自由地产生新消息后，关键答案已基本确定。新颖性需要解释“为什么这里的 relation 值得研究”，不能停在“relation 确实是另一个 relation”。
- **严重性**：这是最可能的主拒稿理由。即使全部模型与日志完美，也不能自动获得实质研究贡献。
- **位置**：[§2.5](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:186)、[Introduction contribution](D:/kwaay-formal/manuscript/sections/01-introduction.tex:45)、[§5.4](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:217)、[§6.1](D:/kwaay-formal/manuscript/sections/06-discussion.tex:15)。
- **影响 claim**：C2/C3/C5/C6 的原创性与重要性。
- **修改**：寻找与 party projection 不同的独立结果谓词，并论证其协议相关性；或者承认这是短篇形式语义案例。说明为何 message-level replacement 是已有实现、标准解释或非平凡候选，而不是由作者为获得非蕴含自行设置的靶子。

### M2. K-Waay 的接收条件被理想 origin oracle 替代，且丢失 receiver/context binding

- **问题**：`SendMessage` 没有 recipient、receiver prekey、receiver state。任一已发送 tuple 能在任一新建 batch 中满足 `!Sent`。`ReceiverAccept` 不是来自 KDF／验证运算，而是来自数据库式 origin 查询。一个真实消息能否在该 `rst` 下解封装，这个问题在当前模型中根本不存在。
- **严重性**：这既可能排除真实协议行为，也可能允许不可实现的接受。不能把它当作天然保守的 over-approximation；没有 simulation/refinement 证明，就不能保证抽象反例能提升回协议。
- **位置**：[模型映射表](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:31)、[R 模型](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_relaxed.spthy:17)。
- **影响 claim**：协议特异性、实际 batch-processing consequence、任何 identity/session binding 结论。
- **修改**：若要提升协议关联，明确投影与适用输入域，至少保留 recipient/prekey/context 的关联并解释原文的 batch-wide failure 和输出边界。无需为一个窄命题强迫重建全部 KEM，但必须说明保留了哪些与命题相关的真实约束。

注意：单纯把 `!Sent` 改为线性事实以消灭 replay 并非正确修复；那会人为加入消费一次语义。必须先由协议说明决定事实应否可复用。

### M3. message distinction 和 scoped injectivity 在当前抽象里不是两项独立证据

令 `Mτ` 表示某条 trace 中，同一 `(bid,rst)` 的不同接受事件具有不同 `m`；`Iτ` 表示正文的 exact-tuple scoped injectivity；`Pτ` 表示接受事件之间的 party distinction。在当前 sender／processing 规则下：

\[
P_\tau\Rightarrow M_\tau\Longleftrightarrow I_\tau,\qquad M_\tau\not\Rightarrow P_\tau.
\]

这是**基于规则的人工推导，不冒充新 Tamarin lemma**：

1. `Mτ ⇒ Iτ`：两次接受如果 tuple 全同，就具有相同 `m`；消息区分迫使它们是同一事件。
2. `Iτ ⇒ Mτ`：每次 Send 的 `m` 全局 fresh；每个接受均需对应 `!Sent`。因此两次接受的相同 `m` 必定对应相同 `A,sid` 和唯一 Send；该 Send 早于两次接受，满足 I 的前提，故只能是同一事件。
3. `Pτ ⇒ Mτ`：相同消息的两个已接受 origin 同属一个 party，与 P 冲突。
4. M 的两次不同 Send witness 证明最后的非蕴含。

- **位置**：[§4.4 freshness discussion](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:202)、[§5.4 中心 separation](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:233)、[§6.2](D:/kwaay-formal/manuscript/sections/06-discussion.tex:49)。
- **影响**：中心结果仍正确，但“同时维持两个保证”的独立性、三维分离的新颖性被高估。当前稿没有声称完全逻辑独立，因此这不是形式矛盾。
- **修改**：明确这一模型内蕴含结构；不要将 14 行结果当作 14 个独立发现。若要讨论不同 message/occurrence 概念在真实协议中的区别，应给出更忠实的消息与 sid 构造，并重新验证相应关系。

### M4. 缺少“原游戏到底在哪使用 distinct-party”的实质分析

- **问题**：引用 p.21 解决“条件来自哪里”，却没有解释“这个条件为何对该 DAKE formalism 有意义”。原游戏以 `j` 选择 receiver 的 `k_j`，`KEY(i,s,j)` 和 `TEST(i,s,j)` 都使用 party 坐标；proof 也选择与测试 party 对应的 component。这个接口比 `A != A` 更接近真正的研究问题。
- **严重性**：作者用一般语义对照替代了本应最具 K-Waay 特异性的分析；目前未证明 cryptographic necessity，也未证明 duplicate-party 域内如何定义输出选择。
- **位置**：[§2 背景](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:10)、[§4 映射](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:22)、[§6 设计讨论](D:/kwaay-formal/manuscript/sections/06-discussion.tex:139)。仓库已有 [security-interface discussion](D:/kwaay-formal/docs/rq-v2/security-interface-dependency-analysis.md)，但明确只属概念层。
- **影响**：研究动机、necessity、protocol-specific contribution。
- **修改**：从向量位置到 party-indexed component 定义一条精确关系；区分唯一选取、任意选取、slot-indexed 扩展等语义，并说明哪些是原文、哪些是自定义扩展。发现扩展需要新规则不等于原文证明错误；现在不能先写结论再让模型支持它。

### M5. 两条 rejection lemma 的 witness 未与被拒绝的合法输入绑定

- **问题**：`repeated_message_rejection_exists` 只要求某个 Send 早于某个 Reject；`same_party_rejection_exists` 只要求同 party 的两个不同 Send 早于某个 Reject。拒绝事件只携带 `bid,rst`，没有被拒 tuple。
- **实际证据**：新导出 graph 中，M 的 Send 是 `Send(~a,~sid,~m.1)`，被拒 pair 使用未与它绑定的消息变量 `m`；P 的两个 honest Sends 用 `~a`，被拒 pair 使用独立的 `A`。这说明 graph 未强制它们相等，不是声称这些自由变量在任何实例中必定不同。这不是模型错误，而是查询允许不相干证据拼接。[trace 摘要](D:/kwaay-formal/reviews/2026-09-16-evidence/trace-audit-summary.txt)
- **位置**：[M 85–90 行](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_message_dedup.spthy:85)、[P 85–94 行](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_party_admission.spthy:85)；正文 §5.3 已承认限制。
- **影响**：不能拿这些结果证明“那两条合法 sender 消息被拒绝”。它们只证明 rejection branch 非空。
- **修改**：若这一 claim 重要，记录 entry-bearing admission/rejection event 或其可追溯来源；增加精确绑定的 witness。若不重要，删去无关 Send 前提并把名称缩减为 rejection reachability。无需强加 liveness；有限 trace 可以合法地停止，absence of liveness 不是攻击。

### M6. 成稿与 canonical authority 对“核心贡献”存在实质分叉

- **问题**：成稿 Introduction 55–57、§5.4 和 §7.5 将 M separation 定为核心；`research-contribution.md`、`g2-admission-semantics.md` 明确把消息/party 非等价和 M 控制限定为辅助，把 distinct-party necessity 作为最终贡献。有些旧叙述还称重复 party 造成 ambiguous attribution，但在 `E1,E2` 中来源均清楚等于 A，真正缺失的是投影的单射性，而非无法识别来源。
- **位置**：[成稿 Introduction](D:/kwaay-formal/manuscript/sections/01-introduction.tex:45)、[canonical research statement](D:/kwaay-formal/docs/rq-v2/research-contribution.md)、[G2 authority](D:/kwaay-formal/docs/rq-v2/g2-admission-semantics.md)、[supporting attribution analysis](D:/kwaay-formal/docs/rq-v2/party-output-binding-analysis-final.md)。
- **影响**：claim–evidence traceability；审稿人不知道论文希望证明 necessity 还是 non-substitutability，也可能被 artifact 里的强表达误导。
- **修改**：统一当前 authority 与成稿；保留历史材料但标记清楚。不以同名事件、同名 lemma 或 M4 的大量目标替当前 RQ-v2 的缺失证据背书。`slot → A` 仍是函数；重复 party 使其非单射。只有反向“由 A 唯一选 slot”的接口才出现选择歧义，且该接口当前未建模。

### M7. 原提交的结果包可重跑，但不是可追溯的原始运行证据

- **问题**：`existing-report-only` freeze 由 Markdown 结果转录而成；输入 hash 不验证当时的工具调用、输出、exit status 或 graph。原稿已经坦诚披露，不能指控其隐藏。
- **本轮状态**：已用相同版本工具独立重跑，14/14 结果与步数一致，保存 raw transcripts 和七个 graph；所以本项现在是**可完成的 artifact 发布修订**，不是结果不成立的证据，也不是主拒稿依据。
- **位置**：[§5.6](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:277)、[Appendix C](D:/kwaay-formal/manuscript/appendix/reproducibility.tex:4)、[freeze environment](D:/kwaay-formal/artifact/rqv2-freeze/environment.txt)。
- **修改**：以新的、明确日期和 commit 的 rerun 发布证据，不把新日志写成当年的 recovered log；使结果表可从 raw output 生成，保留输入 hash、工具版本、命令和工作树状态。

## 7. Minor Issues

1. **同一字段名 `sid` 的误导成本较高。** 当前模型是独立 fresh origin token；原文是身份、key、prekey 和消息的串接值并参与 KDF。正文虽说明了边界，建议用 `oid` 等不冲突符号，或在首次映射时并排给出两者。[§2.3](D:/kwaay-formal/manuscript/sections/02-batchreceive-identity-problem.tex:77)、[§4.2](D:/kwaay-formal/manuscript/sections/04-formal-modeling.tex:124)。影响 session-binding 的阅读，不影响当前模型结果。
2. **同一核心非蕴含重复过多。** §2、§3、§4.4、§5.2、§5.4、§6.1–6.4、§7.4–7.5、Conclusion 反复解释。29 页篇幅与实际命题数量不匹配。压缩不能修复 novelty，但能使审稿人更清楚地看到新增内容。
3. **原文版本仍可更精确。** bibliography 指向浮动 ePrint URL；目前 §5.1 p.21 的定位正确。建议补下载日期、PDF hash／版本标识，不要混用 proceedings 与 full-version 页码。此次 full PDF hash 为 `476f28594806f15f4baab6ce7d3785143db0a013f21fbcf590ac1666161660a8`；封面日期与 ePrint revision 日期不同，应分别记录。
4. **直接后续工作需检查覆盖。** 2025 年已有 [Practical Deniable Post-Quantum X3DH: A Lightweight Split-KEM for K-Waay](https://eprint.iacr.org/2025/853)，官方记录标注 ACM ASIACCS 2025。它主要改进 split-KEM，不据此断言覆盖本稿的 admission 问题；§7.1 至少应交代其是否改变本稿接口前提。这是引用完整性问题，不是要求重写 primitive 综述。
5. **结构没有严重错位，主要是重心问题。** Threat Model 没有代替完整 proof；Background 也没有把新假设冒充原文。PDF 的图表、公式和结果表能阅读，未发现影响审稿的明显裁切、重叠或缺字；不应把版式当主拒稿理由。

### 各章功能审查

| 章节 | 判断 | 具体调整 |
| --- | --- | --- |
| Introduction | 主张边界清楚；重要性与新颖性弱 | 用一个真实协议接口问题引出模型；不要用一般 composition 工作的影响力替本稿证明重要性 |
| Background / §2 | 原文 distinct-party 来源正确；概念区分基本清楚 | 加入 party-indexed game／实际 sid 的必要背景，减少重复“不同字段不等”的说明 |
| Threat Model / §3 | 能力假定明确；没有谎称网络自动控制部署 batch | 用能力表说明 honest repeated Send、network replay 与 composition control 各自作用 |
| Formal Model / §4 | 可读，假设披露充分 | 突出 `!Sent`、receiver/context 缺失和 freshness 如何决定结果；给规则差异而非多次文字复述 |
| Security Analysis / §5 | 结果忠实，但“counterexample”对象需始终明确 | 主打 M 的非蕴含；R 是局部事件重用；P 是正控制；无需赋予其新密码学意义 |
| Verification / §5.5–5.6、Appendix B/C | 14 行结果准确，公式直接引用源文件是优点 | 纳入新独立复核包；将 derived properties 与独立 witness 区分 |
| Discussion / §6 | limits 诚实；设计建议目前较一般 | 少辩护“不是 guard removal”，多解释协议中哪种对象受影响及还缺什么 evidence |
| Related Work / §7 | 大体正确区分邻近工作；没有明显优先权夸大 | 与最近工作比较证据强度和研究对象，而不只是不同的“层”；补直接后续 K-Waay 文献 |
| Conclusion / §8 | 与窄模型结论相符 | 保持非协议攻破边界；根据最终选定贡献统一 necessity/separation 定位 |

建议顺序仍可保持“协议接口及待回答问题 → 目标与能力 → 抽象和关系 → 三种模型结果 → 协议意义与限制”。无需为了审稿形式强拆九个章；当前组织已经覆盖这些职能。

## 8. Claim–Evidence Table

### 8.1 主张和证据对应

| Paper Claim | Evidence | Formal Support | Original K-Waay Support | Assessment |
| --- | --- | --- | --- | --- |
| 一次 BatchReceive 的元素来自不同 party | §2.2；full p.21 | P 将其编码 | Explicitly stated | 正确，条件属于原协议 |
| batch 是 vector，按 receiver state 组合 | §2.1；full §4.1 | 两个线性 slot；fresh bid/rst | Explicitly stated | 概念映射合理；不能视作完整 state 模型 |
| 同一 party 可有两个不同 sender origins | §2.3；SendMessage | `!Party` 可反复使用；fresh sid/m | 多 session 明确；模型 fresh atom 是自选抽象 | 模型内成立，不代表同一 sender session 可多次 Send |
| R 一次匹配 Send 对应两个 accepts | §5.1 | `one_send_two_accepts_exists` + falsified injectivity；本次复现 | 原规范不允许该 input composition | 正确的 relaxed-model counterexample |
| 每次接受都有此前 Send | §4.6、§5 | 三个 `receiver_accept_has_send` | 原文有密码学认证相关论证，但非同一公式 | 理想 origin 前提的保留，不是认证被独立证明 |
| M 可保持 scoped injectivity | §5.2 | M injectivity verified | 非原协议承诺 | 正确，与 M 的消息 safety 非独立 |
| M 仍接受同 party 的不同消息 | §5.2 | 明确绑定两 origins、两 accepts 的 exists | 原文 distinct-party 条件排除此组合 | 本稿最强模型内 separation |
| P 保持 admitted party inequality | §5.3 admission paragraph | `Neq(A1,A2)` + restriction；规则静态可见 | 实现已陈述前置条件 | admission-level 结论来自规则，不只来自接受端 lemma |
| P 保持 accepted party inequality | §5.3 | `accepted_batch_has_distinct_parties` verified | 与条件相容 | 模型正确，正控制 |
| P 不靠拒绝所有 batch 成功 | §5.3 | `distinct_party_batch_exists` verified | 允许合法 distinct-party 调用 | 非空性证据扎实 |
| 拒绝分支可达 | §5.2–5.3 | 两条 rejection exists | 新 admission layer 的自选分支 | 成立；未绑定所展示的 Send，不是 liveness |
| 消息检查不能替代 party contract | Abstract、§5.4、Conclusion | 在既定 origin/freshness/lifecycle 下 M 的 witness | 原文并未建议该替代方案 | 窄结论成立；重要性仍需说明 |
| 协议级修复／身份绑定弱点 | 当前成稿明确不主张 | 无 KDF、key、真实 sid 或 consumer | 原文已有 transcript identity binding | 不允许从当前 evidence 推出 |
| arbitrary batch、cross-batch、rollback 安全 | 当前成稿明确不主张 | 每 batch 两槽；没有相应生命周期 | 非本次结论 | 不支持；不能因 Tamarin 支持 unbounded 而补上 |

### 8.2 Original-paper fidelity 逐项核查

本表基于 [K-Waay 官方 full version](https://eprint.iacr.org/2024/120.pdf)，特别是 pp.15–18、21–27；[USENIX proceedings record](https://www.usenix.org/conference/usenixsecurity24/presentation/collins) 与 full version 分开引用。下列标记评价“该命题与原文的关系”，不代表当前论文一定犯了该命题对应的错误。

| 被核查命题 | 分类 | 核查结果 |
| --- | --- | --- |
| 输入包括 receiver `sk_i,st_i` 和 sender-associated triples | Explicitly stated | §4.1，triple 为 `(pk_j,prek_j,m_j)` |
| batch 是 vector，而非按元素去重的数学 set | Explicitly stated | §4.1 明确类型和长度；不能仅依据 `{...}_j` 语法推断 set semantics |
| 每个 input 属于不同 party | Explicitly stated | §5.1 p.21，Fig.10 后；当前论文引用正确 |
| 原文遗漏了此条件 | Contradicted by original paper | 本轮已用原 PDF 页面核实；不是隐藏假设发现 |
| “several senders”单独蕴含 distinct-party | Weakly implied | 仅自然语言不够；本案已有更强的明文依据 |
| party 可运行多个 sessions | Explicitly stated | §4.2.1；session 记为 `π_i^s` |
| 同一 party 的不同 Init/session 可产生不同 ephemeral keys／prekeys | Strongly implied | 多 session 加上逐次 Init 的 key generation；不可把 ephemeral key distinction 当作 principal distinction |
| honest party 在同一游戏中任意轮换多个 long-term keys | Not stated | 标准 honest setup 将 party 与一个 long-term key pair 关联；多个 session/prekey 不能替代 key-rotation 模型 |
| party 与其 public-key bytes 是定义上的同一个对象 | Not stated | party 有独立索引；key pair 是关联对象；不能把数学关联误写为对象恒等 |
| 攻击者可以注册额外 principal 与指定公钥 | Explicitly stated | `REGISTER(pk_i,i)`；标为 corrupted。不同 principal 是否同 key 不应凭“honest keys 通常不同”武断排除 |
| 同 party 的多个合法 sessions 可直接进入同一合规 batch | Contradicted by original paper | 跨 session 能发消息，不等于同批次可违反 p.21 条件 |
| receiver ephemeral material 会在一个 batch 内复用 | Explicitly stated | §4.1、§5.1；用同一 state 处理关联 inputs |
| 可以无限反复用同一 receiver state 调不同 BatchReceive | Contradicted by original paper（针对此无条件表述） | §4.1 描述每个 ephemeral state 一次；游戏 status 也限制完成后的重复 EXEC；不能从“复用”推出跨批重复调用 |
| 任一 split-KEM failure 会令全批输出 all-bottom | Explicitly stated | Fig.10 13、16 行；signature failure 本身只影响相应元素 |
| receiver 每个成功 slot 各设置一次 protocol status=accept | Contradicted by original paper | 原文一个 receiver session 的 status；足注说明至少一个输出非 bottom 即接受；不等于本文两个事件 |
| 原文 sid 含 principal identities、keys、prekeys、message，并输入 KDF | Explicitly stated | Fig.10 Send 9–10 行及 BatchReceive 12、15 行 |
| 原协议 party identity 只存在于事件 annotation | Contradicted by original paper | 原文 sid/KDF 有实际依赖；当前最小模型才没有密码运算 |
| KEY/TEST 的 `j` 对应单个 receiver output component | Strongly implied | §4.2.3 的 `k_j` 与 party-indexing；distinct-party 条件提供自然的唯一选择域 |
| §4.2 的每一个 EXEC 分支都独立写了 pairwise-distinct guard | Not stated | 未看到局部显式 distinct 检查；不能抹去 §5.1 对具体构造的明文前提 |
| Theorem 1 使用原构造／原游戏定义域 | Explicitly stated | §5.2 定理和 Game Γ1；不是 unrestricted duplicate-party extension 的定理 |
| 去掉 distinct-party 后原密码学 reduction 必然无效 | Not stated | proof 选择测试 component 的写法依赖索引解释，但不存在本文给出的失败 reduction 或 advantage 攻击 |
| split-KEM IND-1BatchCCA 本身要求 batch 内所有 public keys pairwise distinct | Not stated | Fig.5 有一次 BatchDec、challenge-pair 排除及 failure 规则，未见通用 pairwise-key inequality；不能与上层 party 条件混同 |
| caller／server／receiver 哪层维护 party 条件，以及具体失败 API | Not stated | 没有据此得到真实实现漏查；“未固定机制”不同于“没规定不变量” |

这里最有价值的未完成分析是：**如果扩展原域允许同 party 多 entry，`k_j` 和测试 component 如何定义？** 这可能形成接口形式化工作；目前不能预判它会导出安全漏洞。即使引入 slot-indexed outputs 可以消除选择歧义，也仍需重新说明 security game，而不是宣称已经修复原 K-Waay。

### 8.3 Definitions 审计

| 术语 | 当前定义／使用 | 审计结论 |
| --- | --- | --- |
| party | protocol principal，符号 A | 正文稳定；如何从真实 input 得到 A 被假定，不能冒充已验证 identity resolution |
| identity | 多数段落指 party projection | 必须保留限定，不能把所有身份／名字／credential 问题统称为本性质 |
| sender | 执行 Send 的 party 或 sender occurrence | 两者均可合理使用，但 one sender、one Send、one sender session 不同；本稿主 witness 实际是 one matching Send |
| sender public key | 原协议 long-term key pair 的公共部分 | 当前模型没有此对象。公钥不等与 party 不等之间需注册假设，不能直接替代 |
| entry | 抽象 `(A,sid,m)`；原文 `(pk,prek,m)` | 正文承认不是 wire tuple；缺少从后者到前者的构造关系 |
| occurrence | 一次 sender 或 receiver action firing | occurrence equality 应是同一次事件，不只是字段相等 |
| sid | 模型 fresh sender-origin coordinate | 在本模型可唯一定位 Send；原协议 transcript sid 不同，需避免名字诱导的偷换 |
| slot | batch 中位置，规则状态区分 | ReceiverAccept 未显式带 slot；因每条 process rule 单次 action 和线性阶段，当前模型可用 timepoint 区分，不宜无条件推广 |
| batch | 原文输入向量；模型两槽 execution | B 在语义定义中为 ordered collection，bid 为标识；须区分对象与标识 |
| BatchReceive | 原文密码算法；模型 admission action | 同名但层级不同，正文已披露。模型 action 不代表已经输出所有 derived keys |
| distinct-party | `i != j ⇒ party(Ei) != party(Ej)` | 明确的投影单射性；不是每槽“只有一个 party”，也不是所有 entry 各有来源即可 |
| duplicate-party | 不同位置投影相同 | 可以消息相同或不同；不能自动称为 duplicate origin／duplicate session |
| admission condition | 允许 candidate batch 进入 modeled processing 的谓词 | 本文引入的边界，不是原文独立 algorithm；R/M/P 的拒绝行为属于模型设计 |
| identity binding | 若作密码学用语，应表示身份与 key／transcript／peer 的正确关联 | 当前没有该 property；正文将其与 party distinction 分开是正确的 |
| session binding | 真实会话／上下文与消息、key、peer 的关联 | fresh sid ＋ event arguments 不足以实现原协议 session binding，尤其 Send 未绑定 receiver context |
| accepted component | model-local ReceiverAccept action | 不等于原文 session status，不等于最终非 bottom key，也不等于应用安装 |

未发现正文在不同章节偷偷把 A 改成 public-key bytes 的确凿错误。真正的问题是已披露但尚未论证的抽象映射，以及 supporting docs 将“投影非单射”说成“归属含糊”的倾向。

### 8.4 安全性质分类

| Property | 当前正式证据 | 原性质／本文性质及判断 |
| --- | --- | --- |
| authentication | `receiver_accept_has_send` | 仅理想 origin correspondence；缺 recipient、key、crypto checks，不等于原 K-Waay 的 implicit authentication |
| non-injective agreement | 无完整双方运行／参数 agreement 定义 | 不能把 has_send 自动命名为完整标准 AKE non-injective agreement |
| injective agreement | 一个 batch/context 内 exact origin 的接受唯一性 | 本文 scoped diagnostic；不能替代标准 run-to-run injective agreement |
| key secrecy / key indistinguishability | 无 key、K、Test 对象或 lemma | 未分析，不存在相应 violation 证据 |
| identity binding / peer agreement | 无错误 peer、错误 identity 到 key 关联的查询 | 未分析；同一个 A 出现两次不证明错误绑定 |
| unknown-key share | 无双方 shared key 和不同 peer views | 不支持 UKS 分类 |
| session uniqueness | fresh sid 唯一来自建模；I 只限制单批接受 | 不证明原协议的全局 session uniqueness |
| contributive identity | 没有关于各 party 对 key 贡献的定义或计算 | 不能把参与者数量的结构条件命名为 contributiveness 结果 |
| party uniqueness | R/M witness 可违反；P safety 成立 | 正式目标，源自原文输入条件的模型化，不是一般标准 AKE 安全本身 |
| replay resistance | R 展示 exact-origin 重复；M/P 阻止该局部模式 | 不证明 cross-batch、restart、网络全局 replay resistance |
| deniability | 无 equivalence／simulation 模型 | 当前没有正反结论；历史 deniability 结果不替代本稿证据 |

没有 formal evidence 支持 cryptographic authentication／secrecy loss。即使将结构重复视作 bookkeeping 层问题，也应避免说“已证 bookkeeping ambiguity”：当前模型保留每个 entry 的明确 party 来源，尚未定义按 party 反向查唯一输出的 bookkeeping API。

## 9. Tamarin Audit

### 9.1 运行与 scope

本轮检查的是三个 RQ-v2 theory，**10 个不同名字的 lemma，共 14 个 model–lemma 实例**。固定的是每个 batch 两槽，不是总 party 数、Send 次数或 batch 数的全局上界；模型没有给这些生成规则设置总次数 bound。命题仍只观察单个 `(bid,rst)`。

输入 SHA-256 与原记录一致：

| Model | SHA-256 |
| --- | --- |
| R | `e5129575720020aa3f509782c2052fbf2114a540d013126f5a75d316cbabaf9d` |
| M | `90a196f5da5c244026596283d001376427880cd64c5bea3c6cfdfd4ccba99184` |
| P | `c35af64cac7f01182418cb999ea105214b8da4f2295b670a9b3733f0bd976bba` |

没有导入外部 theory，没有用户定义加密函数／equations，没有 compromise、key secrecy、KDF 或 deniability lemma。全部 prove invocation 完成且 wellformedness 成功。

### 9.2 全部核心 lemma

下表 V 表示 verified，F 表示 falsified with trace；括号内为本次与原记录一致的步数。通用假设 H：fresh `sid,m`；持久 `!Party,!Sent`；网络 `In/Out`；batch 内两条线性顺序处理规则；接受要求完整 tuple 的来源匹配。R 无额外不等限制；M 增加 `m1 != m2`；P 增加 `A1 != A2`。

| Lemma | Intended Meaning | Actually Proves | Assumptions | Problem |
| --- | --- | --- | --- | --- |
| R `normal_relaxed_batch_exists` V(10) | 基本可执行性 | 存在 Send、admission、至少一次后续 accept | H、R | 不要求两次 accept、不同 party 或显式完成事件；当前正文解释正确 |
| R `one_send_two_accepts_exists` V(13) | 一 origin 被同 batch 接受两次 | 完整 tuple 全同，`s<b<r1<r2`，匹配 Send 唯一 | H、R、可重放 | 不排除无关 Send；不是原协议合规域攻击 |
| R `receiver_accept_has_send` V(8) | origin correspondence | 每个 accept 有先前精确匹配 Send | H、R | 基本由 `!Sent` 前提强制；不证明密码学认证 |
| R `receiver_accept_injective` F(13) | 同 batch 单一 origin 至多一次接受 | 找到满足前提而 `r1 != r2` 的 trace | H、R | 局部事件性质失败，不是标准 AKE session theorem |
| M `repeated_message_rejection_exists` V(4) | 拒绝可达 | 某 Send 早于某 Reject | H、M 拒绝分支 | 两者未绑定；不能证该 Send 的消息被拒 |
| M `same_party_different_messages_batch_exists` V(16) | 同 party 不同消息均可接受 | 两不同 `sid,m` 的来源、同 batch、两 accept 绑定 | H、M | 对象是 party invariant；没有 origin mismatch |
| M `accepted_batch_has_distinct_messages` V(31) | 接受消息区分 | 同 context 不同接受事件有不同 `m` | H、M | 由 guard 传递；仅接受端 safety，不是进度性质 |
| M `receiver_accept_has_send` V(8) | origin correspondence | 同 R | H、M | 同 R；不是独立 crypto guarantee |
| M `receiver_accept_injective` V(33) | scoped injectivity | 同 tuple/context 不存在两次接受 | H、M | 与 message safety 在本生命周期下等价；不是全局 replay prevention |
| P `same_party_rejection_exists` V(5) | 同 party 拒绝可达 | 某同 party 两次不同 Send 早于某 Reject | H、P 拒绝分支 | 未绑定 rejected pair；本文已披露 |
| P `distinct_party_batch_exists` V(17) | 有效 batch 非空 | 两 party、两 origin、同 batch、两 accept | H、P | 非空性证据合格；不是所有合法输入的完成性 |
| P `accepted_batch_has_distinct_parties` V(31) | 接受端 party distinction | 同 context 两个不同 accept 的 party 不同 | H、P | 正控制；不证明原密码学安全必须用此检查 |
| P `receiver_accept_has_send` V(8) | origin correspondence | 同 R | H、P | 继承 origin 前提 |
| P `receiver_accept_injective` V(33) | scoped injectivity | 同 tuple/context 至多一次接受 | H、P | 是 party safety 的直接后果之一；M 已表明 P 不是 I 的唯一必要机制 |

### 9.3 逻辑公式及 claim → rules → witness 映射

为可读性用 `S(A,sid,m)@s` 代表 `Send`，`B(bid,rst)@b` 代表 `BatchReceive`，`R(A,sid,m,bid,rst)@r` 代表 `ReceiverAccept`，`J(bid,rst)@j` 代表 `Reject`。未展示的变量均按下述公式量化；这仅是事件名缩写，源文件中的精确公式仍为权威。

**共同 correspondence**：

```text
∀ A,sid,m,bid,rst,r.
  R(A,sid,m,bid,rst)@r
  ⇒ ∃s. S(A,sid,m)@s ∧ s<r
```

**共同 scoped injectivity**：

```text
∀ A,sid,m,bid,rst,s,r1,r2.
  S(A,sid,m)@s ∧ R(A,sid,m,bid,rst)@r1
  ∧ R(A,sid,m,bid,rst)@r2 ∧ s<r1 ∧ s<r2
  ⇒ r1=r2
```

二者对应 `SendMessage` 生成 `!Sent`、`ProcessSlot1/2` 读取 `!Sent`。前者在所有模型成立；后者在 R 可被同 tuple 两次收集击败。没有双方对同一 derived key 的 agreement 公式。

**R 的两个存在性查询**：

```text
normal:
∃ A,sid,m,bid,rst,s,b,r.
  S(A,sid,m)@s ∧ B(bid,rst)@b ∧ R(A,sid,m,bid,rst)@r
  ∧ s<b<r

one_send_two_accepts:
∃ A,sid,m,bid,rst,s,b,r1,r2.
  S(A,sid,m)@s ∧ B(bid,rst)@b
  ∧ R(A,sid,m,bid,rst)@r1 ∧ R(A,sid,m,bid,rst)@r2
  ∧ s<b<r1<r2
  ∧ (∀s2. S(A,sid,m)@s2 ⇒ s2=s)
```

对应同一个 `Out(<A,sid,m>)` 两次供给 `CollectSlot1/2`，然后 `AdmitRelaxedBatch` 和两条 process rules。第二条到达第二次接受时同一 rule 已产生 `BatchComplete` state，但 lemma 没有对 completion action 作额外断言。

**M 的三个专属查询**：

```text
rejection:
∃ A,sid,m,bid,rst,s,j. S(A,sid,m)@s ∧ J(bid,rst)@j ∧ s<j

same_party_different_messages:
∃ A,sid1,sid2,m1,m2,bid,rst,s1,s2,b,r1,r2.
  S(A,sid1,m1)@s1 ∧ S(A,sid2,m2)@s2 ∧ B(bid,rst)@b
  ∧ R(A,sid1,m1,bid,rst)@r1 ∧ R(A,sid2,m2,bid,rst)@r2
  ∧ m1≠m2 ∧ sid1≠sid2 ∧ s1<b ∧ s2<b ∧ b<r1<r2

distinct_messages:
∀ A1,A2,sid1,sid2,m1,m2,bid,rst,r1,r2.
  R(A1,sid1,m1,bid,rst)@r1 ∧ R(A2,sid2,m2,bid,rst)@r2
  ∧ r1≠r2 ⇒ m1≠m2
```

分别对应 `RejectRepeatedMessage`、两个 honest Send 后的 `AdmitDistinctMessages` 与顺序处理、admission 的 `Neq(m1,m2)` 传递到事件。第一条无 tuple 关联，第二条关联完整，不能交换它们的证据作用。

**P 的三个专属查询**：

```text
same_party_rejection:
∃ A,sid1,sid2,m1,m2,bid,rst,s1,s2,j.
  S(A,sid1,m1)@s1 ∧ S(A,sid2,m2)@s2 ∧ J(bid,rst)@j
  ∧ sid1≠sid2 ∧ m1≠m2 ∧ s1<j ∧ s2<j

distinct_party_exists:
∃ A1,A2,sid1,sid2,m1,m2,bid,rst,s1,s2,b,r1,r2.
  S(A1,sid1,m1)@s1 ∧ S(A2,sid2,m2)@s2 ∧ B(bid,rst)@b
  ∧ R(A1,sid1,m1,bid,rst)@r1 ∧ R(A2,sid2,m2,bid,rst)@r2
  ∧ A1≠A2 ∧ s1<b ∧ s2<b ∧ b<r1<r2

distinct_parties:
∀ A1,A2,sid1,sid2,m1,m2,bid,rst,r1,r2.
  R(A1,sid1,m1,bid,rst)@r1 ∧ R(A2,sid2,m2,bid,rst)@r2
  ∧ r1≠r2 ⇒ A1≠A2
```

分别对应 equal-party rejection、两真实 parties 的 admitted execution、admission 中 `Neq(A1,A2)` 的保留。相应 safety 量化的是接受事件，不是所有未处理的 collected tuples；后者的 admission inequality 需要由 rule 本身说明。

### 9.4 Restrictions、事实和建模审计

| 审计点 | 结果 |
| --- | --- |
| 是否偷偷把 theorem 全文写成 restriction | 没有。M/P 唯一 restriction 是标准 `All x #i. Neq(x,x)@i ==> F` |
| 是否仍把 desired relation 硬编码 | 是。P 在 admission 中直接输出 `Neq(A1,A2)`；它就是该模型的 guard。这是公开正控制，不是假装从密码学推出它 |
| restriction 编码是否不正当 | 不是；它是 Tamarin 常用 inequality 编码。关键是不能把 guard 的正确实现当作现实必要性的独立证明 |
| baseline/variant 是否同时变更 unrelated processing | 逐规则对照未发现。party/send/batch/collect/process 相同；变的是 admission/reject/restriction、名称和 lemma 集 |
| persistent facts | `!Party` 允许多次 Send；`!Sent` 可支持重复接受；没有隐蔽 persistent key/state。它也使 correspondence 高度直接 |
| `Fr` | `A,sid,m,bid,rst` 来自 fresh；`sid,m` 每次 Send 唯一。不能据此推导真实 message equality／collision／reuse 规律 |
| `In/Out/KU` | 输出公开 tuple；In 允许敌手构造可推导 tuple；KU 属内置敌手推导，无用户直接造 KU 的后门。敌手可重组候选，但没有 `!Sent` 的 tuple 不能被 process 接受 |
| admission 与 accepted domain | admission 可接收没有真实 origin 的公开组合；之后可能卡住。模型没有把卡住解释为真实 cryptographic rejection |
| 身份是否只是 annotation | A 还进入网络 tuple、state 和 `!Sent` 匹配，因此不只是 action annotation；但它不进入任何密码函数，因为当前模型没有这些函数 |
| 真正 identity binding / session binding | 未建模 cryptographic binding；fresh sid 也不是原协议 transcript sid |
| vacuity | R 的基本正常 witness 仅一接受；R 双接受 witness、M 同 party 双接受、P 两 distinct party 双接受足以排除相关 universal claims 因完全不可执行而空真 |
| event/timepoint | 每条 process rule 只发一次 ReceiverAccept，线性状态确保至多两个且顺序不同；用 timepoint 区分槽在这个模型中合理，不可推广到同一 rule 同时发多个 accept 的模型 |
| liveness | 没有。拒绝规则 enabled 不等于任意 trace 最终拒绝；当前正文对此准确 |
| 所谓 necessity | P→party safety 与 R witness 只显示当前变体的依赖；M 的 injectivity 成功直接反对“只有 distinct-party 才能防止 exact-origin 重复”的更强说法 |

编码规则的核查参照 [Tamarin 官方 facts/rules 文档](https://tamarin-prover.com/manual/master/book/005_protocol-specification-rules.html) 与 [restriction 文档](https://tamarin-prover.com/manual/master/book/007_property-specification.html)。本报告的具体结果来自本地 1.12.0 的实际执行，而非假定当前在线文档证明了模型。

### 9.5 历史证据与 archive

已检查历史 [replay README](D:/kwaay-formal/tamarin/replay/README.md)、[replay 规则](D:/kwaay-formal/tamarin/replay/kwaay_replay_original.spthy:65)、[impact 模型](D:/kwaay-formal/tamarin/impact/kwaay_impact_original.spthy:222)、对应结果记录、M4 composite summary，以及 pre-RQ-v2 archive 的研究冻结文档。

- 历史 replay 引入私有 ciphertext/key constructors、`session_id`、`session_key`，但成功处理仍读取理想 `!HonestSession`，不是完整验证／解封装模型。
- 历史 impact 明确依赖 `C_install-v2`：每个 accepted output 独立安装，使用新 handle，不合并或去重。出现两个安装是这一 conditional consumer 的结果，不能借来证明实际应用如此。
- 历史 key construction 中 public-key constructor 还带 sender/receiver state 参数；若要将其作为真实长期 key 生命周期，需另做映射审计。本次不把它升级为旧模型的全面否定。
- M4 的 296 目标是另一个 Tamarin-only composite；它们不等于当前三模型的 14 个目标，也不证明当前 party-level claim。没有本轮重新运行这些历史目标。
- 历史库确有 JSON traces 和 raw logs，不能笼统声称“整个项目没有 trace”；准确说法是**原 RQ-v2 freeze 没有对应 raw traces**。本轮新增的 RQ-v2 graphs 是新审稿复核证据。

## 10. Attack Validity Table

### 10.1 能力分类

| 能力 | R exact replay | M same party / different messages | 与真实协议的关系 |
| --- | --- | --- | --- |
| Dolev–Yao 网络保留／重放 | 需要一次 tuple 的重复供给 | 只需交付两条已产生 tuple，无须 exact replay | 网络能力不自动包含实际 batch builder 权限 |
| honest-party repeated invocation | 一个匹配 Send 足够 | 需要同 party 两个 sender occurrences | 原游戏允许多 session；不能重复调用一个已 accept 的 sender session |
| malicious sender | 不需要 | 不需要 | 也不是通过创建假身份达到目标 |
| long-term compromise | 不需要／未建模 | 不需要／未建模 | 不是证明对 compromise 安全 |
| ephemeral compromise | 不需要／未建模 | 不需要／未建模 | 没有 state-reveal 攻击 |
| batching-layer composition control | 将同 tuple 放进两槽 | 将两个 same-party origins 放同 batch | 当前显式假定；真实 caller 如何授予该能力未证明 |
| API misuse／contract violation | 重复输入违反 distinct-party 域 | 同 party 两输入也违反域 | 即使每次 Send 本身合法，组合调用仍可不合规 |

**不需要密钥泄露是这个受限 witness 的特征，不是独立的新漏洞价值。** 两条正常消息被组合到一个被原规范排除的 batch，不会自动成为对原规范承诺的攻击。

### 10.2 有效性总表

| Attack / Trace | Required Capability | Violated Property | Protocol-level Consequence | Validity |
| --- | --- | --- | --- | --- |
| R：同 tuple 两次入槽 | 网络重复＋不维护条件的 batch composition | 本文 batch-local exact-origin injectivity；party invariant | 本模型两个 accept 事件；无 key 输出 | **Valid model counterexample；不是合规 K-Waay break** |
| M：同 party 两个不同 origins | 两次 honest Send＋选择同批次；无需重放 | party invariant | 两个各有合法 origin 的事件；没有 wrong peer／key confusion | **Valid separation witness** |
| P：same-party rejection | 提交 equal-party candidate | 无被破坏性质 | 仅抽象 rejection branch | **Valid reachability；所展示 Send 未与输入绑定** |
| P：distinct-party normal batch | 两合法 distinct origins | 无 | 证明正控制可接受有效 pair | **Valid non-vacuity witness** |
| 历史 duplicate-install trace | R relaxed input＋`C_install-v2` consumer | 条件模型中的本地安装唯一性 | 两个符号 handle；实际消费者未知 | **Conditional historical result，非当前 RQ-v2 攻击证据** |

最准确的总体命名是 **model-level property failure under relaxed admission / admission-contract non-substitutability**。可以讨论 integration contract；不能直接叫 missing assumption、identity-binding weakness、UKS、full protocol break。规范本身明确，故“specification ambiguity”只能指尚未固定的扩展／实现解释，而不能指原条件是否存在。

### 10.3 强制还原：R 的 exact-origin replay

1. **Initial state**：抽象中创建一个 `Party(A)` 与一个新 batch context。若用协议词汇作候选解释，则接收方 B 已有 receiver prekey/state，A 已有合法 sender state；这部分对应并未由 R 模型表达。
2. **Honest parties**：一个 sender A；模型没有显式 B principal，`rst` 不等同于完整 receiver state。
3. **Attacker knowledge**：一次 Send 后的公开 `(A,sid,m)`；无 key 对象或秘密泄露。
4. **Protocol actions**：抽象执行一次匹配 Send。协议层候选解释应是一次 `Init/Send` 针对 B 的 prekey 得到 ciphertext triple；不能把 fresh atom 当作已构造好的具体 ciphertext。
5. **Batch construction**：敌手／未维护契约的 caller 选择 `(E,E)`。
6. **Duplicate-party occurrence**：两槽都指 A，同一 origin/message；原协议 p.21 的输入域从这里已被违反。
7. **Receiver processing**：R 无 guard，两个 Process rules 重用同一 `!Sent`。
8. **Resulting key/state/event**：两个同坐标接受事件、一个 `BatchComplete` state；**没有 session key，也没有原 K-Waay status 的两次变更**。
9. **Violated property**：两事件不同且匹配同一 origin/context，反驳局部 I；重复 A 反驳 P。

敌手得到的是模型中允许的重复接受事实，没有学到 key，没有冒充另一个 party，没有让 B 把 A 认成 C，也没有把同一 key 绑定到两个不同 identity。即便手动按原算法逐项处理 duplicate ciphertext，在相同 inputs 下可讨论重复计算；但原文域外 vector/index 处理和输出意义尚需指定，不能从本模型直接宣布“两次真实会话接受”。

### 10.4 强制还原：M 的 same-party / different-message witness

1. **Initial state**：同一 `Party(A)`，可启动两个 sender occurrences；新 batch context。
2. **Honest parties**：A 的两个 occurrences；协议候选解释是 A 的两个 sessions 面向同一 B receiver prekey。模型未绑定此接收目标。
3. **Attacker knowledge**：两个公开 origin tuples，不含 secret key。
4. **Protocol actions**：两个 `SendMessage`，产生不同 `sid1,sid2,m1,m2`。
5. **Batch construction**：把 `E1,E2` 放入一 batch。
6. **Duplicate-party occurrence**：`party(E1)=party(E2)=A`；但 `E1 != E2` 且非同一次 Send。
7. **Receiver processing**：M 的消息不等 guard 允许；两条 process rules 各读各自 `!Sent`。
8. **Resulting key/state/event**：两个来源正确的 accept；模型未输出 key，不能推断真实 key 相等、不同或泄露。
9. **Violated property**：只有目标 party distinction；当前 scoped injectivity 没有被破坏。

因此不能称为 bookkeeping ambiguity 已被证明：entry→party 的归属仍明确。若上层只以 A 唯一选一个 entry，才需要选择规则；该上层恰好是模型缺失部分。这比“两个 A 使身份不可知”准确。

### 10.5 强制还原：P 的拒绝与有效执行

P 的 rejection trace：初始可产生一个 party 和两个 Sends；敌手另行提供 equal-party candidate；`RejectRepeatedParty` 生成 `Reject/BatchRejected`；不进入处理，没有 key／accept，没有安全性质被击败。前置 Sends 可以与 rejected pair 无关，故不能给它补写不存在的 tuple 关联。

P 的有效执行：创建 A1、A2，分别 Send；敌手交付两个 origins；两个 slot 的 party 不同；`AdmitDistinctParties` 后两次处理均成功；最终有两 accept 和完成 state。该 witness 只证明至少存在一个有效执行，不证明所有合法 batch 在任意调度下都会完成。

## 11. Reviewer Objections

| 最强反驳 | 判定 | 当前是否能回应／还缺什么 |
| --- | --- | --- |
| “删掉 uniqueness 再证明 uniqueness 失败，基本由定义决定。” | **Partially valid** | 作者有完整生命周期、M 对照与非空性，故不只是文字替换；但这些尚不足以回答 novelty 与 protocol significance |
| “K-Waay 根本没要求 distinct-party，作者在攻击新要求。” | **Invalid** | 原全文 p.21 明确要求；不应继续沿此反驳方向修改 |
| “本文发现了 K-Waay 漏写的 distinct-party assumption。” | **Invalid** | 与原文矛盾；当前正文已经排除这种贡献定位 |
| “trace 没有 secrecy／authentication consequence，不能称 full attack。” | **Valid** | 当前稿已收缩措辞，可回应自己未做此强 claim；但仍需证明弱结果的研究价值 |
| “party identity 并非 K-Waay 密码计算的一部分。” | **Invalid（针对原协议）** | Fig.10 的 sid 含身份并输入 KDF。若反驳改为“本文没有分析该依赖”，则 Valid |
| “敌手控制 batch construction 没有现实依据。” | **Partially valid** | 在模型里是明示能力，在原游戏 EXEC 中也存在输入控制；但实际 caller 权限与合规输入域不同，部署适用性仍无证据 |
| “用 `!Sent` 证明 has_send 只是证明建模前提被保留。” | **Valid** | 对抽象 consistency check 无害；不能让它承担完整认证结果的价值 |
| “message safety 与 injectivity 并不构成两项独立成功控制。” | **Valid** | 本轮给出当前规则下 Mτ⇔Iτ 推导；需调整贡献措辞和依赖图 |
| “新 evidence 只是作者手填，结果不可复现。” | **Invalid（经过本轮复核后）** | 14/14 同结果同步数；旧运行 provenance 仍不足，但新 raw logs 已可审查 |
| “原协议游戏使用 party-indexed key，你们为何完全删除它？” | **Valid** | 限制性说明解释了 scope，却未回答为何省略与题目最相关的对象；需要精确接口工作或降低论文定位 |

与 [Cremers–Jacomme–Naska 的 session-handling 工作](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling) 相比，关键差别不只是“分析层不同”：该工作把具体 session management、实验性 PCS violation 和形式模型连接起来。本稿目前只有受限 admission comparison。引用这一先例不能代替自己的连接证据。

## 12. Required Revision Plan

### P0 — 不解决就无法支撑更强论文定位

1. **先确定可发表主问题。** 必须在“窄模型案例”和“协议接口／安全研究”之间明确目标。现有模型足以支持前者的逻辑结论，尚不足以支撑后者的贡献强度。单纯增加 rejection lemma 或 batch 数量不是替代品。
2. **若保留 K-Waay 特异性主张，补独立的协议接口命题。** 最值得先审查的是 receiver output、party index 与 `KEY/TEST` 的关系；先严格定义合法域、扩展域和输出选择，再判断是否存在真正问题。不预设会找到攻击。
3. **若要声称协议级 counterexample，先补 witness lifting。** 给出实际参与者、Init/Send/prekeys、同 receiver state、算法返回和违背的原文性质。若这一步无法完成，应保留 model-level failure 定位，不制造 crypto consequence。

验收标准不是“多几个 verified”，而是：新增结论没有直接写进 guard、具有原文或实际接口动机，并且 evidence 与结论在同一个语义层。

### P1 — 投稿前必须解决

1. 统一成稿、README、RQ-v2 canonical authority、claim matrix；标清 historical artifacts 的不可借用边界。
2. 明示 `Pτ ⇒ Mτ ⇔ Iτ` 在当前模型中的依赖；合并冗余结果解释，保留真正的 M↛P witness。
3. 完成 source-to-model 映射：principal 与 pk/prekey 的关系、sid 的不同语义、receiver/state 的丢失、batch-wide failure 和按槽事件的观察边界。
4. 将新独立复核作为有日期、commit、输入哈希和 raw outputs 的单独 evidence release；不要假称恢复了旧执行 provenance。
5. 按实际需要强化或缩减两条 rejection queries；如展示“具体合法 pair 被拒”，必须绑定该 pair。不要把 liveness 当作必须增加的无关安全要求。
6. 为每个 witness 配一个九步 trace 与明确攻击收益表；若不能提升到协议层，在相应步骤直接写出断点。

### P2 — 提升论文质量

1. 压缩重复解释和 self-defense；把来源／假设／观测／推论集中成表。
2. 给原 full PDF 稳定版本标识，更新直接后续工作，保留 publication status 的准确区分。
3. 用更不易与原文混淆的 occurrence token 命名；在图中标出 receiver event 是 model-local。
4. 如有独立需要，再研究 key rotation、多个 credentials、distributed admission、slot-indexed game、arbitrary batch。不要为扩大篇幅机械增加范围。

**本轮建议不是“继续润色就能投稿”。** 优先解决的是选题的非平凡性和 source-to-model 连接；否则新增完整日志、更多图、更多 disclaimer 只能让一个正确的小命题更工整。

## 13. Final Answer to One Question

> 基于当前证据，这篇论文最稳妥、最准确、不会过度声称的核心结论应该是什么？

K-Waay 原构造已经明确要求一次 BatchReceive 的不同输入来自不同 party。本文在具有新鲜消息、理想来源匹配和固定两槽顺序处理的 admission 抽象中，验证了仅约束消息不重复，即使足以排除同一 sender origin 在该批次中的重复接受，也不能推出不同输入来自不同 party；直接维护 party 不等关系可以在保留合法执行的同时满足相应结构不变量。这一结果说明的是给定抽象下 admission 条件的非替代性，以及集成契约需要明确其 party 关系；它没有证明合规 K-Waay 存在漏洞、原证明遗漏假设、密码学 identity binding 失效，或真实接收方及上层应用受到攻击。
