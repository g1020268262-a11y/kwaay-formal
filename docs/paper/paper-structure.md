# RQ-v2 Paper Structure

## Status and Writing Rule

This document is a writing plan, not research authority. Each section below
must preserve the frozen RQ-v2 claim boundary and distinguish semantic
definitions, direct formal evidence, conceptual analysis, and historical
background.

## 1. Introduction

### What to write

- Introduce batch admission as an identity-semantics problem in multi-entry
  protocol processing.
- State the paper question: why is `DistinctPartyPerBatch` necessary for the
  intended party-level interpretation of one modeled `BatchReceive` batch?
- Summarize the R/M/P comparison and its bounded result.
- Present the paper's main contribution as invariant-necessity analysis, not as
  a claim about a deployed implementation or primitive-level security.
- Preview the consequence chain ending in loss of intended party-level identity
  interpretation.

### Existing artifacts

- [`../rq-v2/research-contribution.md`](../rq-v2/research-contribution.md)
- [`../rq-v2/rq-v2-complete-argument-map.md`](../rq-v2/rq-v2-complete-argument-map.md)
- [`contribution-outline.md`](contribution-outline.md)

## 2. Background

### What to write

- Explain the relevant `BatchReceive` abstraction and the stated distinct-party
  condition without expanding into unmodeled implementation details.
- Define the identity hierarchy: party, session, prekey, message, sender
  occurrence, slot, receiver state, and batch.
- Explain why one party may legitimately have multiple sessions and messages,
  while two slots of one admitted batch remain subject to party uniqueness.
- Briefly position HMAC confirmation, replay, and exact-message dedup as
  historical or auxiliary context rather than current claim authority.

### Existing artifacts

- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md),
  especially the abstract entry model and identity-layer separation
- [`../../README.md`](../../README.md), especially current versus historical
  artifact roles
- [`../tamarin/README.md`](../tamarin/README.md) for the current/historical model
  index

## 3. Problem Statement

### What to write

- Give the normalized invariant:
  `i != j` implies `party(E_i) != party(E_j)` within one batch.
- Define R-semantics, M-semantics, and P-semantics.
- State the primary question about invariant removal and restoration.
- State the auxiliary message-identity comparison.
- Explain why batch identity semantics, rather than occurrence injectivity
  alone, is the primary target.

### Existing artifacts

- [`../rq-v2/research-contribution.md`](../rq-v2/research-contribution.md)
- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md)
- [`../rq-v2/invariant-vs-enforcement-analysis.md`](../rq-v2/invariant-vs-enforcement-analysis.md)
  as Supporting Analysis

## 4. Threat Model

### What to write

- Reproduce the frozen batch-composition adversary boundary.
- State that the adversary can arrange entries, place them in distinct slots,
  and repeat one valid modeled party coordinate when the identity guard is
  absent.
- Explain that the construction does not require impersonation, key recovery,
  forgery, or modification of authenticated material.
- Define the goal as reaching an invalid repeated-party batch and duplicate
  receiver acceptance at the modeled boundary.
- Keep conceptual interface motivation separate from direct formal evidence.

### Existing artifacts

- [`../rq-v2/rq-v2-threat-model.md`](../rq-v2/rq-v2-threat-model.md) as the sole
  primary threat-model authority
- [`../rq-v2/rq-v2-complete-argument-map.md`](../rq-v2/rq-v2-complete-argument-map.md)
  for its placement in the complete argument

## 5. Formal Model

### What to write

- Describe the fixed-two-slot symbolic abstraction and common entry tuple
  `(A, sid, m)`.
- Explain the separate party-creation and sender-session/message coordinates.
- Present common collection and receiver-acceptance structure across the three
  models.
- Describe only the admission difference:
  no uniqueness guard, message inequality, or party inequality.
- Define events and properties used in the paper without changing their
  formulas.
- State omitted mechanisms: cryptographic primitives, compromise, output keys,
  applications, and concrete enforcement components.

### Existing artifacts

- [`../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy)
- [`../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy`](../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy)
- [`../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy)
- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md)

## 6. Formal Analysis

### What to write

- Present the relaxed witness and the falsified scoped injectivity lemma.
- Explain precisely that the witness contains one matching `Send` occurrence
  and two `ReceiverAccept` occurrences in one batch context.
- Present the message-dedup results: identical-message rejection, distinct
  accepted messages, and reachable same-party/different-message composition.
- Present party-admission safety, same-party rejection reachability, and valid
  distinct-party non-vacuity.
- Connect each result to the canonical chain without extending it to keys or an
  upper-layer consumer.

### Existing artifacts

- [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md)
- [`../../artifact/results/rqv2-claim-matrix.tsv`](../../artifact/results/rqv2-claim-matrix.tsv)
- [`contribution-evidence-map.md`](contribution-evidence-map.md)

## 7. Evaluation

### What to write

- Report the Tamarin and Maude versions and the recorded WSL environment.
- Give the three model hashes and explain that the freeze package transcribes
  the existing execution report without a new prover run.
- Compare the R/M/P result profiles in one table.
- Evaluate non-vacuity, identity-coordinate isolation, and agreement between
  positive witnesses and universal properties.
- Report the bounded scope explicitly rather than treating model size as an
  implementation evaluation.

### Existing artifacts

- [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md)
- [`../../artifact/rqv2-freeze/environment.txt`](../../artifact/rqv2-freeze/environment.txt)
- [`../../artifact/rqv2-freeze/models-sha256.txt`](../../artifact/rqv2-freeze/models-sha256.txt)
- [`../../artifact/rqv2-freeze/verification-commands.txt`](../../artifact/rqv2-freeze/verification-commands.txt)
- [`../../artifact/rqv2-freeze/freeze-manifest.tsv`](../../artifact/rqv2-freeze/freeze-manifest.tsv)

## 8. Discussion

### What to write

- Explain why `DistinctPartyPerBatch` is more than an ordinary input range
  restriction.
- Separate the semantic invariant from party-admission checking as one
  restoration mechanism.
- Discuss why exact-message dedup and HMAC constrain different dimensions.
- Use the original party-indexed interface only as conceptual motivation for
  the identity dependency.
- Keep upper-layer consumption/install impact conditional on an explicit
  composition interface.

### Existing artifacts

- [`../rq-v2/invariant-necessity-analysis.md`](../rq-v2/invariant-necessity-analysis.md)
  as conceptual Supporting Analysis
- [`../rq-v2/invariant-vs-enforcement-analysis.md`](../rq-v2/invariant-vs-enforcement-analysis.md)
- [`../rq-v2/security-interface-dependency-analysis.md`](../rq-v2/security-interface-dependency-analysis.md)
- [`../rq-v2/party-output-binding-analysis-final.md`](../rq-v2/party-output-binding-analysis-final.md)

## 9. Limitations

### What to write

- State the symbolic and fixed-two-slot scope.
- State that the prototypes do not model KEMs, signatures, HMAC computation,
  compromise, prekey cryptography, output keys, applications, or deployed
  behavior.
- Distinguish rejection reachability from a liveness guarantee requiring every
  invalid batch to reach rejection.
- Exclude arbitrary-length, cross-batch, rollback, restart, concurrency, and
  computational-security conclusions.
- State that enforcement location and concrete failure behavior are not fixed.
- State that direct evidence ends at receiver acceptance.

### Existing artifacts

- [`../rq-v2/research-contribution.md`](../rq-v2/research-contribution.md), model
  scope and non-claims
- [`../rq-v2/prototype-execution-report.md`](../rq-v2/prototype-execution-report.md),
  model-design audit findings
- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md),
  open decisions and contract verdict

## 10. Related Work

### What to write

- Organize related work around protocol identity invariants, batch/group
  composition semantics, symbolic correspondence and injectivity, replay and
  deduplication, and formal admission-control models.
- Compare problem dimensions rather than claiming that message authentication
  or replay defenses solve party-level admission.
- Distinguish computational security definitions from the current symbolic
  identity-semantics question.
- Add literature citations only after checking the original sources; the
  current repository does not itself supply a complete related-work corpus.

### Existing artifacts

- [`../rq-v2/research-contribution.md`](../rq-v2/research-contribution.md) for the
  exact contribution boundary
- [`../rq-v2/g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md) for
  comparison dimensions
- [`../../docs/claim-hierarchy.md`](../../docs/claim-hierarchy.md) only as
  historical repository context, not current RQ-v2 claim authority

## Cross-Section Consistency Rule

Every paper section must preserve the following evidence separation:

- semantic authority defines the invariant and admission meanings;
- formal evidence supports only the recorded model properties;
- conceptual analysis motivates interface-level significance;
- historical artifacts provide background and provenance; and
- no section may silently promote a conditional or unmodeled consequence into
  a formal result.
