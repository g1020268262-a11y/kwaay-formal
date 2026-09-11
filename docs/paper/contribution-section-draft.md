# RQ-v2 Contribution Section Draft

This section is derived exclusively from the frozen mappings in
[`contribution-evidence-map.md`](contribution-evidence-map.md). Each contribution
below follows the required Claim → Evidence → Limitation structure and does not
extend the mapped claim set.

## Contribution 1

**Title:** Party-Level Identity Invariant for Batch Admission

**Claim:** `DistinctPartyPerBatch` is the identity invariant requiring distinct
slots in one admitted batch to carry distinct modeled party coordinates. Party
identity is separate from message identity, session identity, and slot
identity.

**Evidence:** The frozen semantic contract defines the invariant as
`i != j` implying `party(E_i) != party(E_j)` within one batch and assigns
separate coordinates to party `A`, message `m`, session `sid`, slot, batch, and
receiver state. This is the semantic evidence recorded as C1 and C6 in the
contribution-evidence map.

**Artifact:**
[`contribution-evidence-map.md`, C1 and C6](contribution-evidence-map.md#claim--evidence--artifact);
[`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md).

**Limitation:** The claim concerns same-batch modeled party coordinates. It does
not prohibit one party from participating through other sessions, messages, or
batches, and it does not map `A` to a particular implementation identity.

## Contribution 2

**Title:** Bounded Consequence of Removing Party Uniqueness

**Claim:** Removing the party-uniqueness guard permits same-batch
repeated-party composition, and duplicate receiver acceptance is reachable in
the relaxed two-slot model.

**Evidence:** R-semantics admits collected entries without comparing `A1` and
`A2`. In the recorded results, `one_send_two_accepts_exists` is verified and
`receiver_accept_injective` is falsified. The witness contains one matching
`Send(A,sid,m)` occurrence and two
`ReceiverAccept(A,sid,m,bid,rst)` occurrences in one batch context. This is the
formal evidence mapped by C2 and C3.

**Artifact:**
[`contribution-evidence-map.md`, C2 and C3](contribution-evidence-map.md#claim--evidence--artifact);
[`../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy);
[`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md).

**Limitation:** The result is restricted to one fixed two-slot batch and
receiver state in the relaxed symbolic model. It is not an execution satisfying
the retained distinct-party precondition, and it does not imply an upper-layer
consumer or installation event.

## Contribution 3

**Title:** Message-Level Comparison and Party-Level Restoration

**Claim:** Exact-message deduplication does not enforce party uniqueness,
whereas party-level admission restores the intended distinct-party batch
semantics in the bounded model while preserving a reachable valid batch.

**Evidence:** In M-semantics, `repeated_message_rejection_exists` and
`same_party_different_messages_batch_exists` are verified: equal messages can
be rejected while different messages from the same party remain admissible. In
P-semantics, `same_party_rejection_exists`,
`accepted_batch_has_distinct_parties`, and `distinct_party_batch_exists` are
verified. These results provide the C4, C5, and C7 evidence in the
contribution-evidence map.

**Artifact:**
[`contribution-evidence-map.md`, C4, C5, and C7](contribution-evidence-map.md#claim--evidence--artifact);
[`../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy`](../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy);
[`../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy);
[`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md).

**Limitation:** The comparison distinguishes message identity from party
identity within the fixed-two-slot prototypes. Party admission is one modeled
restoration mechanism, not a uniquely required algorithm or enforcement
location, and the recorded reachability result is not a general liveness or
throughput guarantee.
