# Conclusion

This paper analyzed the semantic role of K-Waay's stated distinct-party
`BatchReceive` condition, which we normalize as `DistinctPartyPerBatch`. The
analysis answers the research question at the modeled admission boundary:
preserving this party-level identity invariant is necessary for preserving the
intended interpretation that distinct slots in one admitted batch represent
distinct modeled protocol-principal coordinates.

The R/M/P-semantics comparison makes that conclusion concrete. Removing party
uniqueness in R-semantics permits repeated-party composition and a reachable
one-Send/two-`ReceiverAccept` behavior. Exact-message deduplication in
M-semantics restores the scoped occurrence-injectivity property while leaving
same-party/different-message admission reachable. Party-level admission in
P-semantics restores the intended distinct-party batch semantics, makes
same-party rejection reachable, and retains a reachable valid distinct-party
batch.

These results separate three relations that should not be conflated: party
identity, message identity, and occurrence injectivity. A one-to-one relation
between a sender occurrence and receiver acceptances can hold even when two
different messages from the same modeled party occupy one batch. The identity
coordinate constrained by an admission rule must therefore match the semantic
relationship that the batch is intended to preserve.

The evidence is limited to symbolic fixed-two-slot admission models and ends
at `ReceiverAccept`; it supports no conclusion about deployment behavior or
cryptographic security. The resulting design obligation is to preserve the
party-level identity invariant at the relevant composition boundary, not to
mandate one uniquely specified enforcement mechanism.
