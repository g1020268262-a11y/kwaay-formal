# AROCMAG 最终蓝图修订报告

## 1. 修改范围

本次只修改以下规划文档：

- `FINAL_CHINESE_PAPER_BLUEPRINT.md`；
- `AROCMAG_STYLE_GUIDE_FOR_KWAAY.md`；
- `KWAAY_SECTION_RESTRUCTURING_PLAN.md`；
- `STYLE_STUDY_REPORT.md`。

新增：

- `FULL_14_RESULT_PLACEMENT_DECISION.md`；
- `BLUEPRINT_REVISION_REPORT.md`。

按任务边界未修改 `REFERENCE_PAPER_MATRIX.md`、`INTRODUCTION_PATTERN_ANALYSIS.md`、`FORMAL_ANALYSIS_PATTERN.md`、`FORMULA_STYLE_ANALYSIS.md`、`FIGURE_TABLE_STYLE_ANALYSIS.md`、`RESULT_NARRATIVE_ANALYSIS.md`。这些文件保留原始风格研究快照；其中早期 provenance 句子由修订后的四份规划文档和本报告明确取代，不作为下一阶段写作依据。

## 2. 已冻结的结构

一级、二级标题已严格冻结为：

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

未保留独立 Related Work、Threat Model 或 Limitations 一级章。

## 3. 修订结果

### 引言

- 删除文章结构 roadmap；
- 固定为背景、K-Waay、三组相关工作、缺口、方法/结果、三点贡献六段；
- 不在引言重复 scope/non-goal；
- 不以 Tamarin 或三种配置开场。

### 样本权重

- P1/P2 作为 Tamarin 建模和结果组织的主要参考；
- P3～P7 仅作为中文安全论文总体风格参考；
- 删除从认证协议流程、性能图和 ROR 证明向 K-Waay 机械迁移的可能性。

### 模型与叙事

- R/M/P 改称放宽、消息级、参与方级三种接纳配置；
- 明确三者共享完全相同的处理骨架；
- 配置是回答研究问题的方法，不是三套新协议或创新主线；
- 参与方级配置只称 positive control，不称 repair/fix。

### 结果

- 第 3 章固定为全文最大篇幅；
- 3.1 围绕精确来源重复接受和 injectivity 反例；
- 3.2 以机器见证支撑消息级非替代性；
- 3.3 以目标性质和有效批次说明 positive control 与非真空性；
- 正文表 3 突出 7 项，完整 14 项保留在附属/复现材料。

### 公式与图表

- 独立编号公式压缩为条目、目标关系、核心反例事件链三项；
- `oid` 显式映射到现有模型 `sid`，不修改模型；
- 冻结 2 幅核心图和约 3 张主表的功能需求；
- `identity-control-comparison` 不再是独立图；
- 本任务未生成任何正式图表。

### 篇幅

- 删除原先的刚性页数区间；
- 改为“参考样本多为 6～9 页，当前稿件优先保证论证完整，最终页数由实际版面决定”；
- 图表数量由论证功能决定，不由样本平均数决定。

## 4. 统一 provenance

2026-09-16，后续独立 reviewer rerun 在 Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu-24.04 下对三个未修改模型完成 parse/prove；14/14 项 lemma 的结果状态与 proof steps 均与既有记录一致，并保存原始 stdout/stderr、manifest、模型及输出哈希和 7 个导出 graph。该复跑是新的 reviewer-generated evidence，不是历史运行日志恢复；它证明当前抽象结果可复现，不建立完整 K-Waay refinement，也不扩大协议级或部署级安全结论。

该事实已写入四份可修改规划文档。早期关于复现材料缺失和未做独立复核的否定性表述已从这些生效中的规划文档移除。六份禁止修改的原始分析文件仍保留形成时文字，但已在 `STYLE_STUDY_REPORT.md` 中标为历史分析快照，其 provenance 由本节取代。

## 5. Scope/Non-goal 管理

明显边界说明只冻结在：

1. 2.1 的局部模型边界；
2. 3.1 的反例解释边界；
3. 4.3 的完整限制和复跑边界。

引言无 Scope 段；3.2/3.3 不重复免责声明；结束语不重复限制清单。

## 6. 十项自检

| 检查项 | 结果 | 证据 |
|---|---|---|
| 1. 是否仍使用旧 no-transcript/no-rerun 事实 | 通过 | 四份生效规划文档均更新为 2026-09-16 独立复核；原始分析快照明确被取代 |
| 2. 是否仍有英文论文 roadmap | 通过 | 引言明确禁止逐章安排，第 6 段后直接进入第 1 章 |
| 3. 是否把 7 篇样本等权处理 | 通过 | P1/P2 第一层，P3～P7 第二层 |
| 4. 是否把 R/M/P 作为论文主线 | 通过 | 改为三种受控接纳配置，主线是 different-party condition 的语义 |
| 5. 是否仍有过多独立公式 | 通过 | 只冻结 3 个编号公式 |
| 6. 是否让 14 个 lemma 代码名占据中心 | 通过 | 主表 7 项且自然语言优先，完整 14 项外置保留 |
| 7. 是否重复 scope 说明 | 通过 | 只允许 2.1、3.1、4.3 三处 |
| 8. 是否与英文母稿技术内容冲突 | 通过 | 保留三个配置、事件、性质与边界；`oid ↔ sid` 显式映射 |
| 9. 是否与 Tamarin 证据冲突 | 通过 | 14 项状态/steps 取自 `result-comparison.tsv`，13 verified、1 falsified |
| 10. 是否符合 P1/P2 的节奏 | 通过 | 问题/模型与属性/结果解释为主，工具代码和完整结果退居表格/复现材料 |

## 7. 文件边界检查

没有修改 `manuscript/`、`tamarin/`、`reviews/`、现有中文 LaTeX、Word 或正式图。没有 commit/push。

## 8. 最终状态

**AROCMAG_FINAL_BLUEPRINT_READY**

