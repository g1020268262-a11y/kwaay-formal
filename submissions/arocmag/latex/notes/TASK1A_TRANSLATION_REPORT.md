# AROCMAG_CHINESE_LATEX_TASK_1A 翻译报告

## 1. 实际创建内容

工作区：`submissions/arocmag/latex/`

- `main.tex`
- `paper-content.tex`
- `preamble/packages.tex`
- `preamble/macros.tex`
- `preamble/metadata.tex`
- `sections/00-abstract.tex`
- `sections/01-introduction.tex`
- `sections/02-batchreceive-identity-problem.tex`
- `sections/03-security-objective-threat-model.tex`
- `bibliography/references.bib`
- `notes/TERMINOLOGY_MAP.md`
- `notes/TASK1A_TRANSLATION_REPORT.md`
- 空目录 `figures/`、`tables/`
- 编译结果 `main.pdf`

`bibliography/references.bib` 从英文母稿逐字节复制；源文件与副本的 SHA-256 均为 `8A0A5A75D4C0294049FBAC13B4CB74907E06729729D24051733B4DC8D9E04714`。

## 2. 英文到中文的章节映射

| 英文母稿 | 中文 LaTeX | 处理结果 |
| --- | --- | --- |
| `00-abstract.tex` | 摘要 | 保留研究对象、三模型受控比较、三项主要结果和证据边界；更新独立复跑事实。 |
| `01-introduction.tex` | 0 引言 | 保留“组合边界动机 → K-Waay → 原有条件 → 身份坐标 → 三个 RQ → 方法 → 结果 → 范围 → 结构”的推进顺序。 |
| `02-batchreceive-identity-problem.tex` | 1 K-Waay BatchReceive与参与方区分问题 | 五个 subsection 一一对应，保留接口向量、身份坐标表、动机组合、逻辑非蕴含和三个 RQ。 |
| `03-security-objective-threat-model.tex` | 2 安全目标与威胁模型 | 保留任意有限批次目标、批次组合对手、精确来源关系和分析边界；按任务要求显式拆出建模假设。 |
| `references.bib` | `bibliography/references.bib` | 全量复制，BibTeX key 未改变。 |

## 3. 章节结构是否改变

没有改变英文母稿的论证顺序，也没有把安全目标与威胁模型压回问题定义章节。中文编号按任务要求设为“0 引言、1 问题定义、2 安全目标与威胁模型”。

唯一的细分调整是把英文 Section 3 中分散在 `Batch-Composition Adversary`、`Analysis Boundary` 及前文 scope 段落里的共同模型假设集中为中文第 2.3 节“建模假设”，并将直接证据终点和非目标归入第 2.4 节。该调整没有增加模型、能力或研究结论。

本阶段没有创建或翻译英文 Section 4--8 的正文，也没有生成、重绘或修改论文图。

## 4. `sid` / `oid` 处理

中文叙述使用

```text
oid ≡ sid_model
```

首次出现处已经说明：英文母稿和 Tamarin 源模型仍使用 `sid`；中文改用 `oid` 只是为避免与 K-Waay transcript `sid` 混淆，不修改变量、规则、事件或模型语义。除这一说明外，中文公式和叙述统一使用 `oid`。完整规则见 `notes/TERMINOLOGY_MAP.md`。

## 5. 英文母稿之后更新的事实

**SOURCE FACT UPDATED AFTER ENGLISH MANUSCRIPT**

英文摘要和引言仍称 RQ-v2 没有 raw prover transcripts。`reviews/2026-09-16-evidence/` 已记录后续独立复跑，包含运行清单、输入与输出哈希、parse/prove 标准输出和错误输出，以及三个模型的 JSON 导出轨迹；复核结果与当前抽象中的既有结果一致。

中文摘要和引言已改为当前事实，同时保留两项边界：该证据是独立审查复跑，不是历史运行记录的恢复；可复现性更新不改变从模型结果到协议或部署结论的证据层级。

## 6. 术语确认状态

没有阻塞本阶段的无法自然翻译术语。正文保留 `BatchReceive`、`Send`、`ReceiverAccept`、KEM、KDF、split-KEM、Tamarin 等技术名，并采用“参与方”“发送实例”“批处理接纳”“批次组合对手”“精确来源”等译法。

后续可由作者作编辑性偏好确认的非阻塞项只有两组：“参与方／协议主体”和“批处理接纳／批次接纳”。当前稿分别选择“参与方”和“批处理接纳”，并在需要强调抽象层次时使用“建模协议主体”。

## 7. 完整性与遗漏检查

- 英文前半部分的核心论证均有中文去向；未发现缺失的研究问题、定义、公式或证据边界。
- 保留 7 个 `equation` 环境及原有公式标签语义；另保留身份坐标表标签。
- 保留 `\cite{}`、带定位参数的 `\cite[...]`、`\eqref{}` 和 `\ref{}`，未改为手写参考文献编号。
- 保留 RQ1、RQ2、RQ3；参与方级模型仍是正控制，没有制造第四个问题。
- 动机对象 `B^*` 明确标为分析示例，不是机器攻击轨迹。
- 任意有限批次只用于定义目标，机器范围明确限定为 `n=2`。
- 未把模型能力写成真实部署攻击能力，未新增密码学攻击、实现漏洞或协议级认证失败结论。
- 英文前半部分没有需要继承的 figure 输入或引用，因此没有图占位遗漏。
- 本阶段未运行或修改 Tamarin，未改动英文母稿、旧中文稿、证据目录或其他项目文件。

## 8. LaTeX 编译与视觉检查

主编译命令：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

结果：成功，退出码为 0；XeLaTeX、BibTeX 和 `xdvipdfmx` 均完成，生成 6 页 `main.pdf`。最终 `main.log` 中没有未定义引用、未定义标签、overfull/underfull box 或相关 LaTeX 警告。引用、公式编号、章节编号、三线表和中文字体均正常。

Codex 内置编译器在当前 Windows 环境报告 `Unable to find standard directories for platform`，因此没有用它取得编译结果；随后使用项目主机上的 TeX Live 2025 完成了完整多文件 XeLaTeX/BibTeX 编译。该工具环境限制不影响生成的 PDF。

PDF 已按 150 dpi 渲染并逐页检查。检查后修复了跨章节页眉提前变化和长术语断行问题；最终页面未发现文字裁切、表格越界、公式重叠、缺字或不可读引用。

## 9. 后续翻译准备度

当前 `main.tex`、共享 preamble、宏、章节控制方式、术语映射和完整参考文献库可直接承接英文 Section 4--8。后续应继续遵守当前 `oid ≡ sid_model` 映射、`ReceiverAccept` 证据终点以及固定两槽和精确来源边界。

**AROCMAG_CHINESE_LATEX_TASK1A_READY**
