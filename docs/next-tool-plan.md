# Next Tool Plan

## 目的

这个文件记录 K-Waay Figure 7 core ProVerif symbolic analysis 之后的后续工具路线。

当前结论是：

```text
ProVerif core symbolic stage completed.
Full formal verification remains future work.
```

也就是说，当前 ProVerif 阶段可以收束，但完整 K-Waay 形式化验证还没有结束。

后续工作主要分成两条路线：

```text
Tamarin: state / ordering / partnering / BatchReceive
CryptoVerif or hand proof: computational KIND / indistinguishability / reductions
```

## 1. 当前 ProVerif 阶段总结

当前 ProVerif 分析对象是：

```text
K-Waay Figure 7 core
public-channel symbolic model
single receive approximation
```

当前消息结构保持：

```text
m = (ct_l, ct_k, ct_s)
```

当前没有加入：

```text
AEAD
MAC
tag
key confirmation
full BatchReceive
```

当前 ProVerif 阶段已经完成：

1. baseline no-compromise secrecy；
2. public-channel attacker model；
3. 长期公钥显式公开修正；
4. sender-side / receiver-side secrecy 分离；
5. 单独 compromise 实验；
6. 组合 compromise 实验；
7. optional compromise sender-side exception sanity check；
8. split-KEM component authenticity query；
9. `RecvDone ==> SendDone` 降级为 diagnostic query；
10. 与论文 KIND / freshness / partner identifiers / UNF-1KMA / IND-1BatchCCA 的定义对齐。

当前主要 baseline 结果：

```text
HonestRun: reachable
RecvDone ==> SendDone: false
RecvDone ==> SenderPrekeyVerified: true
RecvDone ==> ReceiverPrekeyVerified: true
SenderKey secrecy: true
ReceiverKey secrecy: true
```

当前主要解释：

```text
RecvDone ==> SendDone
```

是 full-message exact agreement，对 Figure 7 core 来说过强，因此只作为 diagnostic query 保留。

当前 main query 包括：

```text
SenderKey secrecy
ReceiverKey secrecy
SenderPrekeyVerified structural query
ReceiverPrekeyVerified structural query
SplitKemAccepted ==> SenderSplitKemComponent
sender-side exception sanity query
```

## 2. ProVerif 阶段可以声称什么

当前可以谨慎声称：

1. 在当前 public-channel single receive symbolic model 下，honest execution 可达。
2. baseline 下 sender-side 和 receiver-side session-key secrecy 成立。
3. 单独泄露 `sig_sk`、`kem_sk`、`ekem_sk` 不破坏当前 session-key secrecy。
4. 单独泄露 `sender_skem_sk` 或 `receiver_skem_sk` 不破坏 honest sender-side secrecy，但会导致 receiver-side secrecy false。
5. `sender_skem_sk` / `receiver_skem_sk` 下的 receiver-side false 更像 split-KEM state compromise 下的 receiver-side unpartnered session bad case。
6. optional compromise model 下，如果 attacker 知道 sender-side key，则必须发生 B 侧三个 decapsulation secret compromise。
7. split-KEM component-level authenticity query 为 true。
8. `RecvDone ==> SendDone` 为 false 不表示 Theorem 1 或 KIND 证明失败。

## 3. ProVerif 阶段不能声称什么

当前不能声称：

1. 已经证明完整 K-Waay 协议安全。
2. 已经证明 full BatchReceive 安全。
3. 已经证明 computational KIND game。
4. 已经证明 full-message exact agreement。
5. 已经完成 receiver-side exception theorem。
6. 已经完整建模 partnered / unpartnered session。
7. 已经完整建模 one-time prekey consumption。
8. 已经完整建模 adaptive compromise ordering。
9. 已经证明 UNF-1KMA 或 IND-1BatchCCA 的 computational security。
10. ProVerif symbolic secrecy 等价于 real-or-random indistinguishability。

## 4. 为什么 ProVerif 阶段到这里收束

ProVerif 适合当前阶段，因为它可以高效检查：

```text
symbolic secrecy
reachability
correspondence query
public-channel attacker
simple compromise experiments
```

但是后续问题开始涉及：

```text
state update
time ordering
one-time state consumption
BatchReceive vector semantics
partnered / unpartnered session
KEY / TEST oracle freshness
computational indistinguishability
```

这些问题超出了当前 ProVerif core model 的自然表达范围。

因此，当前不建议继续无限扩展 ProVerif compromise 组合矩阵。

后续应转向：

```text
Tamarin
CryptoVerif
hand computational proof
```

## 5. Tamarin 后续路线

### 5.1 Tamarin 适合处理什么

Tamarin 更适合处理：

```text
stateful protocols
time ordering
compromise before / after event
persistent facts
linear facts
state consumption
partnered / unpartnered session
BatchReceive
```

因此，Tamarin 后续主要负责 K-Waay 中 ProVerif 没有完整表达的状态语义。

### 5.2 Tamarin 目标 1: partnered / unpartnered session

需要定义：

```text
SenderSession(A,B,s,k)
ReceiverSession(B,A,s,k)
Partnered(A,B,s,k)
UnpartneredReceiver(B,A,s,k)
```

目标不是简单复刻：

```proverif
RecvDone ==> SendDone
```

而是表达更接近论文的关系：

```text
sender session <-> receiver batch component
```

需要研究：

1. sender session 如何绑定 receiver batch slot；
2. receiver batch component 如何绑定 sender identity；
3. partner identifier 和 key identifier 如何表达；
4. unpartnered receiver session 如何分类；
5. receiver-side false 是否来自 expected bad case。

### 5.3 Tamarin 目标 2: BatchReceive

需要建模：

```text
BatchReceive input vector
BatchReceive output vector
batch slot index
batch abort behavior
```

关键语义：

```text
如果 batch 中任意 split-KEM decapsulation 失败，
整个 batch 返回 bottom。
```

需要表达：

1. 多个 sender 使用同一个 receiver split-KEM public key；
2. receiver 用同一个 receiver split-KEM secret state 批量 decapsulate；
3. batch 中每个 component 对应一个 output key；
4. batch slot 与 partner/key identifier 对齐；
5. batch fail 时不输出任何有效 key。

### 5.4 Tamarin 目标 3: state consumption

需要建模：

```text
receiver_skem_sk state consumption
ekem_sk state consumption
one-time prekey use
```

要回答：

1. receiver state 什么时候生成；
2. receiver state 什么时候被使用；
3. 使用后是否失效；
4. compromise 在使用前和使用后有什么区别；
5. state exposure 是否影响 freshness。

### 5.5 Tamarin 目标 4: compromise ordering

需要区分：

```text
compromise before Send
compromise after Send
compromise before Receive
compromise after Receive
compromise after state consumption
```

这对 receiver-side exception 很关键。

当前 ProVerif 只能较粗地表达：

```text
secret is leaked
```

但不能自然表达：

```text
secret was leaked before / after a specific accept event
```

Tamarin 应该用时间顺序约束表达这类性质。

### 5.6 Tamarin 预期输出

Tamarin 阶段的预期输出不是替代 ProVerif，而是补充：

1. receiver-side partnered / unpartnered trace classification；
2. BatchReceive state model；
3. state consumption lemmas；
4. compromise ordering lemmas；
5. receiver-side exception theorem candidate；
6. 对 ProVerif diagnostic false trace 的更精确解释。

## 6. CryptoVerif / computational proof 后续路线

### 6.1 CryptoVerif 适合处理什么

CryptoVerif 或手工 computational proof 更适合处理：

```text
real-or-random key indistinguishability
game-based proof
cryptographic reductions
advantage bounds
KDF as 3PRF
KEM IND-CCA
split-KEM UNF-1KMA
split-KEM IND-1BatchCCA
```

这些不是 ProVerif symbolic model 能完整表达的内容。

### 6.2 CryptoVerif 目标 1: KIND real-or-random game

需要靠近论文 KIND game：

```text
TEST session key: real key vs random key
```

目标是表达：

```text
attacker cannot distinguish real session key from random session key
```

而不是只表达：

```text
attacker(k) is false
```

需要建模：

1. TEST oracle；
2. real-or-random bit；
3. KEY reveal oracle；
4. freshness predicates；
5. sender / receiver test session；
6. partnered / unpartnered cases。

### 6.3 CryptoVerif 目标 2: KDF 3PRF hybrid

当前 K-Waay key derivation 是：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

Theorem 1 的核心直觉是：

```text
只要 K_l / K_k / K_s 至少一个输入对攻击者隐藏，
KDF 输出就应当不可区分于随机。
```

CryptoVerif / hand proof 需要表达：

1. 哪个 hybrid 替换哪个 KDF 输入；
2. 如何使用 3PRF assumption；
3. sid 如何作为 transcript binding；
4. 如果一个输入随机，则最终 session key 如何变随机。

### 6.4 CryptoVerif 目标 3: primitive reductions

需要把 K-Waay KIND advantage 归约到：

```text
LKEM IND-CCA
EKEM IND-CCA
sKEM IND-1BatchCCA
sKEM UNF-1KMA
Sig SUF-CMA
KDF 3PRF
```

目标不是重新证明这些 primitive，而是说明：

```text
如果攻击者能破坏 K-Waay KIND，
则可以构造攻击者破坏其中某个 primitive assumption。
```

### 6.5 CryptoVerif 目标 4: Theorem 1 advantage bound

论文 Theorem 1 给出的是 advantage bound。

后续需要对齐：

1. 每一项 advantage 来自哪个攻击 case；
2. correctness error 如何进入 bound；
3. partnered / unpartnered sender / receiver case 如何分配到不同 assumption；
4. BatchReceive 对 IND-1BatchCCA 项的影响；
5. SUF-CMA 对 prekey signature 的作用；
6. UNF-1KMA 对 split-KEM authenticity 的作用。

### 6.6 CryptoVerif 预期输出

CryptoVerif / computational proof 阶段的预期输出：

1. KIND game 建模草案；
2. TEST / KEY / STATE / LTK oracle 对齐；
3. freshness predicate 草案；
4. KDF hybrid proof outline；
5. primitive reduction map；
6. Theorem 1 advantage bound 对齐说明。

## 7. 推荐执行顺序

后续不建议立刻同时做 Tamarin 和 CryptoVerif。

推荐顺序：

### Step 1: 封存 ProVerif 阶段

执行：

```bash
git status
git tag proverif-core-v1
git push origin proverif-core-v1
```

前提是当前工作区已经 clean。

### Step 2: 先做 Tamarin 预研

原因：

Tamarin 直接补当前最大缺口：

```text
partnered / unpartnered
BatchReceive
state consumption
compromise ordering
```

这些问题也会帮助后续定义 CryptoVerif freshness。

### Step 3: 写 Tamarin model sketch

先不要追求完整模型，只写：

```text
state facts
event facts
batch slot representation
compromise facts
partnering candidate lemmas
```

### Step 4: 再考虑 CryptoVerif / hand proof

等 Tamarin 对 state / partnering / freshness 有更清楚结论后，再进入 computational KIND。

### Step 5: 回到论文 Theorem 1

最后把：

```text
ProVerif symbolic results
Tamarin state lemmas
CryptoVerif / hand proof reductions
```

合并成最终形式化验证路线。

## 8. 下一阶段立即任务

当前最直接的下一阶段任务是 Tamarin 预研。

建议创建：

```text
docs/tamarin-prestudy-plan.md
```

主要回答：

1. Tamarin 要解决 ProVerif 的哪个缺口；
2. K-Waay 的哪些对象需要变成 facts；
3. sender / receiver / batch slot 如何建模；
4. compromise ordering 如何表达；
5. 第一版 lemma 应该写什么；
6. 哪些东西暂时不建模。

暂时不建议直接写 `.spthy` 文件。

## 9. 当前总判断

当前状态可以总结为：

```text
ProVerif core symbolic stage: completed.
Tamarin state / partnering stage: planned.
CryptoVerif computational KIND stage: future work.
```

这意味着：

```text
K-Waay Figure 7 core 的 ProVerif 工作可以收束。
完整 K-Waay 形式化验证还没有结束。
下一步应转向 Tamarin / CryptoVerif 的计划与预研。
```
