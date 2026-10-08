# 投稿前最终科学论证修订报告

## 1. 基线与范围

- 任务：投稿前最终科学论证修订
- 工作区基线：`dba2e821400d4b842da497861df040a490b6b3e8`
- 依据：`submissions/arocmag/final-scientific-audit/`中的最终审计、性质依赖审计和最小修订方案
- 修改类型：论证层级与措辞修复；未改变研究问题、章节结构、模型、lemma、机器结果或实验范围

## 2. 修改文件

1. `sections/00-abstract.tex`
2. `sections/01-introduction.tex`
3. `sections/03-formal-modeling.tex`
4. `sections/04-formal-analysis.tex`
5. `sections/05-discussion.tex`
6. `sections/06-conclusion.tex`（执行可选P2-2的最小收束）
7. `main.pdf`（由当前源码重新生成）
8. 本报告

## 3. 五项P1状态

### P1-1 DONE

第2.3节以$P_\tau$、$M_\tau$和$I_\tau$分别表示一条迹中的批内参与方互异性、批内消息互异性和批内来源单射性，并显式给出

\[
P_\tau\Rightarrow M_\tau,\qquad M_\tau\Leftrightarrow I_\tau.
\]

正文明确说明：该关系依赖当前模型的新鲜消息生成和完整元组精确来源匹配规则，是人工迹语义推导，不是新增Tamarin lemma或证明器运行，也不能推广到允许消息复用、使用其他来源关系的模型或任意协议。

### P1-2 DONE

第4.1节将两类证据分开：既有机器见证`same_party_different_messages_batch_exists`直接支持$M_\tau\nRightarrow P_\tau$；$P_\tau\Rightarrow M_\tau\Leftrightarrow I_\tau$来自人工规则语义分析。正文没有把后者写成机器证明。

### P1-3 DONE

第3.2节把非替代性的决定性证据归于`same_party_different_messages_batch_exists`。正文明确给出完整执行链：同一参与方的两个不同发送实例和新鲜消息各有合法匹配Send来源，进入同一批次生命周期，通过消息级准入，并在共同$(\mathit{bid},\mathit{rst})$中产生两个接受事件。`accepted_batch_has_distinct_messages`和`receiver_accept_injective`的结果继续保留，但不再作为两项独立累积证据。

### P1-4 DONE

引言贡献第3项改为机器验证的完整可达见证，并保留参与方互异模型的目标性质验证和`distinct_party_batch_exists`所支持的有效批次可达性。贡献仍定位为受控语义比较与可达性见证，没有扩展为通用形式化方法、完整K-Waay漏洞或部署攻击。

### P1-5 DONE

中英文摘要同步说明：消息互异性和批内来源单射性均验证通过，但在当前fresh-message/exact-origin规则下逻辑相关；决定性机器证据是同一参与方、不同发送实例、不同消息、各自合法来源、同一批次和两个接受事件组成的完整可达执行；消息级约束不能推出参与方互异性；参与方互异模型保持目标关系并保留有效批次。中文摘要为197个中文汉字，结论仍限定于固定两槽抽象。

## 4. 可选P2状态

- P2-1：既有第1章问题建模和第4.2节已明确$A$是抽象协议主体，不自动等同于账户、公钥编码、设备、预密钥记录或数据库记录，也未证明实现对象到$A$的映射，故无需重复扩写。
- P2-2：结束语改为由同参与方异消息的完整机器见证支撑非替代性结论，并明确M/I在当前规则下存在模型内逻辑依赖。

## 5. 科学结果守恒

- 三个Tamarin模型的SHA-256与修改前一致。
- `result-comparison.tsv`及三张验证/配置表的SHA-256与修改前一致。
- 图1和图2的TikZ源码SHA-256与修改前一致。
- 14项结果仍为13项verified、1项falsified；所有状态与证明步数未改变。
- 本轮未运行Tamarin，未增加实验、lemma或科学主张。
- `ReceiverAccept`仍是模型观察事件，不是现实会话建立或密钥安装。
- 结论仍限于固定两槽符号批次准入抽象；无完整协议漏洞、部署攻击、密钥泄露、认证失效或任意批长结论。

## 6. 编译与版面检查

- 构建命令：`latexmk -C`，随后`latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`
- 构建结果：成功
- PDF：11页A4
- undefined references：0
- undefined citations：0
- LaTeX errors：0
- missing glyphs：0
- overfull boxes：0
- underfull boxes：2（既有非阻断性提示）
- PDF SHA-256：`3F4209E1DEC6C2F7980C6A8930F143A02400468EB086E1ABEA7740B216F89A58`

实际渲染检查了第1、2、5、6、7、8、9、10页，覆盖中英文摘要、贡献列表、P/M/I关系式、消息互异模型结果、综合结果、讨论和结束语。未发现文字裁切、重叠、公式越界、表格越界或异常分页。

编辑器内置编译器未能在当前主机初始化平台标准目录，返回`Unable to find standard directories for platform`，未进入LaTeX源码编译。完整多文件构建和上述QA均由本机`latexmk`成功完成。

## 7. Remaining risks

未发现新的科学论证问题。剩余事项属于投稿格式最终化：官方模板/版面适配、匿名信息核对和参考文献格式检查。论文仍受已披露的两槽抽象、fresh-message、exact-origin matching、无精化定理和无部署证据边界约束。

最终状态：`READY_FOR_SUBMISSION_FORMAT_FINALIZATION`
