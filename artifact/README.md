# K-Waay artifact authority contract

This directory has two authority layers. The current paper research authority
is `docs/rq-v2/`, centered on the necessity of `DistinctPartyPerBatch`. The
RQ-v2 machine-readable overlay is indexed by
`manifest/rqv2-current-authority.tsv` and
`results/rqv2-claim-matrix.tsv`.

The existing M0-M5 paper-mainline manifests and result tables describe frozen
historical artifacts only. Their HMAC, replay, exact-message deduplication, and
combined-variant records remain intact for provenance and reproduction; they
are not the current paper claim authority. Historical labels such as
`paper-mainline` are preserved as frozen record vocabulary and do not override
the RQ-v2 overlay.

## Current RQ-v2 authority

The current research chain is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> conditional upper-layer impact
```

`docs/rq-v2/g2-admission-semantics.md` is the semantic authority for the
identity-level invariant and the R-, M-, and P-semantics comparison.
`docs/rq-v2/prototype-execution-report.md` records the bounded prototype
results and their limitations. Message deduplication is an auxiliary
comparison; HMAC/message-authentication evidence belongs to the frozen M0-M5
history and does not establish party uniqueness.

The RQ-v2 overlay does not mutate, reinterpret, or replace frozen result bytes.
It identifies which documents and supporting prototypes govern current claims.

## Frozen M0-M5 scope and integrity

`manifest/paper-mainline.tsv` separates the historical M0-M5 paper-mainline
inputs and evidence from regression-only support. Optional, historical,
diagnostic, deprecated, and future-work material is outside that frozen
manifest unless an entry explicitly says otherwise.
`manifest/frozen-inputs.tsv` binds every indexed frozen file to a source commit,
Git blob OID, and SHA-256 of the Git blob bytes. Worktree bytes are never the
authoritative checksum source.

Committed evidence under `logs/` is immutable input. New reproductions must use
a new caller-provided output directory and are not committed evidence merely
because a runner completed. `results/expected-results.tsv` is the frozen
cross-artifact expectation contract. Commit A deliberately contains no
`actual-results.tsv`; `scripts/artifact/generate_actual.py` generates that table
from raw evidence. Committed-result rows distinguish model baseline
commit/tree from evidence snapshot commit/tree; new-run rows are accepted only
after the source-run validator has reclassified every result from raw output.
There is no standalone M0 completion record in the frozen
repository, so this contract indexes the V6/V7 models and evidence without
fabricating `M0-completion.md`.

`manifest/property-semantics.tsv` is the explicit, generated
property-to-semantics map. No result is classified from a lemma-name suffix or
from its expected status. `manifest/proverif-targets.tsv` declares the
artifact-wide inherited target set and the independent M4 execution-scope set.
The former contains all 14 original targets plus all three HMAC targets (89
query rows); the latter contains only the five M4 full-mode target groups (20
scope-declaration query rows).

For Tamarin rows, the `expectation_source_*` columns name the historical
milestone authority (V6/V7, M1, M2, M3, or M4 as applicable), while the
separate `regression_matrix_*` columns bind the same property to the complete
296-row M4 canonical matrix. The regression matrix is an independent closeout
check, not a replacement for historical expectation provenance.

## Frozen M0-M5 reproduction entry points

Run `scripts/run-paper-artifact.sh` with one of these modes:

- `verify-committed` (default): validates frozen blobs, schemas, exact
  query/lemma mappings, formula hashes, raw paths, source manifests, M3/M4
  composites, M4 scope, and inherited ProVerif evidence. It runs no prover.
- `list`: prints the supported modes and their reproduction scope.
- `smoke`: a small toolchain/format check, not a full reproduction.
- `paper-core`: runs the selected paper-core direct targets.
- `m4-tamarin`: runs the 296-target Tamarin contract only.
- `full`: runs all direct expected properties; it still keeps M4 ProVerif
  execution rows out of scope.
- `assemble-only`: validates and transparently combines two complete source
  runs using the declared primary/fallback policy. It requires an explicit
  `--mode`, and uses `property_id` as its unique selection key.

Every run mode except `verify-committed` and `list` requires `--output DIR`.
The directory must not exist and must be outside the repository so no tracked
evidence can be overwritten. Target exits and raw output are authoritative;
an older runner's aggregate exit status is never trusted.

Each new source run contains `provenance.txt`, `versions.tsv`,
`target-matrix.tsv`, `aggregate.tsv`, `commands.tsv`, `run-status.txt`,
`raw/**`, `inputs/**`, and a `SHA256SUMS.txt` covering every file except the
manifest itself. Provenance binds the run mode and ID, source HEAD/tree,
contract and expected-results Git blob/SHA-256, target count, UTC interval,
tool-version file, and resource policy. A recorded `VALID` is accepted only
when manifest coverage, the exact mode property set, raw-derived statuses, and
expected matches all revalidate.

The permanent verifier is branch-independent. It requires the frozen base
object and tree, requires that base to be an ancestor of the current checkout,
checks a clean worktree/index by default, validates frozen inputs as
`BASE_COMMIT:path` blobs, and runs the generator stale-check. Review-branch
name, exact Commit A SHA, and single-parent checks are intentionally confined
to the separate review helper and are not release verification conditions.

## Frozen M0-M5 result boundary

M4 is a transparent, Tamarin-only composite over 296 canonical targets. Run 1
is primary and Run 2 is used only for a nonterminal Run 1 target. Run 1 ended
with 294 terminal targets and two OOM events; Run 2 ended with 291 terminal
targets and five timeouts. Neither source run reached 296/296 terminal. The
composite reaches 296/296 terminal and 296/296 expected matches with no
terminal conflict, unresolved target, or mismatch.

M4 did not rerun ProVerif. Its five ProVerif target groups are recorded as
`not_run_out_of_scope` under `tamarin-only`; paper-facing ProVerif claims use
the separately indexed, previously committed original-core and HMAC
confirmation evidence.

## Frozen M0-M5 claim limitations

The models are symbolic and use a fixed two-slot batch. Replay/dedup claims are
for the same `(B,bid,rst)` receiver state and exact base-message identity.
Consumer installation results are conditional on the documented
`C_install-v2` interface. The artifact makes no global, cross-batch, rollback,
restart, arbitrary-length, deployed-system, or computational-security claim.
Allowed and prohibited M0-M5 statements remain authoritative only for
interpreting the frozen historical record in `docs/claim-hierarchy.md`,
`docs/threat-compromise-matrix.md`, and `docs/model-mapping.md`; the historical
claim-evidence table is an index, not a current RQ-v2 claim narrative.
