# M3 legacy exact-message dedup impact model

> **Current interpretation notice.** This is conditional `C_install-v2`
> evidence over the legacy M3 exact-message admission hardening. It does not
> enforce or prove the broader distinct-party-per-`BatchReceive` invariant and
> is not deployed implementation evidence.

[`kwaay_impact_fixed.spthy`](kwaay_impact_fixed.spthy) combines the M3
batch-local pre-scan with the frozen M2 `C_install-v2` composition boundary.
It is a separate theory; the original impact model and its committed evidence
remain unchanged.

The model is frozen in Commit A3. Actual M3 results are recorded in the
transparent composite evidence at `logs/tamarin-m3-closeout/` and in
`docs/milestones/M3-completion.md`.

## Lower-layer exact-message hardening

The lower-layer state flow is the same as the legacy exact-message dedup model:

```text
AddSlot1 -> AddSlot2 -> SealBatch -> DedupPending

duplicate m:
  DuplicateDetected -> BatchFail/BatchClosed/ConsumeReceiverState
  no ReceiverAccept or accepted-output source

distinct m1,m2:
  Neq + DedupPassed -> CheckedSlot1/2 -> ProcessSlot1/2 -> BatchComplete
```

Only `PassDistinctBatch` emits `Neq`; the inequality restriction gives that
explicit comparison event its disequality meaning. Duplicate network input is
not filtered globally and remains executable through the failure branch.

The high-arity `DedupPending` premises in the two decision rules and the
`CheckedSlot1/2` premises in the four processing/failure rules carry
`[no_precomp]`. These are Tamarin search-control annotations only: the rules
still consume the same linear facts at proof time. They prevent fixed-impact
source saturation from expanding the Seal/decision/consumer chain
combinatorially; parse and smoke runs must still reject any wellformedness or
partial-deconstruction warning.

## Unchanged `C_install-v2` consumer

The following M2 interface and consumer rules are retained rather than replaced
by consumer-side deduplication:

```text
AcceptOutputCreated
AcceptedOutput
InstallFromAccept
InstallSession
ConsumerStage0/1/2
ConsumerComplete
```

Each successful `ProcessSlotN` still creates a fresh `aid`, one
`AcceptOutputCreated`, and one linear `AcceptedOutput`. Successful
`CompleteBatch` remains the only producer of `ConsumerStage0`; the fixed model
adds the same-time audit event `ConsumerStarted(B,bid,rst)`. The two installation
rules still consume the two outputs independently, create fresh handles, and
complete the bounded consumer.

The duplicate branch terminates before either `ProcessSlotN`, so it creates no
accepted output and cannot start or complete a consumer. The disappearance of
the duplicate-install witness is therefore attributed to the modeled exact-
message admission boundary, not to removal or weakening of `C_install-v2`.

## Frozen legacy formulas

All 19 M2 composition formulas and all 18 frozen lower-layer formulas are
copied mechanically. They may not be rewritten to match a desired result.

The legacy lemma `normal_consumer_complete` intentionally retains its original
same-`m,sid,k` two-accept/two-install formula. Its actual result is
`falsified` in the fixed model. That result must not be described as failure of
normal distinct-message consumption.

The new `normal_distinct_consumer_complete` separately requires:

```text
two different messages
-> DedupPassed
-> two ReceiverAccept/AcceptOutputCreated occurrences
-> BatchComplete/ConsumerStarted
-> two InstallFromAccept/InstallSession occurrences
-> ConsumerComplete
```

Core fixed-impact actual results are:

```text
one_send_two_accepts_two_installs_exists: falsified
unique_install_within_completed_consumer: verified
normal_consumer_complete:                  falsified
normal_distinct_consumer_complete:         verified
duplicate_batch_has_no_accept_output:      verified
duplicate_batch_has_no_install:            verified
no_consumer_after_failed_batch:            verified
```

The old 37-lemma aggregate count may remain 34 verified / 3 falsified even when
the names change. The runner must compare each lemma by exact name rather than
accepting the aggregate count alone.

## Atomicity and failure scope

`duplicate_batch_has_no_accept_output`, `duplicate_batch_has_no_install`, and
`no_consumer_after_failed_batch` audit the output and consumer boundary.
Batch-local installation properties use the full `InstallFromAccept` event,
because `InstallSession(B,h,A,sid,k)` alone does not carry `bid` or `rst`.

Duplicate atomicity applies only to the `DuplicateDetected` branch. The retained
abstract distinct-message `FailSlot2` can occur after the first accepted output;
the model does not claim that every existing `BatchFail` is output-free.

## Claim boundary

The fixed impact theory can support only a conditional `C_install-v2` statement
about the bounded symbolic consumer. It does not directly prove session-key
secrecy, component origin, HMAC unforgeability, real session cloning behavior,
Double Ratchet behavior, application impact, arbitrary-length batches, or
deployed K-Waay behavior. Existing P0-S/P0-O results require independent
regression runs.

The fixed impact suite has 53/53 expected terminal results in the composite
vector. Evidence is transparent composite evidence assembled from two complete,
manifest-validated A3 runs. Run 1 encountered an intermittent source-saturation
`<<loop>>` at `install_has_prior_accept`; Run 2 verified that lemma in 18 steps
but encountered `<<loop>>` at V6 `executable_seal_batch`. Neither run alone
reached 196/196 terminal, terminal results do not conflict, and the composite
selection does not treat a loop as verified.

The frozen reproduction entry point remains:

```bash
./tamarin/milestones/run-m3-dedup.sh
```

This identifies the A3 runner; it is not a claim that the committed closeout
evidence came from one clean 196/196 successful invocation. M4 separately
records HMAC confirmation combined with this exact-message hardening and its
conditional impact.
