# Stage 2中文初稿自检

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_2`  
日期：2026-10-02（Asia/Shanghai）

## 1. 自检对象

- `sections/00-introduction.md`
- `sections/01-batch-admission-problem.md`
- `sections/02-symbolic-modeling.md`
- `notes/NOTATION_CONSISTENCY.md`
- `notes/FORMAL_RELATION_AUDIT.md`
- `notes/KWAAY_INTERFACE_AUDIT.md`

核对基准包括 Stage 1 的结构/映射/主张矩阵/精简计划，英文母稿 Sections 1–8 及附录，三个 `rq-v2-minimal` 模型，独立复核的结果表和 trace audit，以及 K-Waay full PDF 的 Secs. 4.1、4.2、5.1 和 Fig. 10。

## 2. 十二项必检结果

| 检查项 | 结果 | 证据与结论 |
|---|---|---|
| 1. 是否真正写出第0～2章完整中文初稿 | PASS | 已形成引言、问题定义和符号建模三份连续正文；不是要点式大纲。章节和小节与 Stage 2 指定结构一致。 |
| 2. 是否存在明显英文直译腔 | PASS WITH EDITS | 将 `guard`、`trace`、`witness`、`provenance` 等非必要英文替换为接纳条件、执行轨迹、见证和来源记录；协议/工具/API 名称及首次出现的规范英文术语保留。 |
| 3. 是否错误声称发现K-Waay协议漏洞 | PASS | 引言和 1.1 明确原文已有 different-party condition；全文把异常输入限定为放宽接纳模型的域外组合。 |
| 4. 是否承认原文已提出different-party condition | PASS | 引言、1.1 和接口审计均直接引用 Sec. 5.1、Fig. 10 后 p.21 的条件。 |
| 5. source-to-model映射是否准确 | PASS | 2.1 表 1 区分源输入、模型条目、真实 receiver state 与 $rst$、$k_j$ 与 `ReceiverAccept`、密码失败与抽象 `Reject`。 |
| 6. sid/oid是否统一 | PASS | 正文公式使用 $oid$；原协议 transcript `sid`、源码变量 `sid` 和 lemma 原名只在来源说明中保留。显式写出 $oid\equiv sid_{model}$。 |
| 7. 是否存在不受支持的KEY/TEST结论 | PASS | 1.1 仅用 party-indexed `KEY/TEST` 解释动机；明确重复 $j$ 下的选择语义未建立，当前模型不能推出查询失败。 |
| 8. 是否错误扩大Tamarin证明范围 | PASS | 明确机器验证固定两槽、止于 `ReceiverAccept`、无 arbitrary-$n$ theorem、无密码/部署/refinement 结论。 |
| 9. 是否存在公式、术语或引用不一致 | PASS AFTER FIX | 用 $\mathsf{RA}$ 缩写 `ReceiverAccept`，避免与 R 模型重名；所有 `\cite{}` key 均存在于 `references.bib`；数学块成对闭合。 |
| 10. 是否与CLAIM_EVIDENCE_MATRIX冲突 | PASS | 保留 R/M/P 的窄结论、P 正控制、弱 rejection witness、独立复核和 source-to-model 边界；未新增强结论。 |
| 11. 是否错误沿用“没有独立重跑”的旧表述 | PASS | 2.4 写明独立复核已重跑 14 个模型—引理实例且状态/步数全匹配，同时保留“不是历史日志恢复”的限制。 |
| 12. 是否未经证据支持新增研究结论 | PASS | 新增内容均为结构重写、记号澄清或来源审计；K-Waay duplicate-$j$ 语义标为 NOT ESTABLISHED；P/M/I 人工推导单独标注。 |

## 3. 公式和模型一致性

### 3.1 条目和记号

- 论文条目固定为 $E=(A,oid,m)$。
- 源码条目仍是 `<A,sid,m>`；未修改模型。
- $bid$ 和 $rst$ 均由 `CreateBatch` 的 `Fr` 产生；正文没有把 $rst$ 写成完整 receiver state。
- `ReceiverAccept` 参数与三个模型一致，只在论文层把 `sid` 换成 $oid$。

### 3.2 生命周期

正文顺序与源码一致：`CreateParty` → `SendMessage` → `CreateBatch` → `CollectSlot1` → `CollectSlot2` → admission/rejection → `ProcessSlot1` → `ProcessSlot2`。没有增加验证、解密、安装或 key-return 规则。

### 3.3 三模型差异

- R：无不等 action 和收集后 rejection branch。
- M：`Neq(m1,m2)` + equal-message rejection。
- P：`Neq(A1,A2)` + equal-party rejection。

正文说明 guarded theory 还存在 restriction/rejection/lemma 集差异，没有误写成“只改一行”。

### 3.4 P/M/I关系

关系固定为

$$
(P_\tau\Rightarrow M_\tau)\land(M_\tau\Leftrightarrow I_\tau),
\qquad M_\tau\not\Rightarrow P_\tau.
$$

`FORMAL_RELATION_AUDIT.md` 已逐方向给出假设和推导。前两部分是人工规则推导；非蕴含使用 M 的 `same_party_different_messages_batch_exists` 与 `accepted_batch_has_distinct_messages`。正文没有创造同名 lemma。

## 4. 引用核对

第 0～2 章使用的引用 key 为：

- `collins2024kwaay`
- `collins2024kwaayfull`
- `cohngordon2020signal`
- `bhargavan2024pqxdh`
- `cremers2023session`
- `lupetti2006names`
- `lowe1997hierarchy`
- `meier2013tamarin`

全部存在于 `manuscript/bibliography/references.bib`。没有虚构新文献。K-Waay 接口判断还直接核对了 full PDF p.15–18、p.21–23；不同参与方条件、输出分量和 `KEY/TEST` 的位置已记录在 `KWAAY_INTERFACE_AUDIT.md`。

## 5. 本轮发现并修正的问题

1. **sid歧义**：采用 $oid\equiv sid_{model}$，并建立原协议/模型符号表。
2. **P/M/I结合歧义**：将简写改为带括号的合取关系，非蕴含单列。
3. **模型R与事件缩写重名**：把 `ReceiverAccept` 缩写从 $R(\cdot)$ 改为 $\mathsf{RA}(\cdot)$。
4. **参与方索引与槽位混同**：用 $j$ 表示原文参与方索引，用 $\ell$ 表示本文位置；重复 $j$ 语义标为未建立。
5. **旧复现状态**：删除“没有独立重跑”的旧口径，改用有日期、版本和 raw outputs 的独立复核事实。
6. **过量英文术语**：改写为自然中文，只保留首次定义和不可替代的 API/模型术语。

## 6. 仍存在但不由本阶段解决的风险

- M1 所指出的研究非平凡性/发表增量问题不能通过中文重写消除。当前稿坚持窄的受控形式语义案例定位。
- 模型仍缺 recipient/prekey/context 的密码关联和 key outputs；没有 source-to-model refinement。
- K-Waay 对重复参与方下标的扩展域没有定义，当前稿不补写该语义。
- M 是辅助比较控制，尚无证据表明真实 K-Waay 实现采用消息级去重替代参与方条件。
- 2025 年 K-Waay 后续工作的接口相关性应在完整 Related Work 写作阶段核查；本阶段没有凭题名添加结论或新引用。

## 7. 自检结论

第 0～2 章已达到进入第 3 章结果写作所需的定义一致性：源接口边界、$oid$ 记号、R/M/P 共同生命周期、关键性质和证据层次均已冻结。当前状态只表示前半部分初稿可供人工审查，不表示全文或投稿稿件完成。

**SELF_REVIEW_PASS**

