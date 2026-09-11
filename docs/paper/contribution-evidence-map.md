# RQ-v2 Contribution-Evidence Map

## Status and Use

This paper-planning map connects frozen claims to existing evidence and
artifacts. It does not add claims, properties, models, or results. When drafting
the paper, the wording in the “Allowed paper statement” column is the maximum
scope supported by the mapped evidence.

## Evidence Classes

- **Semantic authority:** defines an invariant or model interpretation; it is
  not by itself a prover result.
- **Formal evidence:** a recorded property of one of the three bounded RQ-v2
  Tamarin prototypes.
- **Conceptual analysis:** explains why the identity relationship may matter
  beyond the directly modeled boundary.
- **Historical context:** preserved earlier work that is not current RQ-v2
  claim authority.

## Claim → Evidence → Artifact

| ID | Claim | Evidence | Artifact | Evidence class | Allowed paper statement | Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | `DistinctPartyPerBatch` is an identity invariant. | The frozen semantic contract requires distinct modeled party coordinates in distinct slots of one admitted batch. | [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md), invariant definition and `P_batch-id` target | Semantic authority | `DistinctPartyPerBatch` is the party-level identity invariant analyzed by RQ-v2. | Same-batch modeled party coordinate only; the same party may have other sessions, messages, or batches. |
| C2 | Removing the invariant allows repeated-party admission. | R-semantics has no party-uniqueness guard and admits collected entries without comparing `A1` and `A2`. | [`../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy); [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md) | Formal model semantics plus recorded execution | The relaxed two-slot model permits same-batch repeated-party composition. | Not a valid execution under the retained distinct-party precondition and not a deployed-behavior claim. |
| C3 | Duplicate receiver acceptance is reachable after invariant removal. | `one_send_two_accepts_exists` is verified and `receiver_accept_injective` is falsified in the relaxed model. | [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md); [`../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy) | Formal evidence | One `Send(A,sid,m)` occurrence can have two `ReceiverAccept(A,sid,m,bid,rst)` occurrences in the scoped relaxed model. | One fixed two-slot batch and receiver state; no upper-layer consequence follows automatically. |
| C4 | Message deduplication cannot replace party uniqueness. | M-semantics rejects equal messages, while `same_party_different_messages_batch_exists` is verified. | [`../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy`](../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy); [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md) | Formal evidence | Exact-message deduplication does not enforce `DistinctPartyPerBatch` because different messages from the same modeled party remain admissible. | Non-equivalence of message and party coordinates; not a claim that deduplication lacks every useful replay property. |
| C5 | Party admission restores the intended semantics. | `accepted_batch_has_distinct_parties`, `same_party_rejection_exists`, and `distinct_party_batch_exists` are verified. | [`../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy); [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md) | Formal evidence | Party-level admission restores distinct-party batch semantics in the bounded model while preserving a reachable valid batch. | One restoration model; no uniquely mandatory algorithm or enforcement location. |
| C6 | Party identity is distinct from message, session, and slot identity. | The entry abstraction and modeling requirements assign separate coordinates to `A`, `m`, `sid`, slot, batch, and receiver state. | [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md) | Semantic authority | Message or session equality/inequality cannot substitute for party equality/inequality in this analysis. | `A` is a modeled protocol-principal coordinate, not a deployed database or API identity. |
| C7 | The party-admission result is non-vacuous. | `distinct_party_batch_exists` is verified and contains two parties, two sends, one admitted batch, and two accepts. | [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md); [`../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy) | Formal evidence | Safety is not obtained by rejecting every batch in the modeled system. | Reachability, not a general liveness or throughput result. |
| C8 | The relevant adversary is a batch-composition adversary. | The frozen threat model permits arranging valid modeled entries and repeating a party coordinate without requiring primitive compromise. | [`../rq-v2/rq-v2-threat-model.md`](../rq-v2/rq-v2-threat-model.md) | Threat-model authority | The studied threat concerns identity-level batch composition at admission. | Cryptographic mechanisms are outside the current prototypes, so their security is not proved by this result. |
| C9 | Party-indexed interfaces motivate the semantic dependency. | The original interface interpretation conceptually relates a party coordinate to a corresponding component. | [`../rq-v2/security-interface-dependency-analysis.md`](../rq-v2/security-interface-dependency-analysis.md); [`../rq-v2/invariant-necessity-analysis.md`](../rq-v2/invariant-necessity-analysis.md) | Conceptual analysis | The original interface motivates why unique party interpretation matters. | No output-key objects, `KEY`, `TEST`, or key-correctness relations are directly formalized. |
| C10 | Upper-layer impact is conditional only. | No current RQ-v2 prototype property models consumption or installation; the claim matrix marks this result `not-modeled-in-current-prototypes`. | [`../../artifact/results/rqv2-claim-matrix.tsv`](../../artifact/results/rqv2-claim-matrix.tsv); [`../rq-v2/research-contribution.md`](../rq-v2/research-contribution.md) | Explicit non-result / composition boundary | Duplicate consumption or installation may be discussed only under a separately stated composition interface such as `C_install-v2`. | Must not be presented as a direct RQ-v2 prototype result. |

## Formal Result Index

| Model | Property | Recorded status | Supports |
| --- | --- | --- | --- |
| `rqv2_relaxed.spthy` | `normal_relaxed_batch_exists` | verified | Relaxed-model non-vacuity |
| `rqv2_relaxed.spthy` | `one_send_two_accepts_exists` | verified | C3 duplicate-acceptance reachability |
| `rqv2_relaxed.spthy` | `receiver_accept_has_send` | verified | Every modeled accept has a prior matching send |
| `rqv2_relaxed.spthy` | `receiver_accept_injective` | falsified | C3 duplicate-acceptance counterexample |
| `rqv2_message_dedup.spthy` | `repeated_message_rejection_exists` | verified | Exact-message rejection reachability |
| `rqv2_message_dedup.spthy` | `same_party_different_messages_batch_exists` | verified | C4 message/party non-equivalence |
| `rqv2_message_dedup.spthy` | `accepted_batch_has_distinct_messages` | verified | M-semantics message-level safety |
| `rqv2_message_dedup.spthy` | `receiver_accept_injective` | verified | Scoped occurrence injectivity under M-semantics |
| `rqv2_party_admission.spthy` | `same_party_rejection_exists` | verified | Same-party rejection reachability |
| `rqv2_party_admission.spthy` | `distinct_party_batch_exists` | verified | C5/C7 valid-batch non-vacuity |
| `rqv2_party_admission.spthy` | `accepted_batch_has_distinct_parties` | verified | C5 party-level safety |
| `rqv2_party_admission.spthy` | `receiver_accept_injective` | verified | Supporting scoped occurrence property |

The complete recorded property sets, including shared
`receiver_accept_has_send` results, remain authoritative in
[`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md)
and
[`../../artifact/rqv2-freeze/freeze-manifest.tsv`](../../artifact/rqv2-freeze/freeze-manifest.tsv).

## Excluded Inference Map

| Available evidence | Inference that must not be made | Reason |
| --- | --- | --- |
| Repeated-party relaxed trace | A deployed server omits party admission | No deployed implementation is modeled or audited. |
| Duplicate `ReceiverAccept` occurrences | Duplicate installation or application action | No current RQ-v2 consumer is modeled. |
| Conceptual party-indexed interface dependency | A key-query or test-query property is false | `KEY`, `TEST`, and output-key objects are absent from the prototypes. |
| Message-dedup comparison | Message deduplication is useless for replay handling | The evidence establishes only that message identity is not party identity. |
| Party-admission restoration | Every implementation must use the modeled check | The result establishes the invariant in one abstraction, not a unique mechanism. |
| Fixed-two-slot proofs | Arbitrary-size or cross-batch guarantees | The current models and evidence are explicitly bounded. |

## Paper Traceability Rule

Every theorem/result sentence in the paper should identify:

1. the model and property name;
2. the recorded status;
3. whether the statement is semantic, formal, conceptual, or historical; and
4. the fixed-two-slot and admission-boundary limitation where applicable.
