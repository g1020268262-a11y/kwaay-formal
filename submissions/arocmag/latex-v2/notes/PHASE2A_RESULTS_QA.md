# Phase 2A 结果章节 QA

任务：AROCMAG_CHINESE_LATEX_PHASE2A_RESULTS

## 前置条件与范围

- [x] 已读取 `PHASE1_FINAL_PATCH_REPORT.md`，状态为 `AROCMAG_PHASE1_FINAL_PATCH_READY`。
- [x] 仅在 `submissions/arocmag/latex-v2/` 写入。
- [x] 开始/结束 SHA-256 比对：Phase 1 四份 section 文件及三份 table 文件逐项相同；三个 Tamarin 模型逐项相同。
- [x] 未修改英文母稿、style-study、研究问题或模型；未运行新的 Tamarin 证明。
- [x] 只增加第3章及规定的四个 subsection，没有第4、5章正文。

## 3.1 放宽条件

- [x] 正常路径作为非真空性支持，未夸大成不同参与方完整批次保证。
- [x] 精确重复见证使用同一 `(A,oid,m)`，与同参与方不同消息的见证明确区分。
- [x] 一个匹配 Send 来源、一个批次、两个不同接受事件及 `s<b<r1<r2` 均保留。
- [x] 唯一匹配 Send 限于精确元组，未排除无关发送；未把它们放进核心事件式。
- [x] 存在性见证和 injectivity falsified 对应同类重复接受形状，没有重复计贡献。
- [x] origin correspondence verified 保留，未称无来源接受。
- [x] 末段只有一个完整协议攻击边界句；无 KEY/TEST、KEM、deployment、refinement 或 consumer 清单。
- [x] 图2仅为规定的两行注释，无图引用、图环境或图资产。

## 3.2 消息级替代性

- [x] 先报告消息区分成功：同一 `(bid,rst)` 的两个不同接受具有不同消息。
- [x] injectivity verified 与来源对应 verified 独立报告；明确放宽配置的精确重复形状被排除。
- [x] same-party/different-message 机器见证是中心证据，两个 oid、两个 m 不同，同一 A，且各有匹配 Send。
- [x] 见证保留两个发送先于批次接纳、接纳先于两个有序接受的时间关系。
- [x] 非替代结论来自满足控制和来源要求的可达执行，没有用抽象 nonimplication 代替机器结果。
- [x] 消息拒绝只用一句报告分支可达性，不声称所有重复消息最终拒绝。
- [x] 末段明确消息区分与作用域内发生注入性同时成立仍不能替代参与方关系。

## 3.3 参与方级正控制

- [x] 定位为正控制，没有改进协议、修复方案或新机制主张。
- [x] party distinction 与 valid batch reachability/non-vacuity 是主线。
- [x] 规则语义、全迹验证和有效批次见证的作用区分清楚。
- [x] 精确来源对应与 injectivity 作为支持性质合并说明。
- [x] 同参与方拒绝见证未绑定此前 Send 条目和被拒候选元组的限制保留；未推断完整 liveness。
- [x] 末段只落在当前两槽抽象的目标性质和有效批次可达性。

## 3.4 汇总及复核

- [x] 关键表正好7行：R 2、M 3、P 2；6个已验证、1个被反例否定。
- [x] 表格有配置、自然语言性质、类型、结果、论证作用；lemma 标识居次要位置。
- [x] 主表 proof steps 数量为0；exists-trace 与 all-traces 含义在正文和表注中说明。
- [x] 另外7项 supporting properties 合为一段，没有第二张完整结果表。
- [x] 全部14项为13 verified / 1 falsified；逐行用 TSV 的 lemma、状态、steps 匹配三个 stdout 汇总，14/14通过。
- [x] 独立复核日期、Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu 24.04和三个未修改模型均与 README/manifest 相符。
- [x] 正文只报告14/14状态和步数匹配，指向相对证据目录，无命令、hash、stdout或graph清单。

## 结构、编译及版面

- [x] 第3章仅4个 subsection；新增编号公式1个（式3），全文编号公式3个。
- [x] 关键结果表自然编号为表4，没有强制重置表号。
- [x] 第3章正文源文件含2614个汉字（去除注释，含小节标题，不含外部表），高于引言926、第1章873、第2章1119；是当前篇幅最大章节。
- [x] 已引用条目式、目标式、身份映射表、接纳配置表和性质语义表，未再复制定义。
- [x] `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` 退出0。
- [x] 最终日志：undefined references=0，undefined citations=0，missing characters=0，overfull boxes=0。
- [x] PDF 为A4、8页；全部页面已渲染检查，公式和表4无裁切、遮挡或越界。
- [x] 两处轻微 underfull hbox（badness 1158、1082）无可见溢出，不影响上述验收项。
- [x] PDF页截图仅作为临时版面检查文件，不是论文图2，交付前清理；figures目录仅有README。

结论：无阻塞项。

**AROCMAG_CHINESE_LATEX_PHASE2A_READY**
