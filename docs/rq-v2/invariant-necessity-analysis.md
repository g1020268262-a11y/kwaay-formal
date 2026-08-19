# DistinctPartyPerBatch Invariant Necessity Analysis

## Status

Frozen RQ-v2 supporting analysis.

This document analyzes why `DistinctPartyPerBatch` should be understood
as a protocol semantic invariant rather than a simple input
precondition.

This analysis is based on the current RQ-v2 semantic documents and
prototype results. It does not claim that a deployed K-Waay
implementation is vulnerable.

------------------------------------------------------------------------

# 1. Research Question

Why is the `DistinctPartyPerBatch` requirement necessary, and why is it
more than an ordinary input restriction?

The analysis studies whether this condition preserves a meaningful
semantic relationship inside `BatchReceive`.

The target relationship is:

    Party Identity

            ↓

    Batch Component

            ↓

    Output Key / Security Reference

------------------------------------------------------------------------

# 2. Ordinary Preconditions vs Semantic Invariants

A normal input precondition only defines which inputs are accepted.

Example:

    input length < N

Violating it means the input is outside the expected range.

However, `DistinctPartyPerBatch` affects how protocol objects are
interpreted.

It defines that:

    one party identity

            corresponds to

    one batch component

inside one batch execution.

Therefore, it is not only filtering invalid input. It maintains the
internal meaning of batch components.

------------------------------------------------------------------------

# 3. What the Invariant Protects

The intended batch semantics are:

    slot 1:

    Party A
       |
       v
    output k_A


    slot 2:

    Party B
       |
       v
    output k_B

Each component has a unique party attribution.

The receiver can interpret each component as belonging to one specific
party.

This matches the party-indexed security interfaces used by the protocol
model.

------------------------------------------------------------------------

# 4. Removing the Invariant

Without `DistinctPartyPerBatch`, the relaxed semantics allow:

    slot 1:

    Party A
       |
       v
    k_1


    slot 2:

    Party A
       |
       v
    k_2

The issue is not necessarily that:

    k_1 = k_2

The issue is:

    Party A -> multiple output components

The party-to-output interpretation is no longer unique.

------------------------------------------------------------------------

# 5. Identity Binding Failure

The removed invariant causes:

    Multiple batch positions

            ↓

    Same party identity

            ↓

    Ambiguous output attribution

This is an identity binding failure.

The failure occurs because:

-   the batch structure no longer represents distinct contributors;
-   output ownership cannot be uniquely interpreted;
-   party-indexed references lose a unique target.

------------------------------------------------------------------------

# 6. Connection to Security Interfaces

Party-indexed references such as:

    KEY(i,s,j)

    TEST(i,s,j)

assume that party `j` identifies one component.

With repeated-party admission:

    Party A -> k_1
    Party A -> k_2

the party identifier no longer selects one unique output.

This demonstrates why the invariant is connected to protocol semantics.

------------------------------------------------------------------------

# 7. Relation to Duplicate Acceptance

The RQ-v2 relaxed prototype demonstrates:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

Duplicate acceptance is a consequence of losing the identity-level
invariant.

The deeper issue is:

    one identity

            ↓

    multiple accepted components

------------------------------------------------------------------------

# 8. Message Deduplication Comparison

Message deduplication checks message identity.

It can reject:

    Party A, Message M

    Party A, Message M

but does not enforce party uniqueness:

    Party A, Message M1

    Party A, Message M2

Therefore:

    message uniqueness != party identity uniqueness

------------------------------------------------------------------------

# 9. HMAC Separation

HMAC addresses:

-   message integrity;
-   authenticity;
-   confirmation.

It does not establish:

-   party uniqueness;
-   batch admission semantics;
-   identity-to-slot binding.

Therefore HMAC cannot replace `DistinctPartyPerBatch`.

------------------------------------------------------------------------

# 10. Evidence Boundary

Current evidence supports:

-   removing the invariant changes batch admission semantics;
-   repeated-party admission is reachable in the relaxed model;
-   duplicate acceptance traces exist;
-   party admission restores the modeled identity constraint.

Current evidence does not claim:

-   deployed K-Waay implementations are affected;
-   this invariant is the only possible implementation solution;
-   confidentiality or key secrecy are directly broken.

------------------------------------------------------------------------

# 11. Final Research Position

`DistinctPartyPerBatch` is a protocol identity invariant that preserves
the unique interpretation between party identity, batch components, and
derived outputs.

Removing this invariant does not merely allow an invalid input. It
changes the semantic structure assumed by party-indexed protocol
reasoning and can lead to identity ambiguity and duplicate acceptance
consequences.
