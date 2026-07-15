# HMAC-only two-slot replay bridge

## Objective

[`kwaay_replay_hmac_only.spthy`](kwaay_replay_hmac_only.spthy) connects the
existing no-batch ProVerif HMAC confirmation semantics to the fixed two-slot
Tamarin replay lifecycle. It asks whether one honest confirmed message can be
accepted in two distinct slots of the same batch and receiver state.

This file records only results obtained from the new bridge. It does not change
or reinterpret [`kwaay_replay_original.spthy`](kwaay_replay_original.spthy).

## Exact confirmation semantics

The sender constructs:

```text
m   = <ct_l,ct_k,ct_s>
sid = session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)
k   = session_key(K_l,K_k,K_s,sid)
tag = hmac(confirm_key(k),sid)
cm  = <m,tag>
```

`confirm_key/1` and `hmac/2` are public symbolic constructors. The session key
is not published. The sender publishes `Out(<A,B,cm>)`; no separate `Out(sid)`
is added. `cm` is ordinary public Dolev-Yao data, so the network can retain one
term and supply it independently to `AddSlot1` and `AddSlot2`.

The tag does not contain `bid`, `idx`, `rst`, a delivery nonce, a receiver-local
challenge, an accept identifier, deduplication state, or an installation
handle. The model contains no `SeenSid`, `SeenMessage`, replay cache, duplicate
rejection, linear confirmation token, or one-time message token.

## HMAC-gated receiver event

The protocol events are:

```text
ConfirmedSend(A,B,m,sid,k,tag)
ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)
```

The matching coordinates are `(A,B,m,sid,k,tag)`. The receiver occurrence
context is `(bid,idx,rst)` and is not added to `sid` or `tag`.

Each `ProcessSlotN` rule requires both:

```text
AddedSlotN(...,<m,hmac(confirm_key(k),sid)>)
!HonestSession(A,B,rst,m,sid,k)
```

The term match is the symbolic HMAC check. `ConfirmedReceiverAccept` is emitted
only by that rule after its premises match; there is no separate verification
event and no accept event before the check.

## Sender-occurrence disambiguation

Sender occurrences are identified by the timepoint of `ConfirmedSend`. The
matching relation is tuple-based, so tuple equality is not assumed to be
occurrence equality. The separate lemma `confirmed_message_unique_send` must
verify that two sender events with the same complete tuple
`(A,B,m,sid,k,tag)` have the same timepoint. The receiver-injectivity lemmas use
receiver timepoint equality, not slot-index equality.

## HonestSession boundary

`!HonestSession(A,B,rst,m,sid,k)` remains the successful-decapsulation/session-
reconstruction abstraction inherited from the original replay model:

1. the sender rule creates it;
2. receiver processing requires it;
3. matching-existence therefore largely checks the source and event mapping of
   that abstraction;
4. the bridge's primary target is replay and receiver occurrence injectivity;
5. it does not replace the ProVerif `HMAC_BASELINE` evidence for no-batch P1;
6. it does not prove concrete KEM, signature, KDF, or HMAC computational
   security.

## Scope

The model is a no-compromise baseline. Original sender/receiver-state
compromise rules are retained for structural compatibility, but the replay
witness excludes every `CompromiseReceiverState` and `CompromiseSenderState`
event. No other HMAC compromise material is modeled.

The batch is fixed to exactly two slots. Positive lifecycle results are scoped
to this bounded model. The occurrence-injectivity property is explicitly
same-batch/same-receiver-state; a positive result would not be an
arbitrary-batch or global theorem.

## Run

From the repository root inside an environment containing Tamarin and Maude:

```bash
PATH=/home/linuxbrew/.linuxbrew/bin:/usr/bin:/bin \
bash tamarin/replay/run-hmac-only.sh
```

The runner writes only to:

```text
logs/tamarin-replay-hmac-only/command.txt
logs/tamarin-replay-hmac-only/versions.txt
logs/tamarin-replay-hmac-only/parse.out
logs/tamarin-replay-hmac-only/raw.out
logs/tamarin-replay-hmac-only/summary.txt
logs/tamarin-replay-hmac-only/attack-trace.out
logs/tamarin-replay-hmac-only/attack-trace.json
logs/tamarin-replay-hmac-only/attack-trace.dot
```

## Result interpretation

The complete run on Tamarin 1.12.0 with Maude 3.5.1 parsed successfully and
finished without a timeout. The commit-bound proof run took 52.75 seconds.

| Lemma | Result | Steps |
| --- | --- | ---: |
| `normal_confirmed_single_accept` | verified | 12 |
| `normal_confirmed_batch_complete` | verified | 18 |
| `confirmed_receiver_accept_has_sender` | verified | 16 |
| `confirmed_message_unique_send` | verified | 2 |
| `one_confirmed_send_two_accepts_exists` | verified | 17 |
| `confirmed_message_accepted_at_most_once` | falsified, trace found | 15 |
| `injective_confirmed_receiver_accept` | falsified, trace found | 15 |
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

The exported witness contains exactly one matching `ConfirmedSend`, followed
by two receiver accepts at distinct timepoints and with distinct slot indices.
Both accepts have the same `(A,B,bid,rst,m,sid,k,tag)` coordinates, both precede
`CompleteBatch`, and the trace has no receiver-state or sender-state compromise
event. Its public slot inputs contain the same exact
`<m,hmac(confirm_key(k),sid)>` term. This is the intended HMAC-only replay
bridge: matching-existence/order holds within the `HonestSession` abstraction,
while receiver-occurrence injectivity does not. This matching result is not a
new split-KEM component-origin theorem and does not replace the ProVerif HMAC
P1 proof.

The evidence is retained in:

- [`summary.txt`](../../logs/tamarin-replay-hmac-only/summary.txt) and
  [`raw.out`](../../logs/tamarin-replay-hmac-only/raw.out) for the complete run;
- [`attack-trace.json`](../../logs/tamarin-replay-hmac-only/attack-trace.json),
  [`attack-trace.dot`](../../logs/tamarin-replay-hmac-only/attack-trace.dot), and
  [`attack-trace.out`](../../logs/tamarin-replay-hmac-only/attack-trace.out) for
  the exported witness;
- [`original-regression-summary.txt`](../../logs/tamarin-replay-hmac-only/original-regression-summary.txt)
  for the unchanged original replay-model regression;
- [`hmac-baseline-regression-summary.txt`](../../logs/tamarin-replay-hmac-only/hmac-baseline-regression-summary.txt)
  for the unchanged ProVerif `HMAC_BASELINE` regression.

The original replay model reproduced its committed result profile. The
ProVerif baseline also remained `STATUS: OK`: honest reachability was retained,
receiver-to-sender and both prekey correspondences were true, and both key
secrecy queries were true.

## Claim boundary

The result supports the following narrowly scoped statement: in this fixed
two-slot symbolic bridge, one honestly constructed HMAC-confirmed message can
be supplied to two slots of the same batch and receiver state, pass the same
HMAC gate twice, produce two distinct receiver-accept occurrences, and still
allow the batch to complete, without a modeled state compromise.

It does not establish a secrecy failure, an HMAC forgery, computational HMAC or
KEM insecurity, arbitrary-batch replay, a deployed-system exploit, or a result
outside the `HonestSession` abstraction. It does not replace the no-batch
ProVerif baseline or show how a concrete receiver reconstructs and installs the
session state.

## Reproducibility notes

The logs record the exact commands, evidence commit, branch, model SHA-256,
runner SHA-256, pre-run and post-run status, evidence-file hashes, and tool
versions. The runner refuses to start unless the pre-run worktree is clean;
post-run changes are the regenerated evidence. ProVerif 2.05 does not accept
`-version`, so its diagnostic and banner are retained verbatim in
`versions.txt`.

- An attack witness is evidence only for the exact fixed-two-slot,
  same-batch/same-state formula.
- A falsified universal injectivity lemma is a counterexample, not a secrecy or
  forgery result.
- A timeout is unknown.
- If normal executability fails, universal results may be vacuous.
- A matching-existence result remains subject to the `HonestSession` boundary
  above.
