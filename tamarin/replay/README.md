# Original BatchReceive duplicate-input model

## Model objective

[`kwaay_replay_original.spthy`](kwaay_replay_original.spthy) checks whether the
original, unhardened K-Waay Figure 7 `BatchReceive` behavior can accept one
complete honest message in two different slots of the same batch, while using
the same receiver state.

The model deliberately contains no `SeenSid`, replay cache, duplicate
rejection, HMAC/key confirmation, session installation, Double Ratchet,
application state, resource counter, or protocol repair.

## Relationship to the existing models

The model reuses the first two slots of the fixed linear lifecycle from
`tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`. Two slots are the smallest
bounded batch that can expose the target behavior:

```text
OpenStage0 -> AddSlot1 -> OpenStage1 -> AddSlot2 -> OpenStage2
           -> SealBatch -> SealedStage0
           -> ProcessSlot1 -> SealedStage1 -> ProcessSlot2 -> SealedStage2
           -> CompleteBatch
```

As in V7, `CreateBatch` consumes one linear `ReceiverState(B,rst)`. Both slots
carry the same `bid,rst`; `CompleteBatch` or an abstract `FailSlotN`
consumes the unique `BatchEndToken` and records `ConsumeReceiverState`. This
prevents the target trace from depending on cross-batch state reuse, a second
call after close, rollback, or duplicated linear state.

Unlike V7's component-only abstraction, this model imports the complete-message
shape and transcript/key construction from the ProVerif core:

```text
m   = <ct_l,ct_k,ct_s>
sid = session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)
k   = session_key(K_l,K_k,K_s,sid)
```

`SenderSession(A,B,m,sid,k)` records the one honest send.
`ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` records a successful receiver output
and additionally exposes `rst` so same-state replay is stated directly.

## Attack represented

The intended trace is:

1. `A` performs one honest sender execution and publishes the complete message
   `m`.
2. The Dolev-Yao network retains that unchanged public `m`.
3. `B` opens one batch with one linear receiver state `rst`.
4. The network supplies the same `m` to two fresh, distinct slots of that batch.
5. After sealing, both slots use the same `bid,rst` and the same honest-session
   relation to output equal `sid,k` values.
6. Thus one `SenderSession` corresponds to two `ReceiverAccept` events.

This is duplicate input within one batch. It is not cross-batch replay, state
reuse after completion, rollback, compromise, forged ciphertext/signature, or
two deliberate sends by `A`.

## Verification environment and command

The final model was checked with:

```text
Tamarin Prover 1.12.0
Maude 3.5.1
WSL 2 / Ubuntu 24.04
```

Command from the repository root:

```bash
tamarin-prover --prove tamarin/replay/kwaay_replay_original.spthy
```

On this machine the Homebrew binaries were invoked through the existing WSL
installation with `/home/linuxbrew/.linuxbrew/bin` on `PATH`. Tamarin reported
22.76 seconds of processing time. No manual oracle was used. Every lemma
terminated, and both counterexample traces were found automatically.

## Actual results

| Lemma | Result | Steps |
|---|---:|---:|
| `normal_single_accept` | verified | 11 |
| `normal_batch_complete` | verified | 16 |
| `one_send_two_accepts_exists` | verified | 15 |
| `same_message_accepted_at_most_once` | falsified, trace found | 13 |
| `full_message_unique_send` | verified | 2 |
| `receiver_accept_has_sender` | verified | 16 |
| `injective_receiver_accept` | falsified, trace found | 16 |
| `slot_indices_distinct` | verified | 1 |
| `process_requires_slot_added` | verified | 12 |
| `process_requires_seal` | verified | 8 |
| `complete_requires_all_slots_processed` | verified | 18 |
| `no_add_after_seal` | verified | 16 |
| `no_accept_after_close` | verified | 68 |
| `batch_complete_consumes_state` | verified | 2 |
| `batch_fail_consumes_state` | verified | 4 |
| `batch_end_token_single_use` | verified | 98 |
| `receiver_state_single_batch` | verified | 24 |
| `receiver_state_single_batch_end` | verified | 218 |

The strengthened `one_send_two_accepts_exists` witness also requires:

- the batch to complete after both accepts;
- every matching `SenderSession` to be the same sender event;
- no `CompromiseReceiverState` event anywhere in the trace;
- no `CompromiseSenderState` event anywhere in the trace.

The automatic proof selects `SenderCreatesMessage`, reuses its public output in
`AddSlot1` and `AddSlot2`, then follows `SealBatch`, `ProcessSlot1`,
`ProcessSlot2`, and `CompleteBatch`. Both accepts therefore share the same
`B,bid,rst,A,m,sid,k` and differ only in their fresh slot indices.

## Modeling approximations

- The batch is bounded to exactly two slots. This is sufficient for the
  duplicate-entry question but is not an arbitrary-length vector traversal.
- The three KEM components, their shared secrets, transcript identifier, and
  KDF are free symbolic constructors. Concrete algorithms and computational
  assumptions are outside this model.
- Successful decapsulation is represented by the persistent
  `HonestSession(A,B,rst,m,sid,k)` relation created by the sender. The model does
  not encode concrete decapsulation failure or signature verification.
- Slots are added and processed in fixed order, following the tractable V7
  linear-stage style. The fresh indices remain distinct symbolic values.
- Compromise events are retained from V7 for scope compatibility, but they do
  not create a `ReceiverAccept`; the replay witness explicitly excludes them.

## Interpretation boundary

The target result concerns duplicate successful outputs, equivalently
non-injective batch acceptance. It does not by itself prove loss of secrecy,
sender forgery, concrete implementation session cloning, Double Ratchet
failure, or an exploitable vulnerability in a deployed K-Waay implementation.
Those questions belong to a later impact/composition model.

For a later impact model, the reusable interface should remain
`SenderSession`, `ReceiverAccept`, `BatchCreated`, `SlotAdded`,
`SlotProcessed`, `BatchComplete`, `ConsumeReceiverState`, and the shared
`bid,rst,m,sid,k` coordinates. An impact extension can connect duplicate
`ReceiverAccept` events to session installation or application effects without
changing this original-protocol replay model.
