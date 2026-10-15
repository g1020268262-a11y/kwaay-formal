# K-Waay 论文参考文献扩充与引用位置规划

核查日期：2026-10-15。本文件是待作者确认的引用规划，不是论文正文替换稿。

审查对象为 `submissions/arocmag/word-final/K-Waay-AROCMAG-submission-working.docx`，读取时 SHA-256 为 `595fb83cc3b7702115cc142b441e714b43490dd60aad5940959da940deee7d85`。当前章节为 §0 引言、§1 协议及安全问题、§2 形式化建模与安全性质、§3 消息篡改与重放及加固、§4 参与方互异假设及影响、§5 身份约束维护、§6 结束语。

建议保留现有8条书目记录，补充下列23篇真实论文，形成31条记录；K-Waay 会议版与完整稿去重后，共30项不同研究。这里的“新增”以当前 Word 文献表为参照，部分论文已在仓库文献库中收录，不表示本轮首次发现。“约30篇”仅是作者的规划目标，不是已经核实的期刊最低要求，也不应靠重复版本凑数。

核验方法：先读取当前 Word 的实际文献表、正文引用与章节，再参考仓库 `docs/paper/literature/citation-verification.tsv` 和 `submissions/arocmag/word-final/source/references.bib` 寻找线索，随后通过出版社、会议官网、作者单位页面或作者提供的论文核对题录与相关内容。以下每项均给出核验入口和实际查看范围；未声称逐页通读所有论文。BibTeX 仅保存在本文件的代码块中，不修改现有 `.bib` 或 Word。

## Existing References Review

### 当前实际文献及保留意见

E1—E8 对应现稿[1]—[8]，只是本规划的稳定标识，不是新编号。Word 文末的编号由列表属性产生，不能因纯文本提取未显示方括号就判定编号丢失。

| 现编号 | 题录及一手核验入口 | 真实性与版本审查 | 当前正文位置与建议 |
| --- | --- | --- | --- |
| E1 / [1] | Cas Cremers, Charlie Jacomme, Aurora Naska. **Formal Analysis of Session-Handling in Secure Messaging: Lifting Security from Sessions to Conversations**. USENIX Security 2023: 1235–1252。[会议题录与摘要](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling) | 真实，作者、年份、页码与官网一致，保留。 | §0 第1段“多会话组合……”后引用，基本合理。该文具体研究 session-handling、会话链合并与 PCS，不能扩写成它已经证明所有批处理都会破坏安全。可在 §4.4 条件化消费影响的相关研究比较处再次引用，但不能把其实际克隆场景当作本项目已验证的部署攻击。 |
| E2 / [2] | Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh Nguyen, Nicolas Rolin, Serge Vaudenay. **K-Waay: Fast and Deniable Post-Quantum X3DH without Ring Signatures**. USENIX Security 2024: 433–450。[会议题录与摘要](https://www.usenix.org/conference/usenixsecurity24/presentation/collins) | 真实，正式会议版，保留。官网提供正式出版信息，未列 DOI，不应补造。 | §0 第1段、§1.1 首段均合理。后续 §4.3.2 解释原协议按参与方索引组织输出及安全接口时，应补引 E2/E3 的具体定义，而非只引一般认证文献。 |
| E3 / [3] | 与 E2 相同的5位作者和标题。**Cryptology ePrint Archive, Paper 2024/120**。[完整稿入口](https://eprint.iacr.org/2024/120)；[会议论文正文](https://www.usenix.org/system/files/usenixsecurity24-collins.pdf)明确指向其 full version。 | 真实，但不是另一项独立研究。保留其完整算法和定义的来源作用。本轮 ePrint 页面直取受限，真实性及版本关系由正式会议正文交叉确认，不声称本轮重新逐页核查了完整稿。 | §0、§1.1、§1.2 已引用。§1.2“完整稿第5.1节……”属于需要精确版本支撑的引用，应继续保留；未来整理时记录实际采用的完整稿版本/日期，不能把网页访问日当版本日期。当前 `[2026-10-08]` 是原有访问日期，本轮不擅改。 |
| E4 / [4] | Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt, Douglas Stebila. **A Formal Security Analysis of the Signal Messaging Protocol**. Journal of Cryptology, 2020, 33(4): 1914–1983. DOI: [10.1007/s00145-020-09360-1](https://link.springer.com/article/10.1007/s00145-020-09360-1)。 | 真实，期刊版，保留。不要再新增其2017会议版来增加计数。 | §0 第2段“Signal、PQXDH……”后引用合理。须注意这是计算安全框架下的多阶段 AKE 分析，不宜写成与本文相同的 ProVerif/Tamarin 分析。 |
| E5 / [5] | Karthikeyan Bhargavan, Charlie Jacomme, Franziskus Kiefer, Rolfe Schmidt. **Formal Verification of the PQXDH Post-Quantum Key Agreement Protocol for End-to-End Secure Messaging**. USENIX Security 2024: 469–486。[会议题录与摘要](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan) | 真实，保留。官方摘要说明使用 ProVerif 和 CryptoVerif。 | §0 第2段合理。适合补充其 KEM 绑定需求及规范分析的研究现状；必须保留“所发现的规范问题由于具体实现选择而不能直接在 Signal 应用中利用”的边界，不能宣传为已攻破实际 Signal。 |
| E6 / [6] | Simon Meier, Benedikt Schmidt, Cas Cremers, David Basin. **The TAMARIN Prover for the Symbolic Analysis of Security Protocols**. CAV 2013, LNCS 8044: 696–701. DOI: [10.1007/978-3-642-39799-8_48](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48)。 | 真实，保留。 | §2.3 首段“多集重写规则……”后引用合理。与 N10/N11 配合说明工具，而不能由工具支持无界会话推出本文固定两槽结果已经覆盖任意批次规模。 |
| E7 / [7] | Simone Lupetti, Feike W. Dillema, Tage Stabell-Kulø. **Names in Cryptographic Protocols**. WOSIS 2006: 185–194. DOI: [10.5220/0002484701850194](https://www.scitepress.org/PublishedPapers/2006/24847/)。 | 真实，出版社题录、摘要和 BibTeX 可检索。保留。作者姓氏末尾的 `ø` 在 Word 中变成 `O`，属于后续题录规范化事项，不是不存在的作者。 | 本轮未在正文检出[7]。建议在 §4.3.1 参与方名称/归属语义比较处，或 §5.2.3 结果与会话身份绑定策略处引用。它讨论跨相关会话的命名唯一性，不等于本文同一批次的参与方互异定理。 |
| E8 / [8] | Gavin Lowe. **A Hierarchy of Authentication Specifications**. 10th IEEE Computer Security Foundations Workshop, 1997: 31–43. DOI: [10.1109/CSFW.1997.596782](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)。 | 真实，保留，认证层次及 injective agreement 的基础来源。 | 本轮未在正文检出[8]。优先补在 §2.4“该性质为非单射对应关系……”和接收发生单射性定义附近。必须明确项目自定义的同批消息单射限制与 Lowe 的一般 agreement 定义之间的对应和差别。 |

### 格式一致性及正文引用问题

现有8条整体采用英文姓氏大写、名字缩写、超过3人用 `et al.`、`[C]//` / `[J]` / `[EB/OL]` 分类，会议文献大多含出版地和出版者，期刊文献含卷期页码。总体框架已经较统一，不需要推倒重做。本轮只记录以下后续整理事项：

1. 采用同一英文题名大小写规则；保留 K-Waay、Signal、PQXDH、TAMARIN 等专名，不把 BibTeX 原始 title 大小写机械当成 Word 排版样式。
2. 保留作者原有变音符号；全文统一 `DOI:` 后空格、页码连接符和会议全称/简称的写法。BibTeX 页码用 `--`，Word 显示可统一为期刊模板要求的连接符。
3. USENIX 条目没有 DOI 不代表缺项；使用其官方作者、会名、出版者、年份、页码、URL 即可。不得为“格式统一”编造 DOI。
4. E3 是 online/full version，继续用相应电子资源类型及实际访问日期；不能一边采用会议版页码，一边把 ePrint 动态全文当作同一固定版式。
5. 正文共检出8处引文簇：§0 第1段两处、§0 第2段一处、§1.1 两处、§1.2 两处、§2.3 一处；实际涉及[1]—[6]，未检出[7][8]。未发现超出1—8的正文文献号。文末存在空段，但本轮不做排版修改。
6. §2.1 的 Dolev–Yao 假设、§2.2 的 ProVerif 方法、§2.4 的对应关系/单射性目前缺少紧邻的基础来源，优先安排 N09、N07/N08、E8。
7. §3 的 HMAC 和显式密钥确认需要 N19、N17/N21；协议自己的修复前后机器结果仍由项目模型/日志支撑，外部文献不替代这些结果。
8. §4.3.2 的 `KEY(i,s,j)` / `TEST(i,s,j)` 等原协议接口解释需要 E2/E3 精确定位；N18/N20/N22 只能提供身份绑定的比较背景，不能证明本文尚未建模的密钥混淆或泄露。
9. §5 的 `Bind(E)`、准入比较和已接受批次互异性质来自本文的模型及假设。新增引用宜用于说明可信绑定的既有问题与策略背景，而非制造“某文献已证明本文具体机制”的印象。

### 计数及来源优先级

本规划采用 E1—E8 与 N01—N23 作为引用键。确认后应按照新正文第一次引用顺序重新生成文末序号，不能把 N01 直接当作未来[9]。

正式发表的会议/期刊版优先作为 BibTeX 主条目，作者公开全文用于内容核查。除已有 E2/E3 的必要版本分工外，不再同时把同一论文的 ePrint、会议版和期刊版计作多篇。候选条目中若 DOI 页面访问受限，明确使用作者或作者单位的一手材料核对内容，不把搜索结果中的他人概述当作研究结论。

## Candidate New References

### A 后量子安全消息及 KEM 认证密钥交换

### N01 SoK Secure Messaging

**完整标题：SoK: Secure Messaging。** 作者 Nik Unger、Sergej Dechand、Joseph Bonneau、Sascha Fahl、Henning Perl、Ian Goldberg、Matthew Smith；2015；IEEE Symposium on Security and Privacy，232–249。

核验依据：[IEEE正式题录与摘要](https://ieeexplore.ieee.org/abstract/document/7163029)、[作者公开论文](https://jbonneau.com/doc/UDBFPGS15-IEEESP-secure_messaging_sok-abridged.pdf)。已核查安全消息评价框架及 trust establishment、conversation security 的摘要/引言。

相关性：为背景中区分消息保密、认证和会话/参与者一致性提供术语基础。适用章节：§0 背景；§1.3 研究范围。推荐引用段落：引言开头异步安全消息的安全目标背景，或后续新增的安全消息研究现状段。边界：这是2015年的系统化研究，不是当前产品功能调查，也不直接讨论 K-Waay BatchReceive。

```bibtex
@inproceedings{unger2015sok,
  author = {Nik Unger and Sergej Dechand and Joseph Bonneau and Sascha Fahl and Henning Perl and Ian Goldberg and Matthew Smith},
  title = {{SoK}: Secure Messaging},
  booktitle = {2015 IEEE Symposium on Security and Privacy},
  year = {2015}, pages = {232--249}, publisher = {IEEE},
  doi = {10.1109/SP.2015.22},
  url = {https://ieeexplore.ieee.org/abstract/document/7163029}
}
```

### N02 split KEM 与 X3DH 后量子化

**完整标题：Towards Post-Quantum Security for Signal’s X3DH Handshake。** 作者 Jacqueline Brendel、Marc Fischlin、Felix Günther、Christian Janson、Douglas Stebila；SAC 2020，正式论文集2021年出版，LNCS 12804，404–430。

核验依据：[Springer题录与摘要](https://link.springer.com/chapter/10.1007/978-3-030-81652-0_16)、[作者页面](https://www.douglas.stebila.ca/research/papers/SAC-BFGJS20/)。已核查 split KEM、密钥复用与实例化局限的摘要。

相关性：是 K-Waay 使用 split-KEM 的直接前史，优先级高。适用章节：§0 后量子握手研究现状；§1.1 原语背景。推荐引用段落：从经典 DH 型异步握手过渡到 KEM/split-KEM 的段落，或 §1.1 首次解释 split-KEM 处。边界：不能写成该文已给出满足后来 K-Waay 全部性质的强后量子实例。年份按出版社2021，会议名称仍为 SAC 2020；作者页面使用2020的记法不混入本条 year。

```bibtex
@inproceedings{brendel2021splitkem,
  author = {Jacqueline Brendel and Marc Fischlin and Felix G{\"u}nther and Christian Janson and Douglas Stebila},
  title = {Towards Post-Quantum Security for {Signal}'s {X3DH} Handshake},
  booktitle = {Selected Areas in Cryptography -- SAC 2020},
  year = {2021}, series = {Lecture Notes in Computer Science},
  volume = {12804}, pages = {404--430}, publisher = {Springer},
  doi = {10.1007/978-3-030-81652-0_16},
  url = {https://link.springer.com/chapter/10.1007/978-3-030-81652-0_16}
}
```

### N03 可否认后量子异步握手

**完整标题：Post-quantum Asynchronous Deniable Key Exchange and the Signal Handshake。** 作者 Jacqueline Brendel、Rune Fiedler、Felix Günther、Christian Janson、Douglas Stebila；PKC 2022，LNCS 13178，3–34。

核验依据：[Springer正式题录与摘要](https://link.springer.com/chapter/10.1007/978-3-030-97131-1_1)、[IACR论文正文](https://www.iacr.org/archive/pkc2022/131770016/131770016.pdf)。已核查异步性、可否认性及 KEM+DVS 构造的摘要/引言。

相关性：解释后量子 X3DH 类协议需要同时处理的设计目标，帮助定位 K-Waay 与先行方案。适用章节：§0 研究现状；§1.1。推荐引用段落：与 N04、E2 一起形成“已有后量子替代构造—K-Waay 的路线”比较。边界：不比较未经统一实验的性能；本篇第一作者组与 N02 不同，不混淆 Fiedler 与 Fischlin。卷号按出版社13178。

```bibtex
@inproceedings{brendel2022asynchronous,
  author = {Jacqueline Brendel and Rune Fiedler and Felix G{\"u}nther and Christian Janson and Douglas Stebila},
  title = {Post-quantum Asynchronous Deniable Key Exchange and the {Signal} Handshake},
  booktitle = {Public-Key Cryptography -- PKC 2022},
  year = {2022}, series = {Lecture Notes in Computer Science},
  volume = {13178}, pages = {3--34}, publisher = {Springer},
  doi = {10.1007/978-3-030-97131-1_1},
  url = {https://link.springer.com/chapter/10.1007/978-3-030-97131-1_1}
}
```

### N04 Signal conforming AKE 的通用构造

**完整标题：An Efficient and Generic Construction for Signal’s Handshake (X3DH): Post-Quantum, State Leakage Secure, and Deniable。** 作者 Keitaro Hashimoto、Shuichi Katsumata、Kris Kwiatkowski、Thomas Prest；PKC 2021，LNCS 12711，410–440。

核验依据：[Springer题录与摘要](https://link.springer.com/chapter/10.1007/978-3-030-75248-4_15)、[作者完整稿](https://eprint.iacr.org/2021/616.pdf)。已核查 Signal-conforming AKE、KEM 构造和泄露条件的摘要/引言。

相关性：提供从 X3DH 到后量子 AKE 的另一条直接研究路线。适用章节：§0 后量子协议现状；§1.1。推荐引用段落：与 N02/N03 对比之后引入 K-Waay；可在 §2.1 讨论不同论文的状态泄露模型时使用。边界：不能把该文泄露安全定理移植到本项目 HMAC 无泄露配置，也不额外计入其2022期刊扩展版。

```bibtex
@inproceedings{hashimoto2021signal,
  author = {Keitaro Hashimoto and Shuichi Katsumata and Kris Kwiatkowski and Thomas Prest},
  title = {An Efficient and Generic Construction for {Signal}'s Handshake ({X3DH}): Post-Quantum, State Leakage Secure, and Deniable},
  booktitle = {Public-Key Cryptography -- PKC 2021},
  year = {2021}, series = {Lecture Notes in Computer Science},
  volume = {12711}, pages = {410--440}, publisher = {Springer},
  doi = {10.1007/978-3-030-75248-4_15},
  url = {https://link.springer.com/chapter/10.1007/978-3-030-75248-4_15}
}
```

### N05 KEM based authentication 的比较背景

**完整标题：Post-Quantum TLS Without Handshake Signatures。** 作者 Peter Schwabe、Douglas Stebila、Thom Wiggers；ACM CCS 2020，1461–1480。

核验依据：[作者题录、摘要与BibTeX](https://www.douglas.stebila.ca/research/papers/CCS-SchSteWig20/)、[作者实验仓库中的出版题录](https://github.com/thomwiggers/kemtls-experiment)。已核查 KEMTLS 使用 KEM 实现服务器认证的摘要。

相关性：表明 KEM 认证协议不限于安全消息，适合简短说明原语替换后的认证设计问题。适用章节：§0，必要时 §1.3。推荐引用段落：后量子 AKE 的较广背景段，以一句旁及 TLS 即可，不扩展为 TLS 综述。边界：KEMTLS 是交互式 TLS 变体，不具有 K-Waay 的批量接收接口，其认证论证不能代替本文确认机制的验证。

```bibtex
@inproceedings{schwabe2020kemtls,
  author = {Peter Schwabe and Douglas Stebila and Thom Wiggers},
  title = {Post-Quantum {TLS} Without Handshake Signatures},
  booktitle = {Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security},
  year = {2020}, pages = {1461--1480}, publisher = {ACM},
  doi = {10.1145/3372297.3423350},
  url = {https://www.douglas.stebila.ca/research/papers/CCS-SchSteWig20/}
}
```

### N06 安全消息的模块化密钥更新

**完整标题：The Double Ratchet: Security Notions, Proofs, and Modularization for the Signal Protocol。** 作者 Joël Alwen、Sandro Coretti、Yevgeniy Dodis；EUROCRYPT 2019，LNCS 11476，129–158。

核验依据：[Springer题录与摘要](https://link.springer.com/chapter/10.1007/978-3-030-17653-2_5)、[作者完整稿](https://eprint.iacr.org/2018/1037.pdf)。已查看安全目标与模块分解的引言相关内容。

相关性：补充 Signal 在握手之后的模块化研究，使“核心会话”与“会话管理/组合”有清晰层次。适用章节：§0 研究现状；§1.3 范围比较。推荐引用段落：E4、E5 所在安全消息形式化现状段，随后用 E1 引向会话管理。边界：本文不分析 Double Ratchet，也不声称证明前向安全或 PCS；不把该文的通用后量子可实例化性误写为所有 Signal 部署已完全后量子化。

```bibtex
@inproceedings{alwen2019doubleratchet,
  author = {Jo{\"e}l Alwen and Sandro Coretti and Yevgeniy Dodis},
  title = {The Double Ratchet: Security Notions, Proofs, and Modularization for the {Signal} Protocol},
  booktitle = {Advances in Cryptology -- EUROCRYPT 2019},
  year = {2019}, series = {Lecture Notes in Computer Science},
  volume = {11476}, pages = {129--158}, publisher = {Springer},
  doi = {10.1007/978-3-030-17653-2_5},
  url = {https://link.springer.com/chapter/10.1007/978-3-030-17653-2_5}
}
```

### B 形式化方法与轨迹性质

### N07 ProVerif 建模与验证基础

**完整标题：Modeling and Verifying Security Protocols with the Applied Pi Calculus and ProVerif。** 作者 Bruno Blanchet；2016；Foundations and Trends in Privacy and Security，1(1–2): 1–135。

核验依据：[作者题录与摘要](https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.html)、[作者公开论文](https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.pdf)。已核查符号建模、机密性/认证查询及工具适用范围的概述。

相关性：当前缺少的 ProVerif 主要方法来源。适用章节：§0 方法选择；§2.2、§2.4。推荐引用段落：§2.2 首段介绍公开信道、原语等式、事件和查询时；引言仅可简引，不堆砌方法历史。边界：工具论文不证明本文特定模型正确抽象了部署实现，也不把不可判定/未证明等同于已找到真实攻击。

```bibtex
@article{blanchet2016proverif,
  author = {Bruno Blanchet},
  title = {Modeling and Verifying Security Protocols with the Applied Pi Calculus and {ProVerif}},
  journal = {Foundations and Trends in Privacy and Security},
  year = {2016}, volume = {1}, number = {1--2}, pages = {1--135},
  doi = {10.1561/3300000004},
  url = {https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.html}
}
```

### N08 对应关系与认证查询

**完整标题：Automatic Verification of Correspondences for Security Protocols。** 作者 Bruno Blanchet；2009；Journal of Computer Security，17(4): 363–434。

核验依据：[作者题录与摘要](https://bblanche.gitlabpages.inria.fr/publications/BlanchetJCS08.html)、[出版者题录](https://journals.sagepub.com/doi/10.3233/JCS-2009-0339)。已核查通过对应关系形式化认证以及 Horn 子句验证方法的摘要。

相关性：直接支撑 `RecvDone ==> SendDone` 的方法解释，而不仅是泛指验证工具。适用章节：§2.4 P1 定义；§3.3 查询结果解释。推荐引用段落：式(6)附近及“非单射对应关系不限制重复接受”的说明。边界：正文仍应使用真实模型中的事件参数和观察点；不能把非单射查询通过称为接收唯一性成立。作者网页文件名含08，但期刊正式出版年为2009。

```bibtex
@article{blanchet2009correspondences,
  author = {Bruno Blanchet},
  title = {Automatic Verification of Correspondences for Security Protocols},
  journal = {Journal of Computer Security},
  year = {2009}, volume = {17}, number = {4}, pages = {363--434},
  doi = {10.3233/JCS-2009-0339},
  url = {https://bblanche.gitlabpages.inria.fr/publications/BlanchetJCS08.html}
}
```

### N09 主动符号攻击者基础

**完整标题：On the Security of Public Key Protocols。** 作者 Danny Dolev、Andrew C. Yao；1983；IEEE Transactions on Information Theory，29(2): 198–208。

核验依据：[IEEE题录与摘要](https://ieeexplore.ieee.org/document/1056650/)。已核查主动攻击者可冒充、修改消息及形式化分析框架的摘要。

相关性：支撑当前 §2.1 明确采用的 Dolev–Yao 攻击者假设。适用章节：§2.1。推荐引用段落：“本文采用 Dolev–Yao 主动网络攻击者……”句末。边界：这不是计算安全归约，不能据此宣称抵抗所有实际量子攻击或实现侧信道。

```bibtex
@article{dolev1983protocols,
  author = {Danny Dolev and Andrew C. Yao},
  title = {On the Security of Public Key Protocols},
  journal = {IEEE Transactions on Information Theory},
  year = {1983}, volume = {29}, number = {2}, pages = {198--208},
  doi = {10.1109/TIT.1983.1056650},
  url = {https://ieeexplore.ieee.org/document/1056650/}
}
```

### N10 状态化多集重写和轨迹公式

**完整标题：Automated Analysis of Diffie-Hellman Protocols and Advanced Security Properties。** 作者 Benedikt Schmidt、Simon Meier、Cas Cremers、David Basin；IEEE CSF 2012，78–94。

核验依据：[IEEE会议论文](https://conferences.computer.org/sp/pdfs/csf/2012/4718a078.pdf)、[ETH题录与摘要](https://www.research-collection.ethz.ch/items/86334f42-ed46-41b4-bf09-de90dbb463a3)。已核查多集重写、含时间点的一阶性质和证伪/证明方法。

相关性：给出 Tamarin 状态和 trace property 的基础，补充 E6 的工具介绍。适用章节：§2.3、§2.4；§3.4/§5.4 的见证与全称性质区分。推荐引用段落：线性状态和事件先后关系的说明，或首次解释存在性引理与全称安全性质时。边界：本文不是在验证 DH 协议；引用其方法，不导入其 NAXOS/eCK 结论，更不把工具的无界会话能力当作本项目批次规模无界的证明。

```bibtex
@inproceedings{schmidt2012advanced,
  author = {Benedikt Schmidt and Simon Meier and Cas Cremers and David Basin},
  title = {Automated Analysis of {Diffie-Hellman} Protocols and Advanced Security Properties},
  booktitle = {2012 IEEE 25th Computer Security Foundations Symposium},
  year = {2012}, pages = {78--94}, publisher = {IEEE},
  doi = {10.1109/CSF.2012.25},
  url = {https://conferences.computer.org/sp/pdfs/csf/2012/4718a078.pdf}
}
```

### N11 Tamarin 的实际协议分析方法综述

**完整标题：Tamarin: Verification of Large-Scale, Real-World, Cryptographic Protocols。** 作者 David Basin、Cas Cremers、Jannik Dreier、Ralf Sasse；2022；IEEE Security & Privacy，20(3): 24–32。

核验依据：[作者提供的正式论文](https://people.inf.ethz.ch/basin/pubs/tamarinIEEE2022.pdf)、[Tamarin项目出版物页](https://tamarin-prover.com/publications.html)。已查看第24–25页的模型输入、局部状态、轨迹性质、有效性/可满足性检查及非终止说明。DOI取论文首页，不误取末页广告的其他 DOI。

相关性：解释为何接收状态、顺序和拒绝路径适合 Tamarin。适用章节：§0 方法选择；§2.3、§2.4。推荐引用段落：§2.3 的生命周期模型说明，以及 §2.4 对“反例存在”和“全称性质成立”的区分。边界：大型协议成功案例不意味着本文做过同等级实现验证或任意规模批次证明。

```bibtex
@article{basin2022tamarin,
  author = {David Basin and Cas Cremers and Jannik Dreier and Ralf Sasse},
  title = {{Tamarin}: Verification of Large-Scale, Real-World, Cryptographic Protocols},
  journal = {IEEE Security \& Privacy},
  year = {2022}, volume = {20}, number = {3}, pages = {24--32},
  doi = {10.1109/MSEC.2022.3154689},
  url = {https://people.inf.ethz.ch/basin/pubs/tamarinIEEE2022.pdf}
}
```

### N12 安全消息中的符号与计算验证应用

**完整标题：Automated Verification for Secure Messaging Protocols and Their Implementations: A Symbolic and Computational Approach。** 作者 Nadim Kobeissi、Karthikeyan Bhargavan、Bruno Blanchet；IEEE EuroS&P 2017，435–450。

核验依据：[作者题录、摘要与BibTeX](https://bblanche.gitlabpages.inria.fr/proverif/publications/KobeissiBhargavanBlanchetEuroSP17.html)、[IEEE出版入口](https://ieeexplore.ieee.org/document/7961995)。已核查 ProScript、ProVerif、CryptoVerif 及 Signal 变体案例的摘要/引言；正式会名、年页码、出版者足以检索，本条不填未从所用一手题录取得的 DOI。

相关性：是 ProVerif 用于安全消息认证/机密性分析的具体应用，不只是工具功能介绍。适用章节：§0 形式化研究现状；§2.2 方法比较。推荐引用段落：当前“Signal、PQXDH……形式化研究”段，与 E4/E5 分开说明计算证明、符号验证及实现联动的不同层次。边界：该文案例是 Signal 变体和 Cryptocat，不应写成完成所有 Signal 实现的验证；本文也没有其代码到模型的保证。

```bibtex
@inproceedings{kobeissi2017messaging,
  author = {Nadim Kobeissi and Karthikeyan Bhargavan and Bruno Blanchet},
  title = {Automated Verification for Secure Messaging Protocols and Their Implementations: A Symbolic and Computational Approach},
  booktitle = {2017 IEEE European Symposium on Security and Privacy},
  year = {2017}, pages = {435--450}, publisher = {IEEE},
  url = {https://bblanche.gitlabpages.inria.fr/proverif/publications/KobeissiBhargavanBlanchetEuroSP17.html}
}
```

### C 多会话及协议组合安全

### N13 协议组合验证的条件

**完整标题：A Framework for Compositional Verification of Security Protocols。** 作者 Suzana Andova、Cas Cremers、Kristian Gjøsteen、Sjouke Mauw、Stig F. Mjølsnes、Saša Radomirović；2008；Information and Computation，206(2–4): 425–459。

核验依据：[出版社摘要与题录](https://www.sciencedirect.com/science/article/pii/S0890540107001228)、[作者单位题录与BibTeX](https://research.tue.nl/en/publications/a-framework-for-compositional-verification-of-security-protocols/)。已核查组件、多协议环境、协议独立性及组合定理条件的摘要。

相关性：直接支持“局部性质不能无条件提升到组合系统”的方法论。适用章节：§0 组合问题动机；§2.1 模型边界；§3.5 或 §5.5 组合机制范围。推荐引用段落：引言对单次会话与组合处理的区别；或两种工具模型不能拼接为联合轨迹的说明。边界：本文未证明满足该文全部独立性前提，不能借此宣布 ProVerif 与 Tamarin 模型之间已有组合定理。

```bibtex
@article{andova2008compositional,
  author = {Suzana Andova and Cas Cremers and Kristian Gj{\o}steen and Sjouke Mauw and Stig F. Mj{\o}lsnes and Sa{\v{s}}a Radomirovi{\'c}},
  title = {A Framework for Compositional Verification of Security Protocols},
  journal = {Information and Computation},
  year = {2008}, volume = {206}, number = {2--4}, pages = {425--459},
  doi = {10.1016/j.ic.2007.07.002},
  url = {https://www.sciencedirect.com/science/article/pii/S0890540107001228}
}
```

### N14 KEM 绑定及协议级安全分析

**完整标题：Keeping Up with the KEMs: Stronger Security Notions for KEMs and Automated Analysis of KEM-based Protocols。** 作者 Cas Cremers、Alexander Dax、Niklas Medinger；ACM CCS 2024。DOI：10.1145/3658644.3670283。

核验依据：[作者单位的论文页与摘要](https://cispa.de/de/research/publications/84212-keeping-up-with-the-kems-stronger-security-notions-for-kems-and-automated-analysis-of-kem-based-protocols)、[作者ePrint题录与摘要](https://eprint.iacr.org/2023/1933)、[正式出版入口](https://dl.acm.org/doi/10.1145/3658644.3670283)。已核查更强 KEM 绑定性质、re-encapsulation 及 Tamarin 模型库的摘要；ACM正文页本轮访问受限。研究内容依据前两项一手来源，不依据他人引用概述。主条目使用已出版的2024会议版，不把ePrint编号中的2023当作会议年份。

相关性：与第3章“局部分量满足性质，但完整消息仍可能失配”的动机非常接近，优先级高。适用章节：§0 KEM协议分析现状；§2.2/§2.3 抽象边界；§3.2 相关原因比较。推荐引用段落：E5 的 KEM 绑定需求之后，说明原语的机密性与额外绑定性质需要区分。边界：该文 re-encapsulation 不自动等同于本项目保留 split-KEM 分量、替换普通 KEM 分量的具体轨迹；不得声称本项目使用了其模型库或完成了计算模型与符号模型的对应证明。

```bibtex
@inproceedings{cremers2024kems,
  author = {Cas Cremers and Alexander Dax and Niklas Medinger},
  title = {Keeping Up with the {KEMs}: Stronger Security Notions for {KEMs} and Automated Analysis of {KEM}-based Protocols},
  booktitle = {Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security},
  year = {2024}, publisher = {ACM},
  doi = {10.1145/3658644.3670283},
  url = {https://eprint.iacr.org/2023/1933}
}
```

### N15 安全消息的组件组合

**完整标题：Modular Design of Secure Group Messaging Protocols and the Security of MLS。** 作者 Joël Alwen、Sandro Coretti、Yevgeniy Dodis、Yiannis Tselekounis；ACM CCS 2021，1463–1483。

核验依据：[作者完整稿题录与摘要](https://eprint.iacr.org/2021/1083)、[作者单位出版题录](https://pure.royalholloway.ac.uk/en/publications/modular-design-of-secure-group-messaging-protocols-and-the-securi/)。已核查安全谓词、组件分解及其组合关系的摘要。

相关性：提供与安全消息直接相关的模块化组合实例，比泛泛列举密码学组合概念更贴近本文。适用章节：§0 组合安全相关研究；§5.5 协同作用与范围。推荐引用段落：讨论会话确认、消息去重和身份准入分别承担什么目标时，作为分层分析的比较背景。边界：MLS 群组成员机制不等于 BatchReceive 批次，本文未套用其组合定理，也不验证群组消息协议。

```bibtex
@inproceedings{alwen2021modular,
  author = {Jo{\"e}l Alwen and Sandro Coretti and Yevgeniy Dodis and Yiannis Tselekounis},
  title = {Modular Design of Secure Group Messaging Protocols and the Security of {MLS}},
  booktitle = {Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security},
  year = {2021}, pages = {1463--1483}, publisher = {ACM},
  doi = {10.1145/3460120.3484820},
  url = {https://eprint.iacr.org/2021/1083}
}
```

### N16 跨上下文效应的安全消息实例

**完整标题：The Complexities of Healing in Secure Group Messaging: Why Cross-Group Effects Matter。** 作者 Cas Cremers、Britta Hale、Konrad Kohbrok；USENIX Security 2021，1847–1864。

核验依据：[会议题录、摘要与BibTeX](https://www.usenix.org/conference/usenixsecurity21/presentation/cremers)。已核查多群组上下文中 PCS/认证恢复变化的摘要。

相关性：作为单一上下文分析不足的补充例子，与 E1 的 session-handling 分工明确。适用章节：§0 组合研究动机；§4.4 综合分析。推荐引用段落：引言从单次协议安全转向状态/组合语义的段落，或影响分析结束处的一句相关研究比较。边界：只适合相邻研究比较，不能称其已发现 K-Waay 批次攻击；该文讨论的 MLS Draft-11 不应泛化为所有当前 MLS 版本。

```bibtex
@inproceedings{cremers2021healing,
  author = {Cas Cremers and Britta Hale and Konrad Kohbrok},
  title = {The Complexities of Healing in Secure Group Messaging: Why Cross-Group Effects Matter},
  booktitle = {30th USENIX Security Symposium (USENIX Security 21)},
  year = {2021}, pages = {1847--1864}, publisher = {USENIX Association},
  url = {https://www.usenix.org/conference/usenixsecurity21/presentation/cremers}
}
```

### D 身份绑定 认证关系与密钥确认

### N17 显式密钥确认的理论区分

**完整标题：Key Confirmation in Key Exchange: A Formal Treatment and Implications for TLS 1.3。** 作者 Marc Fischlin、Felix Günther、Benedikt Schmidt、Bogdan Warinschi；IEEE Symposium on Security and Privacy 2016，452–469。

核验依据：[作者公开论文](https://felixguenther.info/publications/SP_FGSW16.pdf)、[作者出版题录](https://www.felixguenther.info/publications.php)、[会议官方摘要](https://www.ieee-security.org/TC/SP2016/program-links.html)。已核查密钥确认与通常机密性/认证目标的区别。部分机构记录使用稍异题名，本条遵循论文和会议程序中的正式标题。

相关性：比仅引用 HMAC 算法更直接地解释为何第3章要增加确认步骤。适用章节：§2.4；§3.3。推荐引用段落：“引入基于 HMAC 的显式密钥确认机制……”及其设计目标之后。边界：其计算定义不是本文 P1 查询的同义词；本文只报告已验证的对应关系，不借该文声称获得全部密钥确认定义或泄露安全保证。

```bibtex
@inproceedings{fischlin2016confirmation,
  author = {Marc Fischlin and Felix G{\"u}nther and Benedikt Schmidt and Bogdan Warinschi},
  title = {Key Confirmation in Key Exchange: A Formal Treatment and Implications for {TLS} 1.3},
  booktitle = {2016 IEEE Symposium on Security and Privacy},
  year = {2016}, pages = {452--469}, publisher = {IEEE},
  doi = {10.1109/SP.2016.34},
  url = {https://felixguenther.info/publications/SP_FGSW16.pdf}
}
```

### N18 身份误绑定的形式化分析

**完整标题：Formal Verification of Misbinding Attacks on Secure Device Pairing and Bootstrapping。** 作者 Aleksi Peltonen、Mohit Sethi、Tuomas Aura；2020；Journal of Information Security and Applications，51，文章号102461。

核验依据：[出版社全文页与摘要](https://www.sciencedirect.com/science/article/pii/S2214212619307215)、[作者单位题录](https://research.aalto.fi/en/publications/formal-verification-of-misbinding-attacks-on-secure-device-pairin/)。已核查身份误绑定、对应关系断言和 ProVerif 的应用范围。

相关性：解释有效密码处理与正确身份关联是不同问题，并提示性质定义需要把身份纳入参数。适用章节：§4.3 身份归属语义；§5.2.3 结果绑定策略。推荐引用段落：区分消息唯一性与身份归属，或讨论真实身份材料可信绑定的局限时。边界：其攻击通常涉及被攻陷的合法参与方和设备配对，不等于本文无泄露的密文重组攻击；不将 BatchReceive 重复参与方直接称为其 misbinding 攻击。只选2020期刊版，作者顺序不沿用其2019会议版。

```bibtex
@article{peltonen2020misbinding,
  author = {Aleksi Peltonen and Mohit Sethi and Tuomas Aura},
  title = {Formal Verification of Misbinding Attacks on Secure Device Pairing and Bootstrapping},
  journal = {Journal of Information Security and Applications},
  year = {2020}, volume = {51}, pages = {102461},
  doi = {10.1016/j.jisa.2020.102461},
  url = {https://www.sciencedirect.com/science/article/pii/S2214212619307215}
}
```

### N19 HMAC 原始设计及安全基础

**完整标题：Keying Hash Functions for Message Authentication。** 作者 Mihir Bellare、Ran Canetti、Hugo Krawczyk；CRYPTO 1996，LNCS 1109，1–15。

核验依据：[Springer题录与摘要](https://link.springer.com/chapter/10.1007/3-540-68697-5_1)、[作者公开全文](https://cseweb.ucsd.edu/~mihir/papers/kmd5.pdf)。已核查 NMAC/HMAC 的构造目的和带前提的安全论证摘要。

相关性：给 §3.3 的 HMAC 原语提供源头引用，避免将通用算法写成本文原创。适用章节：§3.3。推荐引用段落：第一次给出 `tag_A = HMAC(confirm_key(k_A), sid_A)` 的公式前或公式说明句。边界：该论文不证明本文 KDF、`confirm_key`、具体转录本编码或组合协议安全；本文仍用符号模型及无泄露条件解释验证结论，不讨论过时具体散列算法的部署建议。

```bibtex
@inproceedings{bellare1996hmac,
  author = {Mihir Bellare and Ran Canetti and Hugo Krawczyk},
  title = {Keying Hash Functions for Message Authentication},
  booktitle = {Advances in Cryptology -- CRYPTO '96},
  year = {1996}, series = {Lecture Notes in Computer Science},
  volume = {1109}, pages = {1--15}, publisher = {Springer},
  doi = {10.1007/3-540-68697-5_1},
  url = {https://link.springer.com/chapter/10.1007/3-540-68697-5_1}
}
```

### N20 共享密钥与正确身份关联的区别

**完整标题：Unknown Key-Share Attacks on the Station-to-Station (STS) Protocol。** 作者 Simon Blake-Wilson、Alfred Menezes；PKC 1999，LNCS 1560，154–170。

核验依据：[Springer题录与摘要](https://link.springer.com/chapter/10.1007/3-540-49162-7_12)、[作者单位原始报告说明](https://uwaterloo.ca/combinatorics-and-optimization/research-combinatorics-and-optimization/technical-reports/technical-reports-1998)。已核查 STS-MAC 的 unknown key-share 及身份关联问题；主条目使用1999正式会议版，不把1998技术报告再计一篇。

相关性：说明存在正确密钥/MAC 并不自动解决身份关联问题。适用章节：§2.4 认证层次；§4.3.2、§5.2.3。推荐引用段落：讨论结果应关联到哪个参与方时作概念对比。边界：UKS 通常涉及同一密钥的对端身份认知差异，本项目第3章是会话参数/密钥失配，二者不能改名合并；本文第4章也未证明发生 UKS。

```bibtex
@inproceedings{blakewilson1999uks,
  author = {Simon Blake-Wilson and Alfred Menezes},
  title = {Unknown Key-Share Attacks on the Station-to-Station ({STS}) Protocol},
  booktitle = {Public Key Cryptography -- PKC 1999},
  year = {1999}, series = {Lecture Notes in Computer Science},
  volume = {1560}, pages = {154--170}, publisher = {Springer},
  doi = {10.1007/3-540-49162-7_12},
  url = {https://link.springer.com/chapter/10.1007/3-540-49162-7_12}
}
```

### N21 认证 密钥机密性及确认的关系

**完整标题：Authentication in Key-Exchange: Definitions, Relations and Composition。** 作者 Cyprien Delpech de Saint Guilhem、Marc Fischlin、Bogdan Warinschi；IEEE CSF 2020，288–303。

核验依据：[IEEE会议论文](https://conferences.computer.org/sp/pdfs/csf/2020/657200a288.pdf)、[作者ePrint题录与摘要](https://eprint.iacr.org/2019/1203)。已核查 key/entity authentication、implicit/explicit authentication、confirmation 的区分和组合前提。正式出版年2020，不使用ePrint编号中的2019作为会议年。

相关性：为“机密性不等于完整参数对应”“确认和其他认证目标不能互换”提供直接理论背景。适用章节：§2.4；§3.3；§5.5。推荐引用段落：§2.4 首段分层安全目标之后，或 §3.3 对确认机制作用的解释。边界：其计算模型的组合结论需要相应定义和假设；本文不宣称从一条 P1 通过就获得该文全部实体/密钥认证性质。

```bibtex
@inproceedings{delpech2020authentication,
  author = {Cyprien Delpech de Saint Guilhem and Marc Fischlin and Bogdan Warinschi},
  title = {Authentication in Key-Exchange: Definitions, Relations and Composition},
  booktitle = {2020 IEEE 33rd Computer Security Foundations Symposium},
  year = {2020}, pages = {288--303}, publisher = {IEEE},
  doi = {10.1109/CSF49147.2020.00028},
  url = {https://eprint.iacr.org/2019/1203}
}
```

### N22 身份与密钥材料之间的可信绑定

**完整标题：ASICS: Authenticated Key Exchange Security Incorporating Certification Systems。** 作者 Colin Boyd、Cas Cremers、Michèle Feltz、Kenneth G. Paterson、Bertram Poettering、Douglas Stebila；ESORICS 2013，LNCS 8134，381–399。

核验依据：[作者题录、摘要与BibTeX](https://www.douglas.stebila.ca/research/papers/ESORICS-BCFPPS13/)、[Springer出版入口](https://link.springer.com/chapter/10.1007/978-3-642-40203-6_22)。已核查认证系统、恶意密钥注册与传统 AKE 模型范围的摘要。

相关性：§5 使用参与方绑定时，需要区分符号身份标识与现实可信身份材料。适用章节：§5.3 绑定准入机制；§5.5 局限与适用范围。推荐引用段落：介绍 `Bind(E)` 的来源/信任假设，或说明真实身份材料可信绑定尚需进一步研究时。边界：不要求本文新增 CA/证书系统，也不表示本文已验证 ASICS 模型；只是说明身份标签与可信公钥归属不能自动等价。不同时加入其2017期刊扩展版。

```bibtex
@inproceedings{boyd2013asics,
  author = {Colin Boyd and Cas Cremers and Mich{\`e}le Feltz and Kenneth G. Paterson and Bertram Poettering and Douglas Stebila},
  title = {{ASICS}: Authenticated Key Exchange Security Incorporating Certification Systems},
  booktitle = {Computer Security -- ESORICS 2013},
  year = {2013}, series = {Lecture Notes in Computer Science},
  volume = {8134}, pages = {381--399}, publisher = {Springer},
  doi = {10.1007/978-3-642-40203-6_22},
  url = {https://www.douglas.stebila.ca/research/papers/ESORICS-BCFPPS13/}
}
```

### N23 共享状态中的成员及身份一致性

**完整标题：TreeSync: Authenticated Group Management for Messaging Layer Security。** 作者 Théophile Wallez、Jonathan Protzenko、Benjamin Beurdouche、Karthikeyan Bhargavan；USENIX Security 2023，1217–1233。

核验依据：[会议题录、摘要与BibTeX](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez)。已核查群组状态的一致性、完整性和认证，以及 F*/DY* 验证的摘要。

相关性：提供“单独密钥建立组件之外仍需维护身份/共享状态语义”的近邻例子。适用章节：§4.3；§5.2.2 批次构造与准入策略比较。推荐引用段落：将输入准入约束与消息级密码检查区分时，以一句相关工作比较引用。边界：该文不是 BatchReceive 参与方互异的先行定理，不将 MLS 群组成员当成本文批次槽位，也不把 F*/DY* 写成 ProVerif/Tamarin。

```bibtex
@inproceedings{wallez2023treesync,
  author = {Th{\'e}ophile Wallez and Jonathan Protzenko and Benjamin Beurdouche and Karthikeyan Bhargavan},
  title = {{TreeSync}: Authenticated Group Management for Messaging Layer Security},
  booktitle = {32nd USENIX Security Symposium (USENIX Security 23)},
  year = {2023}, pages = {1217--1233}, publisher = {USENIX Association},
  url = {https://www.usenix.org/conference/usenixsecurity23/presentation/wallez}
}
```

## Citation Placement Plan

### 按现稿段落安排引用

下表是后续写作的插入建议，不是本轮已经做出的正文修改。正文引文应紧跟其支持的判断，而不统一堆在段尾或贡献清单中。

| 位置 | 现有或拟新增段落的功能 | 优先文献 | 应避免的表述 |
| --- | --- | --- | --- |
| §0 背景开头 | 安全消息的保密、认证、会话管理目标；后量子 AKE 背景 | N01、N05 | 用2015综述证明2026具体产品现状，或把 TLS 变体等同于异步握手 |
| §0 协议演进研究现状 | X3DH 的后量子替代路线，split-KEM、DVS/环签名与 K-Waay 的位置 | N02、N03、N04、E2、E3 | 笼统称“所有后量子消息协议都已具备同等认证/可否认安全” |
| §0 安全消息形式化研究现状 | 区分计算 AKE 分析、符号验证、计算验证及实现联动 | E4、E5、N12、N14 | 把 E4 误写为 ProVerif 分析，或把 E5 的规范问题写成 Signal 部署漏洞 |
| §0 多会话/组合动机 | 会话层结果未必涵盖会话管理层；组合需要前提 | E1、N13 | 声称已有文献已证明本文 BatchReceive 的具体攻击 |
| §0 方法及本文定位 | 单次核心密码对应关系与状态化批次分别处理 | N07、E6 | 把两类模型的结果拼接成一条联合轨迹 |
| §1.1 split-KEM 首次说明 | 说明原语前史、K-Waay 构造来源 | E2、E3、N02、N04 | 把 split-KEM 源文献当作本文攻击验证日志 |
| §1.2 BatchReceive/互异条件 | 原协议接口、合法输入域和前置条件 | E3，必要时 E2 | 用一般组合论文替代原协议明确写出的条件 |
| §1.3 接收问题与范围 | 握手、后续棘轮及会话管理不是一个层次 | N06、E1 | 暗示本文证明 PCS 或完整消息系统安全 |
| §2.1 首段 | 主动网络攻击者与符号原语假设 | N09 | 从符号模型直接推出实现安全或计算后量子安全 |
| §2.2 首段及查询说明 | applied pi/ProVerif、事件与对应查询 | N07、N08；N12作应用比较 | 用“未能证明”代替“真实反例”，或忽略事件观察点 |
| §2.3 状态与先后关系 | 多集重写、线性状态、轨迹与两槽边界 | E6、N10、N11 | 把工具无界能力当成本项目无界批次结论 |
| §2.4 式(6)/(7)及性质解释 | 非单射/单射对应、认证与机密性分层 | E8、N08、N21 | 把同消息至多接受一次当作不同消息参与方必定互异 |
| §3.2 原因及相关工作比较 | 普通 KEM 分量合法不等于完整消息绑定 | N14、E5 | 未经映射就把本文轨迹称作某文献的同一种攻击 |
| §3.3 HMAC 及确认目标 | 标准 MAC 原语与显式确认的目标分开介绍 | N19、N17、N21 | 声称 HMAC 原创，或 HMAC 能独立阻止所有重放 |
| §3.4 重复接受与条件化影响 | 重复处理属于批次接收发生层次 | E8、E1 可供比较 | 将独立 C_install-v2 见证说成 HMAC-only 轨迹的直接后半段 |
| §3.5 组合加固及边界 | 分层机制与组合条件 | N13、N15 | 没有前提检查就引用组合定理为本文整体背书 |
| §4.3.1 归属关系 | 名称、参与方、会话与槽位的坐标不同 | E7、N18 | 把一般命名唯一性等同于 DistinctPartyPerBatch |
| §4.3.2 输出/接口语义 | 原协议索引规则与潜在语义影响 | E2/E3为直接依据；N20为对比背景 | 声称已经验证 KEY/TEST 混淆或密钥泄露 |
| §4.4 综合分析 | 上层组件如何消费重复输出会影响后果 | E1、N16 | 将其他协议的实际克隆攻击转移到本项目 |
| §5.2.2 / §5.2.3 策略比较 | 准入、成员/身份关系及输出绑定承担不同作用 | N23、N18、N20、E7 | 将相邻群组管理方案说成本文机制的直接前身或证明 |
| §5.3 Bind(E)的信任假设 | 符号绑定与真实身份材料的关系 | N22 | 因标签不同便声称现实参与方可信且互异 |
| §5.5 协同作用及范围 | 组件组合、身份假设和实际绑定局限 | N15、N22、N13 | 宣称已完成端到端实现或计算安全证明 |

### 引用分布建议与数量口径

| 内容层次 | 建议本部分出现的不同书目数 | 一套可执行的选用集合 |
| --- | --- | --- |
| 引言 | 15条记录，含 K-Waay 两个版本，实为14项研究 | N01、N05；N02、N03、N04、E2、E3；E4、E5、N12、N14；E1、N13；N07、E6 |
| 协议背景 | 约5条主要记录 | E2、E3、N02、N04、N06；N03可与引言交叉引用，但不必再次展开 |
| 形式化建模/性质定义 | 5–8条 | E6、E8、N07、N08、N09、N10、N11、N12；同段只选真正需要的基础来源 |
| 认证/身份/安全性质比较 | 约5条核心记录 | E8、N17、N18、N20、N21；跨 §2—§5 分配，不集中堆入一段 |
| 具体机制与相邻状态研究 | 按解释需求分散 | N19用于HMAC；N15用于分层组合；N16用于跨上下文比较；N22用于可信绑定局限；N23用于准入与成员语义比较；E7补齐原有未引文献 |

这些集合允许重复出现，不能把各行数字相加当作全文文献总数。全文去重总量仍为现有8条加新增23条；是否最终全部纳入，取决于作者确认后正文是否确实写到相应比较内容。尤其 N05、N16、N23 属相邻而非直接研究，若后续不展开相应背景，应留作储备而非孤立悬引。不能为了达到数字而增加没有论述落点的引用。

## Introduction Reconstruction Preparation

本节仅列未来引言需要补齐的研究方向和引用依据，不提供替换引言正文。

1. **补齐后量子异步握手的技术脉络。** 从安全消息目标和后量子 AKE 背景转入 split-KEM、Signal-conforming AKE、可否认异步握手，再定位 K-Waay。核心依据 N01—N05、E2/E3。不需要重述每个算法细节，也不在未检验的不同实验之间做性能排名。
2. **补齐安全消息形式化分析的现状，而非只列工具名。** 区分 E4 的计算 AKE 分析、N12 的符号/计算及实现联动、E5 的 PQXDH 规范验证和 N14 的 KEM 绑定性质分析。由此说明本文关注完整参数对应与批次输入域，不把已有研究描述成只研究机密性。
3. **把多会话与组合风险具体化。** E1 是最接近的 session-handling 例子；N13 提供组合前提背景，N06/N15/N16可在正文相关比较中展开。写作缺口是“为什么单次核心模型不足以回答批次接收问题”，不是“证明任何协议一组合就不安全”。
4. **引出消息、会话和参与方三类坐标的区别。** E8、N08、N21 用于安全性质分层；E7、N18、N20、N22用于身份语义及可信绑定的比较。K-Waay 的参与方互异前置条件必须直接引用 E3，不能由这些一般文献推定。
5. **给出方法选择与研究边界。** N07/E6 足以在引言简述工具选择，细节留 §2。明确本文固定两槽准入结论、无泄露确认结果和条件化安装影响分别属于各自模型。文献数量增加不改变这些边界。
6. **贡献段保持项目证据导向。** 本文新攻击、修复结果、Bind(E)准入验证不靠外部引文“证明”；应与前面相关工作形成差别，再报告自身已完成的研究。当前研究方向不需重选，未来重构的是论述和引用链。

“国内外研究现状”不意味着必须填充与主题关系弱的中文论文。本轮确认的一手核心来源主要为国际会议/期刊，没有据此断言国内没有相关工作，也未加入尚未核验的中文题录。若下一轮作者要求专门覆盖国内研究，应另行核验真正涉及后量子消息协议、认证对应或状态化组合的论文，不用泛化的 IoT 轻量认证论文替代。

## Evidence Boundaries and Handoff

- 已完成：现稿8条来源及引用位置审查；23篇候选论文的题录/相关内容核验；BibTeX、落点及主张边界规划。
- 未做且本轮不应做：修改 Word/LaTeX 正文、实际扩充文末文献表、重编号正文引文、自动替换引言、打开 WPS、生成 PDF、修改模型/日志、运行安全实验或 Git commit/push。
- 某些 ACM/完整稿页面直取受限，已使用作者、作者单位或会议正式材料核对；这不等于所有论文全文已经逐页审查。需要精确使用某个定理、算法行号或完整稿特定版本时，下一轮应针对该论述再次定位原文，不凭摘要推导。
- 未发现需要以虚构文献填补的引用主题缺口。真正需要保持的科学边界是：相邻研究不能证明 K-Waay 的部署攻击；两个符号模型不能自动拼接；消息去重不等于身份互异；身份标签比较不自动建立现实可信身份绑定；引用工具方法不等于证明模型到实现的对应。
- 本规划待作者确认后，再决定哪些相关研究段落进入引言，以及最终引用顺序。本轮只新增本 Markdown 文件，论文工作稿及已有研究证据不变。
