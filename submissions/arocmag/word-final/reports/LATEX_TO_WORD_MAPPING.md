# LaTeX to Word mapping

Scientific baseline: `54ad3723d1c509693693c8b5984c3b1b8bc006e1`

Word target: `K-Waay-AROCMAG-submission-working.docx`

| LaTeX位置 | Word位置 | 类型 | 内容状态 | 转换方法 | QA状态 |
|---|---|---|---|---|---|
| `preamble/metadata.tex` 中文标题 | 首页单栏顶部 | 标题 | 冻结，逐字迁移 | 官方中文标题样式 | PASS |
| `preamble/metadata.tex` 英文标题 | 首页英文信息区 | 标题 | 冻结，逐字迁移 | 官方英文标题样式 | PASS |
| 匿名作者元数据 | 首页中英文作者/单位区 | 元数据 | 未知信息未填写 | `作者信息待补`及英文对应占位 | AUTHOR_METADATA_PENDING |
| `sections/00-abstract.tex` 中文摘要 | 首页中文信息区 | 摘要 | 冻结，逐字迁移 | 官方摘要样式 | PASS |
| `sections/00-abstract.tex` 中文关键词 | 首页中文信息区 | 关键词 | 冻结，逐字迁移 | 官方摘要样式 | PASS |
| 官方模板分类字段 | 中文关键词后 | 投稿字段 | 无权威值 | 中图分类号、文献标志码、文章编号均显式待定 | AUTHOR_METADATA_PENDING |
| `sections/00-abstract.tex` 英文摘要 | 首页英文信息区 | Abstract | 冻结，逐字迁移 | 官方摘要样式 | PASS |
| `sections/00-abstract.tex` 英文关键词 | 首页英文信息区 | Key words | 冻结，逐字迁移 | 官方摘要样式 | PASS |
| `sections/01-introduction.tex` | `0 引言` | 一级正文 | 完整迁移 | 官方一级标题与正文样式 | PASS |
| 引言贡献1–3 | 引言末 | 编号列表 | 完整迁移 | 可编辑Word段落 | PASS |
| `sections/02-problem.tex` | `1 K-Waay批次准入与参与方互异问题` | 一级正文 | 完整迁移 | 官方一级标题样式 | PASS |
| `1.1 BatchReceive机制与批内参与方互异条件` | 1.1 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| 未编号输入向量 | 1.1 | 未编号公式 | 完整迁移 | 可编辑OMML，不编号 | PASS |
| `1.2 比较维度与问题实例` | 1.2 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `eq:abstract-entry` | 1.2，式(1) | 编号公式 | 内容与编号不变 | 可编辑OMML | PASS |
| `tables/identity-coordinate-map.tex` | 1.2，表1 | Word表格 | 6×5内容完整 | 原生Word三线表，全栏 | PASS |
| `1.3 研究问题` | 1.3 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| RQ1–RQ3 | 1.3 | 编号列表 | 三项内容完整 | 可编辑Word段落 | PASS |
| `sections/03-formal-modeling.tex` | `2 批次准入的形式化建模` | 一级正文 | 完整迁移 | 官方一级标题样式 | PASS |
| `2.1 安全目标与攻击者模型` | 2.1 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `eq:distinct-party-objective` | 2.1，式(2) | 编号公式 | 内容与编号不变 | 可编辑OMML | PASS |
| `2.2 Tamarin模型与共同生命周期` | 2.2 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `fig1-two-slot-lifecycle.tex` | 2.2，图1 | 图 | 科学图义冻结 | 当前PDF派生360 dpi占位图；图题为可编辑Word文本 | PASS / EMF_PENDING |
| `2.3 准入模型与验证性质` | 2.3 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `tables/admission-configurations.tex` | 2.3，表2 | Word表格 | 4×5内容完整 | 原生Word三线表，全栏 | PASS |
| `tables/verification-property-semantics.tex` | 2.3，表3 | Word表格 | 5×3内容完整 | 原生Word三线表，全栏 | PASS |
| 批内来源单射性前件 | 2.3 | 未编号公式 | 完整迁移 | 可编辑OMML，不编号 | PASS |
| M/I依赖说明 | 2.3末 | 科学论证 | 完整保留 | Word正文 | PASS |
| `sections/04-formal-analysis.tex` | `3 形式化验证与结果分析` | 一级正文 | 完整迁移 | 官方一级标题样式 | PASS |
| `3.1 无互异约束下的重复接受` | 3.1 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `eq:relaxed-duplicate-witness` | 3.1，式(3) | 编号公式 | 内容与编号不变 | 可编辑OMML | PASS |
| `fig2-duplicate-acceptance-trace.tex` | 3.1，图2 | 图 | 科学图义冻结 | 当前PDF派生360 dpi占位图；图题和证据说明为Word文本 | PASS / EMF_PENDING |
| 图2证据说明 | 图2下 | 图下注 | 逐字保留 | 7.5 pt Word段落 | PASS |
| `3.2 消息互异约束的替代性分析` | 3.2 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `3.3 参与方互异约束下的性质验证` | 3.3 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `3.4 综合验证结果` | 3.4 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `tables/key-verification-results.tex` | 3.4，表4 | Word表格 | 8×5内容完整 | 原生Word三线表，全栏，注释保留 | PASS |
| 13 verified + 1 falsified说明 | 3.4 | 结果文本 | 完整保留 | Word正文 | PASS |
| `sections/05-discussion.tex` | `4 结果讨论与适用范围` | 一级正文 | 完整迁移 | 官方一级标题样式 | PASS |
| `4.1 消息与参与方互异关系` | 4.1 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| 机器结果/人工推导边界 | 4.1 | 科学论证 | 完整保留 | Word正文 | PASS |
| `4.2 批次准入接口的关系维护` | 4.2 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| `4.3 适用范围与局限` | 4.3 | 二级标题 | 标题不变 | 官方二级标题样式 | PASS |
| 固定两槽及非完整协议攻击边界 | 4.3 | 局限性 | 完整保留 | Word正文 | PASS |
| `sections/06-conclusion.tex` | `5 结束语` | 一级正文 | 完整迁移 | 官方一级标题样式 | PASS |
| 全部8个引用键 | 正文首次出现处 | 引用 | 顺序闭合 | `[1]`–`[8]`顺序编码 | PASS |
| `bibliography/references.bib`中实际引用的8项 | 文末参考文献 | 参考文献 | 全部迁移 | 官方参考文献样式；阶段一格式 | PASS / GBT_FINAL_PENDING |

## Coverage result

- 一级标题：6/6。
- 二级标题：13/13。
- 编号公式：3/3；未编号公式：2/2。
- 表格：4/4，均为可编辑Word表格。
- 图：2/2；图题2/2；图2证据说明1/1。
- 正文引用：8个编号闭合；参考文献：8条。
- 未把`notes/`、审计报告、设计报告或QA日志写入论文正文。

