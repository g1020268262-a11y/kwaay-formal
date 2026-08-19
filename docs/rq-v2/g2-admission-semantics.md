# K-Waay RQ-v2 G2 Admission Semantics and Necessity Contract

## 1. Status

**Stage:** RQ-v2 / G2 semantic contract, updated after prototype execution

**Baseline commit:** `930820d8db1e101fb4cb377fb0887f6c004c02a9`

**Document role:** Current semantic authority for `DistinctPartyPerBatch`
necessity analysis

This document freezes the executable semantics for the RQ-v2 admission
comparison. It defines the identity-level invariant, the relaxed comparison,
and the distinction between party admission and auxiliary message-level
deduplication. Prototype results are reported separately in
[`prototype-execution-report.md`](prototype-execution-report.md).

This semantic contract does not claim implementation enforcement, deployed
behavior, an arbitrary-length theorem, or a uniquely necessary mechanism for
occurrence injectivity.

---

## 2. Role in the DistinctPartyPerBatch Necessity Analysis

RQ-v2 studies why K-Waay's stated distinct-party `BatchReceive` precondition is
necessary for the intended batch identity semantics. The comparison removes
the identity-level invariant and observes which same-batch behaviors become
admissible under explicit modeled batch-admission semantics.

The specification-level invariant is named:

```text
I_spec = DistinctPartyPerBatch
```

The research chain is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> conditional upper-layer duplicate consumption/install impact
```

The arrows denote a consequence chain to test in explicitly scoped models; they
do not claim that every invalid batch must produce every later consequence.
The final contribution target is the identity-level batch invariant, not
message identity versus party identity and not occurrence injectivity alone.

The G1 identity result used here is:

```text
specification-level party = protocol principal
modeled A                 = modeled protocol-principal identifier
```

This mapping is restricted to the formal-model identity coordinate. It does
not identify `A` with an application account, public-key bytes, a prekey, a
message, a session identifier, or a sender occurrence.

---

## 3. Abstract Batch Entry Model

For G2, an abstract batch entry has the form:

```text
Entry = (
  party_id,
  message,
  session_coordinate
)
```

The fields have the following meanings:

- `party_id` denotes the specification-level protocol principal. In the
  RQ-v2 symbolic models, this coordinate is represented by `A`.
- `message` denotes the sender-produced content, represented by `m`.
- `session_coordinate` distinguishes a sender session or sender occurrence,
  represented by a session identifier and/or an event occurrence coordinate.

The `session_coordinate` is not the party. Multiple session coordinates and
multiple messages may belong to the same `party_id`.

The entry abstraction does not prescribe a wire format, API structure, server
record, or deployed implementation object.

---

## 4. Identity Layer Separation

The frozen identity hierarchy is:

```text
Party
|
+-- LongTermIdentity
|
+-- Session1
|   |
|   +-- Prekey1
|   +-- Message1
|
+-- Session2
    |
    +-- Prekey2
    +-- Message2
```

Party identity is above session, prekey, and message identity. One party may
own more than one session, and those sessions may use different prekeys and
produce different messages.

Consequently:

- message equality must not substitute for party equality;
- message inequality must not establish party inequality;
- prekey equality must not substitute for party equality;
- prekey inequality must not establish party inequality;
- session equality or inequality must not substitute for party equality or
  inequality.

Every RQ-v2 model must preserve the separation between the party coordinate
`A` and all session/prekey/message coordinates.

---

## 5. Frozen Invariant Definition

For a batch:

```text
S = [E1, E2, ..., En]
```

the normalized invariant is:

```text
forall i,j.
  i != j
  implies
  party(Ei) != party(Ej)
```

Equivalently, no two distinct entry positions in one admitted batch may carry
the same specification-level party identity.

This is the RQ-v2 formal normalization of K-Waay's natural-language
distinct-party condition. It is not presented as a mathematical formula
written verbatim by the K-Waay authors.

This section freezes the meaning of `DistinctPartyPerBatch`; the definition
alone does not prove necessity. Necessity evidence must come from the scoped
R/P comparison, while implementation enforcement, sufficiency beyond the
stated identity semantics, minimality, and uniqueness remain unclaimed.

---

## 6. Admission Semantics for the Necessity Comparison

The comparison uses three admission semantics over the same abstract entry and
batch structure. R- and P-semantics form the core invariant-removal comparison;
M-semantics is retained only as an auxiliary mechanism comparison.

### 6.1 Relaxed Admission

**Name:** R-semantics

R-semantics admits an input batch without checking party uniqueness.

It therefore permits entries such as:

```text
(A, m1, sid1)
(A, m2, sid2)
```

including the case `m1 != m2` and `sid1 != sid2`.

R-semantics is the relaxed baseline used to study the absence of the admission
invariant. It makes same-batch repeated-party composition admissible and can
therefore expose duplicate receiver acceptance. A trace admitted only by
R-semantics is not, for that reason, a valid K-Waay execution satisfying the
specification's stated distinct-party `BatchReceive` precondition.

### 6.2 Message-Level Deduplication

**Name:** M-semantics

M-semantics rejects a batch if two distinct entries contain equal messages:

```text
i != j and message(Ei) == message(Ej)
```

It still permits:

```text
(A, m1, sid1)
(A, m2, sid2)
```

when:

```text
m1 != m2
```

M-semantics is an auxiliary comparison based on message identity. It is not
equivalent to party uniqueness and must not be described as an executable
realization of `DistinctPartyPerBatch`, the main problem, or the current
research contribution. A scoped occurrence-injectivity result under
M-semantics does not restore the intended batch identity semantics.

### 6.3 Party-Level Admission

**Name:** P-semantics

P-semantics rejects a batch if any two distinct entries have the same party:

```text
exists i,j.
  i != j
  and
  party(Ei) == party(Ej)
```

For example, it rejects:

```text
(A, m1, sid1)
(A, m2, sid2)
```

regardless of whether the messages, prekeys, or session coordinates differ.
It permits a party-distinct pair such as:

```text
(A, m1, sid1)
(B, m2, sid2)
```

provided `A != B` at the modeled protocol-principal coordinate.

P-semantics is the executable abstraction of `DistinctPartyPerBatch`. Within
the modeled admission boundary, it restores the intended batch identity
semantics: an admitted batch cannot contain two distinct slots for the same
party. This designation does not claim that a deployed implementation uses
this mechanism or that party admission is the unique way to establish a
separate occurrence-injectivity property.

---

## 7. Batch Rejection Semantics

RQ-v2 does not currently have evidence fixing the enforcement component or
the concrete failure interface. G2 therefore introduces an abstract admission
layer:

```text
BatchReceiveAdmission(S) -> accept | reject
```

This layer decides only whether a batch is admitted to the modeled receiver
processing semantics. It is not identified with a caller, server, client,
batching service, or deployed `BatchReceive` implementation.

The abstract `reject` outcome records that the candidate batch is not admitted
under the selected semantics. Whether rejection drops one entry, rejects the
whole batch, returns an error, or triggers another concrete behavior remains
open.

---

## 8. Comparison Matrix

| Semantics | Identity checked | Same party, different message | Purpose |
| --- | --- | --- | --- |
| R-semantics | none | allowed | core invariant-removed baseline |
| M-semantics | message | allowed when messages differ | auxiliary non-equivalence comparison |
| P-semantics | party | rejected | restores intended batch identity semantics |

All three semantics must otherwise use comparable entry, sender-occurrence,
receiver-state, batch, slot, lifecycle, and acceptance coordinates. The
comparison must not obtain its result by changing unrelated protocol behavior.

HMAC is outside this admission comparison. It may provide message authenticity,
integrity, or confirmation evidence, but it neither replaces party admission
nor establishes `DistinctPartyPerBatch`.

---

## 9. Target Properties

### 9.1 Primary target: batch identity semantics

The primary target is admitted-batch party uniqueness:

```text
P_batch-id:
  two distinct accepted positions in the same batch
  imply two distinct party identities
```

This target directly expresses `DistinctPartyPerBatch` at the modeled
admission/acceptance boundary. The necessity comparison asks whether removing
party-level admission makes a violation reachable and whether P-semantics
restores this identity property while keeping valid distinct-party batches
reachable.

Non-vacuity and valid-batch reachability are mandatory: rejection of every
batch must not be mistaken for preservation of the invariant.

### 9.2 Supporting target: occurrence injectivity

The supporting target `P_accept-inj` concerns same-batch,
same-receiver-state occurrence-level receiver injectivity for one sender
origin. It is useful for identifying a duplicate-acceptance consequence under
R-semantics, but it is not the final contribution and cannot by itself prove
the necessity of party-level admission.

In particular, message-level semantics may restore this scoped occurrence
property while still admitting same-party/different-message batches. Such a
result preserves occurrence injectivity but violates `P_batch-id` and does not
restore the intended batch identity semantics.

The sender-to-receiver matching relation and occurrence coordinates must remain
explicit whenever `P_accept-inj` is reported.

---

## 10. Research Questions

G2 enables the following questions:

**RQ1 — Invariant removal**

> Does removing `DistinctPartyPerBatch` admit invalid same-batch party
> composition, including an execution with duplicate receiver acceptance?

**RQ2 — Identity semantics restoration**

> Does party-level admission restore the intended batch identity semantics
> while preserving reachable valid distinct-party batches?

**Auxiliary comparison — Message identity**

> Can exact-message deduplication satisfy scoped occurrence injectivity while
> still failing to enforce party uniqueness?

The auxiliary comparison exists to rule out message identity as a substitute
for party identity. It is not the main research problem and does not support a
claim that party admission uniquely restores occurrence injectivity. Bounded
prototype outcomes for these questions are recorded in the companion execution
report; broader conclusions remain limited by that report's model scope.

---

## 11. Modeling Requirements

An RQ-v2 Tamarin design must distinguish at least:

| Semantic layer | Required coordinate |
| --- | --- |
| party identity | `A`, interpreted as modeled protocol-principal identifier |
| sender session/occurrence | `sid`, an event occurrence, and/or a separate fresh occurrence coordinate |
| message | `m` |
| prekey | session material separate from `A` |
| receiver state | a receiver-state coordinate |
| batch | a batch coordinate |
| slot | a position/entry coordinate |

The design must not:

- treat `m` as the party identity;
- treat `sid` as the party identity;
- treat a prekey as the party identity;
- infer different parties merely from different messages, sessions, prekeys,
  or public-key byte strings;
- conflate a sender occurrence with `A`;
- add an implementation enforcement location without evidence;
- build the desired theorem into the model by eliminating valid behavior.

The design must state whether two individually legitimate same-party candidate
entries use the same or different prekeys and must keep that choice separate
from party equality. They remain invalid when admitted together into the same
batch.

---

## 12. Open Decisions

The following decisions remain deliberately unfrozen:

1. Whether a batch violation rejects one entry, rejects the whole batch, or
   produces another abstract failure behavior.
2. Whether a concrete admission check belongs to a caller, server, client, or
   another component; G2 uses only an abstract layer.
3. Refinement of the exploratory Tamarin facts, rules, restrictions, events,
   and lemmas used to represent R-, M-, and P-semantics.
4. The mapping from the abstract admission layer to any implementation.

These decisions do not alter the frozen distinction among no identity check,
message-identity checking, and party-identity checking. They therefore do not
block this semantic freeze, but they must be resolved or explicitly scoped by
later design and evidence.

---

## 13. G2 Contract Verdict

Frozen for RQ-v2:

- [x] Entry abstraction
- [x] Party identity coordinate
- [x] `DistinctPartyPerBatch` semantics
- [x] R/P core necessity comparison
- [x] M-semantics as auxiliary comparison
- [x] Batch identity semantics as the primary target
- [x] Occurrence injectivity as a supporting target

Not established by this semantic contract alone:

- [ ] Implementation enforcement location
- [ ] Deployed behavior
- [ ] Arbitrary-length or global theorem
- [ ] Unconditional upper-layer impact

The exploratory model results are reported separately and do not broaden these
boundaries.

**Final status: `RQ_V2_SEMANTIC_AUTHORITY_ACTIVE`**
