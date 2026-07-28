# K-Waay symbolic formal analysis

This repository contains a symbolic formal analysis of the K-Waay Figure 7
core using ProVerif and Tamarin Prover. It is a collection of scoped protocol
models and reproducible evidence, not a verification of a complete K-Waay
implementation.

## Analysis scope

The ProVerif artifacts cover:

- symbolic session-key secrecy;
- split-KEM component origin;
- exact-parameter non-injective correspondence;
- selected compromise experiments.

The Tamarin artifacts cover:

- receiver and batch-state lifecycle;
- duplicate receiver acceptance and occurrence injectivity;
- conditional installation impact;
- batch-local atomic duplicate rejection;
- the combined HMAC-confirmation and dedup regression.

The repository does not provide an arbitrary-length batch proof, a
computational security proof, or a deployed-code security audit.

## Research main line

```text
Original core
  ↓
HMAC confirmation
  ↓
duplicate acceptance remains
  ↓
conditional duplicate-install impact under C_install-v2
  ↓
batch-local atomic dedup
  ↓
HMAC + dedup combined model
  ↓
M5 reproducible artifact freeze
```

## Core results

For the named no-compromise original ProVerif baseline, P0-S symbolic secrecy
and P0-O component origin are established. The original core's exact-parameter
non-injective P1 correspondence is falsified. In the HMAC-confirmation
no-compromise baseline, the ProVerif P1 correspondence is established, but
confirmation alone does not provide replay prevention or duplicate rejection.

In the fixed two-slot, same-batch and same-receiver-state original replay
model, one sender message can produce two receiver-accept occurrences. Under
the bounded `C_install-v2` consumer, those duplicate accepted outputs can lead
to two symbolic local installation handles. This is a conditional composition
result, not a deployed session-cloning claim.

The fixed repair performs batch-local atomic duplicate rejection before
processing. Within the modeled same `B,bid,rst` scope, an exact duplicate
complete message cannot produce two receiver accepts.

M4 combines HMAC confirmation with that batch-local repair. Its canonical
Tamarin-only matrix contains 296 targets. The transparent composite result is:

```text
terminal:                    296/296
MATCH:                       296/296
verified:                    281
falsified:                   15
selected Run 2 fallbacks:    2
terminal conflicts:          0
unresolved:                  0
mismatches:                  0
```

M4 did not rerun ProVerif. Paper-facing ProVerif conclusions use the previously
committed original-core and HMAC-confirmation evidence.

## Quick artifact validation

Validate the committed artifact contract and evidence without running a formal
prover:

```bash
bash scripts/run-paper-artifact.sh verify-committed
bash artifact/validation/run-tests.sh
```

These commands validate committed result tables, Git blobs, provenance,
composite selection, and negative tamper fixtures. They are not full formal
proof reruns. Both entrypoints should leave the worktree clean and are
configured not to generate Python bytecode.

List the available validation and reproduction modes:

```bash
bash scripts/run-paper-artifact.sh list
```

Modes that execute formal targets require an explicit repository-external
output directory; see [the artifact contract](artifact/README.md).

## Important paths

- [Artifact contract and usage](artifact/README.md)
- [Committed actual results](artifact/results/actual-results.tsv)
- [Paper claim matrix](artifact/results/claim-matrix.tsv)
- [Raw-to-summary provenance](artifact/results/raw-to-summary.tsv)
- [Paper artifact inventory](artifact/manifest/artifact-inventory.tsv)
- [Git-blob SHA-256 manifest](artifact/manifest/git-blob-SHA256SUMS.txt)
- [Claim hierarchy](docs/claim-hierarchy.md)
- [Paper/model mapping](docs/model-mapping.md)
- [Threat and compromise matrix](docs/threat-compromise-matrix.md)
- [Model roadmap](docs/K-Waay投稿模型路线图.md)
- [Milestone records](docs/milestones/)

## Known boundaries

- Dolev-Yao symbolic analysis;
- fixed two-slot scope for the replay, repair, and combined models;
- batch-local, same-`B,bid,rst` duplicate reasoning;
- exact complete-message identity for the frozen dedup result;
- bounded conditional `C_install-v2` consumer interface;
- no deployed upper-layer implementation evidence;
- no arbitrary-length, global, cross-batch, rollback, or restart theorem;
- no computational KEM, KDF, HMAC, signature, or full-protocol proof;
- M4 ProVerif rows are inherited evidence or explicit scope declarations, not
  an M4 ProVerif rerun.

## Project status

M0-M5 implementation and artifact documentation are complete on the
`codex/m5-paper-artifact` review branch. The branch has not yet been merged
into `main`.
