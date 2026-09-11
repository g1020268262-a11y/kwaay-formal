# RQ-v2 Paper Contribution Outline

## Status and Authority Boundary

This is a paper-planning document derived from the frozen RQ-v2 authority. It
organizes the contribution for writing but does not redefine the research
question, model semantics, threat model, lemmas, or prototype results.

The central paper claim is scoped to the current symbolic, fixed-two-slot
`BatchReceive` admission models:

> `DistinctPartyPerBatch` is a necessary identity invariant for preserving the
> intended party-level interpretation of an admitted batch in the modeled
> boundary.

## Research Problem

K-Waay's `BatchReceive` semantics require distinct entries in one batch to
correspond to distinct parties. The paper studies the semantic role of this
condition, named `DistinctPartyPerBatch`, by separating party identity from
message identity, session identity, slot identity, and batch identity.

The research problem is whether removing the identity invariant changes the
set of reachable batch compositions and receiver-acceptance behaviors, and
whether restoring party-level admission recovers the intended batch identity
semantics without eliminating valid distinct-party executions.

The frozen consequence chain is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> loss of intended party-level identity interpretation
```

## Motivation

An admission condition can appear to be ordinary input validation while also
carrying protocol-level meaning. In this setting, one admitted batch is
intended to represent a set of distinct modeled protocol principals. If party
identity is replaced by message or session identity, a batch can contain two
different entries from the same party while satisfying a message-level check.

This motivates treating `DistinctPartyPerBatch` as an identity-semantics
invariant rather than as a particular implementation check. The paper therefore
asks what must remain true at the modeled boundary, independently of where or
how an implementation might enforce it.

The original K-Waay party-indexed interface supplies conceptual motivation for
why unique party interpretation matters. The current RQ-v2 prototypes do not
formalize output keys, `KEY`, `TEST`, or correctness relations over keys; that
interface connection remains conceptual rather than direct formal evidence.

## Main Contribution

The main contribution is an evidence-bounded necessity analysis of the
`DistinctPartyPerBatch` identity invariant. The analysis defines a distinct
party coordinate, removes the corresponding admission guard in a relaxed
model, and compares the resulting behavior with message-level and party-level
admission models.

Within the fixed-two-slot symbolic scope, the comparison establishes that:

1. relaxed admission permits one modeled party to occupy two slots in the same
   batch;
2. the relaxed model has a reachable trace in which one `Send` occurrence has
   two `ReceiverAccept` occurrences in the same receiver batch context;
3. exact-message deduplication can reject identical messages while still
   admitting two different messages from the same party; and
4. party-level admission rejects same-party composition, ensures distinct
   modeled parties in admitted batches, and retains a reachable valid
   distinct-party batch.

Together, these results support the scoped conclusion that preserving party
uniqueness is necessary for the intended party-level batch interpretation.
They do not identify one mandatory implementation algorithm.

## Supporting Contributions

### Identity-layer separation

The paper provides an explicit hierarchy in which the modeled party coordinate
is distinct from message, session, prekey, sender-occurrence, slot, receiver
state, and batch coordinates. This prevents message inequality or session
inequality from being used as evidence of party inequality.

### Admission-semantics comparison

The R/M/P comparison isolates the identity coordinate checked at admission:

- R-semantics performs no party- or message-uniqueness check;
- M-semantics checks exact message identity only; and
- P-semantics checks modeled party identity.

This comparison keeps the batch and acceptance structure comparable while
changing the admission condition under study.

### Separation of invariant and enforcement

The analysis distinguishes the invariant that must hold from one modeled
mechanism that restores it. Party-level admission is an executable restoration
model, not a claim that every implementation must use the same check or place
it in the same component.

### Separation from message authentication

HMAC-related historical evidence concerns authenticity, integrity, agreement,
or explicit confirmation. It is not used to derive party uniqueness. The
message-dedup model is retained as an auxiliary non-equivalence comparison, not
as the paper's main contribution.

### Evidence-bounded interface discussion

The paper can use the original party-indexed interface to explain the semantic
dependency between party identity and party-indexed interpretation, while
keeping the direct formal claim at the admission and receiver-acceptance
boundary.

## Formal Evidence

| Evidence role | Model / property | Recorded result | Paper use |
| --- | --- | --- | --- |
| Relaxed execution | `rqv2_relaxed.spthy`: `normal_relaxed_batch_exists` | verified | Non-vacuity of relaxed processing |
| Repeated acceptance witness | `rqv2_relaxed.spthy`: `one_send_two_accepts_exists` | verified | One `Send` occurrence can have two accepts in the scoped relaxed model |
| Relaxed injectivity check | `rqv2_relaxed.spthy`: `receiver_accept_injective` | falsified | Corroborates the duplicate-acceptance witness |
| Exact-message rejection | `rqv2_message_dedup.spthy`: `repeated_message_rejection_exists` | verified | M-semantics rejects an identical-message pair |
| Party/message non-equivalence | `rqv2_message_dedup.spthy`: `same_party_different_messages_batch_exists` | verified | Different messages do not establish distinct parties |
| Party-level safety | `rqv2_party_admission.spthy`: `accepted_batch_has_distinct_parties` | verified | Admitted batches have distinct modeled parties in the two-slot model |
| Same-party rejection | `rqv2_party_admission.spthy`: `same_party_rejection_exists` | verified | The intended rejection branch is reachable |
| Restoration non-vacuity | `rqv2_party_admission.spthy`: `distinct_party_batch_exists` | verified | A valid distinct-party batch remains reachable |

Primary evidence sources:

- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md)
- [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md)
- [`../rq-v2/rq-v2-complete-argument-map.md`](../rq-v2/rq-v2-complete-argument-map.md)
- [`../../artifact/results/rqv2-claim-matrix.tsv`](../../artifact/results/rqv2-claim-matrix.tsv)
- [`../../artifact/rqv2-freeze/freeze-manifest.tsv`](../../artifact/rqv2-freeze/freeze-manifest.tsv)

## Non-Claims

The paper does not establish any of the following:

- a general failure of K-Waay;
- failure of a cryptographic primitive or computational security definition;
- an exploitable condition in a deployed implementation;
- failure of `KEY`, `TEST`, output-key, or key-correctness interfaces;
- unconditional duplicate consumption, installation, session cloning, or
  application-level impact;
- an arbitrary-length, cross-batch, rollback, restart, or concurrent-execution
  theorem;
- compromise-resilient guarantees beyond the stated model;
- exact-message deduplication as an implementation of party uniqueness;
- one uniquely required admission algorithm or enforcement location; or
- occurrence injectivity as the final research contribution.

Any upper-layer impact discussion must remain conditional on an explicit
composition interface such as `C_install-v2` and must not be presented as a
result of the current RQ-v2 prototypes.
