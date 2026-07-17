# M3 fixed impact model

[`kwaay_impact_fixed.spthy`](kwaay_impact_fixed.spthy) combines the M3
batch-local pre-scan with the frozen M2 `C_install-v2` composition boundary.
It is a separate theory; the original impact model and its committed evidence
remain unchanged.

This README belongs to Commit A. Expected statuses are hypotheses, not formal
M3 evidence.

## Lower-layer repair

The lower-layer state flow is the same as the fixed replay model:

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
the duplicate-install witness is therefore attributed to the repaired
BatchReceive boundary, not to removal or weakening of `C_install-v2`.

## Frozen legacy formulas

All 19 M2 composition formulas and all 18 frozen lower-layer formulas are
copied mechanically. They may not be rewritten to match a desired result.

The legacy lemma `normal_consumer_complete` intentionally retains its original
same-`m,sid,k` two-accept/two-install formula. Its Commit A hypothesis is
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

Core fixed-impact hypotheses are:

```text
one_send_two_accepts_two_installs_exists: verified  -> falsified
unique_install_within_completed_consumer: falsified -> verified
normal_consumer_complete:                  verified  -> falsified
normal_distinct_consumer_complete:         new       -> verified
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
