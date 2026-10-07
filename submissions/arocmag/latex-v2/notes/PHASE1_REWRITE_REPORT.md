# AROCMAG 中文 LaTeX 重写 Phase 1 报告

## 1. 创建文件

新建独立工作区 `submissions/arocmag/latex-v2/`，包含：

- `main.tex`、`paper-content.tex`；
- `preamble/packages.tex`、`preamble/macros.tex`、`preamble/metadata.tex`；
- `sections/00-abstract.tex`、`01-introduction.tex`、`02-problem.tex`、`03-formal-modeling.tex`；
- `tables/identity-coordinate-map.tex`、`admission-configurations.tex`、`verification-property-semantics.tex`；
- `figures/README.md`；
- 从英文母稿原样复制的 `bibliography/references.bib`；
- `notes/SOURCE_MAPPING.md`、`LANGUAGE_QA.md` 和本报告；
- 编译产物 `main.pdf`。

## 2. 实际完成章节

已完成中文摘要、英文摘要、0 引言、第1章及其 1.1--1.3、第2章及其 2.1--2.3。`paper-content.tex` 只保留一行 Phase 2 注释，没有生成第3--5章的空章节或正文。

## 3. 英文母稿到中文稿的重组方式

技术事实来自英文 `00-abstract.tex` 至 `04-formal-modeling.tex`，结果概述与相关工作分别回查 `05-formal-analysis.tex` 和 `07-related-work.tex`。中文稿没有按英文小节逐段翻译：英文独立的协议问题、威胁模型和多个模型小节被重组为冻结的第1、2章；重复边界说明被压缩；旧中文稿仅用于术语与 XeLaTeX 配置核对。逐段来源见 `SOURCE_MAPPING.md`。

## 4. 引言修辞顺序

引言依次完成异步组合背景、K-Waay与既有条件、三组相关研究、研究缺口、方法与核心结果、三项贡献。没有 subsection、章节 roadmap 或独立 Scope 段，符合冻结蓝图的六段推进顺序。

## 5. 三张表状态

- 表1“身份坐标与模型映射”：已生成并编号；
- 表2“接纳配置与验证目标”：已生成并编号；
- “核心验证性质的迹语义”：已生成，使用不编号标题，为 Phase 2 的验证结果表保留“表3”编号。

三张表均采用 booktabs、无竖线；最终 PDF 渲染未发现越界或不可读单元格。

## 6. 两个核心编号公式

Phase 1 仅有两个编号公式：

1. `E_i=(A_i,oid_i,m_i)`；
2. `DistinctPartyPerBatch(B)`。

BatchReceive 输入向量和 2.3 注入性语义均未编号，没有增加其他编号公式。

## 7. Injectivity语义核对

已逐一核对三个 Tamarin 文件的 `receiver_accept_injective`。三者均全称量化 `A,sid,m,bid,rst,s,r1,r2`，要求同一个 `Send(A,sid,m)@s` 早于两个坐标相同的 `ReceiverAccept`，并推出 `r1=r2`。中文稿仅将模型 `sid` 等价记为 `oid`，保留两个时间条件和同一 `(bid,rst)` 作用域，并明确该性质不检查批内参与方数目。

精确来源对应、消息区分和参与方区分也分别与真实 lemma 核对：后两者都以同一 `(bid,rst)` 中两个不同接收事件为前件，分别约束 `m` 和 `A` 坐标。

## 8. 图1未生成的原因

任务明确要求将正式图留给独立绘图阶段。本阶段仅在 2.2 位置写入两行 LaTeX 注释，并在 `figures/README.md` 记录信息需求；未创建 Mermaid、Graphviz、TikZ、SVG、PNG、EMF 或占位图，也没有加入未定义图引用。

## 9. LaTeX编译状态

在 `submissions/arocmag/latex-v2/` 执行：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

编译成功并生成 `main.pdf`。最终日志中：

- LaTeX错误：0；
- undefined references：0；
- undefined citations：0；
- missing characters：0；
- overfull boxes：0；
- 仍有一处普通正文的轻微 underfull hbox（badness 1158），不涉及表格、公式或内容越界。

全部5页已渲染为 PNG 进行视觉检查；未见裁切、重叠、表格越界、公式越界或不可读字形。

## 10. 页数

当前 `main.pdf` 为 A4、5页。第1--4页为双语摘要和 Phase 1 正文，第5页包含性质语义、未编号注入性式及参考文献。该页数是高质量单栏草稿结果，不作为最终《计算机应用研究》版面页数承诺。

## 11. 技术事实待作者确认

没有阻止 Phase 2 的技术事实待确认。具体实现中何种对象对应模型参与方 `A`，以及由哪个组件维护不同参与方关系，仍需在后续讨论章保持条件式表述；当前模型没有验证该实现映射。

## 12. 语言表达待进一步审查

当前逐节语言 QA 全部通过，没有阻塞项。Phase 2 完成后仍建议进行一次全篇衔接和期刊版式审读，统一结果章与本阶段的“发送发生”“精确来源对应”“正控制”等术语，并复核最终模板中的摘要长度和表格字号。

## 13. Phase 2 适用性

章节结构、术语、引用、交叉引用和模型性质接口已经稳定，适合进入 Phase 2。旧 `submissions/arocmag/latex/` 是历史 Task1A 版本，继续保留但不再作为当前投稿稿正文来源；新权威中文稿为 `submissions/arocmag/latex-v2/`。

**AROCMAG_CHINESE_LATEX_PHASE1_READY**

