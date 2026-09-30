# FormaliSE 2027 Setup Report

建立日期：2026-09-29。Verdict：**FORMALISE_WORKSPACE_READY**。

本结论仅表示投稿骨架、真实副本和后续计划已建立且可编译，不表示论文已完成内容适配或达到投稿标准。

## Source Manuscript

- 来源：`D:/kwaay-formal/manuscript/`。
- 复制时与交付时 Git HEAD：`a645f5a5b274977db1d39ceefa66c57db94c8e16`，branch `main`，提交说明 `整体审稿-1`。
- 任务开始时工作树干净。任务后仅新增 `submissions/formalise2027/` 下文件，未 stage、commit 或 push。
- 复制清单：[COPY_MANIFEST.tsv](COPY_MANIFEST.tsv)，逐项记录来源、目标与 SHA-256。

## Created Structure

```text
submissions/formalise2027/
├── .gitignore
├── main.tex
├── paper-content.tex
├── README.md
├── preamble/
│   ├── packages.tex
│   ├── macros.tex
│   └── metadata.tex
├── sections/
│   ├── 00-abstract.tex
│   ├── 01-introduction.tex
│   ├── 02-batchreceive-identity-problem.tex
│   ├── 03-security-objective-threat-model.tex
│   ├── 04-formal-modeling.tex
│   ├── 05-formal-analysis.tex
│   ├── 06-discussion.tex
│   ├── 07-related-work.tex
│   └── 08-conclusion.tex
├── bibliography/references.bib
├── figures/tikz/
│   ├── attack-trace.tex
│   └── identity-control-comparison.tex
├── tables/
│   ├── model-comparison.tex
│   └── verification-results.tex
├── appendix/
│   ├── appendix.tex
│   ├── trace-details.tex
│   ├── model-properties.tex
│   └── reproducibility.tex
└── notes/
    ├── COPY_MANIFEST.tsv
    ├── FORMALISE_PLAN.md
    └── FORMALISE_SETUP_REPORT.md
```

本地另有生成的 `main.pdf`、LaTeX 辅助文件、`build-console.log` 与 `build-review/` 版面核查图；均被目录级 `.gitignore` 排除，没有从母稿复制 PDF、旧日志、cache 或截图。

## Venue Configuration

- Document class：`\documentclass[10pt,conference]{IEEEtran}`，未启用 compsoc/compsocconf。
- Bibliography style：`IEEEtran`；`references.bib` 与来源字节完全一致，无新增引用。
- Anonymous status：标题保持 `Party Identity in Batch Admission: A Formal Study of K-Waay BatchReceive`；作者显示 `Anonymous Author(s)`；PDF author 字段为空。
- README 已记录 15th FormaliSE、ICSE 2027 co-location、10+2 页、lightweight double anonymous、三个 AoE 截止日期、可选且鼓励的 artifact evaluation，以及 [官方 CFP](https://2027.formalise.org/track/Formalise-2027-papers)（2026-09-29 核对）。
- 未改变 IEEE 字号、行距、页边距以缩页。

## Copied Materials

真实复制 sections、bibliography、figures/tikz、tables、appendix、packages、macros；另以母稿 paper-content 为基础建立入口，共 21 个有复制来源的文件。9 个字节一致，12 个仅有 LaTeX 配置、路径或版式适配。无 symlink；无回指母稿的 LaTeX input。

适配差异如下，未改变正文叙述、公式含义、lemma、结果或引用集合：

| 文件 | 仅限 scaffold 的调整 |
| --- | --- |
| paper-content.tex | plain 改 IEEEtran；加入最终主 PDF 不保留全部详细附录的页数注释；保持 Section 1--8 次序 |
| appendix/appendix.tex | 多附录入口改用 IEEEtran 的 `\appendices` |
| appendix/model-properties.tex | 精确 listings 路径从 `../tamarin/` 改为 `../../tamarin/`；表格改跨栏 |
| appendix/reproducibility.tex | 64 位 SHA-256 中间增加可断行点；值不变 |
| figures/tikz/*.tex、tables/*.tex | 浮动体使用 figure*/table* 适配双栏，内容不变 |
| sections/02-batchreceive-identity-problem.tex | 表格跨栏；两条宽公式分行 |
| sections/03-security-objective-threat-model.tex | 目标不变量公式分行 |
| sections/04-formal-modeling.tex | 两张表格跨栏 |
| sections/05-formal-analysis.tex | message/party 非蕴含公式分行 |

已对 21 份复制材料执行比较：剔除上述格式、配置、路径差异后内容一致。包括 Abstract、Introduction、Discussion、Related Work、Conclusion 的文件字节完全一致。未根据 review 重写研究主张，也未在本阶段更改旧正文关于 raw logs 可用性的叙述；该待办只记录在计划中。

精确 lemma listings 继续只读依赖仓库权威模型。因此本目录是独立于母稿的写作工作区，尚非脱离仓库可独立构建的 artifact 包；此依赖在 README 和计划中明确记录。

## Research Files Modified

**Research Files Modified: 0**

对 `manuscript/`、`tamarin/`、`docs/`、`artifact/`、`reviews/`、`results/`、`archive/` 中全部现存文件建立前后 SHA-256 对照：260/260 文件路径与内容保持一致。Git tracked diff 为空，新文件全部位于允许目录。

本次没有执行 Tamarin，没有新增/修改 lemma、研究模型、verification result 或旧 artifact，没有移动任何证据。

## Current Page Status

当前 `main.pdf` 为 **17 页**，包含完整正文、references 和详细附录。正文延续到第 14 页，references 位于第 14 页，附录从第 14 页开始；该分布仅用于记录当前完整 scaffold，不是最终分页方案。

**NOT YET PAGE-LIMIT COMPLIANT**。

已浏览全 17 页渲染缩略图，并放大检查结果表/比较图和附录哈希页。未发现裁切或跨栏重叠。未为满足页数限制删除任何研究内容。浮动体位置、留白和完整附录仍须在未来内容压缩后重新排版。

## Review Issues To Address

已读取 adversarial review 并将后续处理写入 [FORMALISE_PLAN.md](FORMALISE_PLAN.md)：

- Non-triviality：M 的 coordinate non-substitutability 是最强模型结果，但改为 case study 定位不能自动解决 novelty。
- M/I dependency：在现有 freshness/origin 假设下记录 `Pτ ⇒ Mτ ⇔ Iτ`；人工规则推导不冒充新 lemma。
- Abstraction boundary：R 是模型反例；P 是正控制；没有完整 protocol refinement，不能声称 AKE、KEY/TEST 或部署漏洞。
- Evidence integration：正式引入 2026-09-16 独立复核；区分它与历史 freeze 的 provenance，未来修正正文日志可用性表述。
- Rejection reachability、历史 authority 与当前 separation 定位的差异，在未来写作中准确限定；本阶段不修改研究层。

## Artifact Plan

Independent rerun evidence will later be consolidated into submission artifact。

本次只读核查 `reviews/2026-09-16-evidence/`：SHA256SUMS 中 24/24 文件匹配；result-comparison 为 14/14 MATCH（13 verified、1 falsified）；manifest 的 7 次历史 invocation exit code 均为 0，三个 prove 原始输出的结果和 wellformedness 记录与之相符。这是对现存记录的核查，不是本次重新运行 prover。

未来在保留原件的前提下整理模型、原始输出、graphs、命令、版本、日期、commit 与 hashes，形成 claim/lemma/evidence 对照；不把新独立复核称为历史日志恢复。本阶段不新建研究 artifact、不搬移证据。

## Build

**PASS — BUILD_PASS**。

使用已安装的 IEEEtran class/style（TeX Live 2025），无模板下载。执行了：

```powershell
cd D:/kwaay-formal/submissions/formalise2027
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf main.tex
```

LaTeX/BibTeX 构建完成、exit code 0；PDF 为 17 页。最终 log 无 LaTeX 错误、undefined reference/citation、multiply defined label 或 overfull box。保留 46 条 underfull box 诊断（段落疏松/断行），属于后续排版优化事项，不影响本阶段编译。Windows Perl 有 locale fallback 提示，未阻断构建。

## Next Stage

**FORMALISE_CONTENT_ADAPTATION**。

本次停在 scaffold 完成边界，不自动进入正文压缩，不 commit/push。README 约定即使放弃 FormaliSE 也保留此目录；LNCS venue 另建 `submissions/lncs-<venue>/`。
