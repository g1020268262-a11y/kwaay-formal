# Tamarin Documentation

This directory indexes historical Tamarin documentation. The repository now
contains completed and frozen Tamarin models and evidence; the earlier planning
statement that no formal Tamarin model existed is obsolete.

## Current status

M0–M5 Tamarin models, milestone records, raw logs, result tables, and artifact
bindings are preserved as a reproducible legacy evidence snapshot. They must be
read through the current transition notice in [`../../README.md`](../../README.md).

In particular, the frozen duplicate-input model is now interpreted as a
relaxed-input / integration-contract experiment because it permits the same
modeled sender identity `A` and the same complete message in multiple batch
entries. The exact mapping from `A` to the specification-level notion of party
remains a Stage-0 modeling question. No distinct-party model or RQ-v2 theorem
has been created during this cleanup.

## Retained documentation

- [`tamarin-v7-results.md`](tamarin-v7-results.md): fixed-slot lifecycle result
  record.
- [`tamarin-deniability-results.md`](tamarin-deniability-results.md): historical
  deniability experiment results.
- [`../kwaay-tamarin-deniability-review.md`](../kwaay-tamarin-deniability-review.md):
  historical review and scope assessment.
- [`../../tamarin/replay/README.md`](../../tamarin/replay/README.md): frozen
  relaxed duplicate-input model interpretation.
- [`../../tamarin/replay/README-fixed.md`](../../tamarin/replay/README-fixed.md):
  legacy exact-message dedup hardening.
- [`../../tamarin/impact/README.md`](../../tamarin/impact/README.md): conditional
  `C_install-v2` impact model.
- [`../milestones/`](../milestones/): immutable M1–M5 completion records.

## Superseded planning documents

The earlier Tamarin model plan and stage summary are retained under
[`../../archive/pre-rq-v2/docs/tamarin/`](../../archive/pre-rq-v2/docs/tamarin/).
They are historical provenance, not current research direction.

## Boundary

This index does not define Stage 0, the RQ-v2 invariant, a new model, a new
lemma, or a new theorem.
