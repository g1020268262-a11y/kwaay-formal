# Party-Level Attribution Analysis for DistinctPartyPerBatch

## Status

Frozen RQ-v2 **Supporting Analysis**. This document is not primary RQ-v2
authority.

The retained `-final` filename is a legacy document name only. It does not
identify a separate final research version or override the canonical primary
authority documents.

This document explains the semantic role of `DistinctPartyPerBatch` at the
modeled `BatchReceive` boundary and separates that formal result from the
original K-Waay interface interpretation.

The evidence boundary is:

- **Formal evidence:** the relaxed, message-dedup, and party-admission
  prototypes model party coordinates, slots, admission, rejection, `Send`, and
  `ReceiverAccept` events.
- **Conceptual analysis:** the original K-Waay interface motivates how a
  party-indexed interpretation could extend from an accepted component to an
  output object.

The current prototypes do not model output keys, `KEY`, `TEST`, or application
consumers.

------------------------------------------------------------------------

# 1. Research Objective

The central question is:

> Why does K-Waay require entries in one `BatchReceive` execution to
> correspond to distinct parties?

At the formal evidence boundary, `DistinctPartyPerBatch` maintains the
intended relationship:

    Party identity

            ↓

    Batch slot

            ↓

    Accepted occurrence

Removing the invariant permits two slots to carry the same modeled party,
causing ambiguous party-level attribution across those accepted occurrences.

------------------------------------------------------------------------

# 2. Identity Semantics

A batch entry carries a modeled party coordinate. This coordinate is neither a
permanent party-to-key mapping nor an assertion about a deployed identity
representation.

With the invariant:

    slot 1 → Party A → accepted occurrence 1
    slot 2 → Party B → accepted occurrence 2

Without the invariant:

    slot 1 → Party A → accepted occurrence 1
    slot 2 → Party A → accepted occurrence 2

The latter is a loss of the intended party-level interpretation: one modeled
party is attributed to multiple positions in the same batch. It does not by
itself prove equality, ambiguity, exposure, or compromise of derived keys.

------------------------------------------------------------------------

# 3. Why DistinctPartyPerBatch Matters

The invariant requires, for every two distinct slots `i` and `j` in one batch:

    party_i != party_j

It therefore preserves the intended participant structure of that batch. A
batch containing `Party A, Party A, Party C` does not have the same identity
composition as a batch containing `Party A, Party B, Party C`.

This is a semantic property of the batch, not a claim that one particular
party-admission algorithm is mandatory.

------------------------------------------------------------------------

# 4. Duplicate Acceptance Consequence

The relaxed RQ-v2 prototype establishes:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

The witness contains one `Send` occurrence and two `ReceiverAccept`
occurrences for the same modeled sender identity and receiver batch context.
This is direct symbolic evidence of reachable admission and acceptance
behavior; it is not a proof about keys or upper-layer output objects.

------------------------------------------------------------------------

# 5. Conceptual Security-Interface Motivation

The original K-Waay interface interpretation uses party-indexed references
such as `KEY(i,s,j)` and `TEST(i,s,j)`. If a party coordinate is intended to
select one corresponding output component, the distinct-party invariant
provides the semantic basis for that interpretation.

With repeated-party admission, the same party coordinate labels more than one
batch position. Under the conceptual interface interpretation, this creates
ambiguous party-level attribution unless another selection rule is supplied.

The current RQ-v2 prototypes do not directly formalize `KEY`, `TEST`, output
keys, or correctness relations over keys. They therefore do not prove output-
key confusion, failure of the security experiment, or key compromise.

------------------------------------------------------------------------

# 6. Conditional Upper-Layer Impact

If a separate upper layer independently consumes every accepted occurrence,
duplicate receiver acceptance can lead to duplicate consumption or
installation under that explicit composition assumption. The current RQ-v2
prototypes do not model this consumer, so such impact remains conditional.

------------------------------------------------------------------------

# 7. Comparison Mechanisms

Message deduplication constrains message identity. It can reject an exact
message repetition but can still admit two different messages carrying the
same party coordinate. It is an auxiliary comparison and does not enforce
party uniqueness.

HMAC concerns message authenticity, integrity, or confirmation. It does not
establish party uniqueness, batch admission, or identity-to-slot semantics.

------------------------------------------------------------------------

# 8. Research Contribution and Scope

The supported contribution is:

> `DistinctPartyPerBatch` preserves the intended party-level interpretation
> between admitted slots and accepted occurrences. Removing the invariant
> permits invalid repeated-party composition and duplicate acceptance in the
> bounded symbolic model.

The original K-Waay interface motivates why this identity dependency may
matter to party-indexed outputs. That motivation is conceptual and is not a
formal claim about an output-key component.

This analysis does not determine where a deployed implementation enforces the
invariant, whether existing implementations perform such checking, or how the
fixed two-slot result generalizes to arbitrary batch sizes.
