# Security Interface Dependency Analysis

## Status

Frozen RQ-v2 supporting analysis.

This document analyzes how the K-Waay security model's party-indexed
interfaces depend on the identity uniqueness provided by
`DistinctPartyPerBatch`.

The purpose is not to claim that removing the invariant directly breaks
the original K-Waay theorem. The purpose is to show that the invariant
preserves the unambiguous interpretation of security-model objects.

------------------------------------------------------------------------

# 1. Research Question

The question is:

> Does `DistinctPartyPerBatch` provide semantic support for the
> party-indexed security interfaces used by K-Waay?

The relevant relationship is:

    Party identity

            ↓

    Batch component

            ↓

    Output key

            ↓

    Security query reference

The invariant ensures that this relationship remains uniquely
interpretable.

------------------------------------------------------------------------

# 2. Output Model Background

A batch component is associated with a modeled party.

Conceptually:

    (pk_j, prek_j, m_j)

            ↓

    Party P_j

            ↓

    key k_j

The receiver stores outputs as party-indexed components.

The security model then refers to these components through party
indexes.

Therefore, the identity of the party is not only metadata. It is part of
the meaning of the output component.

------------------------------------------------------------------------

# 3. KEY Interface Dependency

The security model contains party-indexed key access.

Conceptually:

    KEY(i,s,j)

means:

    return the key component associated with party j

Under `DistinctPartyPerBatch`:

    slot 1:

    Party A → k_A

    slot 2:

    Party B → k_B

The query has a unique target.

After removing the invariant:

    slot 1:

    Party A → k_1

    slot 2:

    Party A → k_2

The reference:

    KEY(i,s,A)

no longer identifies one unique output component.

The issue is not necessarily that the two keys are equal.

The issue is that one identity corresponds to multiple possible
components.

------------------------------------------------------------------------

# 4. TEST Interface Dependency

The security experiment uses party-indexed testing.

Conceptually:

    TEST(i,s,j)

selects the key associated with party j and replaces it with a random
value for the security challenge.

This requires:

    party j

            ↓

    one unique key component

Without the invariant:

    Party A → k_1
    Party A → k_2

the meaning of:

    TEST(i,s,A)

becomes ambiguous.

The experiment cannot uniquely identify which component is being tested.

This demonstrates that `DistinctPartyPerBatch` supports the semantic
well-definedness of the testing interface.

------------------------------------------------------------------------

# 5. Correctness Relationship Dependency

Correctness compares matching outputs between protocol participants.

The intended relationship is:

    sender party

            ↓

    corresponding receiver component

            ↓

    same derived key

With unique parties:

    Party A

            ↓

    one receiver component

            ↓

    one matching key

After repeated-party admission:

    Party A

            ↓

    multiple receiver components

The correspondence between sender identity and receiver output becomes
ambiguous.

The problem is not that the cryptographic computation necessarily fails.

The problem is that the identity-based matching relation loses
uniqueness.

------------------------------------------------------------------------

# 6. Connection With RQ-v2 Prototype Trace

The relaxed prototype demonstrates:

    Remove DistinctPartyPerBatch

            ↓

    same-party repeated admission

            ↓

    invalid batch composition

            ↓

    two receiver accept events

The trace shows:

    One Send occurrence

            +

    Two ReceiverAccept occurrences

for the same modeled sender identity and receiver batch state.

This provides evidence that removing the identity constraint can create
multiple accepted components associated with the same identity.

------------------------------------------------------------------------

# 7. Message Deduplication Comparison

Message deduplication operates on a different coordinate.

It checks:

    (message identity)

not:

    (party identity)

Therefore:

Message deduplication can prevent:

    Party A, Message M

    Party A, Message M

but does not prevent:

    Party A, Message M1

    Party A, Message M2

The security-interface ambiguity remains.

------------------------------------------------------------------------

# 8. HMAC Separation

HMAC provides:

-   authenticity;
-   integrity;
-   confirmation.

It does not provide:

-   party uniqueness;
-   batch admission;
-   identity-to-output binding.

Therefore HMAC does not resolve the dependency discussed here.

------------------------------------------------------------------------

# 9. Evidence Boundary

Supported by current evidence:

-   K-Waay outputs are interpreted through party-indexed components.
-   KEY, TEST, and correctness reasoning rely on unique party-component
    association.
-   Removing `DistinctPartyPerBatch` creates repeated-party batch
    compositions in the relaxed model.
-   The relaxed prototype contains duplicate acceptance traces.

Not claimed:

-   the original K-Waay theorem is false;
-   deployed implementations are vulnerable;
-   the invariant is the only possible implementation solution.

------------------------------------------------------------------------

# 10. Conclusion

`DistinctPartyPerBatch` is not merely an input-format restriction.

It maintains the semantic uniqueness required for interpreting:

    party identity

            ↓

    batch component

            ↓

    output key

            ↓

    security-model reference

The RQ-v2 analysis shows that removing this invariant changes the
meaning of party-indexed protocol objects and enables duplicate
acceptance behavior in the relaxed symbolic model.
