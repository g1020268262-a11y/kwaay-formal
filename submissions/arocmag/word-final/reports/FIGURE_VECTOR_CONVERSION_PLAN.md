# Figure vector conversion plan

## Stage 1 status

图1和图2的科学内容及TikZ结构保持冻结。本阶段没有重画、改字、改布局或改图义。

Word工作稿当前插入方式：

- 保留当前冻结的`fig1-preview.pdf`和`fig2-preview.pdf`作为矢量来源副本；
- 从当前PDF以360 dpi生成单栏PNG占位图；
- 仅裁去独立预览中已经包含的图题和图2说明，避免与Word中的可编辑图题/说明重复；
- 图题及图2说明均以Word文本保留。

## Fig.1

- 名称：两槽批次准入的共同生命周期。
- 权威源：`latex-v2/figures/fig1-two-slot-lifecycle.tex`。
- 当前矢量中间件：`word-final/figures/fig1-preview.pdf`。
- 当前Word对象：`fig1-word-placeholder.png`，360 dpi，单栏内联。
- 后续方案：TikZ → PDF → SVG/EMF；优先使用保持文本和线条为矢量的EMF转换链。
- 转换后QA：7个主单元、箭头action fact、Reject范围、BatchComplete、灰度层级、单栏宽度逐项对照。

## Fig.2

- 名称：无互异约束模型中的重复接受可达执行。
- 权威源：`latex-v2/figures/fig2-duplicate-acceptance-trace.tex`。
- 当前矢量中间件：`word-final/figures/fig2-preview.pdf`。
- 当前Word对象：`fig2-word-placeholder.png`，360 dpi，单栏内联。
- 后续方案：TikZ → PDF → SVG/EMF；保持时间轴、来源读取虚线、两个接受事件和共同批次边界不变。
- 转换后QA：唯一匹配Send表述、两个ReceiverAccept、`E_1=E_2`、`s<b<r_1<r_2`及图下注逐项对照。

## Acceptance gate for final EMF

1. EMF在Word与PDF中均保持清晰，不发生字体替换或裁切。
2. EMF与当前冻结PDF的科学内容逐项一致。
3. 图号、图题、正文引用和图2证据说明保持不变。
4. 转换后重新渲染并逐页检查。

状态：`EMF_VECTOR_CONVERSION_PENDING`

