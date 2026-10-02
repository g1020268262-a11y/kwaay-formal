# 《计算机应用研究》中文稿适配第3阶段报告

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_3`  
日期：2026-10-02（Asia/Shanghai）

## 1. 本阶段新增和修改的文件

修改：

- `sections/02-symbolic-modeling.md`：仅完成任务指定的两处小修订。

新增：

- `sections/03-formal-analysis.md`；
- `figures/FIGURE_2_SPEC.md`；
- `notes/STAGE3_EVIDENCE_AUDIT.md`；
- `notes/STAGE3_SELF_REVIEW.md`；
- `notes/ADAPTATION_STAGE3_REPORT.md`。

未修改模型、英文母稿、reviews/evidence、Stage 1/2 审计、官方材料或其他目录；未运行 Tamarin，未制作 Word，未 commit/push。

## 2. 第三章各小节完成情况

### 3.1 宽松接纳模型中的精确来源重复接受

完成 R 的基本可达性、精确来源重复接受见证、来源对应性和 injectivity 反例分析。正文明确区分一个精确匹配的 Send、同一三元组进入两个槽、同一 $(bid,rst)$ 下两个不同时间点的 `ReceiverAccept`，并说明公式的唯一性条件不排除无关 Send。结果被限定为 batch-local exact-origin injectivity 反例，没有升级为 K-Waay AKE 或部署攻击。

### 3.2 消息级接纳模型的限制与反例

完成 M 的消息接纳条件、消息区分、scoped injectivity、origin correspondence 和 same-party/different-message witness 分析。核心执行明确绑定同一参与方的两个不同 $oid/m$ 来源和两个接受事件，从实际模型行为说明消息区分不蕴含参与方区分。正文排除了 origin mismatch、身份错误归属、UKS、misbinding、密钥泄露及合规 K-Waay 输入域攻击等无证据结论。

### 3.3 参与方级接纳模型的性质验证

完成 P 的参与方 safety、distinct-party non-vacuity、origin/injectivity 支持性质及 rejection 限制分析。P 明示为直接维护目标关系的正控制；non-vacuity 只证明至少一个有效双接受执行，不扩大为所有合法批次最终完成。

### 3.4 综合结果与性质关系分析

新增完整表 3，覆盖 14 个 model–lemma 实例的 Model、Lemma、Property Type、Outcome、Steps 和 Independent Rerun Match。正文说明独立复核运行环境、证据留存及历史 freeze/新 rerun 的来源区别，并解释 $P_\tau$、$M_\tau$、$I_\tau$ 的各蕴含方向和机器/人工证据边界。

## 3. 两处Stage 2小问题的修复结果

### 修复1：补全性质公式量词

$P_\tau$ 和 $M_\tau$ 现已完整量化参与方、发送实例、消息、batch/context 和时间点：

$$
\forall A_1,A_2,oid_1,oid_2,m_1,m_2,bid,rst,r_1,r_2.
$$

$r_1\ne r_2$ 已置于蕴含前件。两式与 `accepted_batch_has_distinct_parties/messages` 的源公式一致。

### 修复2：准确表达Reject映射

第 2.1 节表 1 已明确：K-Waay 的签名失败、split-KEM batch-wide failure 和 $\bot$ 返回在当前接纳抽象中没有直接对应物；M/P `Reject` 只表示消息或参与方接纳条件不满足。二者没有被解释成同一安全事件。

`git diff` 核对显示第 2 章只有上述两个修改 hunk。

## 4. 14项结果与独立复核的一致性

证据核查结果：

- `SHA256SUMS.txt` 中 24 个条目全部匹配；
- manifest 记录的 3 个模型哈希与当前源文件全部匹配；
- 7 次 version/parse/prove 调用均 exit 0；
- 三个 prove transcript 均通过 wellformedness checks；
- 14/14 项状态和 steps 与 `result-comparison.tsv` 一致；
- 总计 13 verified、1 falsified with trace；
- 三个 JSON 文件共包含 7 个 witness/counterexample graph。

未发现任务预期表、当前模型和独立证据之间的数字或状态不一致。证明 steps 仅作为运行对应元数据使用。

## 5. 核心反例与见证的解释

- **R witness**：同一精确 $(A,oid,m)$ 由一个唯一匹配来源产生，进入同一批次的两个槽，并在同一 $(bid,rst)$ 下产生两个不同接受事件。导出 graph 中的无关 Send 没有被误删为“不存在”。
- **R counterexample**：上述见证直接否定当前作用域内 exact-origin injectivity；它不是完整 AKE injective agreement 反例。
- **M witness**：同一 $A$ 的两个不同 $oid/m$ 来源各自支持一次接受，因此来源对应和消息区分均可成立，而参与方区分不成立。
- **P witness**：两个不同参与方及其来源完成同一批次的双接受，只用于证明正控制不是空真。
- **Rejection witness**：M/P 两项只报告抽象拒绝分支可达，不声称前置 Send 就是被拒条目。

## 6. P/M/I关系的论证状态

正文采用

$$
(P_\tau\Rightarrow M_\tau)
\land
(M_\tau\Leftrightarrow I_\tau),
\qquad
M_\tau\not\Rightarrow P_\tau.
$$

$P_\tau\Rightarrow M_\tau$、$M_\tau\Rightarrow I_\tau$ 和 $I_\tau\Rightarrow M_\tau$ 均明确标为依赖 fresh message、精确来源对应和共同 context 的人工规则推导，不是新增 Tamarin lemma。$M_\tau\not\Rightarrow P_\tau$ 由 M 的 all-traces message safety 与 same-party/different-message exists-trace witness 联合支持。

## 7. 图表完成情况

- **表3** 已完成，含全部 14 项结果和独立复核列，编号接续第 2 章的表 1、表 2。
- **图2** 已在正文预留中英文图题和 provenance 注记，并建立 `FIGURE_2_SPEC.md`。设计说明提供机器依据、事件主线、持久来源复用、可编辑 Mermaid 草图、正式重绘要求及禁止升级的含义。
- 当前未制作最终 Word 或出版级矢量图，符合本阶段边界。

## 8. 尚未解决的研究问题

1. 机器证据固定为两个槽位，没有任意有限批次的验证或归纳证明。
2. $!Sent$ 缺少 receiver/prekey/context binding，没有 source-to-model refinement。
3. message-level substitute 的现实规范或实现来源仍未建立。
4. K-Waay 重复 party index 下的输出选择和 `KEY/TEST` 扩展语义仍为 `NOT ESTABLISHED`。
5. rejection lemma 仍未绑定具体 rejected tuple，也没有活性性质。
6. 图 2 尚需在后续排版阶段转换为正式可编辑矢量图。
7. 研究增量和投稿竞争力风险仍需在全文完成后结合第 4 章讨论与局限性评估。

## 9. 与CLAIM_EVIDENCE_MATRIX的一致性

第三章逐项落实矩阵 C3～C11 和 C13：

- C3：三模型 origin correspondence；
- C4/C5：R 精确来源重复接受与 injectivity 反例；
- C6/C7：M safety 与同 party/不同 message witness；
- C8/C9：P safety 与 non-vacuity；
- C10：两条弱 rejection reachability；
- C11：受假设限制的 P/M/I 派生关系；
- C13：14/14 独立复核事实。

未引入矩阵 U1～U3 禁止的完整协议攻击、密钥后果、部署漏洞、任意批大小或 refinement 主张。自检未发现与矩阵冲突的表述。

## 10. 进入第4～5章的条件判断

第 0～3 章已经形成连续的“接口条件—坐标定义—符号模型—机器结果”证据链。第三章的结果表、见证解释、性质关系和 provenance 均已冻结到当前证据边界，因此在人工审阅本阶段稿件后，具备进入“4 讨论与局限性”和“5 结束语”写作的条件。

这里的 `READY` 不表示论文全文、图形、Word 排版或投稿包已经完成，也不消除上述研究增量与 refinement 风险。

**AROCMAG_STAGE3_READY**
