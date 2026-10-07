# AROCMAG 正文冻结报告

## 基线与范围

- 任务名称：`AROCMAG_FINAL_3_MICRO_FIXES_AND_TEXT_FREEZE`
- 提交基线：`d4500127a9ea51402b85d8a4416ec05fb975062e`
- 修改范围：仅三类指定科学措辞及其必要的中英文同步位置
- 未修改：标题、章节结构、研究问题数量、Tamarin 模型、lemma 公式、验证状态、术语体系和研究内容
- 未生成图或 Word 稿；未执行 commit 或 push

## 三处修改前后

### 1. 第 3.2 节性质指代

修改前：

> 该模型中的发送来源对应性和批内来源单射性也都验证通过。由此，无互异约束模型中一个匹配发送来源对应同批两个接受事件的形状被排除，同时每个接受仍有更早的完整元组匹配发送。前一项性质比较不同接受事件的消息分量，后一项性质限制一个来源对应的接受事件数，两者不能合并为参与方关系。

修改后：

> 该模型中的发送来源对应性和批内来源单射性也均验证通过。发送来源对应性说明每个接受事件都有更早的完整元组匹配发送，批内来源单射性则排除一个匹配发送来源在同一批次和接收方上下文中对应两个不同接受事件。结合上一段已经验证的批内消息互异性，三项性质分别约束消息分量、接受事件的匹配发送存在性以及同一来源对应接受事件的数量，但均不直接比较两个条目的参与方分量。

原文的“前一项性质”在语法上指向发送来源对应性，却把它解释为消息分量比较，因而发生性质指代错位。修订后明确区分：批内消息互异性比较消息分量 $m$；发送来源对应性要求每个接受事件存在更早的完整元组匹配发送；批内来源单射性限制同一匹配来源不能在同一批次和接收方上下文中对应两个不同接受事件。三项性质没有被合并或提升为更强认证性质。

### 2. 中英文摘要研究问题措辞

中文修改前：

> 但消息或发送实例层面的限制能否维持这一批内关系仍需明确。

中文修改后：

> 但批内消息互异性以及发送来源与接受事件之间的单射关系能否替代这一批内参与方关系仍需明确。

英文修改前：

> It remains necessary to determine whether constraints on messages or sender occurrences can preserve this same-batch relation.

英文修改后：

> It remains necessary to determine whether message distinction and an injective correspondence between sender origins and acceptance events can substitute for this same-batch party relation.

修订后的中英文摘要均把消息互异性表述为准入模型约束，把发送来源与接受事件之间的单射关系表述为验证性质，不再暗示本文构造了独立的发送实例级准入模型。中英文研究问题和作用域保持同步。

### 3. 删除“非真空实现/真空成立”翻译腔

引言贡献第 3 项：

- 修改前：“并以目标对照验证该性质的非真空实现。”
- 修改后：“并通过目标对照确认批内参与方互异性成立，且有效的不同参与方批次仍然可达。”

第 3.3 节：

- 修改前：“目标性质不是通过拒绝全部批次而真空成立。”
- 修改后：“该结果同时说明有效的不同参与方批次能够完成后续处理，目标性质并非依赖拒绝全部批次而成立。”

关键结果表：

- 修改前：“排除真空成立”
- 修改后：“确认有效批次可达”

上述修改直接陈述机器证据：目标全称性质成立，同时 `distinct_party_batch_exists` 证明有效的不同参与方批次可达。修改没有改变该 lemma 的存在性语义，也没有把“实现”误解为工程实现。

## 科学主张与机器结果守恒

- 未改变任何科学主张、研究问题、结论边界或模型假设。
- 未修改任何 Tamarin 模型、lemma 公式、验证状态或证明步数。
- 无互异约束模型：3 verified，1 falsified。
- 消息互异约束模型：5 verified。
- 参与方互异约束模型：5 verified。
- 合计：13 verified，1 falsified。
- 7 项核心结果的表格行、性质类型和结果状态均未改变；仅将 `distinct_party_batch_exists` 的论证作用改为自然中文。

## 编译与版面检查

- 执行命令：`latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`
- 编译结果：成功。
- undefined references：0
- undefined citations：0
- missing glyphs：0
- overfull boxes：0
- 当前 PDF：9 页，A4。
- 视觉复核：检查受影响的第 1、2、6、7 页，未发现裁切、重叠、表格越界或异常分页。
- PDF SHA-256：`6127B852811F27647FBAE93A84499E48BD23D30BC72337D1F81790B7B4EF73E4`

## 冻结状态

**TEXT CONTENT FROZEN**

后续除图表插入、匿名信息、投稿格式、参考文献格式和明显排版错误外，不得再对正文进行大规模改写。

最终状态：`AROCMAG_TEXT_FROZEN_READY`
