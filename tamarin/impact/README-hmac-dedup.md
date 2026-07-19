# M4 combined impact: confirmed outputs under C_install-v2

This theory derives the M4 impact model from the combined replay model and
adds the frozen bounded `C_install-v2` consumer. It keeps only the lower-layer
events `ConfirmedSend` and `ConfirmedReceiverAccept`; it does not emit
`SenderSession` or `ReceiverAccept` aliases.

## Tag-free consumer interface

HMAC validation is discharged at the lower-layer acceptance transition. The
consumer interface deliberately remains tag-free:

```text
AcceptOutputCreated(aid,B,A,bid,idx,rst,m,sid,k)
AcceptedOutput(aid,B,A,bid,idx,rst,m,sid,k)
InstallFromAccept(aid,B,h,A,bid,idx,rst,m,sid,k)
InstallSession(B,h,A,sid,k)
```

Every `AcceptOutputCreated` must have, at the same timepoint, a matching
`ConfirmedReceiverAccept(...,tag)` and `HmacValidated(...,tag)`. This is the
complete source bridge between the confirmed lower layer and the tag-free
consumer.

The following three rules are copied from `kwaay_impact_fixed.spthy` without
fact, annotation, or token changes:

```text
InstallAcceptedOutputFirst
InstallAcceptedOutputSecond
CompleteConsumer
```

Whitespace, indentation, and comments are the only permitted normalized
differences. In particular, `[no_precomp]` is not treated as formatting.

## Conditional boundary

`C_install-v2` remains an explicit bounded composition assumption. It is not a
claim that deployed K-Waay independently installs every successful batch
output. The model has two linear accepted-output tokens, installs them using
fresh symbolic handles, and completes only after both tokens are installed.

`normal_one_confirmed_accept_one_install` proves that at least one confirmed
output is installed within a completed two-output consumer. It does not mean
that the consumer received only one output; the second output is part of the
existential execution context even though the formula names only one source.

`legacy_same_confirmed_message_consumer_complete_exists` mechanically retains
the old same-message/two-output witness and is expected to be falsified after
dedup. Normal consumer non-vacuity is instead established by
`normal_two_distinct_valid_confirmed_outputs_consumer_complete`.

## Failure and partial output

Duplicate input fails before any accept/output/install. A slot-2 explicit HMAC
mismatch may follow a valid slot-1 `HmacValidated`,
`ConfirmedReceiverAccept`, `AcceptOutputCreated`, and `AcceptedOutput`.
Nevertheless, the failed batch has no `BatchComplete` or `ConsumerStarted`, so
its output token cannot reach `InstallFromAccept` or `ConsumerComplete`.

The model does not assert that every invalid tag emits
`HmacValidationFailed`, and it does not prohibit unrelated
`InstallSession` events whose event signature has no `bid/rst` coordinates.
Batch-scoped absence is stated through `InstallFromAccept`, together with
`install_session_has_interface_origin`, `install_from_accept_has_session`, and
`no_consumer_after_failed_batch`.

## Formula inventory and expected contract

The theory contains exactly 62 uniquely named lemmas: 38 combined lower-layer
properties, 19 mechanically mapped composition properties, and 5 impact-only
properties. Key expectations include:

```text
one_confirmed_send_two_accepts_two_installs_exists           falsified
unique_install_within_completed_consumer                    verified
legacy_same_confirmed_message_consumer_complete_exists      falsified
normal_two_distinct_valid_confirmed_outputs_consumer_complete verified
hmac_failure_slot2_after_prior_accept_exists                verified
duplicate_batch_has_no_accept_output                        verified
duplicate_batch_has_no_install                              verified
no_consumer_after_failed_batch                              verified
```

These are Commit A expected statuses only. No M4 proofs, regressions, ProVerif
suite, or formal evidence directory was produced during Commit A.
