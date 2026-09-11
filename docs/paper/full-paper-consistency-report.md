# Full Paper Consistency Report

## 1. Structural Completeness

The assembled draft contains the required title followed by 13 second-level
sections: Abstract, eleven numbered body sections, and References. All required
roles are present:

| Section | Editorial role | Status |
| --- | --- | --- |
| Abstract | Context, stated condition, method, results, and bounded scope | Complete |
| Introduction | Problem, gap, approach, results overview, and exactly three contributions | Complete |
| Background | K-Waay `BatchReceive`, condition origin, and identity coordinates | Complete |
| Problem Statement | Single formal definition and RQ1–RQ3 | Complete |
| Threat Model | Batch-composition adversary, capability, goal, and exclusions | Complete |
| Formal Model | Common lifecycle, R/M/P-semantics, events, properties, and abstraction | Complete |
| Formal Analysis | Evidence-based answers to RQ1–RQ3 | Complete |
| Evaluation | Toolchain, one complete result table, steps, hashes, and provenance | Complete |
| Discussion | Interpretation and formal/conceptual/conditional boundaries | Complete |
| Limitations | Bounded evidence and active non-claims | Complete |
| Related Work | Phase 7A substance with integrated heading and citation format | Complete |
| Conclusion | Answer, comparison, conceptual separation, scope, and design obligation | Complete |
| References | One entry for every cited verified work | Complete |

The Abstract contains 176 English words. The assembled draft contains
approximately 5,800 words, excluding Markdown markup. The Introduction presents
exactly three contributions and does not enumerate the complete lemma set.

## 2. Claim-Evidence Alignment

| Paper claim | Evidence class | Supporting evidence | Alignment |
| --- | --- | --- | --- |
| `DistinctPartyPerBatch` is the analyzed party-level identity invariant | Semantic definition | Separate `A`, `sid`, `m`, slot, `bid`, and `rst` coordinates; formal definition in Section 3 | Aligned |
| Removal permits repeated-party admission | Model semantics plus reachability | R-semantics has no `A1 != A2` guard; repeated complete tuple appears in `one_send_two_accepts_exists` | Aligned |
| Duplicate `ReceiverAccept` behavior is reachable | Formal evidence | R `one_send_two_accepts_exists` verified; R `receiver_accept_injective` falsified | Aligned |
| Exact-message deduplication does not establish party uniqueness | Formal evidence | M `same_party_different_messages_batch_exists` verified alongside message distinction and scoped injectivity | Aligned |
| Party admission restores the intended semantics non-vacuously | Formal evidence | P same-party rejection, accepted-party distinction, and valid distinct-party reachability all verified | Aligned |
| Loss of intended party-level interpretation | Semantic conclusion | Comparison of admitted repeated `A` coordinates with the stated invariant | Aligned and labeled semantic |
| Party-indexed interfaces motivate the dependency | Conceptual analysis | Discussion explicitly states that query/output objects are not modeled | Aligned and labeled conceptual |
| Duplicate installation is only conditional | Separate historical composition evidence | Discussion conditions the statement on `C_install-v2` and excludes it from R/M/P evidence | Aligned and labeled conditional |

No formal result is used to infer deployment behavior, cryptographic security,
key-interface failure, or unconditional upper-layer impact.

## 3. Citation/Reference Alignment

The paper cites 18 unique works: L1, L2, L3, L4, L5, L6, L7, L9, L10, L11,
L13, L15, L16, L17, L18, L19, L20, and L21. Each has
`source_verified=yes` in `literature/citation-verification.tsv`.

| Check | Result |
| --- | ---: |
| Unique in-text citation IDs | 18 |
| Unique bibliography IDs | 18 |
| Unsupported citation IDs | 0 |
| Unverified cited works | 0 |
| Citation without reference | 0 |
| Reference without citation | 0 |
| Duplicate bibliography work | 0 |

L9 is represented as one research work. Its 2019 peer-reviewed conference
version is the main entry, with the extended 2020 journal version recorded as
a note rather than a second bibliography item. The Phase 7A novelty tiers and
collision positioning are unchanged.

## 4. Formal Result Audit

Every machine-checked outcome in the paper belongs to the permitted result
set. The single complete table in Evaluation records all outcomes and step
counts:

| Semantics | Verified | Falsified |
| --- | --- | --- |
| R | `normal_relaxed_batch_exists`; `one_send_two_accepts_exists`; `receiver_accept_has_send` | `receiver_accept_injective` |
| M | `repeated_message_rejection_exists`; `same_party_different_messages_batch_exists`; `accepted_batch_has_distinct_messages`; `receiver_accept_has_send`; `receiver_accept_injective` | None |
| P | `same_party_rejection_exists`; `distinct_party_batch_exists`; `accepted_batch_has_distinct_parties`; `receiver_accept_has_send`; `receiver_accept_injective` | None |

Unexpected lemma names or additional machine-checked statements: **0**. Model
semantics, prover outcomes, semantic interpretation, conceptual motivation, and
conditional historical evidence are kept in separate layers.

## 5. Terminology Audit

The draft consistently uses `K-Waay`, `BatchReceive`,
`DistinctPartyPerBatch`, party-level identity invariant, modeled
protocol-principal coordinate, R-semantics, M-semantics, P-semantics,
`ReceiverAccept`, batch-composition adversary, and fixed-two-slot symbolic
model. In the R/M/P models, `A` always denotes a modeled protocol-principal
coordinate.

“Participant,” “member,” and related terms occur only when describing prior
secure-messaging or group-membership properties. They are not substituted for
the modeled party coordinate. Internal project language such as “frozen,”
“authority,” “repository,” “cleanup,” “Phase,” “claim matrix,” and “current
authority” has zero occurrences in the full paper body.

## 6. Scope and Necessity Audit

Every use of *necessary*, *necessity*, *required*, or *requires* was classified.
The positive research claim is stated only as necessity for preserving the
intended party-level batch identity semantics within the modeled admission
boundary. Other occurrences describe the original stated condition, a formal
predicate, an admission branch, or the scoped literature positioning.

The draft does not claim necessity for K-Waay security, secrecy,
authentication, cryptographic correctness, or every implementation. Abstract
and Conclusion contain no `KEY`, `TEST`, output-key, HMAC-history, or
`C_install-v2` result. The full paper confines interface language to conceptual
motivation and confines `C_install-v2` to a conditional discussion paragraph.

## 7. Novelty Audit

The paper credits K-Waay with the different-party `BatchReceive` condition. It
does not present identity uniqueness, injective agreement, composition-layer
security, participant consistency, or Tamarin as new concepts. The strong
positioning remains limited to:

- the bounded removal/restoration analysis of K-Waay's stated condition; and
- the M-semantics divergence between scoped occurrence injectivity and party
  uniqueness.

The message-versus-party distinction and invariant-versus-enforcement framing
remain supporting explanations rather than upgraded independent novelty
claims. The Related Work section retains the “within the verified literature
corpus and search scope” qualification. Positive priority claims using
“first,” “first-ever,” “no prior work,” or “no previous work”: **0**.

## 8. Redundancy Audit

The formal `DistinctPartyPerBatch` formula appears once, in Problem Statement.
Background gives only its source and informal role. R/M/P-semantics receive a
short overview in Introduction, full rule-level definitions in Formal Model,
RQ-oriented interpretation in Formal Analysis, and one consolidated outcome
table in Evaluation. No second complete lemma table appears.

The fixed-two-slot boundary is stated where a reader needs it—Abstract,
Introduction, the formal definition/model boundary, Related Work positioning,
and Conclusion—without repeating the full non-claims list in every section.
Deployment and cryptographic exclusions are concentrated in Threat Model and
Limitations, with only brief framing in the opening and closing sections.
Remaining repetition is functional scope signaling rather than duplicated
argumentation.

## 9. Reviewer Risk Assessment

### Risk A — The condition is already explicit in K-Waay

**Rating: MEDIUM.** The paper answers that the condition is stated by K-Waay
and is not claimed as a discovery. The contribution is the bounded analysis of
its semantic role and the R/M/P separation. Session/composition work is used
as methodological context for treating such a boundary as an independent
formal object. The residual risk is presentational: a reviewer may still value
the condition only as an assumption unless the controlled comparison remains
prominent.

### Risk B — Removing `A1 != A2` appears trivial

**Rating: MEDIUM.** The paper does not stop at reachability of `A1 = A2`. It
connects removal to a verified one-Send/two-accept trace, uses M-semantics to
show that occurrence injectivity can return while party uniqueness remains
false, and uses P-semantics to show restoration plus valid-batch non-vacuity.
These points directly answer the objection, although the small model leaves a
moderate reviewer-perception risk.

### Risk C — Fixed-two-slot model may look like a toy

**Rating: MEDIUM.** The draft explains that two slots are the minimal witness
size for a pairwise distinctness violation and that the abstraction isolates
the checked identity coordinate. It explicitly declines arbitrary-size
generalization. The remaining risk is inherent to the deliberately bounded
evidence, not an unacknowledged scope expansion.

### Risk D — Occurrence injectivity as a contribution

**Rating: LOW.** The paper explicitly answers “no.” Injectivity is established
prior vocabulary and serves only as a supporting comparison dimension. The
primary result concerns party-level invariant necessity and R/M/P separation.

### Risk E — Why message deduplication does not solve party uniqueness

**Rating: LOW.** The M-semantics evidence is stated together:
`receiver_accept_injective` is verified and
`same_party_different_messages_batch_exists` is verified. The paper explains
that these properties constrain occurrence and party coordinates,
respectively, without portraying deduplication as ineffective.

### Risk F — Absence of a real-world vulnerability

**Rating: LOW.** No such result is claimed. Threat Model and Limitations state
that the work is a specification- and integration-level invariant analysis
without implementation or deployment evidence.

### Risk G — Novelty relative to names, session handling, and injectivity

**Rating: MEDIUM.** The Related Work section assigns the general concepts to
prior work and scopes the contribution to the K-Waay `BatchReceive`
removal/control/restoration comparison and the M-semantics divergence. The
qualified search conclusion avoids an exhaustive priority assertion. Residual
risk comes from the closeness of the conceptual vocabulary, so the scoped
positioning must remain intact through venue-format revision.

## 10. Temporary Title Review

Candidate titles:

1. **Identity Invariants in Batch Admission: A Formal Analysis of K-Waay BatchReceive**
2. **Formalizing Party Distinctness at the K-Waay BatchReceive Boundary**
3. **Party-Level Identity in Batched Reception: A Symbolic Analysis of K-Waay**
4. **From Message Deduplication to Party Admission: An R/M/P Analysis of K-Waay BatchReceive**
5. **Distinct Parties per Batch: A Bounded Formal Study of K-Waay BatchReceive**

**Selected temporary title:** *Identity Invariants in Batch Admission: A
Formal Analysis of K-Waay BatchReceive*.

The selected title identifies the semantic object (identity invariants), the
analyzed boundary (batch admission), the method (formal analysis), and the
protocol interface (`BatchReceive`). It does not suggest a full verification
of K-Waay or foreground adversarial language that the evidence does not
support.

## 11. Final Verdict

**PAPER_DRAFT_READY_FOR_REVIEW**
