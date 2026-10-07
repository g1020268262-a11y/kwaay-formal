# 图1产物重建与冻结报告

## 1. 基线与源码

- 任务：`AROCMAG_FIG1_ARTIFACT_REBUILD_AND_FREEZE`
- 基线提交：`102fa2e652d42bf2233570ca43797ca2781ad64d`
- 当前TikZ源码：`submissions/arocmag/latex-v2/figures/fig1-two-slot-lifecycle.tex`
- 源码SHA-256：`09EF99E6E62227E67224425FF80A5295AC103BAC8226D9E956148ABA30726C72`
- 源码状态：与基线提交一致，本任务未修改该文件。

## 2. 独立预览重建

在`submissions/arocmag/latex-v2/figures/`中执行：

```text
latexmk -C fig1-preview.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error fig1-preview.tex
```

完整清理删除了旧预览PDF及辅助文件，随后从当前`fig1-preview.tex`和TikZ源码重新生成`fig1-preview.pdf`，未复用旧缓存产物。新预览为1页矢量PDF，SHA-256为`566698C2AEAC87B9E6A4A172923755B3C1DBBBC1D9774792C68F0BC39A26EA28`。

对新预览进行实际渲染检查后，确认其为已审查的7主单元版本：

1. 发送实例与候选条目暴露；
2. 候选条目组合（攻击者可控）；
3. 两槽顺序收集；
4. 批次准入（受控变化）；
5. 处理槽位1并匹配发送来源；
6. 处理槽位2并匹配发送来源；
7. 处理完成与`BatchComplete`终止状态。

`BatchReceive`和两个`ReceiverAccept`均位于转移箭头上。右侧小型虚线拒绝框明确限定为消息互异和参与方互异模型。预览中不存在旧版独立“批次获准”框、独立`ReceiverAccept`大框、分离的Send/Expose大框或分离的Slot1/Slot2大框。

## 3. 全文重建

在`submissions/arocmag/latex-v2/`中执行：

```text
latexmk -C main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

全文同样在完全清理旧辅助文件和旧PDF后重新生成。`main.pdf`为10页A4 PDF，SHA-256为`428669D4A71338D7321DAA6A6663A278ABA1B2C72DBB840091F649C5E7CC5E0C`。

## 4. 三方一致性核验

已实际打开独立预览和`main.pdf`第5页进行视觉核对。三者关系如下：

| 核验对象 | 结果 |
|---|---|
| TikZ源码 | 7个主单元；动作事实置于箭头；`Reject`范围受限；`BatchComplete`为终止状态 |
| 独立预览 | 与源码的节点、文字、箭头、灰度层级和图题一致 |
| 正文图1 | 与独立预览一致，保持单栏纵向布局，字体可读，无裁切或越界 |

因此，`fig1-two-slot-lifecycle.tex`、`fig1-preview.pdf`和`main.pdf`中的图1三方一致。

## 5. 已审查模型结构守恒

重建后的图1仍保持已通过人工审查的结构：7个主要视觉单元；`BatchReceive`与`ReceiverAccept`作为箭头动作事实；拒绝支路只属于消息互异和参与方互异模型；`BatchComplete`作为终止状态；批次准入节点是唯一浅灰视觉中心；整体采用黑白/灰度、薄框、单栏纵向表达。

本任务没有修改正文科学内容、Tamarin模型、14项验证结果、图题或图1的科学与视觉设计，也没有开始图2。

## 6. 编译QA

| 检查项 | 独立预览 | 全文 |
|---|---:|---:|
| PDF页数 | 1 | 10 |
| undefined references | 0 | 0 |
| undefined citations | 0 | 0 |
| missing glyphs | 0 | 0 |
| overfull boxes | 0 | 0 |

两个构建均以退出码0完成。

## 7. 冻结状态

**FIGURE 1 FROZEN**

后续除投稿版尺寸适配、EMF/vector转换和明显排版错误外，不得再修改图1的科学内容或视觉结构。

最终状态：`AROCMAG_FIG1_FROZEN_READY`
