# M3 fixed replay model

[`kwaay_replay_fixed.spthy`](kwaay_replay_fixed.spthy) is the M3 dedup-only
variant of the frozen two-slot original replay model. It does not modify or
replace `kwaay_replay_original.spthy`.

This README belongs to Commit A. All result statuses below are hypotheses until
the reviewed Commit A is run by the formal M3 evidence runner.

## Repair boundary

The repair is deliberately narrow:

```text
scope:          same B, bid, rst
identity:       exact complete public message m
check timing:   after both slots are collected and sealed
                before any successful ProcessSlot
duplicate:      whole-batch failure
distinct:       normal fixed-two-slot processing
```

It is not a global replay cache, cross-batch theorem, arbitrary-length batch
theorem, HMAC+dedup model, or deployed implementation claim.

## Linear decision state

`SealBatch` consumes `OpenStage2`, `AddedSlot1`, and `AddedSlot2`. It produces
one `DedupPending` fact containing both complete slot records and one
`DedupDecisionToken`. It does not produce `SealedStage0`.

The duplicate rule matches the same variable `m` in both collected slots. It
consumes the pending state, decision token, and unique batch-end token, then
emits at one timepoint:

```text
DuplicateDetected
UseDedupDecisionToken
UseBatchEndToken
BatchFail
BatchClosed
ConsumeReceiverState
```

It produces only `ClosedBatch` and `UsedReceiverState`; consequently it cannot
produce `ReceiverAccept`, `BatchComplete`, or any later processing state.

The distinct-pass rule consumes the same pending state and decision token. It
emits `Neq(m1,m2)`, `DedupPassed`, and `UseDedupDecisionToken`, then produces
`CheckedSlot1`, `CheckedSlot2`, and the sole `SealedStage0`.

`ProcessSlot1` consumes only `CheckedSlot1`; `CheckedSlot2` remains available
for `ProcessSlot2`. The existing abstract failure branches consume the
corresponding checked fact:

```text
distinct pass -> FailSlot1
distinct pass -> ProcessSlot1 -> FailSlot2
```

Both paths have dedicated exists-trace smoke lemmas. Duplicate atomicity applies
only to `DuplicateDetected`. The pre-existing abstract `FailSlot2` may still
occur after one successful accept for a distinct batch, so this model does not
claim that every possible `BatchFail` has no partial output.

## Disequality restriction

Only `PassDistinctBatch` emits `Neq`. The restriction

```tamarin
restriction Inequality:
  "All x #i. Neq(x,x) @ #i ==> F"
```

assigns the explicit comparison event its expected meaning. It is not attached
to `ReceiverAccept`, a security lemma, or network input. Exact duplicate input
remains reachable and must take the real `RejectDuplicateBatch` branch. The
restriction does not replace the linear decision state or the duplicate-failure
rule.

## Frozen legacy targets

All 18 formulas from `kwaay_replay_original.spthy` are copied without changes.
In particular, the attack formula, sender-occurrence disambiguation, time
ordering, slot coordinates, and compromise exclusions remain intact.

Commit A hypotheses for the three intended changes are:

```text
one_send_two_accepts_exists          verified  -> falsified
same_message_accepted_at_most_once  falsified -> verified
injective_receiver_accept           falsified -> verified
```

`no_accept_after_close` is a frozen original lemma and is not duplicated as an
M3 lemma.

## M3 proof obligations

The model adds explicit obligations for duplicate-failure reachability,
pre-output detection, no duplicate accept, pass provenance, distinct-pass
soundness, decision single use, outcome exclusivity, distinct success,
continued reachability of both abstract failure paths, fail/complete
exclusivity, and receiver-state consumption.

Universal properties are paired with exists-trace lemmas so a verified result
cannot be interpreted without duplicate-failure and distinct-success
non-vacuity.

## Modeling boundary

The KEM components, transcript identifier, and key remain free symbolic
constructors. Successful reconstruction is still represented by persistent
`HonestSession`. This model has Dolev-Yao network delivery but no direct secrecy
lemma, concrete decapsulation, split-KEM component-origin proof, computational
HMAC property, session database, Double Ratchet, or application action.

