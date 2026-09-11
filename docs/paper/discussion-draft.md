# Discussion

## 1. Why This Is More Than Input Validation

`DistinctPartyPerBatch` appears operationally as a condition on which entries
may pass admission. Its semantic role, however, is to preserve how the batch is
interpreted: distinct accepted slots are intended to correspond to distinct
modeled parties. Removing the condition therefore changes not only the set of
syntactically admissible vectors but also the participant structure attributed
to one admitted batch.

This distinction separates syntactic validity from a semantic identity
invariant. An entry can be individually well formed and have a matching sender
origin while still form part of an invalid same-batch identity composition.
The analysis does not infer that absence of the invariant necessarily causes a
cryptographic property to fail; its supported conclusion concerns the intended
party-level batch identity semantics within the modeled admission boundary.

## 2. Invariant vs Enforcement

The contribution concerns the necessity of preserving
`DistinctPartyPerBatch` for the intended party-level batch identity semantics
within the modeled admission boundary. P-semantics realizes that invariant by
comparing `A1` and `A2` at admission. This party check is one modeled
enforcement and restoration mechanism, rather than the research contribution
itself.

In a general system design, the same invariant might be maintained by a caller,
a batch builder, or a receiver admission layer. These are possible placement
choices, not findings about a deployed K-Waay implementation. The present
evidence neither identifies an existing enforcement location nor establishes
that one algorithm or component is uniquely required.

## 3. Message Deduplication Is a Different Dimension

The M-semantics result exposes an important distinction. Its
`receiver_accept_injective` lemma is verified, so exact-message admission is
sufficient to restore the scoped occurrence property checked by that lemma:
one matching `Send(A,sid,m)` does not yield two distinct accept occurrences in
the same modeled batch context.

Nevertheless, `same_party_different_messages_batch_exists` is also verified.
Two legitimate sender occurrences can carry the same party coordinate and
different message and session coordinates, after which both entries are
accepted in one batch. M-semantics therefore restores scoped occurrence
injectivity without restoring party-level batch uniqueness. In short,
occurrence injectivity is not party uniqueness; success on the former cannot be
used as evidence for the latter.

## 4. Authentication / HMAC Is Orthogonal

The historical HMAC line concerns authentication, integrity, agreement, or
confirmation relations. Those properties can be relevant to the provenance
and integrity of a message, but they do not establish that different slots in
one batch carry different party coordinates. HMAC is not replay prevention by
itself, and a historical HMAC result is not an alternative restoration of
`DistinctPartyPerBatch`.

Accordingly, no HMAC result is used as current RQ-v2 formal evidence. The R/M/P
comparison isolates admission predicates, while HMAC remains orthogonal
historical context.

## 5. Party-Indexed Interface Motivation

The original K-Waay party-indexed interface provides conceptual motivation for
why a unique party interpretation has semantic value. If a party coordinate is
used to identify a corresponding component, repeated-party composition makes
that party-level attribution non-unique unless an additional selection rule is
provided. This is a semantic dependency and an interface interpretation, not a
formally verified output-key consequence.

The current RQ-v2 prototypes do not formalize `KEY`, `TEST`, output-key
objects, or key-correctness relations. They therefore do not establish a
failure of either interface or a key-level correctness result. The interface
discussion remains conceptual motivation beyond the direct
admission/acceptance evidence.

## 6. Conditional Upper-Layer Impact

Direct RQ-v2 formal evidence ends at `ReceiverAccept`. The current prototypes
contain no consumer that installs or otherwise processes each accepted output,
so duplicate acceptance alone does not establish an upper-layer action.

Historical `C_install-v2` composition evidence illustrates a conditional
extension: if a modeled upper-layer consumer independently consumes every
`ReceiverAccept` output, duplicate acceptance can propagate to duplicate
symbolic installations. That implication is conditional on the modeled
consumer assumption and is not a result of the current RQ-v2 prototypes.

## 7. Design Implication

The conservative design implication is that an integration layer whose batch
semantics depend on a distinct-party interpretation must preserve the intended
party-level invariant. The invariant can be maintained before construction,
during batch building, or at receiver admission, provided the resulting
admitted batch satisfies the required party relationship.

This implication specifies the semantic obligation rather than a unique
enforcement location. It does not assert that a public K-Waay implementation
omits such a condition or prescribe one engineering realization.

