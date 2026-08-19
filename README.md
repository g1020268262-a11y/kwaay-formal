# K-Waay symbolic formal-analysis repository

This repository contains scoped ProVerif and Tamarin models for K-Waay,
together with the frozen M0–M5 evidence, result tables, raw logs, provenance,
checksums, and reproducibility contract.

It is a symbolic formal-analysis repository. It is not a verification of a
complete K-Waay implementation or evidence about a deployed system.

## Current research status

M0–M5 remain frozen as a reproducible historical evidence snapshot. They
record the earlier symbolic-analysis milestones, models, lemmas, queries,
results, and evidence; they are not the current research direction.

The current research direction is **RQ-v2: DistinctPartyPerBatch necessity
analysis**. RQ-v2 studies the identity-level invariant that two distinct slots
of one `BatchReceive` batch must not carry the same party. It compares relaxed,
message-level, and party-level admission semantics in order to determine the
formal consequences of removing that invariant.

The active RQ-v2 authority is under [`docs/rq-v2/`](docs/rq-v2/):

- [`g2-admission-semantics.md`](docs/rq-v2/g2-admission-semantics.md) defines
  the party, message, session, and batch-admission semantics;
- [`prototype-execution-report.md`](docs/rq-v2/prototype-execution-report.md)
  records the bounded exploratory comparison.

The current research chain is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> conditional upper-layer duplicate consumption/install impact
```

The final contribution target is the necessity of
`DistinctPartyPerBatch` for the intended batch identity semantics. Scoped
occurrence injectivity and exact-message deduplication are supporting analyses,
not the final contribution.

## Important interpretation update

The frozen duplicate-input Tamarin model permits the same modeled sender
identity `A` and the same complete message to occur in multiple entries within
one `BatchReceive` instance. K-Waay's full specification states a distinct-
party-per-`BatchReceive` precondition. For the current RQ-v2 formal identity
coordinate, modeled `A` denotes the specification-level protocol principal;
this does not identify `A` with an application account, public-key byte string,
prekey, message, session identifier, or sender occurrence.

The frozen duplicate-acceptance result is therefore currently interpreted as a
**relaxed-input / integration-robustness result**: it records what the bounded
symbolic model permits when that admission invariant is not enforced. It is not
a counterexample to executions satisfying the specification's stated distinct-
party `BatchReceive` precondition or evidence of a deployed implementation
flaw.

The current repository contains no evidence of a complete, publicly auditable
K-Waay caller/server/batching implementation. The repository consequently does
not claim that a real server omits a distinct-party check.

## Historical evidence roles

### HMAC confirmation

HMAC confirmation is retained as evidence about agreement and explicit key
confirmation. It is not treated as a proposed solution to `BatchReceive`
admission uniqueness. HMAC confirmation addresses agreement/key confirmation;
it is not an admission-uniqueness mechanism.

### Exact-message dedup

The frozen M3 exact-message dedup model is retained as historical message-level
hardening. It rejects identical complete-message duplication within the
modeled batch. It is not equivalent to the specification's broader distinct-
party invariant: the same modeled sender identity `A` may be associated with
two different messages. RQ-v2 retains this model only as an auxiliary
comparison showing that message identity is not party identity.

### Conditional installation impact

`C_install-v2` remains conditional composition evidence only. It models a
bounded consumer that independently installs accepted outputs; it is not an
observed K-Waay consumer, deployed session cloning, or Double Ratchet evidence.

## Validate the frozen artifact

Validate the committed M0–M5 artifact without running a formal prover:

```bash
bash scripts/run-paper-artifact.sh verify-committed
bash artifact/validation/run-tests.sh
```

These commands validate committed tables, Git blobs, provenance, composite
selection, and negative fixtures. Formal reproduction modes require an
explicit repository-external output directory; see the
[artifact contract](artifact/README.md).

## Repository entry points

- [Documentation index](docs/README.md)
- [Current RQ-v2 authority](docs/rq-v2/)
- [Artifact contract](artifact/README.md)
- [M5 completion record](docs/milestones/M5-completion.md)
- [Frozen claim hierarchy](docs/claim-hierarchy.md)
- [Frozen model mapping](docs/model-mapping.md)
- [Frozen threat/compromise matrix](docs/threat-compromise-matrix.md)
- [Relaxed duplicate-input model notes](tamarin/replay/README.md)
- [Milestone records](docs/milestones/)
- [Pre-RQ-v2 historical archive](archive/pre-rq-v2/)

## Scope boundaries

- Dolev–Yao symbolic analysis;
- fixed two-slot scope for the frozen replay, dedup, and combined models;
- exact complete-message identity for the frozen M3 dedup result;
- exploratory fixed-two-slot RQ-v2 admission prototypes, not a deployed-system
  or arbitrary-length theorem;
- no arbitrary-length, global, cross-batch, rollback, or restart theorem;
- no computational proof or complete implementation audit;
- no deployed upper-layer evidence.
