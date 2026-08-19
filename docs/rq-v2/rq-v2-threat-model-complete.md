# RQ-v2 Threat Model

## Status

Frozen RQ-v2 supporting analysis.

This document defines the adversary model for studying the necessity of
the `DistinctPartyPerBatch` identity invariant.

The goal is not to claim a deployed K-Waay vulnerability. The goal is to
define the symbolic adversarial behavior required to analyze what
happens when the identity-level batch constraint is removed.

------------------------------------------------------------------------

# 1. Security Question

RQ-v2 studies the following question:

> What consequences arise when `DistinctPartyPerBatch` is removed from
> the `BatchReceive` admission semantics?

The studied property is:

    one modeled party

            corresponds to

    one batch component

The analysis focuses on identity-level batch composition, not on
breaking cryptographic primitives.

------------------------------------------------------------------------

# 2. Attack Surface

The attack surface is the batch admission boundary.

The attacker does not attack:

-   encryption;
-   authentication primitives;
-   HMAC computation;
-   signature verification.

Instead, the attacker influences the construction or admission of batch
entries before or during `BatchReceive`.

The relevant interface is:

    Adversary

        |
        v

    Batch input vector

        |
        v

    BatchReceive

The security question is whether invalid identity composition can enter
the receiver state when the identity invariant is removed.

------------------------------------------------------------------------

# 3. Adversary Capabilities

Within the relaxed symbolic model, the adversary can influence batch
composition.

The adversary can:

-   select or arrange batch entries;
-   place entries into different batch slots;
-   reuse an existing modeled party identity in multiple slots;
-   trigger executions allowed by the relaxed admission semantics.

The key adversarial action is:

    slot 1:

    Party A


    slot 2:

    Party A

The attacker is not required to impersonate Party A.

The attack uses repeated use of a valid modeled identity.

------------------------------------------------------------------------

# 4. Adversary Limitations

The adversary cannot:

-   break cryptographic assumptions;
-   forge authentication material;
-   recover secret keys;
-   modify authenticated messages;
-   exploit implementation-specific software bugs.

The model does not represent a cryptographic primitive failure.

It represents a semantic failure caused by removing an identity-level
constraint.

------------------------------------------------------------------------

# 5. Attack Goal

The attacker goal is:

> Create a batch execution where one modeled party identity corresponds
> to multiple accepted batch components.

The target condition is:

    one party identity

            ↓

    multiple accepted components

This differs from a normal multi-party batch:

    Party A → component 1

    Party B → component 2

The attack requires:

    Party A → component 1

    Party A → component 2

------------------------------------------------------------------------

# 6. Attack Execution Path

The RQ-v2 attack path is:

    Remove DistinctPartyPerBatch

            ↓

    same-batch repeated-party admission

            ↓

    invalid batch composition

            ↓

    duplicate receiver acceptance

            ↓

    identity binding failure

The relaxed prototype provides the corresponding symbolic evidence.

The trace contains:

    one Send occurrence

            +

    two ReceiverAccept occurrences

for the same modeled sender identity and receiver batch context.

------------------------------------------------------------------------

# 7. Security Meaning of the Attack

The primary issue is not simply that two accept events exist.

The deeper issue is:

    one identity

            ↓

    multiple accepted outputs

This affects:

-   party-output attribution;
-   batch participant interpretation;
-   party-indexed security references.

The consequence is loss of unique identity interpretation.

------------------------------------------------------------------------

# 8. Relation to Security Interfaces

K-Waay security reasoning uses party-indexed references.

Conceptually:

    KEY(i,s,j)

    TEST(i,s,j)

These references assume that party identity identifies one corresponding
component.

After repeated-party admission:

    Party A → k1

    Party A → k2

the same identity no longer selects one unique component.

Therefore, the invariant supports the semantic well-definedness of
party-indexed security objects.

------------------------------------------------------------------------

# 9. Comparison With Existing Mechanisms

Different mechanisms protect different coordinates.

## HMAC

Protects:

    message authenticity
    message integrity
    confirmation

It does not provide:

    party uniqueness
    batch admission semantics
    identity-to-slot binding

## Message Deduplication

Protects:

    message identity

It can reject:

    Party A, Message M

    Party A, Message M

but does not reject:

    Party A, Message M1

    Party A, Message M2

Therefore:

    message uniqueness

    !=

    party identity uniqueness

------------------------------------------------------------------------

# 10. Evidence Scope

The current evidence supports:

-   removing `DistinctPartyPerBatch` changes reachable batch executions;
-   repeated-party admission exists in the relaxed model;
-   duplicate acceptance traces are reachable;
-   party admission restores the modeled identity constraint;
-   message-level mechanisms do not replace party-level uniqueness.

The current evidence does not claim:

-   every deployed K-Waay implementation is vulnerable;
-   the original K-Waay theorem is invalid;
-   party admission is the only possible implementation solution.

------------------------------------------------------------------------

# 11. Final Threat Model Statement

The RQ-v2 adversary is a batch-composition adversary.

The adversary does not break cryptography.

The adversary exploits the absence of an identity-level invariant:

    DistinctPartyPerBatch removed

            ↓

    repeated-party batch composition

            ↓

    identity binding failure

            ↓

    duplicate acceptance consequence

The threat studied is therefore an identity-semantics threat at the
batch admission boundary.
