# AROCMAG 风格研究与最终蓝图修订报告

## 1. 样本与全文状态

风格研究分析 7 篇《计算机应用研究》安全协议/形式化验证论文，共 52 个正式排版页。7 篇均取得期刊官网正式版全文；只看摘要的论文为 0，`FULL_TEXT_NOT_AVAILABLE` 为 0。

## 2. 样本权重

### 第一层：主要结构参考

- P1《基于 Tamarin 的 MQTT 协议安全性分析方法》；
- P2《基于安全协议代码的形式化辅助建模研究》。

P1/P2 与当前 Tamarin 语义分析最接近，主要用于决定建模章节、安全属性、攻击者说明、结果节奏和图表功能。

### 第二层：总体中文安全论文风格参考

P3～P7 主要用于观察中文引言、章节压缩、数学表达、安全分析措辞、图表版式和结束语。其 ROR/BPR 证明、注册/认证流程和性能比较是内容特例，不构成 K-Waay 的结构要求。

## 3. 仍然有效的主要观察

- 样本多为 6～9 页，但这一分布不是稿件硬约束。
- 5/7 在引言完成主要 related work；独立 Threat Model 一级章为 0/7。
- 形式化论文通常采用“协议/问题 → 模型与属性 → 验证结果与解释”的主线。
- Tamarin 类论文公式密度低于 ROR/BPR 论文；工具结果通常由表格压缩，正文解释关键成功和失败。
- Discussion 与 Limitations 是否独立受研究对象影响；K-Waay 需要一个紧凑讨论章来承载身份坐标含义、维护责任和集中边界。
- 图表数量由论证功能决定，不能从 46 幅图、27 张表的样本总数反推硬配额。

原始分析证据保留在：

- [REFERENCE_PAPER_MATRIX.md](REFERENCE_PAPER_MATRIX.md)
- [INTRODUCTION_PATTERN_ANALYSIS.md](INTRODUCTION_PATTERN_ANALYSIS.md)
- [FORMAL_ANALYSIS_PATTERN.md](FORMAL_ANALYSIS_PATTERN.md)
- [FORMULA_STYLE_ANALYSIS.md](FORMULA_STYLE_ANALYSIS.md)
- [FIGURE_TABLE_STYLE_ANALYSIS.md](FIGURE_TABLE_STYLE_ANALYSIS.md)
- [RESULT_NARRATIVE_ANALYSIS.md](RESULT_NARRATIVE_ANALYSIS.md)

上述六份文件按任务要求不修改，保留风格研究形成时的分析快照；其中早期的复现/原始 transcript 表述已由本报告、第 6 节和最终蓝图的统一 provenance 取代。

## 4. 冻结的中文结构

```text
0 引言

1 K-Waay批处理接纳与参与方区分问题
  1.1 BatchReceive机制与不同参与方条件
  1.2 身份坐标与问题实例
  1.3 研究问题

2 批处理接纳的形式化建模
  2.1 安全目标与攻击者模型
  2.2 Tamarin模型与共同生命周期
  2.3 接纳配置与验证性质

3 形式化验证与结果分析
  3.1 放宽参与方条件后的重复接受
  3.2 消息级限制的替代性
  3.3 参与方级条件下的性质验证
  3.4 综合验证结果

4 结果讨论与适用范围
  4.1 消息区分与参与方区分
  4.2 批处理接口的维护责任
  4.3 适用范围与局限

5 结束语
```

五个正文一级章依次回答：研究对象和问题是什么；如何形式化；机器验证得到什么；结果意味着什么且不能意味着什么；最终结论是什么。

## 5. 本次关键修订

1. 删除引言 roadmap，固定为背景、K-Waay、三组相关工作、缺口、方法/结果、三点贡献六段。
2. 以 P1/P2 为结构主参考，P3～P7 降为总体中文风格参考。
3. 术语从笼统“批接收/准入”统一为冻结标题中的“批处理接纳”；条目记号改用 `oid`，并明确映射到模型 `sid`。
4. 三个模型重写为同一骨架上的三种接纳配置，不作为三套协议或论文创新主线。
5. 第 3 章设为全文核心，3.2 必须由同一参与方/不同消息的机器见证支撑中心分离结论。
6. 正文表 3 从完整 14 行改为 7 项关键结果；完整 14 项仍保留在附属/复现材料。
7. 独立编号公式压缩为条目、目标关系、核心反例事件链三项。
8. Scope/non-goal 只放 2.1、3.1、4.3 三处。
9. 图表冻结为 2 幅核心论证图和约 3 张主表的功能需求，不把样本均值变成硬数量。
10. 复现事实更新为 2026-09-16 后续独立 reviewer rerun。

## 6. 统一复现事实

2026-09-16，后续独立 reviewer rerun 在 Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu-24.04 下对三个未修改模型完成 parse/prove；14/14 项 lemma 的结果状态与 proof steps 均与既有记录一致，并保存原始 stdout/stderr、manifest、模型及输出哈希和 7 个导出 graph。该复跑是新的 reviewer-generated evidence，不是历史运行日志恢复；它证明当前抽象结果可复现，不建立完整 K-Waay refinement，也不扩大协议级或部署级安全结论。

证据目录为 `reviews/2026-09-16-evidence/`。正文 3.4 只保留环境、三个未修改模型和 14/14 状态/步数匹配这一句；其他细节留在复现材料。

## 7. 结果表决定

正文主表突出 7 项：

- relaxed：精确来源重复接受 exists；scoped injectivity falsified；
- message-level：distinct messages verified；scoped injectivity verified；same-party/different-message exists；
- party-level：party distinction verified；valid distinct-party batch exists。

其余 7 项合并为 supporting properties。完整 14 项状态与 steps 保留，详见 [FULL_14_RESULT_PLACEMENT_DECISION.md](FULL_14_RESULT_PLACEMENT_DECISION.md)。

## 8. 图表与公式

当前研究最少需要 2 幅核心论证图和约 3 张主表；数量由信息功能决定，不因样本平均数强制增减。

- 图 1：两槽批组成与接纳生命周期；
- 图 2：放宽条件下的精确来源重复接受轨迹；
- 表 1：身份坐标与模型映射；
- 表 2：三种接纳配置与验证目标；
- 表 3：关键 Tamarin 验证结果。

`identity-control-comparison` 不再作为独立图。正文核心编号公式只保留 (E_i=(A_i,oid_i,m_i))、`DistinctPartyPerBatch(B)` 和核心反例事件链。

## 9. 页数和未决事项

参考样本多为 6～9 页，当前稿件优先保证论证完整，最终页数由实际版面决定。仍需在下一阶段确认：

- 中文 LaTeX 实际排版页数；
- 期刊投稿系统是否允许附属材料；
- 若不允许，完整 14 项结果采用正文压缩表还是文后附表；
- 图 1、图 2 的正式绘制和双栏可读性。

这些事项不改变已冻结的章节和论证顺序。

## 10. 交付物

- [FINAL_CHINESE_PAPER_BLUEPRINT.md](FINAL_CHINESE_PAPER_BLUEPRINT.md)：最终冻结蓝图；
- [AROCMAG_STYLE_GUIDE_FOR_KWAAY.md](AROCMAG_STYLE_GUIDE_FOR_KWAAY.md)：写作节奏约束；
- [KWAAY_SECTION_RESTRUCTURING_PLAN.md](KWAAY_SECTION_RESTRUCTURING_PLAN.md)：英文到中文映射；
- [FULL_14_RESULT_PLACEMENT_DECISION.md](FULL_14_RESULT_PLACEMENT_DECISION.md)：14 项结果位置决定；
- [BLUEPRINT_REVISION_REPORT.md](BLUEPRINT_REVISION_REPORT.md)：本次修订与自检。

本次未生成中文正文、正式图、Word，未修改英文母稿、中文 LaTeX 或 Tamarin 模型，也未 commit/push。

**AROCMAG_FINAL_BLUEPRINT_READY**

