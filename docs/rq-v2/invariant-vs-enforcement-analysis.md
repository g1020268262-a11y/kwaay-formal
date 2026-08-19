# Invariant vs Enforcement Analysis

## Status

Frozen RQ-v2 supporting analysis.

This document analyzes the difference between:

-   the necessity of the `DistinctPartyPerBatch` semantic invariant;
-   one specific enforcement mechanism such as party-admission checking.

The goal is to clarify that the research contribution concerns
preservation of the identity invariant, not proposing one mandatory
implementation method.

------------------------------------------------------------------------

# 1. Research Question

The question is:

> Is `DistinctPartyPerBatch` necessary as a protocol semantic property,
> or is the research only describing one possible admission-check
> mechanism?

The distinction is:

    Invariant

    =

    what must remain true

while:

    Enforcement mechanism

    =

    how an implementation maintains it

------------------------------------------------------------------------

# 2. The Invariant Under Study

`DistinctPartyPerBatch` expresses:

    Within one batch:

    different components correspond to different parties.

Conceptually:

    slot 1:

    Party A → output k_A


    slot 2:

    Party B → output k_B

The important property is not the specific checking code.

The important property is:

    one modeled party

            corresponds to

    one batch component

------------------------------------------------------------------------

# 3. Why Party Admission Is Not the Contribution

The RQ-v2 party-admission prototype implements one possible restoration:

    input batch

          ↓

    check party uniqueness

          ↓

    accept only distinct-party batches

This demonstrates that the invariant can be restored.

However, the research claim is not:

> Every implementation must use party admission.

The research claim is:

> The batch semantics require preservation of party-level uniqueness.

Other mechanisms could theoretically preserve the same invariant.

Examples:

-   construction of batches that never create repeated parties;
-   protocol-level constraints before BatchReceive;
-   trusted batching services enforcing the condition.

The current work does not evaluate these alternatives.

------------------------------------------------------------------------

# 4. Evidence That the Invariant Matters

The current RQ-v2 evidence compares three semantics:

## Relaxed semantics

The party uniqueness condition is removed.

Result:

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate acceptance trace

The relaxed model demonstrates that removing the invariant changes
reachable executions.

------------------------------------------------------------------------

## Message-dedup semantics

Message identity is restricted.

Result:

    same message repetition

    can be rejected

but:

    Party A, Message M1

    Party A, Message M2

remains possible.

Therefore message-level enforcement does not preserve the party identity
invariant.

------------------------------------------------------------------------

## Party-admission semantics

Party identity is checked.

Result:

    same-party batch composition rejected

    valid distinct-party batch remains reachable

This demonstrates restoration of the intended invariant in the
prototype.

------------------------------------------------------------------------

# 5. What Is Necessary and What Is Not Proven

The current evidence supports:

    DistinctPartyPerBatch is a meaningful semantic invariant.

because removing it changes:

-   batch composition semantics;
-   party-output interpretation;
-   reachable acceptance behavior.

The current evidence does not prove:

    Party admission is the only possible solution.

Nor does it prove:

    Every real implementation must contain the same check.

------------------------------------------------------------------------

# 6. Why This Is Different From an Ordinary Input Restriction

An ordinary restriction says:

    invalid input

    ↓

    reject or undefined behavior

The RQ-v2 invariant is different because it defines the interpretation
of protocol objects:

    party identity

            ↓

    batch component

            ↓

    output key

            ↓

    security-model reference

Removing it creates ambiguity in how outputs are attributed to parties.

Therefore the issue is semantic consistency, not only input validation.

------------------------------------------------------------------------

# 7. Research Boundary

This analysis does not claim:

-   a deployed K-Waay implementation fails to enforce the invariant;
-   party admission is the only implementation solution;
-   removal directly breaks the original K-Waay theorem.

The supported claim is:

> `DistinctPartyPerBatch` is a necessary semantic property for
> maintaining the intended party-level interpretation of batch
> components and outputs within the modeled boundary.
