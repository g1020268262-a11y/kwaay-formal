# Documentation Index

This index separates the current RQ-v2 research authority from the immutable
M0–M5 historical evidence. A document being preserved does not make it
authority for the current research question.

## Current authority: RQ-v2

- [`../README.md`](../README.md): repository entry point and current research
  status.
- [`rq-v2/research-contribution.md`](rq-v2/research-contribution.md): frozen
  current research question, contribution, non-claims, and evidence boundary.
- [`rq-v2/g2-admission-semantics.md`](rq-v2/g2-admission-semantics.md): active
  semantic authority for `DistinctPartyPerBatch`, the identity hierarchy, and
  relaxed/message-level/party-level admission.
- [`rq-v2/prototype-execution-report.md`](rq-v2/prototype-execution-report.md):
  active report for the bounded exploratory RQ-v2 prototypes.
- [`rq-v2/rq-v2-threat-model.md`](rq-v2/rq-v2-threat-model.md): current
  batch-composition adversary and threat-model boundary.
- [`rq-v2/rq-v2-complete-argument-map.md`](rq-v2/rq-v2-complete-argument-map.md):
  canonical argument-map artifact and formal/conceptual evidence boundary.

The canonical chain is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> loss of intended party-level identity interpretation
```

Conditional upper-layer consumption or installation is a separate discussion
boundary and is not a final step of the canonical chain.

## Supporting Analysis

The following documents provide supporting interpretation and do not override
the primary authority above:

- [`rq-v2/invariant-necessity-analysis.md`](rq-v2/invariant-necessity-analysis.md):
  conceptual motivation from the original K-Waay security interface.
- [`rq-v2/invariant-vs-enforcement-analysis.md`](rq-v2/invariant-vs-enforcement-analysis.md):
  distinction between invariant necessity and implementation enforcement.
- [`rq-v2/party-output-binding-analysis-final.md`](rq-v2/party-output-binding-analysis-final.md):
  supporting party-attribution analysis; the legacy `-final` filename does not
  denote primary authority.
- [`rq-v2/security-interface-dependency-analysis.md`](rq-v2/security-interface-dependency-analysis.md):
  conceptual security-interface dependency analysis.

RQ-v2 treats exact-message deduplication as an auxiliary comparison and HMAC as
message-authenticity/integrity/confirmation background. The contribution
target is the necessity of the `DistinctPartyPerBatch` identity invariant for
the intended batch identity semantics, not message identity versus party
identity, a uniquely necessary admission mechanism, or scoped occurrence
injectivity by itself.

## Historical: frozen M0–M5 claim/evidence documents

The following are the **M5 frozen claim/evidence snapshot**, not the authority
for the current RQ-v2 claim vocabulary:

- [`claim-hierarchy.md`](claim-hierarchy.md)
- [`model-mapping.md`](model-mapping.md)
- [`threat-compromise-matrix.md`](threat-compromise-matrix.md)
- [`milestones/`](milestones/)
- [`../artifact/README.md`](../artifact/README.md) and the complete
  [`../artifact/`](../artifact/) contract
- committed evidence under [`../logs/`](../logs/)

Their historical wording and result mappings are preserved verbatim. Read them
as historical artifacts through the current-status notice in the root README.

Historical model-specific interpretation records include:

- [`../tamarin/replay/README.md`](../tamarin/replay/README.md): frozen relaxed
  duplicate-input model;
- [`../tamarin/replay/README-fixed.md`](../tamarin/replay/README-fixed.md):
  legacy exact-message dedup hardening;
- [`../tamarin/replay/README-hmac-only.md`](../tamarin/replay/README-hmac-only.md)
  and [`../tamarin/replay/README-hmac-dedup.md`](../tamarin/replay/README-hmac-dedup.md):
  HMAC confirmation and legacy combined-regression records;
- [`../tamarin/impact/README.md`](../tamarin/impact/README.md): conditional
  `C_install-v2` impact boundary.

## Model documentation

- [`proverif-final-results.md`](proverif-final-results.md) and
  [`proverif-final-targets.md`](proverif-final-targets.md): completed ProVerif
  records.
- [`tamarin/tamarin-v7-results.md`](tamarin/tamarin-v7-results.md) and
  [`tamarin/tamarin-deniability-results.md`](tamarin/tamarin-deniability-results.md):
  historical Tamarin result documentation.
- [`kwaay-tamarin-deniability-review.md`](kwaay-tamarin-deniability-review.md):
  historical review record.
- [`paper/threat-model.md`](paper/threat-model.md): existing scoped threat-model
  notes; it is not a new RQ-v2 document.
- [`cryptoverif/README.md`](cryptoverif/README.md): historical computational-
  proof planning status.

## Historical: milestones and archives

Superseded roadmaps, model plans, stage summaries, and the old paper outline are
preserved under [`../archive/pre-rq-v2/docs/`](../archive/pre-rq-v2/docs/).
They document earlier research decisions and are not the current main line.

[`milestones/`](milestones/) contains the immutable M1–M5 completion records.
They remain authoritative for what was run and frozen at each milestone, even
where their historical research framing has since been superseded.

[`maintenance/pre-rq-v2-cleanup.md`](maintenance/pre-rq-v2-cleanup.md) is the
dated maintenance record for the earlier navigation cleanup. Its stage-status
statements are historical rather than current RQ-v2 status.

## Archive

- [`../archive/pre-rq-v2/`](../archive/pre-rq-v2/): documents superseded during
  the pre-RQ-v2 cleanup.
- [`../archive/old-doc/`](../archive/old-doc/): earlier tool documentation.
- [`../archive/aead-confirmation/`](../archive/aead-confirmation/): historical
  AEAD-confirmation branch material.
- [`../archive/proverif-experiments/`](../archive/proverif-experiments/) and
  [`../archive/tamarin-experiments/`](../archive/tamarin-experiments/): retained
  experimental models.

## Maintenance rule

Do not edit frozen models, raw evidence, result tables, manifests, checksums,
claim sources, or milestone records to retrofit the current RQ-v2 narrative.
Current RQ-v2 claims must be defined under [`rq-v2/`](rq-v2/); frozen historical
files must not be rewritten to retrofit the new narrative.
