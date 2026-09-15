# Section 5 Writing Report

## Modified and Created Files

- Modified: `manuscript/sections/05-formal-analysis.tex`
- Modified: `manuscript/figures/tikz/attack-trace.tex`
- Modified: `manuscript/figures/tikz/identity-control-comparison.tex`
- Modified: `manuscript/tables/verification-results.tex`
- Created: `manuscript/notes/section5-writing-report.md`

No Tamarin or ProVerif model, recorded result, artifact, evidence hash, or
research-authority document was modified. No prover execution was performed
during this writing task.

## Review-Driven Revision

This report now reflects the revision following
`manuscript/notes/section5-review-report.md`; the review itself is retained
unchanged as a record of the earlier version.

- The party-level rejection result is used only for branch reachability.
  The two Send tuples in the existence formula are not bound to the rejected
  batch. Rejection of a collected same-party/different-message pair is
  described separately as a rule-semantics observation.
- The unfulfilled assertion that the appendix already summarizes the evidence
  has been removed. Section 5 now identifies the actual model files and static
  evidence package, including the absence of raw prover transcripts.
- Figure/table placement allows positions near the text, and a Section 5
  boundary flush prevents these floats from moving into later sections.
- The duplicate-witness equation separates event assertions from the ordering
  of their timepoints. Repeated step counts remain in the complete result
  table rather than in each paragraph, and redundant comparison prose was cut.

## Structure

1. `5.1 Relaxed Admission: Repeated-Party Counterexample`
2. `5.2 Message-Level Restriction as a Control`
3. `5.3 Party-Level Restoration`
4. `5.4 Controlled Comparison`
5. `5.5 Verification Summary`
6. `5.6 Verification Environment`

## Result Audit

| Model | Lemma | Outcome | Steps | Reported correctly? |
| --- | --- | --- | ---: | --- |
| Relaxed | `normal_relaxed_batch_exists` | verified | 10 | YES |
| Relaxed | `one_send_two_accepts_exists` | verified | 13 | YES |
| Relaxed | `receiver_accept_has_send` | verified | 8 | YES |
| Relaxed | `receiver_accept_injective` | falsified (counterexample found) | 13 | YES |
| Message-level | `repeated_message_rejection_exists` | verified | 4 | YES |
| Message-level | `same_party_different_messages_batch_exists` | verified | 16 | YES |
| Message-level | `accepted_batch_has_distinct_messages` | verified | 31 | YES |
| Message-level | `receiver_accept_has_send` | verified | 8 | YES |
| Message-level | `receiver_accept_injective` | verified | 33 | YES |
| Party-level | `same_party_rejection_exists` | verified | 5 | YES |
| Party-level | `distinct_party_batch_exists` | verified | 17 | YES |
| Party-level | `accepted_batch_has_distinct_parties` | verified | 31 | YES |
| Party-level | `receiver_accept_has_send` | verified | 8 | YES |
| Party-level | `receiver_accept_injective` | verified | 33 | YES |

Mechanical comparison against the approved result set: 14/14 matched;
mismatches: 0.

Rechecked after revision against the 14 rows in the existing prototype
execution report. This validates transcription, not a new prover execution.

## Relaxed Counterexample

- One matching `Send(A,sid,m)` occurrence: YES
- Two `ReceiverAccept` occurrences: YES
- Same `A`, `sid`, `m`, `bid`, and `rst`: YES
- Distinct ordered acceptance timepoints with `r1 < r2`: YES
- Uniqueness of the matching Send occurrence stated: YES
- Unrelated Sends incorrectly excluded: NO
- Modeled sender-origin correspondence preserved: YES
- Formal outcome separated from semantic interpretation: YES

## Message-Level Control

- Equal-message rejection branch reachable: YES
- Rejection existence kept distinct from liveness: YES
- Accepted messages distinct in the modeled batch context: YES
- Scoped receiver injectivity verified: YES
- Same-party/different-message batch reachable: YES
- Witness uses two distinct legitimate sender origins: YES
- Message-level model presented as a control, not a proposed fix: YES

## Party-Level Restoration

- Same-party rejection branch reachable: YES
- Two distinct Send tuples are bound to the rejected batch by the lemma: NO
- Rejection result used only for branch reachability: YES
- Same-party/different-message rejection explained by rule semantics: YES
- Accepted parties distinct in the two-slot model: YES
- Valid distinct-party batch reachable: YES
- Non-vacuity stated explicitly: YES
- Modeled sender-origin correspondence retained: YES
- Scoped receiver injectivity retained as a supporting result: YES
- Unique implementation mechanism claimed: NO

## Controlled Comparison

- Relaxed duplicate-acceptance witness included: YES
- Message-level injectivity plus same-party witness included: YES
- Party-level safety plus valid-batch reachability included: YES
- Message identity, occurrence injectivity, and party identity separated: YES
- Reviewer-triviality objection answered beyond syntactic variable equality: YES

## Necessity Scope

- Necessity is limited to intended party-level batch identity semantics within
  the modeled two-slot admission boundary: YES
- Claim of necessity for all K-Waay security: 0
- Claim of necessity for secrecy or authentication: 0
- Claim of a unique enforcement mechanism: 0
- The reviewed rejection-witness overstatement has been removed; no stronger
  tuple-bound rejection result is claimed.

## Property Misinterpretation

- Full-authentication claim: 0
- Deployment-vulnerability claim: 0
- `KEY`/`TEST` claim: 0
- Upper-layer unconditional impact claim: 0
- Occurrence injectivity equated with party uniqueness: 0
- Rejection reachability presented as universal rejection/liveness: 0

## Figures

- Relaxed counterexample figure: INCLUDED
- One Send, repeated exact tuple, one batch context, two accepts: PASS
- Same `A/sid/m/bid/rst` and distinct `r1/r2` shown: PASS
- Controlled-comparison figure: INCLUDED
- Three coordinate choices and analytical distinction shown: PASS
- Page-render visual inspection after revision: PASS (PDF pages 8-14)
- Relaxed trace: page 9, within 5.1
- Controlled comparison: page 12, before 5.5

## Table

- Verification summary: PASS
- Approved outcome rows: 14
- Extra outcome rows: 0
- Status vocabulary: `verified` / `falsified (counterexample found)`
- Columns: Variant, Property, Outcome, Steps
- Width and page-render inspection after revision: PASS
- Placement before Section 6 and back matter: PASS
- Table 3: page 12, immediately following the 5.5 introduction

## Approximate Word Count

- `texcount -inc -sum sections/05-formal-analysis.tex`: 1,796 total units
  including included figure/table captions and math counts
- Main Section 5 prose: 1,717 words

## Build

- Command: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- Result after revision: PASS
- Output: `manuscript/main.pdf`, 14 pages
- Fatal errors: 0
- Undefined references or citations: 0
- Missing figures or tables: 0
- TikZ failures: 0
- Overfull/underfull box warnings: 0
- Final PDF pages 8-14 visually checked: PASS; no clipping or overlap
- Section 5 ends and Section 6 begins on page 13. A scoped `\FloatBarrier`
  keeps the Section 5 result floats before the discussion without forcing a
  new page; Figure 2 and Table 3 remain on page 12.
- After the boundary revision, PDF pages 12–17 were visually rechecked with
  no clipping, overlap, orphaned heading, or cross-section float.
- The build launcher reports a non-fatal Perl locale fallback; the final
  LaTeX log contains no compilation or reference warnings.
- QA page images remain in `tmp/pdfs/section5-revision/` as untracked scratch
  output because the environment blocked the cleanup command. They are not
  part of the manuscript or verification evidence.

## Verification Environment

- Reported environment: Tamarin 1.12.0, Maude 3.5.1, WSL Ubuntu 24.04
- Manuscript-preparation prover rerun claimed or performed: NO
- Model SHA-256 values match the recorded execution report: YES
- Before/after hashes unchanged for all three models, the execution report,
  frozen environment/command/hash records, Section 4 and its writing report,
  and the original Section 5 review report: YES

## Remaining Issues

- The three Section 5 review findings have been addressed and checked in the
  source and compiled PDF.
- The three appendix files remain placeholders and are not part of this
  Section 5 revision. The text no longer presents them as completed evidence.
- Raw prover transcripts and a stronger tuple-bound rejection witness have not
  been added. Recorded statuses remain report-derived, without a new prover run.
- Broader design implications and limitations remain assigned to Section 6.
- Git commit/push performed: NO

## Verdict

`SECTION_5_REVISED_AND_VALIDATED`

This verdict covers the targeted Section 5 revision, not completion of the
appendices or an independent reproduction of the recorded proofs.
