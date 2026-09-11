# Security Interface Dependency Analysis

## Status

Frozen RQ-v2 **Supporting Analysis**: conceptual security-interface
motivation. This document is not primary RQ-v2 authority.

This document explains why the original K-Waay security interface motivates a
dependency on party-indexed interpretation. It does not extend the formal
claims of the current RQ-v2 prototypes.

The evidence boundary is explicit:

- **Formal evidence:** `rqv2_relaxed.spthy`, `rqv2_message_dedup.spthy`, and
  `rqv2_party_admission.spthy` establish admission and acceptance results at the
  modeled `BatchReceive` boundary.
- **Conceptual analysis:** the original K-Waay interface interpretation
  motivates why party uniqueness matters to party-indexed objects.

The current RQ-v2 prototypes do not directly formalize output keys, `KEY`,
`TEST`, correctness queries over keys, or application-consumer objects.

------------------------------------------------------------------------

# 1. Research Question

The question is:

> Does `DistinctPartyPerBatch` provide the semantic basis for the intended
> party-indexed interpretation of one batch?

At the formally modeled boundary, the relevant relationship is:

    Party identity

            ↓

    Batch slot

            ↓

    ReceiverAccept occurrence

The original K-Waay interface supplies a further conceptual motivation for
relating a party coordinate to an output or security-query reference. That
further relationship is not encoded in the current prototypes.

------------------------------------------------------------------------

# 2. Modeled Identity Semantics

A batch entry carries a modeled party coordinate. Within one batch,
`DistinctPartyPerBatch` requires different slots to carry different party
coordinates.

With the invariant:

    slot 1 → Party A
    slot 2 → Party B

Without the invariant:

    slot 1 → Party A
    slot 2 → Party A

The second composition loses the intended one-party-per-slot interpretation.
This statement concerns batch identity semantics; it does not assert anything
about the equality, secrecy, or compromise of derived keys.

------------------------------------------------------------------------

# 3. Conceptual KEY and TEST Dependency

Under the original interface interpretation, expressions such as
`KEY(i,s,j)` and `TEST(i,s,j)` use a party coordinate to select a corresponding
object. If one party coordinate is intended to denote one component in a
batch, then `DistinctPartyPerBatch` supplies the semantic basis for that
interpretation.

After repeated-party admission, two slots can carry the same modeled party.
Under that conceptual interface interpretation, party-level attribution is no
longer unique without an additional selection rule.

This is an interface-level motivation, not a Tamarin result. The current
prototypes contain neither `KEY`/`TEST` operations nor output-key objects, and
therefore do not prove key ambiguity, output-key confusion, or a failure of a
security experiment.

------------------------------------------------------------------------

# 4. Connection With the RQ-v2 Prototype Trace

The relaxed prototype establishes the bounded chain:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

The witness contains one `Send` occurrence and two `ReceiverAccept`
occurrences for the same modeled sender identity and receiver batch context.
This is the end of the direct formal evidence. The trace does not contain an
output key, a `KEY`/`TEST` query, or an upper-layer consumer.

------------------------------------------------------------------------

# 5. Message Deduplication and HMAC Separation

Message deduplication constrains message identity, not party identity. It can
reject the same party with the same message while still admitting the same
party with two different messages. It is therefore an auxiliary comparison,
not an enforcement of `DistinctPartyPerBatch`.

HMAC concerns message authenticity, integrity, or confirmation. It does not
establish party uniqueness or same-batch admission semantics. No HMAC claim is
used to derive the RQ-v2 identity result.

------------------------------------------------------------------------

# 6. Evidence Boundary

Formally supported by the current RQ-v2 prototypes:

- removing `DistinctPartyPerBatch` permits repeated-party batch composition;
- the relaxed prototype has a duplicate-acceptance witness;
- exact-message deduplication does not enforce party uniqueness; and
- the party-admission prototype restores the modeled invariant while retaining
  a reachable distinct-party batch.

Conceptually motivated by the original K-Waay interface interpretation:

- party-indexed output and query references depend on an intended
  party-to-component interpretation.

Not established by the current prototypes:

- a failure of `KEY`, `TEST`, correctness, or output-key semantics;
- key compromise, confidentiality failure, or a deployed-system break; or
- a claim that one admission algorithm is the unique enforcement mechanism.

------------------------------------------------------------------------

# 7. Conclusion

`DistinctPartyPerBatch` provides the semantic basis for the intended
party-indexed interpretation of one batch. The current formal evidence shows
what happens at the admission and acceptance boundary when that invariant is
removed. The original K-Waay security interface motivates why the identity
dependency may matter beyond that boundary, while the current RQ-v2 prototypes
do not directly formalize `KEY`, `TEST`, output keys, or their consumers.
