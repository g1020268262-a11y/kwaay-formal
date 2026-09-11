# RQ-v2 Threat Model

## Status

Frozen RQ-v2 **Primary Authority** for the batch-composition adversary and
threat-model boundary.

This document defines the adversary model used to study the necessity of the
`DistinctPartyPerBatch` identity invariant. It does not claim a deployed
K-Waay vulnerability.

------------------------------------------------------------------------

# 1. Security Question

RQ-v2 asks:

> What admission and acceptance consequences arise when
> `DistinctPartyPerBatch` is removed from the modeled `BatchReceive`
> boundary?

The analysis concerns identity-level batch composition, not cryptographic
primitive failure.

------------------------------------------------------------------------

# 2. Attack Surface

The attack surface is the batch admission boundary:

    Batch-composition adversary

            ↓

    Batch input vector

            ↓

    BatchReceive

The security question is whether an invalid identity composition becomes
reachable when the identity invariant is absent.

------------------------------------------------------------------------

# 3. Adversary Capabilities

Within the relaxed symbolic model, the adversary can:

- select or arrange batch entries;
- place entries into different batch slots;
- repeat one valid modeled party coordinate in multiple slots; and
- trigger executions allowed by the relaxed admission semantics.

The relevant composition is:

    slot 1 → Party A
    slot 2 → Party A

The construction does not require impersonating Party A. It uses repeated
admission of the same modeled protocol-principal identity coordinate.

------------------------------------------------------------------------

# 4. Cryptographic Boundary

The attack construction does not require:

- breaking cryptographic assumptions;
- recovering secret keys;
- forgery or modification of authenticated material; or
- exploiting an implementation-specific software bug.

These are threat-model boundaries, not properties proved by the current
prototypes. The prototypes do not model an authentication mechanism, HMAC
computation, signatures, encryption, or keys.

------------------------------------------------------------------------

# 5. Attack Goal and Execution Path

The adversary's modeled goal is to reach a batch execution where one party
coordinate occupies multiple slots and yields multiple accepted occurrences.

The formally supported path is:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

The relaxed prototype contains one `Send` occurrence and two
`ReceiverAccept` occurrences for the same modeled sender identity and receiver
batch context. This is a loss of the intended identity interpretation at the
admission/acceptance boundary, not a demonstrated key or confidentiality
failure.

------------------------------------------------------------------------

# 6. Conceptual Relation to Security Interfaces

The original K-Waay interface interpretation motivates a dependency between a
party coordinate and party-indexed references such as `KEY(i,s,j)` or
`TEST(i,s,j)`. If one party coordinate is expected to select one corresponding
component, repeated-party composition creates ambiguous party-level
attribution unless another selection rule is supplied.

This relation is conceptual. The current prototypes do not directly formalize
`KEY`, `TEST`, output keys, or correctness relations over keys, so they do not
prove key ambiguity or failure of those interfaces.

------------------------------------------------------------------------

# 7. Comparison Mechanisms

HMAC concerns message authenticity, integrity, or confirmation. It does not
establish party uniqueness or batch-admission semantics.

Exact-message deduplication constrains message identity. It can reject an
identical message repetition while still admitting two different messages
with the same party coordinate. It is an auxiliary comparison, not an
enforcement of `DistinctPartyPerBatch`.

------------------------------------------------------------------------

# 8. Evidence Scope

The current RQ-v2 evidence supports:

- reachable repeated-party admission in the relaxed model;
- a reachable duplicate-acceptance witness;
- the distinction between message and party coordinates; and
- restoration of the modeled invariant by the party-admission prototype while
  retaining a reachable valid distinct-party batch.

It does not establish a deployed-system vulnerability, invalidate an original
theorem, make an admission check the unique implementation solution, or prove
unconditional upper-layer impact.

------------------------------------------------------------------------

# 9. Final Threat Model Statement

The RQ-v2 adversary is a batch-composition adversary, not a cryptographic
attacker. The studied threat is the admission of a same-batch repeated-party
composition when the identity invariant is absent, with duplicate receiver
acceptance as the bounded formal consequence.
