# K-Waay 论文 Stage 3.1 投稿前定点修订报告

## 1. 基线与范围

- 任务：`AROCMAG_STAGE3_1_FINAL_TYPOGRAPHY_PATCH`
- 日期：2026-10-09
- 分支：`main`
- 起始 HEAD：`b636bf4ca32cf21dd3a2f380644f9e645c998a91`
- 科学内容权威源：`submissions/arocmag/latex-v2/`
- Word 基线：`K-Waay-AROCMAG-submission-stage3-polished.docx`
- 新交付文件：`K-Waay-AROCMAG-submission-stage3.1.docx`

本轮只处理中文摘要、首页英文摘要排版、参考文献排版和末页双栏平衡。未进行第二次全文润色，也未修改 Introduction、正文各章、Discussion、Conclusion、公式、表格或图示的科学内容。

Stage 3 Word 保持原文件不变，SHA-256 仍为 `34518736176B6E2B4C7743E854074AE582BD7668A77C3BD8C738772FFE6420FA`。

## 2. 实际修改文件

### 2.1 LaTeX

- `submissions/arocmag/latex-v2/sections/00-abstract.tex`
  - 将中文摘要从 198 个汉字调整为 200 个汉字。
  - 明确区分“人工语义推导”和“机器可达见证”。
  - 同步压缩英文摘要，并按官方模板要求保持第三人称、研究对象用现在时、方法和结果用过去时、结论用现在时。
- `submissions/arocmag/latex-v2/main.pdf`
  - 由当前摘要重新编译生成。

### 2.2 Word 与构建/QA

- `submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage3.1.docx`
  - 独立生成，未覆盖 Stage 3 Word。
- `submissions/arocmag/word-final/source/build_word_stage3_1.py`
  - 英文摘要和关键词显式左对齐。
  - 参考文献显式左对齐，保留 18 pt 悬挂缩进、8 pt 字号和 9.5 pt 固定行距。
  - 在参考文献第 2 条前设置受控分栏，使末页两栏视觉高度接近。
- `submissions/arocmag/word-final/source/export_stage3_1_with_wps.ps1`
  - 用 WPS 实际打开 Stage 3.1 Word 并导出独立 PDF。
- `submissions/arocmag/word-final/source/run_content_audit_stage3_1.py`
- `submissions/arocmag/word-final/source/run_layout_audit_stage3_1.py`
- `submissions/arocmag/word-final/source/build-manifest-stage3.1.json`
- `submissions/arocmag/word-final/source/citation-order-stage3.1.json`
- `submissions/arocmag/word-final/formulas/formulas-stage3.1.json`
- `submissions/arocmag/word-final/figures/fig1-word-stage3.1.png`
- `submissions/arocmag/word-final/figures/fig2-word-stage3.1.png`
- `submissions/arocmag/word-final/qa/stage3.1-content-audit.json`
- `submissions/arocmag/word-final/qa/stage3.1-layout-audit.json`
- `submissions/arocmag/word-final/qa/stage3.1-render-final/`
  - 保存 WPS 导出的 6 页 A4 PDF、逐页 PNG 和文本检查产物。

两幅 Stage 3.1 PNG 仍由冻结的图 1、图 2 PDF 预览生成，只是供新 Word 独立引用；图形科学内容和源文件没有变化。

## 3. 四项问题完成状态

| 项目 | 状态 | 证据 |
|---|---|---|
| 中文摘要篇幅和表达规范 | DONE | 官方模板写明“200字以内为宜”；修订后按 Unicode CJK 汉字统计正好 200 字，包含研究问题、共同生命周期、三种固定两槽模型、人工语义推导、机器可达见证、非蕴含结论和固定两槽边界。 |
| 首页英文摘要单词间距 | DONE | 摘要段与关键词段显式设为左对齐，Times New Roman 8.5 pt、11 pt 固定行距、无首行缩进；WPS 第 1 页实际渲染中单词间距自然，无人为拉伸、裁切或不合理复合词断行。 |
| 第 6 页参考文献排版 | DONE | 8 条文献显式左对齐，18 pt 左缩进和 -18 pt 首行缩进形成悬挂效果，编号对齐；WPS 渲染中英文、标点、DOI、URL 和类型标识换行自然，内容逐条与 Stage 3 完全相同。 |
| 最后一页双栏视觉平衡 | DONE | 结论和参考文献标题、第 1 条文献留在左栏，第 2—8 条从右栏开始；两栏文本底部高度接近，阅读顺序仍为左栏后右栏。保留由全文篇幅造成的自然下部留白。 |

## 4. 摘要检查

### 4.1 官方要求与统计口径

仓库内官方模板 `投稿编辑模板-计算机应用研究.doc` 明确要求：摘要应包含目的、方法、结果和结论四个要素，**200 字以内为宜**，采用第三人称客观表述，避免“我”“我们”“本文”，且摘要中不使用引文。

因此，本轮没有采用任务建议中的 210—240 字范围，因为这会超过当前仓库官方模板的明确建议。统计口径为 Unicode CJK 统一汉字数量，不计拉丁字符、LaTeX 命令、数字和标点。

### 4.2 修改前中文摘要

> K-Waay的BatchReceive要求同次调用的输入对应不同参与方，但消息级限制能否替代该条件仍需验证。为此，在共同生命周期上构造无互异、消息互异和参与方互异三种固定两槽Tamarin准入模型。结果表明，无互异模型允许一个匹配发送来源对应同批两个接受；消息互异模型的消息互异性与批内来源单射性在新鲜消息和精确来源匹配规则下等价，但同一参与方的不同发送实例和消息仍可各自匹配发送来源并在同批被接受；参与方互异模型保持目标关系且有效批次可达。结论限于两槽批次准入抽象。

- 汉字数：198
- 问题：信息完整，但“等价”与机器可达见证处于同一结果句中，没有在摘要层面直接标明其证据类型。

### 4.3 修改后中文摘要

> K-Waay的BatchReceive要求同次调用对应不同参与方，但消息限制能否替代该条件需验证。基于共同生命周期构造无互异、消息互异和参与方互异三种固定两槽Tamarin准入模型。无互异模型允许一个匹配发送来源对应同批两个接受；人工语义推导表明，新鲜消息和精确来源匹配使消息互异性与批内来源单射性等价。机器可达见证显示，同一参与方的不同发送实例与消息各有匹配发送来源，可同批接受，故消息约束不能推出参与方互异性。参与方模型保持目标关系，有效批次可达。结论限于固定两槽准入抽象。

- 汉字数：200
- 无第一人称、无“本文”、无引文。
- $P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$ 的依据明确为当前规则下的人工语义推导。
- $M_\tau\nRightarrow P_\tau$ 的依据明确为既有机器可达见证。

### 4.4 英文摘要

- 修改前：138 词。
- 修改后：139 词。
- 修改后用 `A manual semantic derivation ...` 表达人工规则语义推导，用 `A machine-reachable execution ...` 表达机器可达见证。
- 研究对象和结论使用一般现在时；模型构造、模型结果和见证使用一般过去时；无 `I`、`we` 或 `In this paper`。
- 中英文摘要均保留三种固定两槽模型、共同生命周期、同参与方异消息见证、消息约束不能推出参与方互异性和固定两槽边界，科学含义一致。

## 5. 页面效果

| 检查项 | Stage 3 | Stage 3.1 |
|---|---|---|
| 总页数 | 6 页 A4 | 6 页 A4 |
| 首页英文摘要 | 两端/分散对齐导致部分行单词间距明显扩大 | 显式左对齐，单词间距自然，字号和行距未缩小 |
| 参考文献 | 英文行被拉伸，词间空白不均 | 左对齐、悬挂缩进稳定，编号、类型标识、DOI 和 URL 均可读 |
| 末页双栏 | 左栏只有结束语，全部参考文献位于右栏，两栏高度差明显 | 左栏含结束语、参考文献标题和第 1 条，右栏含第 2—8 条，两栏底部接近 |
| 下部留白 | 较大 | 仍有自然留白；没有用拉大字距、删文或缩小字号强行填满 |

WPS 实际渲染统计：6 页、9536 words、258 个段落、4 张表、2 幅图、99 个 OMath 数学对象、10 个版式分节。

全部 6 页均由最终 PDF 重新渲染为 PNG 并逐页查看：

- 第 1 页：中文摘要和英文摘要完整，无异常英文空白；正文仍在首页正常开始。
- 第 2—3 页：双栏、公式、图 1、表 1—3正常，无新分页或裁切。
- 第 4 页：Stage 3 已修复的中文异常字距没有回退；图 2 完整。
- 第 5 页：表 4 的长 lemma 仍按下划线边界稳定换行，没有越界或标识符损坏。
- 第 6 页：参考文献内容完整、顺序正确，两栏平衡改善，无异常字距、裁切或重叠。

标准 `render_docx.py` 也已实际调用，但当前环境没有 LibreOffice `soffice.exe`，因此该工具未生成第二套渲染产物。本轮视觉验收依据成功的 WPS 实际打开、PDF 导出和逐页 PNG 检查，不把失败的标准渲染尝试记为通过。

## 6. 科学内容保护

- 三种固定两槽准入模型未修改。
- 14 项验证结果仍为 13 项 verified、1 项 falsified；状态和证明步数未修改。
- RQ1—RQ3 未修改。
- 三个编号公式和三个未编号展示公式未修改。Stage 3 与 Stage 3.1 公式清单逐字节相同，SHA-256 均为 `6BC9FA3B7024B99A4F273D5F83ADCAF5A9C6BD65DA68049227B0DDD599388A68`。
- 所有 lemma 名称和机器见证未修改，`same_party_different_messages_batch_exists` 完整保留。
- 人工迹语义推导与机器证明的区别未改变，并在摘要中进一步显式标注。
- 4 张表、2 幅图及其科学内容未修改。
- 8 条参考文献的作者、题名、出版信息、年份、页码、DOI/URL 和顺序均未修改。Stage 3 与 Stage 3.1 参考文献清单逐字节相同，SHA-256 均为 `C4AE8FF8F35EDA7998854918C1B5F98EB25D5DC023BC3B0B878293B9B1B51B84`。
- 6 个一级章节、13 个二级标题、4 张表、2 幅图、3 个编号公式、3 个未编号展示公式、正文 `[1]`—`[8]` 引用和全部关键 lemma 均通过自动内容审计。
- `tamarin/`、`reviews/`、LaTeX 的 `figures/`、`tables/`、`bibliography/` 以及 `sections/01`—`06` 均无差异。

Stage 3.1 内容审计与版式审计的 `all_pass` 均为 `true`，并已由实际逐页视觉检查补充验证。

## 7. 编译与 QA

LaTeX 本地执行 `latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex` 成功，生成 11 页 A4 PDF：

- undefined references：0
- undefined citations：0
- missing glyphs：0
- overfull boxes：0
- LaTeX errors：0
- underfull hbox：1（既有非阻塞提示）

内置 LaTeX 编译器被调用，但长时间没有返回可用诊断，已终止等待；本报告的编译结论来自本机 XeLaTeX/latexmk 的实际成功构建。

`git diff --check` 通过，仅显示 Windows 工作区的 LF/CRLF 提示。未执行 Tamarin，未 commit，未 push。

## 8. 仍待人工处理事项

1. 补充真实作者、单位、城市、邮编、基金、作者简介、通信作者和电子邮箱。
2. 确认匿名投稿阶段是否继续保留身份占位，并在实名阶段同步中英文信息和文档元数据。
3. 确认中图分类号、文献标志码和文章编号。
4. 若投稿系统强制 MathType，在具备可靠 MathType 6.9d 转换环境后逐式转换并验证；当前状态仍为 `MATH_TYPE_CONVERSION_PENDING`。
5. 若投稿系统强制 EMF 或其他矢量格式，转换冻结图 1、图 2 并在目标 Word/WPS 环境复核；当前状态仍为 `FIGURE_VECTOR_CONVERSION_PENDING`。
6. 用最终投稿所用 Microsoft Word 版本执行一次打开、域更新、打印预览和投稿系统 PDF 预览。
7. 如需匿名公开复核材料，补充经确认的 artifact URL，不得编造链接。

## 9. 最终状态

四项定点修订均已完成，Stage 3 成果得到保留，Stage 3.1 Word 与当前 LaTeX 摘要一致，科学内容和机器结果没有回退。排版修订完成不等于全部投稿条件已经满足，作者元数据、MathType 和矢量图要求仍需人工确认。

**最终状态：`STAGE3_1_PATCH_COMPLETE`**
