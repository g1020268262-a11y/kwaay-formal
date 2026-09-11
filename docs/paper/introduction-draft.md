# Introduction

## Paragraph 1: Background

Batch processing in security protocols is commonly motivated by efficiency,
but it also determines how multiple inputs are related within a single
protocol execution. When several entries are processed together, the batch
structure assigns positions to those entries and thereby induces an
interpretation of which participants contribute to that execution. A batch
condition can therefore carry semantic meaning beyond input syntax: it can
define the identity structure that the protocol expects the batch to preserve.

## Paragraph 2: Problem

This paper studies `DistinctPartyPerBatch`, the condition that distinct slots
of one admitted `BatchReceive` batch carry distinct modeled party identities.
We treat this condition as an identity-level invariant rather than as ordinary
input filtering. In particular, party identity is a separate coordinate from
message identity, session identity, and slot identity. One party may produce
multiple messages or participate through multiple sessions, while two slots in
the same admitted batch are still required to represent distinct parties.
Consequently, message inequality, session inequality, or slot inequality does
not by itself establish party inequality.

## Paragraph 3: Research Gap

Replay controls, message deduplication, and authentication mechanisms primarily
constrain message reuse, message equality, origin, integrity, agreement, or
confirmation. These dimensions are important, but their guarantees do not by
themselves imply same-batch party uniqueness. Exact-message deduplication, for
example, can distinguish two messages while leaving open whether both messages
belong to the same party. The resulting gap is not that such mechanisms fail at
their stated goals; rather, message/authenticity properties and party-level
batch identity are different formal dimensions.

## Paragraph 4: Research Question

We ask whether removing `DistinctPartyPerBatch` from the modeled
`BatchReceive` admission boundary permits a composition in which the same
modeled party occupies multiple slots of one batch, and whether that change
affects the intended party-level interpretation of the batch. The question is
scoped to admission and receiver-acceptance behavior: which compositions become
reachable without the invariant, and which party-level semantics are recovered
when the invariant is restored?

## Paragraph 5: Approach

We compare three symbolic admission models over a common fixed-two-slot batch
structure. R-semantics removes party uniqueness and admits a collected pair
without comparing party or message coordinates. M-semantics performs
exact-message deduplication, rejecting equal messages while permitting distinct
messages independently of party equality. P-semantics performs party-level
admission, rejecting a pair with equal modeled party coordinates and admitting
a party-distinct pair. This R/M/P design isolates the checked identity
coordinate while retaining comparable sender, batch, receiver-state, slot, and
acceptance structure.

## Paragraph 6: Results

The recorded prototype results show three complementary behaviors. In the
relaxed model, `one_send_two_accepts_exists` is verified: a reachable trace has
one `Send(A,sid,m)` occurrence and two
`ReceiverAccept(A,sid,m,bid,rst)` occurrences in the same batch context, while
the corresponding scoped injectivity lemma is falsified. In the message-dedup
model, exact-message repetition is rejectable, yet
`same_party_different_messages_batch_exists` is verified, so two different
messages from the same modeled party remain admissible. In the party-admission
model, same-party rejection is reachable,
`accepted_batch_has_distinct_parties` is verified, and
`distinct_party_batch_exists` confirms that a valid distinct-party batch
remains reachable.

## Paragraph 7: Contributions

This paper makes three contributions within a **bounded symbolic
fixed-two-slot model**:

1. It formulates `DistinctPartyPerBatch` as a party-level identity invariant
   and separates party identity from message, session, and slot identity.
2. It gives a bounded formal consequence analysis showing that invariant
   removal permits repeated-party composition and a reachable one-Send/two-
   accept trace at the modeled receiver boundary.
3. It establishes a comparative result: exact-message deduplication does not
   enforce party uniqueness, whereas party-level admission restores the
   intended distinct-party batch semantics while preserving a reachable valid
   batch.

These contributions are limited to the frozen admission prototypes and their
recorded properties. They do not establish implementation behavior,
primitive-level insecurity, output-key properties, or upper-layer consumption
and installation effects.
