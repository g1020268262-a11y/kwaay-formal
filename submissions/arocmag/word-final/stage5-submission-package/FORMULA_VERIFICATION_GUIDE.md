# Stage 5 公式核对指南

## 当前真实状态

- 当前稿件含 99 个可编辑 OMML 数学对象：86 个行内对象、13 个展示公式成员。
- 展示公式段落共 6 项，其中编号公式 3 项、未编号公式 3 项。
- 当前环境未检测到真正的 MathType 转换链，因此状态保持为 `MATHTYPE_CONVERSION_BLOCKED`。
- `FORMULA_VERIFICATION_CHECKLIST.csv` 已逐项列出 99 个对象，并预留转换、可编辑性、符号和视觉核对栏。

## Microsoft Word + MathType 6.9d 人工转换流程

1. 将整个 `stage5-submission-package` 复制到不受 Git 跟踪的私有目录，在副本上操作。
2. 使用 Microsoft Word 打开 Stage 5 Word，先确认 MathType 6.9d 选项卡和 `Convert Equations` 命令真实可用。
3. 另存为带 `-mathtype-private` 后缀的新文件，不覆盖本包中的 OMML 基线。
4. 打开 **MathType → Convert Equations**：来源勾选 `Word 2007 and later (OMML) equations`，`Range` 选 `Whole document`，目标选 `MathType equations (OLE objects)`。
5. 转换完成对话框必须报告 99 项。保存、关闭并重新打开副本后，剩余 OMML 应为 0，MathType OLE/embedding 对象应为 99；任一数量不符都保持阻塞。
6. 依 `FORMULA_VERIFICATION_CHECKLIST.csv` 的 1—99 顺序核对；每个对象必须能够双击进入 MathType 编辑器，不能只凭外观判断。
7. 重点检查 `⇏`、`⇒`、`⇔`、`≜`、`≠`、`≤`、`≥`、`∧`、`…`、`τ`、Unicode 上下标、$P_\tau$、$M_\tau$、$I_\tau$、`ReceiverAccept`、`DistinctPartyPerBatch` 和时间关系；当前 99 个 OMML 中没有 `∃`。
8. 重点逐行核对含 4 个对象的段落 133 和含 5 个对象的段落 142（式(3)），确认换行、正体算子和 Unicode 下标没有漂移；再核对其余 4 个展示公式及 (1)—(3) 编号。
9. 更新域并重新分页，用 Microsoft Word 导出 PDF；逐页检查六页，特别检查首页、式(1)—(3)、表4和末页参考文献。
10. 只有全部 99 行的四个核对栏均已勾选，且最终 PDF 通过视觉检查，才可将状态改为 MathType 已完成。

## 六项展示公式

### 1. 未编号展示公式 — `02-problem.tex`

```latex
S=\bigl((\mathit{pk}_{j_1},\mathit{prek}_{j_1},m_{j_1}),\ldots,
           (\mathit{pk}_{j_d},\mathit{prek}_{j_d},m_{j_d})\bigr),
  \qquad d\geq 1,
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换
### 2. 式(1) — `02-problem.tex`

```latex
E_i=(A_i,\mathit{oid}_i,m_i),
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换
### 3. 式(2) — `03-formal-modeling.tex`

```latex
\mathsf{DistinctPartyPerBatch}(B)
  \triangleq
  \forall\,1\leq i<j\leq n,\quad
  \mathsf{party}(E_i)\neq\mathsf{party}(E_j).
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换
### 4. 未编号展示公式 — `03-formal-modeling.tex`

```latex
\begin{aligned}
  \forall A,\mathit{oid},m,\mathit{bid},\mathit{rst},s,r_1,r_2:\quad
  &\mathsf{Send}(A,\mathit{oid},m)@s \\
  {}\land{}&\mathsf{ReceiverAccept}(A,\mathit{oid},m,\mathit{bid},\mathit{rst})@r_1 \\
  {}\land{}&\mathsf{ReceiverAccept}(A,\mathit{oid},m,\mathit{bid},\mathit{rst})@r_2 \\
  {}\land{}&s<r_1\land s<r_2
  \quad\Longrightarrow\quad r_1=r_2.
\end{aligned}
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换
### 5. 未编号展示公式 — `03-formal-modeling.tex`

```latex
P_\tau\Rightarrow M_\tau,\qquad M_\tau\Leftrightarrow I_\tau.
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换
### 6. 式(3) — `04-formal-analysis.tex`

```latex
\begin{aligned}
    &\mathsf{Send}(A,\mathit{oid},m)@s,\\
    &\mathsf{BatchReceive}(\mathit{bid},\mathit{rst})@b,\\
    &\mathsf{ReceiverAccept}(A,\mathit{oid},m,\mathit{bid},\mathit{rst})@r_1,\\
    &\mathsf{ReceiverAccept}(A,\mathit{oid},m,\mathit{bid},\mathit{rst})@r_2,\\
    &s<b<r_1<r_2.
  \end{aligned}
```

- [ ] 已转换为真正的 MathType 对象
- [ ] 双击后由 MathType 打开并可编辑
- [ ] 与 LaTeX 源逐字符核对
- [ ] 编号、居中、字号和行距正确
- [ ] Word 导出 PDF 后无裁切或符号替换

## 禁止做法

- 不得把公式转成图片并称为 MathType。
- 不得把 OMML、OLE 占位或扩展名修改称为 MathType 转换完成。
- 不得只检查 6 个展示公式而忽略 86 个行内对象。
- 不得在未完成双击编辑验证和 PDF 复核时标记转换完成。
