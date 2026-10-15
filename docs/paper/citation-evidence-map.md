# 引言候选稿：引用与研究证据映射

核验日期：2026-10-15。对应同目录 `introduction-candidate.md`，不是正式参考文献表，也不改变 Word 引用编号。

## 1. 阅读基线、核验口径与结论

本轮只读核对了以下材料：

- 当前工作稿：`submissions/arocmag/word-final/K-Waay-AROCMAG-submission-working.docx`。SHA-256：`595fb83cc3b7702115cc142b441e714b43490dd60aad5940959da940deee7d85`。
- 作者确认稿：`submissions/arocmag/word-final/source/chapter3-combined-author-approved.md`、`chapter4-party-author-approved.md`、`chapter5-party-author-approved.md`。当前 Word 对部分边界另有明确补充，例如 HMAC-only 与消费模型不是联合攻击轨迹；以当前 Word 的这些限定为准，不倒退到历史旧章稿。
- 原规划：`docs/paper/reference-expansion-plan.md`；历史题录核查矩阵：`docs/paper/literature/citation-verification.tsv`。原规划提供检索线索，不能代替本轮对引言所用来源的核查。
- K-Waay 正式会议题录及原论文；本地完整稿：`reviews/2026-09-16-evidence/kwaay-full-2024-120.pdf`，62页，首页标注2024-01-27及USENIX 2024文章的完整版本，SHA-256：`476f28594806f15f4baab6ce7d3785143db0a013f21fbcf590ac1666161660a8`。核对了摘要、§4.1、§5.1及相邻算法页；完整稿图号为Figure 10，不能误称完整稿Figure 7。印刷第21页明确要求一次BatchReceive中每个输入对应不同参与方。
- 第3～5章的模型、既有stdout及结果向量，见第5节。未运行任何新的安全实验。

候选引言实际引用16项不同研究，含3项新增国内研究。引言正文及三项贡献共981个汉字；去除引用键及空白后共1188个字符，包含英文术语与标点。字数不含候选稿的说明和调整记录。

核验层级应如实理解：出版社/会议正式题录确认“确有此文”；摘要和相关正文确认“该文支持所引论述”。下列条目逐项说明实际阅读范围，不声称逐页通读全部论文。部分国内期刊PDF由官方站点的可检索首面确认，直接打开工具返回错误；相应条目明确记录这一限制，不使用二手概述替代研究结论。

## 2. 引言逐篇引用证据

P1～P5分别指候选引言的五个自然段，C1～C3指三项贡献。以下引文摘录仅用于定位；正式整合仍应保留候选稿中的就近引用位置。

### R01 `unger2015sok`（原规划N01）

**完整题录：** Nik Unger, Sergej Dechand, Joseph Bonneau, Sascha Fahl, Henning Perl, Ian Goldberg, Matthew Smith. *SoK: Secure Messaging*. 2015 IEEE Symposium on Security and Privacy. IEEE, 2015: 232–249. DOI：[10.1109/SP.2015.22](https://doi.org/10.1109/SP.2015.22)。[作者研究团队题录](https://teamusec.de/publications/conf-sp-ungerdbfpg015/)，[公开论文](https://css.csail.mit.edu/6.5660/2018/readings/secure-messaging.pdf)。

- 实际内容：建立安全消息的安全、隐私、可用性与部署评价框架，讨论异步通信、认证、可否认性等目标之间的关系。
- 支持P1：“安全消息协议需要在异步通信中兼顾机密性、认证与可否认性。”这是背景目标归纳，不表示所有系统都实现所有性质。
- 核验：作者团队题录、DOI及论文摘要/评价目标；不是后量子算法来源，故量子迁移句另引PQXDH。
- 相关性与保留：安全消息背景直接相关；与K-Waay具体批次反例间接相关。建议保留，不能用其证明本文攻击。

### R02 `bhargavan2024pqxdh`（E5）

**完整题录：** Karthikeyan Bhargavan, Charlie Jacomme, Franziskus Kiefer, Rolfe Schmidt. *Formal Verification of the PQXDH Post-Quantum Key Agreement Protocol for End-to-End Secure Messaging*. 33rd USENIX Security Symposium (USENIX Security 24). USENIX Association, 2024: 469–486。[正式题录、摘要与论文入口](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan)。官网未列DOI，不补造。

- 实际内容：用ProVerif与CryptoVerif分析PQXDH，研究X3DH性质保持、后量子前向安全及共存部署；发现规范问题，说明具体Signal实现选择使所述问题不能直接利用，并识别额外KEM绑定要求。
- 支持P1：“后量子迁移不仅要求替换密钥交换原语，还需保留握手协议的安全保证。”支持P3：“PQXDH研究结合ProVerif与CryptoVerif分析认证、机密性及后量子前向安全，并指出证明所需的额外KEM绑定条件。”
- 核验：会议官网全部摘要及官方BibTeX，核对工具名称、目标和实现边界。
- 相关性与保留：高度相关的协议验证实例，建议保留。不能写成PQXDH实现已被攻破，也不能把其KEM绑定等同于本文`Bind(E)`。

### R03 `collins2024kwaay`（E2；E3为同一工作的完整稿）

**完整题录：** Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh Nguyen, Nicolas Rolin, Serge Vaudenay. *K-Waay: Fast and Deniable Post-Quantum X3DH without Ring Signatures*. 33rd USENIX Security Symposium (USENIX Security 24). USENIX Association, 2024: 433–450。[会议题录](https://www.usenix.org/conference/usenixsecurity24/presentation/collins)，[会议正文](https://www.usenix.org/system/files/usenixsecurity24-collins.pdf)。完整稿：Cryptology ePrint Archive, Paper 2024/120，[正式入口](https://eprint.iacr.org/2024/120)。

- 实际内容：扩展split-KEM安全定义并给出基于LWE的实例，构造无需环签名的后量子可否认异步交换；DAKE语法及BatchReceive显式处理临时状态复用。
- 支持P1：“当多个发送会话共享接收方预密钥状态时，接收过程还涉及多个输入之间的安全关系。”其中“安全关系”是由接口和复用事实引出的本文动机，不是将原论文归纳为已证明本文三项性质。
- 支持P2：“K-Waay采用强化的split-KEM安全定义，无需环签名，并以BatchReceive处理共享接收状态的输入。”
- 支持P5：“原论文已明确规定同批输入来自不同参与方。”精确依据为本地完整稿§5.1、印刷第21页的输入前提；§4.1为批量输入和输出语法。
- 核验：会议题录/摘要、本地完整稿上述段落和算法。线上ePrint直取受限，不据此否定已有本地全文，也不把当前网页访问时间当版本时间。
- 相关性与保留：核心直接来源，必须保留。建议引用库以同一工作关联会议版和完整稿，必要时在正文注明确切版本；不得作为两篇独立研究凑数。

### R04 `chen2020composable`（新增国内研究CN1，中文期刊）

**完整题录：** 陈明. 后量子前向安全的可组合认证密钥交换方案[J]. 计算机研究与发展, 2020, 57(10): 2158–2176. DOI：[10.7544/issn1000-1239.2020.20200472](https://doi.org/10.7544/issn1000-1239.2020.20200472)。[期刊官方PDF](https://crad.ict.ac.cn/cn/article/pdf/preview/10.7544/issn1000-1239.2020.20200472.pdf)，[官方当期目录](https://crad.ict.ac.cn/attached/file/20200927/20200927155554_681.pdf)。英文题名：*A Composable Authentication Key Exchange Scheme with Post-Quantum Forward Secrecy*。

- 实际内容：GC-AKE把签密和DHKE-like交换组合；实例将传统椭圆曲线身份基签密与Ring-LWE交换结合，在相应模型中研究完美前向安全及未来量子攻击下的前向机密性。
- 支持P2：“国内研究通过传统签密与格密钥交换的组合探索后量子前向安全。”
- 核验：官方PDF检索首面显示作者、完整题名、卷期页码、DOI及中英文摘要，官方目录交叉确认。直接打开页面返回错误，因此没有声称通读其证明章节。年份取正式卷期2020，而非搜索引擎的抓取时间。
- 相关性与保留：**国内协议研究，间接相关**。建议保留这一精准背景句；不能称其为完全后量子认证的异步可否认消息协议，也不能把GC-AKE“可组合”直接套为本文组合安全定理。

### R05 `brendel2021splitkem`（N02）

**完整题录：** Jacqueline Brendel, Marc Fischlin, Felix Günther, Christian Janson, Douglas Stebila. *Towards Post-Quantum Security for Signal’s X3DH Handshake*. Selected Areas in Cryptography – SAC 2020. LNCS 12804. Springer, **2021**: 404–430. DOI：[10.1007/978-3-030-81652-0_16](https://link.springer.com/chapter/10.1007/978-3-030-81652-0_16)。

- 实际内容：提出split-KEM以刻画DH式密钥复用，将X3DH转换为不额外增加消息流的KEM结构；摘要明确区分框架、被动安全格实例及主动攻击下复用的困难。
- 支持P2：“Brendel等提出split-KEM，探索不增加消息轮次的X3DH后量子化。”
- 核验：出版社题录、作者、出版日期、卷页及完整摘要。
- 相关性与保留：K-Waay直接技术前序，必须保留。SAC会议年份为2020、论文集出版年份为2021；不能写成该文已经提供满足后来K-Waay全部定义的主动安全实例。

### R06 `hashimoto2021signal`（N04）

**完整题录：** Keitaro Hashimoto, Shuichi Katsumata, Kris Kwiatkowski, Thomas Prest. *An Efficient and Generic Construction for Signal’s Handshake (X3DH): Post-Quantum, State Leakage Secure, and Deniable*. Public-Key Cryptography – PKC 2021. LNCS 12711. Springer, 2021: 410–440. DOI：[10.1007/978-3-030-75248-4_15](https://link.springer.com/chapter/10.1007/978-3-030-75248-4_15)。

- 实际内容：定义Signal-conforming AKE并用KEM、签名等构造；区分弱可否认性及借助环签名强化可否认性的方案，提供实例和实现评估。
- 支持P2：“基于KEM与签名的通用构造及指定验证者签名等方案进一步发展了异步可否认交换。”本条支持前半句；后半句由R07支持，不混为同一构造。
- 核验：出版社作者、卷页、DOI及完整摘要。
- 相关性与保留：直接技术邻近研究，建议保留。不能把较早版本的具体参数安全性无条件扩展为所有后量子实例安全。

### R07 `brendel2022asynchronous`（N03）

**完整题录：** Jacqueline Brendel, Rune Fiedler, Felix Günther, Christian Janson, Douglas Stebila. *Post-quantum Asynchronous Deniable Key Exchange and the Signal Handshake*. Public-Key Cryptography – PKC 2022. LNCS **13178**. Springer, 2022: 3–34. DOI：[10.1007/978-3-030-97131-1_1](https://link.springer.com/chapter/10.1007/978-3-030-97131-1_1)。

- 实际内容：结合KEM与指定验证者签名构造异步可否认密钥交换，并讨论直接DVS或环签名实例化。
- 支持P2同R06定位句的“指定验证者签名等方案”部分。
- 核验：出版社题录和摘要；第二作者为Rune Fiedler，不能误写为Marc Fischlin；卷号取出版社13178。
- 相关性与保留：直接技术邻近，建议保留。不把“DVS”和“环签名”当作两篇独立研究。

### R08 `hashimoto2025bake`（本轮新增国际研究R24）

**完整题录：** Keitaro Hashimoto, Shuichi Katsumata, Thom Wiggers. *Bundled Authenticated Key Exchange: A Concrete Treatment of Signal’s Handshake Protocol and Post-Quantum Security*. 34th USENIX Security Symposium (USENIX Security 25). USENIX Association, 2025: 6777–6796。[会议官方题录、摘要及全文入口](https://www.usenix.org/conference/usenixsecurity25/presentation/hashimoto-key-exchange)。官网未列DOI，不补造。

- 实际内容：BAKE显式建模预密钥束及状态，统一比较X3DH、PQXDH与其新构造RingXKEM的安全级别。
- 支持P2：“近期BAKE框架进一步显式建模预密钥束及状态，体现了准确描述异步握手状态的重要性。”后半句为基于该建模贡献的动机归纳。
- 核验：会议官网完整摘要及BibTeX，包括三位作者、2025正式出版及页码。
- 相关性与保留：协议状态建模高度相关，建议保留。不把bundled prekeys等同于本文固定两槽BatchReceive，也不据其“optimal security”术语判定K-Waay本文三项性质。

### R09 `cohngordon2020signal`（E4）

**完整题录：** Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt, Douglas Stebila. *A Formal Security Analysis of the Signal Messaging Protocol*. Journal of Cryptology, 2020, 33(4): 1914–1983. DOI：[10.1007/s00145-020-09360-1](https://link.springer.com/article/10.1007/s00145-020-09360-1)。

- 实际内容：将X3DH及Double Ratchet视为多阶段AKE，描述树形密钥演化并证明抽象核心在定义模型中的密钥安全；不是本文式的ProVerif/Tamarin结果。
- 支持P3：“Signal的多阶段认证密钥交换分析证明了其核心模型的密钥安全。”
- 核验：期刊官网作者、日期、卷页及摘要。
- 相关性与保留：正式分析代表性成果，建议保留期刊版，不另计2017会议版。该文不能支撑“所有Signal应用层会话组合均安全”。

### R10 `li2024loet`（新增国内研究CN3，国内团队英文期刊论文）

**完整题录：** Zehuan Li, Meihua Xiao, Ruihan Xu. *Formal analysis of signal protocol based on logic of events theory*. Scientific Reports, 2024, 14: **20606**. DOI：[10.1038/s41598-024-71666-y](https://www.nature.com/articles/s41598-024-71666-y)。[作者单位机构库记录](https://ir.specialsci.cn/hdjt/department/result?department=b7daf60f5a99&page=6)，[正式题录交叉核对](https://pubmed.ncbi.nlm.nih.gov/39232203/)。

- 实际内容：扩展事件逻辑的密钥关系、密钥链谓词及组合推理，分析Signal的DR结构与X3DH—DR顺序组合；其“强认证”结果依赖文中具体定义及事件顺序。
- 支持P3：“国内研究亦以事件逻辑刻画Signal的棘轮结构与子协议组合。”不在此句宣称其认证性质等同于本文P1。
- 核验：出版社页面的可检索正文，包括相关工作、结论、作者单位和正式引用信息；机构库确认华东交通大学作者归属。直接打开出版社页面遇到跳转限制，但检索返回了上述一手正文；交叉确认文章号20606，不使用聚合页“1–18”代替文章号。未声称本轮复现其证明。
- 相关性与保留：**新增国内、主题直接相关**，建议保留。它是国内团队的英文论文，不伪装成中文期刊；不将其弱/强认证术语与Lowe层次或本文接收单射性直接划等号。

### R11 `cremers2024kems`（N14）

**完整题录：** Cas Cremers, Alexander Dax, Niklas Medinger. *Keeping Up with the KEMs: Stronger Security Notions for KEMs and Automated Analysis of KEM-based Protocols*. Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security. ACM, 2024. DOI：[10.1145/3658644.3670283](https://doi.org/10.1145/3658644.3670283)。[作者公开正式论文](https://www.alexanderdax.org/assets/Kem/KEM.pdf)。

- 实际内容：建立更细的KEM绑定性质层次，并以Tamarin分析KEM协议对具体绑定假设的依赖；其再封装攻击涉及不同密文解封到相同密钥，不是本文保留split-KEM分量并替换其他分量的同一攻击。
- 支持P3：“针对KEM协议的研究进一步区分密钥、密文和公钥的绑定性质。”
- 核验：作者提供的15页会议论文首页作者、会议年和DOI，及§1、绑定层次图、符号建模/案例分析相关段落。ACM页面返回403；题录不填仅从二手页取得的连续页码，DOI及正式会议信息足以定位。
- 相关性与保留：协议形式化方法高度相关，建议保留；KEM绑定不是参与方批次互异，更不是`Bind(E)`真实认证过程的证明。

### R12 `fischlin2016confirmation`（N17）

**完整题录：** Marc Fischlin, Felix Günther, Benedikt Schmidt, Bogdan Warinschi. *Key Confirmation in Key Exchange: A Formal Treatment and Implications for TLS 1.3*. 2016 IEEE Symposium on Security and Privacy. IEEE, 2016: 452–469. DOI：[10.1109/SP.2016.34](https://doi.org/10.1109/SP.2016.34)。[作者公开论文](https://www.felixguenther.info/publications/SP_FGSW16.pdf)，[作者机构正式题录](https://research-information.bris.ac.uk/en/publications/key-confirmation-in-key-exchange-protocols-formal-definitions-and/)。机构题录使用题名变体 *Key Confirmation in Key Exchange Protocols: Formal Definitions and Implications for TLS 1.3*；同一DOI，不另计文献。

- 实际内容：独立形式化full/almost-full key confirmation，区分它与机密性、隐式认证的保证，分析当时TLS 1.3 draft-10并讨论通用MAC转换。
- 支持P3：“密钥确认理论则独立刻画对端持有密钥的保证。”
- 核验：作者论文摘要及§I A/B的定义动机、模块化关系，机构题录核对作者、会名、页码及DOI。
- 相关性与保留：**理论直接支持该句，与K-Waay实例及批次性质间接相关**，建议保留。一般密钥确认本身不保证持有者就是预期对端；本文HMAC对应关系结论仍需自己的模型，不能直接搬用该文计算定理。

### R13 `gao2014formal`（新增国内研究CN2，中文期刊）

**完整题录：** 高尚, 胡爱群, 石乐, 陈先棒. 安全协议形式化分析研究[J]. 密码学报, 2014, 1(5): 504–512. DOI：[10.13868/j.cnki.jcr.000047](https://doi.org/10.13868/j.cnki.jcr.000047)。[期刊官方全文入口](https://www.jcr.cacrnet.org.cn/CN/article/downloadArticleFile.do?attachType=PDF&id=60)。英文题名：*A Survey on Formal Analysis of Security Protocols*。

- 实际内容：综述模态逻辑、模型检测、定理证明及其局限，特别概述可靠协议组合后的复合协议安全分析。
- 支持P4：“国内形式化分析综述专门讨论复合协议。”
- 核验：官方PDF可检索首面完整题录、DOI、中英文摘要和作者单位。直接打开工具返回错误；没有声称逐页阅读全文。仅引用摘要中确有的复合协议研究范围。
- 相关性与保留：**国内方法研究、间接相关**。建议保留作为国内组合分析背景，不包装成近期Signal或K-Waay结果，也不从综述推出本文新定理。

### R14 `andova2008compositional`（N13）

**完整题录：** Suzana Andova, Cas Cremers, Kristian Gjøsteen, Sjouke Mauw, Stig F. Mjølsnes, Saša Radomirović. *A framework for compositional verification of security protocols*. Information and Computation, 2008, 206(2–4): 425–459. DOI：[10.1016/j.ic.2007.07.002](https://www.sciencedirect.com/science/article/pii/S0890540107001228)。[作者公开版本](https://satoss.uni.lu/members/sjouke/papers/AnCrGjMaMjRa08.pdf)，[作者机构题录](https://research.tue.nl/en/publications/a-framework-for-compositional-verification-of-security-protocols/)。

- 实际内容：为多协议环境定义协议独立性等条件，通过组件分析推导组合性质，以WiMAX子协议序列说明应用。
- 支持P4：“组合验证框架则通过协议独立性等条件建立组件与组合结论的联系。”同时支持“多会话安全也不能仅由单次会话结论推出”的条件化分析动机，不将多协议与多槽位混为一谈。
- 核验：出版社摘要、卷期页码与DOI，以及作者机构六位作者题录。DOI年份段2007不等于正式出版年2008。
- 相关性与保留：**组合方法、间接相关**，建议保留。不能声称本文已满足其全部独立性前提，或已证明HMAC、去重、身份准入的统一组合安全。

### R15 `cremers2023sessions`（E1）

**完整题录：** Cas Cremers, Charlie Jacomme, Aurora Naska. *Formal Analysis of Session-Handling in Secure Messaging: Lifting Security from Sessions to Conversations*. 32nd USENIX Security Symposium (USENIX Security 23). USENIX Association, 2023: 1235–1252。[会议官方题录、摘要及全文](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)。官网未列DOI，不补造。

- 实际内容：把会话管理纳入Signal/Sesame分析，用Tamarin研究多条棘轮链合并与失陷后安全，并提出加固机制；有该文自身的实现情形和clone攻击前提。
- 支持P4：“针对Signal会话管理的Tamarin研究发现，多条棘轮链合并会影响失陷后安全。”
- 核验：会议题录及完整摘要，核对Tamarin、session-handling、ratcheting chains与PCS的关系。
- 相关性与保留：多会话层次的高度相关先例，建议保留。不能借该文实际应用结果声称本文已证明K-Waay会话克隆；它也不是BatchReceive参与方互异性质的直接证明。

### R16 `lowe1997hierarchy`（E8）

**完整题录：** Gavin Lowe. *A Hierarchy of Authentication Specifications*. Proceedings of the 10th Computer Security Foundations Workshop. IEEE Computer Society, 1997: 31–43. DOI：[10.1109/CSFW.1997.596782](https://doi.org/10.1109/CSFW.1997.596782)。[会议官方论文](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)。

- 实际内容：用CSP区分aliveness、weak agreement、non-injective agreement及injective agreement，讨论参数一致与运行一一对应的差别。
- 支持P4：“认证层次理论还区分参数一致与执行的一一对应。”精确位置为§2.3及§2.4。
- 核验：官方全文相关定义及摘要；所引非单射/单射区别不是仅凭标题推测。
- 相关性与保留：安全性质定义直接相关，必须保留。本文同批消息的局部接收单射性质不自动等于该文所有全局认证定义，更不能推出同批参与方互异。

### 引言中不宜分配给外部文献的句子

P3末句“不能直接回答K-Waay批次接收中的对应关系与身份约束问题”、P4末句关于分别考察三种关系，是在明确各文研究对象后的**本文问题定位**，不是声称检索证明“全球从未有人研究身份认证”。P5关于研究安排及C1～C3为本文自身工作，必须由项目证据支撑，不能用外部论文的结果替代，见第5节。

## 3. 原文献池复审与全文25～30项的取舍

原规划为E1～E8及N01～N23，共31条书目记录、30项不同研究。没有发现应仅因无法打开个别网页就判为虚构的项目；但真实性不等于必须引用。下表复审引用必要性，非引言用文献的详细题录/一手入口沿用原规划，**不声称本轮重新通读了所有未采用论文**。

| 原编号 | 研究 | 本轮建议 | 位置及必要性/边界 |
| --- | --- | --- | --- |
| E1 | Formal Analysis of Session-Handling in Secure Messaging | 保留，已入引言 | 多会话层次；不借用其部署攻击作为本文结论 |
| E2 | K-Waay正式会议版 | 必留，已入引言 | 协议、原前提、研究对象 |
| E3 | K-Waay ePrint 2024/120完整稿 | 与E2关联，不独立计数 | 精确算法/定义版本；不能另凑一篇 |
| E4 | A Formal Security Analysis of the Signal Messaging Protocol | 保留，已入引言 | 多阶段计算模型，不误写为本项目符号证明 |
| E5 | Formal Verification of the PQXDH… | 保留，已入引言 | 认证/机密性/绑定条件与实现边界 |
| E6 | The TAMARIN Prover for the Symbolic Analysis of Security Protocols | 保留 | §2工具和方法来源，不在引言罗列工具文献 |
| E7 | Names in Cryptographic Protocols | 保留，正文相关研究简述 | §4.3或§5.2.3；身份命名与会话结果归属，间接相关 |
| E8 | A Hierarchy of Authentication Specifications | 必留，已入引言 | 非单射与单射，不能扩展为参与方互异 |
| N01 | SoK: Secure Messaging | 保留，已入引言 | 背景，不作为后量子算法证据 |
| N02 | Towards Post-Quantum Security for Signal’s X3DH Handshake | 必留，已入引言 | split-KEM源头；出版年2021 |
| N03 | Post-quantum Asynchronous Deniable Key Exchange… | 保留，已入引言 | KEM+DVS可否认握手；Fiedler作者名、13178卷号 |
| N04 | An Efficient and Generic Construction for Signal’s Handshake… | 保留，已入引言 | 通用构造与可否认性层次 |
| N05 | Post-quantum TLS without handshake signatures | 候补，不计主集合 | KEMTLS不是异步批次接口，当前论证无需另开TLS支线 |
| N06 | The Double Ratchet: Security Notions, Proofs, and Modularization… | 候补，不计主集合 | 本文不建模DR；不把握手分析扩成完整消息协议验证 |
| N07 | Modeling and Verifying Security Protocols with the Applied Pi Calculus and ProVerif | 保留 | §2.2方法依据 |
| N08 | Automatic Verification of Correspondences for Security Protocols | 必留 | §2.4、§3完整参数query及对应关系解释 |
| N09 | On the Security of Public Key Protocols | 保留 | §2.1明确采用的符号网络攻击者 |
| N10 | Automated Analysis of Diffie-Hellman Protocols and Advanced Security Properties | 保留 | §2状态重写、时间点与轨迹性质；仅引用方法 |
| N11 | Tamarin: Verification of Large-Scale, Real-World, Cryptographic Protocols | 候补，不计主集合 | 与E6/N10方法来源重叠；原规划2022年是正确的 |
| N12 | Automated Verification for Secure Messaging Protocols and Their Implementations… | 保留 | §2.2相关方法，区分代码联动与本文手工抽象模型 |
| N13 | A framework for compositional verification of security protocols | 保留，已入引言 | 有条件的组合推理，不是自动组合定理 |
| N14 | Keeping Up with the KEMs… | 保留，已入引言 | KEM细粒度绑定，不混同本文密文重组 |
| N15 | Modular Design of Secure Group Messaging Protocols and the Security of MLS | 候补，不计主集合 | 群组持续通信与本文异步批次接收差异大 |
| N16 | The Complexities of Healing in Secure Group Messaging: Why Cross-Group Effects Matter | 候补，不计主集合 | 跨群组PCS不是本文性质，避免为数量扩展综述 |
| N17 | Key Confirmation in Key Exchange… | 保留，已入引言 | 与机密性/认证区别；记录题名变体而不重复计数 |
| N18 | Formal Verification of Misbinding Attacks on Secure Device Pairing and Bootstrapping | 保留，间接相关 | §5可信绑定边界；不得称本文已验证misbinding攻击 |
| N19 | Keying Hash Functions for Message Authentication | 保留 | §3 HMAC算法源头，不虚称通用HMAC为本文原创 |
| N20 | Unknown Key-Share Attacks on the Station-to-Station (STS) Protocol | 候补，不计主集合 | 本文没有证明UKS；避免与密钥失配、身份重复混称 |
| N21 | Authentication in Key-Exchange: Definitions, Relations and Composition | 保留 | §2.4与§5机制分层；不导入其计算组合结论 |
| N22 | ASICS: Authenticated Key Exchange Security Incorporating Certification Systems | 保留 | §5.3/§5.5，公钥/身份可信归属的未建模边界 |
| N23 | TreeSync: Authenticated Group Management for Messaging Layer Security | 候补，不计主集合 | 群组成员一致性不是BatchReceive同批参与方互异 |

建议主集合：原30项不同研究减去7项候补（N05、N06、N11、N15、N16、N20、N23），加CN1～CN4及R24，共**28项不同研究**。如会议版与完整稿仍分列，表现为29条书目记录，但只有28项研究。此数字是待审查的选择集合，不是本轮实际加入Word的数量，也不是期刊硬性最低数量。

28项包含引言已用16项；其余12项为E6、E7、N07、N08、N09、N10、N12、N18、N19、N21、N22及下述CN4，供§1～5按实际论述选用。若某节没有相应实质论述，应继续删减，不机械把28项全部塞入正文。

## 4. 国内检索结果及相关性筛选

检索覆盖中文的“后量子认证密钥交换/协商”“后量子安全消息”“安全协议形式化分析”“协议组合”“身份绑定”等，并以Signal英文题名检索国内团队工作。优先核对期刊官网、正式题录和作者机构。未检索到可在本轮核验范围内替代K-Waay原文的中文BatchReceive同题研究；这不是“国内无人研究”的断言。

### 已纳入引言的三项

- CN1陈明2020：国内后量子前向安全AKE背景，明确是传统认证与格交换的混合语境。
- CN2高尚等2014：国内复合协议形式化研究背景，不伪装为最新安全消息结果。
- CN3 Li等2024：华东交通大学团队对Signal棘轮与协议组合的研究，直接相关，不把英文发表混称为中文期刊。

### CN4：纳入全文候选集合，不插入本版引言

**葛艺, 黄文超, 熊焰. 基于安全协议代码的形式化辅助建模研究[J]. 计算机应用研究, 2023, 40(4): 1189–1193,1202.** DOI：[10.19734/j.issn.1001-3695.2022.08.0446](https://www.arocmag.cn/abs/2022.08.0446)。候选键：`ge2023modeling`。

已核对期刊官网题录、摘要、页码、作者及出版历史：2022-12-07为优先出版，2023-04-05为印刷出版，正式卷期年取2023。该文用污点分析、通信状态机辅助生成Tamarin模型的关键部分。它是同刊的真实国内方法研究，与模型构造相关，但本文不是代码自动抽模研究，所以建议仅在§2交代模型来源/建模方法差异时简述，**不能声称本文有该文式的代码到模型保证**。为控制引言长度，本稿不再增加一段工具工程综述。

### 已查证但本版不选用的邻近方向

| 文献/线索 | 已核实信息与正式入口 | 不选用原因 |
| --- | --- | --- |
| 刘亚敏, 李祥学, 刘晗林. 基于格的后量子密钥交换研究 | 密码学报2017,4(5):485–497；[DOI 10.13868/j.cnki.jcr.000200](https://doi.org/10.13868/j.cnki.jcr.000200)，[官方PDF首面](https://www.jcr.cacrnet.org.cn/CN/article/downloadArticleFile.do?attachType=PDF&id=219) | 主要为LWE/RLWE/MLWE交换及性能综述，不能替代异步认证和身份语义工作；陈明2020已承担精简背景位置 |
| 廉欢欢, 侯慧莹, 赵运磊. 后量子基于验证元的三方口令认证密钥交换协议 | 通信学报2022,43(4):95–106；[期刊官网与DOI 10.11959/j.issn.1000-436x.2022062](https://www.joconline.com.cn/zh/article/doi/10.11959/j.issn.1000-436x.2022062/)；已核对正式题录 | 口令/验证元/三方信任模式与X3DH差异明显；不能仅因“后量子认证”而增加到引言 |
| 田新蕾, 董奕逸, 张济显, 王伟嘉. 后量子密码Falcon实现的形式化验证技术 | 软件学报2025,36(11):4990–5007；[期刊官网及DOI 10.13328/j.cnki.jos.007368](https://jos.org.cn/jos/article/abstract/7368?st=search) | 研究密码原语实现正确性，不是接收端认证/批次模型；不因“形式化”相同而牵强引用 |
| 基于格的抗量子认证密钥协商协议研究综述 | 检索有《计算机科学》2020,47(9):293–303的引文线索，但本轮未取得可充分核对的该刊原始题录/正文 | 仅二次引文线索不足，不补猜作者、DOI或结论，不纳入主集合 |
| 泛物联网、车联网认证与“Signal”同名同步语言文献 | 排除只因关键词命中、与异步消息/组合身份问题无实质关系者 | 不为中文文献数量或同刊数量添加无关论文 |

## 5. 本文贡献与真实项目证据对应

外部参考文献说明研究语境，以下本项目证据才支撑C1～C3。本轮仅查阅历史结果，不把已完成验证标为待完成，也不重新运行工具。

| 引言贡献/事实 | 对应模型与证据 | 已有结果及允许表述 |
| --- | --- | --- |
| C1：密文重组、密钥仍机密、完整参数失配 | `proverif/kwaay_core_final.cpp.pv`；`logs/final/proverif/out/BASELINE.out`、`COMPONENT.out` | `RecvDone ==> SendDone`为false，收发密钥机密性true，独立分量来源query true。BASELINE原始攻击轨迹含攻击者构造新的普通KEM分量并提取诚实split-KEM分量；这是真实攻击发现，不只是一般设计讨论 |
| C1：HMAC恢复对应关系 | `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`；`logs/variants/hmac-confirmation/proverif/out/HMAC_BASELINE.out`、`HMAC_COMPONENT.out` | 无泄露配置对应关系、机密性及分量来源true；`not event(HonestRun(k))`为false代表正常执行可达，不是失败结果。原始发送观察点与加固观察点不同，应保留正文说明 |
| C1适用条件 | 同目录`HMAC_LEAK_SIGSK_A.out`及`summary.txt` | 签名秘密密钥泄露配置对应关系再次false，不能宣称普遍泄露安全。引言明确无泄露条件 |
| C2：HMAC-only重复接受 | `tamarin/replay/kwaay_replay_hmac_only.spthy`；`logs/tamarin-replay-hmac-only/summary.txt` | `one_confirmed_send_two_accepts_exists` verified；`confirmed_message_accepted_at_most_once`、`injective_confirmed_receiver_accept` falsified；`confirmed_receiver_accept_has_sender` verified。固定两槽放宽输入，不是满足原参与方互异前提的反例 |
| C2：独立条件化安装影响 | `tamarin/impact/kwaay_impact_original.spthy`；`logs/tamarin-impact-original/proofs/one_send_two_accepts_two_installs_exists.out`、`unique_install_within_completed_consumer.out` | 前者verified、后者falsified。C_install-v2在批次成功完成后逐输出独立消费且不合并会话参数；不是HMAC-only模型的直接扩展，不证明实际系统必然会话克隆 |
| C2：原子消息去重 | `tamarin/replay/kwaay_replay_fixed.spthy`、`tamarin/impact/kwaay_impact_fixed.spthy`；`logs/tamarin-m3-closeout/composite-result-vector.tsv` | 相同消息至多接受一次、局部接收单射、条件化安装唯一性verified，正常不同消息批次可达。只比较完整基础消息m、同批同状态；不是跨批次全局防重放 |
| C2：HMAC与去重的组合接收证据 | `tamarin/replay/kwaay_replay_hmac_dedup.spthy`、`tamarin/impact/kwaay_impact_hmac_dedup.spthy`；`logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv` | 重复确认接受见证被否定、`confirmed_message_accepted_at_most_once`与单射性verified；`duplicate_same_base_different_tag_fail_exists`、`normal_distinct_batch_complete` verified。M4是既有Tamarin透明合成结果，不是本轮重跑，也不含参与方准入的统一密码学证明 |
| C2：消息互异不推出参与方互异 | `tamarin/rq-v2-minimal/rqv2_message_dedup.spthy`；`reviews/2026-09-16-evidence/rqv2_message_dedup-prove.stdout.txt`及`rqv2_message_dedup-traces.json` | `same_party_different_messages_batch_exists` verified；`accepted_batch_has_distinct_messages`和`receiver_accept_injective`同时verified。这是不同合法发送，不是一次发送重复接受的同一反例 |
| C3：策略比较 | 当前Word第5.2节及`source/chapter5-party-author-approved.md` | 消息去重、可信批次构造或准入、结果/会话绑定的作用比较为接口与设计分析；不宣称可信构造及扩展输出绑定均有独立机器证明 |
| C3：绑定准入恢复身份不变量并保留正常执行 | `tamarin/rq-v2-minimal/rqv2_party_admission.spthy`；`reviews/2026-09-16-evidence/rqv2_party_admission-prove.stdout.txt`及`rqv2_party_admission-traces.json` | `same_party_rejection_exists`、`accepted_batch_has_distinct_parties`、`distinct_party_batch_exists`、发送来源及接收单射性均verified。拒绝分支可达不等于每个非法输入必然有限时拒绝 |

### 第三项贡献的准确含义

贡献是分析**身份约束由哪个接口维护**、说明消息/会话标识不能充当参与方标识，并以可执行准入实例验证已接受批次的身份不变量及非空正常行为。它不是宣称新发明了字符串不等比较，也不是宣称已经建立真实密码学身份认证机制。模型直接使用已建立的独立参与方坐标：`Bind(E)=party(E)`；从具体公钥、证书、签名或用户身份到这一坐标的可信绑定仍未建模。

### 不能扩大的结论

1. 不把ProVerif核心反例、HMAC-only批次见证、C_install-v2影响、RQ-v2准入见证拼成同一条机器验证轨迹。
2. 不从固定两槽结果推出任意批次规模、跨批次重放防护或实际实现攻击。
3. 不把原协议已要求的`DistinctPartyPerBatch`描述为作者遗漏；本文研究的是其未被维持时的行为和显式维护方式。
4. 不宣称完整密码处理、HMAC、精确消息去重和参与方绑定准入已有统一计算安全/精化定理。
5. 第4章KEY/TEST及输出索引的讨论属于接口语义分析；不能改写成已经验证的密钥泄露、身份混淆或会话克隆。

## 6. 整合前检查结论

新版引言的研究进展与三项贡献可由上述文献及项目证据分别支撑；发现的限制主要是**结论范围和实际身份材料映射的未建模边界**，不是第3～5章历史证明仍未完成。候选稿没有为填补引用数量而新增研究贡献。

本轮只新增引言候选稿及本映射文档；正式Word、原规划、参考文献编号、作者确认章节、模型及验证结果均保持不变。待作者审查后，再决定选用哪些全文文献、如何统一K-Waay版本引用及正式编号。
