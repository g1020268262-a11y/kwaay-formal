# 术语清单

审计日期：2026-10-07。扫描对象为当前中文5份section、4份table、6份notes，英文paper-content、全部section/table，以及三个模型。下表收录82组概念；近义词合并记录。T=工具概念，A=既有学术概念，M=本文模型或分析性表达。分类说明词的来源，不自动证明某个中文译名已形成共识。

正文实际词形与审计扩展候选严格分开；没有逐字命中的概念仍可来自符号定义或用户要求。全部逐行匹配见 [term-scan-index.json](evidence/term-scan-index.json)，检索是子串定位，不能把命中次数当独立概念计数。模型与段落语义已另行人工核对。

| 编号 | English term | 当前中文/当前出现状态 | 类别 | 扫描位置示例 |
| --- | --- | --- | --- | --- |
| T01 | party; protocol principal | 参与方；协议主体 | A | `manuscript/sections/00-abstract.tex:5`；`manuscript/sections/00-abstract.tex:12`；`manuscript/sections/00-abstract.tex:13` |
| T02 | party identity | 参与方身份；参与方坐标 | M | `manuscript/sections/01-introduction.tex:26`；`manuscript/sections/03-security-objective-threat-model.tex:12`；`manuscript/sections/04-formal-modeling.tex:262` |
| T03 | party projection | 参与方投影；身份投影 | M | `manuscript/sections/03-security-objective-threat-model.tex:39`；`manuscript/sections/03-security-objective-threat-model.tex:77`；`manuscript/sections/04-formal-modeling.tex:27` |
| T04 | message identity; message coordinate | 消息坐标 | M | `manuscript/sections/01-introduction.tex:26`；`manuscript/sections/02-batchreceive-identity-problem.tex:119`；`manuscript/sections/02-batchreceive-identity-problem.tex:206` |
| T05 | sender occurrence | 发送发生 | M | `manuscript/sections/01-introduction.tex:22`；`manuscript/sections/03-security-objective-threat-model.tex:31`；`manuscript/sections/04-formal-modeling.tex:51` |
| T06 | sender occurrence coordinate; sid; oid | 发送发生坐标；一次发送发生 | M | `manuscript/sections/01-introduction.tex:8`；`manuscript/sections/01-introduction.tex:13`；`manuscript/sections/02-batchreceive-identity-problem.tex:7` |
| T07 | sender-origin tuple | 发送来源元组；精确元组 | M | `manuscript/sections/03-security-objective-threat-model.tex:68`；`manuscript/sections/04-formal-modeling.tex:204`；`manuscript/sections/04-formal-modeling.tex:256` |
| T08 | exact sender origin | 精确发送来源；精确来源 | M | `manuscript/sections/06-discussion.tex:61`；`manuscript/sections/08-conclusion.tex:3`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:44` |
| T09 | identity coordinate; comparison dimension | 身份坐标；坐标 | M | `manuscript/sections/02-batchreceive-identity-problem.tex:67`；`manuscript/sections/02-batchreceive-identity-problem.tex:92`；`manuscript/sections/03-security-objective-threat-model.tex:100` |
| T10 | tuple component | 分量；坐标 | A | `submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:21`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:60`；`submissions/arocmag/latex-v2/notes/PHASE1_FINAL_PATCH_REPORT.md:25` |
| T11 | batch | 批次；批处理 | M | `manuscript/paper-content.tex:6`；`manuscript/paper-content.tex:7`；`manuscript/paper-content.tex:12` |
| T12 | batch admission | 批处理接纳；接纳 | M | `manuscript/paper-content.tex:12`；`manuscript/sections/02-batchreceive-identity-problem.tex:43`；`manuscript/sections/02-batchreceive-identity-problem.tex:70` |
| T13 | batch composition | 批组成；批次组合 | M | `manuscript/sections/03-security-objective-threat-model.tex:80`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:37`；`submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:16` |
| T14 | receiver context | 接收方上下文；接收上下文 | M | `manuscript/sections/04-formal-modeling.tex:257`；`manuscript/sections/05-formal-analysis.tex:96`；`manuscript/sections/07-related-work.tex:124` |
| T15 | batch context; same-batch scope | 批次上下文；作用域 | M | `manuscript/sections/00-abstract.tex:10`；`manuscript/sections/01-introduction.tex:50`；`manuscript/sections/04-formal-modeling.tex:235` |
| T16 | slot; position | 槽位；位置 | M | `manuscript/sections/00-abstract.tex:4`；`manuscript/sections/00-abstract.tex:17`；`manuscript/sections/00-abstract.tex:18` |
| T17 | entry; candidate tuple | 条目；候选元组 | M | `manuscript/sections/01-introduction.tex:4`；`manuscript/sections/01-introduction.tex:24`；`manuscript/sections/02-batchreceive-identity-problem.tex:70` |
| T18 | trace; execution trace | 迹；执行；执行轨迹；符号迹 | T | `manuscript/paper-content.tex:15`；`manuscript/sections/01-introduction.tex:49`；`manuscript/sections/02-batchreceive-identity-problem.tex:176` |
| T19 | trace semantics | 迹语义 | T | `submissions/arocmag/latex-v2/notes/PHASE1_FINAL_PATCH_REPORT.md:39`；`submissions/arocmag/latex-v2/notes/PHASE1_REWRITE_REPORT.md:32`；`submissions/arocmag/latex-v2/tables/verification-property-semantics.tex:3` |
| T20 | trace property | 迹性质 | T | `submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md:81`；`submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:21`；`submissions/arocmag/latex-v2/sections/04-formal-analysis.tex:30` |
| T21 | all-traces; all traces | 全迹；全迹性质；全迹验证 | T | `manuscript/sections/05-formal-analysis.tex:9`；`manuscript/sections/05-formal-analysis.tex:183`；`manuscript/sections/05-formal-analysis.tex:268` |
| T22 | exists-trace | 存在迹；存在迹性质 | T | `submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:47`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md:38`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md:42` |
| T23 | witness | 见证；机器见证；存在性见证 | M | `manuscript/sections/00-abstract.tex:8`；`manuscript/sections/04-formal-modeling.tex:66`；`manuscript/sections/04-formal-modeling.tex:82` |
| T24 | witness value | 见证值（正文未直接使用） | A | 审计扩展概念；见语义来源（非声称当前稿逐字出现） |
| T25 | witness execution; witness trace | 见证；机器见证 | M | `submissions/arocmag/latex-v2/notes/PHASE1_FINAL_PATCH_REPORT.md:17`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:16`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:19` |
| T26 | same-party/different-message witness | 同一参与方见证；同参与方不同消息见证 | M | `submissions/arocmag/latex-v2/notes/PHASE1_FINAL_PATCH_REPORT.md:17`；`submissions/arocmag/latex-v2/sections/00-abstract.tex:2`；`submissions/arocmag/latex-v2/tables/admission-configurations.tex:11` |
| T27 | counterexample; counterexample trace | 反例；反例轨迹 | A | `manuscript/paper-content.tex:15`；`manuscript/sections/05-formal-analysis.tex:13`；`manuscript/sections/05-formal-analysis.tex:46` |
| T28 | attack trace | 攻击轨迹；完整协议攻击 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:176`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:21`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md:57` |
| T29 | reachability | 可达性；可达执行 | A | `manuscript/sections/04-formal-modeling.tex:72`；`manuscript/sections/04-formal-modeling.tex:245`；`manuscript/sections/05-formal-analysis.tex:160` |
| T30 | correspondence | 对应；对应关系 | A | `manuscript/sections/01-introduction.tex:28`；`manuscript/sections/03-security-objective-threat-model.tex:107`；`manuscript/sections/04-formal-modeling.tex:73` |
| T31 | origin correspondence | 精确来源对应；来源对应 | M | `manuscript/sections/04-formal-modeling.tex:249`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:53`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:61` |
| T32 | injectivity | 注入性；认证注入性 | A | `manuscript/sections/00-abstract.tex:11`；`manuscript/sections/00-abstract.tex:15`；`manuscript/sections/01-introduction.tex:52` |
| T33 | occurrence injectivity; scoped occurrence injectivity | 作用域内发生注入性；发生注入性 | M | `manuscript/sections/00-abstract.tex:11`；`manuscript/sections/00-abstract.tex:15`；`manuscript/sections/04-formal-modeling.tex:253` |
| T34 | injective agreement | 单射一致性（待审计术语） | A | `manuscript/sections/07-related-work.tex:112`；`manuscript/sections/07-related-work.tex:113`；`manuscript/sections/07-related-work.tex:114` |
| T35 | distinct-party condition; different-party condition | 不同参与方条件 | M | `manuscript/sections/02-batchreceive-identity-problem.tex:47`；`manuscript/sections/02-batchreceive-identity-problem.tex:163`；`manuscript/sections/02-batchreceive-identity-problem.tex:197` |
| T36 | party distinction | 参与方区分 | M | `manuscript/sections/00-abstract.tex:16`；`manuscript/sections/01-introduction.tex:37`；`manuscript/sections/01-introduction.tex:54` |
| T37 | message distinction | 消息区分 | M | `manuscript/sections/00-abstract.tex:15`；`manuscript/sections/01-introduction.tex:51`；`manuscript/sections/01-introduction.tex:56` |
| T38 | positive control | 正控制 | M | `manuscript/sections/01-introduction.tex:42`；`manuscript/sections/02-batchreceive-identity-problem.tex:210`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:52` |
| T39 | relaxed admission | 放宽配置；放宽 | M | `manuscript/sections/00-abstract.tex:5`；`manuscript/sections/00-abstract.tex:8`；`manuscript/sections/01-introduction.tex:38` |
| T40 | message-level restriction; message-level configuration | 消息级限制；消息级配置 | M | `manuscript/sections/00-abstract.tex:5`；`manuscript/sections/01-introduction.tex:36`；`manuscript/sections/04-formal-modeling.tex:86` |
| T41 | party-level admission; party-level configuration | 参与方级配置；参与方级正控制 | M | `manuscript/sections/00-abstract.tex:12`；`manuscript/sections/01-introduction.tex:39`；`manuscript/sections/01-introduction.tex:53` |
| T42 | controlled comparison | 受控比较；受控配置 | M | `manuscript/sections/00-abstract.tex:4`；`manuscript/sections/02-batchreceive-identity-problem.tex:211`；`manuscript/sections/05-formal-analysis.tex:217` |
| T43 | fact | 事实；来源事实 | T | `manuscript/sections/04-formal-modeling.tex:53`；`manuscript/sections/04-formal-modeling.tex:61`；`manuscript/sections/04-formal-modeling.tex:71` |
| T44 | action fact | 动作事实；动作 | T | `manuscript/sections/04-formal-modeling.tex:71`；`manuscript/sections/04-formal-modeling.tex:72`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:44` |
| T45 | persistent fact | 持久事实；持久来源事实 | T | `submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md:33`；`submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:21`；`submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:25` |
| T46 | linear fact; state fact | 线性槽位；收集状态 | T | `manuscript/sections/04-formal-modeling.tex:242`；`submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:23`；`submissions/arocmag/latex-v2/tables/identity-coordinate-map.tex:13` |
| T47 | multiset rewriting | 多集重写 | T | `submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:21` |
| T48 | rule; rule-level semantics | 规则；规则层；规则语义 | T | `manuscript/sections/02-batchreceive-identity-problem.tex:96`；`manuscript/sections/02-batchreceive-identity-problem.tex:98`；`manuscript/sections/02-batchreceive-identity-problem.tex:111` |
| T49 | restriction | 不等式约束；限制 | T | `manuscript/sections/00-abstract.tex:5`；`manuscript/sections/01-introduction.tex:17`；`manuscript/sections/01-introduction.tex:36` |
| T50 | guard; admission condition | 接纳条件；约束 | M | `manuscript/sections/01-introduction.tex:40`；`manuscript/sections/04-formal-modeling.tex:90`；`manuscript/sections/04-formal-modeling.tex:107` |
| T51 | lemma | lemma；性质；引理 | T | `manuscript/sections/05-formal-analysis.tex:16`；`manuscript/sections/05-formal-analysis.tex:19`；`manuscript/sections/05-formal-analysis.tex:40` |
| T52 | fresh name; fresh value | 新鲜；新鲜坐标 | T | `submissions/arocmag/latex-v2/sections/03-formal-modeling.tex:21` |
| T53 | timepoint; event occurrence | 时间条件；事件发生；接受发生数 | T | `manuscript/sections/04-formal-modeling.tex:159`；`manuscript/sections/05-formal-analysis.tex:25`；`submissions/arocmag/latex-v2/notes/PHASE1_REWRITE_REPORT.md:47` |
| T54 | Send; send event | Send动作；发送事件 | M | `manuscript/sections/00-abstract.tex:6`；`manuscript/sections/00-abstract.tex:9`；`manuscript/sections/01-introduction.tex:3` |
| T55 | ReceiverAccept; acceptance event | 接收事件；接受事件；ReceiverAccept | M | `manuscript/sections/01-introduction.tex:50`；`manuscript/sections/03-security-objective-threat-model.tex:106`；`manuscript/sections/03-security-objective-threat-model.tex:108` |
| T56 | BatchReceive action | BatchReceive动作；批次接纳 | M | `submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:29`；`submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md:71`；`submissions/arocmag/latex-v2/sections/02-problem.tex:14` |
| T57 | rejection branch; rejection reachability | 拒绝分支；拒绝见证 | M | `manuscript/sections/04-formal-modeling.tex:90`；`manuscript/sections/04-formal-modeling.tex:107`；`manuscript/sections/04-formal-modeling.tex:110` |
| T58 | non-vacuity; vacuous truth | 非真空性；真空成立 | M | `manuscript/sections/04-formal-modeling.tex:227`；`manuscript/sections/05-formal-analysis.tex:18`；`manuscript/sections/05-formal-analysis.tex:199` |
| T59 | refinement; refinement theorem | refinement；refinement theorem | A | `manuscript/sections/00-abstract.tex:19`；`manuscript/sections/01-introduction.tex:65`；`manuscript/sections/04-formal-modeling.tex:65` |
| T60 | symbolic model; symbolic abstraction | 符号模型；两槽抽象 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:83`；`manuscript/sections/02-batchreceive-identity-problem.tex:201`；`manuscript/sections/02-batchreceive-identity-problem.tex:221` |
| T61 | Dolev–Yao adversary; attacker | 攻击者；对手；敌手 | A | `manuscript/sections/01-introduction.tex:61`；`manuscript/sections/02-batchreceive-identity-problem.tex:220`；`manuscript/sections/03-security-objective-threat-model.tex:55` |
| T62 | replay; repeated acceptance | 重放；重复接受 | A | `manuscript/sections/01-introduction.tex:23`；`manuscript/sections/03-security-objective-threat-model.tex:60`；`manuscript/sections/06-discussion.tex:36` |
| T63 | authentication; secrecy | 认证；保密性；密钥安全 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:138`；`manuscript/sections/03-security-objective-threat-model.tex:34`；`manuscript/sections/03-security-objective-threat-model.tex:118` |
| T64 | authenticated key exchange; deniable | 认证密钥交换；可否认 | A | `manuscript/sections/01-introduction.tex:11`；`manuscript/sections/02-batchreceive-identity-problem.tex:3`；`manuscript/sections/07-related-work.tex:12` |
| T65 | KEM; split-KEM; prekey bundle | KEM；split-KEM；预密钥束 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:4`；`manuscript/sections/02-batchreceive-identity-problem.tex:11`；`manuscript/sections/02-batchreceive-identity-problem.tex:25` |
| T66 | transcript; session identifier; wire representation | transcript；session标识；线路编码 | A | `manuscript/sections/00-abstract.tex:22`；`manuscript/sections/01-introduction.tex:69`；`manuscript/sections/02-batchreceive-identity-problem.tex:80` |
| T67 | non-implication; non-substitutability | 非蕴含；非替代性 | M | `manuscript/sections/02-batchreceive-identity-problem.tex:166`；`manuscript/sections/04-formal-modeling.tex:191`；`manuscript/sections/06-discussion.tex:63` |
| T68 | verified; falsified; proof steps | 已验证；被反例否定；证明步数 | T | `manuscript/sections/05-formal-analysis.tex:17`；`manuscript/sections/05-formal-analysis.tex:23`；`manuscript/sections/05-formal-analysis.tex:57` |
| T69 | bounded abstraction; arbitrary batch sizes | 固定两槽；任意批长 | M | `manuscript/sections/01-introduction.tex:67`；`manuscript/sections/03-security-objective-threat-model.tex:47`；`manuscript/sections/04-formal-modeling.tex:83` |
| T70 | matching origin; idealized origin relation | 来源匹配；精确来源关系 | M | `manuscript/sections/04-formal-modeling.tex:61`；`submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md:46`；`submissions/arocmag/latex-v2/sections/01-introduction.tex:9` |
| T71 | sequential processing; common lifecycle | 顺序处理；共同生命周期；共同骨架 | M | `manuscript/sections/00-abstract.tex:6`；`manuscript/sections/01-introduction.tex:40`；`manuscript/sections/05-formal-analysis.tex:244` |
| T72 | scope; global uniqueness | 作用域；全局唯一性 | A | `manuscript/sections/00-abstract.tex:11`；`manuscript/sections/01-introduction.tex:51`；`manuscript/sections/01-introduction.tex:56` |
| T73 | aliveness; liveness | liveness；存活性 | A | `manuscript/sections/05-formal-analysis.tex:90`；`manuscript/sections/07-related-work.tex:113`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:40` |
| T74 | supporting property; key result | 支持性质；核心结果 | M | `manuscript/sections/02-batchreceive-identity-problem.tex:30`；`manuscript/sections/02-batchreceive-identity-problem.tex:41`；`submissions/arocmag/latex-v2/notes/PHASE1_REWRITE_REPORT.md:26` |
| T75 | source-to-abstraction mapping | 来源到抽象映射；模型映射 | M | `manuscript/sections/01-introduction.tex:64`；`manuscript/sections/04-formal-modeling.tex:33`；`submissions/arocmag/latex-v2/notes/PHASE1_REWRITE_REPORT.md:30` |
| T76 | composition boundary; cryptographic component | 组合边界；密码组件 | M | `manuscript/sections/00-abstract.tex:17`；`manuscript/sections/03-security-objective-threat-model.tex:55`；`manuscript/sections/07-related-work.tex:60` |
| T77 | receiver ephemeral state | 接收方临时状态；共享状态 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:13`；`submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md:17`；`submissions/arocmag/latex-v2/sections/02-problem.tex:4` |
| T78 | unknown key-share; misbinding | UKS；misbinding（notes边界） | A | `manuscript/sections/07-related-work.tex:79`；`manuscript/sections/07-related-work.tex:99`；`manuscript/sections/07-related-work.tex:100` |
| T79 | implementation; deployment | 实现；部署缺陷 | A | `manuscript/sections/02-batchreceive-identity-problem.tex:60`；`manuscript/sections/02-batchreceive-identity-problem.tex:63`；`manuscript/sections/02-batchreceive-identity-problem.tex:85` |
| T80 | reachability sanity check | 正常路径；非真空性支持 | M | `submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md:15`；`submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md:50`；`submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md:71` |
| T81 | one-send/two-accepts witness | 一个精确来源支持两个同批接受 | M | `submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md:38`；`submissions/arocmag/latex-v2/tables/key-verification-results.tex:10` |
| T82 | valid distinct-party batch | 有效不同参与方批次 | M | `manuscript/sections/00-abstract.tex:14`；`manuscript/sections/01-introduction.tex:55`；`manuscript/sections/05-formal-analysis.tex:229` |

## 完整输入清单

| 路径 | 行数 | SHA-256 |
| --- | --- | --- |
| manuscript/paper-content.tex | 30 | d8b4b12f70fbdefd01d010b791a8362a9cdec3598e8c80cf0537f826506be0bc |
| manuscript/sections/00-abstract.tex | 23 | 3b31b7fd6f13881ee22179ec29f5c72ffe15a1e3abe2dd1d173ae6b7fb591aa1 |
| manuscript/sections/01-introduction.tex | 75 | 7e6fe85a47d4f41a2e10d50e4e071743d06ee4c9c615afa4ae8c59d45aed1874 |
| manuscript/sections/02-batchreceive-identity-problem.tex | 221 | f1b97047676756171a879572eb82cfe3206392714c4fde8fb4b50880b1981a4f |
| manuscript/sections/03-security-objective-threat-model.tex | 126 | 9787c36e60f54d809668e945dc851f7dbcfb31bad7b3daed39d6be78c0e9e69f |
| manuscript/sections/04-formal-modeling.tex | 263 | 0be0ac16c256b9da227f2d85a23acaa82a4d8b1d38b37db770fb0b9d7fceb2f4 |
| manuscript/sections/05-formal-analysis.tex | 298 | e1522ca0387391edac4b4b7caeb36a18a70a7059c4f2103150b6a7e1886b4e39 |
| manuscript/sections/06-discussion.tex | 224 | 30baae5a5c9998c9815a2efd80c7cc209e659cefe4460ddf2f2fc06bfa515e2d |
| manuscript/sections/07-related-work.tex | 170 | 0856a97b6ee0547a47c17c69238a916a21660f2a42fb295ae57a7da9b9b5664a |
| manuscript/sections/08-conclusion.tex | 18 | e6f0c1e487309f975dfd1ab3995b836f00ffc609bdec362cfd8984b80ce29fad |
| manuscript/tables/model-comparison.tex | 15 | b3345836778a3f98f2d3768bc275f6ce96421ca6ef28b34b78decae05c402741 |
| manuscript/tables/verification-results.tex | 30 | 980743e4ff509c42a947182320d703fee08b901be866b58a3a7578bc8d02397f |
| submissions/arocmag/latex-v2/notes/LANGUAGE_QA.md | 70 | 8118dffe630f40174b51fae07ecae64d0acca4c6db99c977a3ede5f6fdc4203a |
| submissions/arocmag/latex-v2/notes/PHASE1_FINAL_PATCH_REPORT.md | 69 | dcec4cebd85e9c6d5216e2b9f642fd89c2ace49ce2da5c09d88ea1026b182183 |
| submissions/arocmag/latex-v2/notes/PHASE1_REWRITE_REPORT.md | 91 | ddcb1e393f4fcf07d37fcadf75117efb92a7aa50ef14385e629bd90de3ca4a79 |
| submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_QA.md | 67 | e61bc93a3cc79dcf0cdb404622f9886d5aac06e88a2ecef20ff6c0bb25e18160 |
| submissions/arocmag/latex-v2/notes/PHASE2A_RESULTS_REPORT.md | 111 | 33d4c1396f1a4eec225db67b681026faf80d73fc591e47b363cdcbf5e52e48de |
| submissions/arocmag/latex-v2/notes/SOURCE_MAPPING.md | 98 | 840494f272c003e95aed7e53908ddf9e13591f2c69dc871bd5b7d0af64851f80 |
| submissions/arocmag/latex-v2/sections/00-abstract.tex | 31 | b64047a90695827c6e1d430c316807c3dcf194278b90aa8582dbc12fea51c5d1 |
| submissions/arocmag/latex-v2/sections/01-introduction.tex | 17 | f83d767a6c1aedddf13a267fd7c2e9e32385ef85675a5346397571c67964d42e |
| submissions/arocmag/latex-v2/sections/02-problem.tex | 43 | 517e59c43778fc12c6eddb0e05a4b1f86702c2239e133f824dab225fb419e7f6 |
| submissions/arocmag/latex-v2/sections/03-formal-modeling.tex | 55 | 30282a62b8d48f00b1e8495e77f3495c103e564579ff1fff8132796222414cbb |
| submissions/arocmag/latex-v2/sections/04-formal-analysis.tex | 92 | 02e3bbb0238f5b4de1f3d9c86c47d4286a4004e7cd025dcfc1d61f05ce99d2d9 |
| submissions/arocmag/latex-v2/tables/admission-configurations.tex | 16 | ca952c3581d40997bf66e1897921f61d4927be4bcfd2cb663a9add89b7b0bad0 |
| submissions/arocmag/latex-v2/tables/identity-coordinate-map.tex | 18 | 184ddc4b0ec6d7888fac44b76dc838f37b1b1da191aa6ef097361308d33e52b2 |
| submissions/arocmag/latex-v2/tables/key-verification-results.tex | 32 | 8b9ecd8c158874a10e79d3953d0e596165c9c97fe44959a813aa1a0dab6a4f8f |
| submissions/arocmag/latex-v2/tables/verification-property-semantics.tex | 27 | da57f8a63b9a45c7741eedf685b21f65c20a325a153284fc587f519f576ef4c6 |
| tamarin/rq-v2-minimal/rqv2_message_dedup.spthy | 130 | 90a196f5da5c244026596283d001376427880cd64c5bea3c6cfdfd4ccba99184 |
| tamarin/rq-v2-minimal/rqv2_party_admission.spthy | 133 | c35af64cac7f01182418cb999ea105214b8da4f2295b670a9b3733f0bd976bba |
| tamarin/rq-v2-minimal/rqv2_relaxed.spthy | 111 | e5129575720020aa3f509782c2052fbf2114a540d013126f5a75d316cbabaf9d |
