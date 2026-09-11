# Abstract

Batch processing can impose semantic relationships among multiple protocol
inputs rather than merely improve efficiency. K-Waay's `BatchReceive`
description states that different elements in one call correspond to different
parties. We refer to this stated condition as `DistinctPartyPerBatch` and study
its semantic necessity. We construct three fixed-two-slot symbolic Tamarin
admission models: R-semantics removes party uniqueness, M-semantics applies
exact-message deduplication, and P-semantics applies party-level admission. In
all three cases, a common sender-origin and sequential receiver-acceptance
lifecycle supports controlled comparison. In
R-semantics, `one_send_two_accepts_exists` is verified and
`receiver_accept_injective` is falsified, exhibiting a reachable trace in
which one sender occurrence supports two receiver-acceptance occurrences. In
M-semantics, `receiver_accept_injective` is verified, but
`same_party_different_messages_batch_exists` is also verified: distinct
messages from one modeled party can still occupy the batch. In P-semantics,
`accepted_batch_has_distinct_parties`, `same_party_rejection_exists`, and
`distinct_party_batch_exists` are verified, establishing party-distinct
admission, reachable rejection of a same-party pair, and non-vacuous valid
batch behavior. The comparison shows that message-level occurrence properties
and party-level uniqueness are distinct dimensions. Within the modeled
fixed-two-slot admission boundary, the analysis supports the necessity of
`DistinctPartyPerBatch` for preserving the intended party-level batch identity
semantics.
