# Identity Invariants in Batch Admission: A Formal Analysis of K-Waay BatchReceive

## Abstract

Batch processing can impose semantic relationships among multiple protocol
inputs rather than merely improve efficiency. K-Waay's `BatchReceive`
description states that different elements in one call correspond to different
parties. We refer to this stated condition as `DistinctPartyPerBatch` and study
its semantic necessity. We construct three fixed-two-slot symbolic Tamarin
admission models: R-semantics removes party uniqueness, M-semantics applies
exact-message deduplication, and P-semantics applies party-level admission. In
all three cases, a common sender-origin and sequential receiver-acceptance
lifecycle supports controlled comparison. In
R-semantics, `one_send_two_accepts_exists` is verified and
`receiver_accept_injective` is falsified, exhibiting a reachable trace in
which one sender occurrence supports two receiver-acceptance occurrences. In
M-semantics, `receiver_accept_injective` is verified, but
`same_party_different_messages_batch_exists` is also verified: distinct
messages from one modeled party can still occupy the batch. In P-semantics,
`accepted_batch_has_distinct_parties`, `same_party_rejection_exists`, and
`distinct_party_batch_exists` are verified, establishing party-distinct
admission, reachable rejection of a same-party pair, and non-vacuous valid
batch behavior. The comparison shows that message-level occurrence properties
and party-level uniqueness are distinct dimensions. Within the modeled
fixed-two-slot admission boundary, the analysis supports the necessity of
`DistinctPartyPerBatch` for preserving the intended party-level batch identity
semantics.

## 1. Introduction

Batch processing in security protocols is commonly motivated by efficiency,
but it also determines how several inputs relate within one protocol
execution. Once inputs are collected into a single receiver-side operation,
their positions can acquire a joint identity interpretation: the batch may be
expected to represent contributions from a particular set of parties. A
condition on batch composition can therefore be a semantic invariant, not
merely a syntactic filter.

K-Waay is a post-quantum X3DH-like deniable authenticated key-exchange
construction based on split-KEM techniques. Its `BatchReceive` description
already states that different elements in one call correspond to different
parties ([L1](https://www.usenix.org/conference/usenixsecurity24/presentation/collins)).
We call this condition `DistinctPartyPerBatch`. Our purpose is not to discover
the condition or revisit K-Waay's computational proof. We ask what identity
semantics the condition preserves at admission and what bounded behavior
becomes reachable when that condition is removed.

The key distinction is between identity coordinates. Party identity is not
message identity, session identity, or slot identity. One modeled party can
produce several messages through several sender occurrences, and two batch
slots remain distinct positions even if they carry the same party coordinate.
Replay controls, exact-message deduplication, and authentication mechanisms
constrain important message- or origin-level relations, but those relations do
not by themselves imply same-batch party uniqueness. This is a separation of
properties, not a claim that those mechanisms fail at their stated purposes.

We study three admission semantics in Tamarin's multiset-rewriting trace model
([L11](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48)).
R-semantics removes party uniqueness, M-semantics applies exact-message
deduplication, and P-semantics applies party-level admission. The theories
share a symbolic fixed-two-slot structure, sender-origin relation, batch and
receiver-state coordinates, and sequential `ReceiverAccept` lifecycle. This
controlled design changes the coordinate compared at admission while holding
the remaining lifecycle stable.

The comparison produces two central observations. In the relaxed case, the model
admits repeated-party composition and contains a reachable trace in which one
sender occurrence supports two receiver-acceptance occurrences. Second,
message-level admission can restore the scoped occurrence-injectivity property
while a same-party/different-message batch remains reachable. Party-level
admission instead restores the intended distinct-party interpretation and
retains a reachable valid batch. Thus, occurrence injectivity and party
uniqueness are related evaluation dimensions but are not the same property.

Within the fixed-two-slot symbolic admission boundary, this paper makes three
contributions:

1. We isolate K-Waay's stated distinct-party `BatchReceive` condition as a
   party-level identity invariant within the modeled admission boundary.
2. We formally characterize the bounded consequence of removing that
   condition: same-batch repeated-party composition and a reachable
   one-Send/two-accept behavior.
3. We provide an R/M/P-semantics comparison showing that message-level
   deduplication can restore scoped occurrence injectivity without restoring
   party uniqueness, whereas party-level admission restores the intended
   distinct-party semantics and preserves a reachable valid batch.

The analysis is specification- and integration-level. It does not model the
complete K-Waay construction, a deployed implementation, or cryptographic
security games. The direct evidence ends at admission, rejection, and
`ReceiverAccept`.

## 2. Background

### 2.1 K-Waay and BatchReceive

K-Waay constructs an efficient, deniable, post-quantum X3DH-like exchange and
uses split-KEM techniques to support its receiver-side processing
([L1](https://www.usenix.org/conference/usenixsecurity24/presentation/collins)).
The aspect relevant here is the `BatchReceive` abstraction, in which a single
receiver-side operation processes several input elements together. The
original description requires the elements in one call to correspond to
different parties. We normalize that already stated condition as
`DistinctPartyPerBatch` for analysis.

Our abstraction isolates the admission and composition boundary of one such
operation. It does not reconstruct the KEM construction, signatures, prekey
processing, or Double Ratchet behavior. The batch is treated as a structured
input whose slots jointly describe which modeled parties contribute to one
admitted receiver execution.

### 2.2 Entry and Identity Coordinates

An abstract entry is written as `E = (A, sid, m)`. Here `A` is a modeled
protocol-principal coordinate, `sid` is a sender-session or sender-occurrence
coordinate, and `m` is a message coordinate. This tuple is symbolic notation
for the distinctions needed at admission; it is not a claim about K-Waay's
wire format. Processing also introduces a slot coordinate, a batch identifier
`bid`, and a receiver-state coordinate `rst`.

The coordinates have different roles. The same `A` may occur with several
`sid` and `m` values, in other batches, or in other slot positions. Different
messages, sessions, or slots therefore do not imply different modeled parties.
Conversely, a condition over party coordinates need not be a condition over
message equality. `A` is not identified with an account object, database
record, public-key encoding, or other deployed representation.

### 2.3 Neighboring Security Dimensions

Authentication and integrity relate messages to origins and protected
material. Replay handling and deduplication constrain reuse or equality of
messages. Injective correspondence constrains the multiplicity of matching
event occurrences, following an established line of authentication
definitions ([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)).
These dimensions are relevant to protocol reasoning, but none is definitionally
equivalent to pairwise party distinctness inside one admitted batch. The
analysis below makes that logical separation executable.

## 3. Problem Statement

### 3.1 Intended Batch Identity Semantics

Let a batch be

```text
B = [E_1, E_2, ..., E_n],
```

and let `party(E_i)` return the modeled protocol-principal coordinate carried
by entry `E_i`. We define the party-level identity invariant by

```text
DistinctPartyPerBatch(B) iff
    for all i != j, party(E_i) != party(E_j).
```

The invariant concerns distinct positions within one admitted batch. It does
not impose global uniqueness on a modeled party or prohibit that party from
having other messages, sessions, or batches. Although the formula states the
semantic condition for a general batch, the machine-checked models instantiate
only `n = 2` and provide no arbitrary-size result.

The intended interpretation is that each accepted slot represents a distinct
modeled protocol-principal coordinate in that batch. Within the modeled
admission boundary, `DistinctPartyPerBatch` is necessary for preserving that
party-level batch identity semantics. This is the only necessity claim made in
the paper.

### 3.2 Relaxation and Message-Level Control

R-semantics removes the party-level restriction. Once two entries have been
collected, admission does not compare their `A` coordinates. The immediate
composition question is whether the same coordinate can occupy both slots and
what acceptance behavior follows.

M-semantics instead requires `m1 != m2`. This is a useful control because the
assignment `A1 = A2` together with `m1 != m2` is consistent: two messages can
be different while belonging to the same modeled party. P-semantics compares
`A1` and `A2` directly and serves as the modeled restoration of the intended
party-level condition. P-semantics is one realization of the invariant, not a
claim about a uniquely required implementation algorithm or location.

### 3.3 Research Questions

The comparison addresses three research questions:

- **RQ1:** What batch compositions become reachable when
  `DistinctPartyPerBatch` is removed?
- **RQ2:** Can removal of the invariant produce duplicate receiver acceptance
  within the fixed-two-slot symbolic model?
- **RQ3:** Can a message-level restriction substitute for party-level
  uniqueness, or does the modeled comparison require party-level admission to
  restore the intended semantics?

RQ3 compares formal coordinates and the three executable semantics. It does
not prescribe how every implementation must maintain the invariant.

## 4. Threat Model

### 4.1 Batch-Composition Adversary

The adversarial surface is the modeled `BatchReceive` admission boundary. A
batch-composition adversary selects or arranges admissible symbolic entries,
places them in the two slots, and triggers behavior allowed by the selected
admission semantics. In R-semantics, the absence of a party-uniqueness guard
allows the adversary to repeat one valid modeled protocol-principal coordinate
in both positions.

The relevant composition is therefore `slot 1 -> A` and `slot 2 -> A`. It does
not require inventing a second identity or presenting the repeated coordinate
as a different party. The question is whether a candidate vector with that
identity structure reaches receiver processing.

### 4.2 Goal and Supported Consequence

The adversary's goal is to have a same-batch repeated-party composition
admitted when the invariant is absent. The bounded formal consequence is a
reachable duplicate-acceptance pattern: one matching `Send(A,sid,m)` occurrence
can correspond to two `ReceiverAccept(A,sid,m,bid,rst)` occurrences in the
same batch and receiver-state context. Calling the composition invalid means
that it violates the stated party-level invariant.

The semantic consequence is loss of the intended party-level identity
interpretation. This conclusion interprets the admitted coordinates; it is not
a separate modeled event or an additional prover result.

### 4.3 Excluded Capabilities and Consequences

The construction does not require recovering secret keys, breaking a KEM,
forging signatures or HMACs, impersonating another party, or modifying
authenticated material. These are boundary statements, not verified
cryptographic properties: the admission models contain none of those
mechanisms. The threat model also makes no inference about deployment behavior,
output consumption, installation, confidentiality, or application state.

## 5. Formal Model

### 5.1 Modeling Objective and Common Lifecycle

The three Tamarin theories isolate one `BatchReceive` admission decision in a
fixed-two-slot symbolic model. They share party creation, sender origin,
two-entry collection, a fresh batch identifier, a fresh receiver-state
coordinate, sequential slot processing, and the same acceptance events. The
only principal variation is the predicate applied after collection.

`CreateParty` generates a fresh `A` and stores `!Party(A)`. `SendMessage`
combines that persistent fact with fresh `sid` and `m`, emits
`Send(A,sid,m)`, exposes `<A,sid,m>` to the adversarial network, and records a
persistent `!Sent(A,sid,m)` origin fact. A two-slot batch then follows the
linear collection lifecycle

```text
CreateBatch(bid,rst)
  -> CollectSlot1(A1,sid1,m1)
  -> CollectSlot2(A2,sid2,m2)
  -> Collected(bid,rst,A1,sid1,m1,A2,sid2,m2).
```

After admission, slot processing is sequential. A slot can emit
`ReceiverAccept(A,sid,m,bid,rst)` only with a matching persistent
`!Sent(A,sid,m)` fact. The slot-1 acceptance advances processing to slot 2;
the second completes the batch. This common structure retains the sender
origin relation while exposing admission multiplicity and party composition.

### 5.2 R-Semantics: Relaxed Admission

R-semantics admits the collected pair without requiring either `A1 != A2` or
`m1 != m2`. Both a same-party/different-message pair and a repeated complete
tuple are therefore allowed by the admission rule. R-semantics provides the
invariant-removed baseline against which the other two models are compared.

### 5.3 M-Semantics: Message Deduplication

M-semantics branches on the message coordinates. If `m1 = m2`, the model emits
`Reject(bid,rst)` and reaches a rejected state. The admitted branch emits
`Neq(m1,m2)` and `BatchReceive(bid,rst)`; a global inequality restriction
rules out `Neq(x,x)`. No corresponding condition is placed on `A1` and `A2`.
The model therefore enforces exact-message distinction while leaving
same-party/different-message composition available.

### 5.4 P-Semantics: Party Admission

P-semantics applies the analogous decision to party coordinates. If `A1 = A2`,
the model emits `Reject(bid,rst)` and reaches a rejected state. The admitted
branch emits `Neq(A1,A2)` and `BatchReceive(bid,rst)`, subject to the same
inequality restriction. A distinct-party pair can proceed through both
acceptance slots. P-semantics is an executable restoration of
`DistinctPartyPerBatch` at the abstract admission boundary.

### 5.5 Events and Properties

The analysis uses five action-event forms. `Send(A,sid,m)` records a sender
occurrence. `BatchReceive(bid,rst)` records admission. `ReceiverAccept(A,sid,m,
bid,rst)` records acceptance of one slot with a matching origin fact.
`Reject(bid,rst)` records an M- or P-semantics rejection, and `Neq(x,y)` records
the admitted branch's inequality guard.

The properties fall into four groups. Existence lemmas establish reachable
normal, rejection, same-party, distinct-party, or duplicate-acceptance traces.
`receiver_accept_has_send` checks prior matching sender origin.
`receiver_accept_injective` checks whether two accept occurrences for the same
send tuple and batch context must be the same event occurrence. Finally,
`accepted_batch_has_distinct_messages` and
`accepted_batch_has_distinct_parties` check the coordinate-specific safety
conditions of M- and P-semantics.

### 5.6 Abstraction Boundary

The theories do not encode KEM operations, signatures, HMAC computation,
compromise rules, prekey cryptography, key derivation, Double Ratchet state,
output-key objects, or an application consumer. They do not model arbitrary
batch lengths, cross-batch behavior, rollback, restart, concurrency, fairness,
or deployment enforcement. The abstraction is intentionally limited to the
identity coordinate checked at admission and the resulting rejection and
`ReceiverAccept` lifecycle.

## 6. Formal Analysis

### 6.1 RQ1: Repeated-Party Composition

RQ1 asks what becomes reachable after removing the party-level invariant.
R-semantics supplies the semantic premise: its admission rule does not compare
`A1` and `A2`. The verified `normal_relaxed_batch_exists` property establishes
that receiver processing is reachable rather than blocked by the abstraction.
The stronger `one_send_two_accepts_exists` witness instantiates both slots with
the same complete sender tuple. Because the two accepted slots carry the same
`A`, the witness is also a repeated-party composition.

The formal and semantic conclusions should be separated. The model establishes
admission and acceptance events with repeated coordinates. The conclusion that
this composition loses the intended party-level identity interpretation follows
from comparing those coordinates with the invariant defined in Section 3; it
is not an additional Tamarin property.

### 6.2 RQ2: Duplicate Receiver Acceptance

The duplicate-acceptance witness contains one matching
`Send(A,sid,m) @ s` occurrence followed by two acceptances

```text
ReceiverAccept(A,sid,m,bid,rst) @ r1
ReceiverAccept(A,sid,m,bid,rst) @ r2
```

with `s < r1 < r2` and distinct acceptance timepoints. The verified
`one_send_two_accepts_exists` lemma establishes this trace, while the universal
`receiver_accept_injective` lemma is falsified in R-semantics. The accompanying
`receiver_accept_has_send` property is verified, so the counterexample is not
caused by an acceptance that lacks a matching modeled sender origin.

This answers RQ2 within one batch and receiver-state context. It does not imply
that a separate consumer processes both occurrences, because no such consumer
appears in the theories.

### 6.3 RQ3: Message and Party Controls

M-semantics tests whether exact-message distinction is sufficient for the
party-level objective. Its verified `repeated_message_rejection_exists`
property shows that the equal-message rejection branch is reachable, and
`accepted_batch_has_distinct_messages` is verified for admitted pairs. The
scoped `receiver_accept_injective` property is also verified. These results
show that M-semantics achieves the message-coordinate and occurrence goals
encoded in that theory.

At the same time, `same_party_different_messages_batch_exists` is verified. Its
witness uses two legitimate sender occurrences with the same `A` and different
`sid` and `m` coordinates, followed by one acceptance for each entry. The
combination is decisive for RQ3: scoped occurrence injectivity can hold while
same-batch party uniqueness does not.

P-semantics compares the party coordinate named by the invariant.
`same_party_rejection_exists` verifies a reachable rejection of two different
messages from the same modeled party, and
`accepted_batch_has_distinct_parties` verifies party distinctness for admitted
pairs. The result is non-vacuous: `distinct_party_batch_exists` verifies a
trace with two distinct modeled parties, two legitimate sender occurrences,
one admitted batch, and two acceptances. P-semantics therefore restores the
intended identity semantics in this comparison without rejecting every batch.

### 6.4 Comparative Answer

The three questions yield one bounded argument chain:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> loss of intended party-level identity interpretation.
```

The initial four stages are grounded in the relaxed admission semantics and
recorded reachability or correspondence results. “Invalid” means inconsistent
with the specified invariant. The final stage is the semantic interpretation
of that mismatch. M-semantics establishes that a message-coordinate control can
remove the exact one-Send/two-accept occurrence while leaving party repetition
reachable. P-semantics checks the party coordinate itself and restores the
intended interpretation.

## 7. Evaluation

### 7.1 Verification Setup

The recorded verification used Tamarin 1.12.0 with Maude 3.5.1 under WSL
Ubuntu 24.04. The recorded executable was
`/home/linuxbrew/.linuxbrew/bin/tamarin-prover`, with
`/home/linuxbrew/.linuxbrew/bin:/usr/bin:/bin` as the non-interactive path.
Models were parsed using `tamarin-prover --parse-only` and properties were
executed using `tamarin-prover --prove`. This paper preparation did not rerun
the prover; it reports the existing executions and binds them to the model
hashes below.

### 7.2 Recorded Results

Table 1 is the complete set of prover outcomes used in the paper. “Falsified”
means that Tamarin found a counterexample trace for the universal property.

| Semantics | Property | Outcome | Steps |
| --- | --- | --- | ---: |
| R | `normal_relaxed_batch_exists` | verified | 10 |
| R | `one_send_two_accepts_exists` | verified | 13 |
| R | `receiver_accept_has_send` | verified | 8 |
| R | `receiver_accept_injective` | falsified; trace found | 13 |
| M | `repeated_message_rejection_exists` | verified | 4 |
| M | `same_party_different_messages_batch_exists` | verified | 16 |
| M | `accepted_batch_has_distinct_messages` | verified | 31 |
| M | `receiver_accept_has_send` | verified | 8 |
| M | `receiver_accept_injective` | verified | 33 |
| P | `same_party_rejection_exists` | verified | 5 |
| P | `distinct_party_batch_exists` | verified | 17 |
| P | `accepted_batch_has_distinct_parties` | verified | 31 |
| P | `receiver_accept_has_send` | verified | 8 |
| P | `receiver_accept_injective` | verified | 33 |

The cross-model comparison separates two dimensions. M-semantics verifies
receiver-occurrence injectivity and accepted-message distinction while still
admitting a same-party/different-message batch. P-semantics verifies
receiver-occurrence injectivity and admitted-party distinction, and its valid
distinct-party witness confirms non-vacuity. R-semantics provides the duplicate
witness and counterexample to scoped injectivity.

Rejection properties are reachability statements, not liveness results. In
particular, `same_party_rejection_exists` does not assert that every collected
invalid pair must eventually take an enabled rejection transition.

### 7.3 Reproducibility Binding

The verification package records the environment, parse and prove commands,
model hashes, and a manifest relating models to their reported results. The
three SHA-256 bindings are:

| Model | SHA-256 |
| --- | --- |
| `rqv2_relaxed.spthy` | `E5129575720020AA3F509782C2052FBF2114A540D013126F5A75D316CBABAF9D` |
| `rqv2_message_dedup.spthy` | `90A196F5DA5C244026596283D001376427880CD64C5BEA3C6CFDFD4CCBA99184` |
| `rqv2_party_admission.spthy` | `C35AF64CAC7F01182418CB999EA105214B8DA4F2295B670A9B3733F0BD976BBA` |

The package does not include raw prover transcripts and is not presented as an
independent repeat execution. Its role is provenance and traceability for the
recorded results.

## 8. Discussion

### 8.1 Invariant and Enforcement

`DistinctPartyPerBatch` appears operationally as an admission condition, but
its role is semantic: it preserves the interpretation that different accepted
slots correspond to different modeled parties. An individually well-formed
entry with a matching sender origin can still participate in a composition
that violates this relation. The relevant design obligation is therefore to
preserve the identity invariant at the composition boundary.

P-semantics realizes the invariant by comparing `A1` and `A2` during admission.
That check is one modeled enforcement mechanism, not the contribution itself
and not a uniquely prescribed implementation. A trusted caller, batch builder,
or receiver admission layer could in principle maintain the same relationship;
the present analysis evaluates none of those deployment choices.

### 8.2 Occurrence Injectivity and Party Uniqueness

Occurrence injectivity asks whether a matching sender occurrence can support
more than one acceptance occurrence under the lemma's batch and receiver-state
scope. Party uniqueness asks whether different accepted slots carry different
`A` coordinates. M-semantics demonstrates their non-equivalence: its injective
property is verified while its same-party/different-message witness is also
verified.

Injectivity is therefore a supporting comparison dimension, not a new notion
or the primary contribution. Established authentication literature already
provides injective correspondence vocabulary
([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf),
[L19](https://www.sciencedirect.com/science/article/pii/S2352220815000528)).
The contribution here is the controlled separation of that occurrence
property from party-level batch identity in the K-Waay `BatchReceive` setting.

### 8.3 Message Deduplication and HMAC

Exact-message deduplication constrains `m1` and `m2`; party admission constrains
`A1` and `A2`. M-semantics is effective for its modeled message-level purpose:
it makes repeated-message rejection reachable, proves accepted messages
distinct, and restores scoped occurrence injectivity. It does not establish a
predicate over party coordinates. The result therefore identifies different
property dimensions rather than a general deficiency in deduplication.

HMAC-based mechanisms similarly concern message authenticity, integrity, or
confirmation under their surrounding assumptions. Those relations do not by
themselves establish party inequality across batch slots. No HMAC result is
used as evidence for the present R/M/P-semantics comparison.

### 8.4 Conceptual Interface Motivation

K-Waay's party-indexed interface motivates why unique party interpretation has
semantic value. If a party coordinate is intended to select a corresponding
component in `KEY` or `TEST`, repeated use of that coordinate within one batch
would require an additional rule to make the party-level attribution unique.
This observation explains a semantic dependency; it is not a verified
interface failure.

The models contain no `KEY` or `TEST` query operations, output-key objects, or
key-correctness relations. Consequently, all formal conclusions in this paper
stop at admission, rejection, `ReceiverAccept`, and the stated correspondence
and coordinate properties.

### 8.5 Conditional Upper-Layer Impact

The direct model contains no consumer that independently processes every
`ReceiverAccept` occurrence. Duplicate acceptance therefore does not establish
duplicate installation or another application action. A historical
composition model using the explicit `C_install-v2` consumer assumption
illustrates a conditional extension: if each acceptance is consumed
independently, duplicate acceptances can propagate to duplicate symbolic
installations. That result depends on a separate model and assumption and is
not part of the direct R/M/P evidence.

### 8.6 Why the Bounded Comparison Matters

The two-slot instance is the smallest batch in which pairwise party
distinctness can be violated. It isolates the identity coordinate without
requiring unrelated protocol machinery and is sufficient to witness the
specific repeated-party and duplicate-acceptance behaviors reported here. It
does not establish that the proofs generalize to larger batches.

The comparison also goes beyond the tautology that removing `A1 != A2` permits
`A1 = A2`. It connects that relaxation to a reachable receiver-level
consequence, uses M-semantics to distinguish occurrence and identity
properties, and uses P-semantics to establish both restoration and non-vacuity.

## 9. Limitations

The machine-checked evidence covers one symbolic fixed-two-slot batch. The
general definition of `DistinctPartyPerBatch` states the intended relation,
but the results do not prove the relation or the R/M/P comparison for arbitrary
batch length.

The models isolate admission and the `ReceiverAccept` lifecycle. They omit the
complete K-Waay cryptographic construction, signatures, HMAC computation,
prekey processing, key derivation, Double Ratchet state, compromise rules,
output-key objects, application consumers, and deployment behavior. The
results accordingly make no claim about secrecy, authentication, key
correctness, a public implementation, or real-world exploitability.

The theories do not analyze cross-batch behavior, rollback, restart,
concurrency, distributed enforcement, or fairness. Rejection lemmas establish
reachable rejection branches rather than eventual rejection of every invalid
input. P-semantics also represents only one enforcement placement; the evidence
does not show that it is the only algorithm or component capable of preserving
the invariant.

Finally, the reproducibility package binds models, commands, environment, and
recorded outcomes but does not contain raw prover transcripts or a newly
repeated verification run. These limitations constrain the evidence to a
specification-level identity analysis at the modeled admission boundary.

## 10. Related Work

### 10.1 K-Waay and Post-Quantum Asynchronous Key Exchange

K-Waay is the direct protocol context for this work. Collins et al. construct
an efficient, deniable, post-quantum X3DH-like deniable authenticated key
exchange from split-KEM techniques and introduce `BatchReceive` to model
receiver-side processing when ephemeral material is reused across several
inputs ([L1](https://www.usenix.org/conference/usenixsecurity24/presentation/collins)).
The K-Waay specification already states that, for a given `BatchReceive` call,
each input element corresponds to a different party. The present work does not
claim to discover that condition, correct the construction, or challenge the
computational proof. It instead asks what party-level interpretation the stated
condition maintains and whether its semantic necessity can be exhibited in a
bounded symbolic admission model.

This positioning separates two proof boundaries. K-Waay develops
computational security games and reductions for its DAKE and split-KEM
construction, including key indistinguishability, implicit authentication, and
deniability. Our analysis abstracts away those primitives and properties and compares
three admission semantics over a fixed-two-slot batch. Its evidence is
therefore not a full symbolic verification of K-Waay and does not transfer to
the computational guarantees established by Collins et al.

The broader asynchronous-messaging line reinforces this separation. Formal
analysis of Signal treats X3DH and the Double Ratchet as a multi-stage
authenticated key-exchange system ([L2](https://link.springer.com/article/10.1007/s00145-020-09360-1)),
while the X3DH specification explicitly distinguishes authentication,
protocol replay, key reuse, and identity binding
([L13](https://signal.org/docs/specifications/x3dh/)). Formal verification of
PQXDH translates a prose specification into ProVerif and CryptoVerif models
and makes the corresponding assumptions, ambiguities, and model boundaries
explicit ([L3](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan)).
These works share the asynchronous key-exchange setting and the need for
precise identity/session modeling; their main properties concern
cryptographic-session security, whereas our analysis isolates party composition at
the `BatchReceive` admission boundary.

### 10.2 Formal Analyses of Secure Messaging

Formal secure-messaging research spans computational and symbolic methods.
The Signal analysis gives a computational account of X3DH and Double Ratchet
security ([L2](https://link.springer.com/article/10.1007/s00145-020-09360-1));
the PQXDH study uses both ProVerif and CryptoVerif to analyze authentication,
confidentiality, post-quantum forward secrecy, and co-deployment
([L3](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan));
and session-handling research uses Tamarin to study what happens when an
application composes several ratcheting chains into a conversation
([L4](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)).
Together, these analyses show why formalizing specification and application
details can reveal which assumptions belong to a security statement and where
an abstraction boundary lies. They do not imply that every modeled detail is
a vulnerability or that one verification method subsumes the others.

We use Tamarin's multiset-rewriting trace framework
([L11](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48))
only to express a minimal admission lifecycle and its reachability and
correspondence properties. Tool choice is inherited methodology, not a
contribution. Although Tamarin supports substantially broader symbolic
analyses, the current prototypes explicitly encode one fixed-two-slot batch
and omit KEMs, signatures, HMAC computation, compromise, prekey cryptography,
Double Ratchet, and application behavior.

Secure-messaging taxonomies further distinguish trust establishment,
participant consistency, authentication, destination validation, speaker
consistency, and message-oriented properties
([L18](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf)).
Our analysis shares this discipline of separating property dimensions. Its target is
neither a general secure-messaging definition nor participant-list agreement;
it is the narrower question of whether two slots in one admitted batch retain
a distinct modeled-party interpretation.

### 10.3 Session- and Composition-Layer Security

A central lesson from composition research is that security established for a
component does not automatically determine the property of the object into
which that component is composed. In secure messaging, a conversation may
merge multiple individually protected ratcheting chains. The Tamarin analysis
of Signal's session-handling layer demonstrates that conversation-level
post-compromise security must therefore be analyzed separately from
single-session guarantees
([L4](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)).
Analysis of healing across several groups similarly shows that update and
compromise effects depend on whether a user is represented through pairwise
channels or group-key state
([L20](https://www.usenix.org/conference/usenixsecurity21/presentation/cremers)).

General compositional-verification frameworks formalize the same methodological
concern through conditions such as protocol independence and preservation of
component properties in a multi-protocol environment
([L21](https://research.tue.nl/en/publications/a-framework-for-compositional-verification-of-security-protocols/)).
Our work is adjacent to this literature because it treats admission as a semantic
composition boundary: individually legitimate entries are composed into one
accepted `BatchReceive` batch. The shared dimension is the need to state and
check a composition condition. The objects and properties differ: prior work
studies session-to-conversation lifting, cross-group healing, or composition of
whole protocols, while our analysis studies pairwise distinctness of modeled party
coordinates within one batch. Those studies do not prove
`DistinctPartyPerBatch`, and our result does not establish their PCS or
protocol-independence properties.

### 10.4 Group Membership, State Consistency, and Administration

Secure group messaging separates several relationships that can otherwise be
collapsed under “membership.” TreeSync gives a formal and executable account
of MLS shared group state, including consistency, integrity, authentication,
and group-management operations
([L5](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez)).
Cryptographic administration adds authorization and membership-consistency
guarantees for administrator-controlled add and remove operations
([L6](https://www.usenix.org/system/files/usenixsecurity23-balbas.pdf)). Modular
analysis of MLS instead decomposes secure group messaging into cryptographic
components and derives a security predicate from the guarantees of those
components ([L7](https://eprint.iacr.org/2021/1083)). The secure-messaging
taxonomy places participant consistency alongside, but separately from,
authentication and message/transcript properties
([L18](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf)).

These works establish that member-indexed state, participant-list agreement,
membership authorization, and cryptographic group composition are substantive
security concerns. None of those notions is identical to our property.
Membership consistency asks whether parties share the intended view of a
group; administration asks who may change that group; TreeSync protects an
evolving group-state representation; and modular MLS concerns composition of
cryptographic primitives and predicates. `DistinctPartyPerBatch` instead
requires that two different positions of one admitted batch carry different
modeled party coordinates. Our work neither attributes this invariant to group
messaging nor transfers its bounded result to MLS or another group protocol.

### 10.5 Identity Binding, Names, and Authentication

Identity/name uniqueness is already recognized as a security-relevant semantic
assumption. Lupetti, Dillema, and Stabell-Kulø argue that principal names must
remain unique across appropriately correlated protocol sessions if those names
are to retain their intended meaning, and they discuss local and global means
of verifying that assumption
([L16](https://www.scitepress.org/papers/2006/24847/24847.pdf)). Chosen-name
analysis further shows that allowing an adversary to select or assign agent
names changes the formal attack surface and can produce type-flaw attacks
([L17](https://satoss.uni.lu/papers/CMR07.pdf)). These works limit our
novelty: the general idea that identity-bearing names require carefully scoped
semantic assumptions is not introduced here.

The specific identity relation is nevertheless different. The name-uniqueness
work concerns distinct and meaningful principal naming across correlated
sessions, particularly where one session's messages can be reused in another.
We assume an explicit modeled party coordinate and ask whether the same
coordinate may occupy two different slots of one admitted batch. Its novelty
claim is therefore confined to normalizing and testing the K-Waay condition at
that boundary, not to identity uniqueness as a general concept.

Identity binding and authentication introduce further neighboring, but
non-equivalent, relations. Lowe's hierarchy distinguishes aliveness,
agreement, and injective agreement between protocol runs
([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)).
Formal misbinding analysis examines executions in which an endpoint, device,
or run becomes associated with the wrong identity
([L9](https://acris.aalto.fi/ws/portalfiles/portal/36903088/Sethi_Peltonen_Aura_Misbinding_Attacks_on_Secure_Device.pdf)).
UKS analysis for TLS with SDP likewise concerns a malicious binding between an
external identity and another endpoint's key, fingerprint, or session
([L15](https://www.rfc-editor.org/rfc/rfc8844.html)). Our
repeated-party composition does not, on current evidence, establish that an
endpoint is bound to the wrong identity or that peers disagree about with whom
they share a key. **The repeated-party result is not established as a misbinding or UKS attack.**
The shared dimension is precise identity interpretation; the formal failure
relations remain distinct.

### 10.6 Replay, Deduplication, and Injectivity

Replay and injective correspondence are mature protocol-analysis concepts.
The X3DH specification discusses replayed initial messages, repeated
acceptance, and resulting key reuse as explicit security considerations
([L13](https://signal.org/docs/specifications/x3dh/)). Lowe's authentication
hierarchy characterizes injective agreement through a one-to-one relation
between relevant runs
([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)).
A later automated type-based analysis formalizes injective agreement through
unique matching begin/end resources and illustrates how one transmitted
message copied to two receiver processes violates that occurrence relation
([L19](https://www.sciencedirect.com/science/article/pii/S2352220815000528)).
Our work does not introduce injectivity or replay correspondence.

Its supported comparison concerns the boundary between occurrence and party
identity. In M-semantics, exact-message admission verifies
`receiver_accept_injective`: within the model's batch and receiver-state scope,
one matching sender occurrence cannot support two accept occurrences. At the
same time, `same_party_different_messages_batch_exists` is verified, so two
different messages and sender occurrences belonging to the same modeled party
can occupy the two slots. Thus, in this model, scoped occurrence injectivity
does not imply party-level batch uniqueness.

This result does not make message deduplication ineffective. Exact-message
deduplication controls message equality and, in the prototype, restores the
stated occurrence property. Party admission controls a separate coordinate,
`A1 != A2`. Authentication, integrity protection, replay handling, message
deduplication, and party uniqueness should therefore be evaluated against
their respective properties rather than treated as interchangeable repairs.

### 10.7 Positioning of This Work

Within the verified literature corpus and search scope, we found no work that
performs the complete `DistinctPartyPerBatch` removal, comparison, and
restoration analysis. This is a scoped search conclusion, not an exhaustive
claim about all literature. The closest prior work addresses the underlying
protocol, identity/name uniqueness, session composition, membership
consistency, or injective correspondence. Our analysis instead isolates their
intersection at the `BatchReceive` party-admission boundary.

Two contributions have strong support within that scope. One is a
bounded formal analysis of K-Waay's already stated distinct-party
`BatchReceive` condition: R-semantics removes party-level admission,
P-semantics restores it, and the comparison records both an invalid
repeated-party composition and a reachable valid distinct-party batch. Second,
the M-semantics control demonstrates that scoped occurrence injectivity can
hold while party-level uniqueness still fails. Both statements are limited to
the symbolic fixed-two-slot admission models and their recorded properties.

Two further contributions require more moderate wording. The separation of
message-level uniqueness from party uniqueness is novel here only as the
controlled `BatchReceive` comparison; the abstract distinction between
messages and identities is established background. Likewise, treating the
different-party condition as a semantic invariant rather than prescribing a
specific enforcement check is a contribution of this K-Waay analysis, not a
new general concept of invariants or composition-layer security.

This positioning makes no claim that K-Waay omits its condition, that its
computational theorem is invalid, or that a deployed implementation violates
the invariant. It also makes no claim of cryptographic failure, misbinding,
UKS, `KEY`/`TEST` failure, arbitrary-length security, or unconditional
upper-layer impact.

## 11. Conclusion

This paper analyzed the semantic role of K-Waay's stated distinct-party
`BatchReceive` condition, which we normalize as `DistinctPartyPerBatch`. The
analysis answers the research question at the modeled admission boundary:
preserving this party-level identity invariant is necessary for preserving the
intended interpretation that distinct slots in one admitted batch represent
distinct modeled protocol-principal coordinates.

The R/M/P-semantics comparison makes that conclusion concrete. Removing party
uniqueness in R-semantics permits repeated-party composition and a reachable
one-Send/two-`ReceiverAccept` behavior. Exact-message deduplication in
M-semantics restores the scoped occurrence-injectivity property while leaving
same-party/different-message admission reachable. Party-level admission in
P-semantics restores the intended distinct-party batch semantics, makes
same-party rejection reachable, and retains a reachable valid distinct-party
batch.

These results separate three relations that should not be conflated: party
identity, message identity, and occurrence injectivity. A one-to-one relation
between a sender occurrence and receiver acceptances can hold even when two
different messages from the same modeled party occupy one batch. The identity
coordinate constrained by an admission rule must therefore match the semantic
relationship that the batch is intended to preserve.

The evidence is limited to symbolic fixed-two-slot admission models and ends
at `ReceiverAccept`; it supports no conclusion about deployment behavior or
cryptographic security. The resulting design obligation is to preserve the
party-level identity invariant at the relevant composition boundary, not to
mandate one uniquely specified enforcement mechanism.

## References

**[L1]** Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh Nguyen, Nicolas
Rolin, and Serge Vaudenay. “K-Waay: Fast and Deniable Post-Quantum X3DH
without Ring Signatures.” *33rd USENIX Security Symposium*, 2024, pp. 433–450.
[URL](https://www.usenix.org/conference/usenixsecurity24/presentation/collins).

**[L2]** Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt, and
Douglas Stebila. “A Formal Security Analysis of the Signal Messaging
Protocol.” *Journal of Cryptology*, vol. 33, 2020, pp. 1914–1983.
[DOI](https://doi.org/10.1007/s00145-020-09360-1).

**[L3]** Karthikeyan Bhargavan, Charlie Jacomme, Franziskus Kiefer, and Rolfe
Schmidt. “Formal Verification of the PQXDH Post-Quantum Key Agreement Protocol
for End-to-End Secure Messaging.” *33rd USENIX Security Symposium*, 2024,
pp. 469–486.
[URL](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan).

**[L4]** Cas Cremers, Charlie Jacomme, and Aurora Naska. “Formal Analysis of
Session-Handling in Secure Messaging: Lifting Security from Sessions to
Conversations.” *32nd USENIX Security Symposium*, 2023, pp. 1235–1252.
[URL](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling).

**[L5]** Théophile Wallez, Jonathan Protzenko, Benjamin Beurdouche, and
Karthikeyan Bhargavan. “TreeSync: Authenticated Group Management for Messaging
Layer Security.” *32nd USENIX Security Symposium*, 2023, pp. 1217–1233.
[URL](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez).

**[L6]** David Balbás, Daniel Collins, and Serge Vaudenay. “Cryptographic
Administration for Secure Group Messaging.” *32nd USENIX Security Symposium*,
2023, pp. 1253–1270.
[URL](https://www.usenix.org/system/files/usenixsecurity23-balbas.pdf).

**[L7]** Joël Alwen, Sandro Coretti, Yevgeniy Dodis, and Yiannis Tselekounis.
“Modular Design of Secure Group Messaging Protocols and the Security of MLS.”
*ACM SIGSAC Conference on Computer and Communications Security*, 2021,
pp. 1463–1483. [DOI](https://doi.org/10.1145/3460120.3484820).

**[L9]** Mohit Sethi, Aleksi Peltonen, and Tuomas Aura. “Misbinding Attacks on
Secure Device Pairing and Bootstrapping.” *ACM Asia Conference on Computer and
Communications Security*, 2019, pp. 453–464.
[DOI](https://doi.org/10.1145/3321705.3329813). Extended journal version:
“Formal Verification of Misbinding Attacks on Secure Device Pairing and
Bootstrapping,” *Journal of Information Security and Applications*, vol. 51,
2020, article 102461.
[DOI](https://doi.org/10.1016/j.jisa.2020.102461).

**[L10]** Gavin Lowe. “A Hierarchy of Authentication Specifications.” *10th
IEEE Computer Security Foundations Workshop*, 1997, pp. 31–43.
[DOI](https://doi.org/10.1109/CSFW.1997.596782).

**[L11]** Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. “The
TAMARIN Prover for the Symbolic Analysis of Security Protocols.” *Computer
Aided Verification (CAV 2013), LNCS 8044*, 2013, pp. 696–701.
[DOI](https://doi.org/10.1007/978-3-642-39799-8_48).

**[L13]** Moxie Marlinspike and Trevor Perrin. “The X3DH Key Agreement
Protocol.” Signal Protocol Specification, Revision 1, 2016.
[URL](https://signal.org/docs/specifications/x3dh/).

**[L15]** Martin Thomson and Eric Rescorla. “Unknown Key-Share Attacks on Uses
of TLS with the Session Description Protocol (SDP).” RFC 8844, 2021.
[DOI](https://doi.org/10.17487/RFC8844).

**[L16]** Simone Lupetti, Feike W. Dillema, and Tage Stabell-Kulø. “Names in
Cryptographic Protocols.” *4th International Workshop on Security in
Information Systems (WOSIS 2006)*, 2006, pp. 185–194.
[URL](https://www.scitepress.org/papers/2006/24847/24847.pdf).

**[L17]** Pieter Ceelen, Sjouke Mauw, and Saša Radomirović. “Chosen-Name
Attacks: An Overlooked Class of Type-Flaw Attacks.” *Electronic Notes in
Theoretical Computer Science*, vol. 197, no. 2, 2008, pp. 31–43.
[DOI](https://doi.org/10.1016/j.entcs.2007.12.015).

**[L18]** Nik Unger, Sergej Dechand, Joseph Bonneau, Sascha Fahl, Henning Perl,
Ian Goldberg, and Matthew Smith. “SoK: Secure Messaging.” *2015 IEEE Symposium
on Security and Privacy*, 2015, pp. 232–249.
[DOI](https://doi.org/10.1109/SP.2015.22).

**[L19]** B. Sattarzadeh and M. S. Fallah. “Automated Type-Based Analysis of
Injective Agreement in the Presence of Compromised Principals.” *Journal of
Logical and Algebraic Methods in Programming*, vol. 84, no. 5, 2015,
pp. 576–610. [DOI](https://doi.org/10.1016/j.jlamp.2015.06.002).

**[L20]** Cas Cremers, Britta Hale, and Konrad Kohbrok. “The Complexities of
Healing in Secure Group Messaging: Why Cross-Group Effects Matter.” *30th
USENIX Security Symposium*, 2021, pp. 1847–1864.
[URL](https://www.usenix.org/conference/usenixsecurity21/presentation/cremers).

**[L21]** Suzana Andova, Cas Cremers, Kristian Gjøsteen, Sjouke Mauw, Stig F.
Mjølsnes, and Saša Radomirović. “A Framework for Compositional Verification of
Security Protocols.” *Information and Computation*, vol. 206, nos. 2–4, 2008,
pp. 425–459. [DOI](https://doi.org/10.1016/j.ic.2007.07.002).
