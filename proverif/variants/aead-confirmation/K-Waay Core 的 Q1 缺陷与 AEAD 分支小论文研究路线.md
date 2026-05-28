# K-Waay Core 的 Q1 缺陷与 AEAD 分支小论文研究路线

## 研究问题的精确定义

K-Waay 的公开论文把其核心描述为一种基于 split-KEM 的、X3DH-like 的 deniable authenticated key exchange：协议的发送方生成三段核心封装密文，接收方解封装后与 `sid` 一起经 `KDF` 导出会话密钥；论文证明的主线性质是 KIND（key indistinguishability）和 deniability，而 Figure 7 的核心流程本身是围绕 `m=(ctℓ,ctk,cts)`、`sid` 和 `k=KDF(...)` 展开的。与此同时，ProVerif 正好擅长把“保密性”和“事件对应/认证性”拆开验证：它能分别证明 secrecy 与 correspondence，并在性质失败时重构反例轨迹。citeturn1view0turn14view0turn11view0

你现在最适合写成的，不是“大而全”的 K-Waay 全协议安全论文，而是一篇**聚焦 receiver-side acceptance gap 的 attack-and-fix case study**。最稳妥的研究问题可以压缩成三条：第一，`proverif/kwaay-core-public-channel.pv` 这个 public-channel baseline，是否满足“接收方一旦接受 `(A,B,sid,k)`，发送方就确实完成过匹配会话”的 Q1 correspondence；第二，如果 Q1 不成立，是否能用一个**最小化的、sid-bound 的 authenticated confirmation layer** 修复它；第三，这个修复是否能在不破坏 baseline secrecy-oriented 结论的前提下完成。这样写，与 ProVerif 的能力、K-Waay Figure 7 的结构，以及现代协议分析中“先发现缺口，再给最小修复”的写法是对齐的。citeturn11view0turn17view0turn19view0turn22view0

可以把论文的核心命题写成一句非常直白的话：**“在 public-channel symbolic model 中，K-Waay core 可以保持 baseline secrecy 结果，但不能保证 receiver-to-sender exact matching completion；一个 sid-bound authenticated confirmation tag 能把这个 receiver-side acceptance gap 从 false 变成 true。”** 这句话的好处是，它既不把问题夸大成 key recovery，又把你真正发现的缺陷和修复点钉死在 `RecvDone`/`SendDone` 的对应关系上。Lowe 在讨论认证层次时特别提醒过，如果协议设计者不把“认证到底指什么”说清楚，使用者就会错误地以为协议满足更强的性质；你的论文正好可以把这个“更强的性质”具体化为 Q1。citeturn33view0turn31view0

**A. 建议写进论文导言中的研究问题**可以直接表述为：

1. 原始 K-Waay core 是否在 active public-channel attacker 下满足接收方到发送方的 matching-session agreement，即  
   `event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))`？
2. 若不满足，攻击者究竟是如何在**不必恢复会话密钥**的前提下，让接收端进入 bogus accepted session 的？
3. 一个保持异步结构的、sender-to-receiver 的 sid-bound confirmation tag，能否恢复这一性质，并保持 baseline secrecy-oriented 查询不变？

## 攻击者模型与 baseline 缺陷的边界

你这篇短论文最适合使用的是**标准的 Dolev–Yao active network attacker**。Dolev 和 Yao 的原始表述非常直接：攻击者可以得到所有经过网络的消息、可以作为网络中的合法用户主动发起会话、也可以成为收信方；Lowe 在认证层次论文里也把攻击者建模为“完全控制通信网络，可以拦截并注入新消息的人”。对 ProVerif 来说，这个假设与“`free c: channel` 是公开信道、公开信道输出会被攻击者得到、free names 默认攻击者已知”完全一致。也就是说，你的 `public-channel` baseline 天然就是一个强主动攻击者模型，而不是温和 attacker。citeturn27view1turn33view0turn13view0turn17view0

在这个模型里，主攻击者能力应该写得非常实：他可以窃听、拦截、删除、重放、延迟、重排和注入消息；对你这类核心消息 `mCore=(ctL,ctE,ctS)` 的模型来说，还要明确写出“攻击者可以替换其中一段或多段 ciphertext，或者把不同会话里合法出现过的片段重新拼接”，但**不能**凭空打破 KEM、KDF 或认证原语的黑盒安全。这样定义以后，你的攻击目标就不是 `attacker(k)`，而是：在攻击者不知道 honest long-term secret 的情况下，是否仍能诱导 `RecvDone(B,A,s,k)` 出现而没有匹配的 `SendDone(A,B,s,k)`。这正是 correspondence 风格缺陷，而不是 secrecy 缺陷。citeturn27view1turn11view0turn29view0

这里有一个非常重要、论文里必须提前交代的前提：**事件语义必须是“对的”**。ProVerif 手册明确说过，事件本身不改变攻击者知识，但事件放在哪里会改变你在证明什么；把 before-arrow 的事件往前放、把 after-arrow 的事件往后放，都会强化对应性质。因此，在论文中要明确宣布：`SendDone` 表示发送方已经完成核心发送并输出网络消息；`RecvDone` 表示接收方已经把该会话当作“正式接受”的会话。只要这两点写清楚，Q1 为 false 就不是“事件乱放造成的假阳性”，而是你模型里真实的 receiver-side agreement 缺口。citeturn28view0turn12view0

**B. 对这篇小论文最合适的攻击者模型**可以分成“主线”和“扩展线”两层来写。主线只做 uncompromised active network attacker：不允许长期密钥泄露，不允许 session-state reveal，只允许完全控制公共信道。这样最容易迅速出结果。扩展线作为 future work 再提：K-Waay 的 KIND 模型本身还考虑了 `REGISTER`、`STATE`、`KEY` 等 oracle；而且作者明确指出，在允许 session-state exposure 的模型下，若攻击者学到接收方的临时状态，确实可能伪造被接收方接受的消息。换言之，你的 AEAD 分支第一版不要碰 compromise model；碰了后，故事会从“网络篡改”升级为“状态泄露”，会显著拉长战线。citeturn3view0turn15view0

**C. baseline 中 Q1=false 应如何解释成安全缺陷而不是 key recovery**，建议用最稳的表述：  
Q1 的失败，严格按 ProVerif 语义，就是“存在一个轨迹，接收方到达了你定义为 `RecvDone` 的正式接受点，但不存在带相同参数 `(A,B,s,k)` 的先前 `SendDone`。” 这说明失败的是**receiver-to-sender agreement on exact session data**。按照 Lowe 的层次，agreement 的强弱取决于双方是否在同一数据上匹配；你的 Q1 匹配的是 `(A,B,sid,k)`，而 Figure 7 里的 `sid` 又显式绑定了双方标识、公钥/预密钥和消息 `m`，因此这明显强于“只证明对方活着”或“只证明对方曾经跑过协议”的弱认证目标。citeturn28view0turn23view0turn14view0

这类失败**不是** key recovery。ProVerif 手册把 secrecy 查询和 correspondence 查询严格区分开：前者问 `attacker(M)`，后者问“某接受事件是否有匹配的先前事件”；K-Waay 论文自己的主定理也证明的是 KIND 和 deniability，而不是你这个 Q1。换句话说，你可以而且应该在文中同时写出两句话：  
一方面，“baseline secrecy-oriented queries 仍可成立，所以这不是 ‘攻击者得到会话密钥’ 的结论”；另一方面，“NIST 对 key confirmation 的定义恰恰是：让一方确信另一方确实拥有相同的 secret/shared secret，而 Q1=false 正说明这种 assurance 在 receiver acceptance 处缺席。” 这依然是安全缺陷，只是缺陷位于认证/确认层，而不是保密层。citeturn29view0turn14view0turn31view0

这不是一个只在学术定义里才重要的“洁癖式”问题。5G AKA 的大型形式化分析就把“缺少 key confirmation”明确当作 weakness 来批评：作者指出，一些 intended security guarantees 只有在额外 key-confirmation roundtrip 之后才成立，并进一步讨论了“missing key confirmation”的危险，还给出两类修复——要么把 challenge 本身做更强的绑定，要么加一个**更便宜的单向 key confirmation**。这与你的 AEAD 分支几乎是同一类思想：问题不是“密钥一定泄露”，而是“接收方在缺少对方 possession evidence 时就接受了会话”。citeturn23view0turn30view0turn18view0

## 把 ProVerif 反例写成协议攻击

ProVerif 的一个关键价值，在于它不只给出 `false`，还会在性质失败时尽量重构反例轨迹；手册甚至专门建议看更详细的 trace 输出，并说明 `set traceDisplay = long` 可以得到更适合人工解读的长轨迹。对你的论文来说，这意味着最重要的不是把 `.out` 文件原样贴出来，而是把它**翻译成协议语言**：谁先发、谁被拦、哪一段被换、哪个事件首先“坏了”。citeturn11view0turn28view0

最适合写进正文的 trace 翻译模板，是一个六步式的攻击叙述。先固定一个 honest sender run `S_A` 和一个 honest receiver run `R_B`；然后说明攻击者在公开信道上观察到哪个合法的 `mCore=(ctL,ctE,ctS)`；接着指出它究竟是**替换**了 `ctL/ctE/ctS` 中的哪一项，还是**重放/重组**了此前出现过的片段；再写出 `R_B` 因此计算出不同的 `sid'` 和 `k'`；然后指出 `R_B` 在 baseline 中直接触发了 `RecvDone(B,A,sid',k')`；最后强调不存在匹配的 `SendDone(A,B,sid',k')`，所以攻击者成功制造了一个 **unpartnered receiver session**。这种写法非常接近 Lowe 的经典“发现认证攻击—解释攻击流程—给出修复”的模式，也与现代符号分析论文把工具反例翻译为协议攻击流程的做法一致。citeturn32view0turn19view1

正文中最实用的写法，通常不是直接写“攻击者修改了 `ctE`”，而是写得更稳一点：  
“在 ProVerif 生成的 counterexample 中，攻击者通过对核心 KEM transcript 的主动干预——具体为对 `ctL`、`ctE`、`ctS` 之一的替换或重组——使得接收方在本地导出 `(sid',k')`，并在不存在匹配发送方完成事件的情况下执行 `RecvDone`。”  
等你拿到实际 trace 后，再把“之一”换成真实位置即可。这样写的好处是：在没 final trace 之前，不会预设错误细节；拿到 trace 后，只需把一句话具体化。citeturn11view0turn28view0

论文里还应该单独写一句“这条攻击**不等于** `attacker(k')`”。因为 secrecy 和 correspondence 在 ProVerif 中是两类不同结果，读者很容易把“接收端错误接受”脑补成“密钥已泄露”。最稳的写法是：  
“该攻击证明的是 receiver acceptance semantics failure，而不是 session-key recovery. 攻击者的能力是诱导 B 安装一个没有发送方匹配完成的会话状态。”  
这样既准确，也能和后文“AEAD 分支只修复 agreement，不宣称提升所有性质”自然连起来。citeturn29view0turn31view0

## AEAD 分支的形式化定位与要验证的 query

你的 AEAD 分支设计，从研究叙事上看，最应该被称为 **sid-bound authenticated confirmation layer**，而不是“一条完整的新数据通道”。理由有两个。第一，K-Waay Figure 7 原本就是先从三段核心密文得到 `m`、再把 `sid` 绑定到双方身份、公钥、prekey 和消息、然后用 `KDF` 导出 `k`；你的分支只是在这个结构外侧追加一个 sender-to-receiver 的确认标签，因此最忠于原始思路的写法，仍然是“先 `mCore`，再 `sid`，再 `k`，最后 `kc`”。第二，NIST 的 key confirmation 定义与 TLS 1.3 的 `Finished` 都表明：这里真正需要的是“证明对方持有相同 secret”的认证值，而不必在模型中额外引入应用层 payload 的保密性。TLS 1.3 就明确把 `Finished` 描述成对整个握手的 MAC，它提供 key confirmation、身份与已交换密钥的绑定以及握手完整性。citeturn14view0turn31view0turn8view1turn8view3

因此，论文中最顺的形式化描述就是：保留原始核心 transcript 为  
`mCore = core_msg(ctL, ctE, ctS)`；  
按原始逻辑计算  
`sid = sid_of(A,B,pkA,pkB,prekeys,mCore)` 和 `k = kdf(KL,KE,KS,sid)`；  
然后只额外加入  
`kc = aead_tag(k,sid)`；  
最终网络上发送  
`confirmed_msg(mCore,kc)`。  
这样做的研究价值在于：它既保留了 Figure 7 中 `sid` 绑定 core transcript 的结构，又把一个与 `(sid,k)` 绑定的确认标签挂在外面，最小化地改变了协议。citeturn14view0turn4view0

这里还可以加一句设计理由，专门化解“为什么不用双向 challenge-response”的问题：K-Waay/X3DH-like 协议的重要特点是异步，发送方在拿到接收方的预密钥材料后就应能立刻导出密钥并发出初始消息，而 `Init` 还刻意要求其输出只依赖本方公钥材料，以保持 receiver obliviousness。为避免破坏这种异步结构，你的修复不应要求接收方必须先在线发 challenge 再由发送方响应；把单向 confirmation piggyback 在首条消息里，才与 K-Waay 的设计精神一致。5G AKA 的形式化分析也给出了非常相似的结论：完整 roundtrip key confirmation 不是唯一选项，**较便宜的单向 key confirmation** 就足以恢复所需保证。citeturn1view0turn3view0turn30view0

接下来是 query 集的选择。对一篇要“尽快出成绩”的小论文，最推荐的是**四个核心查询加两个 reachability 诊断**。第一组必须保留 baseline 里原有的 secrecy-oriented 查询，用来证明你没有把话题偷换成“修复 agreement 的同时破坏 secrecy”；第二个就是主角 Q1：  
`event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))`。  
AEAD 分支里再加两个辅助 correspondence：  
`event(RecvDone(B,A,s,k)) ==> event(AeadConfirmed(B,A,s,k))`，  
以及  
`event(AeadConfirmed(B,A,s,k)) ==> event(SendDone(A,B,s,k))`。  
这样一来，Q1 修不修得好，你能一眼看出；如果没修好，也能快速定位是“接收端没真正被确认门控”，还是“确认 tag 没有绑定到正确的 `(sid,k)`”。ProVerif 手册明确支持这类由事件构成的 basic correspondence 与更复杂的 conjunction/disjunction 查询。citeturn29view0

除了这四个核心查询，再补两个 reachability/调试查询就够了：一个检查 `RecvComputed` 在 honest run 下是可达的，另一个检查 `AeadConfirmed` 在 honest run 下也是可达的。这样你能区分“AEAD 分支把 honest execution 也堵死了”和“AEAD 分支只把攻击轨迹堵死了”这两种完全不同的问题。ProVerif 手册专门建议把 event-reachability 当作 debug 工具，用于检查某条分支或某个事件是否根本不可达。citeturn29view0

还有一个边界必须在文中主动写出来：**这条 AEAD 分支修的是 uncompromised active-network attacker，下不覆盖 state exposure。** K-Waay 自己的论文已经写得很清楚：在允许接收方 ephemeral state 暴露的模型里，攻击者可能伪造被接收方接受的消息。你的 `aead_tag(k,sid)` 与 `aead_verify(k,sid,kc)` 也是基于同一个 `k` 在工作；如果攻击者已经拿到这个层面的状态或派生密钥材料，那么 tag 本身也会失去意义。所以第一版论文不要声称修复了所有 compromise setting，下阶段再考虑 `STATE` oracle 场景。citeturn15view0turn3view0

## 实验组织与最短产出路径

你这篇文章的实验组织，最适合做成一张**性质对照表**和一张**模型差异表**。前者只写 query 和结果，后者只写 baseline 与 AEAD 的设计差别。这样读者能迅速抓到“问题是什么、改了什么、结果如何”。ProVerif 能同时给出 secrecy、correspondence 和 reachability 结果，而且失败时会附反例轨迹；这一点正适合做成“baseline false / AEAD true”的对照。citeturn11view0turn29view0

建议你的主结果表直接写成这样的结构：

| 目标 | baseline | AEAD 分支 | 论文中的解释 |
|---|---|---|---|
| 原有 secrecy-oriented queries | 保留当前结果 | 目标是保持不变 | 说明问题不是 key recovery |
| `RecvDone ==> SendDone` | false | 目标是 true | baseline 存在 unpartnered receiver session |
| `RecvDone ==> AeadConfirmed` | 不适用 | 目标是 true | 接收端接受被 AEAD 验证门控 |
| `AeadConfirmed ==> SendDone` | 不适用 | 目标是 true | tag 确认了 sender 对 `(sid,k)` 的 possession |
| `event(RecvComputed(...))` 可达 | 可达 | 可达 | 攻击前后 honest run 仍然活着 |
| `event(AeadConfirmed(...))` 可达 | 不适用 | 可达 | AEAD 分支不是死分支 |

然后再配一张“模型差异表”：

| 方面 | baseline | AEAD 分支 |
|---|---|---|
| 网络消息 | `m=(ctL,ctE,ctS)` | `confirmed_msg(mCore,kc)` |
| `sid_of` 输入 | 核心消息 | 仍是核心消息 `mCore` |
| 接收端接受条件 | 解封装 + `kdf` | 解封装 + `kdf` + `aead_verify` |
| 接受事件位置 | `RecvDone` 在接收端本地导钥后 | `RecvDone` 在 `AeadConfirmed` 之后 |
| 预期反例 | Q1 攻击 trace | tampered trace 在 `AeadVerify` 处被阻断 |

为了尽快出成绩，工作流建议压成四步。第一步，冻结 baseline，不再改 `proverif/kwaay-core-public-channel.pv`，把 Q1 的反例跑稳定，打开长 trace，写一页“攻击转写说明”。第二步，只在 `proverif/variants/aead-confirmation/kwaay-core-public-channel-aead.pv` 上实现 AEAD 分支，并跑出新的 query 结果。第三步，写一页 blocked-trace 解释：攻击者为何能到 `RecvComputed` 却过不了 `AeadConfirmed`。第四步，再写 related work 和 limitation。这个节奏很像 5G 论文结尾强调的那种“模型一旦建好，就能快速评估修改方案并避免 regression”的形式化工作流。citeturn30view0

如果想把时间安排再具体一点，可以按“产出物”而不是“天数”来推进：

| 阶段 | 必须产出的文件 | 在论文中对应什么 |
|---|---|---|
| baseline 定稿 | `baseline.out`、`baseline-q1-false.md` | 反例与缺陷章节 |
| AEAD 验证 | `aead.out`、`aead-fix.md` | 修复设计与结果章节 |
| 对照整理 | `comparison.md` | 主结果表 |
| 写作 | `draft.tex` / `draft.md` | 6–8 页 short paper |

## 最适合对照的小论文模板与写法

如果目标是“较快产出”，最值得对照的模板不是一篇，而是**五类不同风格**。Lowe 关于 Needham–Schroeder 的工作是最经典的 attack-and-fix 模板：先发现认证攻击，再提出修复，再验证修复版本。OAuth 2.0 的形式化分析更像“标准级结构”：建模、定义性质、发现多个攻击、给 fixes、证明 fixed version 的性质。5G AKA 的分析很适合借鉴“从标准/设计目标抽取安全需求，指出缺失或未说明的 goal，再给 provably secure fix”的写法。MTProto 2.0 适合借鉴“组件分离、逐模块验证、发现一个具体弱点”的增量式结构。PQXDH 2024 则非常适合你当前的 messaging 场景：作者与协议设计方互动，形式化分析发现规范需要额外 binding property，然后更新规范并重新验证。若你以后要往“实现/模型联动”或 computational lifting 方向扩展，再看 KBB17 那类 symbolic + computational 的 methodology paper。citeturn32view0turn19view0turn18view0turn19view1turn22view0turn21view0

把它们翻译成你最可直接套用的写法，大致如下：

| 模板论文 | 你最该借的部分 |
|---|---|
| Lowe 的 Needham–Schroeder attack/fix | 一条攻击、一条最小修复、一次重新验证 |
| OAuth 2.0 formal analysis | 明确列出 security goals、分清 baseline 和 fixed variant |
| 5G AKA formal analysis | 把“缺失 key confirmation”当成真正缺陷来讨论，并给轻量修复 |
| MTProto 2.0 symbolic verification | 逐模块、增量、对照表驱动的写法 |
| PQXDH 2024 | “形式化分析指出需要额外 binding / confirmation property”的叙事 |
| KBB17 secure messaging methodology | 若以后想扩成 symbolic + computational，可把当前工作接上去 |

**H. 如果用最快的 workshop/case-study 结构来写，正文最好是六块：**  
引言；K-Waay core 与 ProVerif 模型；baseline Q1 反例；AEAD extension；实验结果；讨论与限制。related work 视篇幅可以并入引言末尾或讨论末尾。这样最像 Lowe / MTProto / PQXDH 一类“一个主要缺陷 + 一个主要修复”的小论文，不会被 related work 和大模型细节稀释掉。citeturn32view0turn19view1turn22view0

**I. 如果只选三个最该深读的模板，优先级建议是：**  
第一，Lowe 的 Needham–Schroeder 两篇，因为你的故事线与它最像；  
第二，5G AKA，因为它直接展示了“missing key confirmation 也是 serious weakness，而且可以用 binding/unidirectional confirmation 修”；  
第三，PQXDH 2024，因为它最贴近异步 secure messaging 和“补 binding property”的现代写法。citeturn32view0turn30view0turn22view0

**J. 这类论文最容易出问题的地方，不是技术，而是表述过头。** 最建议在初稿阶段就避免下面这些句子：

| 避免这样写 | 建议这样写 |
|---|---|
| “K-Waay 被攻破了” | “The public-channel baseline violates receiver-to-sender agreement Q1.” |
| “攻击者恢复了会话密钥” | “攻击者诱导了一个 unpartnered receiver session / bogus accepted session.” |
| “我们证明了协议安全” | “We restore the modeled Q1 property while preserving the baseline secrecy-oriented queries in the symbolic model.” |
| “我们实现了完整 AEAD 通道” | “We model an AEAD-style authenticated confirmation tag via `aead_tag` / `aead_verify`.” |
| “该扩展保持了原始 deniability” | “Deniability preservation is out of scope for this extension and remains future work.” |

这么写的原因很简单。ProVerif 的正结果在符号模型里是 sound 的，但它不是 complete，也不是自动生成 computational theorem；同时，K-Waay 原论文对 Figure 7 证明了 KIND 与 deniability，而你的分支是修改过的协议，因此**不能**顺手继承原 deniability 结论。你的第一版文章只需要把 claim 范围收紧在：public-channel symbolic model、receiver agreement gap、sid-bound confirmation repair。这样最稳。citeturn29view0turn14view0

## 可直接用于小论文的 detailed outline

下面这份 outline 可以直接开写，基本就是 6–8 页 short paper 的骨架。

**可选标题：**

- *Formal Analysis of a Receiver-Agreement Gap in the K-Waay Core Protocol*  
- *A sid-bound AEAD Confirmation Extension for the K-Waay Core Protocol*  
- *Repairing Receiver-Side Agreement in the K-Waay Core by Authenticated Key Confirmation*

**一句话主张：**  
*We show that the K-Waay core, under an active public-channel symbolic attacker, admits an unpartnered receiver session that violates receiver-to-sender agreement, and that a minimal sid-bound authenticated confirmation tag restores this property without changing the baseline secrecy-oriented conclusions.*

**摘要**

- 一句背景：K-Waay 是基于 split-KEM 的异步 X3DH-like core。  
- 一句问题：你的 ProVerif public-channel baseline 中，secrecy-oriented queries 可以成立，但 Q1  
  `RecvDone ==> SendDone`  
  为 false。  
- 一句攻击含义：这不是 key recovery，而是 receiver-side exact matching completion failure。  
- 一句修复：提出 sid-bound AEAD-style authenticated confirmation tag。  
- 一句结果：baseline 中 Q1=false，AEAD variant 中 Q1=true，且保留 baseline secrecy-oriented queries。  
- 一句边界：结论限于 symbolic active-network model；deniability preservation 与 compromise model 留作 future work。

**引言**

- 介绍 K-Waay/X3DH-like asynchronous messaging 背景。  
- 说明为什么单看 secrecy 不够，receiver acceptance 也需要形式化。  
- 给出本文核心发现：public-channel baseline 的 Q1 失败。  
- 给出本文核心修复：sender-to-receiver sid-bound authenticated confirmation。  
- 列三条贡献：  
  1. 一个可重现的 receiver-side agreement counterexample；  
  2. 一个最小 AEAD/key-confirmation extension；  
  3. 一组 baseline vs AEAD 的 ProVerif 对照结果。  

**背景与模型**

- 简述 K-Waay Figure 7：`m=(ctL,ctE,ctS)`，`sid` 绑定 transcript，`k=KDF(...)`。  
- 简述 ProVerif：secrecy、correspondence、attack reconstruction。  
- 给出攻击者模型：active public-channel / Dolev–Yao。  
- 交代事件语义：`SendDone` 和 `RecvDone` 的放置含义。  
- 如果篇幅够，再用一段话说明：Q1 是“matching-session agreement on `(A,B,sid,k)`”，不要一上来就宣称 injective agreement。  

**baseline 模型与 Q1 缺陷**

- 说明 baseline 文件：`proverif/kwaay-core-public-channel.pv`。  
- 列出保留的 secrecy-oriented queries。  
- 给出 Q1：  
  `query A,B,s,k; event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).`  
- 解释其安全含义：接收方正式接受应有匹配发送方完成。  
- 报告结果：Q1=false。  
- 单独写一段“这不是 key recovery”——因为 secrecy 与 correspondence 是不同性质。  

**攻击轨迹解释**

- 先用一段自然语言总述攻击。  
- 再用 5–6 个步骤解释 trace：  
  1. honest sender 产生合法核心消息；  
  2. 攻击者拦截并主动篡改/重组核心 ciphertext；  
  3. 接收方据此导出 `sid'`、`k'`；  
  4. baseline 在导钥后直接进入 `RecvDone`；  
  5. 没有匹配的 `SendDone(A,B,sid',k')`；  
  6. 因而形成 unpartnered receiver session。  
- 用一句话点明结果影响：receiver installs bogus session state。  

**AEAD/key-confirmation extension**

- 说明新分支只改副本模型，不改 baseline。  
- 给出新流程：  
  `mCore -> sid -> k -> kc=aead_tag(k,sid) -> confirmed_msg(mCore,kc)`。  
- 说明接收方流程：  
  `RecvComputed` 之后必须执行 `aead_verify(kRecv,sid,kc)=aead_ok`，  
  只有成功后才能 `AeadConfirmed`、`ReceiverKey`、`RecvDone`。  
- 说明为什么 `sid` 只绑定 `mCore` 不绑定 `kc`：避免循环依赖。  
- 说明为什么称它为 AEAD-style confirmation，而不是完整 payload AEAD channel。  
- 说明为什么选择单向确认：保持异步性。  

**AEAD 分支验证结果**

- 给出比较表：baseline vs AEAD。  
- 报告主结果：Q1 从 false 变为 true。  
- 报告 secrecy-oriented queries：保持为原状。  
- 报告辅助查询：  
  `RecvDone ==> AeadConfirmed`，  
  `AeadConfirmed ==> SendDone`。  
- 解释 blocked trace：攻击者也许仍能让接收方到达 `RecvComputed`，但无法伪造匹配 `(sid,k)` 的 `kc`，因此过不了 `AeadConfirmed`。  

**讨论与限制**

- 明确本文修复的是 active-network agreement gap，不是 key recovery。  
- 明确本文不证明 deniability preservation。  
- 明确本文暂不覆盖 `STATE`/`KEY` reveal 等 compromise setting。  
- 如需一句 future work：后续可扩展到 Tamarin / CryptoVerif / stronger compromise models。  

**相关工作**

- Lowe：attack-and-fix 的经典模板。  
- OAuth 2.0：标准级 formal analysis + attacks + fixes。  
- 5G AKA：missing key confirmation / missing goals / lightweight fixes。  
- MTProto 2.0：incremental ProVerif analysis + UKS。  
- PQXDH 2024：formal verification 驱动 binding-property 更新。  
- 若篇幅够，再补一句 KBB17 作为 secure messaging methodology。  

**结论**

- 重述 baseline 的 Q1 缺陷。  
- 重述 AEAD 分支的最小修复。  
- 重述最重要的结论边界：  
  这是一个 public-channel symbolic result；  
  修的是 receiver-side agreement / key confirmation，  
  不是在宣称原始 K-Waay 出现了 key recovery。  

如果只追求最快成稿，最建议优先完成的四个成稿部件依次是：**Q1 反例图解、AEAD 设计图、baseline vs AEAD 结果表、限制声明**。这四块一旦写稳，文章就已经具备完整的“发现缺陷—解释攻击—提出修复—工具验证—边界声明”的闭环，而这正是 Lowe、5G AKA、MTProto、PQXDH 这类小而完整的形式化分析论文最共同的成功结构。citeturn32view0turn30view0turn19view1turn22view0