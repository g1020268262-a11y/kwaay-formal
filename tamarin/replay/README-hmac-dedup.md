# M4 legacy combined regression: HMAC confirmation and exact-message dedup

> **Current interpretation notice.** This frozen artifact is retained as a
> legacy combined regression. HMAC supplies agreement/key-confirmation
> semantics; the dedup component supplies exact-complete-message admission
> hardening. Neither component, alone or in combination here, establishes the
> K-Waay distinct-party-per-`BatchReceive` invariant.

This artifact is the fixed two-slot Commit A model for the M4 combination.  It
uses `kwaay_replay_hmac_only.spthy` as the confirmed-event/HMAC vocabulary and
ports the sealed, batch-local, single-use dedup decision from
`kwaay_replay_fixed.spthy`.

## Scope and message shape

```text
m   = <ct_l,ct_k,ct_s>
sid = session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)
k   = session_key(K_l,K_k,K_s,sid)
tag = hmac(confirm_key(k),sid)
cm  = <m,tag>
```

The only lower-layer sender/receiver events are:

```text
ConfirmedSend(A,B,m,sid,k,tag)
ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)
```

The theory does not produce `SenderSession` or `ReceiverAccept` aliases.

## Parser boundary

`AddSlot1/2` accept only `In(<A,B,<m,tag>>)` and store `m` and `tag` in
separate linear fact fields.  A malformed non-pair network term remains at the
parser boundary and does not enter a batch.  The generic `FailSlot1/2` rules
represent other abstract processing failures *after* a wrapper has parsed.
This artifact does not prove that every malformed wrapper causes `BatchFail`.
That is an explicit narrowing relative to the HMAC-only bridge, whose slot
collection used a generic `cm` variable.

## Dedup decision

The scope is one `(B,bid,rst)`.  Identity is the exact complete base message
`m`, not `<m,tag>`, `tag`, `sid`, `(m,sid)`, `(m,tag)`, `idx`, or a global
seen-message state.

After both wrappers are collected, `SealBatch` consumes the two `AddedSlot`
facts and creates one `DedupPending` plus one linear
`DedupDecisionToken`. Equal base messages take `RejectDuplicateBatch`, which
atomically emits `DuplicateDetected`, consumes both decision/end tokens, and
emits `BatchFail`, `BatchClosed`, and `ConsumeReceiverState` before any slot
processing. Distinct messages take the sole `Neq`-emitting rule,
`PassDistinctBatch`, and become `CheckedSlot1/2`.

## HMAC success and failures

A successful slot must match a persistent
`HonestSession(A,B,rst,m,sid,k)` and the exact term
`hmac(confirm_key(k),sid)`. `HmacValidated` and
`ConfirmedReceiverAccept` are emitted in the same transition.

Explicit tag mismatch is deliberately a two-transition path:

```text
TagMismatch + HmacValidationFailed
  -> HmacRejectPendingSlotN
  -> BatchFail/BatchClosed/ConsumeReceiverState
```

This establishes `HmacValidationFailed < BatchFail`. Generic `FailSlot1/2`
remain possible. Therefore an invalid tag may take an explicit mismatch path
or a generic abstract-failure path. The model proves that an invalid tag cannot
produce a successful confirmed accept and that explicit mismatch paths are
reachable; it does not claim that every invalid tag necessarily emits
`HmacValidationFailed`.

Slot-2 failure may occur after slot 1 has been validated and accepted. The
duplicate branch is atomic and output-free, but the model does not claim that
all `BatchFail` traces have no partial lower-layer output.

## Formula inventory and expected contract

The theory contains exactly 38 uniquely named lemmas. The frozen expected map
is declared in `tamarin/milestones/run-m4-hmac-dedup.sh`. Key expectations are:

```text
one_confirmed_send_two_accepts_exists                         falsified
confirmed_message_accepted_at_most_once                      verified
confirmed_base_message_accepted_at_most_once                 verified
injective_confirmed_receiver_accept                          verified
duplicate_same_base_different_tag_fail_exists                verified
normal_two_distinct_valid_confirmed_accepts_complete         verified
hmac_failure_slot1_exists                                    verified
hmac_failure_slot2_after_prior_accept_replay_exists          verified
```

These were Commit A expected statuses at model-freeze time. Formal evidence was
later generated in Evidence Commit B
`740666a3abd6937b52818d0f4acaf8ea0d023c58` under
`logs/tamarin-m4-hmac-dedup/`.

## Evidence Commit B

M4 replay is included in the Tamarin-only evidence scope:

```text
evidence_scope=tamarin-only
canonical_target_count=296
proverif_targets=not_run_out_of_scope
composite terminal=296/296
composite MATCH=296/296
terminal_conflicts=0
unresolved=0
mismatches=0
```

The two source runs are both complete `VALID` invocations. Run 1 has two
combined-impact OOM nonterminals, both verified by Run 2. Run 2 has five
combined-impact timeout nonterminals, all already terminal in Run 1. No single
source run is described as 296/296 terminal; that is the transparent composite
result.

Reproduction entry points:

```bash
bash tamarin/milestones/run-m4-hmac-dedup.sh --tamarin-only --static-only
bash tamarin/milestones/run-m4-hmac-dedup.sh --tamarin-only --source-run 1
bash tamarin/milestones/run-m4-hmac-dedup.sh --tamarin-only --source-run 2
bash tamarin/milestones/run-m4-hmac-dedup.sh --tamarin-only --assemble-composite
```

The full 301-target mode also exists in the runner, but Evidence Commit B is
not a full 301-target run. It does not rerun ProVerif.

## Limitations

- fixed two-slot batch only;
- batch-local, not cross-batch/global replay protection;
- no rollback/restart theorem;
- Dolev--Yao/free-constructor abstraction, not computational security;
- `HonestSession` remains the successful reconstruction abstraction;
- no independent key-material compromise theory;
- no deployed implementation or arbitrary-length batch claim;
- ProVerif original/HMAC claims are inherited from prior committed evidence,
  not rerun in this M4 Tamarin-only evidence round.
