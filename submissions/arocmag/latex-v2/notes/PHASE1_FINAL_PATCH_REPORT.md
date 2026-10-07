# AROCMAG Phase 1 Final Language Patch Report

## 1. 任务与修改边界

- 任务：`AROCMAG_PHASE1_FINAL_LANGUAGE_PATCH`
- 修改范围：仅 `submissions/arocmag/latex-v2/`
- 未改变章节结构、研究问题、Tamarin 模型、style-study 或英文母稿。
- 未续写第3--5章，未生成论文插图，未执行 commit 或 push。

## 2. 中文摘要压缩

中文摘要现为137个中文汉字（按 Unicode CJK 统一汉字计数，不计 LaTeX 命令、拉丁字符和标点），低于200字上限。摘要保留以下信息：

1. K-Waay 原协议已有不同参与方条件；
2. 采用两槽 Tamarin 模型进行受控比较；
3. 放宽配置可重复接受同一精确发送来源；
4. 消息级配置的消息区分与作用域内发生注入性成立，但同一参与方见证仍可达；
5. 参与方级配置作为正控制保持参与方区分，且有效批次可达，排除真空成立；
6. 结论仅适用于两槽批处理接纳抽象。

摘要已删除 `different-party condition` 和 `positive control` 英文括注。两组术语分别在引言正文首次出现时写为“不同参与方条件（different-party condition）”和“正控制（positive control）”。

## 3. 引言术语修订

- 删除以“精确来源不重复”概括 injectivity 的表述，改为“消息区分、作用域内发生注入性与参与方区分描述的是不同坐标和量词关系”。
- 将放宽配置的结果改为“一个精确发送来源可支持同一批次中的两个 `ReceiverAccept` 事件”，不再写成来源“产生”接收事件。

## 4. 引用定位中文化

正文中的 `\cite[...]{...}` 已全部消除，并改为自然中文定位加普通引用：

- “完整规范第5.1节（第21页）……`\cite{collins2024kwaayfull}`”；
- “原文第4.1节说明……`\cite{collins2024kwaayfull}`”。

全目录正文中 `\cite[` 的剩余数量为0。

## 5. 验证性质表修订

- “核心验证性质的迹语义”由无编号标题改为正常 `\caption{...}`，当前排版编号为表3；后续表格按 LaTeX 编号自然顺延。
- “消息级配置要求”改为“该性质断言”。
- “参与方级配置要求”改为“该性质要求”。
- 第2.3节正文改为通过 `\ref{tab:verification-property-semantics}` 引用该表。

## 6. 其他语言修订

“发送发生活跃于其他批次时仍保持全局唯一”已改为“发送发生在其他批次或其他执行中保持全局唯一”，消除不自然搭配，同时保留原有作用域边界。

## 7. 编译与质量检查

执行命令：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

结果：

- XeLaTeX 编译成功，生成 `main.pdf`；
- PDF 为 A4，共5页；
- undefined references：0；
- undefined citations：0；
- overfull box：0；
- missing character：0；
- 有一处非阻塞的 `Underfull \hbox (badness 1158)`，未造成可见越界或重叠；
- 逐页渲染检查未发现裁切、遮挡、表格越界或不可读内容。

## 8. 最终状态

**AROCMAG_PHASE1_FINAL_PATCH_READY**
