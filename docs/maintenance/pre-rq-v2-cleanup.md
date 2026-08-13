# Pre-RQ-v2 Cleanup

BASE_HEAD: `420515623f97d5c2a4ffb04402e2c8d842278a1f`
DATE: 2026-08-13

This cleanup changes repository navigation and interpretation only. It does not
change any formal result.

## Classification summary

All 1,557 tracked files at `BASE_HEAD` were assigned to an exclusive cleanup
class. Classification is conservative: all models, runners, formal logs,
artifact files, milestone records, and frozen claim sources are protected even
when a path is not one of the 66 rows in `frozen-inputs.tsv`.

| Class | Count | Treatment |
| --- | ---: | --- |
| A. FROZEN_EVIDENCE | 1,497 | kept exactly |
| B. ACTIVE_CURRENT_DOC | 13 | reviewed; rewritten where necessary |
| C. STALE_ACTIVE_DOC | 6 | archived with Git history |
| D. HISTORICAL_DOC | 39 | kept |
| E. LEGACY_INTERNAL_TOOL | 2 | kept in place and marked legacy |
| F. GENERATED_OR_REDUNDANT | 0 | no deletion justified |
| G. UNKNOWN | 0 | none |

`E` counts the two Q1 diagnostic documents. Its `.pv` model and runner are
included in protected class A because model and runner files were globally
protected.

## Rewritten

| Path | Old role | New role | Reason |
| --- | --- | --- | --- |
| `README.md` | M0–M5 duplicate/dedup sequence as current research main line | repository identity and pre-RQ-v2 transition entry | prevents the relaxed duplicate-input witness from being presented as a counterexample to executions satisfying the specification's stated distinct-party precondition or as a deployed attack |
| `docs/README.md` | obsolete tool-stage plan | current documentation index | distinguishes active transition material from frozen M0–M5 authorities and archives |
| `docs/tamarin/README.md` | claimed no formal Tamarin model existed | historical Tamarin documentation index | reflects completed frozen Tamarin work without starting RQ-v2 |
| `docs/cryptoverif/README.md` | prospective next-tool direction | historical prospective direction | prevents it from becoming an accidental RQ-v2 plan |
| `docs/kwaay-tamarin-deniability-review.md` | referenced old stage-summary path | references archived path | repairs the only non-frozen active path affected by archival |
| `tamarin/replay/README.md` | original/unhardened K-Waay replay framing | frozen relaxed duplicate-input model | scopes the witness to violation of the distinct-party admission invariant |
| `tamarin/replay/README-fixed.md` | M3 fixed/repair framing | legacy exact-message dedup hardening | distinguishes exact-message identity from party uniqueness |
| `tamarin/replay/README-hmac-only.md` | HMAC-only duplicate-input bridge | agreement/key-confirmation bridge with interpretation notice | records that HMAC addresses agreement/key confirmation and is not an admission-uniqueness mechanism |
| `tamarin/replay/README-hmac-dedup.md` | combined replay repair | legacy combined regression | prevents it from being read as a future distinct-party admission mechanism |
| `tamarin/impact/README.md` | original-protocol impact framing | conditional impact over relaxed input | preserves `C_install-v2` and removes deployed/original-protocol implication |
| `tamarin/impact/README-fixed.md` | fixed impact/repair framing | conditional legacy exact-message hardening impact | keeps both the message-level and consumer boundaries explicit |
| `tamarin/impact/README-hmac-dedup.md` | combined impact artifact | legacy combined conditional regression | separates HMAC, exact-message dedup, and conditional consumer roles |
| `proverif/variants/hmac-confirmation/README.md` | HMAC variant documentation | agreement/key-confirmation evidence | states that HMAC does not enforce party uniqueness |
| `q1-analysis-model/README.md` | reusable Q1 diagnostic | legacy/internal diagnostic retained in place | preserves runner/log path provenance and removes it from the active main line |

No `.spthy`, `.pv`, runner, result, or evidence file was rewritten.

## Archived

| Old path | New path | Reason |
| --- | --- | --- |
| `docs/K-Waay投稿模型路线图.md` | `archive/pre-rq-v2/docs/K-Waay投稿模型路线图.md` | completed M0–M5 roadmap no longer represents the active research line |
| `docs/roadmap/next-tool-plan.md` | `archive/pre-rq-v2/docs/roadmap/next-tool-plan.md` | superseded prospective tool plan |
| `docs/tamarin/tamarin-model-plan.md` | `archive/pre-rq-v2/docs/tamarin/tamarin-model-plan.md` | superseded pre-model plan |
| `docs/tamarin/tamarin-stage-summary.md` | `archive/pre-rq-v2/docs/tamarin/tamarin-stage-summary.md` | completed historical stage summary |
| `docs/paper/formal-analysis-outline.md` | `archive/pre-rq-v2/docs/paper/formal-analysis-outline.md` | old paper outline tied to the superseded research main line |
| `docs/paper/trace.txt` | `archive/pre-rq-v2/docs/paper/trace.txt` | supporting trace narrative for the old outline |

Before each move, repository references and Git history were checked. None of
these files is in `artifact/manifest/frozen-inputs.tsv`, the artifact contract,
or an active runner. The one non-frozen reference to the old Tamarin stage
summary was updated to its archived path.

## Deleted

None.

`results/logs/env.txt` is unreferenced and not frozen, but it records early
ProVerif environment provenance and has repository history. It was retained as
a historical document. No tracked file satisfied all deletion requirements:
unreferenced, non-frozen, non-evidence, non-reproduction input, and without
historical reasoning value.

## Explicitly preserved frozen evidence

The following remain unchanged:

- all 66 paths in `artifact/manifest/frozen-inputs.tsv`;
- every `.spthy` and `.pv` model, including all replay, impact, V6/V7, HMAC,
  ProVerif, deniability, and Q1 models;
- all runners and artifact validation/generation scripts;
- all committed content under `logs/` and `artifact/`;
- checksums, manifests, raw output, summaries, result tables, and claim-evidence
  mappings;
- `docs/claim-hierarchy.md`, `docs/model-mapping.md`, and
  `docs/threat-compromise-matrix.md`;
- every file under `docs/milestones/`;
- existing archives and historical experimental models.

The final `git diff --name-only`/frozen-manifest intersection must remain empty.

## Legacy but retained in place

- `q1-analysis-model/` remains in place because its runner, RESULTS document,
  and committed logs encode the path. Its README now marks it as a legacy
  internal diagnostic.
- `results/logs/env.txt` remains historical environment provenance.
- older deniability models and their review/results remain in place; this
  cleanup does not reassess or extend them.
- frozen claim sources and milestone records retain historical terminology.
  The active indexes identify them as M0–M5 snapshot authorities only.

## Remaining known semantic debt

- Stage 0 must freeze the exact RQ-v2 research question and the identity-level
  integration invariant.
- The repository still has no public, auditable K-Waay caller/server/batching
  implementation evidence.
- The exact mapping from modeled sender identity `A` to the specification-level
  notion of party, including its relationship to account identity, public keys,
  and message identity, remains a Stage-0 modeling question.
- No distinct-party-precondition comparison model exists yet.
- The `same modeled sender identity A, m1 != m2` distinction has not been
  formally tested.
- `C_install-v2` remains a conditional composition interface rather than an
  observed consumer.
- Frozen historical claim and milestone documents retain their original
  wording by design; future v2 claim documents must not overwrite them.
- Licensing and citation-author metadata remain owner-level release decisions
  recorded by M5.

No item in this section is performed or claimed by this cleanup.

## Validation

Baseline before edits:

```text
git status --short: clean
verify-committed: PASS
```

The complete artifact test suite was also run against `BASE_HEAD` in a clean,
temporary detached worktree:

```text
repository portability checks: PASS
committed actual rows: 405 PASS
negative fixtures: 37/37 PASS
wrapper verify-committed: PASS
wrapper bytecode cleanliness: PASS
artifact_validation: PASS
```

Running `artifact/validation/run-tests.sh` directly in the intentionally dirty
cleanup worktree reaches and passes all portability, generation, committed-
actual, and 37 negative-fixture tests, then exits at its hard-coded
`wrapper_cleanliness` precondition: `wrapper regression requires a clean
repository`. This is an expected validation-interface constraint, not an
artifact mismatch. Final validation temporarily restores a clean checkout for
that wrapper test and then restores the uncommitted cleanup changes.

Final validation procedure:

1. verify `git diff --check`, Markdown links, semantic grep, and the frozen-path
   intersection in the cleanup worktree;
2. save the complete staged/unstaged/untracked cleanup state to a temporary Git
   stash;
3. run both required validation commands against the resulting clean checkout
   at the same `BASE_HEAD`;
4. restore the temporary stash, verify that its object still exists, and drop
   only that exact temporary stash entry;
5. repeat the diff, link, semantic, frozen-intersection, status, and stat checks.

Final validation record:

```text
git diff --check: PASS
Markdown relative links: 15 files checked, 0 broken
active strong-conflict grep: 0 matches
verify-committed: PASS on final clean BASE_HEAD validation
artifact validation tests: PASS; 37/37 negative fixtures and wrapper checks PASS
modified frozen paths: 0
```
