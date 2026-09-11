# RQ-v2 Complete Argument Map

## Status

Frozen RQ-v2 **Primary Authority** argument-map artifact.

This is the canonical argument map for the frozen RQ-v2 line. The word
`complete` describes its end-to-end coverage; it does not denote one member of
a `complete`/`final`/`latest` version sequence.

This document connects the semantic definition, threat model, bounded symbolic
evidence, comparison mechanisms, restoration model, conceptual interface
motivation, and claim boundary of the current RQ-v2 research direction.

The evidence classes are distinct:

- **Formal evidence** comes from `rqv2_relaxed.spthy`,
  `rqv2_message_dedup.spthy`, and `rqv2_party_admission.spthy`.
- **Conceptual analysis** comes from interpreting the original K-Waay
  party-indexed security interface.

The current prototypes do not formalize output keys, `KEY`, `TEST`, or an
upper-layer consumer. This map does not claim a deployed vulnerability, a
cryptographic break, or invalidation of an original theorem.

------------------------------------------------------------------------

# Step 1: Invariant Definition

`DistinctPartyPerBatch` requires distinct slots in one `BatchReceive` batch to
carry distinct modeled party coordinates:

    for every i != j:

    party_i != party_j

Here `A` is the modeled protocol-principal identity coordinate. It is not
identified with a deployed identity, database identity, or implementation
object.

The invariant constrains one batch only. One party may participate in multiple
sessions, send multiple messages, and occur in different batches.

------------------------------------------------------------------------

# Step 2: Why the Invariant Matters

With the invariant:

    slot 1 → Party A
    slot 2 → Party B

Without the invariant:

    slot 1 → Party A
    slot 2 → Party A

The second batch loses the intended one-party-per-slot identity
interpretation. This is a statement about batch composition, not about a key
or output object.

------------------------------------------------------------------------

# Step 3: Threat Model

The RQ-v2 adversary is a batch-composition adversary. The adversary can cause
two entries carrying the same valid modeled party coordinate to occupy two
slots of one batch when the identity guard is absent.

The construction does not require breaking cryptography, forging or modifying
authenticated material, or recovering keys. Those mechanisms are not modeled
by the current RQ-v2 prototypes.

------------------------------------------------------------------------

# Step 4: Relaxed Attack Trace

The complete formally supported chain is:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

In `rqv2_relaxed.spthy`, a trace with one `Send` occurrence and two
`ReceiverAccept` occurrences for the same modeled sender identity and receiver
batch context is reachable. This establishes duplicate acceptance at the
modeled boundary. It does not establish key compromise, confidentiality
failure, output-key confusion, or unconditional upper-layer impact.

------------------------------------------------------------------------

# Step 5: Security-Interface Dependency

`DistinctPartyPerBatch` provides the semantic basis for the intended
party-indexed interpretation of one batch.

The original K-Waay interface motivates this dependency: if a party coordinate
is used to select a corresponding output or query object, repeated use of that
coordinate in one batch creates ambiguous party-level attribution unless an
additional selection rule is supplied.

This is conceptual analysis. The current RQ-v2 prototypes do not directly
formalize `KEY`, `TEST`, output keys, or correctness relations over keys, and
therefore do not prove a failure of those objects or interfaces.

------------------------------------------------------------------------

# Step 6: Message and HMAC Comparison

The message-dedup prototype compares a different coordinate. Exact-message
deduplication can reject:

    Party A, Message M
    Party A, Message M

while still admitting:

    Party A, Message M1
    Party A, Message M2

It can restore scoped occurrence injectivity in that model, but it does not
enforce same-batch party uniqueness.

HMAC concerns message authenticity, integrity, or confirmation. It does not
establish party uniqueness or batch-admission semantics. Neither mechanism is
the main RQ-v2 contribution.

------------------------------------------------------------------------

# Step 7: Restoration Model

The party-admission prototype restores the invariant in the bounded model:

- same-party batch composition is rejected;
- every admitted batch has distinct modeled parties; and
- a valid distinct-party batch remains reachable.

This demonstrates restoration of the intended batch identity semantics. It
does not make the modeled admission check a new algorithm or the unique
possible enforcement mechanism. Batch construction rules or other trusted
components could preserve the same invariant; those alternatives are not
evaluated here.

------------------------------------------------------------------------

# Step 8: Claim Boundary

The strongest supported claim is:

> `DistinctPartyPerBatch` is a necessary identity-level invariant for the
> intended party-level batch semantics of the modeled `BatchReceive` boundary.
> Removing it permits same-batch repeated-party admission, invalid batch
> composition, and duplicate receiver acceptance in the bounded symbolic
> model.

Conditional upper-layer consumption or installation impact requires a
separately stated consumer-composition assumption and is not modeled by the
current prototypes.

The current work does not claim:

- a deployed K-Waay implementation is vulnerable;
- an original theorem has been invalidated;
- duplicate acceptance establishes confidentiality loss;
- arbitrary-size or cross-batch behavior; or
- one mandatory implementation mechanism for preserving the invariant.
