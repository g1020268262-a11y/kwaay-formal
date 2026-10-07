# 全文术语应用报告

任务：`AROCMAG_FULL_MANUSCRIPT_PROSE_REWRITE`

## 1. 应用范围

术语归一化覆盖标题、中文与英文摘要、0--5章正文、四张表、PDF元数据和图稿计划说明。既有历史阶段报告保留其形成时的表述，用于记录过程，不作为当前正文术语来源。

## 2. 最终术语

| 概念 | 当前正文用语 | 首次定义或使用方式 |
|---|---|---|
| batch admission | 批次准入 | 作为分析边界，不等同于接受事件 |
| distinct-party condition | 批内参与方互异条件 | 引言首次附英文括注 |
| party distinction | 批内参与方互异性 | 表示同批不同接受事件的参与方投影互异 |
| message distinction | 批内消息互异性 | 表示同批不同接受事件的消息分量互异 |
| sender occurrence | 发送实例 | 一次`SendMessage`规则实例化所对应的发送 |
| sender occurrence coordinate | 发送实例标识 | 中文稿`oid`，对应模型`sid` |
| identity coordinate | 比较维度 | 元组中分别称参与方分量、发送实例标识、消息分量 |
| exact sender origin | 与完整`(A,oid,m)`元组匹配的发送来源 | 后文简称匹配发送来源 |
| origin correspondence | 发送来源对应性 | 每个`ReceiverAccept`存在更早的完整元组匹配`Send` |
| scoped occurrence injectivity | 批内来源单射性 | 同一批次和接收方上下文内，不同接受事件不能对应同一匹配来源 |
| positive control | 直接施加目标约束的对照模型 | 后文简称目标对照 |

批内来源单射性已明确区别于Lowe意义下的单射一致性。三种模型首次出现时使用完整名称，后文使用“无互异约束模型”“消息互异约束模型”“参与方互异约束模型”，表格按要求去掉“模型”二字。

## 3. trace与witness处理

- 理论语境使用“迹语义”“迹性质”；具体运行使用“执行轨迹”；违反全称性质时使用“反例轨迹”。
- exists-trace在正文写为“存在性性质”或“可达执行”，表格类型写“存在性”。
- all-traces在正文写为“全称性质”，表格类型写“全称性”。
- same-party/different-message witness写为“同一参与方不同消息批次的可达执行”；重复接受结果按语境写为“可达执行”或“反例轨迹”。

## 4. 模型名称与结果表

四张表均已同步：表1使用“比较维度与模型映射”，表2使用三种互异约束名称，表3使用发送来源对应性、批内来源单射性、批内消息互异性和批内参与方互异性，表4以“存在性/全称性”标记结果类型。

活动LaTeX源文件扫描未发现以下旧称：批处理接纳、批次接纳、不同参与方条件、参与方区分、消息区分、发送发生、精确发送来源、作用域内发生注入性、正控制、三种旧配置名、机器见证、同一参与方见证、存在迹、全迹。英文式可选参数引用`\\cite[...]`和本地复核目录同样为0处。

## 5. 标题同步

- 旧标题：`K-Waay批处理接纳中参与方区分条件的形式化分析`
- 新标题：`K-Waay批次准入中参与方互异条件的形式化分析`
- 修改理由：新标题与正文最终术语一致，直接指向研究对象和目标关系，同时不扩大为完整K-Waay安全性或漏洞分析。

英文题目同步为`Formal Analysis of the Distinct-Party Condition in K-Waay Batch Admission`，已在英文摘要区显示；PDF英文主题元数据使用相同表述。

结论：全文活动LaTeX源文件已应用最终术语体系。

**AROCMAG_FULL_MANUSCRIPT_PROSE_REWRITE_READY**
