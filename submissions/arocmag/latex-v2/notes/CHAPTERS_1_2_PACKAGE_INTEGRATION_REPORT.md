# 第1、2章精简替换包机械整合与编译报告

日期：2026-10-13。目标工程：`submissions/arocmag/latex-v2/`。本轮仅机械替换、标题补丁和主工程编译；没有开展研究、改写正文、新增公式或重新运行证明器。

## 1. 输入与替换一致性

整合前 HEAD：`f3f163bfa4d9ba580b750389b4c0dd35d618655c`。

附件 ZIP SHA-256：`3552f54564bcc6f8de426c648a74269b0db9b3252abe73691e6a8982175142f7`。

| 目标文件 | 执行内容 | 与附件核对 |
| --- | --- | --- |
| `sections/02-problem.tex` | 完整替换第1章 | 4664 字节；SHA-256 `2cf3ab86ad9665a1432d19a964570a39ffd38757f4ae631e3791f7dfb1f364ec`；逐字节一致 |
| `sections/03-formal-modeling.tex` | 完整替换第2章，含内嵌表1 | 6146 字节；SHA-256 `79b472d89a8c72fd515ce6640b58006ec65673c2cce2470042617b960e55e30c`；逐字节一致 |
| `paper-content.tex` | 按 `paper-content-title.patch` 修改两条 section 标题 | 仅2行标题替换；原有 input 路径与章节标签均保留 |

新标题分别为“K-Waay协议及安全问题”和“形式化建模与安全性质”。没有改动主入口、宏包、宏定义、题名元数据、摘要、引言、第3章及其后正文或参考文献数据库。

本轮更新已有 `main.pdf`，并添加本报告；不提交压缩包说明文件，也未创建新的论文项目或独立审阅稿。原有未跟踪的 `submissions/arocmag/rewrite-draft/` 保持原状，不纳入本次 commit。

## 2. 编译结果

在原工程目录中，使用原有 `main.tex`：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=C:/Users/10202/AppData/Local/Temp/kwaay-chapter12-integration-53d33a854a4e420ca7f8965172c697a0 main.tex
```

工具：TeX Live 2025、XeLaTeX、BibTeX、latexmk 4.87。输出目录只是编译中间文件目录，不是复制的论文工程；所有正文、表格和既有图源均读取原工程。

退出码为 **0**，生成 **11页**完整投稿模板 PDF，并将其复制回已有 `main.pdf`。新 PDF SHA-256：

`59617e077b2429e75ac4aab98d572b11251bf4eeb5905fd23c7f365fa7523a9a`。

| 最终检查 | 结果 |
| --- | --- |
| 致命编译错误 | 0 |
| 重复标签 / multiply-defined labels | 0 |
| 未解析文献引用 | 0 |
| 缺字 | 0 |
| Overfull hbox/vbox | 0 |
| 未解析交叉引用 | 2个旧标签，共6处；见第3节 |
| 宏包 Warning | 1条 caption 警告；见第4节 |
| Underfull hbox | 1处，位于未改动的后续正文；见第4节 |
| BibTeX warning | 0 |

初轮编译中的文献、附件内新标签及书签重编译提示经自动多轮处理已消失；以下只将最终仍存在的问题列为剩余问题。编译成功不等于全文无警告。

最终 LaTeX 日志、BibTeX 日志及辅助文件位于上述系统临时目录中的 `main.log`、`main.blg`、`main.aux` 和 `main.fls`。为避免无关跟踪文件变动，没有覆盖工程中旧的 `main.aux`、`main.bbl`、`main.blg`、`main.fdb_latexmk`、`main.fls`、`main.log`、`main.out` 或 `main.xdv`。

## 3. 保留并报告的旧标签引用

新附件不再定义 `subsec:configurations-properties` 和 `eq:distinct-party-objective`；后续章节仍使用它们。没有添加标签别名，也没有擅自改写引用或后续正文。

| 引用文件及行号 | 旧标签 | PDF页 | 最终表现 |
| --- | --- | --- | --- |
| `sections/04-formal-analysis.tex:41` | `subsec:configurations-properties` | 7 | 节号显示 `??` |
| `sections/04-formal-analysis.tex:57` | `eq:distinct-party-objective` | 7 | 式号显示 `(??)` |
| `sections/05-discussion.tex:4` | `subsec:configurations-properties` | 9 | 节号显示 `??` |
| `sections/05-discussion.tex:8` | `eq:distinct-party-objective` | 9 | 式号显示 `(??)` |
| `sections/05-discussion.tex:13` | `eq:distinct-party-objective` | 9 | 式号显示 `(??)` |
| `sections/05-discussion.tex:22` | `eq:distinct-party-objective` | 10 | 式号显示 `(??)` |

最终日志还包含汇总警告 `LaTeX Warning: There were undefined references.`。上述6处即本轮全部未解析交叉引用；没有其他未解析文献或交叉引用。是否迁移这些引用，留待用户审查决定。

## 4. 其他警告及图表核验

- `sections/03-formal-modeling.tex:56`：`Package caption Warning: The option hypcap=true will be ignored for this particular caption.` 原因是附件使用 minipage 内的 `\captionof{table}`，而非浮动 table 环境；表题仍正常显示。没有为消除警告修改附件代码或宏包设置。
- `sections/04-formal-analysis.tex:64–65`：`Underfull \hbox (badness 3312)`，位于第3章已有正文的参与方互异性质段落，不是表1或表格溢出。没有调整这一段。
- latexmk 启动时 Perl 报告 Windows 环境不支持当前 `LC_ALL/LANG=C.UTF-8` locale，随后回退到系统简体中文 locale；构建退出码仍为0。没有改动用户环境。
- Git 提示这些 LF 文本按现有 autocrlf 配置在未来 checkout 时可能转为 CRLF；没有修改仓库行尾规则。当前两章工作区文件已与 ZIP 原始字节核对一致。

按 PDF 检查流程，在内存中渲染并检查全部11页，没有创建 PNG/JPEG/SVG 等图形文件。第5页内嵌表1“安全性质与验证模型的对应关系”四列、六个性质行显示完整，没有裁切、重叠或超出版心。既有结果表在第8、9页显示完整。

`tab:security-goal-map` 在最终 aux 中编号为表1；旧的 `identity-coordinate-map`、`source-to-abstraction`、`admission-configurations` 和 `verification-property-semantics` 表源保留为既有文件，但本轮完整编译的输入清单不再载入它们，没有重复插入旧表1。

第1章只保留附件中的图1注释预留位置，没有制作或插入新的图1。第3章已有 `figures/fig2-duplicate-acceptance-trace.tex` 及其正文引用未改动；由于旧第2章的生命周期图已随完整替换退出正文，LaTeX 自动将这一既有后续图编号为“图1”，位于第6页。未强制图号，也未更改其图源或后续章节。

## 5. 变更范围与停止条件

本次 commit 仅包括两个替换章节、两行标题补丁、更新后的已有 `main.pdf` 和本报告，共5个文件。没有修改形式化模型、证明结果、实验日志、既有图源、摘要、引言、后续正文或参考文献；没有运行 ProVerif/Tamarin。

排除明确允许变动的3个 TeX 文件和 `main.pdf`，整合前后其余 **2334个已有跟踪文件**的有序 `路径+SHA-256` 清单摘要保持一致：

`13d366e5ee87b549a000acb48af26d49d44304965e576a09c36975b8b2ae1d79`。

机械整合与编译已经完成；现存6处旧标签引用及上述非致命提示均保留供审查。本轮不修订这些内容，提交 GitHub commit 后停止等待用户审查。
