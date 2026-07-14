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

These claims form a property and dependency structure, not a global security
ladder:

```text
P0-S  symbolic session-key secrecy                  independent property
P0-O  split-KEM component origin                    independent property
P1    non-injective correspondence                  artifact/event-tuple scoped
P2    matching existence/order + occurrence         artifact/event-tuple scoped
      injectivity
P3 under C_install                                  impact/composition property
```

The only positive implication frozen at M0 is:

```text
P2 => P1
```

This implication is valid only within the same artifact instantiation, event
semantics, and parameter tuple. In particular, it does not identify ProVerif's
`SendDone`/`RecvDone` with Tamarin replay's
`SenderSession`/`ReceiverAccept`. P0-S and P0-O are independent of P1/P2, and
P3 under `C_install` is a conditional impact claim rather than a stronger
authentication level.

## 2. P0-S and P0-O: symbolic secrecy and component origin

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

- P0-S: `established` for the named ProVerif and HMAC no-compromise baselines.
- P0-O: `established` for the named ProVerif/HMAC component targets and the
  stated V6/V7 abstractions.

The ProVerif component targets currently have cross-target non-vacuity support:
the shared protocol process is reachable through the corresponding baseline
`HonestRun`, but the component-only target has no target-local reachability
query. Compromise targets are classification experiments and are not part of
either unqualified established baseline.

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

For one fixed artifact and event vocabulary, define the matching relation over
the two events with their actual, different parameter lists:

```text
Match(
  SenderSession(A,B,m,sid,k) @ s,
  ReceiverAccept(B,A,bid,idx,rst,m,sid,k) @ r
)
```

The common protocol matching coordinates are:

```text
(A,B,m,sid,k)
```

The receiver-side occurrence context is:

```text
(bid,idx,rst)
```

`Match` compares the common protocol coordinates, including the reversed role
order in the receiver event. It does not pretend that sender and receiver
events have one identical event tuple. P2 is the conjunction of two safety
conditions over this relation.

First, matching existence and order:

```text
for every ReceiverAccept(B,A,bid,idx,rst,m,sid,k) @ r,
there exists SenderSession(A,B,m,sid,k) @ s such that
Match(SenderSession @ s, ReceiverAccept @ r) and s < r.
```

Second, occurrence injectivity:

```text
for every sender occurrence S @ s and receiver occurrences R1 @ r1, R2 @ r2,
Match(S @ s, R1 @ r1) and Match(S @ s, R2 @ r2)
imply r1 = r2.
```

The current replay lemma `injective_receiver_accept` is narrower than this
global occurrence-injectivity schema. It directly quantifies one shared `bid`,
one shared `rst`, and two potentially different `idx1,idx2`. Its exact scope is
therefore same-batch/same-receiver-state occurrence injectivity.

The falsified same-batch/same-state lemma is nevertheless sufficient to
falsify the stronger global one-send-one-accept property: the trace contains
two different receiver occurrences in a subset of the global property's
quantification domain. The converse does not hold. A future positive
same-batch/same-state lemma alone would not establish injectivity across
arbitrary batches or receiver states.

Normal-path executability/non-vacuity is required evidence before either
condition is reported as a meaningful result; it is not a conjunct of the P2
safety formula. Within the same instantiation, P2 implies P1. No such
implication is inferred across the ProVerif and replay event vocabularies.

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

### 4.5 Events and evidence roles

- `SenderSession(A,B,m,sid,k)`
- `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)`

| Evidence role | Query / lemma | Actual result |
|---|---|---|
| matching existence/order | `receiver_accept_has_sender` | `verified` |
| same-batch/same-receiver-state occurrence injectivity | `injective_receiver_accept` | `falsified - found trace` |
| normal-path executability | `normal_single_accept` | `verified` |
| lifecycle sanity | `normal_batch_complete` | `verified` |
| attack witness | `one_send_two_accepts_exists` | `verified` |

Supporting replay lemmas are `same_message_accepted_at_most_once`,
`full_message_unique_send`, and `slot_indices_distinct`.

### 4.6 Actual results

- `one_send_two_accepts_exists`: `verified`.
- `same_message_accepted_at_most_once`: `falsified - found trace`.
- `full_message_unique_send`: `verified`.
- `receiver_accept_has_sender`: `verified`.
- `injective_receiver_accept`: `falsified - found trace`.
- `slot_indices_distinct`: `verified`.
- `normal_single_accept`: `verified`.
- `normal_batch_complete`: `verified`.
- all selected lifecycle/state-consumption lemmas in the same model terminate
  with the results recorded in `tamarin/replay/README.md`.

Evidence:

- `tamarin/replay/README.md`
- model lemmas in `tamarin/replay/kwaay_replay_original.spthy`

Thus global P2 is `falsified` because occurrence injectivity already fails in
the same-batch/same-receiver-state subdomain. Matching existence/order and
normal-path executability both hold in the replay abstraction; they are not the
failure point. No positive global injectivity theorem is present.

The repository currently lacks a committed raw replay `.out`/summary file; the
documented command and result table are therefore weaker artifact evidence than
the ProVerif and V6/V7 log directories.

### 4.7 Assumptions

- fixed two-slot symbolic batch;
- one matching honest `SenderSession` event;
- matching coordinates `(A,B,m,sid,k)`;
- same receiver-side `B,bid,rst`, with distinct fresh slot indices `idx1,idx2`;
- the witness reaches normal `BatchComplete`;
- no `CompromiseReceiverState` or `CompromiseSenderState` anywhere in the witness;
- successful decapsulation is abstracted by a persistent `HonestSession` relation;
- no HMAC, duplicate cache, `SeenSid`, session installation, or application state.

### 4.8 Allowed paper statement

> In the bounded original BatchReceive model, one complete honest message can
> be accepted in two distinct slots of the same batch and receiver state, with
> no sender or receiver state compromise and with normal batch completion.
> This same-batch/same-state counterexample is sufficient to falsify the
> stronger global one-send-one-accept property, without claiming that the
> model supplies a positive theorem over arbitrary batches or states.

### 4.9 Prohibited overstatements

Do not write:

- “The message is forged.” The witness reuses one authentic message.
- “Component authenticity prevents duplicate acceptance.”
- “The attack is cross-batch replay, rollback, or state reuse after close.”
- “HMAC has been proved replayable.” The HMAC-only bridge does not exist.
- “A fixed model proves injectivity.” No fixed model exists yet.
- “Duplicate receiver outputs prove duplicate installed sessions.” That would be
  P3 under `C_install`, which is not modeled.

### 4.10 Completion milestone

M1 must test the same-batch/same-receiver-state P2 condition in the HMAC-only
replay bridge. M3 and M4 must state whether their positive injectivity lemmas
remain batch/state scoped or explicitly quantify across batches and receiver
states; a same-batch positive result must not be relabeled as global P2. M3
owns the batch-local atomic dedup model, M4 owns the combined HMAC+dedup model
and lifecycle/P0 regressions, and M5 must save raw reproducible evidence.

## 5. P3 under C_install: unique session installation

### 5.1 Exact definition and named composition assumption

P3 under `C_install` is a conditional composition claim. `C_install` names the
future M2 receiver-output-to-installation interface and freezes all of the
following assumptions:

1. Every `InstallSession(B,h,A,sid,k)` has an earlier
   `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` with the complete matching tuple.
2. Every `ReceiverAccept` occurrence triggers exactly one later
   `InstallSession` occurrence through the designated composition interface.
3. Every installation generates a fresh local handle `h`; distinct installation
   occurrences therefore have distinct handles.
4. `InstallSession` can be produced only by that named interface; there is no
   out-of-interface or ex nihilo installation rule.
5. A normal one-accept-one-install trace is reachable.

The intended future interface has the shape:

```text
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
  -> InstallSession(B,handle,A,sid,k)
```

Under `C_install`, unique session installation requires that one sender
occurrence cannot lead to two installation events with the same peer, `sid`,
and key but distinct local handles:

```text
InstallSession(B,h1,A,sid,k)
InstallSession(B,h2,A,sid,k)
same matching SenderSession
implies h1 = h2.
```

This is not a protocol-only claim or an authentication rank. It is conditional
on all of `C_install`. The assumptions are frozen now for naming only; their
events, rules, executability, and result are future M2 work.

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

None. P3 under `C_install` is `not modeled`. Its event and lemma names in the
roadmap are expected future names, not observed tool results.

### 5.7 Assumptions required before the claim can be evaluated

- every clause of `C_install` must be represented and checked in M2;
- protocol `sid` must remain distinct from the fresh local handle;
- the document must state whether the interface represents K-Waay's
  specification, a real integration, or only a conditional consumer;
- selected compromise and state-reuse assumptions for the upper layer must be
  explicit.

### 5.8 Allowed paper statement

Current allowed statement:

> The protocol-level replay model produces two equal `(sid,k)` receiver outputs.
> P3 under `C_install` is not modeled; any installation impact remains
> conditional on the explicitly named future composition interface.

After M2, a stronger statement is allowed only in conditional form unless the
interface is justified from a specification or implementation.

### 5.9 Prohibited overstatements

Do not write:

- “K-Waay installs two sessions from one send.”
- “A session-cloning attack has been proved.”
- “Double Ratchet state is duplicated.”
- “P3 under `C_install` is falsified or established.”
- “The protocol itself mandates one installation per receiver accept,” unless
  supported by an external specification or implementation mapping.

### 5.10 Completion milestone

M2 must implement `C_install` and evaluate the original duplicate-install trace.
M3 must connect the dedup repair to the same interface. M4 must establish the
combined result. M5 must freeze the interface assumptions and result logs.

## 6. Property and dependency rules

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

The only frozen positive dependency is:

```text
P2 => P1, only for the same artifact instantiation, event semantics,
          and matching parameter tuple.
```

The main-line evidence state at M0 is therefore:

```text
P0 baseline: established
P1 original: falsified
P1 HMAC baseline: established
P1 HMAC under A signing-key compromise: falsified
P2 Tamarin replay original: falsified
P2 HMAC-only/fixed/combined: not modeled
P3 under C_install: not modeled
```
