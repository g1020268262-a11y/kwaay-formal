# 《计算机应用研究》中文稿适配第1阶段报告

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_1`  
日期：2026-10-01（Asia/Shanghai）

## 1. 已阅读资料

### 英文母稿

已阅读 `manuscript/` 当前完整论文组织，包括：

- `main.tex`、`paper-content.tex`、metadata/preamble/venue 入口；
- Abstract、Introduction、Sections 2–8；
- `model-comparison.tex`、`verification-results.tex`；
- `attack-trace.tex`、`identity-control-comparison.tex`；
- trace details、exact model properties、reproducibility 三部分附录；
- `references.bib` 及论文写作/审查说明。

母稿目前是英文、多文件 LaTeX、匿名版本。其主线是固定两槽的 R/M/P 接纳比较；其 Appendix C 仍写“没有独立重跑/raw transcript”，已经被后来的独立 reviewer evidence 更新，不能原样进入中文稿。

### 《计算机应用研究》资料

已阅读：

- `submissions/arocmag/README.md`；
- `notes/AROCMAG_SETUP_REPORT.md`；
- `notes/SUBMISSION_REQUIREMENTS.md`；
- `notes/TEMPLATE_AUDIT.md`；
- `notes/SOURCE_MANIFEST.tsv`；
- 官方投稿模板 `.doc` 的审计记录和官方参考文献 PDF 的已核规则。

与本阶段结构直接相关的要求是：期刊暂不刊登英文稿；初投推荐 Word `.doc/.docx`；中英文摘要和关键词对应；公式使用 MathType；图尽量采用可编辑矢量图/EMF；参考文献按首次引用顺序并遵循其 GB/T 7714—2005 口径；正式出版正文双栏而初投可通栏。官网未公布全文页数/字数上限，因此本阶段没有设定强制页限。

### 审稿、独立复核和模型

已阅读：

- `reviews/2026-09-16-adversarial-review.md`，重点核对 M1–M7 和逐章审查；
- `reviews/2026-09-16-evidence/` 的 README、manifest、14 行结果比较、raw stdout/stderr、trace audit、7 个 JSON graphs、hash 和 K-Waay full PDF；
- `tamarin/rq-v2-minimal/` 的三个权威 `.spthy` 模型及全部 lemma。

独立复核在 commit `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57` 的 clean worktree 上使用 Tamarin 1.12.0 / Maude 3.5.1，对三个未改模型完成 parse/prove：14/14 状态与 steps 全部匹配，13 verified、1 falsified。该证据证明当前抽象结果可重复；它不是历史日志恢复，也不证明抽象与完整 K-Waay 的 refinement。

## 2. 最终推荐结构

推荐采用：

```text
0 引言
1 K-Waay批处理接纳及参与方区分问题
  1.1 K-Waay的BatchReceive接口
  1.2 身份坐标与批内参与方区分
  1.3 研究问题、对手能力与证据终点
2 批处理接纳机制的符号建模
  2.1 源接口到符号模型的映射
  2.2 共同生命周期和两槽范围
  2.3 三种接纳语义
  2.4 性质、运行证据与复核口径
3 形式化验证与结果分析
  3.1 宽松模型：精确origin重复接受
  3.2 消息级模型：排除精确重复但不保证party区分
  3.3 参与方级模型：safety与non-vacuity
  3.4 当前规则下的P/M/I关系与结果汇总
4 讨论与局限性
  4.1 批处理组合关系的不可替代性
  4.2 K-Waay接口动机与条件性设计启示
  4.3 建模和复现边界
5 结束语
```

该结构保留用户给出的六章骨架，并做三项调整：用“接纳”限定模型层次；把 Threat Model 并入问题定义/建模；把 Related Work 压入引言和讨论，不再单独成章。0 引言成稿不设下级标题。详细公式、图表、来源和正文比例见 `outline/CHINESE_PAPER_OUTLINE.md`。

## 3. 与英文母稿的映射情况

- Abstract → 中英文摘要：`KEEP + REWRITE + SHORTEN`。
- Introduction → 0 引言：`KEEP + MERGE + REWRITE + SHORTEN`。
- Section 2 → 第 1 章：`KEEP + MERGE + REWRITE`。
- Section 3 → 第 1、2、4 章：`KEEP + MERGE + REWRITE + SHORTEN`。
- Section 4 → 第 2 章：`KEEP + MERGE + REWRITE + SHORTEN`。
- Section 5 → 第 3 章：`KEEP + REWRITE + SHORTEN`。
- Section 6 → 第 4 章和结束语：`KEEP + MERGE + REWRITE + SHORTEN`。
- Section 7 → 引言和讨论：`KEEP + MERGE + SHORTEN`。
- Conclusion → 第 5 章：`KEEP + REWRITE + SHORTEN`。
- Appendices → 正文关键证据 + 附录/补充材料候选：`KEEP + SHORTEN + MOVE_TO_APPENDIX`；reproducibility 内容还需 `REWRITE`。

没有将定义、威胁假设、机器结果或局限性直接删除。逐项路径和标签见 `outline/SECTION_MAPPING.md`。

## 4. 核心贡献的建议中文表述

建议将贡献压缩为以下三点，并在引言中明确它们属于固定两槽接纳抽象：

1. `构造具有共同发送来源和顺序处理生命周期的三种接纳模型，对无坐标限制、消息级限制和参与方级限制进行受控比较。`
2. `机器结果表明，宽松模型允许一个精确sender origin在同一batch context中支持两次接受；消息级模型虽排除该模式并满足当前作用域内的消息区分/occurrence injectivity，仍允许同一参与方的两条不同消息共同被接受。`
3. `参与方级模型验证了接受端的party distinction，并保留一个可达的有效不同参与方批次；由此得到的有限启示是，按参与方解释批内位置的接口需要显式维护相应participant relation。`

同时必须紧接着说明：`P_tau => M_tau <=> I_tau` 是当前 freshness/origin 规则的人工推导，不是新增 Tamarin lemma；`M_tau !=> P_tau` 由 M witness 支持。P safety 是公开 guard 的正控制，不应包装成定义之外的密码学发现。

## 5. 必须保留的形式化结果

| 模型 | 性质 | 结果 | steps | 中文稿用途 |
|---|---|---:|---:|---|
| R | `normal_relaxed_batch_exists` | verified | 10 | 基本可执行性，简述 |
| R | `one_send_two_accepts_exists` | verified | 13 | 核心负向 witness |
| R | `receiver_accept_has_send` | verified | 8 | 理想 origin correspondence |
| R | `receiver_accept_injective` | falsified | 13 | 核心反例 |
| M | `repeated_message_rejection_exists` | verified | 4 | 仅 rejection branch 可达 |
| M | `same_party_different_messages_batch_exists` | verified | 16 | 核心 non-implication witness |
| M | `accepted_batch_has_distinct_messages` | verified | 31 | 与 scoped injectivity 合并解释 |
| M | `receiver_accept_has_send` | verified | 8 | 理想 origin correspondence |
| M | `receiver_accept_injective` | verified | 33 | 依赖当前 freshness/origin 规则 |
| P | `same_party_rejection_exists` | verified | 5 | 仅 rejection branch 可达 |
| P | `distinct_party_batch_exists` | verified | 17 | non-vacuity |
| P | `accepted_batch_has_distinct_parties` | verified | 31 | party safety 正控制 |
| P | `receiver_accept_has_send` | verified | 8 | 理想 origin correspondence |
| P | `receiver_accept_injective` | verified | 33 | P 蕴含链的一致性结果 |

两条 rejection lemma 的前置 Send 与被拒 tuple 未绑定；图中还可出现无关 Send。中文稿必须保留这一限制。完整主张—证据映射见 `outline/CLAIM_EVIDENCE_MATRIX.md`。

## 6. 第一轮审稿问题的处理方案

### M1：研究非平凡性

表述层能做的是降低贡献口径：把文章定位成 protocol-specific、fixed-two-slot 的 formal semantic case study；P 只作正控制；14 个结果不拆成 14 项发现。此举能修正过度包装，但不能消除研究增量不足的发表风险。如果需要更强论文，必须另行找到真实的 message-level substitute/implementation practice 或独立结果谓词，并形成新的协议相关分析；本阶段不制造这类证据。

### M2：协议抽象差距

将 source-to-abstraction mapping 放到第 2 章主线，明确 `!Sent` 是无 recipient/prekey/context 的理想 origin oracle，模型既可能允许不可实现行为，也可能排除真实行为，不能称天然保守。当前结论止于 `ReceiverAccept`。若要提升为协议反例，需要另行增加相关接收上下文/密码操作并建立 simulation/refinement；本阶段只作为明确局限。

### M3：消息区分与occurrence injectivity依赖

直接落实为公式 `P_tau => M_tau <=> I_tau`、`M_tau !=> P_tau`，前者标为规则层人工推导，后者由 M witness 支持。消息 safety 与 scoped injectivity 不再作为两项独立贡献。

### M4：K-Waay-specific interface motivation

第 1.1 和 4.2 将加入原算法按 `j` 处理 `(pk_j,prek_j,m_j)`、形成 `k_j` 并返回 `{k_j}_j` 的事实，以及 game 使用 party/component 索引的动机。当前模型没有这些输出和查询，因此只说明 party coordinate 为何值得研究；不能主张 cryptographic necessity、输出歧义或 game 失效。

### M5：rejection witness未绑定输入

正文把两条结果降为“拒绝分支可达”，不写成“给出的两条合法 sender 消息被拒”。若将精确拒绝行为升级为贡献，需要新增 entry-bearing event/绑定 witness 并重跑模型；不在本阶段完成。

### M6：authority分叉

中文稿统一使用“party projection 的非单射/其他坐标不可替代 party relation”，不再用“来源归属含糊”。`slot -> party` 仍然有定义；只有未建模的反向 party-to-slot/output selection 才可能产生选择问题。

### M7：reproducibility/provenance

以新 reviewer rerun 作为独立复核证据，保留 commit、clean state、工具版本、输入 hash、exit status、raw outputs、graphs 和 match。它必须以 2026-09-16 新证据发布，不能写成找回旧运行日志；也不能用 reproducibility 替代 protocol validity 或 novelty。

## 7. 合并与缩减内容

计划合并：

- Section 2/3 的 identity coordinates、目标和对手；
- Section 4 与 Appendix B 的共同模型语义和关键性质；
- Section 5/6 中反复解释的 M non-implication；
- Section 6 的 authentication、replay、dedup 和 enforcement 讨论；
- Section 7 的五节 related work 到引言/讨论两处；
- 六类 limitations 到 4.3 一处。

计划缩减：英文 paper roadmap、逐 lemma 散文复述、逐规则 trace 清单、对同一证据边界的多次防御性说明、MLS/misbinding/UKS 的长篇分类讨论。所有被压缩内容的事实级保留点已写入 `outline/CONTENT_REDUCTION_PLAN.md`。

## 8. 计划保留的图表

1. **图 1**：`K-Waay BatchReceive输入条目、索引输出与参与方投影关系` / `Input Entries, Indexed Outputs, and Party Projections in K-Waay BatchReceive`。后续新绘，只复述有来源的接口事实并标出 abstraction boundary。
2. **图 2**：`宽松接纳模型中的代表性精确origin重复接受执行` / `Representative Exact-Origin Duplicate-Acceptance Execution in the Relaxed Model`。由现有 TikZ 图和独立复核 graph 重制，caption 明示人工整理，不能称为直接导出的攻击图。
3. **表 1**：`三种两槽接纳模型的语义比较` / `Admission Semantics of the Three Two-Slot Models`。
4. **表 2**：`三个接纳模型的Tamarin验证结果及独立复核` / `Tamarin Verification Results and Independent Reproduction for the Three Admission Models`，保留 14 行、steps 和 match。
5. **source-to-abstraction 表**：从 M2 风险看强烈建议保留；若版面不足，可改为结构化正文，但不能删除其事实。

现有 `identity-control-comparison` 图与表 1、`P/M/I` 公式重复，建议合并而不单独保留。

## 9. 后续Word转换风险

- 官方模板是 `.doc`，当前稿是多文件 LaTeX；不能靠自动转换保证样式、单双栏、页眉页脚、交叉引用和公式编号正确。
- 官方要求 MathType；现有 LaTeX 公式需逐式重录和对照模型，不能用公式图片代替。
- TikZ 图需重绘为可编辑矢量图/EMF；EMF 字体、线宽和双语题注需要 Word 内逐页检查。
- 当前 BibTeX 使用 `plain`；22 条现有文献需按首次引用顺序和官方 GB/T 7714—2005 口径逐条转换，不能机械套用其他年份国标或 IEEE/ACM 样式。
- 中文摘要的“200字以内/200～300字”公开口径冲突；需先确定执行口径。
- 作者、单位、通信作者、手机号、基金、作者简介只能由用户确认后填写；不能从匿名稿或历史目录猜测。
- 投稿后作者自行替换稿件受限，正式制作前应先冻结 author metadata 和 claim wording。

本阶段没有执行任何 Word、MathType、EMF 或参考文献转换。

## 10. 尚需用户确认的问题

进入完整中文正文或 Word 阶段前，需要确认：

1. 是否接受“窄的受控形式语义案例”作为当前稿件定位，并知悉 M1 的发表价值风险不能仅靠改写消除；
2. 中文/英文题名是否采用本阶段候选，或提供作者偏好的题名；
3. 是否在下一阶段先写中文 Markdown 分节稿，再进入官方 Word 模板；
4. 中文摘要采用“200字以内”还是“200～300字”的工作口径；
5. 是否保留正文 source-to-abstraction 第 3 张表；
6. 是否需要向编辑部另行确认附录/补充材料、匿名初审和特殊文献类型；本阶段未发送邮件；
7. 正式作者顺序、单位、通信作者、手机号、邮箱、基金和作者简介；未提供前继续保留占位而不猜测。

## 11. 边界核验与结论

本阶段只在 `submissions/arocmag/draft/` 创建结构、映射、证据矩阵、精简计划和本报告。没有修改 `manuscript/`、`tamarin/`、`docs/`、`artifact/`、`reviews/`、`results/`、`archive/`、`submissions/formalise2027/`、`submissions/arocmag/official/`、`submissions/arocmag/snapshots/` 或既有 `submissions/arocmag/notes/`；没有运行 Tamarin、转换 Word、投稿、发邮件、commit 或 push。

第 1 阶段结构与证据控制文件已经足以支持下一阶段逐节中文改写。`READY` 只表示结构设计完成，不表示研究贡献风险已解决、全文已适配或稿件已达到投稿状态。

**AROCMAG_STRUCTURE_READY**

