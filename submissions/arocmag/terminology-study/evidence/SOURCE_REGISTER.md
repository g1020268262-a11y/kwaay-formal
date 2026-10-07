# 证据登记与适用范围

检索与核对日期：2026-10-07。本登记只服务术语研究，不向论文新增引用，也不替换原研究证据。页码均优先写 **PDF物理页码**，避免与刊物页码混淆。

## 本地目标期刊全文

原件位于 `submissions/arocmag/style-study/reference-pdfs/`。原件SHA-256见本目录 `protected-inputs.sha256.json`，文本抽取见 `local_pdf_text.json`。所有七篇均检查了与认证、模型、实例、执行和验证有关的段落；P4的文本编码不能可靠提取，改看原PDF第6、7页。不能以P4的检索零命中断言全文没有某词。

| 编号 | 正式论文及官网 | 本地文件 | 本轮直接支持的用语与定位 | 不能支持的推论 |
| --- | --- | --- | --- | --- |
| P1 | [基于Tamarin的MQTT协议安全性分析方法](https://www.arocmag.cn/abs/2023.02.0038) | `2023.02.0038-tamarin-mqtt.pdf` | PDF第3页认证属性列举“存活性、弱一致性、非单射一致性和单射一致性”；第4页使用反例、攻击路径；第1页有安全属性引理 | 单射一致性属于认证层级，不能移用于任意带injective名称的性质 |
| P2 | [基于安全协议代码的形式化辅助建模研究](https://www.arocmag.cn/abs/2022.08.0446) | `2022.08.0446-assisted-formal-modeling.pdf` | PDF第2页§1.2有“多重集合改写规则”，前提/动作/结论及facts；第3、5页有参与方、in/out事实；第4页以一条路径对应一次完整运行 | 支持工具词和规则结构，不证明“发送发生”“作用域内发生注入性”等复合词是惯例 |
| P3 | [可证明安全的后量子两方口令认证密钥协商协议](https://www.arocmag.cn/abs/2022.07.0377) | `2022.07.0377-post-quantum-paka.pdf` | PDF第3页使用参与者的实例，并列出pid、sid等状态参数 | 该文的会话sid不能移植到本文发送规则生成的sid |
| P4 | [无线传感器网络中基于PUF的轻量级多网关身份认证协议](https://www.arocmag.cn/abs/2024.06.0249) | `2024.06.0249-puf-multi-gateway.pdf` | PDF第6页（刊页1235）§4.2用ProVerif、Dolev–Yao模型、双向认证、形式化安全验证；图5显示inj-event查询；§4.3及第7页用攻击者、重放攻击、身份认证 | 不能把其双向认证或会话密钥安全结论用于本文；图中inj-event也不自动给出中文“单射对应性”的稳定译名 |
| P5 | [多网关无线医疗传感器网络中基于PUF的轻量级匿名认证协议](https://www.arocmag.cn/abs/2024.12.0536) | `2024.12.0536-puf-medical-multi-gateway.pdf` | PDF第4页模型要素使用实体实例、参与方，第5页使用执行查询 | 只支持实例和参与方等基础词，不支持将发送实例解释为完整协议会话 |
| P6 | [安全增强的智能电网轻量级匿名认证方案](https://www.arocmag.cn/abs/2022.03.0118) | `2022.03.0118-smart-grid-auth.pdf` | PDF第4页使用会话实例，第5页ProVerif段用可达性、认证性、观测等效性 | 可达性、认证、等效性是不同性质；本文没有后两类完整保证 |
| P7 | [一种基于格的轻量级多因素认证密钥交换协议](https://www.arocmag.cn/abs/2025.08.0441) | `2025.08.0441-lattice-mfa-ake.pdf` | PDF第3页符号表有用户实例、服务器实例，第4页ROR模型有参与方及并发实例 | 不能把ROR计算安全证明套用于本文符号模型 |

P1、P2作为工具与认证术语的主证据；P3—P7用于比较普通协议用语。七篇是定向样本，不能据此报告全刊词频、全领域“最常用”译法或不存在某用语。

已有 `REFERENCE_PAPER_MATRIX.md`、`FORMAL_ANALYSIS_PATTERN.md`、`FORMULA_STYLE_ANALYSIS.md`、`RESULT_NARRATIVE_ANALYSIS.md`用于定位章节；它们是项目研究笔记，不计为独立文献证据。旧蓝图或QA中已采用某译法也不是外部共识。

## 额外正式中文来源

| 编号 | 来源 | 实际取得层次与定位 | 用于本审计的有限结论 |
| --- | --- | --- | --- |
| S1 | 贾凡等，[5G网络认证及密钥协商协议的安全性分析](https://jst.tsinghuajournals.com/article/2021/4302/20211107.htm)，清华大学学报（自然科学版），2021，61(11):1260–1266 | 官方全文HTML；§2.1.1及表3 | 单射一致性是Lowe认证概念，涉及参与角色、运行及一致数据；与P1交叉确认。页面英文摘要的single shot consistency不作为规范英文译名，英文概念以Tamarin手册为准 |
| S2 | [软件学报2005，16(6)，起始页1182的MSC形式语义论文](https://jos.org.cn/1000-9825/16/1182.pdf) | 官方PDF可检索片段，刊页1184 §1.2直接出现“半序语义(或迹语义)”；重开全文失败，未补造题名/作者 | 足以证实“迹语义”是中文形式方法专业表达；不足以确定它在Tamarin中文文献中比“执行轨迹”常用，更不能把MSC半序语义当作Tamarin定义 |
| S3 | [基于Event-B方法的安全协议设计、建模与验证](https://www.jos.org.cn/html/2018/11/5622.htm)，软件学报，2018 | 官方搜索摘要直接使用“安全协议模型之间的精化关系”；全文获取失败，标记为摘要层证据 | 支持“精化”基础词；未将该文未读的公式或结论列为证据，“精化定理”在本文仅用于说明尚未建立的边界 |
| A1 | [基于延迟敏感任务动态准入与时延评估的边云协同调度策略](https://www.arocmag.cn/abs/2025.12.0494)，计算机应用研究 | 官方题名、摘要与关键词页面，使用动态准入/准入控制 | 支持目标刊物中的admission相关基础用语“准入”，不证明batch admission已有固定译名 |
| A2 | [在无线/移动网络中基于赏罚模型的自适应准入控制](https://jcst.ict.ac.cn/cn/article/id/1387)，计算机科学技术学报，2007，22(4):527–531 | 官方中英文题名与摘要页面，对应admission control | 与A1交叉确认“准入控制”基础用语，不将连接/呼叫准入的技术机制移植到本文 |

## 官方工具语义来源

| 编号 | 文档 | 使用内容 |
| --- | --- | --- |
| T1 | [Tamarin手册：Protocol Specification using Rules](https://tamarin-prover.com/manual/master/book/005_protocol-specification-rules.html) | 多集重写、规则、动作事实、线性与持久事实、新鲜值的英文定义 |
| T2 | [Tamarin手册：Property Specification](https://tamarin-prover.com/manual/master/book/007_property-specification.html) | 迹公式、all-traces、exists-trace、restriction及Lowe认证示例；与模型声明对照 |
| T3 | [Tamarin手册：Modeling Issues，Exist-Trace Lemmas](https://tamarin-prover.com/manual/master/book/010_modeling-issues.html) | 相关动作不可达时全称蕴涵可能空真；存在性检查用于排除此类退化模型。用于解释non-vacuity，不声称中文固定译名 |

手册是动态master版本，本次访问日期已记录；模型实际结果仍以项目既有版本记录为准。这里没有重新运行Tamarin，也没有据新版手册改变已有结果。

## 项目英文与模型语义来源

| 编号 | 路径/内容 |
| --- | --- |
| E1 | `manuscript/sections/01-introduction.tex` |
| E2 | `manuscript/sections/02-batchreceive-identity-problem.tex` |
| E3 | `manuscript/sections/03-security-objective-threat-model.tex` |
| E4 | `manuscript/sections/04-formal-modeling.tex`及`manuscript/tables/model-comparison.tex` |
| E5 | `manuscript/sections/05-formal-analysis.tex`及`manuscript/tables/verification-results.tex` |
| E6 | `manuscript/sections/06-discussion.tex`；相关工作与结论亦纳入扫描 |
| M | `tamarin/rq-v2-minimal/rqv2_relaxed.spthy`、`rqv2_message_dedup.spthy`、`rqv2_party_admission.spthy`全部规则、restriction与lemma |

M中的注释写session coordinate，但实际`SendMessage`每次独立生成`Fr(~sid)`和`Fr(~m)`，正文已说明不是完整session ID。因此翻译以可执行规则及明确边界为准，不机械采用注释里的session。

## 检索记录与未形成共识的范围

检索围绕中文正式期刊域名及工具官网，包括“单射一致性 Tamarin”“迹语义 MSC”“安全协议 执行迹/执行轨迹”“安全协议 精化”“准入控制 admission”“正控制/正对照 形式化验证”“空真 形式化验证”。前述P1—P7同时全文检索指定术语及候选词。搜索出现博客、论坛、机器翻译网站、营销页和无关领域结果时均排除。

没有建立稳定中文对应的完整词组包括：sender occurrence、identity coordinate、scoped occurrence injectivity、batch admission、positive control、本文三模型名称、party/message distinction及各类具体witness复合表达。统一标记 **NO_STABLE_CONSENSUS**，以项目语义和已有基础词形成可解释的工作命名。non-vacuity不硬造四字名词，采用解释性句子。

S2、S3的访问限制降低的是词频/全文解释证据，未用它们推导本文性质。最终名称的语义可由M、E及官方工具定义完整核对，因此不构成必须由作者补证才可冻结的阻塞项。
