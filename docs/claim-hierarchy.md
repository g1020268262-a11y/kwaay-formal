# K-Waay Claim Hierarchy

> **Authority notice.** This document is the frozen M0-M5 historical claim
> hierarchy. It records the historical M0-M5 formal exploration and is not
> the current RQ-v2 claim authority. Current RQ-v2 authority is
> [`docs/rq-v2/`](rq-v2/).

## 1. Purpose and status vocabulary

This document freezes the names, scope, evidence, and non-claims used by the
historical M0-M5 formal exploration. It distinguishes protocol properties from
conditional composition properties and records actual tool results separately
from historical roadmap expectations. Every status and allowed/prohibited
statement below is scoped to that frozen historical artifact.

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

### 2.2 Historical artifact status

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

P0's current ProVerif baseline remains established through the previously
committed original core and HMAC confirmation evidence. M4's new evidence is
Tamarin-only and therefore does not rerun the five ProVerif targets. M5 now
freezes the final reproducible tables in `artifact/results/actual-results.tsv`
and `artifact/results/claim-matrix.tsv` without describing M4 Evidence Commit B
as a ProVerif rerun.

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

### 3.2 Historical artifact status

`partially modeled` across the paper main line:

- original Figure 7 core: `falsified`;
- HMAC confirmation, no-compromise ProVerif baseline: `established`;
- HMAC under A signing-key compromise: `falsified`;
- HMAC-only two-slot Tamarin bridge: matching existence/order `established`,
  while same-batch/same-state occurrence injectivity is `falsified`.
  Because receiver processing requires persistent `HonestSession`, the bridge's
  matching-existence result is mainly structural; ProVerif remains the main
  independent evidence for HMAC P1.
- dedup-only fixed replay: does not model or restore the original ProVerif P1
  event/query; it establishes only its own batch-local P2 result;
- HMAC+dedup combined P1: no new ProVerif run in M4; the Tamarin combined
  artifacts establish confirmed-send/confirmed-accept matching and occurrence
  boundaries in their own event vocabulary, while the paper-level ProVerif P1
  statement continues to cite the prior HMAC confirmation baseline.

### 3.3 Protocol variants

- original Figure 7 core;
- HMAC confirmation;
- HMAC-only two-slot replay bridge;
- dedup-only fixed two-slot replay (P2 only, not a ProVerif P1 repair);
- actual HMAC+dedup combined fix.

### 3.4 Model files

- `proverif/kwaay_core_final.cpp.pv`
- `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`
- `tamarin/replay/kwaay_replay_hmac_only.spthy`
- `tamarin/replay/kwaay_replay_hmac_dedup.spthy`
- `tamarin/impact/kwaay_impact_hmac_dedup.spthy`

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

The HMAC-only Tamarin bridge now adds actual occurrence evidence:

- `confirmed_receiver_accept_has_sender`: `verified`;
- `confirmed_message_unique_send`: `verified`;
- `one_confirmed_send_two_accepts_exists`: `verified`;
- `injective_confirmed_receiver_accept`: `falsified - found trace`.

These results do not replace the ProVerif HMAC P1 theorem. In the bridge,
`ConfirmedReceiverAccept` structurally consumes a persistent
`HonestSession(A,B,rst,m,sid,k)` source relation, so matching existence/order is
mainly a source-event mapping result. The bridge establishes replay/occurrence
behavior for a confirmed message, not concrete HMAC-origin or computational
security.

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

M1 is complete: the HMAC-only bridge separates structural matching existence
from falsified same-batch/same-state occurrence injectivity and preserves the
ProVerif HMAC baseline as the main independent P1 evidence. M4 is complete as a
Tamarin-only combined HMAC+dedup result: it validates confirmed
send/confirmed-accept matching and duplicate rejection in the combined event
vocabulary, but it does not rerun ProVerif. M5 has frozen the final paper
artifact while keeping the ProVerif/Tamarin evidence roles distinct.

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
events have one identical event tuple.

In the current replay artifact, interpreting the common tuple
`(A,B,m,sid,k)` as identifying one sender occurrence relies on the verified
lemma `full_message_unique_send`: two `SenderSession` events carrying the same
complete sender tuple must have the same timepoint. Thus, only in this artifact
and together with that lemma, same complete sender tuple identifies the same
`SenderSession` occurrence. `full_message_unique_send` is matching
disambiguation, not P2 injectivity and not replay prevention.

P2 is the conjunction of two safety conditions over the `Match` relation.

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

Matching-accept executability/non-vacuity is required evidence before either
condition is reported as a meaningful result; it is not a conjunct of the P2
safety formula. The current `normal_single_accept` exists-trace establishes
only that at least one honest `SenderSession` and one later matching
`ReceiverAccept` are reachable. It does not exclude additional
`ReceiverAccept` events in the same trace. Within the same instantiation, P2
implies P1. No such implication is inferred across the ProVerif and replay
event vocabularies.

### 4.2 Historical artifact status

`falsified` for both replay original and the HMAC-only replay bridge in the
same-batch/same-receiver-state subdomain.

P2 is `established` for the dedup-only fixed two-slot model and for the M4
HMAC+dedup combined replay model, strictly within the same `B,bid,rst` and exact
complete base message `m` scope. This is a batch-local result, not a global or
cross-batch replay theorem.

### 4.3 Protocol variants

- original, unhardened `BatchReceive` replay abstraction;
- HMAC-only two-slot replay bridge;
- actual dedup-only fixed two-slot model;
- actual HMAC+dedup combined model.

### 4.4 Model file

- `tamarin/replay/kwaay_replay_original.spthy`
- `tamarin/replay/kwaay_replay_hmac_only.spthy`
- `tamarin/replay/kwaay_replay_fixed.spthy`
- `tamarin/replay/kwaay_replay_hmac_dedup.spthy`

### 4.5 Events and evidence roles

Original events:

- `SenderSession(A,B,m,sid,k)`
- `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)`

HMAC-only bridge events:

- `ConfirmedSend(A,B,m,sid,k,tag)`
- `ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)`

The HMAC matching coordinates are `(A,B,m,sid,k,tag)`; its receiver occurrence
context is `(bid,idx,rst)`.

| Artifact | Evidence role | Query / lemma | Actual result |
|---|---|---|---|
| original | matching existence/order | `receiver_accept_has_sender` | `verified` |
| original | sender-occurrence disambiguation | `full_message_unique_send` | `verified` |
| original | same-batch/same-state occurrence injectivity | `injective_receiver_accept` | `falsified - found trace` |
| original | matching-accept non-vacuity | `normal_single_accept` | `verified` |
| original | lifecycle sanity | `normal_batch_complete` | `verified` |
| original | attack witness | `one_send_two_accepts_exists` | `verified` |
| HMAC-only | matching existence/order | `confirmed_receiver_accept_has_sender` | `verified` |
| HMAC-only | sender-occurrence disambiguation | `confirmed_message_unique_send` | `verified` |
| HMAC-only | same-batch/same-state occurrence injectivity | `injective_confirmed_receiver_accept` | `falsified - found trace` |
| HMAC-only | confirmed message at-most-once | `confirmed_message_accepted_at_most_once` | `falsified - found trace` |
| HMAC-only | matching-accept non-vacuity | `normal_confirmed_single_accept` | `verified` |
| HMAC-only | lifecycle sanity | `normal_confirmed_batch_complete` | `verified` |
| HMAC-only | attack witness | `one_confirmed_send_two_accepts_exists` | `verified` |
| dedup-only fixed | matching existence/order | `receiver_accept_has_sender` | `verified` |
| dedup-only fixed | sender-occurrence disambiguation | `full_message_unique_send` | `verified` |
| dedup-only fixed | same-`B,bid,rst` exact-message occurrence injectivity | `injective_receiver_accept` | `verified` |
| dedup-only fixed | exact-message at-most-once | `same_message_accepted_at_most_once` | `verified` |
| dedup-only fixed | legacy duplicate witness | `one_send_two_accepts_exists` | `falsified` |
| dedup-only fixed | duplicate failure non-vacuity | `duplicate_batch_fail_exists` | `verified` |
| dedup-only fixed | duplicate has no accept | `duplicate_batch_has_no_accept` | `verified` |
| dedup-only fixed | distinct completion non-vacuity | `normal_distinct_batch_complete` | `verified` |
| M4 HMAC+dedup combined replay | matching existence/order | `confirmed_receiver_accept_has_sender` | `verified` |
| M4 HMAC+dedup combined replay | sender-occurrence disambiguation | `confirmed_message_unique_send` | `verified` |
| M4 HMAC+dedup combined replay | same-`B,bid,rst` occurrence injectivity | `injective_confirmed_receiver_accept` | `verified` |
| M4 HMAC+dedup combined replay | confirmed-message at-most-once | `confirmed_message_accepted_at_most_once` | `verified` |
| M4 HMAC+dedup combined replay | confirmed base-message at-most-once | `confirmed_base_message_accepted_at_most_once` | `verified` |
| M4 HMAC+dedup combined replay | legacy duplicate witness | `one_confirmed_send_two_accepts_exists` | `falsified` |
| M4 HMAC+dedup combined replay | same-base/different-tag duplicate rejection | `duplicate_same_base_different_tag_fail_exists` | `verified` |
| M4 HMAC+dedup combined replay | normal distinct-message completion | `normal_two_distinct_valid_confirmed_accepts_complete` | `verified` |

The original, HMAC-only, dedup-only fixed, and M4 combined replay artifacts also
verify their selected slot/lifecycle lemmas. The combined replay model is
`tamarin/replay/kwaay_replay_hmac_dedup.spthy`, and the M4 results above come
from Evidence Commit B's frozen Tamarin-only composite vector.

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

HMAC-only actual results:

- `normal_confirmed_single_accept`: `verified` (12 steps).
- `normal_confirmed_batch_complete`: `verified` (18 steps).
- `confirmed_receiver_accept_has_sender`: `verified` (16 steps).
- `confirmed_message_unique_send`: `verified` (2 steps).
- `one_confirmed_send_two_accepts_exists`: `verified` (17 steps).
- `confirmed_message_accepted_at_most_once`: `falsified - found trace` (15 steps).
- `injective_confirmed_receiver_accept`: `falsified - found trace` (15 steps).
- all 11 selected lifecycle/state-consumption lemmas: `verified`.

Dedup-only fixed actual results:

- `one_send_two_accepts_exists`: `falsified`.
- `same_message_accepted_at_most_once`: `verified`.
- `injective_receiver_accept`: `verified`.
- `duplicate_batch_fail_exists`: `verified`.
- `duplicate_batch_has_no_accept`: `verified`.
- `normal_distinct_batch_complete`: `verified`.
- `normal_distinct_fail_slot1_exists`: `verified`.
- `normal_distinct_fail_slot2_exists`: `verified`.
- all 30 fixed replay targets have expected terminal results in the transparent
  composite vector.

M4 HMAC+dedup combined replay actual results:

- `confirmed_receiver_accept_has_sender`: `verified`.
- `confirmed_message_unique_send`: `verified`.
- `injective_confirmed_receiver_accept`: `verified`.
- `confirmed_message_accepted_at_most_once`: `verified`.
- `confirmed_base_message_accepted_at_most_once`: `verified`.
- `one_confirmed_send_two_accepts_exists`: `falsified`.
- `duplicate_same_base_different_tag_fail_exists`: `verified`.
- `normal_two_distinct_valid_confirmed_accepts_complete`: `verified`.
- M4 transparent composite evidence is 296/296 terminal and 296/296 MATCH, with
  0 terminal conflicts, 0 unresolved rows, and 0 mismatches. This 296/296 result
  is the transparent composite result, not the result of any single source run.

Evidence:

- `tamarin/replay/README.md`
- `tamarin/replay/README-hmac-only.md`
- model lemmas in `tamarin/replay/kwaay_replay_original.spthy`
- model lemmas in `tamarin/replay/kwaay_replay_hmac_only.spthy`
- `logs/tamarin-replay-hmac-only/summary.txt`
- `logs/tamarin-replay-hmac-only/raw.out`
- `logs/tamarin-replay-hmac-only/attack-trace.out`
- `logs/tamarin-replay-hmac-only/original-regression-summary.txt`
- `logs/tamarin-replay-hmac-only/hmac-baseline-regression-summary.txt`
- `tamarin/replay/README-fixed.md`
- `logs/tamarin-m3-closeout/`
- `docs/milestones/M3-completion.md`
- `tamarin/replay/kwaay_replay_hmac_dedup.spthy`
- `tamarin/replay/README-hmac-dedup.md`
- `logs/tamarin-m4-hmac-dedup/`
- `docs/milestones/M4-completion.md`

Thus global P2 is `falsified` for original and HMAC-only because occurrence
injectivity already fails in their same-batch/same-receiver-state subdomain. Matching
existence/order and matching-accept executability hold; they are not the failure
point. The HMAC bridge's `confirmed_message_unique_send` disambiguates the
sender occurrence but does not provide P2 injectivity or replay prevention.
No positive global injectivity theorem is present. The fixed and M4 combined
positive results are only same-`B,bid,rst`, exact-complete-base-message-`m`,
fixed-two-slot injectivity results; they cannot be lifted to cross-batch,
rollback, restart, arbitrary-state, or arbitrary-length replay safety. The M4
combined result uses `ConfirmedSend` / `ConfirmedReceiverAccept` events, and
its dedup identity is the base message `m`, not the complete `<m,tag>` wrapper.

The M1 evidence bundle contains committed full raw output, a selected attack
trace in text/JSON/DOT, exact commands and versions, and original/HMAC-baseline
regressions. The selected-lemma trace run labels unrelated lemmas incomplete
because only one lemma was requested; the full `raw.out` completed all lemmas
with no timeout or incomplete result.

### 4.7 Assumptions

- the four main replay artifacts use a fixed two-slot symbolic batch: original
  replay, HMAC-only replay, dedup-only fixed replay, and HMAC+dedup combined
  replay;
- original and dedup-only matching coordinates are `(A,B,m,sid,k)`; HMAC-only
  and M4 combined coordinates are `(A,B,m,sid,k,tag)` and use
  `ConfirmedSend` / `ConfirmedReceiverAccept`;
- receiver-side occurrence context is `(bid,idx,rst)`;
- each witness uses the same `B,bid,rst` and distinct fresh slot indices
  `idx1,idx2`;
- each witness reaches normal `BatchComplete`;
- no `CompromiseReceiverState` or `CompromiseSenderState` anywhere in either witness;
- successful decapsulation/session reconstruction is abstracted by persistent
  `HonestSession`; in the HMAC bridge this also makes matching existence largely structural;
- the HMAC bridge models symbolic `tag=hmac(confirm_key(k),sid)` and exact
  confirmed-message equality, but not a computational HMAC game;
- the fixed and M4 combined artifacts use one linear, batch-local decision over
  exact complete base message `m`; it is not a global cache;
- in the M4 combined artifact, `HonestSession` remains the successful
  reconstruction/HMAC-confirmation abstraction, and dedup is over base message
  `m`, not the full `<m,tag>` term;
- replay artifacts contain no session installation or application state.

### 4.8 Allowed paper statement

> In the bounded original and HMAC-only BatchReceive replay models, one complete
> honest message can be accepted in two distinct slots of the same batch and
> receiver state, with no sender or receiver state compromise and with normal
> batch completion. In the HMAC-only bridge, both accepts pass the same symbolic
> confirmation gate over `<m,hmac(confirm_key(k),sid)>`. These same-batch/
> same-state counterexamples are sufficient to falsify the stronger global
> one-send-one-accept property, without claiming a positive theorem over
> arbitrary batches or states.

For the fixed model it is additionally allowed to state:

> In the fixed two-slot model, an atomic pre-processing decision rejects an
> exact duplicate complete message before either slot is processed. Within one
> `B,bid,rst`, the same message cannot produce two receiver accepts, while a
> distinct-message batch can complete.

### 4.9 Prohibited overstatements

Do not write:

- “The message is forged.” The witness reuses one authentic message.
- “Component authenticity prevents duplicate acceptance.”
- “The attack is cross-batch replay, rollback, or state reuse after close.”
- “HMAC is forged or computationally broken.” The witness reuses one honestly
  constructed confirmed message; it establishes duplicate acceptance, not forgery.
- “The fixed model proves global replay prevention.” Its verified result is
  limited to fixed two-slot, same `B,bid,rst`, exact complete message `m`.
- “Duplicate receiver outputs by themselves prove duplicate installed sessions.”
  M2 establishes that propagation only inside the separate, explicit
  `C_install-v2` conditional composition model; it is not an inference from P2
  alone and does not establish deployed behavior.

### 4.10 Completion milestone

M1 falsified the same-batch/same-receiver-state P2 condition in the HMAC-only
bridge. M3 is complete: the dedup-only fixed model establishes the positive
condition only for fixed two-slot, same `B,bid,rst`, exact complete `m`, with
transparent composite evidence. M4 is also complete for the combined
HMAC+dedup replay model under the same fixed two-slot, batch-local base-message
scope. Neither result is global P2. M5 has completed the final artifact freeze
without changing either result.

When a future artifact uses the current direct tuple-based matching style, it
must disambiguate sender occurrences. Two possible approaches are:

1. prove that its complete sender matching tuple uniquely determines one sender
   occurrence, as `full_message_unique_send` does here;
2. carry an explicit sender occurrence/session identifier in the sender and
   receiver events and establish injective matching on that identifier.

These are not the only valid encodings. An alternative occurrence-level
injective-correspondence formulation is acceptable if its matching relation,
sender witnesses, and injectivity argument are stated explicitly and it does
not identify tuple equality with occurrence equality without justification.

M1 satisfied this constraint with the full tuple
`(A,B,m,sid,k,tag)`, fresh sender ciphertext randomness, and the verified
`confirmed_message_unique_send` lemma. M3 retained `full_message_unique_send`;
future combined artifacts must retain an equally explicit occurrence-
disambiguation argument.

## 5. P3 under C_install-v2: unique session installation

### 5.1 Exact definition and conditional composition boundary

P3 under `C_install-v2` is a conditional composition claim evaluated in the
separate M2 impact theory. It is not a protocol-only claim, authentication rank,
specification fact, implementation fact, or deployed-behavior fact.

The actual M2 instantiation is:

```text
C1:
Every installation has an earlier complete-parameter-matching accept-output
source.

C2a:
Each accepted-output source is installed at most once.

C2b:
If ConsumerComplete occurs, every successful output belonging to that consumer
has been installed exactly once. This combines completion-gated totality with
at-most-once; no future-install restriction forces the result.

C2c:
A normal accept → install → ConsumerComplete execution is reachable.

C3:
Each installation creates a fresh local handle.

C4:
InstallSession can only be emitted by the designated installation interface
rules.

C5:
At least one matching accept/install pair is reachable. This does not imply the
whole trace contains only one accept or one install.

C6:
Installations from distinct accept-source occurrences use distinct local
handles.

C7:
The fixed two-output consumer independently processes every successful batch
output and does not merge or deduplicate by sid, message, peer, or key.

C8:
C7 is an explicit composition assumption, not an established fact about
deployed K-Waay.
```

The modeled provenance chain is:

```text
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
AcceptOutputCreated(aid,B,A,bid,idx,rst,m,sid,k)
InstallFromAccept(aid,B,h,A,bid,idx,rst,m,sid,k)
InstallSession(B,h,A,sid,k)
ConsumerComplete(B,bid,rst)
```

`sid` is the protocol session identifier, `aid` is a fresh accepted-output
occurrence identifier, and `h` is a fresh symbolic local installation handle.
`aid` does not enter the protocol message, `sid`, or key. `InstallFromAccept`
preserves complete provenance; `InstallSession` is the conditional composition
event. `ConsumerComplete` is only the terminal event of this bounded consumer,
not real application completion.

Unique installation asks whether one matching sender occurrence can produce
two installation events carrying the same peer, `sid`, and key but distinct
local handles:

```text
InstallSession(B,h1,A,sid,k)
InstallSession(B,h2,A,sid,k)
same matching SenderSession
implies h1 = h2.
```

### 5.2 Historical artifact status

- original conditional duplicate-install witness under `C_install-v2`:
  `established`;
- original unique installation under `C_install-v2`: `falsified`;
- fixed dedup duplicate-install witness: `falsified`;
- fixed dedup unique installation under `C_install-v2`: `established`;
- fixed dedup normal distinct consumer completion: `established`;
- M4 combined duplicate-install witness under `C_install-v2`: `falsified`;
- M4 combined unique installation under `C_install-v2`: `established`;
- M4 combined duplicate accepted output: `blocked` / `verified`;
- M4 combined duplicate installation: `blocked` / `verified`;
- M4 combined distinct confirmed-message consumer completion: `established`;
- deployed K-Waay per-output installation: `unknown` / unsupported by repository
  specification or implementation evidence.

### 5.3 Protocol variants

- actual original impact/composition model over replay original;
- actual fixed dedup impact model;
- actual HMAC+dedup combined impact model.

The M2 result applies only to the first variant; the M3 result applies only to
the second. M4 establishes the combined HMAC+dedup P3 result only under the same
bounded `C_install-v2` consumer and fixed two-slot batch-local scope.

### 5.4 Model and evidence

Model:

- `tamarin/impact/kwaay_impact_original.spthy`
- `tamarin/impact/kwaay_impact_fixed.spthy`
- `tamarin/impact/kwaay_impact_hmac_dedup.spthy`

Runner and boundary description:

- `tamarin/impact/run-impact-original.sh`
- `tamarin/impact/README.md`
- `tamarin/impact/README-fixed.md`
- `tamarin/impact/README-hmac-dedup.md`

Committed evidence:

- `logs/tamarin-impact-original/`
- `docs/milestones/M2-completion.md`
- `logs/tamarin-m3-closeout/`
- `docs/milestones/M3-completion.md`
- `logs/tamarin-m4-hmac-dedup/`
- `docs/milestones/M4-completion.md`

### 5.5 Events and 19 composition lemmas

Key events:

- `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)`;
- `AcceptOutputCreated(aid,B,A,bid,idx,rst,m,sid,k)`;
- `InstallFromAccept(aid,B,h,A,bid,idx,rst,m,sid,k)`;
- `InstallSession(B,h,A,sid,k)`;
- `ConsumerComplete(B,bid,rst)`.

Composition lemmas and actual results:

| Lemma | Actual result |
|---|---|
| `accept_output_has_same_time_accept` | verified, 4 steps |
| `receiver_accept_has_output` | verified, 4 steps |
| `receiver_accept_has_unique_output` | verified, 20 steps |
| `accept_id_unique` | verified, 193 steps |
| `install_has_prior_accept` | verified, 18 steps |
| `install_session_has_interface_origin` | verified, 4 steps |
| `install_from_accept_has_session` | verified, 4 steps |
| `install_event_has_single_source` | verified, 26 steps |
| `install_handle_unique` | verified, 52 steps |
| `accept_output_installed_at_most_once` | verified, 180 steps |
| `distinct_accept_sources_have_distinct_handles` | verified, 26 steps |
| `install_requires_batch_complete` | verified, 10 steps |
| `consumer_complete_requires_all_outputs_installed` | verified, 30 steps |
| `consumer_complete_single_use` | verified, 36 steps |
| `no_install_after_consumer_close` | verified, 44 steps |
| `normal_one_accept_one_install` | verified, 22 steps |
| `normal_consumer_complete` | verified, 25 steps |
| `one_send_two_accepts_two_installs_exists` | verified, 28 steps |
| `unique_install_within_completed_consumer` | falsified - found trace, 28 steps |

The composition profile is 18 verified and 1 falsified. With the frozen 18
lower-layer lemmas, the full theory has 37 terminal results: 34 verified, 3
falsified, 0 incomplete, 0 failed invocation, 0 wellformedness failure, and 0
`<<loop>>` in the final sequential-per-lemma evidence run.

### 5.6 Actual result and witness scope

`one_send_two_accepts_two_installs_exists` verifies a 28-step trace in which one
unique matching `SenderSession` leads to two distinct `ReceiverAccept`
occurrences, two fresh `aid`, and two installations. Both `InstallSession`
events carry the same `A,B,sid,k` but different fresh handles, and the consumer
then completes.

`unique_install_within_completed_consumer` is falsified by a 28-step
counterexample. The trace has one matching sender occurrence, the same
`A,B,m,sid,k,bid,rst`, distinct receiver timepoints and slot indices, distinct
installation timepoints, distinct `aid` and handles, and both installations
after `BatchComplete` and before `ConsumerComplete`. It contains no
`CompromiseReceiverState` or `CompromiseSenderState` occurrence.

The 18 frozen lower-layer formula blocks are 18/18 MATCH, and their actual
result vector is 18/18 MATCH against the original regression. This is selected
formula/result preservation, not full trace equivalence.

Fixed-impact M3 actual results:

| Lemma | Actual result |
|---|---|
| `one_send_two_accepts_two_installs_exists` | falsified |
| `unique_install_within_completed_consumer` | verified |
| `normal_consumer_complete` | falsified |
| `normal_distinct_consumer_complete` | verified |
| `duplicate_batch_has_no_accept_output` | verified |
| `duplicate_batch_has_no_install` | verified |
| `no_consumer_after_failed_batch` | verified |

`normal_consumer_complete` is the frozen legacy same-message two-output target;
its falsification is expected after duplicate rejection. The distinct-message
consumer remains non-vacuous through `normal_distinct_consumer_complete`.
Fixed impact has 53/53 expected terminal targets in the transparent composite
vector. Consumer rules remain 3/3 byte-for-byte MATCH, so this result still uses
the same conditional `C_install-v2` interface rather than consumer-side dedup.

### 5.7 Allowed paper statement

> Under the explicitly modeled `C_install-v2` consumer assumptions, the bounded
> original replay witness propagates from two receiver-accept outputs to two
> distinct symbolic local installation handles carrying the same peer,
> session identifier, and session key.

It is also permitted to report that installation provenance correspondence is
verified in both directions, distinct accept sources use distinct handles,
normal accept/install/complete paths are reachable, lower-layer formula/result
vectors did not regress, and unique installation under this consumer is
falsified.

For the fixed impact model it is permitted to report that, under the same
explicit `C_install-v2` assumptions, the batch-local duplicate branch produces
no accepted output or installation, unique installation is verified, and two
distinct messages can still complete the consumer.

For the M4 combined impact model it is permitted to report that, under the same
explicit bounded `C_install-v2` assumptions, duplicate same-base confirmed input
does not produce duplicate accepted output or duplicate installation, unique
installation is verified, and two distinct valid confirmed messages can still
complete the consumer. It is also required to preserve the boundary that slot-2
HMAC mismatch can occur after slot-1 has already accepted; therefore M4 must not
be summarized as proving that every failed batch has no partial lower-layer
output.

### 5.8 Prohibited overstatements

Do not write:

- “Deployed K-Waay necessarily installs two sessions from one send.”
- “Figure 7 specifies independent installation of every output.”
- “A real implementation session-cloning exploit has been proved.”
- “Two `InstallSession` events are two complete real sessions.”
- “Double Ratchet state is duplicated.”
- “Application, payment, authorization, or another business action repeats.”
- “Arbitrary-length or cross-batch impact has been proved.”
- “HMAC-only duplicate acceptance already proves duplicate installation.”
- “M4 proves deployed upper-layer behavior.” M4 is complete only as a
  fixed-two-slot Tamarin-only artifact under `C_install-v2`.
- “Computational security has been proved.”

### 5.9 General inference boundary

The general implications remain forbidden:

```text
ReceiverAccept does not by itself imply InstallSession
two ReceiverAccept events do not by themselves imply two installed sessions
```

Only inside the explicit `C_install-v2` composition model may the conditional
M2 witness be cited. The conditional result cannot be transferred to a deployed
upper layer without independent specification or implementation evidence.

### 5.10 Completion milestone

M2 is complete with model/runner Commit A2, formal evidence Commit B, 19
composition results, 18 frozen lower-layer regressions, trace artifacts, and a
verified 52-entry manifest covering 53 evidence files including the manifest.

M3 is complete with frozen A3 models and transparent composite evidence: fixed
P2 and fixed P3 under `C_install-v2` match their expected vectors without
changing the completed M2 result. M4 is complete with frozen combined
HMAC+dedup replay/impact models and Tamarin-only transparent composite evidence:
296/296 terminal, 296/296 MATCH, 0 terminal conflicts, 0 unresolved rows, and 0
mismatches. M5 has completed the final artifact freeze without changing the P3
status or its bounded conditional-composition scope.

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

The main-line evidence state after M4 is therefore:

```text
P0 baseline: established
P1 original: falsified
P1 HMAC ProVerif baseline: established
P1 HMAC under A signing-key compromise: falsified
HMAC-only Tamarin matching existence/order: established but structurally mediated by HonestSession
P2 Tamarin replay original: falsified
P2 HMAC-only replay: falsified in the same-batch/same-state subdomain
P2 fixed: established within fixed two-slot, same B/bid/rst, exact complete m
P2 combined: established within fixed two-slot, same B/bid/rst,
             exact complete base message m, batch-local scope
P3 under C_install-v2: conditional duplicate-install witness established;
                       unique installation falsified
P3 fixed/dedup under C_install-v2: unique installation established;
                                      duplicate-install witness falsified
P3 combined under C_install-v2: established only under the bounded conditional
                                consumer and the same fixed two-slot
                                batch-local scope
```

M5 has frozen the reproducible artifact/result tables and paper-facing bundle.
M2, M3, and M4 impact results may still be cited only under the explicit
`C_install-v2` composition assumptions; duplicate `ConfirmedReceiverAccept`
outside those impact models must not be relabeled as duplicate installation.
M4 Evidence Commit B is Tamarin-only; the ProVerif 5-target story is inherited
from prior committed evidence, not rerun in M4. The M4 combined results are not
global, cross-batch, rollback, restart, arbitrary-state, or arbitrary-length
theorems, and they do not establish deployed upper-layer behavior.

## 7. M5 evidence index

- `artifact/results/claim-evidence.tsv` is the frozen claim index.
- `artifact/results/claim-matrix.tsv` is the mechanical join of each indexed
  claim with its expected and actual result.
- `artifact/results/actual-results.tsv` distinguishes direct Tamarin results,
  inherited committed ProVerif results, and M4
  `not_run_out_of_scope` scope declarations.
- `artifact/results/raw-to-summary.tsv` maps every actual property to its raw
  and summary provenance.
- `artifact/manifest/artifact-inventory.tsv` joins the paper-mainline index to
  frozen Git-blob identities.

M5 does not change any P0-S, P0-O, P1, P2, or P3 established/falsified/partial
status. In the claim matrix, a verified attack witness means the modeled attack
is reachable. A falsified blocked-attack witness means that particular attack
is unreachable in the corresponding repair model; it does not mean the repair
failed.
