# K-Waay Claim Hierarchy

## 1. Purpose and status vocabulary

This document freezes the names, scope, evidence, and non-claims used by the
K-Waay formal-analysis main line. It distinguishes protocol properties from
conditional composition properties and records actual tool results separately
from roadmap expectations.

Status terms in this document have the following meanings:

- `established`: the stated property, under the stated assumptions, has a model,
  a completed tool run, and a positive result.
- `falsified`: a completed tool run found a counterexample to the stated property.
- `partially modeled`: relevant models and results exist, but the variants,
  assumptions, or interfaces needed for the complete claim are not connected.
- `not modeled`: the required event, interface, or protocol variant does not exist.

The hierarchy is ordered by strictly increasing strength:

```text
P0 secrecy / component origin
  < P1 full-parameter non-injective correspondence
  < P2 injective one-send-one-accept
  < P3 unique session installation under an explicit composition interface
```

An established lower layer does not imply any higher layer.

## 2. P0: symbolic secrecy / component origin

### 2.1 Exact definition

P0 contains two distinct properties.

**P0-S: symbolic session-key secrecy.** For an honest role event carrying a
session key, the Dolev-Yao attacker cannot derive that exact key:

```proverif
attacker(k) && event(SenderKey(A,B,sid,k)) ==> false
attacker(k) && event(ReceiverKey(B,A,sid,k)) ==> false
```

**P0-O: split-KEM component origin.** Every accepted split-KEM component has a
matching honest sender-origin event with the same parties, ciphertext, and
component secret:

```proverif
event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks))
```

The Tamarin counterpart is slot-local and ordering-sensitive:

```text
BatchSlotAccept(B,bid,idx,A,rst,cts,Ks)
  with no early sender/receiver state compromise
  implies an earlier SenderComponent(A,B,rst,cts,Ks).
```

P0-S is secrecy, while P0-O is component authenticity. Neither property is
full-message agreement, replay prevention, or injective authentication.

### 2.2 Current status

`established`, restricted to the assumptions below.

Compromise targets are classification experiments and are not part of this
unqualified established baseline.

### 2.3 Protocol variants

- original Figure 7 core, no-batch/single-receive symbolic abstraction;
- HMAC confirmation variant, for regression of baseline secrecy and component origin;
- Tamarin V6 receiver/batch lifecycle abstraction;
- Tamarin V7 fixed four-slot lifecycle abstraction, only for its narrower
  component-origin/lifecycle scope.

### 2.4 Model files

- `proverif/kwaay_core_final.cpp.pv`
- `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`
- `tamarin/kwaay_splitkem_batch_dynamic_v6.spthy`
- `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`

### 2.5 Events, queries, and lemmas

- `SenderKey`, `ReceiverKey`
- `SenderSplitKemComponent`, `SplitKemAccepted`
- ProVerif sender/receiver secrecy queries
- `SplitKemAccepted ==> SenderSplitKemComponent`
- `slot_origin_without_early_compromise`
- `slot_key_known_requires_exception`
- `partnered_slot_key_not_attacker_known_without_early_compromise`
- V7 `slot_origin`, interpreted only inside the V7 abstraction

### 2.6 Actual results

- `BASELINE`: sender secrecy `true`; receiver secrecy `true`.
- `COMPONENT`: `SplitKemAccepted ==> SenderSplitKemComponent` is `true`.
- `HMAC_BASELINE`: sender secrecy `true`; receiver secrecy `true`.
- `HMAC_COMPONENT`: component-origin correspondence is `true`.
- V6: the three origin/exception lemmas listed above are `VERIFIED`.
- V7: `slot_origin` is `VERIFIED`.

Evidence:

- `logs/final/proverif/summary.txt`
- `logs/variants/hmac-confirmation/proverif/summary.txt`
- `logs/tamarin-v6/summary.txt`
- `logs/tamarin-v7/summary.txt`

The leak experiments have mixed results. In particular, receiver secrecy is
falsified by `LEAK_SIGSK_A`, `LEAK_SIGSK_AB`/`LEAK_SIGSK`, `LEAK_RSKEMSK`, and
`LEAK_SSKEMSK`. Therefore they must not be folded into the baseline theorem.

### 2.7 Assumptions

- active public-channel Dolev-Yao attacker;
- free symbolic constructors/destructors for the KEM, split-KEM, KDF, and signature abstractions;
- no leak process in the ProVerif `BASELINE` and `COMPONENT` targets;
- no early `CompromiseReceiverState(B,rst)` or
  `CompromiseSenderState(A,sst)` for the V6 origin and partnered-key lemmas;
- no computational claim about concrete primitives;
- no claim that the no-batch ProVerif process implements full `BatchReceive`.

### 2.8 Allowed paper statement

> In the no-compromise symbolic baseline, the ProVerif model establishes
> sender- and receiver-side session-key secrecy and split-KEM component origin.
> The Tamarin V6 model additionally establishes slot-level component origin and
> partnered-key secrecy in the absence of early sender or receiver state compromise.

### 2.9 Prohibited overstatements

Do not write:

- “K-Waay is secure under arbitrary key compromise.”
- “Component origin proves full-message authentication or agreement.”
- “Message authenticity prevents duplicate acceptance.”
- “The symbolic results prove computational KIND, UNF-1KMA, or IND-1BatchCCA.”
- “V7 proves compromise-resilient origin.” V7 does not replace V6's
  compromise/exception model.

### 2.10 Completion milestone

P0's current baseline is established. M4 must regress P0-S and P0-O across the
dedup-only and HMAC+dedup variants and record the exact compromise exceptions.
M5 must freeze the reproducible result table.

## 3. P1: full-parameter non-injective correspondence

### 3.1 Exact definition

For every receiver completion carrying `(B,A,sid,k)`, there exists a sender
completion carrying the exact reversed party order and the same `(sid,k)`:

```proverif
event(RecvDone(B,A,sid,k)) ==> event(SendDone(A,B,sid,k))
```

This is a non-injective correspondence. One `SendDone` may justify more than one
`RecvDone`. In the ProVerif models, `sid` is a free constructor over identities,
long-term public keys, both prekey bundles, and the complete
`m=(ct_l,ct_k,ct_s)`. “Full-parameter” therefore means the exact event tuple
`(A,B,sid,k)` in this symbolic model; it does not include an occurrence number,
batch slot, local session handle, or implementation state.

### 3.2 Current status

`partially modeled` across the paper main line:

- original Figure 7 core: `falsified`;
- HMAC confirmation, no-compromise baseline: `established`;
- HMAC under A signing-key compromise: `falsified`;
- HMAC plus batch-slot replay semantics: `not modeled`.

### 3.3 Protocol variants

- original Figure 7 core;
- HMAC confirmation;
- future HMAC-only replay bridge;
- future HMAC+dedup combined fix.

### 3.4 Model files

- `proverif/kwaay_core_final.cpp.pv`
- `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`
- no HMAC-only replay or combined model currently exists

### 3.5 Events and query

- `SendDone(A,B,sid,k)`
- `RecvDone(B,A,sid,k)`
- `RecvDone ==> SendDone`

Neither current ProVerif model contains an `inj-event` query.

### 3.6 Actual results

- `BASELINE`: `RecvDone ==> SendDone` is `false`.
- `HMAC_BASELINE`: the same query is `true`.
- `HMAC_LEAK_SIGSK_A`: the same query is `false`.

Evidence:

- `logs/final/proverif/summary.txt`
- `logs/variants/hmac-confirmation/proverif/summary.txt`

The roadmap expectation that HMAC confirmation still permits duplicate slot
acceptance is not an actual P1/P2 result. It remains an M1 hypothesis.

### 3.7 Assumptions

- original-core falsification already holds with no compromise;
- the HMAC positive result is restricted to `HMAC_BASELINE` with no leak process;
- the HMAC tag is `hmac(confirm_key(k),sid)` and is checked before
  `ReceiverKey`/`RecvDone`;
- compromise coverage for HMAC is limited to the single
  `HMAC_LEAK_SIGSK_A` experiment;
- no inference is made for untested receiver-key, ephemeral-state, or
  receiver-state compromise cases.

### 3.8 Allowed paper statement

> The original symbolic core does not satisfy exact non-injective
> correspondence on `(A,B,sid,k)`. Explicit HMAC key confirmation restores this
> correspondence in the no-compromise HMAC baseline, but the result does not
> provide injectivity or replay prevention and does not survive the modeled A
> signing-key compromise experiment.

### 3.9 Prohibited overstatements

Do not write:

- “HMAC proves injective agreement.”
- “HMAC prevents replay or duplicate BatchReceive outputs.”
- “The HMAC repair is proved under all compromise scenarios.”
- “P1 is full implementation-session agreement.”
- “The original P1 counterexample is a key-recovery attack.”

### 3.10 Completion milestone

M1 must connect HMAC confirmation to a two-slot replay model and separate
non-injective correspondence from injectivity. M4 must establish the combined
HMAC+dedup P1 result and regress the selected compromise cases. M5 must freeze
the final evidence.

## 4. P2: injective one-send-one-accept

### 4.1 Exact definition

Every matching receiver acceptance must correspond injectively to a unique
sender occurrence. Equivalently, one sender occurrence for the exact
`(A,B,m,sid,k)` coordinates must not justify two distinct receiver acceptances:

```text
SenderSession(A,B,m,sid,k) @ s
ReceiverAccept(B,A,bid,idx1,rst,m,sid,k) @ r1
ReceiverAccept(B,A,bid,idx2,rst,m,sid,k) @ r2
implies r1 = r2.
```

P2 is stronger than P1. A message can be authentic and satisfy a non-injective
correspondence while still being replayed into two batch slots.

### 4.2 Current status

`falsified` for replay original.

Positive P2 for dedup-only or HMAC+dedup is `not modeled`.

### 4.3 Protocol variants

- original, unhardened `BatchReceive` replay abstraction;
- future HMAC-only replay bridge;
- future dedup-only fixed model;
- future HMAC+dedup combined model.

### 4.4 Model file

- `tamarin/replay/kwaay_replay_original.spthy`

No HMAC-only replay, fixed, or combined model currently exists.

### 4.5 Events and lemmas

- `SenderSession(A,B,m,sid,k)`
- `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)`
- `one_send_two_accepts_exists`
- `same_message_accepted_at_most_once`
- `full_message_unique_send`
- `receiver_accept_has_sender`
- `injective_receiver_accept`
- `slot_indices_distinct`

### 4.6 Actual results

- `one_send_two_accepts_exists`: `verified`.
- `same_message_accepted_at_most_once`: `falsified - found trace`.
- `full_message_unique_send`: `verified`.
- `receiver_accept_has_sender`: `verified`.
- `injective_receiver_accept`: `falsified - found trace`.
- `slot_indices_distinct`: `verified`.
- all selected lifecycle/state-consumption lemmas in the same model terminate
  with the results recorded in `tamarin/replay/README.md`.

Evidence:

- `tamarin/replay/README.md`
- model lemmas in `tamarin/replay/kwaay_replay_original.spthy`

The repository currently lacks a committed raw replay `.out`/summary file; the
documented command and result table are therefore weaker artifact evidence than
the ProVerif and V6/V7 log directories.

### 4.7 Assumptions

- fixed two-slot symbolic batch;
- one matching honest `SenderSession` event;
- same `B,bid,rst,A,m,sid,k`, with distinct fresh slot indices;
- the witness reaches normal `BatchComplete`;
- no `CompromiseReceiverState` or `CompromiseSenderState` anywhere in the witness;
- successful decapsulation is abstracted by a persistent `HonestSession` relation;
- no HMAC, duplicate cache, `SeenSid`, session installation, or application state.

### 4.8 Allowed paper statement

> In the bounded original BatchReceive model, one complete honest message can
> be accepted in two distinct slots of the same batch and receiver state, with
> no sender or receiver state compromise and with normal batch completion.
> Thus one-send-one-accept injectivity is falsified in this abstraction.

### 4.9 Prohibited overstatements

Do not write:

- “The message is forged.” The witness reuses one authentic message.
- “Component authenticity prevents duplicate acceptance.”
- “The attack is cross-batch replay, rollback, or state reuse after close.”
- “HMAC has been proved replayable.” The HMAC-only bridge does not exist.
- “A fixed model proves injectivity.” No fixed model exists yet.
- “Duplicate receiver outputs prove duplicate installed sessions.” That is P3.

### 4.10 Completion milestone

M1 must test P2 in the HMAC-only replay bridge. M3 must establish positive P2
for the batch-local atomic dedup model. M4 must establish positive P2 for the
combined HMAC+dedup model and run lifecycle/P0 regressions. M5 must save raw,
reproducible evidence.

## 5. P3: unique session installation under an explicit composition interface

### 5.1 Exact definition

P3 is a conditional composition claim. It first requires an explicit upper-layer
interface such as:

```text
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
  -> InstallSession(B,handle,A,sid,k)
```

with a fresh local `handle` for every installation. Under that interface, unique
session installation requires that one sender occurrence cannot lead to two
installation events with the same peer, `sid`, and key but distinct local handles:

```text
InstallSession(B,h1,A,sid,k)
InstallSession(B,h2,A,sid,k)
same matching SenderSession
implies h1 = h2.
```

This is not a protocol-only claim. It is conditional on the modeled composition
rule that consumes receiver outputs.

### 5.2 Current status

`not modeled`.

### 5.3 Protocol variants

- future impact/composition model over replay original;
- future fixed impact model;
- future HMAC+dedup combined impact model.

### 5.4 Model files

No impact/composition model exists.

### 5.5 Events and lemmas

No `InstallSession`, session-handle event, `one_send_two_installs_exists`, or
`unique_install` lemma exists in the current non-archived models.

The only reusable lower-layer event is
`ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` in
`tamarin/replay/kwaay_replay_original.spthy`.

### 5.6 Actual results

None. The P3 event and lemma names in the roadmap are expected future names,
not observed tool results.

### 5.7 Assumptions required before the claim can be evaluated

- an explicit, documented receiver-output-to-installation interface;
- a fresh local handle for each installation;
- a stated policy for whether every successful slot output is installed;
- a clear distinction between protocol `sid` and local implementation handle;
- an explicit statement of whether the interface models K-Waay's specification,
  a real integration, or only a conditional consumer;
- selected compromise and state-reuse assumptions for the upper layer.

### 5.8 Allowed paper statement

Current allowed statement:

> The protocol-level replay model produces two equal `(sid,k)` receiver outputs.
> The effect on session installation is not yet modeled and remains conditional
> on an explicit upper-layer interface.

After M2, a stronger statement is allowed only in conditional form unless the
interface is justified from a specification or implementation.

### 5.9 Prohibited overstatements

Do not write:

- “K-Waay installs two sessions from one send.”
- “A session-cloning attack has been proved.”
- “Double Ratchet state is duplicated.”
- “Unique installation is falsified or established.”
- “The protocol itself mandates one installation per receiver accept,” unless
  supported by an external specification or implementation mapping.

### 5.10 Completion milestone

M2 must define the interface and evaluate the original duplicate-install trace.
M3 must connect the dedup repair to the same interface. M4 must establish the
combined result. M5 must freeze the interface assumptions and result logs.

## 6. Cross-layer rules

The following implications are explicitly forbidden:

```text
P0 secrecy                    does not imply P0 component origin
P0 component origin           does not imply P1 exact correspondence
P1 non-injective agreement    does not imply P2 injective agreement
authentic message origin      does not imply duplicate rejection
ReceiverAccept                does not imply InstallSession
two ReceiverAccept events     do not imply two installed sessions
protocol-level P2 failure     does not by itself prove implementation impact
roadmap expected result       is not an actual model result
```

The main-line evidence state at M0 is therefore:

```text
P0 baseline: established
P1 original: falsified
P1 HMAC baseline: established
P1 HMAC under A signing-key compromise: falsified
P2 original: falsified
P2 HMAC-only/fixed/combined: not modeled
P3: not modeled
```
