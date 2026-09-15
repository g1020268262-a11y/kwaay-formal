# Section 4 Writing Report

## Modified and Created Files

- Modified: `manuscript/sections/04-formal-modeling.tex`
- Modified: `manuscript/paper-content.tex` (Section 4 title only)
- Created: `manuscript/notes/section4-writing-report.md`

## Structure

- `4.1 Modeling Objective and Abstraction`
- `4.2 Common Two-Slot Lifecycle`
- `4.3 Relaxed Admission Model`
- `4.4 Message-Level Restriction Model`
- `4.5 Party-Level Admission Model`
- `4.6 Events and Analysis Properties`

## Model Authority

- `rqv2_relaxed.spthy`: read and checked
- `rqv2_message_dedup.spthy`: read and checked
- `rqv2_party_admission.spthy`: read and checked
- Requested `tamarin/rq-v2-minimal/README.md`: MISSING
- Markdown/model conflict resolution: actual `.spthy` semantics take priority

## Model-Fidelity Audit

- Sender tuple is `(A,sid,m)`: YES
- Sender origin recorded for the complete tuple: YES
- Candidate tuple exposed through the symbolic network: YES
- Fresh batch and receiver-context coordinates represented by `bid` and `rst`: YES
- Collection is sequential over two slots: YES
- Accepted processing requires an exact persistent sender-origin tuple: YES
- `ReceiverAccept` parameter order checked against all three models: YES
- Unsupported model statements: 0

## Cross-Model Control Audit

- Common lifecycle identified across all three models: YES
- Principal analytical variation identified as the admission predicate: YES
- Relaxed model described without a party or message inequality guard: YES
- Message-level equality/rejection and inequality/admission branches described: YES
- Party-level equality/rejection and inequality/admission branches described: YES
- Theories claimed to differ in only one line: NO
- Party admission described as the unique implementation mechanism: NO

## Events and Property Classes

- `Send`, `BatchReceive`, `ReceiverAccept`, `Reject`, and `Neq` checked: YES
- `Reject` scoped to message-level and party-level models: YES
- `Neq` global-restriction encoding described: YES
- Reachability/non-vacuity described: YES
- Sender-origin correspondence described: YES
- Scoped occurrence injectivity described: YES
- Identity-coordinate safety described: YES
- Lemma outcomes reported: NO

## Notation Audit

- Stable coordinates: `A`, `sid`, `m`, `bid`, `rst`
- `rho` occurrences: 0
- `rst` described only as a modeled receiver-context coordinate: YES

## Result-Leakage Audit

- Machine-checked outcomes reported prematurely: 0
- Step counts reported: 0
- Counterexample outcomes reported: 0

## Citation Audit

- Tamarin citation key checked: `meier2013tamarin`
- Repository paths exposed in paper prose: 0

## Approximate Word Count

- `texcount` sum: 1,239 words/units (1,168 prose words, 20 heading words,
  and 6 caption words; mathematical tokens are counted separately by the
  tool).
- This is within the accepted compact range for a complete modeling section.

## Build

- Command: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- Result: PASS
- Output: `manuscript/main.pdf`, 14 pages
- Undefined references or citations: 0
- Section 4 overfull/underfull box warnings: 0
- Pre-existing warnings outside Section 4: 2 underfull boxes in the Section 5
  model-comparison table

## Remaining TODOs

- None within Section 4.
- Section 5 retains all prover outcomes, traces, and step counts.

## Verdict

`SECTION_4_READY_FOR_REVIEW`
