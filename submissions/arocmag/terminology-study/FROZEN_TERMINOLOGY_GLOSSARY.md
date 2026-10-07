# 冻结术语表 v1

状态：**AROCMAG_TERMINOLOGY_FREEZE_READY**。冻结日期：2026-10-07。权威范围：后续中文稿的术语选择；本轮没有应用到正文。此表优先于旧语言QA中“统一使用发送发生/正控制”的要求，但不改动历史报告。

冻结表示本文用语已作明确决策，不表示所有词都有行业标准。证据矩阵中的NO_STABLE_CONSENSUS一并有效。摘要采用中文短名；英文括注放正文首次定义处。数学符号、事件名、lemma键、引用键、标签和结果状态均不改；首次出现格式是定义模板，后续重写应融入句子，不能把全部英文别名塞进一处。

| 英文术语 | 最终中文术语 | 首次出现格式 | 后续简称 | 允许替代 | 禁止表达 | 语境说明 |
| --- | --- | --- | --- | --- | --- | --- |
| T01 party; protocol principal | 参与方 | 参与方（party） | 参与方 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | A是建模主体，不自动等同于账户、公钥字节串或预密钥 |
| T02 party identity | 参与方标识 | 参与方标识（party identity） | 参与方标识 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 指条目中A分量；不得据此主张身份认证；NO_STABLE_CONSENSUS：本文工作命名 |
| T03 party projection | 参与方投影 | 参与方投影（party projection） | 参与方投影 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 保留数学投影party(E)，即从条目取出A；不用身份认证；NO_STABLE_CONSENSUS：本文工作命名 |
| T04 message identity; message coordinate | 消息标识维度；元组中称消息分量 | 消息标识维度（message identity），在条目元组中由消息分量m表示 | 消息分量 | 比较不同对象时说消息维度 | 消息ID字段（模型未定义）；参与方身份 | m为模型中的符号消息；不是实现中的message ID字段；NO_STABLE_CONSENSUS：本文工作命名 |
| T05 sender occurrence | 发送实例 | 发送实例（sender occurrence），指模型中一次SendMessage规则实例化所对应的发送 | 发送实例 | 某次发送；涉及事件时写发送事件 | 发送发生；发送会话；真实session ID | 一次SendMessage规则实例化产生的发送实例，不是完整协议会话；NO_STABLE_CONSENSUS：本文工作命名 |
| T06 sender occurrence coordinate; sid; oid | 发送实例标识 | 发送实例标识（sender occurrence coordinate） | 发送实例标识 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | oid对应模型sid；与事件时间点s分开，禁止完整会话标识；NO_STABLE_CONSENSUS：本文工作命名 |
| T07 sender-origin tuple | 发送来源元组 | 发送来源元组（sender-origin tuple） | 发送来源元组 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 完整(A,oid,m)，不是仅A，也不是网络编码；NO_STABLE_CONSENSUS：本文工作命名 |
| T08 exact sender origin | 精确发送来源 | 精确发送来源（exact sender origin） | 精确发送来源 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 首次解释为与完整(A,oid,m)匹配的发送来源；禁止真实来源认证；NO_STABLE_CONSENSUS：本文工作命名 |
| T09 identity coordinate; comparison dimension | 标识维度 | 标识维度（identity coordinate），用于区分参与方、发送实例、消息、槽位及批次上下文的比较维度 | 标识维度 | 数学公式逐项解释时用分量；参与方投影保留 | 身份属性（统称所有分量）；几何坐标 | 用于比较A、oid、m、槽位和上下文；不是几何坐标或均为人的身份属性；NO_STABLE_CONSENSUS：本文工作命名 |
| T10 tuple component | 元组分量 | 元组分量（tuple component） | 元组分量 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 解释E=(A,oid,m)时用分量；槽位和上下文不擅自加入该三元组 |
| T11 batch | 批次 | 批次（batch） | 批次 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 一组有序候选条目；处理过程才称批处理；NO_STABLE_CONSENSUS：本文工作命名 |
| T12 batch admission | 批次准入 | 批次准入（batch admission） | 批次准入 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 本文分析边界，非K-Waay原协议算法名；不等于接受事件；NO_STABLE_CONSENSUS：本文工作命名 |
| T13 batch composition | 批次组合 | 批次组合（batch composition） | 批次组合 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 选择、排列、重复已有候选条目，非密码组件的可组合安全定理；NO_STABLE_CONSENSUS：本文工作命名 |
| T14 receiver context | 接收方上下文 | 接收方上下文（receiver context） | 接收方上下文 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | rst是模型标识，不是完整接收方临时密码状态；NO_STABLE_CONSENSUS：本文工作命名 |
| T15 batch context; same-batch scope | 批次上下文；同一批次上下文内 | 批次上下文；同一批次上下文内（batch context） | 批次上下文；同一批次上下文内 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 性质中的共同上下文为同一(bid,rst)，简称批内须先定义；NO_STABLE_CONSENSUS：本文工作命名 |
| T16 slot; position | 槽位 | 槽位（slot） | 槽位 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 批次内位置，两个槽位不推出两消息或两参与方不同；NO_STABLE_CONSENSUS：本文工作命名 |
| T17 entry; candidate tuple | 条目；候选条目 | 条目；候选条目（entry） | 条目；候选条目 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 候选条目、准入条目、已产生接受事件的条目不可混同；NO_STABLE_CONSENSUS：本文工作命名 |
| T18 trace; execution trace | 执行轨迹；理论定义后可简称迹 | 执行轨迹（trace），即由模型执行产生的动作事实序列；理论段下文简称迹 | 理论：迹；运行叙述：执行轨迹 | 具体运行；事件序列（仅描述所展示片段） | 将符号轨迹称真实抓包记录 | 运行叙述用执行轨迹；不把符号轨迹称真实网络日志 |
| T19 trace semantics | 迹语义 | 迹语义（trace semantics） | 迹语义 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 保留专业表达并定义本文动作事实序列的语义；不移植MSC半序定义 |
| T20 trace property | 迹性质 | 迹性质（trace property） | 迹性质 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 理论语境保留；正文也可说关于执行轨迹的性质 |
| T21 all-traces; all traces | 全称性质（all-traces） | 对所有执行轨迹量化的全称性质（all-traces） | 表格：全称性；正文：全称性质 | 理论连续论述：全迹性质 | 所有真实协议执行均安全 | 表中简称全称性；对模型所有执行轨迹量化，不是无限协议能力保证 |
| T22 exists-trace | 存在性性质（exists-trace） | 存在满足指定公式的执行轨迹，即存在性性质（exists-trace） | 表格：存在性；正文：存在性性质 | 本文有目标事件时称可达性性质 | 存在迹（作为无解释表项）；把验证通过写成所有执行成立 | 表中简称存在性；本文相关性质可解释为某类执行可达，但不是所有exists-trace都叫可达性 |
| T23 witness | 按语境：见证值／满足性质的执行轨迹 | 按对象给出：存在量词的见证值，或满足指定存在性性质的执行轨迹 | 按语境决定 | 见CONTEXT_SENSITIVE_TERMS.md | 机器见证（无所指）；同一参与方见证 | 不得把所有witness一律改成反例或攻击；NO_STABLE_CONSENSUS：本文工作命名 |
| T24 witness value | 见证值 | 见证值（witness value） | 见证值 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 逻辑存在量词的取值；复合中文用法未在本次中文样本建立共识 |
| T25 witness execution; witness trace | 满足存在性性质的执行轨迹 | 满足存在性性质的执行轨迹（witness execution） | 满足存在性性质的执行轨迹 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 简写可达执行或该执行轨迹；需标明满足哪项性质；NO_STABLE_CONSENSUS：本文工作命名 |
| T26 same-party/different-message witness | 同一参与方不同消息批次的可达执行 | 同一参与方不同消息批次的可达执行（same-party/different-message witness） | 同一参与方不同消息批次的可达执行 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 同一A，不同oid和m，两个匹配Send及两个同上下文接受；NO_STABLE_CONSENSUS：本文工作命名 |
| T27 counterexample; counterexample trace | 反例；反例轨迹 | 反例；反例轨迹（counterexample） | 反例；反例轨迹 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 反驳指定全称性质的执行；不是完整K-Waay攻击 |
| T28 attack trace | 攻击轨迹（仅已建立攻击语义时） | 攻击轨迹（仅已建立攻击语义时）（attack trace） | 攻击轨迹（仅已建立攻击语义时） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 当前两槽结果称反例轨迹或可达执行，不升级为部署攻击 |
| T29 reachability | 可达性 | 可达性（reachability） | 可达性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 存在所需事件及次序的执行，不是所有输入都能到达 |
| T30 correspondence | 对应关系；性质名称用对应性 | 对应关系；性质名称用对应性（correspondence） | 对应关系；性质名称用对应性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 匹配字段、方向、时间及量词均须定义；不默认是认证 |
| T31 origin correspondence | 精确发送来源对应性 | 精确发送来源对应性（origin correspondence）：每个接受事件都有先前的完整元组匹配Send | 来源对应性 | 发送来源对应性；精确来源对应关系 | 来源认证；源真实性；身份认证 | ReceiverAccept蕴含先前完整元组匹配Send；不等于源真实性；NO_STABLE_CONSENSUS：本文工作命名 |
| T32 injectivity | 单射性（抽象数学语境） | 单射性（抽象数学语境）（injectivity） | 单射性（抽象数学语境） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 具体性质按下列完整名；文献回顾Lowe概念用单射一致性 |
| T33 occurrence injectivity; scoped occurrence injectivity | 批次上下文内的发送—接受单射对应性 | 批次上下文内的发送—接受单射对应性（scoped occurrence injectivity），按本文同一(bid,rst)的条件唯一性公式定义 | 批内单射对应性 | 在已明确上下文的连续论述中用单射对应性 | 单射一致性；全局单射性；双射；一一交付 | 简称批内单射对应性；同一(bid,rst)下给定先前精确Send最多对应一次接受；NO_STABLE_CONSENSUS：本文工作命名 |
| T34 injective agreement | 单射一致性 | 单射一致性（injective agreement） | 单射一致性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 只用于Lowe认证概念；不能命名本文receiver_accept_injective |
| T35 distinct-party condition; different-party condition | 批内参与方互异条件 | 批内参与方互异条件（distinct-party condition） | 批内参与方互异条件 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 原协议已有条件；本文命名而非原文正式算法；限定同次调用；NO_STABLE_CONSENSUS：本文工作命名 |
| T36 party distinction | 批内参与方互异性 | 批内参与方互异性（party distinction） | 批内参与方互异性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 同一(bid,rst)不同接受事件具有不同A，不是身份认证或全局唯一；NO_STABLE_CONSENSUS：本文工作命名 |
| T37 message distinction | 批内消息互异性 | 批内消息互异性（message distinction） | 批内消息互异性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 不同接受事件的m不等；不是密码学可区分性或机密性；NO_STABLE_CONSENSUS：本文工作命名 |
| T38 positive control | 目标对照 | 直接施加目标约束的对照模型（positive control），下文称目标对照 | 目标对照 | 目标对照模型；直接施加参与方互异约束的对照模型 | 正控制；修复方案；安全加固协议 | 首次用直接施加目标约束的对照模型（positive control）；非修复方案；NO_STABLE_CONSENSUS：本文工作命名 |
| T39 relaxed admission | 无互异约束的批次准入模型 | 无互异约束的批次准入模型（relaxed admission） | 无互异约束模型 | 无互异约束配置；表内无互异约束 | 无约束模型；原始K-Waay模型 | 仅不施加消息/参与方互异约束，仍有来源和顺序约束；禁无约束模型；NO_STABLE_CONSENSUS：本文工作命名 |
| T40 message-level restriction; message-level configuration | 消息互异约束的批次准入模型 | 消息互异约束的批次准入模型（message-level restriction） | 消息互异约束模型 | 消息互异约束配置；表内消息互异约束 | 消息级安全协议；全面防重放模型 | 比较m1与m2；并非新协议或实现中的全部去重策略；NO_STABLE_CONSENSUS：本文工作命名 |
| T41 party-level admission; party-level configuration | 参与方互异约束的批次准入模型 | 参与方互异约束的批次准入模型（party-level admission） | 参与方互异约束模型 | 参与方互异约束配置；表内参与方互异约束 | 修复模型；新认证协议 | 比较A1与A2；用作目标对照，禁止修复协议；NO_STABLE_CONSENSUS：本文工作命名 |
| T42 controlled comparison | 受控比较 | 受控比较（controlled comparison） | 受控比较 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 相同生命周期下改变准入约束，非随机实验或三种真实实现；NO_STABLE_CONSENSUS：本文工作命名 |
| T43 fact | 事实 | 事实（fact） | 事实 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 模型符号对象，不表示经验证的真实世界事实 |
| T44 action fact | 动作事实 | 动作事实（action fact） | 动作事实 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 记录事件供性质使用，区分状态事实与动作标签 |
| T45 persistent fact | 持久事实 | 持久事实（persistent fact） | 持久事实 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 可被多次匹配，不是数据库持久化，也不自动产生多个Send事件 |
| T46 linear fact; state fact | 线性事实；状态事实 | 线性事实；状态事实（linear fact） | 线性事实；状态事实 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 线性事实使用时消耗；不要把槽位本身误称不可复用的消息 |
| T47 multiset rewriting | 多集重写 | 多集重写（multiset rewriting） | 多集重写 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 允许多重集重写/多重集合改写；同文优先多集重写 |
| T48 rule; rule-level semantics | 规则；规则语义 | 规则；规则语义（rule） | 规则；规则语义 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 约束执行构造方式，不等于已验证性质 |
| T49 restriction | 限制条件（restriction） | 限制条件（restriction）（restriction） | 限制条件（restriction） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 工具关键字限制允许的轨迹；与普通message-level restriction区别 |
| T50 guard; admission condition | 准入条件 | 准入条件（guard） | 准入条件 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | Neq动作联合restriction落实不等式，不能称独立布尔guard即全部实现；NO_STABLE_CONSENSUS：本文工作命名 |
| T51 lemma | 待验证性质（lemma） | 待验证性质（lemma）（lemma） | 待验证性质（lemma） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | lemma是声明类别，可能被否定；不统一称已证明引理 |
| T52 fresh name; fresh value | 新鲜值；新鲜标识 | 新鲜值；新鲜标识（fresh name） | 新鲜值；新鲜标识 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 符号新鲜性不等同现实随机数碰撞概率；sid与m分别生成 |
| T53 timepoint; event occurrence | 事件时间点；一次事件发生 | 事件时间点；一次事件发生（timepoint） | 事件时间点；一次事件发生 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | r1与r2表示事件位置，不是sid/oid；接受发生数改接受事件数 |
| T54 Send; send event | 发送事件（Send） | 发送事件（Send）（Send） | 发送事件（Send） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 模型动作不是完整原协议Send算法的全部语义；NO_STABLE_CONSENSUS：本文工作命名 |
| T55 ReceiverAccept; acceptance event | 接受事件（ReceiverAccept） | 接受事件（ReceiverAccept）（ReceiverAccept） | 接受事件（ReceiverAccept） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 不是In网络接收，不是完整会话接受，不是成功密钥建立；NO_STABLE_CONSENSUS：本文工作命名 |
| T56 BatchReceive action | 批次准入事件（模型中的BatchReceive） | 批次准入事件（模型中的BatchReceive）（BatchReceive action） | 批次准入事件（模型中的BatchReceive） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 必须与规范BatchReceive操作区分；准入不等于两槽均已接受；NO_STABLE_CONSENSUS：本文工作命名 |
| T57 rejection branch; rejection reachability | 拒绝分支可达性 | 拒绝分支可达性（rejection branch） | 拒绝分支可达性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 存在性不蕴含所有无效输入最终拒绝，且Send未绑定被拒元组；NO_STABLE_CONSENSUS：本文工作命名 |
| T58 non-vacuity; vacuous truth | 排除因无相关接受事件而成立的情形（non-vacuity） | 通过有效批次可达性，排除性质仅因没有相关接受事件而成立的情形（non-vacuity） | 结果叙述：有效批次可达性；解释：排除空真成立 | 空真成立须首次解释；理论讨论可保留non-vacuity | 非真空性（无解释）；非空性（未指明对象）；所有输入均可完成 | 中文短名NO_STABLE_CONSENSUS；结果处用有效批次可达性及明确解释；NO_STABLE_CONSENSUS：本文工作命名 |
| T59 refinement; refinement theorem | 精化；精化定理 | 精化；精化定理（refinement） | 精化；精化定理 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 当前未建立模型到完整协议/实现的精化定理；不把映射说明称精化证明 |
| T60 symbolic model; symbolic abstraction | 符号模型；符号抽象 | 符号模型；符号抽象（symbolic model） | 符号模型；符号抽象 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 固定两槽不等于整个模型仅两次会话，也不是任意批长定理 |
| T61 Dolev–Yao adversary; attacker | Dolev–Yao攻击者；攻击者 | Dolev–Yao攻击者；攻击者（Dolev–Yao adversary） | Dolev–Yao攻击者；攻击者 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 文献中的敌手可保留引用；模型实例能力以规则为准 |
| T62 replay; repeated acceptance | 重放；重复接受 | 重放；重复接受（replay） | 重放；重复接受 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 重复接受是抽象行为，重放候选元组不推出完整协议重放攻击 |
| T63 authentication; secrecy | 认证；保密性 | 认证；保密性（authentication） | 认证；保密性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 仅背景或边界说明；来源对应和消息互异不升级为这些性质 |
| T64 authenticated key exchange; deniable | 认证密钥交换；可否认性 | 认证密钥交换；可否认性（authenticated key exchange） | 认证密钥交换；可否认性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 原协议背景，不是本模型新增证明 |
| T65 KEM; split-KEM; prekey bundle | KEM；split-KEM；预密钥束 | KEM；split-KEM；预密钥束（KEM） | KEM；split-KEM；预密钥束 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 保留源协议术语；首次KEM可注密钥封装机制，split-KEM不强造拆分中文标准 |
| T66 transcript; session identifier; wire representation | 协议交互记录；会话标识；传输编码 | 协议交互记录；会话标识；传输编码（transcript） | 协议交互记录；会话标识；传输编码 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 说明oid不是完整协议交互记录或会话标识；勿把抽象元组写成网络字段 |
| T67 non-implication; non-substitutability | 不蕴含；不能替代 | 不蕴含；不能替代（non-implication） | 不蕴含；不能替代 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 逻辑例子和机器可达执行分别给证据，不将常识例子充当机器结果；NO_STABLE_CONSENSUS：本文工作命名 |
| T68 verified; falsified; proof steps | 验证通过；被否定；证明步数 | 验证通过；被否定；证明步数（verified） | 验证通过；被否定；证明步数 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 全称falsified可称被反例否定；exists-trace的falsified不可照搬；steps不是运行时间 |
| T69 bounded abstraction; arbitrary batch sizes | 固定两槽抽象；任意批次长度 | 固定两槽抽象；任意批次长度（bounded abstraction） | 固定两槽抽象；任意批次长度 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 两槽界限是每批槽数；批次/发送实例总数未被固定为2；NO_STABLE_CONSENSUS：本文工作命名 |
| T70 matching origin; idealized origin relation | 精确发送来源匹配；抽象来源关系 | 精确发送来源匹配；抽象来源关系（matching origin） | 精确发送来源匹配；抽象来源关系 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | !Sent是持久事实的建模假设，不是实现的密码学认证机制；NO_STABLE_CONSENSUS：本文工作命名 |
| T71 sequential processing; common lifecycle | 顺序处理；共同生命周期 | 顺序处理；共同生命周期（sequential processing） | 顺序处理；共同生命周期 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 三模型共同处理过程，不推断现实网络时序完全相同；NO_STABLE_CONSENSUS：本文工作命名 |
| T72 scope; global uniqueness | 作用域；全局唯一性 | 作用域；全局唯一性（scope） | 作用域；全局唯一性 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 批内性质不声称跨批唯一；但模型Fr确实令新生成sid/m在一条执行中新鲜，不可否认这一规则事实 |
| T73 aliveness; liveness | Lowe存活性；活性（liveness） | Lowe存活性；活性（liveness）（aliveness） | Lowe存活性；活性（liveness） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 区分Lowe认证层级aliveness与最终发生的活性性质；拒绝存在性不证明后者 |
| T74 supporting property; key result | 支持性质；核心结果 | 支持性质；核心结果（supporting property） | 支持性质；核心结果 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 论文取舍标签，非工具安全等级；不可删去量词类型；NO_STABLE_CONSENSUS：本文工作命名 |
| T75 source-to-abstraction mapping | 协议来源与模型抽象的对应说明 | 协议来源与模型抽象的对应说明（source-to-abstraction mapping） | 协议来源与模型抽象的对应说明 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 说明性映射不等于精化证明，不能把缺失机制当已实现；NO_STABLE_CONSENSUS：本文工作命名 |
| T76 composition boundary; cryptographic component | 组合边界；密码组件 | 组合边界；密码组件（composition boundary） | 组合边界；密码组件 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 批内关系区别于组件安全，不主张新的通用组合定理；NO_STABLE_CONSENSUS：本文工作命名 |
| T77 receiver ephemeral state | 接收方临时状态 | 接收方临时状态（receiver ephemeral state） | 接收方临时状态 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 原协议状态与模型rst标识分开；不复制完整密码结构 |
| T78 unknown key-share; misbinding | 未知密钥共享（UKS）；错误绑定（misbinding） | 未知密钥共享（UKS）；错误绑定（misbinding）（unknown key-share） | 未知密钥共享（UKS）；错误绑定（misbinding） | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 本任务仅界限清单；不得把同A的两次接受命名为UKS或错误绑定攻击 |
| T79 implementation; deployment | 实现；部署 | 实现；部署（implementation） | 实现；部署 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 抽象模型结果不等同部署漏洞或客户端遗漏检查 |
| T80 reachability sanity check | 正常路径可达性检查 | 正常路径可达性检查（reachability sanity check） | 正常路径可达性检查 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 这里只要求准入及后续一次接受，不证明两个不同参与方完成；NO_STABLE_CONSENSUS：本文工作命名 |
| T81 one-send/two-accepts witness | 一个精确发送来源对应两个同批接受事件的可达执行 | 一个精确发送来源对应两个同批接受事件的可达执行（one-send/two-accepts witness） | 一个精确发送来源对应两个同批接受事件的可达执行 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 唯一匹配Send仅限完整元组；不排除无关发送事件；NO_STABLE_CONSENSUS：本文工作命名 |
| T82 valid distinct-party batch | 有效的不同参与方批次 | 有效的不同参与方批次（valid distinct-party batch） | 有效的不同参与方批次 | 在已定义语境中按含义自然转述，不新增安全主张 | 任何超出右列定义的替换 | 两匹配Send和两个接受均存在；有效仅在本抽象中解释；NO_STABLE_CONSENSUS：本文工作命名 |

## 优先执行规则

1. 注入性统一按数学用语改为单射性，但Lowe的injective agreement单独叫单射一致性。
2. “批内”在性质段先定义为同一(bid,rst)；不能省略接收方上下文而加强结论。
3. 标识维度是分析视角，三元组分量是数学结构；槽位及上下文不增补进E的三元组。
4. 新鲜发送实例标识与事件时间点不同。Send事件、!Sent持久事实、In网络输入和ReceiverAccept接受事件严格区分。
5. 规则或restriction施加约束；lemma验证执行是否满足性质。表述不能互换。
6. 本表不授权全文重写、改变研究问题、增添模型机制或新增证明。
