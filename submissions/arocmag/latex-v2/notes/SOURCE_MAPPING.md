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

## 5. Phase 2A 第3章逐段映射

正文以 `% P31-1` 等注释标记段落，注释不进入 PDF。以下英文位置均相对于
`manuscript/sections/05-formal-analysis.tex`；R/M/P 分别指 relaxed、message_dedup、party_admission 模型，
仅用于本来源记录，不作为正文协议名称。证据目录统一为 `reviews/2026-09-16-evidence/`。
每项状态及 steps 同时核对 `result-comparison.tsv` 和相应 `*-prove.stdout.txt` 的最终汇总。

| 中文段落 | 英文母稿位置 | Tamarin lemma / 规则 | 独立复核证据 | 压缩/合并处理 |
|---|---|---|---|---|
| P31-1 正常路径 | Relaxed Admission 首段 | R: `normal_relaxed_batch_exists` | TSV、R stdout、trace-audit 的 normal graph | 压缩；只报告批次接纳与后续一次接受，不称完整不同参与方批次 |
| P31-2 核心见证及式(3) | Relaxed Admission 核心公式及前段 | R: `one_send_two_accepts_exists` | TSV、R stdout、trace-audit 的 duplicate graph | 重写；oid 沿用前文记号，保留 s<b<r1<r2 |
| P31-3 匹配来源唯一性 | 核心公式后的唯一来源解释 | R: 同上，全称 Send 时间子句 | R stdout 中精确公式、trace-audit | 压缩；不把唯一匹配 Send 扩大为全执行只有一个 Send |
| P31-4 两槽复用与RQ | Relaxed Admission 轨迹重构及语义段 | R: 同上；CollectSlot1/2、ProcessSlot1/2 | trace-audit 中两个槽位和接受的相同元组 | 合并；只解释见证路径，不复制完整模型 |
| P31-5 全迹反例 | Relaxed Admission universal diagnostic 两段 | R: `receiver_accept_injective` | TSV、R stdout、trace-audit 的 injectivity graph | 合并；存在性与全迹失败不重复计贡献 |
| P31-6 来源及边界 | Relaxed Admission 来源解释与末段 | R: `receiver_accept_has_send` | TSV、R stdout、README | 合并；只用一个完整协议攻击边界句 |
| P32-1 消息性质 | Message-Level Restriction universal message 段 | M: `accepted_batch_has_distinct_messages` | TSV、M stdout | 压缩；同上下文、不同接受事件与消息不等齐全 |
| P32-2 注入性及来源 | 同节 universal results 段 | M: `receiver_accept_injective`、`receiver_accept_has_send` | TSV、M stdout | 合并；分别解释两项性质的作用，不重新给量词定义 |
| P32-3 核心同参与方见证 | 同节 decisive control 段 | M: `same_party_different_messages_batch_exists` | TSV、M stdout、trace-audit 的同名 graph | 改为行内条目，无非蕴含编号式 |
| P32-4 事件时序及来源 | 同节 More precisely 段 | M: 同上及 ProcessSlot1/2 | 精确 lemma 的时间约束、trace-audit 两组 Send/Accept | 合并；两条目各有来源，只有参与方坐标相等 |
| P32-5 机器证据作用 | 同节结论；Controlled Comparison | M: 上述 witness 与两项全迹性质 | TSV、M stdout、trace-audit | 合并；非替代性来自真实可达见证，非抽象常识冒充结果 |
| P32-6 消息拒绝 | Message-Level Restriction 首段 | M: `repeated_message_rejection_exists` | TSV、M stdout、trace-audit 拒绝 graph | 压为一句；不推断所有输入最终拒绝 |
| P32-7 小节结论 | Message-Level Restriction 末段 | M: 消息区分、注入性、同参与方见证 | TSV、M stdout | 压缩；不引入实现层的去重效果主张 |
| P33-1 目标性质 | Party-Level Restoration all-traces safety | P: `accepted_batch_has_distinct_parties` | TSV、P stdout | 重写为正控制；引用既有目标式 |
| P33-2 规则与接受边界 | 同节 Admission-rule semantics | P: AdmitDistinctParties、Inequality；目标 lemma | P stdout 中规则、restriction 与已验证性质 | 合并；区分规则语义与全迹结果 |
| P33-3 非真空性 | 同节 Reachability and non-vacuity | P: `distinct_party_batch_exists` | TSV、P stdout、trace-audit 的有效批次 graph | 保留两匹配来源、接纳及两次接受的时序 |
| P33-4 支持与拒绝限制 | 同节 supporting results 及首段 | P: `receiver_accept_has_send`、`receiver_accept_injective`、`same_party_rejection_exists` | TSV、P stdout、README、trace-audit 拒绝 graph | 合并；保留 Send 未绑定被拒元组限制，不展开 Discussion |
| P33-5 正控制结论 | 同节末段 | P: 目标性质及有效批次可达性 | TSV、P stdout | 压缩；不写修复方案、机制唯一性或协议安全结论 |
| P34-1 表格导语与类型 | Verification Summary | 三模型7项核心 lemma | TSV、三个 stdout | 重组；解释 exists-trace 与 all-traces 的不同验证含义 |
| 表4 7项核心结果 | `manuscript/tables/verification-results.tex` | R 2项、M 3项、P 2项 | TSV、三个 stdout | 按冻结取舍压缩为7行；不列 steps，自然编号为表4 |
| P34-2 三配置比较 | Controlled Comparison | R重复接受；M区分/注入性/同参与方；P目标/非真空 | TSV、trace-audit | 压成一段结果链，不提前写接口设计 |
| P34-3 7项支持结果 | Verification Summary；完整结果表 | R正常路径；R/M/P来源对应；M/P拒绝；P注入性 | TSV、三个 stdout，14行 MATCH | 合并为一段，完整14项和steps留在既有复现材料 |
| P34-4 后续独立复核 | Verification Environment 的主题；其历史口径由新版证据替代 | 三个未修改模型的全部14项 | README、manifest、TSV、三个 stdout | 更新为2026-09-16复核；只列环境、14/14状态及steps匹配与相对目录 |

`04-formal-modeling.tex` 用于核对共同生命周期、接纳规则与性质定义；
`06-discussion.tex` 用于控制解释边界，没有搬入接口维护责任、完整局限或后续研究段落。
本任务没有执行新的 Tamarin 运行；正文的后续独立复核指2026-09-16已有记录。

