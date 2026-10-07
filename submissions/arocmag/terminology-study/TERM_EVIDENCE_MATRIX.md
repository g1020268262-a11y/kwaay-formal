# 术语证据矩阵

日期：2026-10-07。来源编号、页码口径和证据摘录见 [SOURCE_REGISTER.md](evidence/SOURCE_REGISTER.md)。E与M是项目语义来源，绝不能充当外部中文惯用证据；Tamarin英文手册证明工具语义，不证明中文译名。来源2不足时如实记录，不凑两篇假共识。

**NO_STABLE_CONSENSUS** 表示本次限定样本与正式来源检索没有建立稳定中文对应，不表示全领域不存在该说法。本文仍可依据模型精确定义冻结工作用语。表中“基础词有用法”不等于完整复合译名有共识。中文证据不足的工具译名仍保留英文并列。

| English term | 当前中文 | 候选中文 | 来源1 | 来源2 | 目标期刊是否使用 | 形式化验证文献是否使用 | 语义风险 | 建议 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 party; protocol principal | 参与方；协议主体 | 参与方；协议主体 / 参与方 | P2 p5 | P3 p3；M | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | A是建模主体，不自动等同于账户、公钥字节串或预密钥 | 参与方 |
| T02 party identity | 参与方身份；参与方坐标 | 参与方身份；参与方坐标 / 参与方标识 | P3 p3（身份概念） | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 指条目中A分量；不得据此主张身份认证 | 参与方标识 |
| T03 party projection | 参与方投影；身份投影 | 参与方投影；身份投影 / 参与方投影 | E2 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 保留数学投影party(E)，即从条目取出A；不用身份认证 | 参与方投影 |
| T04 message identity; message coordinate | 消息坐标 | 消息坐标 / 消息标识维度；元组中称消息分量 | E2 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | m为模型中的符号消息；不是实现中的message ID字段 | 消息标识维度；元组中称消息分量 |
| T05 sender occurrence | 发送发生 | 发送发生 / 发送实例 | P3 p3、P6 p4（仅支持实例一词） | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 一次SendMessage规则实例化产生的发送实例，不是完整协议会话 | 发送实例 |
| T06 sender occurrence coordinate; sid; oid | 发送发生坐标；一次发送发生 | 发送发生坐标；一次发送发生 / 发送实例标识 | T1 Fresh Names | M SendMessage | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | oid对应模型sid；与事件时间点s分开，禁止完整会话标识 | 发送实例标识 |
| T07 sender-origin tuple | 发送来源元组；精确元组 | 发送来源元组；精确元组 / 发送来源元组 | E4 | M !Sent | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 完整(A,oid,m)，不是仅A，也不是网络编码 | 发送来源元组 |
| T08 exact sender origin | 精确发送来源；精确来源 | 精确发送来源；精确来源 / 精确发送来源 | E4 | M Send/!Sent | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 首次解释为与完整(A,oid,m)匹配的发送来源；禁止真实来源认证 | 精确发送来源 |
| T09 identity coordinate; comparison dimension | 身份坐标；坐标 | 身份坐标；坐标 / 标识维度 | E2 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 用于比较A、oid、m、槽位和上下文；不是几何坐标或均为人的身份属性 | 标识维度 |
| T10 tuple component | 分量；坐标 | 分量；坐标 / 元组分量 | E2 | M | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 解释E=(A,oid,m)时用分量；槽位和上下文不擅自加入该三元组 | 元组分量 |
| T11 batch | 批次；批处理 | 批次；批处理 / 批次 | E2 | M CreateBatch | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 一组有序候选条目；处理过程才称批处理 | 批次 |
| T12 batch admission | 批处理接纳；接纳 | 批处理接纳；接纳 / 批次准入 | A1 | A2（均仅支持准入）；E2/M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 本文分析边界，非K-Waay原协议算法名；不等于接受事件 | 批次准入 |
| T13 batch composition | 批组成；批次组合 | 批组成；批次组合 / 批次组合 | E3 | M CollectSlot1/2 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 选择、排列、重复已有候选条目，非密码组件的可组合安全定理 | 批次组合 |
| T14 receiver context | 接收方上下文；接收上下文 | 接收方上下文；接收上下文 / 接收方上下文 | E4 | M CreateBatch | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | rst是模型标识，不是完整接收方临时密码状态 | 接收方上下文 |
| T15 batch context; same-batch scope | 批次上下文；作用域 | 批次上下文；作用域 / 批次上下文；同一批次上下文内 | E4 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 性质中的共同上下文为同一(bid,rst)，简称批内须先定义 | 批次上下文；同一批次上下文内 |
| T16 slot; position | 槽位；位置 | 槽位；位置 / 槽位 | E2 | M CollectSlot1/2 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 批次内位置，两个槽位不推出两消息或两参与方不同 | 槽位 |
| T17 entry; candidate tuple | 条目；候选元组 | 条目；候选元组 / 条目；候选条目 | E2 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 候选条目、准入条目、已产生接受事件的条目不可混同 | 条目；候选条目 |
| T18 trace; execution trace | 迹；执行；执行轨迹；符号迹 | 迹；执行；执行轨迹；符号迹 / 执行轨迹；理论定义后可简称迹 | S2（迹语义） | T2 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 运行叙述用执行轨迹；不把符号轨迹称真实网络日志 | 执行轨迹；理论定义后可简称迹 |
| T19 trace semantics | 迹语义 | 迹语义 / 迹语义 | S2 §1.2 | T2 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 保留专业表达并定义本文动作事实序列的语义；不移植MSC半序定义 | 迹语义 |
| T20 trace property | 迹性质 | 迹性质 / 迹性质 | T2 | M lemma | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 理论语境保留；正文也可说关于执行轨迹的性质 | 迹性质 |
| T21 all-traces; all traces | 全迹；全迹性质；全迹验证 | 全迹；全迹性质；全迹验证 / 全称性质（all-traces） | T2 | M 默认lemma | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 表中简称全称性；对模型所有执行轨迹量化，不是无限协议能力保证 | 全称性质（all-traces） |
| T22 exists-trace | 存在迹；存在迹性质 | 存在迹；存在迹性质 / 存在性性质（exists-trace） | T2 | T3；M | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 表中简称存在性；本文相关性质可解释为某类执行可达，但不是所有exists-trace都叫可达性 | 存在性性质（exists-trace） |
| T23 witness | 见证；机器见证；存在性见证 | 见证；机器见证；存在性见证 / 按语境：见证值／满足性质的执行轨迹 | T2/T3（语义） | E5/M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 不得把所有witness一律改成反例或攻击 | 按语境：见证值／满足性质的执行轨迹 |
| T24 witness value | 见证值（正文未直接使用） | 见证值（正文未直接使用） / 见证值 | T2 量词 | M Ex | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 逻辑存在量词的取值；复合中文用法未在本次中文样本建立共识 | 见证值 |
| T25 witness execution; witness trace | 见证；机器见证 | 见证；机器见证 / 满足存在性性质的执行轨迹 | T2/T3 | M exists-trace | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 简写可达执行或该执行轨迹；需标明满足哪项性质 | 满足存在性性质的执行轨迹 |
| T26 same-party/different-message witness | 同一参与方见证；同参与方不同消息见证 | 同一参与方见证；同参与方不同消息见证 / 同一参与方不同消息批次的可达执行 | E5 | M same_party_different_messages_batch_exists | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 同一A，不同oid和m，两个匹配Send及两个同上下文接受 | 同一参与方不同消息批次的可达执行 |
| T27 counterexample; counterexample trace | 反例；反例轨迹 | 反例；反例轨迹 / 反例；反例轨迹 | P1 p4 | T2 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 反驳指定全称性质的执行；不是完整K-Waay攻击 | 反例；反例轨迹 |
| T28 attack trace | 攻击轨迹；完整协议攻击 | 攻击轨迹；完整协议攻击 / 攻击轨迹（仅已建立攻击语义时） | P1 p4（攻击路径） | S1 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 当前两槽结果称反例轨迹或可达执行，不升级为部署攻击 | 攻击轨迹（仅已建立攻击语义时） |
| T29 reachability | 可达性；可达执行 | 可达性；可达执行 / 可达性 | P6 p5 | T3 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 存在所需事件及次序的执行，不是所有输入都能到达 | 可达性 |
| T30 correspondence | 对应；对应关系 | 对应；对应关系 / 对应关系；性质名称用对应性 | T2 Authentication | S1 表3 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 匹配字段、方向、时间及量词均须定义；不默认是认证 | 对应关系；性质名称用对应性 |
| T31 origin correspondence | 精确来源对应；来源对应 | 精确来源对应；来源对应 / 精确发送来源对应性 | E4/E5 | M receiver_accept_has_send | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | ReceiverAccept蕴含先前完整元组匹配Send；不等于源真实性 | 精确发送来源对应性 |
| T32 injectivity | 注入性；认证注入性 | 注入性；认证注入性 / 单射性（抽象数学语境） | P1 p3 | S1 §2.1.1；T2 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 具体性质按下列完整名；文献回顾Lowe概念用单射一致性 | 单射性（抽象数学语境） |
| T33 occurrence injectivity; scoped occurrence injectivity | 作用域内发生注入性；发生注入性 | 作用域内发生注入性；发生注入性 / 批次上下文内的发送—接受单射对应性 | M receiver_accept_injective | T2（对照定义） | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 简称批内单射对应性；同一(bid,rst)下给定先前精确Send最多对应一次接受 | 批次上下文内的发送—接受单射对应性 |
| T34 injective agreement | 单射一致性（待审计术语） | 单射一致性（待审计术语） / 单射一致性 | P1 p3 | S1 §2.1.1/表3；T2 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 只用于Lowe认证概念；不能命名本文receiver_accept_injective | 单射一致性 |
| T35 distinct-party condition; different-party condition | 不同参与方条件 | 不同参与方条件 / 批内参与方互异条件 | E2 | M；P3（仅基础名词） | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 原协议已有条件；本文命名而非原文正式算法；限定同次调用 | 批内参与方互异条件 |
| T36 party distinction | 参与方区分 | 参与方区分 / 批内参与方互异性 | M accepted_batch_has_distinct_parties | E5 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 同一(bid,rst)不同接受事件具有不同A，不是身份认证或全局唯一 | 批内参与方互异性 |
| T37 message distinction | 消息区分 | 消息区分 / 批内消息互异性 | M accepted_batch_has_distinct_messages | E5 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 不同接受事件的m不等；不是密码学可区分性或机密性 | 批内消息互异性 |
| T38 positive control | 正控制 | 正控制 / 目标对照 | E2/E5 | M party_admission | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 首次用直接施加目标约束的对照模型（positive control）；非修复方案 | 目标对照 |
| T39 relaxed admission | 放宽配置；放宽 | 放宽配置；放宽 / 无互异约束的批次准入模型 | M rqv2_relaxed | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 仅不施加消息/参与方互异约束，仍有来源和顺序约束；禁无约束模型 | 无互异约束的批次准入模型 |
| T40 message-level restriction; message-level configuration | 消息级限制；消息级配置 | 消息级限制；消息级配置 / 消息互异约束的批次准入模型 | M rqv2_message_dedup | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 比较m1与m2；并非新协议或实现中的全部去重策略 | 消息互异约束的批次准入模型 |
| T41 party-level admission; party-level configuration | 参与方级配置；参与方级正控制 | 参与方级配置；参与方级正控制 / 参与方互异约束的批次准入模型 | M rqv2_party_admission | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 比较A1与A2；用作目标对照，禁止修复协议 | 参与方互异约束的批次准入模型 |
| T42 controlled comparison | 受控比较；受控配置 | 受控比较；受控配置 / 受控比较 | E4/E5 | M共同规则 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 相同生命周期下改变准入约束，非随机实验或三种真实实现 | 受控比较 |
| T43 fact | 事实；来源事实 | 事实；来源事实 / 事实 | P2 p2–3 | T1 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 模型符号对象，不表示经验证的真实世界事实 | 事实 |
| T44 action fact | 动作事实；动作 | 动作事实；动作 / 动作事实 | P2 p2（动作/action事实） | T1 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 记录事件供性质使用，区分状态事实与动作标签 | 动作事实 |
| T45 persistent fact | 持久事实；持久来源事实 | 持久事实；持久来源事实 / 持久事实 | T1 | M !Sent/!Party | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 可被多次匹配，不是数据库持久化，也不自动产生多个Send事件 | 持久事实 |
| T46 linear fact; state fact | 线性槽位；收集状态 | 线性槽位；收集状态 / 线性事实；状态事实 | T1 | M OpenSlot/AdmittedSlot | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 线性事实使用时消耗；不要把槽位本身误称不可复用的消息 | 线性事实；状态事实 |
| T47 multiset rewriting | 多集重写 | 多集重写 / 多集重写 | P2 p2（多重集合改写） | T1 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 允许多重集重写/多重集合改写；同文优先多集重写 | 多集重写 |
| T48 rule; rule-level semantics | 规则；规则层；规则语义 | 规则；规则层；规则语义 / 规则；规则语义 | P2 p2 | T1；M | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 约束执行构造方式，不等于已验证性质 | 规则；规则语义 |
| T49 restriction | 不等式约束；限制 | 不等式约束；限制 / 限制条件（restriction） | T2 Restrictions | M Inequality | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 工具关键字限制允许的轨迹；与普通message-level restriction区别 | 限制条件（restriction） |
| T50 guard; admission condition | 接纳条件；约束 | 接纳条件；约束 / 准入条件 | M Neq+Inequality | T2 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | Neq动作联合restriction落实不等式，不能称独立布尔guard即全部实现 | 准入条件 |
| T51 lemma | lemma；性质；引理 | lemma；性质；引理 / 待验证性质（lemma） | P1 p1 | P2 p2；T2 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | lemma是声明类别，可能被否定；不统一称已证明引理 | 待验证性质（lemma） |
| T52 fresh name; fresh value | 新鲜；新鲜坐标 | 新鲜；新鲜坐标 / 新鲜值；新鲜标识 | T1 Fresh Names | M Fr | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 符号新鲜性不等同现实随机数碰撞概率；sid与m分别生成 | 新鲜值；新鲜标识 |
| T53 timepoint; event occurrence | 时间条件；事件发生；接受发生数 | 时间条件；事件发生；接受发生数 / 事件时间点；一次事件发生 | T2 | M #s/#r | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | r1与r2表示事件位置，不是sid/oid；接受发生数改接受事件数 | 事件时间点；一次事件发生 |
| T54 Send; send event | Send动作；发送事件 | Send动作；发送事件 / 发送事件（Send） | M SendMessage | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 模型动作不是完整原协议Send算法的全部语义 | 发送事件（Send） |
| T55 ReceiverAccept; acceptance event | 接收事件；接受事件；ReceiverAccept | 接收事件；接受事件；ReceiverAccept / 接受事件（ReceiverAccept） | M ProcessSlot1/2 | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 不是In网络接收，不是完整会话接受，不是成功密钥建立 | 接受事件（ReceiverAccept） |
| T56 BatchReceive action | BatchReceive动作；批次接纳 | BatchReceive动作；批次接纳 / 批次准入事件（模型中的BatchReceive） | M admission规则 | E4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 必须与规范BatchReceive操作区分；准入不等于两槽均已接受 | 批次准入事件（模型中的BatchReceive） |
| T57 rejection branch; rejection reachability | 拒绝分支；拒绝见证 | 拒绝分支；拒绝见证 / 拒绝分支可达性 | M 两个rejection_exists | M（语义核对，不是中文证据） | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 存在性不蕴含所有无效输入最终拒绝，且Send未绑定被拒元组 | 拒绝分支可达性 |
| T58 non-vacuity; vacuous truth | 非真空性；真空成立 | 非真空性；真空成立 / 排除因无相关接受事件而成立的情形（non-vacuity） | T3 | M distinct_party_batch_exists | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 中文短名NO_STABLE_CONSENSUS；结果处用有效批次可达性及明确解释 | 排除因无相关接受事件而成立的情形（non-vacuity） |
| T59 refinement; refinement theorem | refinement；refinement theorem | refinement；refinement theorem / 精化；精化定理 | S3（检索摘要） | E6 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 当前未建立模型到完整协议/实现的精化定理；不把映射说明称精化证明 | 精化；精化定理 |
| T60 symbolic model; symbolic abstraction | 符号模型；两槽抽象 | 符号模型；两槽抽象 / 符号模型；符号抽象 | P1/P2 | T1；M | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 固定两槽不等于整个模型仅两次会话，也不是任意批长定理 | 符号模型；符号抽象 |
| T61 Dolev–Yao adversary; attacker | 攻击者；对手；敌手 | 攻击者；对手；敌手 / Dolev–Yao攻击者；攻击者 | P1 p3 | P4 p6；P6 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 文献中的敌手可保留引用；模型实例能力以规则为准 | Dolev–Yao攻击者；攻击者 |
| T62 replay; repeated acceptance | 重放；重复接受 | 重放；重复接受 / 重放；重复接受 | P1 | P4 p6；M | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 重复接受是抽象行为，重放候选元组不推出完整协议重放攻击 | 重放；重复接受 |
| T63 authentication; secrecy | 认证；保密性；密钥安全 | 认证；保密性；密钥安全 / 认证；保密性 | P1 p3 | P4 p6；S1 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 仅背景或边界说明；来源对应和消息互异不升级为这些性质 | 认证；保密性 |
| T64 authenticated key exchange; deniable | 认证密钥交换；可否认 | 认证密钥交换；可否认 / 认证密钥交换；可否认性 | P3/P7（认证密钥协商） | E1/E2 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 原协议背景，不是本模型新增证明 | 认证密钥交换；可否认性 |
| T65 KEM; split-KEM; prekey bundle | KEM；split-KEM；预密钥束 | KEM；split-KEM；预密钥束 / KEM；split-KEM；预密钥束 | E2及其引用 | M（语义核对，不是中文证据） | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 保留源协议术语；首次KEM可注密钥封装机制，split-KEM不强造拆分中文标准 | KEM；split-KEM；预密钥束 |
| T66 transcript; session identifier; wire representation | transcript；session标识；线路编码 | transcript；session标识；线路编码 / 协议交互记录；会话标识；传输编码 | E2 | P3 p3（会话标识） | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 说明oid不是完整协议交互记录或会话标识；勿把抽象元组写成网络字段 | 协议交互记录；会话标识；传输编码 |
| T67 non-implication; non-substitutability | 非蕴含；非替代性 | 非蕴含；非替代性 / 不蕴含；不能替代 | E2/E5 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 逻辑例子和机器可达执行分别给证据，不将常识例子充当机器结果 | 不蕴含；不能替代 |
| T68 verified; falsified; proof steps | 已验证；被反例否定；证明步数 | 已验证；被反例否定；证明步数 / 验证通过；被否定；证明步数 | T2/T3 | E5结果表 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 全称falsified可称被反例否定；exists-trace的falsified不可照搬；steps不是运行时间 | 验证通过；被否定；证明步数 |
| T69 bounded abstraction; arbitrary batch sizes | 固定两槽；任意批长 | 固定两槽；任意批长 / 固定两槽抽象；任意批次长度 | E3/E6 | M | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 两槽界限是每批槽数；批次/发送实例总数未被固定为2 | 固定两槽抽象；任意批次长度 |
| T70 matching origin; idealized origin relation | 来源匹配；精确来源关系 | 来源匹配；精确来源关系 / 精确发送来源匹配；抽象来源关系 | E4 | M !Sent | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | !Sent是持久事实的建模假设，不是实现的密码学认证机制 | 精确发送来源匹配；抽象来源关系 |
| T71 sequential processing; common lifecycle | 顺序处理；共同生命周期；共同骨架 | 顺序处理；共同生命周期；共同骨架 / 顺序处理；共同生命周期 | E4 | M ProcessSlot1/2 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 三模型共同处理过程，不推断现实网络时序完全相同 | 顺序处理；共同生命周期 |
| T72 scope; global uniqueness | 作用域；全局唯一性 | 作用域；全局唯一性 / 作用域；全局唯一性 | M 量词 | E2 | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 批内性质不声称跨批唯一；但模型Fr确实令新生成sid/m在一条执行中新鲜，不可否认这一规则事实 | 作用域；全局唯一性 |
| T73 aliveness; liveness | liveness；存活性 | liveness；存活性 / Lowe存活性；活性（liveness） | P1 p3 | T2；E5 | 有基础词/相近用法；以所列页码为限 | 按来源对应具体概念；不外推词频或唯一标准 | 区分Lowe认证层级aliveness与最终发生的活性性质；拒绝存在性不证明后者 | Lowe存活性；活性（liveness） |
| T74 supporting property; key result | 支持性质；核心结果 | 支持性质；核心结果 / 支持性质；核心结果 | E5 | 当前表4 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 论文取舍标签，非工具安全等级；不可删去量词类型 | 支持性质；核心结果 |
| T75 source-to-abstraction mapping | 来源到抽象映射；模型映射 | 来源到抽象映射；模型映射 / 协议来源与模型抽象的对应说明 | E4 | E6 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 说明性映射不等于精化证明，不能把缺失机制当已实现 | 协议来源与模型抽象的对应说明 |
| T76 composition boundary; cryptographic component | 组合边界；密码组件 | 组合边界；密码组件 / 组合边界；密码组件 | E1/E3/E6 | M（语义核对，不是中文证据） | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 批内关系区别于组件安全，不主张新的通用组合定理 | 组合边界；密码组件 |
| T77 receiver ephemeral state | 接收方临时状态；共享状态 | 接收方临时状态；共享状态 / 接收方临时状态 | E2 | M（语义核对，不是中文证据） | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 原协议状态与模型rst标识分开；不复制完整密码结构 | 接收方临时状态 |
| T78 unknown key-share; misbinding | UKS；misbinding（notes边界） | UKS；misbinding（notes边界） / 未知密钥共享（UKS）；错误绑定（misbinding） | E6/notes | M（语义核对，不是中文证据） | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 本任务仅界限清单；不得把同A的两次接受命名为UKS或错误绑定攻击 | 未知密钥共享（UKS）；错误绑定（misbinding） |
| T79 implementation; deployment | 实现；部署缺陷 | 实现；部署缺陷 / 实现；部署 | E3/E6 | notes | P1–P7未建立该完整中文词形共识 | 官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS | 抽象模型结果不等同部署漏洞或客户端遗漏检查 | 实现；部署 |
| T80 reachability sanity check | 正常路径；非真空性支持 | 正常路径；非真空性支持 / 正常路径可达性检查 | T3 | M normal_relaxed_batch_exists | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 这里只要求准入及后续一次接受，不证明两个不同参与方完成 | 正常路径可达性检查 |
| T81 one-send/two-accepts witness | 一个精确来源支持两个同批接受 | 一个精确来源支持两个同批接受 / 一个精确发送来源对应两个同批接受事件的可达执行 | M one_send_two_accepts_exists | E5 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 唯一匹配Send仅限完整元组；不排除无关发送事件 | 一个精确发送来源对应两个同批接受事件的可达执行 |
| T82 valid distinct-party batch | 有效不同参与方批次 | 有效不同参与方批次 / 有效的不同参与方批次 | M distinct_party_batch_exists | E5 | 未建立完整复合词的稳定刊内用法 | 仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS | 两匹配Send和两个接受均存在；有效仅在本抽象中解释 | 有效的不同参与方批次 |
