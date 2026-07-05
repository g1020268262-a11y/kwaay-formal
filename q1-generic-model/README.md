# 通用 Q1 分层诊断模型

这个文件夹是 `q1-analysis-model` 的通用化副本，用来分析不只 K-Waay 一类协议的 Q1 问题。

第一版通用模型选择 `ProVerif`，因为这里的主要任务是快速筛查 correspondence、secrecy 和 reachability。`Tamarin` 更适合后续对某个具体协议做有状态生命周期、batch state、消耗性状态、撤销、复杂时序或多阶段 lemma 的精细证明。

## 文件

- `q1_generic_triage.cpp.pv`：通用 ProVerif 模板。
- `run-q1-generic.sh`：批量运行脚本。

运行全部目标：

```bash
bash q1-generic-model/run-q1-generic.sh
```

运行单个目标：

```bash
bash q1-generic-model/run-q1-generic.sh AUTH_SECRET_Q1_GAP
```

输出摘要：

```text
logs/q1-generic-model/summary.txt
```

## 检测矩阵

可达性 sanity check：

```prolog
query k: session_key; event(HonestRun(k)).
```

检测什么：模型里是否真的存在至少一个接收方完成的 honest execution。

为什么需要：如果协议过程因为类型、验证条件或输入输出写错而根本跑不到 `RecvDone`，后面的 correspondence 查询可能会“真得很漂亮”，但那只是 vacuous truth。这个查询用来防止“没有执行路径，所以所有安全性质都成立”的假阳性。

怎么解释：ProVerif 输出 `RESULT not event(HonestRun(k)) is false` 才是好现象，表示 `HonestRun(k)` 可达。如果它是 `true`，说明模型不可执行，需要先修模型，不能继续解释 Q1 结果。

核心 Q1 查询：

```prolog
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))
```

检测什么：接收方 `B` 认为自己和 `A` 完成了会话 `(s,k)` 时，发送方 `A` 是否也确实完成过同一个 `(s,k)`。

为什么需要：这是 Q1 的主检测项，捕获 receiver-to-sender exact agreement 缺口。如果它失败，说明存在 unpartnered receiver session，也就是接收方完成的会话没有匹配发送方完成事件。

怎么解释：`true` 表示没有发现 Q1 缺口。`false` 表示存在 Q1 缺口，但还不能直接说有实际危害；需要继续看 key、origin、context、data 和 side effect 查询。

密钥保密：

```prolog
attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false
```

检测什么：攻击者是否能知道接收方已经接受的会话密钥 `k`。

为什么需要：很多 Q1 争议的核心是“攻击者能不能让接收方接受一个攻击者知道的 key”。如果这个查询失败，Q1 不再只是 agreement gap，而是实际 key compromise。

怎么解释：`true` 表示所有接收方接受的 key 都没有被攻击者知道。`false` 表示攻击者能知道某个接收方接受的 key，应分类为有害 Q1。

受保护数据保密：

```prolog
attacker(d) && event(ProtectedData(B,A,s,d)) ==> false
```

检测什么：接收方用已接受 key 保护的应用数据 `d` 是否会泄露。

为什么需要：严格的理想加密模型里，key secrecy 往往能推出数据保密，但通用模板不能默认协议一定正确使用 key。显式检查数据保密可以捕获错误派生、错误输出、错误绑定或 key 已知导致的实际数据泄露。

怎么解释：`true` 表示该抽象下受保护数据不泄露。`false` 表示 Q1 或相关建模路径已经导致应用数据泄露，属于直接危害。

发送方来源认证：

```prolog
event(OriginComponentAccepted(B,A,co,so))
  ==> event(OriginComponentSent(A,B,co,so))
```

检测什么：接收方接受的发送方来源认证分量 `co` 及其 secret `so` 是否真的由发送方 `A` 发送给 `B`。

为什么需要：key 不泄露不等于发送方来源正确。如果接收方能接受攻击者伪造的 origin component，那么协议可能存在 impersonation、unknown-origin 或错误认证路径。

怎么解释：`true` 表示接收方接受的来源认证分量都有真实发送方来源。`false` 表示来源认证失败，Q1 具有认证层危害。

身份上下文一致：

```prolog
event(ReceiverIdentityContext(B,A,peer,local))
  ==> event(SenderIdentityContext(A,B,peer,local))
```

检测什么：接收方记录的对端身份、本端身份是否和发送方承诺的身份一致。

为什么需要：这用于捕获 unknown-key-share、身份绑定缺失、把同一个 key 绑定到不同 peer 的错误。很多协议即使 key 不泄露，也可能因为身份上下文不一致而失败。

怎么解释：`true` 表示身份上下文一致。`false` 表示接收方和发送方对“这是谁和谁的会话”理解不同，应分类为稳定语义上下文攻击。

角色上下文一致：

```prolog
event(ReceiverRoleContext(B,A,sr,rr))
  ==> event(SenderRoleContext(A,B,sr,rr))
```

检测什么：发送方角色、接收方角色是否被双方一致绑定。

为什么需要：如果 KDF、sid 或 transcript 没有绑定 initiator/responder、sender/receiver 等角色，协议可能出现 reflection 或 role confusion。此类问题不一定导致 key 泄露，但会破坏认证语义。

怎么解释：`true` 表示角色绑定一致。`false` 表示存在角色混淆，应分类为有害上下文攻击。

算法套件上下文一致：

```prolog
event(ReceiverSuiteContext(B,A,suite))
  ==> event(SenderSuiteContext(A,B,suite))
```

检测什么：双方对算法套件、协议模式或安全等级的理解是否一致。

为什么需要：协议如果没有把 suite/mode 绑定进 transcript、sid 或 KDF，攻击者可能做 downgrade、cross-suite confusion 或跨模式重放。key secrecy 成立也不能排除这种协商语义攻击。

怎么解释：`true` 表示算法套件上下文一致。`false` 表示存在降级或跨套件混淆风险，应分类为有害上下文攻击。

应用上下文一致：

```prolog
event(ReceiverApplicationContext(B,A,app))
  ==> event(SenderApplicationContext(A,B,app))
```

检测什么：业务场景、channel binding、群组上下文、用途分离标签等应用层上下文是否一致。

为什么需要：同一个密码学握手在不同应用上下文里可能有完全不同含义。如果 app context 未绑定，攻击者可能把一个上下文中的会话搬到另一个上下文里使用，造成 confused deputy 或跨协议/跨业务攻击。

怎么解释：`true` 表示应用上下文一致。`false` 表示接收方接受的会话被绑定到了发送方未承诺的应用语义，属于有害上下文攻击。

稳定语义上下文一致：

```prolog
event(ReceiverStableContext(B,A,sc))
  ==> event(SenderStableContext(A,B,sc))
```

检测什么：身份、角色、算法套件、应用上下文这些稳定语义字段作为整体是否一致。

为什么需要：单个维度查询用于定位问题，`stable_context` 查询用于给出总括判断。它回答“除了可被重组的 transcript 细节之外，双方对这次会话的稳定语义是否一致”。

怎么解释：`true` 表示稳定语义一致。`false` 表示至少一个稳定语义维度不一致；需要回看 identity、role、suite、app 中哪个维度失败。

完整 transcript 一致：

```prolog
event(ReceiverFullContext(B,A,fc))
  ==> event(SenderFullContext(A,B,fc))
```

检测什么：接收方接受的完整上下文，包括稳定语义、凭据和完整 transcript，是否完全等于发送方承诺过的完整上下文。

为什么需要：这是 stronger-than-harmlessness 的 exact transcript agreement。它能明确显示是否存在 transcript 重组、替换或 replay 导致的 full agreement 缺口。

怎么解释：`true` 表示完整上下文也能匹配发送方完成。`false` 表示 full transcript agreement 失败。注意：K-Waay-like 的重组型 Q1 gap 预期会让 full-context 查询失败，但如果 identity、role、suite、app、origin、key/data secrecy 都成立，而且没有授权副作用，则仍可论证为 harmless agreement gap。

授权副作用：

```prolog
event(AuthorizedAction(B,A,s,k)) ==> event(SendDone(A,B,s,k))
```

检测什么：接收方执行的授权动作是否一定有匹配的发送方完成事件。

为什么需要：很多协议的 Q1 危害不体现在 key 泄露，而体现在接收方把“我接受了会话”当成“发送方授权了某个动作”。例如提交状态、加入群组、扣款、发布消息、确认交易。只看 key secrecy 会漏掉这类语义攻击。

怎么解释：`true` 表示所有授权副作用都有匹配发送方完成。`false` 表示接收方能在没有匹配 `SendDone` 的情况下执行授权动作，即使 key 不泄露也应判为有害。

确认修复：

```prolog
event(RecvDone(B,A,s,k)) ==> event(Confirmed(B,A,s,k))
event(Confirmed(B,A,s,k)) ==> event(SendDone(A,B,s,k))
```

检测什么：接收方完成是否必须经过显式确认，以及确认事件是否必然来自匹配发送方完成。

为什么需要：这是修复验证，不是危害检测。它用于检查加入 key/sid/transcript 绑定的 MAC、AEAD confirmation、signature confirmation 或 key confirmation 后，Q1 是否被消除。

怎么解释：两个查询都为 `true` 时，说明确认机制在该抽象中阻止了未匹配接收方完成。若第一个失败，表示接收方仍可能绕过确认完成；若第二个失败，表示确认本身没有可靠绑定到发送方完成。

## 抽象接口

模型把协议拆成几个可替换部件：

- `mutable_ct`：攻击者可替换、重组、重放的公开 transcript 分量，例如普通 KEM ciphertext、DH share、nonce 或未认证扩展字段。
- `origin_ct`：应该带有发送方来源认证的分量，例如签名绑定分量、sender-authenticated KEM、静态 DH 认证分量。
- `origin_credential`：接收方用来判断 `origin_ct` 是否属于发送方 `A` 的凭据。
- `receiver_credential`：发送方用来向接收方 `B` 封装或派生材料的凭据。
- `stable_ctx(...)`：稳定语义上下文，包含身份、角色、算法套件和应用上下文。
- `full_ctx(...)`：完整上下文，包含稳定语义上下文、凭据和完整 transcript。
- `sid_of(...)`：会话标识，应该包含身份、凭据和 transcript。
- `key_mixed(...)`：最终 key 同时混入可变分量和来源认证分量。
- `key_public_only(...)`：危险变体，最终 key 只依赖攻击者可选择的公开分量。
- `AuthorizedAction(...)`：接收方接受后触发的上层副作用，例如授权、提交、扣款、群组状态变更。

迁移新协议时，需要明确：

1. 哪些 transcript 分量可由攻击者替换但接收方仍会处理。
2. 哪些分量真正提供发送方来源认证。
3. 最终 key 是否混入攻击者不知道的来源认证 secret。
4. `sid` 和 KDF 是否绑定身份、角色、算法套件、应用上下文、凭据和 transcript。
5. 接收方接受后是否会产生“发送方授权”含义。
6. 是否有 key/sid/transcript 绑定的确认、MAC、AEAD confirmation 或签名确认。

## 目标场景

`AUTH_SECRET_Q1_GAP` 是通用的“无害 Q1 缺口”类。攻击者能替换 `mutable_ct` 并复用真实 `origin_ct`，所以 Q1 和 full-context 查询失败；但 key/data secrecy、origin、identity、role、suite、app、stable context 都成立。

`PUBLIC_ONLY_BAD` 表示最终 key 只依赖攻击者可选择的公开/可变分量。此时 Q1 失败会升级成 key secrecy 失败和数据泄露。

`NO_ORIGIN_AUTH_BAD` 表示接收方没有验证发送方来源凭据。攻击者可以把自己的 `fakeOriginPk()` 当成 `A` 的来源 key，使接收方接受没有真实发送方来源的 `origin_ct`。

`IDENTITY_CONTEXT_BAD` 表示接收方记录的对端身份和发送方承诺的身份不一致。它用于捕获 unknown-key-share 或身份绑定缺失。

`ROLE_CONTEXT_BAD` 表示发送方/接收方角色未正确绑定。它用于捕获 role confusion。

`SUITE_CONTEXT_BAD` 表示算法套件或协商模式未正确绑定。它用于捕获 downgrade 或 cross-suite confusion。

`APP_CONTEXT_BAD` 表示应用上下文未正确绑定。它用于捕获 channel binding、业务上下文、群组上下文或用途分离失败。

`SIDE_EFFECT_BAD` 表示 key 本身仍安全，但接收方把 `RecvDone` 当成发送方授权事件。这种情况下 Q1 仍然有害。

`CONFIRMED_FIX` 表示发送方输出绑定 `sid/key` 的确认标签，接收方验证后才 `RecvDone`。在这个抽象中，Q1 和 full-context agreement 都恢复为真。

## 结论分类

- Q1 `true`：没有发现接收方到发送方 exact-agreement 缺口。
- Q1 `false`，full-context `false`，但 key/data secrecy、origin、identity、role、suite、app、stable context 都 `true`，且没有授权副作用：可论证为 harmless Q1 agreement gap。
- Q1 `false` 且 key/data secrecy 为 `false`：有实际机密性攻击。
- Q1 `false` 且 origin correspondence 为 `false`：发送方来源认证失败。
- Q1 `false` 且 identity/role/suite/app 任一维度为 `false`：存在稳定语义上下文攻击。
- Q1 `false` 且授权副作用查询为 `false`：即使 key 不泄露，也有协议语义攻击。
- `CONFIRMED_FIX` 下 Q1 和 confirmation queries 都为 `true`：说明确认机制在该抽象中修复了 Q1。
