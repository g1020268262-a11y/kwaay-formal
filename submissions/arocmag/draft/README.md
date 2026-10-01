# 《计算机应用研究》中文稿工作区

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_1`

状态：结构与证据规划已完成；尚未开始完整中文正文、Word 制稿或投稿。

## 本阶段成果

- `outline/CHINESE_PAPER_OUTLINE.md`：推荐的中文论文结构、章节论证任务、公式与图表配置。
- `outline/SECTION_MAPPING.md`：英文母稿逐部分到中文稿的去向与操作标签。
- `outline/CLAIM_EVIDENCE_MATRIX.md`：拟写主张、证据来源、模型性质、假设和允许的中文表述。
- `outline/CONTENT_REDUCTION_PLAN.md`：重复内容压缩、相关工作缩减、附录处置和后续格式转换计划。
- `notes/ADAPTATION_STAGE1_REPORT.md`：第 1 阶段总结、审稿意见处置与待确认事项。
- `sections/`、`figures/`、`tables/`、`references/`：后续阶段占位目录；本阶段不填充完整稿件。

## 研究定位

中文稿应定位为 K-Waay `BatchReceive` 接口上一次受控的、固定两槽的接纳语义比较。直接证据止于模型事件 `ReceiverAccept`。文章可以报告：

1. 宽松接纳模型中，同一精确 sender origin 支持同一 batch context 内两次接受的可达执行；
2. 消息级限制排除该精确重复模式并满足当前模型中的消息区分与作用域内 occurrence injectivity，但仍允许同一 party 的两条不同消息共同进入一个 batch；
3. 参与方级接纳直接维持 party distinction，且有效的不同参与方批次仍可达；
4. 在当前 freshness/origin 与两槽生命周期下，`P_tau => M_tau <=> I_tau` 且 `M_tau` 不蕴含 `P_tau`。该关系是对规则的人工推导，不是新增 Tamarin lemma。

不得将这些结论写成完整 K-Waay 攻击、密钥泄露、`KEY/TEST` 失效、部署漏洞、密码学身份绑定失效、任意批大小定理或 refinement theorem。

## 证据权威顺序

1. K-Waay 原文及其中明确写出的 `BatchReceive` 不同参与方条件；
2. `tamarin/rq-v2-minimal/` 中三个当前模型及其 lemma；
3. `reviews/2026-09-16-evidence/` 的独立复核原始输出、图和清单；
4. `reviews/2026-09-16-adversarial-review.md` 对主张边界与证据强度的审计；
5. `manuscript/` 英文母稿，作为内容来源而非高于模型或原始协议的权威来源。

## 工作边界

本目录只保存中文适配工作产物。第 1 阶段没有修改英文母稿、Tamarin 模型、既有证据、历史 FormaliSE 稿或期刊官方资料；没有运行 Tamarin、转换 Word、填写作者/单位/基金信息、提交稿件、发送邮件、提交 Git 或推送远端。

