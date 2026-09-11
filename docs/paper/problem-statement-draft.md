# Problem Statement

## 1. Intended Batch Identity Semantics

The intended identity semantics considered in this paper assigns one distinct
modeled party coordinate to each component of one admitted batch. Informally,
each admitted batch component represents a different modeled protocol
principal within that batch execution. This interpretation concerns the
relationship among batch slots, not global participation: the same party may
have multiple sessions, produce multiple messages, and participate in other
batches.

The semantic object of interest is therefore the admitted batch composition.
Message, session, slot, batch, and receiver-state coordinates remain available
to distinguish other relations, but none substitutes for the party coordinate
in this interpretation.

## 2. Identity Invariant

Let a batch be

```text
B = [E1, E2, ..., En].
```

We define `DistinctPartyPerBatch(B)` by

```text
for all i != j,
    party(E_i) != party(E_j).
```

This definition states the intended invariant in general form. The current
Tamarin prototypes instantiate only `n = 2`; accordingly, the verified results
are fixed-two-slot results and do not constitute a proof for arbitrary `n`.
Within that bounded admission model, preserving
`DistinctPartyPerBatch` is necessary for preserving the intended party-level
batch identity semantics.

## 3. Relaxation

R-semantics defines the relaxed comparison by removing the party-level
restriction from the admission decision. For two collected entries, admission
does not require

```text
A1 != A2.
```

The immediate question is then compositional: can the same modeled party
coordinate occupy both slots of one admitted batch? This relaxation defines
the behavior to be examined. Reachability of its receiver-acceptance
consequences is addressed separately by the formal analysis.

## 4. Message-Level Alternative

M-semantics introduces a message-level restriction instead. For the two-slot
prototype, its admitted branch requires

```text
m1 != m2,
```

but does not require `A1 != A2`. These are predicates over different
coordinates, and the assignment

```text
A1 = A2  and  m1 != m2
```

is logically consistent. Exact-message deduplication can therefore enforce a
message-level distinction without establishing the party-level invariant.
P-semantics, by contrast, applies the comparison to `A1` and `A2` and is the
modeled restoration of the intended admission semantics.

## 5. Research Questions

The comparison is organized around three research questions:

**RQ1.** What batch compositions become reachable when
`DistinctPartyPerBatch` is removed?

**RQ2.** Can removal of the invariant produce duplicate receiver acceptance
within the bounded model?

**RQ3.** Can a message-level restriction substitute for party-level
uniqueness, or is explicit party-level admission required to restore the
intended semantics in the modeled comparison?

In RQ3, party-level admission denotes P-semantics, the executable restoration
used in the current model. It is not a claim that every implementation must use
one particular check, algorithm, or enforcement location.

## 6. Scope of Necessity

In this paper, “necessary” has a specific semantic scope:
`DistinctPartyPerBatch` is necessary for preserving the intended party-level
batch identity semantics within the modeled admission boundary. The necessity
claim follows the R/P comparison: removing the party restriction permits the
prohibited composition, while the modeled party-level admission restores the
invariant and retains a reachable valid batch.

This use of necessity is neither a claim about K-Waay security in general nor a
claim about secrecy, authentication, IND-CCA security, or other cryptographic
properties. It also does not establish that P-semantics is the only possible
implementation mechanism. The formal evidence remains bounded to one symbolic
fixed-two-slot batch and its receiver-acceptance lifecycle.

