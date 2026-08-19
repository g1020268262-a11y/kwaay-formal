# Tamarin Documentation

This directory indexes historical Tamarin documentation. The repository now
contains completed and frozen Tamarin models and evidence; the earlier planning
statement that no formal Tamarin model existed is obsolete.

## Current RQ-v2 status

The current RQ-v2 semantic and result authority is
[`../rq-v2/`](../rq-v2/). In this research line, `A` is the modeled
protocol-principal identity coordinate. This model-level coordinate is not a
claim that `A` equals a deployed real-world party identifier or implementation
object.

The current bounded exploratory prototypes are:

- [`rqv2_relaxed.spthy`](../../tamarin/rq-v2-minimal/rqv2_relaxed.spthy):
  relaxed admission model used to expose the consequence of removing
  `DistinctPartyPerBatch`;
- [`rqv2_message_dedup.spthy`](../../tamarin/rq-v2-minimal/rqv2_message_dedup.spthy):
  exact-message dedup auxiliary comparison, not a replacement for party
  admission;
- [`rqv2_party_admission.spthy`](../../tamarin/rq-v2-minimal/rqv2_party_admission.spthy):
  party-admission model of the identity-level invariant.

Their semantics and limitations are defined in
[`g2-admission-semantics.md`](../rq-v2/g2-admission-semantics.md) and
[`prototype-execution-report.md`](../rq-v2/prototype-execution-report.md).

## Historical M0-M5 status

M0–M5 Tamarin models, milestone records, raw logs, result tables, and artifact
bindings are preserved as a reproducible legacy evidence snapshot. They must be
read through the current transition notice in [`../../README.md`](../../README.md).

In particular, the frozen duplicate-input model is now interpreted as a
relaxed-input / integration-contract experiment because it permits the same
modeled sender identity `A` and the same complete message in multiple batch
entries. It is a historical predecessor, not the current RQ-v2 relaxed
prototype or the current party-admission invariant model.

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

This index does not modify any model, lemma, theorem, or frozen result. Current
RQ-v2 definitions and claims remain under [`../rq-v2/`](../rq-v2/).
