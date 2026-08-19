# Identity Binding Analysis for DistinctPartyPerBatch

## Status

Frozen RQ-v2 supporting analysis.

This document explains the semantic role of the `DistinctPartyPerBatch`
invariant in K-Waay `BatchReceive` semantics.

The goal is not to claim that deployed K-Waay implementations are
vulnerable, but to analyze why the identity-level constraint is
meaningful and what semantic consequences arise when it is removed.

This document does not claim:

-   that `DistinctPartyPerBatch` is the only possible enforcement
    mechanism;
-   that duplicate acceptance alone proves a deployed security failure;
-   that cryptographic primitives such as HMAC or encryption are broken.

------------------------------------------------------------------------

# 1. Research Objective

The central question is:

> Why does K-Waay require entries in one `BatchReceive` execution to
> correspond to distinct parties?

The RQ-v2 analysis identifies `DistinctPartyPerBatch` as an
identity-level invariant that maintains the intended relationship:

    Party Identity

            ↓

    Batch Slot

            ↓

    Output Key

Without this invariant, the receiver may still compute outputs, but the
meaning of those outputs with respect to party identity becomes
ambiguous.

------------------------------------------------------------------------

# 2. Identity Binding Semantics

A batch entry represents a claimed sender party.

Conceptually:

    (pk_j, prek_j, m_j)

            ↓

    party P_j

            ↓

    output key k_j

The intended receiver-session-local relationship is:

    P_j → k_j

This does not represent a permanent global mapping between a party and a
key.

It represents that, within one receiver session, a party coordinate
identifies one corresponding output component.

------------------------------------------------------------------------

# 3. Why DistinctPartyPerBatch Exists

The invariant requires:

    for every i != j:

    party_i != party_j

Therefore a valid batch has:

    slot 1:

    Party A
       |
       v
     k_A


    slot 2:

    Party B
       |
       v
     k_B

Each party corresponds to one batch component.

As a result, party-indexed operations such as:

    KEY(i,s,j)

    TEST(i,s,j)

    correctness checks

have a unique interpretation.

------------------------------------------------------------------------

# 4. Removing the Identity Constraint

After removing `DistinctPartyPerBatch`, a batch may contain:

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

The problem is not necessarily:

    k_1 = k_2

The problem is:

    Party A → {k_1, k_2}

The original one-party-one-component interpretation is lost.

This creates an identity binding failure:

    multiple logical batch positions

            ↓

    same modeled identity

            ↓

    ambiguous component attribution

------------------------------------------------------------------------

# 5. Impact on Security Interfaces

K-Waay security interfaces reference components using party coordinates.

For example:

    KEY(i,s,j)

    TEST(i,s,j)

These interfaces assume that a party identifier selects one unique
output.

However, after repeated-party admission:

    Party A → k_1

    Party A → k_2

the reference:

    KEY(i,s,A)

no longer identifies a unique component.

The same ambiguity affects:

-   key exposure queries;
-   test queries;
-   correctness relationships;
-   partner/output correspondence.

Therefore, `DistinctPartyPerBatch` preserves the uniqueness of
party-indexed output interpretation.

------------------------------------------------------------------------

# 6. Batch Composition Integrity

A batch does not only contain messages.

It also represents a participant structure.

The intended meaning is:

    Batch structure

    =

    actual participant structure

For example:

Expected:

    [
     Party A,
     Party B,
     Party C
    ]

After identity constraint removal:

    [
     Party A,
     Party A,
     Party C
    ]

The batch no longer represents the intended set of contributors.

This is a semantic integrity failure of the batch composition.

------------------------------------------------------------------------

# 7. Duplicate Acceptance Consequence

The relaxed RQ-v2 prototype demonstrates:

    DistinctPartyPerBatch removed

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

The duplicate acceptance trace is an operational consequence of losing
the identity-level invariant.

The deeper issue is that one modeled party identity can correspond to
multiple accepted batch components.

------------------------------------------------------------------------

# 8. Output Attribution Ambiguity

If outputs are later consumed according to their batch component:

    Output1 ← Slot1

    Output2 ← Slot2

the system assumes:

    Output1 belongs to Party A

    Output2 belongs to Party B

However, with repeated-party admission:

    Slot1 = Party A

    Slot2 = Party A

both outputs originate from the same modeled identity.

Therefore, the protocol loses a unique attribution relationship between:

    party identity

            ↓

    output component

------------------------------------------------------------------------

# 9. Comparison with Message Deduplication

Message deduplication constrains message identity.

It can reject:

    Party A, Message M

    Party A, Message M

However, it does not enforce party uniqueness:

    Party A, Message M1

    Party A, Message M2

may still be admitted.

Therefore:

    message uniqueness

    !=

    party identity uniqueness

Message deduplication is an auxiliary comparison mechanism, not a
replacement for identity-level admission.

------------------------------------------------------------------------

# 10. Relation to HMAC

HMAC addresses:

-   message authenticity;
-   message integrity;
-   confirmation.

It does not establish:

-   party uniqueness;
-   batch admission rules;
-   identity-to-slot binding.

Therefore HMAC and `DistinctPartyPerBatch` operate on different semantic
dimensions.

------------------------------------------------------------------------

# 11. Research Contribution

The contribution is not simply that removing a protocol condition allows
invalid executions.

The contribution is:

> `DistinctPartyPerBatch` preserves a unique identity-level
> interpretation between batch components and derived outputs. Removing
> this invariant changes the semantic structure assumed by party-indexed
> security interfaces.

This explains why the condition is meaningful beyond a simple input
restriction.

------------------------------------------------------------------------

# 12. Scope Boundary

This analysis does not determine:

-   where a deployed implementation enforces the invariant;
-   whether existing implementations perform such checking;
-   whether all applications require identical enforcement;
-   arbitrary-size batch behavior beyond the bounded prototype.

These remain future implementation and composition questions.
