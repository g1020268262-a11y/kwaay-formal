# FormaliSE 2027 submission workspace

这是 venue-specific submission workspace，仅建立 IEEE 投稿骨架和后续内容适配计划；它不是新的 research authority，也不是已可提交的定稿。

## Venue constraints

以下信息于 2026-09-29 核对 [官方 CFP](https://2027.formalise.org/track/Formalise-2027-papers)。

| 项目 | 要求 |
| --- | --- |
| Venue | 15th International Conference on Formal Methods in Software Engineering (FormaliSE 2027) |
| Co-located with | ICSE 2027 |
| Full Research Paper | 10 pages content + 2 pages references |
| Format | IEEE conference proceedings; `\documentclass[10pt,conference]{IEEEtran}` |
| Bibliography | `IEEEtran` |
| Review | lightweight double anonymous |
| Abstract registration | 2026-10-30 AoE |
| Paper submission | 2026-11-06 AoE |
| Artifact submission | 2026-11-10 AoE |
| Artifact evaluation | optional but encouraged |

AoE 为 UTC-12。未启用 `compsoc` 或 `compsocconf`。保留工作标题，作者为 Anonymous Author(s)，PDF author 字段为空。将来投稿前仍需核查最终正文、artifact 及当时 CFP；当前匿名 metadata 不等于完成整个投稿包的匿名化审查。

## Source and authority

- 复制源：`D:/kwaay-formal/manuscript/`，Git commit `a645f5a5b274977db1d39ceefa66c57db94c8e16`。
- 完整母稿仍在 `../../manuscript/`，未修改。
- 研究模型仍在 `../../tamarin/rq-v2-minimal/`，未修改。
- 正式 verification evidence 保持原位置，包括 `../../artifact/rqv2-freeze/` 和 `../../reviews/2026-09-16-evidence/`；两者有不同的 provenance。
- 论文材料为真实文件副本，不使用 symlink，不加载母稿的 sections、preamble、figures、tables 或 bibliography。
- 附录的精确 lemma listings 仍只读加载原有三个权威模型；路径因目录层级改为 `../../tamarin/rq-v2-minimal/`。因此这是独立于母稿的写作副本，尚不是脱离仓库即可编译的独立 artifact 包。未复制或创立第二套模型权威。
- `notes/COPY_MANIFEST.tsv` 记录逐文件来源和源/副本 SHA-256，以及仅限 LaTeX 适配的差异。

## Build and scope

在本目录执行：

```powershell
latexmk -pdf main.tex
```

需要本机 IEEEtran 和现有 LaTeX 依赖。没有下载外部模板。当前保留完整 Section 1--8、全部引用和详细附录；未进行压缩、合章、研究改写或新增引用。

**NOT YET PAGE-LIMIT COMPLIANT**。页数、编译诊断与核查结论见 [Setup report](notes/FORMALISE_SETUP_REPORT.md)。生成的 PDF、LaTeX 辅助文件和版面检查图片由本目录 `.gitignore` 排除；没有复制母稿的编译产物。

后续工作仅在获得对应任务时进入 `FORMALISE_CONTENT_ADAPTATION`，参见 [内容适配计划](notes/FORMALISE_PLAN.md)。本次未运行 Tamarin，未新增 lemma，未改模型或证据，未 commit/push。

如果以后不投 FormaliSE，保留本目录，不删除或覆盖。若切换到 LNCS venue，另建 `submissions/lncs-<venue>/`；不要把本 IEEE 版本直接改成 LNCS。
