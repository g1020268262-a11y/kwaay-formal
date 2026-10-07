# Phase 1 中文段落来源映射

## 1. 使用原则

- 技术事实以 `manuscript/`、三个 `tamarin/rq-v2-minimal/` 模型和 `reviews/2026-09-16-evidence/` 为准。
- 章节节奏、取舍和术语以 `style-study/FINAL_CHINESE_PAPER_BLUEPRINT.md` 及其最终补丁为准。
- `submissions/arocmag/latex/` 只用于确认 XeLaTeX 配置和既有译法，没有复制其段落。
- `oid` 只在 1.2 说明一次与模型 `sid` 的映射；Tamarin 文件未改名。

## 2. 逐段映射

| 中文位置 | 主要英文/模型来源 | 重组方式 | 事实处理 |
|---|---|---|---|
| 中文摘要 | `00-abstract.tex`；`05-formal-analysis.tex`；冻结蓝图摘要要求 | 按“问题—方法—结果—结论”重写 | 删除旧摘要的长边界清单；保留固定两槽和非完整协议攻击边界 |
| 英文摘要 | 最终中文摘要 | 依据中文摘要重新撰写 | 未复制英文母稿摘要 |
| 引言第1段 | `01-introduction.tex` 第1段；`07-related-work.tex` 的 composition 论述 | 合并为异步接收与组合边界问题 | 未引入模型名、lemma 或验证数量 |
| 引言第2段 | `01-introduction.tex` 第2段；`02-batchreceive-identity-problem.tex` 前两小节 | 压缩 K-Waay、BatchReceive、共享状态和原条件来源 | 明确条件已存在，不写成协议遗漏 |
| 引言第3段 | `07-related-work.tex` 的 K-Waay/PQXDH、Tamarin、identity/injectivity/composition 小节 | 三组文献压成一段问题链 | 只使用英文母稿已有 BibTeX key，无新增文献 |
| 引言第4段 | `01-introduction.tex` 的坐标区别和 Questions | 提炼为全文问题句 | 明确研究问题不是“K-Waay是否存在漏洞” |
| 引言第5段 | `01-introduction.tex` 的 approach/results；`05-formal-analysis.tex`；`result-comparison.tsv` | 合并方法与三条核心结果，不写 lemma 名 | 结果状态与 2026-09-16 对照表一致 |
| 引言贡献项 | `01-introduction.tex` 的 contribution；冻结蓝图 | 压缩为三项 | 配置定位为方法，未当作新协议贡献 |
| 1.1 第1段 | `02-batchreceive-identity-problem.tex` 的 K-Waay and BatchReceive | 仅保留 Send、共享接收状态和输入向量 | 删除完整 KEM、split-KEM、密钥派生过程 |
| 1.1 第2段 | 同文件的 Stated Distinct-Party Condition | 压缩为批内作用域和机制未指定 | 未推断部署中缺少检查 |
| 1.1 第3段 | 同文件的 batch admission 解释 | 收束到条目关系 | “批处理接纳”仅作为分析术语 |
| 1.2 定义段 | `02-batchreceive-identity-problem.tex` 的 Identity Coordinates；`04-formal-modeling.tex` | 将英文 `sid` 改为中文稿 `oid` | 明确 `oid` 不是完整协议 transcript/session 标识 |
| 表1 | 英文 identity-coordinate 表；source-to-abstraction mapping | 合并、压缩为五类坐标 | 接收状态并入“批次/接收上下文”行 |
| 1.2 解释段 | `02-batchreceive-identity-problem.tex` 身份坐标解释 | 合并边界说明 | 不把参与方自动等同于账户或公钥编码 |
| 1.2 最小实例 | 英文 Motivating Identity Problem | 去除三个额外编号公式，改为一次行内实例 | 只表达逻辑分离，不称机器攻击轨迹 |
| 1.3 RQ1--RQ3 | 英文 Research Questions；冻结蓝图 | 各压缩为一句 | 研究问题内容未改变 |
| 2.1 目标定义 | `03-security-objective-threat-model.tex` 的 Party-Level Objective | 保留唯一目标编号公式 | 定义面向有限批次，机器证据明确固定两槽 |
| 2.1 攻击者段 | 同文件的 Batch-Composition Adversary | 合并 Dolev--Yao 与批次选择、排列、重放能力 | 区分组合已有条目与制造精确来源 |
| 2.1 边界段 | 同文件 Analysis Boundary；冻结蓝图 | 压缩为一个局部边界段 | 只写两槽、组合假设和证据终点 |
| 2.2 第1段 | `04-formal-modeling.tex` 的 Modeling Objective、Common Lifecycle | 将规则语义改写为论文叙述 | 区分 `Send` 动作与 `!Sent` 持久事实 |
| 2.2 第2段 | 三个 Tamarin 模型的 `CollectSlot1/2` 规则 | 合并共同收集过程 | `bid/rst` 只表示模型上下文 |
| 2.2 第3段 | 三个模型的 admission/process 规则 | 合并接纳、顺序处理和精确来源要求 | 未把 `!Sent` 称为真实认证机制 |
| 2.2 收束段 | `common-rules-comparison.txt`；三个模型 | 提炼共同骨架与唯一分析变量 | 图1只留注释，无引用和占位图 |
| 2.3 表2 | `04-formal-modeling.tex` 三个模型小节；真实 admission 规则 | 合并为三行受控配置 | 不称 R/M/P 协议、修复或新协议 |
| 2.3 性质表 | 三个模型的 `receiver_accept_has_send`、`receiver_accept_injective`、消息/参与方区分 lemma | 按真实量词范围压缩成语义表 | 消息区分和参与方区分的前件均保留同上下文与不同接收事件 |
| 2.3 未编号式 | 三个模型相同的 `receiver_accept_injective` | 用 `oid` 等价改写 `sid`，保持全称量词和两个时间条件 | 明确其不检查批内参与方数目 |

## 3. 主张排除检查

正文没有新增或暗示以下主张：

- K-Waay存在协议漏洞或其原条件缺失；
- 密码学攻击、底层原语被攻破或密钥泄露；
- 部署缺陷、真实客户端/服务器必然缺少检查；
- UKS、misbinding 或应用层状态损坏；
- 任意批长定理；
- 完整协议认证或 refinement theorem。

## 4. 引用检查

Phase 1 使用的 8 个引用键均来自英文母稿现有 `references.bib`：

`cremers2023session`、`collins2024kwaay`、`collins2024kwaayfull`、
`cohngordon2020signal`、`bhargavan2024pqxdh`、`meier2013tamarin`、
`lupetti2006names`、`lowe1997hierarchy`。

当前三组相关工作已有足够的英文母稿来源支撑 Phase 1 定位，未发现需要临时补造文献的空缺。

