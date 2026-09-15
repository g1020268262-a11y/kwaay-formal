# Section 3 Structural Revision Report

## Structure

- Chapter title: `Security Objective and Threat Model`
- `3.1 Party-Level Batch Identity Objective`
- `3.2 Batch-Composition Adversary`
- `3.3 Analysis Boundary`

## Security Objective

- DistinctPartyPerBatch formally defined in Section 3: YES
- Formal definition removed from Section 2: YES
- Same-batch locality distinguished from global party uniqueness: YES
- Definitional `necessary` claim removed: YES
- General-n objective separated from fixed two-slot evidence: YES
- Arbitrary-n protocol proof claimed: NO
- Unique implementation mechanism claimed: NO

## Threat Model

- Batch-composition adversary clearly defined: YES
- Selection, replay, arrangement, and admission-presentation capabilities stated: YES
- Candidate availability connected to the modeled sender lifecycle: YES
- Exact sender-origin tuple required for accepted-component matching: YES
- Party-only matching used: NO
- Occurrence notation unified from `rho` to `sid` across Sections 2--3: YES
- DistinctPartyPerBatch quantifier simplified: YES
- Adversary first introduced as a symbolic network adversary with batch-composition control: YES
- Cryptographic-break claim introduced: NO
- HMAC wording retained: NO
- Cryptographic-capability exclusion expressed as path non-reliance: YES
- Concrete implementation input-acquisition claim introduced: NO

## Analysis Boundary

- Direct evidence endpoint: `ReceiverAccept`
- `ReceiverAccept` identified as a component-level symbolic event: YES
- `KEY`/`TEST` modeled: NO
- Deployment claim: NO
- Original K-Waay theorem invalidation claim: NO
- Upper-layer unconditional impact claim: NO

## Research Questions and Controls

- Dedicated Research Questions subsection retained: NO
- Existing Section 2 research questions referenced briefly: YES
- Section 2 RQ2 aligned to the full sender-origin occurrence relation: YES
- Section 2 RQ3 reduced to message-to-party coordinate substitution: YES
- Admission-control design detail retained in Section 3: NO
- RQ1--RQ3 location checked: Section 2 currently contains their formal statements; Introduction remains a writing skeleton.

## Result Leakage

- Premature machine outcomes: 0
- Tamarin rules or lemma names introduced: 0
- Counterexample traces reported: 0

## Unsupported Claims

- Count: 0

## Approximate Word Count

- 831 English words after stripping comments and LaTeX commands approximately.
- Required range: 800--1200 words.
- Required range: 800--1200 words.

## Build

- Command: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- Result: PASS
- Output: `manuscript/main.pdf` (12 pages)
- Undefined references or citations: 0
- Chapter 3 overfull/underfull box warnings: 0
- Existing unrelated table underfull-box warnings: 2

## Remaining TODOs

- Two-slot methodological rationale moved to Section 4.1: YES
- Repeated fixed-two-slot sentence removed from Section 3.3: YES
- Confirm when completing Section 4 that the concrete sender-origin instrumentation matches the full tuple described here.
- Keep all machine-checked outcomes in Section 5; Section 3 intentionally states none.

## Verdict

`SECTION_3_READY_TO_FREEZE`
