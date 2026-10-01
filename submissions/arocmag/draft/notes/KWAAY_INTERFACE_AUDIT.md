# K-Waay BatchReceive索引语义审查

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_2`

## 1. 审查对象与版本

审查文件：`reviews/2026-09-16-evidence/kwaay-full-2024-120.pdf`。

- 标题：*K-Waay: Fast and Deniable Post-Quantum X3DH without Ring Signatures*。
- ePrint：2024/120，full version。
- PDF：62 页；封面日期 2024-01-27；ePrint 记录 revision 日期 2024-01-29。
- SHA-256：`476f28594806f15f4baab6ce7d3785143db0a013f21fbcf590ac1666161660a8`。

本次直接核对了 PDF 第 15～18 页的 DAKE syntax、安全游戏与 `KEY/TEST` 定义，以及第 20～23 页的 K-Waay 构造、Fig. 10、different-party condition 和证明开头。下述判断不依赖历史审稿报告转述。

## 2. 审查结论总表

| 问题 | 原始论文位置 | 原文依据 | 允许的解释 | 不能推出的结论 |
|---|---|---|---|---|
| `j`在输入中指什么 | Sec. 4.1 p.15；Sec. 4.2.1 pp.15–16；Fig. 10 p.21 | `BatchReceive` 输入写成按 $j$ 标记的 $(pk_j,prek_j,m_j)$；文本把 $P_j$ 称为 sender/counterpart | $j$ 是参与方索引，标记声称发送方及其输入分量 | 不能把 $j$ 简化为纯槽位序号 |
| `j`在输出中指什么 | Sec. 4.1 p.15；Fig. 10 p.21 | 语法输出 key vector；Fig. 10 循环按 $j$ 计算 $k_j$，返回 $\{k_j\}_j$ | 在合法输入域内，$k_j$ 对应该 $j$ 标记的输入处理结果 | 重复同一 $j$ 时返回几个独立分量及其选择规则 `NOT ESTABLISHED` |
| 接收方会话如何记录对端 | Sec. 4.2.1 p.16 | 接收方的 `sid`、`pid` 和 $k$ 为 vectors；一个 receiver 可有多个 counterparts | `pid` 向量保存对端参与方索引，$k$ 向量保存相应分量 | 不能把模型 $rst$ 当作这些向量或真实 state |
| `j`在执行查询中指什么 | Sec. 4.2.3 p.17 | 启动 sender 时 `pid=j`，启动 receiver 时 `pid=\vec j`；receiver EXEC 检查输入索引向量与 `pid` 一致 | `j` 是安全游戏中的参与方/partner index | 原游戏未定义把同一 partner index 重复登记为两个独立 slot |
| `j`在 `KEY` 中指什么 | Sec. 4.2.3 p.17 | `KEY(i,s,j)` 对 receiver 输出 $\pi_i^s.k_j$，对 sender 输出单个 $\pi_i^s.k$ | receiver 的 `j` 选择一个 party-indexed key component | 当前 Tamarin `ReceiverAccept` 不支持任何 `KEY` 后果 |
| `j`在 `TEST` 中指什么 | Sec. 4.2.3 pp.17–18 | receiver 分支要求 $j\in\pi_i^s.pid$，随后返回真实 $\pi_i^s.k_j$ 或随机 key；sender 分支要求 $j=pid$ | receiver test session 可“with respect to key $j$” | 当前模型的重复接受不能推出 test advantage 或 key indistinguishability failure |
| 原文是否建立输入party与output component联系 | Sec. 4.1–4.2；Fig. 10 | 同一下标 $j$ 连续用于 $P_j$、输入三元组、会话向量和 $k_j$ | 在原文合法域内，可以说输入参与方索引与输出分量通过 $j$ 对应 | 不能把该对应扩展到违反 different-party condition 的重复 $j$ 域 |
| 原文是否建立独立slot到party/output的双射 | 无单独定义 | 原文使用 vector/集合及 party 下标，没有 first-class slot 对象 | 本文可为两槽模型另设位置 $\ell$，并与 party 索引区分 | 独立的 `slot ↔ party ↔ output` 双射：`NOT ESTABLISHED` |
| 原文是否规定不同参与方条件 | Sec. 5.1 p.21，Fig. 10 后 | 明确写出一次调用中 $S$ 的每个元素对应不同 party | 该条件是 source fact；本文研究其受控抽象语义 | 不能声称本文发现原文漏写该条件 |
| 原文是否规定条件的具体执行位置 | p.21 自然语言条件 | 条件存在，但未给出单独 admission algorithm/check | caller、batch builder、receiver 等只能作为可能位置讨论 | 某个部署一定漏查，或必须在 receiver 新增 check：`NOT ESTABLISHED` |

## 3. BatchReceive输入与输出

### 3.1 DAKE语法（Sec. 4.1, p.15）

原文把 `BatchReceive` 定义为接收执行方 $P_i$ 的算法，输入包括 $sk_i$、临时状态 $st_i$ 和大小 $d\ge 1$ 的向量。向量元素含声称发送方的 $pk_j$、$prek_j$ 和 $m_j$；输出是长度 $d$ 的 key vector，其中部分或全部分量可以为 $\bot$。

**允许解释**：$j$ 标识声称的对端参与方，输入的 key/prekey/message 和输出 key component 使用共同下标。

**不能解释**：Sec. 4.1 没有以独立变量定义“槽位身份”，也没有给出参与方下标重复时的向量规范。因此，重复同一 $j$ 后仍存在两个可由 `KEY(i,s,j)` 区分的输出，不由该语法支持。

### 3.2 K-Waay构造（Sec. 5.1, Fig. 10, p.21）

Fig. 10 的 `BatchReceive` 循环写为“对 $(pk_j,prek_j,m_j)\in S$ 的每个 $j$”。循环内部把结果写入 $k_j$，若 split-KEM 解封装失败则设置 `fail`，最后根据该标志返回全 $\bot$ 向量或 $\{k_j\}_j$。图后文本明确给出 different-party condition。

**允许解释**：在条件满足的输入域内，每个参与方下标至多出现一次，同一 $j$ 把一个输入分量和一个输出分量联系起来。

**不能解释**：如果把同一参与方的两个输入放入 $S$，原算法记号是否覆盖、重复下标是否覆盖旧值、输出是否按位置而非 party 选择，均为 `NOT ESTABLISHED`。当前研究不得替原文选择其中一种扩展语义。

### 3.3 失败语义

Fig. 10 区分分量结果与 batch-wide failure：签名失败可令当前 $k_j=\bot$ 后继续；split-KEM 解封装失败会设置 `fail`，最终返回 $\bot^{|S|}$。当前 R/M/P 模型的 `Reject(bid,rst)` 是按消息或参与方相等设置的分析分支，没有重建上述密码失败条件。

**结论**：不能把 M/P `Reject` 直接称为 K-Waay 的 batch-wide cryptographic failure。

## 4. 安全游戏中的索引

### 4.1 receiver向量字段（Sec. 4.2.1, p.16）

原文说明，当角色为 receiver 时，`sid`、`pid` 和 $k$ 是 vectors。接收方会话可有多个 sender counterparts；`pid` 因而记录多个参与方索引。该设计给出了 party-indexed key component 的游戏语义背景。

原协议 `sid` 也可为向量，且通过 partnering definition 与 sender session 对应。它不是当前模型的 fresh `sid_model`。正文采用 $oid$ 后，两种对象已明确分开。

### 4.2 EXEC（Sec. 4.2.3, p.17）

启动 sender 会话时，特殊输入记录单个 $j$ 为 `pid`；启动 receiver 会话时记录向量 $\vec j$。receiver 的执行输入按 $j\in\vec j'$ 组织，挑战者检查 $\vec j'$ 与会话 `pid` 相等后才调用 `BatchReceive`。

**允许解释**：原安全游戏把 receiver 输入域和其 counterpart-party 向量联系起来。

**不能解释**：原文的向量相等检查不说明重复元素是否允许；K-Waay 构造随后明确的 different-party condition 排除了本文模型中的同 party 两槽情况。

### 4.3 KEY与TEST（Sec. 4.2.3, pp.17–18）

`KEY(i,s,j)` 在 receiver 分支输出 $\pi_i^s.k_j$。`TEST(i,s,j)` 在 receiver 分支先要求 $j\in\pi_i^s.pid$，随后返回真实 $\pi_i^s.k_j$ 或同分布随机 key；论文也把 receiver test session 称为“with respect to key $j$”。freshness 条件继续使用相同的 $j$ 约束直接 key query。

**允许解释**：$j$ 不是无语义的数组位置，而是 receiver session 中用于选择参与方相关 key component 的索引。这能解释为什么批内 party relation 具有协议接口动机。

**不能解释**：当前 R/M/P 模型没有 $k_j$、session status、`KEY`、`TEST` 或 challenge bit。因此，模型中的 party repetition、exact-origin repetition 或两个 `ReceiverAccept` 均不能推出 `KEY/TEST` 失败、key confusion、密钥泄露或 KIND advantage。

## 5. slot、party与output component的最终判断

原文在**合法输入域**内通过共同下标 $j$ 建立以下关系：

$$
P_j
\longleftrightarrow
(pk_j,prek_j,m_j)
\longleftrightarrow
k_j,
$$

接收方安全游戏还通过 `pid` 向量和 `KEY/TEST(i,s,j)` 使用该下标。这个关系足以作为本文研究 party-level batch relation 的动机。

原文没有把位置 $\ell$ 建模为独立协议坐标，也没有定义一个可脱离合法域使用的

$$
\ell\longleftrightarrow P_j\longleftrightarrow k_j
$$

双射。本文两槽模型中的 Slot 1/2 是分析结构；把它提升为原协议明示的 slot semantics，或给同一 $j$ 的两个槽补写 output selection，均标记为 **NOT ESTABLISHED**。

## 6. 中文正文允许使用的最强表述

可以写：

> 在 K-Waay 规定的合法输入域内，参与方下标 $j$ 同时标识声称发送方的输入分量和接收方的输出密钥分量；安全游戏也用 $j$ 选择 receiver session 的 $k_j$。这为批内参与方关系提供了协议接口动机。

必须紧接着限定：

> 原文没有规定重复参与方下标下的扩展语义，当前模型也未编码 $k_j$ 或 `KEY/TEST`，因此本文不从两槽接纳结果推出密钥接口后果。

不得写：

- “K-Waay 忘记检查不同参与方”；
- “两个同 party slot 必然覆盖同一 $k_j$”；
- “模型已经证明 `KEY/TEST` 接口失效”；
- “`ReceiverAccept` 等于输出或安装了一个真实会话密钥”；
- “原论文明确规定 slot 到 party 和 output 的独立双射”。

