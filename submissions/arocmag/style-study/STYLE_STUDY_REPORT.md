# AROCMAG 论文风格与结构研究报告

## 1. 完成范围

本研究实际分析 7 篇《计算机应用研究》安全协议/形式化验证论文，共 52 个正式排版页。7 篇均取得期刊官网 `version=v2` 正式全文并逐页检查；只看摘要的论文为 0，`FULL_TEXT_NOT_AVAILABLE` 为 0。样本覆盖 Tamarin、形式化辅助建模、ProVerif、ROR/BPR 可证明安全、后量子口令认证和多因素认证。

## 2. 主要统计结论

- 单篇 6～9 页，中位数 7 页；一级章通常 5～7 个。
- 5/7 在引言中完成主要 related work，2/7 单列“相关工作”。
- 0/7 将 Threat Model 设为独立一级章；4/7 设置明确的攻击者/威胁模型小节。
- 0/7 单列 Discussion，0/7 单列 Limitations。
- 7/7 使用紧凑结束语，通常 1～2 段。
- 共 46 幅图、27 张表；图承担系统/流程/状态机/工具结果/性能功能，表承担符号、安全性质、机器结果和性能比较。
- Tamarin 论文公式密度低，以状态机、性质表和轨迹为主；高公式密度主要出现在 RLWE 与 ROR/BPR 证明。
- 结果的稳定顺序为“对象/性质 → 机器或数学结果 → 安全含义”，完整结果由表压缩，正文只展开代表性成功和失败。

详细证据见：

- [REFERENCE_PAPER_MATRIX.md](REFERENCE_PAPER_MATRIX.md)
- [INTRODUCTION_PATTERN_ANALYSIS.md](INTRODUCTION_PATTERN_ANALYSIS.md)
- [FORMAL_ANALYSIS_PATTERN.md](FORMAL_ANALYSIS_PATTERN.md)
- [FORMULA_STYLE_ANALYSIS.md](FORMULA_STYLE_ANALYSIS.md)
- [FIGURE_TABLE_STYLE_ANALYSIS.md](FIGURE_TABLE_STYLE_ANALYSIS.md)
- [RESULT_NARRATIVE_ANALYSIS.md](RESULT_NARRATIVE_ANALYSIS.md)

## 3. 推荐的 K-Waay 中文结构

唯一推荐结构为：

0 引言

1 K-Waay 批接收的身份约束  
1.1 BatchReceive 接口与不同参与方条件  
1.2 身份坐标与最小问题实例  
1.3 研究问题与分析目标

2 批组成的形式化建模  
2.1 安全目标与批组成攻击者  
2.2 共同两槽生命周期与源抽象  
2.3 受控准入变体与安全性质

3 Tamarin 验证结果与分析  
3.1 放宽准入的重复发生反例  
3.2 消息级限制的对照结果  
3.3 参与方级约束的恢复结果  
3.4 结果汇总与语义解释

4 讨论  
4.1 身份坐标的非蕴含关系  
4.2 组合不变量与执行责任  
4.3 适用范围与局限

5 结束语

逐节目的、英文来源、公式、图表、篇幅和节末结论见 [FINAL_CHINESE_PAPER_BLUEPRINT.md](FINAL_CHINESE_PAPER_BLUEPRINT.md)。

## 4. 推荐图表

正文推荐 2 幅图、3 张主表：

- 图 1：两槽批组成与准入生命周期；
- 图 2：放宽模型的重构抽象反例轨迹；
- 表 1：身份坐标、源语义、模型表示和解释边界；
- 表 2：三种准入变体、约束坐标、分析角色和性质；
- 表 3：14 条 Tamarin 记录结果及论证作用。

现有 `identity-control-comparison.tex` 的内容建议转为表 2。没有运行时、通信或存储实验，不设置性能图。样本文中的工具截图不应被机械仿制；K-Waay 应继续把反例图标明为基于模型和执行记录的重构图。

## 5. 对英文母稿的调整建议

1. 把独立 Related Work 的五个小节压缩并吸收入引言。
2. 把独立 Security Objective and Threat Model 合入形式化建模的 2.1。
3. 合并身份坐标、source-to-abstraction 和模型条目的重复定义。
4. 将 relaxed/message-level/party-level 定位为同一实验设计中的基线、替代对照和正控制，不称为三套协议。
5. 保留核心不变量、最小问题实例、反例事件链和中心非蕴含；将重复不等式与规则条件移入表格。
6. 保留 14 条记录结果的完整主表，正文只展开三条证据链。
7. 将 scope/non-goal 分为：2.1 的必要局部边界、3.1 的反例边界、4.3 的完整限制；删除其他重复。
8. 将英文 Discussion 的六个小节压缩为三个中文小节，维持解释性贡献但缩短篇幅。
9. 保留 recorded executions、版本、哈希和无原始 transcript 的 provenance，不写成重新运行。

完整映射见 [KWAAY_SECTION_RESTRUCTURING_PLAN.md](KWAAY_SECTION_RESTRUCTURING_PLAN.md)，写作规则见 [AROCMAG_STYLE_GUIDE_FOR_KWAAY.md](AROCMAG_STYLE_GUIDE_FOR_KWAAY.md)。

## 6. 尚不确定的事项

- 本研究从同类论文归纳写作节奏，没有据此推定编辑部的官方页数、图表数量或章节强制要求；正式改写前仍应以最新投稿须知和模板为准。
- 中文 LaTeX 版的实际页数只有在正文重写、参考文献和图表定稿后才能确认。
- 图 1 尚未绘制；本任务按边界只规定其信息功能和放置位置。
- 本任务没有重新运行 Tamarin；机器结论仍以项目中已有执行记录、模型哈希和证据边界为准。
- 若期刊在线系统对补充材料有限制，完整 lemma、命令、哈希和 trace provenance 的承载位置需在投稿制作阶段确认。

## 7. 交付物

本目录包含任务要求的 10 份 Markdown 文档和 7 份用于核查的正式版参考 PDF。未修改 `manuscript/`、`tamarin/`、`docs/`、`artifact/` 或其他投稿目录，未生成中文论文正文、Word 或正式图，也未 commit/push。

**AROCMAG_STYLE_STUDY_READY**

