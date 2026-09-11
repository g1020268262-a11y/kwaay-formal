# Formal Model

## 1. Modeling Objective

The purpose of the formal model is not to encode the complete K-Waay
protocol. Instead, the model isolates the admission semantics of a single
`BatchReceive` execution. This abstraction is designed to study one specific
identity question: whether distinct slots of an admitted batch must carry
distinct modeled party identities in order to preserve the intended
party-level interpretation of that batch.

We compare three Tamarin theories over a common two-slot structure. The relaxed
model, denoted R-semantics, omits both party- and message-uniqueness checks. The
message-deduplication model, denoted M-semantics, compares message coordinates.
The party-admission model, denoted P-semantics, compares party coordinates. The
comparison therefore changes the identity-level admission condition while
keeping the sender, collection, batch, receiver-state, and acceptance structure
as similar as possible.

The formalization follows the frozen admission contract in
[`g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md), the adversary
boundary in [`rq-v2-threat-model.md`](../rq-v2/rq-v2-threat-model.md), and the
executed theories recorded in
[`prototype-execution-report.md`](../rq-v2/prototype-execution-report.md).

## 2. Identity Coordinates

An entry collected for the modeled batch has three explicit data coordinates,
and its processing introduces three additional structural coordinates:

| Coordinate | Meaning |
| --- | --- |
| `A` | modeled protocol-principal identity coordinate |
| `sid` | sender session or sender-occurrence coordinate |
| `m` | sender-produced message coordinate |
| `slot` | position of an entry in the two-slot batch |
| `bid` | fresh identifier of the batch execution |
| `rst` | fresh receiver-state coordinate associated with that batch |

The coordinate `A` denotes only a modeled protocol principal. It is not an
account record, public-key encoding, API object, or other implementation-level
identity representation. A party can participate through multiple sender-rule
occurrences, and each such occurrence creates a fresh `sid` and a fresh `m`.
Thus, the formalization keeps the following dimensions separate:

```text
party identity   != message identity
party identity   != session identity
party identity   != slot identity
message identity != session identity
```

In particular, two different messages or sessions do not imply two different
parties. Similarly, two distinct slots are structural positions and do not by
themselves establish party inequality. The invariant under study constrains
the relationship between these coordinates within one batch:

```text
for distinct slots i and j in one admitted batch:
    party(E_i) != party(E_j)
```

## 3. Common Two-Slot Batch Structure

All three theories begin with the same party and sender abstraction.
`CreateParty` generates a fresh party coordinate and stores it in a persistent
`!Party(A)` fact. `SendMessage` consumes this persistent party fact together
with fresh session and message values. It emits the action
`Send(A,sid,m)`, publishes the tuple `<A,sid,m>` to the adversarial network,
and records a persistent `!Sent(A,sid,m)` origin fact.

A batch is created with one fresh `bid` and one fresh `rst`. The collection
lifecycle then proceeds through two linear states:

```text
CreateBatch(bid,rst)
        -> CollectSlot1(A1,sid1,m1)
        -> CollectSlot2(A2,sid2,m2)
        -> Collected(bid,rst,A1,sid1,m1,A2,sid2,m2)
```

The network controls the tuples supplied to the two collection rules. After
both entries have been collected, the selected admission rule either creates
the state required to process slot 1 or records rejection. Admission emits
`BatchReceive(bid,rst)`. The accepted path processes the two slots in order.
Each slot can emit `ReceiverAccept(A,sid,m,bid,rst)` only in the presence of a
matching persistent `!Sent(A,sid,m)` fact. The first acceptance advances the
linear state to slot 2; the second produces `BatchComplete(bid,rst)`.

This common lifecycle holds the following dimensions constant across R-, M-,
and P-semantics:

- party creation and persistent party state;
- fresh sender session and message creation;
- adversarial delivery of collected tuples;
- exactly two batch slots;
- one batch identifier and one receiver-state coordinate;
- sequential slot processing; and
- the `Send`-to-`ReceiverAccept` origin relation.

The principal difference among the theories is the predicate used at the
admission decision.

## 4. R-Semantics: Relaxed Admission

The relaxed theory
[`rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy)
contains a single `AdmitRelaxedBatch` rule after collection. Its premises carry
both complete slot records, but its action and conclusion impose neither

```text
A1 != A2
```

nor

```text
m1 != m2.
```

Consequently, admission is independent of both party equality and message
equality. A pair with the same party coordinate can enter the batch, including
the special case in which the complete tuple `<A,sid,m>` is supplied in both
slots. R-semantics defines the invariant-removed baseline; this section states
only its admission behavior. Reachability consequences are reported separately
in the Security Analysis.

## 5. M-Semantics: Message Deduplication

The message-deduplication theory
[`rqv2_message_dedup.spthy`](../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy)
splits the post-collection decision into rejection and admission. If the two
message coordinates are syntactically equal, `RejectRepeatedMessage` emits
`Reject(bid,rst)` and produces `BatchRejected(bid,rst)`. Otherwise,
`AdmitDistinctMessages` emits the inequality action `Neq(m1,m2)` together with
`BatchReceive(bid,rst)`. The global `Inequality` restriction rules out
`Neq(x,x)` events.

The accepted branch therefore requires

```text
m1 != m2,
```

but it imposes no condition

```text
A1 != A2.
```

M-semantics constrains the message coordinate. A candidate pair
`(A,m1,sid1)` and `(A,m2,sid2)` remains admissible when `m1 != m2`, even though
both entries carry the same party coordinate. The model thus separates
exact-message uniqueness from party uniqueness without treating message-level
admission as party-level admission.

## 6. P-Semantics: Party Admission

The party-admission theory
[`rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy)
applies the corresponding decision to party coordinates. If both collected
entries carry the same `A`, `RejectRepeatedParty` emits `Reject(bid,rst)` and
produces `BatchRejected(bid,rst)`. The admitted branch,
`AdmitDistinctParties`, emits `Neq(A1,A2)` and `BatchReceive(bid,rst)`, and is
subject to the same `Inequality` restriction.

The accepted branch therefore requires

```text
A1 != A2.
```

Message or session equality is not used as a substitute for this comparison.
A same-party pair follows the rejection branch, whereas a distinct-party pair
can enter the two-slot processing lifecycle. P-semantics is an executable
restoration model for `DistinctPartyPerBatch` at the abstract admission
boundary. It represents one way to realize the invariant in the model; it does
not select a uniquely required implementation algorithm or component.

## 7. Events and Properties

The paper uses only action events that occur in the three theories:

| Event | Role |
| --- | --- |
| `Send(A,sid,m)` | records one sender-rule occurrence for a party, session, and message tuple |
| `BatchReceive(bid,rst)` | records admission of a collected pair into receiver processing |
| `ReceiverAccept(A,sid,m,bid,rst)` | records acceptance of one slot under a matching persistent sender-origin fact |
| `Reject(bid,rst)` | records rejection in M- or P-semantics |
| `Neq(x,y)` | records the inequality guard used by the admitted branch in M- or P-semantics |

`BatchComplete(bid,rst)` and `BatchRejected(bid,rst)` are resulting state
facts, not action events. They represent terminal states of the modeled
two-slot lifecycle.

The relaxed theory contains the following lemmas:

- `normal_relaxed_batch_exists` checks reachability of a relaxed batch with a
  prior matching send and a receiver acceptance;
- `one_send_two_accepts_exists` asks for one unique matching send occurrence
  and two ordered receiver-accept occurrences in one batch context;
- `receiver_accept_has_send` checks that every receiver acceptance has a prior
  matching send; and
- `receiver_accept_injective` asks whether two accept occurrences for the same
  send tuple and batch context must be the same event occurrence.

The message-deduplication theory contains:

- `repeated_message_rejection_exists`;
- `same_party_different_messages_batch_exists`;
- `accepted_batch_has_distinct_messages`;
- `receiver_accept_has_send`; and
- `receiver_accept_injective`.

The party-admission theory contains:

- `same_party_rejection_exists`;
- `distinct_party_batch_exists`;
- `accepted_batch_has_distinct_parties`;
- `receiver_accept_has_send`; and
- `receiver_accept_injective`.

The existence lemmas provide non-vacuity or witness obligations. The universal
lemmas express sender origin, scoped receiver-occurrence injectivity, or the
identity property of admitted batches. Their recorded outcomes are reported in
the next section rather than built into the model description.

## 8. Scope and Abstraction Boundary

The three theories are symbolic fixed-two-slot admission prototypes. They do
not contain:

- KEM operations;
- signatures;
- HMAC computation;
- compromise rules;
- prekey cryptography;
- output-key objects;
- `KEY` or `TEST` operations;
- Double Ratchet state;
- an application consumer; or
- a deployed implementation.

These omissions are deliberate. The object of analysis is the identity
coordinate checked at the `BatchReceive` admission boundary and the resulting
receiver-acceptance behavior. The model is not an abstraction of every
cryptographic or application layer of K-Waay, and the results do not constitute
verification of the complete protocol. They also do not establish
arbitrary-length, cross-batch, rollback, restart, liveness, or upper-layer
consumption properties.

All model-level statements in this section are traceable to the frozen mapping
in
[`contribution-evidence-map.md`](contribution-evidence-map.md) and to the three
theory files cited above.
