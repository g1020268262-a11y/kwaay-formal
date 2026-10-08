# 图2最终措辞修订与冻结报告

## 1. 基线与任务范围

- 基线提交：`e019b59cfaeaa6b75bae73cd6d2a3f08d6c05bc0`
- 图题：无互异约束模型中的重复接受可达执行
- 本轮范围：两处指定措辞、第三方参考PDF副本清理、预览与全文重编和冻结。
- 未重新设计图2，未修改图1、Tamarin模型、lemma、14项验证结果或正文论证。

## 2. 两处措辞修改

### 2.1 顶部唯一性说明

- 修改前：`匹配发送来源（该完整元组唯一）`
- 修改后：`唯一匹配Send来源`

修改后的文字限定的是：对所示完整元组`(A,oid,m)`，与之匹配的`Send`事件发生点唯一。图中继续完整保留`Send(A,oid,m) @ s`。

该性质不能解释为整个执行只有一次`Send`，也不能推出参与方`A`只能发送一次或完整元组在所有位置全局不可重复。存在性lemma的全称子句只把与该完整元组匹配的所有`Send`发生点约束为同一时间点`s`。

### 2.2 图下注中的额外Send

- 修改前：`执行中可能存在其他无关Send。`
- 修改后：`执行中可能存在与其不匹配的其他Send。`

正式论文和独立预览现统一使用：

> 依据Tamarin模型及独立复核的可达执行重构，仅显示与所示完整元组相关的关键事件；该元组的匹配Send唯一，执行中可能存在与其不匹配的其他Send。

独立复核graph中省略的协议`Send`具有相同参与方分量，但发送实例标识和消息分量不同，因而不匹配图中所示完整元组。它可能参与其他知识推导，所以不能称为对整个执行完全无关；省略它也不等于删除了第二个匹配`Send`。

## 3. 第三方参考PDF清理

已确认`fig2-qa/reference-pdfs/5G-CCS18.pdf`和`OAuth-CCS16.pdf`只是图形风格研究期间下载的第三方论文副本，不是本项目原创产物，不被LaTeX构建、Tamarin模型、lemma或机器证据链引用。

由于未核实这两份作者PDF的再分发许可，已从项目提交内容中移除。`FIG2_REFERENCE_ANALYSIS.md`和`FIG2_DESIGN_REPORT.md`继续保留论文标题、作者、会议、DOI、原始公开URL、参考图号、PDF物理页码、文件核对哈希及图形风格分析结论。

## 4. 科学内容与布局守恒

- `SendMessage`、`CollectSlot1`、`CollectSlot2`、`AdmitRelaxedBatch`、`ProcessSlot1`和`ProcessSlot2`未修改。
- `one_send_two_accepts_exists`与`receiver_accept_injective`未修改，机器结果和14项汇总结果未修改。
- 图中继续保持`E_1=E_2=(A,\mathit{oid},m)`和`s<b<r_1<r_2`。
- 两个`ReceiverAccept`事件的五个参数完全相同，仅发生时间`r_1`和`r_2`不同。
- 单个持久事实`!Sent(A,oid,m)`仍由两条虚线分别连接两个处理步骤。
- TikZ只替换顶部一行文字；时间轴方向、节点坐标、主节点布局、事件顺序、线型、灰度、框体和箭头均未改变。

## 5. 产物一致性与视觉检查

独立预览使用下列命令完全清理后重建：

```text
latexmk -C fig2-preview.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error fig2-preview.tex
```

全文使用下列命令完全清理后重建：

```text
latexmk -C main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

已实际打开`fig2-preview.pdf`和`main.pdf`物理第7页。两者与当前TikZ源码一致：顶部唯一性文字和图下注均为修订版本；单栏文字可读；两条来源读取虚线、相同的两个槽位条目、共同批次上下文、两个接受事件及时间顺序均完整可见；未发生裁切、重叠或布局变化。

## 6. 编译QA

| 检查项 | 独立预览 | 全文 |
|---|---:|---:|
| PDF页数 | 1 | 11 |
| undefined references | 0 | 0 |
| undefined citations | 0 | 0 |
| missing glyphs | 0 | 0 |
| overfull boxes | 0 | 0 |

两个XeLaTeX构建均以退出码0完成。最终产物SHA-256：

- `fig2-preview.pdf`：`BE81E8FC048DD19AFA3796A5789A80E5F537DA8431010B451267CE866573E7D5`
- `main.pdf`：`EB5E177E69A5CB6BED07AE4A19D8DD9AB03BAA78D13BC0201BCF972144E4428B`

## 7. 冻结状态

**FIGURE 2 FROZEN**

后续不得修改图2科学内容或视觉结构；仅允许投稿版尺寸适配、EMF/vector转换和明显排版错误修复。

最终状态：`AROCMAG_FIG2_FROZEN_READY`
