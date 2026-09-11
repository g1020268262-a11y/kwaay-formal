# DistinctPartyPerBatch Invariant Necessity Analysis

## Status

Frozen RQ-v2 **Supporting Analysis**: conceptual motivation analysis.

This document uses the original K-Waay security interface to motivate and
explain a semantic dependency between party identity and party-indexed
interpretation. It is not formal evidence from the current RQ-v2 prototypes.

The current RQ-v2 prototypes do not formalize `KEY` queries, do not formalize
`TEST` queries, do not contain output-key objects, and do not prove a
correctness failure. Their direct formal evidence ends at admission,
rejection, and receiver-acceptance behavior.

This document analyzes why `DistinctPartyPerBatch` should be understood
as a protocol semantic invariant rather than a simple input
precondition.

This conceptual analysis is informed by the current RQ-v2 semantic documents
and prototype results. It does not extend those results or claim that a
deployed K-Waay implementation is vulnerable.

------------------------------------------------------------------------

# 1. Research Question

Why is the `DistinctPartyPerBatch` requirement necessary, and why is it
more than an ordinary input restriction?

The analysis studies whether this condition preserves a meaningful
semantic relationship inside `BatchReceive`.

The conceptually motivated relationship is:

    Party Identity

            ↓

    Batch Component

            ↓

    Conceptual Output-Key / Security-Reference Interpretation

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

Under the original interface interpretation, the intended batch semantics can
be conceptualized as:

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

Each component has a unique party attribution at the modeled boundary.

The receiver can interpret each accepted component as belonging to one
specific party.

The original K-Waay security interface motivates extending this interpretation
to party-indexed objects. That extension is conceptual and is not encoded in
the current prototypes.

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

The conceptual interface question is:

    Party A -> multiple conceptually indexed output components

Under that conceptual interface interpretation, the party-to-output relation
would no longer be unique unless another selection rule were supplied. The
current prototypes do not contain these output components.

------------------------------------------------------------------------

# 5. Conceptual Identity-Binding Motivation

The original interface interpretation motivates the following dependency:

    Multiple batch positions

            ↓

    Same party identity

            ↓

    Potentially non-unique conceptual output attribution

This explains a conceptual identity-binding dependency. It is not a formally
proved output-key or security-interface failure.

The conceptual concern arises because:

-   the modeled batch structure no longer represents distinct contributors;
-   a conceptual output-ownership interpretation would require an additional
    selection rule; and
-   party-indexed references would require a clarified target interpretation.

------------------------------------------------------------------------

# 6. Connection to Security Interfaces

The original K-Waay interface contains party-indexed references such as:

    KEY(i,s,j)

    TEST(i,s,j)

Under a conceptual reading, party `j` may be intended to identify one
corresponding component.

With repeated-party admission:

    Party A -> k_1
    Party A -> k_2

the party identifier would not select one unique output without an additional
selection rule.

This motivates and explains why the invariant is connected to party-indexed
protocol semantics. It does not prove `KEY` failure, `TEST` failure, output-key
ambiguity, or correctness failure.

------------------------------------------------------------------------

# 7. Relation to Duplicate Acceptance

The RQ-v2 relaxed prototype formally records:

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
-   confidentiality or key secrecy are directly broken;
-   `KEY` or `TEST` queries fail;
-   output-key objects are ambiguous; or
-   a correctness relation over keys fails.

------------------------------------------------------------------------

# 11. Final Research Position

`DistinctPartyPerBatch` is a protocol identity invariant that preserves the
intended relationship between party identity and batch components. The
original K-Waay interface conceptually motivates why that relationship may
matter to party-indexed derived outputs.

Removing this invariant does not merely allow an invalid input. It changes the
modeled batch identity structure and permits duplicate acceptance. Any further
interpretation involving party-indexed outputs is conceptual motivation, not a
formal claim of the current RQ-v2 prototypes.
