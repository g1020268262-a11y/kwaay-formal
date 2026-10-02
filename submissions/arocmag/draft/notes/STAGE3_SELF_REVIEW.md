# Stage 3中文初稿自检

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_3`  
日期：2026-10-02（Asia/Shanghai）

## 1. 自检对象

- `sections/02-symbolic-modeling.md` 的两处指定修订；
- `sections/03-formal-analysis.md`；
- `figures/FIGURE_2_SPEC.md`；
- `notes/STAGE3_EVIDENCE_AUDIT.md`。

审查基线为当前三个 `.spthy` 源文件、`result-comparison.tsv`、三组 raw stdout/stderr、三个 JSON graph、manifest、SHA-256 清单以及 Stage 1/2 的 claim/notation/interface 审计。

## 2. Claim-to-evidence检查

| 检查项 | 结果 | 核查说明 |
|---|---|---|
| 是否真正解释机器结果，而非只重复 lemma 名称 | PASS | 3.1 解释精确三元组重复收集及持久来源复用；3.2 解释两个独立来源共享 party；3.3 区分 safety、non-vacuity 和 rejection reachability。 |
| 是否完整覆盖 14 项结果 | PASS | 表3逐行覆盖 4 个 R、5 个 M、5 个 P 实例；正文重点解释核心实例，其余结果给出限定作用。 |
| 是否混淆 verified 与 falsified | PASS | 13 项标为 VERIFIED；仅 R `receiver_accept_injective` 标为 FALSIFIED WITH COUNTEREXAMPLE。 |
| 是否误读 exists-trace | PASS | 所有存在性结果均写为“至少存在一条执行/分支可达”，未写为全称或活性保证。 |
| 是否夸大两个弱 rejection lemma | PASS | 明确说明前置 Send 不绑定 rejected tuple，也不推出 eventual rejection。 |
| 是否把人工推导写成机器证明 | PASS | $P/M/I$ 的三个蕴含方向均标注为基于共同规则的人工推导；只有非蕴含使用 M 的机器 safety+witness。 |
| 是否保留 P/M/I 的必要假设 | PASS | 保留 fresh message、精确 `!Sent`、已验证 origin correspondence、共同 $(bid,rst)$ 和不同时间点。 |
| 是否存在重复讨论 | PASS WITH EDIT | 每个模型在各自小节展开；3.4 只综合证据层次和逻辑关系，未再次复述完整见证。 |
| 是否与第 0～2 章矛盾 | PASS | 沿用 $oid\equiv sid_{model}$、固定两槽、`ReceiverAccept` 终点、R/M/P 定义及 K-Waay 合法输入域限制。 |
| 是否夸大 K-Waay 协议层后果 | PASS | 未声称完整协议攻击、UKS、misbinding、密钥泄露、`KEY/TEST` 失败、部署漏洞或任意批大小定理。 |
| 是否存在旧 provenance 表述 | PASS | 写明 2026-09-16 独立重跑保留 raw stdout/stderr 与 JSON graphs；同时与历史 freeze 记录分开。 |

## 3. 14项结果逐组核对

### R模型

- `normal_relaxed_batch_exists`：verified 10，与 evidence MATCH；仅作基本可达性。
- `one_send_two_accepts_exists`：verified 13，与 evidence MATCH；唯一性只限匹配 $(A,sid,m)$ 的 Send。
- `receiver_accept_has_send`：verified 8，与 evidence MATCH；只作理想来源对应。
- `receiver_accept_injective`：falsified 13，与 evidence MATCH；限定为 batch-local exact-origin injectivity。

### M模型

- `repeated_message_rejection_exists`：verified 4，与 evidence MATCH；弱 rejection reachability。
- `same_party_different_messages_batch_exists`：verified 16，与 evidence MATCH；核心非蕴含见证。
- `accepted_batch_has_distinct_messages`：verified 31，与 evidence MATCH；all-traces 消息区分。
- `receiver_accept_has_send`：verified 8，与 evidence MATCH。
- `receiver_accept_injective`：verified 33，与 evidence MATCH。

### P模型

- `same_party_rejection_exists`：verified 5，与 evidence MATCH；弱 rejection reachability。
- `distinct_party_batch_exists`：verified 17，与 evidence MATCH；只证明至少一个有效双接受执行。
- `accepted_batch_has_distinct_parties`：verified 31，与 evidence MATCH；正控制 safety。
- `receiver_accept_has_send`：verified 8，与 evidence MATCH。
- `receiver_accept_injective`：verified 33，与 evidence MATCH。

## 4. 第2章两处修订核对

1. $P_\tau$ 和 $M_\tau$ 已补全 $A_1,A_2,oid_1,oid_2,m_1,m_2,bid,rst,r_1,r_2$ 的全称量化，$r_1\ne r_2$ 位于蕴含前件；公式与模型 lemma 的变量及作用域一致。
2. source-to-model 表已把 K-Waay 密码失败与 M/P `Reject` 分开：前者在模型中无直接对应物，后者只表示消息或参与方接纳条件不满足，二者不能视为同一安全事件。
3. `git diff` 显示第 2 章只有上述两个 hunk，没有顺带改写其他段落。

## 5. 图2审查

- 图题中英文与任务指定文本一致。
- 设计只使用模型规则、`one_send_two_accepts_exists` 公式和对应 JSON graph 中出现的事件。
- 明确标注“根据 Tamarin 见证人工整理”。
- 图中只说该精确三元组有一个匹配 Send；没有删除导出 graph 中可能存在的无关 Send 这一事实。
- 未加入 key、应用、认证成功或部署攻击节点。

## 6. 本轮发现并修正的问题

1. **第2章量词缩写不完整**：按 Stage 3 指令改为完整全称量化，并把事件不等放入前件。
2. **第2章 Reject 映射可能造成等同误读**：改为“源密码失败无直接对应，模型 Reject 仅属接纳条件分支”。
3. **图注初稿含内部设计文件指针**：为保持正文的论文体例，已从正文图注删除文件路径；绘图细节仅保存在独立设计说明中。
4. **英文母稿 provenance 已过时**：第三章改用独立重跑事实，没有沿用“无 raw transcripts/未独立重跑”的旧描述。

## 7. 尚存但不由本阶段解决的问题

- 当前证据仍固定为两个槽位，没有任意批次大小的机器证明。
- $!Sent$ 是理想化 exact-origin fact，没有 receiver/prekey/context binding。
- 没有 K-Waay 到当前抽象的 simulation/refinement。
- M 的 message-level substitute 仍是受控比较变量，不是已证实的现实实现策略。
- K-Waay 对重复 party index 的输出和 `KEY/TEST` 扩展语义仍未建立。
- 两条 rejection lemma 仍缺少 rejected tuple binding。
- 图 2 当前完成的是可编辑设计规范，尚未进入正式 Word/矢量制图阶段。

## 8. 自检结论

第三章已形成完整中文论文初稿，14 项机器结果、三个核心见证、P/M/I 关系及独立复核 provenance 均有明确证据来源。未发现需要回退结果或改为 `NEEDS_REVISION` 的矛盾。

**SELF_REVIEW_PASS**
