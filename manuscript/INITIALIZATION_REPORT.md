# K-Waay RQ-v2 LaTeX 工程初始化报告

## 1. Created structure

已在 `manuscript/` 下建立 venue-neutral 正式论文工程，包括短入口
`main.tex`、正文装配文件、9 个 section source（Abstract 加 8 个 numbered
sections）、venue/preamble 分层、
TikZ/PDF figure 目录、两张表、BibTeX bibliography、appendix、写作 notes、
Makefile、latexmk 配置与忽略规则。`figures/pdf/` 已作为空的未来 PDF 图目录
建立。

正文 section 文件没有包含同级 `\section` 命令，也没有包含 ACM、IEEE、
Springer 或 Elsevier 专用 front-matter 命令。

## 2. Paper flow

reader-facing flow 为：

1. Introduction
2. K-Waay BatchReceive and the Identity Problem
3. Security Objective and Threat Model
4. Formal Modeling Methodology
5. Formal Analysis and Counterexample Traces
6. Discussion and Design Implications
7. Related Work
8. Conclusion

该顺序把 stated party-level condition、semantic obligation、attacker boundary、
formal abstraction、controlled comparison、result scope 连成一条论证链，而不以
Tamarin 文件或 lemma 清单组织叙事。

## 3. Difference from the previous planning structure

原 research-preparation 阶段近似平行的 Background、Problem Statement、Threat
Model、Formal Model、Formal Analysis、Evaluation、Discussion、Limitations 和
Related Work 已重组为：

- protocol/problem；
- security objective + threat model；
- formal modeling；
- formal analysis + counterexample traces；
- discussion + design implications + principal limitations；
- related work；
- conclusion。

当前证据不是 performance benchmark 或 empirical systems evaluation，因此未建立
独立的 systems-style Evaluation 大章。counterexample trace 属于 Formal Analysis，
不被包装成现实部署攻击章节。主要 modeling/interpretation limitations 被并入
Discussion，用于直接限定结果解释；Reproducibility 不再占据独立一级章节：Section
5 保留简短 verification environment，详细 commands、hashes、exact lemmas 和
traces 进入 Appendix。

2026-09-14 根据最终章节编排讨论，将原九章结构收敛为当前八章结构；§1--§6 的
技术叙事不变，Related Work 与 Conclusion 分别前移为 §7、§8。

## 4. Section/source mapping

完整映射记录在 `notes/section-source-map.md`。每个 section source 内也保留了直接
来源注释。`docs/paper/*.md` 被明确标为 writing material，而不是 authoritative
final prose；本阶段没有迁移 `full-paper-draft.md`，也没有正式撰写 Introduction。

## 5. Bibliography status

`bibliography/references.bib` 包含
`docs/paper/literature/citation-verification.tsv` 中全部 21 条
`source_verified=yes` 记录。正式 key 使用作者/年份/主题形式，不使用 `L1`、`L2`
等内部编号。

未猜测不确定 metadata：合并了 conference/journal 信息的 misbinding source row，
以及只给出 2023--2024 revision period 的 PQXDH specification，均保留显式 TODO，
待正文确定实际引用版本后处理。

## 6. Figure infrastructure

已创建并实际接入编译：

- `figures/tikz/attack-trace.tex`：relaxed admission model 中的 bounded
  counterexample trace；caption 没有称为 “K-Waay attack”。
- `figures/tikz/identity-control-comparison.tex`：以 party identity requirement
  为顶层，比较 relaxed、message-level 和 party-level admission variants。

图中概念中心是 party identity、message identity、occurrence injectivity 和 batch
admission，而不是内部 R/M/P shorthand。

## 7. Result-table infrastructure

`tables/verification-results.tex` 仅列出指定的 14 个 recorded outcomes，包含
variant、property、outcome 和 steps。`tables/model-comparison.tex` 不堆积 lemma
名称，而比较 admission variant、identity coordinate、same-party/different-message
admissibility、scoped occurrence injectivity 与 party uniqueness。

## 8. Venue neutrality

`venue/generic.tex` 只采用 11pt `article` 与合理 margin，用于 writing/review；
`venue/README.md` 明确声明它不是 submission template。未来 ACM、IEEE、LNCS/
Springer 或 Elsevier migration 仅在投稿目标确定且核对 official current author
instructions 后进行。venue-specific class、front matter、bibliography style 和
page-dependent layout 与 `sections/*.tex` 核心正文分离。

## 9. Build result

- command: `latexmk -pdf main.tex`
- latexmk: 4.87
- TeX distribution observed during build: TeX Live 2025
- PDF: `manuscript/main.pdf`（8 页；由 `.gitignore` 排除）
- BibTeX: pass
- broken input path: none
- Undefined control sequence: none
- TikZ compile failure: none
- undefined citation/reference: none
- overfull box warning: none

Build verdict: `LATEX_BUILD_PASS`

初始化期正文仍为空而四个 floats 连续出现，因此 Section 5 设置了三个明确标注的
scaffold-only `\clearpage`；待相邻正式 prose 稳定 float placement 后删除。

## 10. Research artifact integrity

最终 Git 审计结果：

- existing tracked research files modified: 0
- changes outside `manuscript/`: 0
- `.spthy` diff: 0
- `.pv` diff: 0
- lemma/prototype result diff: 0
- `tamarin/`, `artifact/`, `logs/`, `docs/rq-v2/`, `docs/paper/`, and
  `proverif/` diff: 0
- commit: NO
- push: NO
- audited HEAD: `6a10877ca5f527813585fd9c0e6d9aea35b19d22`

所有新增 source 均位于 `manuscript/`。编译生成物由该目录的 `.gitignore` 隔离。

## 11. Next writing section

下一阶段首先写 Section 2 — **K-Waay BatchReceive and the Identity Problem**。
先稳定 protocol object、stated distinct-party condition、identity coordinates、
motivating composition 和 RQ1--RQ3；随后再写 security objective、formal model 与
analysis。Introduction 和 Abstract 在技术核心稳定后完成。

## Final verdict

`LATEX_MANUSCRIPT_SCAFFOLD_READY`
