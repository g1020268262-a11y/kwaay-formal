# 图2设计与科学映射报告

任务：AROCMAG_FIGURE2_DUPLICATE_ACCEPTANCE_TRACE

状态：**AROCMAG_FIG2_READY_FOR_REVIEW**

日期：2026-10-08（Asia/Shanghai）。正文 TEXT CONTENT FROZEN；图1 FIGURE 1 FROZEN / AROCMAG_FIG1_FROZEN_READY。只制作图2，未运行 Tamarin，未修改模型或14项结果，未制作图3、Word、EMF，未 commit / push。

## 1. 交付物与证据边界

- [可编辑TikZ](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-duplicate-acceptance-trace.tex)
- [单栏预览源码](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-preview.tex)
- [单栏预览PDF](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-preview.pdf)
- [参考图研究](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/FIG2_REFERENCE_ANALYSIS.md)
- [全文PDF](D:/kwaay-formal/submissions/arocmag/latex-v2/main.pdf)，11页，图2在物理第7页；第3.1节图引用在物理第6页。
- [静态核对及编译检查记录](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/qa-summary.json)
- [预览编译日志](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/fig2-preview-build.log)、[全文编译日志](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/main-build.log)
- [96dpi单栏灰度预览](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/fig2-column-96dpi-gray.png)、[180dpi预览](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/fig2-preview-180dpi.png)、[全文图2页](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/main-page-07.png)

图题：**无互异约束模型中的重复接受可达执行**。

图为真实模型和独立复核可达执行的关键事件投影。它不是原始Tamarin截图，不是完整constraint graph，也不构成完整K-Waay协议或部署攻击的声明。两个接受只是模型中的 `ReceiverAccept` 事件。

已完整读取的任务权威：

1. [rqv2_relaxed.spthy](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_relaxed.spthy)，全部规则及性质。
2. [trace-audit-summary.txt](D:/kwaay-formal/reviews/2026-09-16-evidence/trace-audit-summary.txt)。
3. [rqv2_relaxed-traces.json](D:/kwaay-formal/reviews/2026-09-16-evidence/rqv2_relaxed-traces.json)，完整解析3个graph的所有节点、事实和边，重点核对下述2个graph。
4. [result-comparison.tsv](D:/kwaay-formal/reviews/2026-09-16-evidence/result-comparison.tsv)，14项全部为MATCH。
5. [prototype-execution-report.md](D:/kwaay-formal/docs/rq-v2/prototype-execution-report.md)。
6. [冻结第3节源码](D:/kwaay-formal/submissions/arocmag/latex-v2/sections/04-formal-analysis.tex)及[图目录README](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/README.md)。
7. [旧FIGURE_2_SPEC.md](D:/kwaay-formal/submissions/arocmag/draft/figures/FIGURE_2_SPEC.md)，仅作为科学检查表，未继承旧标题、术语、蓝橙配色或横向布局。

另核对独立复核的 [prove输出](D:/kwaay-formal/reviews/2026-09-16-evidence/rqv2_relaxed-prove.stdout.txt)和[运行清单](D:/kwaay-formal/reviews/2026-09-16-evidence/independent-rerun-manifest.json)。该复核在2026-09-16执行；本次只是读取和核对已有证据，不产生新的证明运行。

## 2. 独立复核结果及两个性质视角

| 性质 | 独立复核结果 | 步数 | 本图语义 |
|---|---|---|---|
| `one_send_two_accepts_exists` | verified | 13 steps | 存在一个完整元组的唯一匹配发送支持同批两个不同接受事件 |
| `receiver_accept_injective` | falsified, found trace | 13 steps | 上述重复接受形状使批内来源单射性不成立 |
| `receiver_accept_has_send` | verified | 8 steps | 接受具有更早的完整元组匹配发送，不能解释为无来源接受 |

前两项是同一种重复接受形状的两种性质视角，不是两条不同攻击。图中不显示lemma名或证明步数。

存在性graph（以下简称G-ex）：

```text
trace_RQv2_Relaxed_SL2-AS0-CL0-A1-C1-NB_one_send_two_accepts_exists-CreateParty-CollectSlot2-ProcessSlot1-AdmitRelaxedBatch-SendMessage-ProcessSlot2-ProcessSlot1-SendMessage-SendMessage-SendMessage-SendMessage
```

单射性反例graph（以下简称G-inj）：

```text
trace_RQv2_Relaxed_SL2-AS0-CL0-A1-C1-NB_receiver_accept_injective-case_1-CreateParty-ProcessSlot1-AdmitRelaxedBatch-SendMessage-ProcessSlot2-ProcessSlot1-SendMessage-SendMessage-SendMessage-SendMessage
```

两者各有16个节点、26条边。graph标签末尾的证明分支名称不是执行事件数量；不能按标签里 `SendMessage` 的重复次数计数。规则节点、动作事实和证明步骤始终分开理解。

## 3. 符号与时间映射

模型使用 `sid`，冻结正文使用 `oid`。图仅按正文约定重命名坐标，保持位置和含义不变：

```text
graph ~a   -> 图 A
graph ~sid -> 图 oid（发送实例标识）
graph ~m   -> 图 m
graph ~bid -> 图 bid
graph ~rst -> 图 rst
```

`E=(A,oid,m)` 是对模型网络项 `<A,sid,m>` 的显示记法。图没有新增构造器，也没有改写任何模型规则。

G-ex中的 `#s/#b/#r1/#r2` 分别显示为 `s/b/r₁/r₂`。G-inj的准入节点是 `#vr.1`，在图中将其 `BatchReceive` 发生位置记作 `b`，并非声称该graph包含一个字面ID为 `#b` 的节点。

纵轴只表达先后顺序，不表达真实时间间隔。未显示 `CreateParty`、`CreateBatch` 及完整攻击者知识推导，不能从图推出它们与其他省略节点的完整排序。

## 4. 逐元素科学映射

| 图中元素 | Tamarin rule / fact / action | 独立graph证据 | 冻结正文语义 |
|---|---|---|---|
| `Send(A,oid,m) @ s` | `SendMessage` 的动作 `Send(A,~sid,~m)` | G-ex/G-inj：`#s`，动作 `Send(~a,~sid,~m)` | 所示完整元组的匹配发送来源；不是整个执行唯一的发送 |
| 公开 `E=(A,oid,m)`、`Out(E)` | `SendMessage` 结论 `Out(<A,~sid,~m>)` | 两graph：`#s:c0 -> #vl.1:p0`，后者为攻击者 `Recv` 规则 | 条目被公开，网络可重复使用同一条目；发送规则没有再次执行 |
| 单个 `!Sent(A,oid,m)` | `SendMessage` 结论中的持久事实 `!Sent` | 两graph：`#s:c1` | 理想化的持久匹配来源事实，不是密码学身份认证 |
| 槽位1 `E=(A,oid,m)` | `CollectSlot1` 读取 `In(<A,sid,m>)`，产生 `OpenSlot2(bid,rst,A,sid,m)` | G-ex：`#vr.2`；G-inj：`#vr.3`；两者输入都是 `In(<~a,~sid,~m>)` | 首次收集同一完整元组；槽位标签是状态投影，不是新增action fact |
| 槽位2 `E=(A,oid,m)` | `CollectSlot2` 再读取相同 `In`，产生双份同元组的 `Collected` | G-ex：`#vr.1`；G-inj：`#vr.2`；两者输入仍为 `In(<~a,~sid,~m>)` | 再次选取/投递同一公开条目，不是不同消息或不同发送实例 |
| Out节点至两槽的同源实线支路 | 网络知识至两个 `In(E)` 输入；省略中间知识规则 | 两graph：`#vf.4:c0`进入槽位1，`#vf.3:c0`进入槽位2；其`In`项完全相同；`#vl.1`均早于两个投递节点 | 重复发生在候选条目组合/网络使用层，发送方不主动发送两次 |
| 同一批次边界 `(bid,rst)` | `OpenSlot1/OpenSlot2/Collected/AdmittedSlot1/AdmittedSlot2` 的相同批次坐标 | 两graph均从相同 `~bid,~rst` 状态沿收集和处理规则传递 | 两个接受在同一批次与接收方上下文；边界不是第二个协议参与者 |
| `BatchReceive(bid,rst) @ b` | `AdmitRelaxedBatch` 动作；规则只有 `Collected` 前提，无A/m互异guard | G-ex：`#b`；G-inj：`#vr.1`，动作均为 `BatchReceive(~bid,~rst)` | 无互异约束模型的批次准入事件 |
| 规则说明 `ProcessSlot1` | 读取 `AdmittedSlot1` 与持久 `!Sent`，产生 `AdmittedSlot2` | 两graph：`#r1`；`#r1:p1`读取同元组的持久事实 | 处理槽位1并匹配发送来源 |
| `ReceiverAccept(A,oid,m,bid,rst) @ r₁` | `ProcessSlot1` 的动作 `ReceiverAccept` | 两graph：`#r1`，参数为 `~a,~sid,~m,~bid,~rst` | 第一次模型接受事件；不表示握手、认证或密钥建立成功 |
| 规则说明 `ProcessSlot2` | 读取 `AdmittedSlot2` 与相同持久 `!Sent`，产生 `BatchComplete` | 两graph：`#r2`；`#r2:p1`再次读取同一来源 | 顺序处理槽位2；本图省略无关的完成状态 |
| `ReceiverAccept(A,oid,m,bid,rst) @ r₂` | `ProcessSlot2` 的动作 `ReceiverAccept` | 两graph：`#r2`，所有五个参数与`#r1`完全相同 | 第二次不同的事件发生，仅发生时间与r₁不同 |
| 两条虚线来源读取 | 持久事实复用，没有消耗或复制一个匹配发送动作 | 两graph均有 `#s:c1 -> #r1:p1` 与 `#s:c1 -> #r2:p1`，关系都为 `PersistentFact` | 一个来源支持两次处理；只画一个`!Sent`节点 |
| `s < b < r₁ < r₂` | 存在性lemma的显式顺序合取；处理状态链也保持顺序 | G-ex：`#b:c0 -> #r1:p0 -> #r2:p0`；G-inj：`#vr.1:c0 -> #r1:p0 -> #r2:p0`；匹配网络输出早于输入 | 先发送、再准入、随后两个不同时间点接受，尤其r₁≠r₂ |
| `E₁=E₂=(A,oid,m)` | `Collected` 的两个三元组分量相同 | 两graph：`Collected(~bid,~rst,~a,~sid,~m,~a,~sid,~m)` | 三个分量均相同，不是仅参与方相同 |

收集规则没有action fact，因此其框只标槽位数据、规则名与输入。四个动作事件使用数学动作名与`@`时间点；规则名另起小字号一行并带“规则：”。图没有把二者作为同一语义类别。

## 5. 唯一匹配发送与无关Send

存在性lemma含：

```text
All #s2. Send(A,sid,m) @ #s2 ==> #s2 = #s
```

这只保证该完整 `(A,sid,m)` 元组的匹配发送发生点唯一。图中使用“匹配发送来源（该完整元组唯一）”，图注附近保留如下限定：

> 依据Tamarin模型及独立复核的可达执行重构。仅显示与完整元组相关的关键事件投影；该元组的匹配Send唯一，执行中可能存在其他无关Send。

两graph实际上都还有一个协议 `SendMessage` 节点：

| graph | 省略节点 | 动作 | 与所示元组的关系 |
|---|---|---|---|
| G-ex | `#vr.4` | `Send(~a,~sid.1,~m.1)` | 同参与方，发送实例标识和消息不同，不匹配完整所示元组 |
| G-inj | `#vr.5` | `Send(~a,~sid.1,~m.1)` | 同参与方，发送实例标识和消息不同，不匹配完整所示元组 |

因此省略的是与目标完整元组匹配关系无关的Send，没有删除一个与该元组匹配的第二个Send。所谓“无关”是相对于图所强调的元组匹配和来源对应；额外发送在完整知识依赖图中仍参与获取参与方分量的知识推导，不能据此声称它与整个constraint graph的所有推导都无关。

graph中的 `#vf.3/#vf.4` 另有名为 `Send` 的攻击者规则节点，它们的动作是 `K(<~a,~sid,~m>)`，结论是 `In`。这些是网络投递规则，不是协议动作事实 `Send(A,sid,m)`，也不是第二次匹配发送。正式图只以公开条目至两个槽位的分支表示它们。

## 6. 参考图与版式决策

完整细项见[参考记录](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/FIG2_REFERENCE_ANALYSIS.md)。在图2源码创建前，已实际查看：

- P1《基于Tamarin的MQTT协议安全性分析方法》：物理第5页图7是工具截图；第2页图2、第6页图8是向下时间的细线时序图；第2/3页图3/4/5为状态迁移图。
- H1 [A Formal Analysis of 5G Authentication](https://people.inf.ethz.ch/rsasse/pub/5G-CCS18.pdf)，ACM CCS 2018作者扩展版本：物理第5页Figure 3，纵向生命线、状态框、相同消息标识、黑白/浅灰。该参考图本身是协议流程，未将其误写成反例图。
- H2 [A Comprehensive Formal Security Analysis of OAuth 2.0](https://publ.sec.uni-stuttgart.de/FettKuestersSchmitz-CCS-2016.pdf)，ACM CCS 2016：物理第5页Figure 3，将形式化分析发现的路径整理为可读顺序及数据标签。只借鉴表达，不引入其OAuth攻击结论。

为便于复查，保留本次实际查看的作者PDF副本：

| 副本 | 页数/所查页 | SHA-256 |
|---|---|---|
| [5G作者扩展PDF](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/reference-pdfs/5G-CCS18.pdf) | 21页/物理第5页 | `2878bfacffd1118c67f9a26cd4401544b83391a1c7b593a55519d189af6d0e1c` |
| [OAuth作者PDF](D:/kwaay-formal/submissions/arocmag/latex-v2/figures/fig2-qa/reference-pdfs/OAuth-CCS16.pdf) | 12页/物理第5页 | `799f2c2f4027b15b08a7d1c2fac8340db47a7ea40992a02aed887cd484bc81e2` |

这些只用于图形研究，不作为本稿新增安全证据，也不加入冻结参考文献。

图2采用向下时间轴。若把7个阶段横排在8.2cm内，阶段说明及完整接受参数会争夺水平空间。纵向图能保留9pt动作文字、7.5pt规则说明，且让单一Out分支、持久来源复用和顺序接受同时可读。没有使用 `figure*` 或缩放整个图。

视觉参数：白底；0.35pt框/依赖线；0.45pt实线箭头；1pt圆角；接受事件仅7%黑浅灰。时间点为小实心标记，无装饰图标、阴影、渐变或大面积颜色。动作事件的灰度和线宽与冻结图1协调，但图2没有重画三种准入分支或完整生命周期。

## 7. 科学QA

| 必查项 | 结果及依据 |
|---|---|
| SendMessage产生Send、Out、!Sent | PASS：源码和两graph的`#s`均一致 |
| CollectSlot1读取In(E) | PASS：G-ex `#vr.2` / G-inj `#vr.3` |
| CollectSlot2再次读取同一In(E) | PASS：G-ex `#vr.1` / G-inj `#vr.2`，输入项完全相同 |
| 准入没有A/m互异guard | PASS：`AdmitRelaxedBatch`只有`Collected`前提 |
| ProcessSlot1读取匹配来源并产生第一次接受 | PASS：`#r1:p1`及`#r1`动作 |
| ProcessSlot2再次读取同一来源并产生第二次接受 | PASS：`#r2:p1`及`#r2`动作 |
| 两槽完整A/oid/m相同 | PASS：两次In及Collected各分量一致，图中逐项原样显示 |
| 两接受完整五参数相同 | PASS：静态比较动作参数列表完全相等 |
| 两接受时间不同且有序 | PASS：事件ID为`#r1/#r2`；状态边`#r1:c0 -> #r2:p0`；存在性lemma规定r₁<r₂ |
| s<b<r₁<r₂ | PASS：lemma显式合取与图中关系一致 |
| 匹配完整元组的Send唯一 | PASS：lemma的全称子句；两graph协议Send动作中各只有1个完整匹配 |
| 两性质13 steps、状态正确 | PASS：TSV及prove输出；两项均MATCH |
| 额外Send处理正确 | PASS：各有1个不同sid/m的额外Send，图省略，正文图注限定，报告列出真实节点 |

静态QA完整读取导出JSON，核对相同动作参数、两槽输入、共享持久边、处理状态边、额外发送数和14行结果。这是对记录证据的核对，不是新的Tamarin证明。

## 8. 视觉QA与编译

| 视觉QA项 | 结果 |
|---|---|
| 单栏真实尺寸 | PASS：预览minipage为8.2cm；未使用resizebox；PDF总宽8.622cm含两侧6pt留白，正文内容宽8.2cm |
| 字体可读 | PASS：主信息9pt、规则及图例7.5pt；已查看180dpi及96dpi灰度渲染 |
| 两槽完全相同 | PASS：每个槽位均显示`E=(A,oid,m)`，底部再给出E₁=E₂ |
| 两接受同bid/rst | PASS：完整参数均显示，同时置于共同批次边界 |
| r₁/r₂明显不同 | PASS：轴上不同位置、事件内各自标注时间、下方明确不等式 |
| 时序明确 | PASS：向下时间轴及s<b<r₁<r₂ |
| 一个!Sent供两次读取 | PASS：单节点、同一虚线干线、两条指向处理框的读取箭头 |
| 无第二个匹配Send | PASS：图主体只显示一个协议Send动作 |
| 未画成发送方发送两次 | PASS：分支来自单个Out公开条目；两槽分别读取In(E) |
| 箭头交叉 | PASS：网络支路在左侧、来源读取在右侧；两者不相交；跨共享上下文框线只是进入同一上下文 |
| 密度及边距 | PASS：规则次级标注，接受完整参数不换行；公开条目和来源事实分开，文字未碰框 |
| 黑白打印 | PASS：全部黑白/灰度，语义由时间、线型和符号表示 |
| 核心关系突出 | PASS：顶部唯一匹配来源、两个相同槽位、两个浅灰接受事件构成主链 |
| 全文落位 | PASS：已检查物理第6–8页；图引用、图题编号2和图注正确，未裁切或重叠 |

执行命令：

```text
cd D:/kwaay-formal/submissions/arocmag/latex-v2/figures
latexmk -xelatex -interaction=nonstopmode -halt-on-error fig2-preview.tex

cd D:/kwaay-formal/submissions/arocmag/latex-v2
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

最终两项退出码均为0。

| 最终日志 | undefined refs | undefined citations | missing glyphs | overfull boxes |
|---|---:|---:|---:|---:|
| fig2-preview | 0 | 0 | 0 | 0 |
| main | 0 | 0 | 0 | 0 |

正文唯一改动是替换原两行图2占位注释，加入一句图引用及figure环境、短图题和证据说明。原有段落、公式、14项结果、参考文献均未改写。当前全文保留原版式；图2按目标8.2cm列宽居中，编译后的浮动图位于第3.1节引用的下一页。

## 9. 冻结边界核对

| 受保护文件 | 本次前后SHA-256（相同） |
|---|---|
| rqv2_relaxed.spthy | `e5129575720020aa3f509782c2052fbf2114a540d013126f5a75d316cbabaf9d` |
| rqv2_relaxed-traces.json | `78fc92c506df4e5fb5ab61c2d0ee711f8408ae7a39cc5bbb2913759600e28986` |
| result-comparison.tsv | `27826a17a5e0eb90ebf40647dc1e5055285a58ce5641ea3bebf343b23b2bb4e6` |
| fig1-two-slot-lifecycle.tex | `09ef99e6e62227e67224425ff80a5295ac103bac8226d9e956148aba30726c72` |
| fig1-preview.pdf | `566698c2aeac87b9e6a4a172923755b3c1dbbbc1d9774792c68f0bc39a26ea28` |

Git受跟踪内容改动限定为第3节的图2插入、图目录README的图2状态和重编译全文PDF。图2源码、预览、两份报告和其QA/参考资料为新增文件。图1全部独立资产没有修改。

## 10. 九项设计问题的最终回答

1. **为什么不是图1的复制？** 图1是三种模型共享生命周期与准入对照；图2只显示一次经审计执行，具有s/b/r₁/r₂时间轴、相同完整条目的重复输入、单个来源的两次读取和两个接受发生点，没有三分支或一般完成路径。
2. **参考哪些图？** P1图7用于判断截图不适用，P1图2/8用于细线纵向时序及短图题；CCS 2018的5G作者扩展PDF Figure 3用于时间与状态分层；CCS 2016 OAuth Figure 3用于可读路径投影。全部实际查看PDF。
3. **为什么当前时间方向？** 所看时序参考图均向下；8.2cm中纵向排列能保留完整参数，避免横向7阶段导致缩字。
4. **为什么当前事件表示？** 以数学动作名与时间点为主层，小字号规则名为说明层；收集规则只显示状态和输入，保持rule/action语义区别。
5. **如何表现同一来源复用？** 只有一个`!Sent(A,oid,m)`节点，右侧同一虚线干线分成两条读取箭头，对应两条真实PersistentFact边。
6. **如何表现接受事件不同？** 完整五参数相同，而两框时间分别为r₁/r₂；纵轴和r₁<r₂显示两次发生，底部明确r₁≠r₂。
7. **如何处理无关Send？** 省略G-ex `#vr.4` / G-inj `#vr.5` 的不同sid/m发送；图注限定唯一性只针对完整所示元组，报告保留其参数和知识依赖边界。
8. **为什么不用Tamarin截图？** 截图保留证明界面与知识展开，单栏信息密度过高；本文需要经审计的相关事件投影，故依据真实节点与边重构可编辑TikZ。
9. **为什么不称完整K-Waay攻击？** 当前两槽抽象只表达准入、来源匹配与模型接受；没有完整密码机制、上层安装或部署服务，且所示执行未满足原有参与方互异条件。
