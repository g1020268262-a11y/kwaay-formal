# K-Waay Threat and Compromise Matrix

## 1. Purpose

This document records which threat/compromise cells are supported by an actual
model result. It prevents no-compromise theorems, isolated leak experiments,
and roadmap expectations from being generalized into stronger claims.

Every status cell in the matrices uses exactly one of these terms:

- `proved`
- `falsified`
- `experimentally checked`
- `not modeled`
- `not applicable`
- `unknown`

Interpretation:

- `proved`: a completed universal query/lemma establishes the row property in
  that column's stated scope.
- `falsified`: a completed run gives a counterexample to the row property in
  that scope.
- `experimentally checked`: one or more concrete leak targets were run, but the
  result is not a complete theorem for the whole compromise class.
- `not modeled`: the necessary compromise dimension, event, or protocol variant
  is absent.
- `not applicable`: the compromise dimension does not apply to the stated row
  property or its explicit premise.
- `unknown`: related model structure exists, but no query/lemma decides the
  exact cell.

“No attack found” is never promoted to `proved`. A cell is `proved` only when a
named universal query/lemma completed positively.

## 2. Compromise dimensions

| Dimension | Meaning in this repository |
|---|---|
| no compromise | No ProVerif leak process and no relevant Tamarin compromise event before the target event. |
| sender long-term authentication key compromise | Exposure of A's signature key, represented by `LEAK_SIGSK_A` or `HMAC_LEAK_SIGSK_A`. This is distinct from sender split-KEM state compromise. |
| receiver long-term key compromise | Exposure of B long-term authentication/KEM material. Existing experiments split `LEAK_SIGSK_B` and `LEAK_KEMSK`; they do not form one universal theorem. |
| ephemeral/session material compromise | Exposure of receiver ephemeral KEM state or sender/receiver split-KEM state, represented by selected `LEAK_EKEMSK`, `LEAK_SSKEMSK`, and `LEAK_RSKEMSK` targets. |
| early compromise | Tamarin compromise event strictly before the acceptance/key event. ProVerif leak targets are not ordering-sensitive. |
| late compromise | Tamarin compromise event after the target event, where the lemma permits it. ProVerif leak targets do not distinguish it. |
| receiver state compromise | Exposure of the receiver split-KEM/batch state, distinct from a generic receiver long-term-key label. |

## 3. Main matrix

The property column is part of the row identity. A status never combines
sender secrecy, receiver secrecy, authenticity, and agreement in one cell.

| Protocol variant / artifact | Property | no compromise | sender long-term authentication key compromise | receiver long-term key compromise | ephemeral/session material compromise | early compromise | late compromise | receiver state compromise |
|---|---|---|---|---|---|---|---|---|
| original core | P1 non-injective correspondence | falsified | falsified | falsified | falsified | not modeled | not modeled | falsified |
| original core | P2 injective one-send-one-accept | falsified | not modeled | not modeled | not modeled | not modeled | not modeled | unknown |
| ProVerif final core | P0 sender-key secrecy | proved | experimentally checked | experimentally checked | experimentally checked | not modeled | not modeled | experimentally checked |
| ProVerif final core | P0 receiver-key secrecy | proved | falsified | experimentally checked | experimentally checked | not modeled | not modeled | falsified |
| ProVerif final core | P0 component origin | proved | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| ProVerif final core | P1 non-injective correspondence | falsified | falsified | falsified | falsified | not modeled | not modeled | falsified |
| HMAC confirmation | P0 sender-key secrecy | proved | experimentally checked | unknown | unknown | not modeled | not modeled | unknown |
| HMAC confirmation | P0 receiver-key secrecy | proved | falsified | unknown | unknown | not modeled | not modeled | unknown |
| HMAC confirmation | P0 component origin | proved | unknown | unknown | unknown | not modeled | not modeled | unknown |
| HMAC confirmation | P1 non-injective correspondence | proved | falsified | unknown | unknown | not modeled | not modeled | unknown |
| HMAC confirmation | P2 injective one-send-one-accept | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| Tamarin receiver/batch lifecycle V6 | P0 slot component origin | proved | not modeled | not modeled | not modeled | not applicable | proved | not applicable |
| Tamarin receiver/batch lifecycle V6 | partnered receiver-slot key secrecy | proved | not modeled | not modeled | not modeled | not applicable | proved | not applicable |
| Tamarin receiver/batch lifecycle V6 | attacker-known key exception classification | proved | not modeled | not modeled | not modeled | proved | unknown | proved |
| Tamarin receiver/batch lifecycle V7 | P0 slot component origin in V7 abstraction | proved | not modeled | not modeled | not modeled | unknown | unknown | unknown |
| Tamarin receiver/batch lifecycle V7 | terminal batch lifecycle | proved | not applicable | not applicable | not applicable | unknown | unknown | unknown |
| replay original | P2 injective one-send-one-accept | falsified | not modeled | not modeled | not modeled | unknown | unknown | unknown |
| replay original | no accept after close / single batch end | proved | not applicable | not applicable | not applicable | unknown | unknown | unknown |
| HMAC-only replay bridge | P1 non-injective correspondence | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC-only replay bridge | P2 injective one-send-one-accept | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| impact/composition model | P3 unique session installation | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup model | P2 injective one-send-one-accept | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup impact model | P3 unique session installation | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined model | P0 regression | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined model | P1 non-injective correspondence | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined model | P2 injective one-send-one-accept | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined impact model | P3 unique session installation | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |

## 4. Evidence for `proved` and `falsified` cells

### 4.1 ProVerif final core

Model: `proverif/kwaay_core_final.cpp.pv`

Actual log: `logs/final/proverif/summary.txt`

Named results:

- P0 sender secrecy: `attacker(k) && event(SenderKey(A,B,s,k)) ==> false`,
  `true` in `BASELINE`.
- P0 receiver secrecy: `attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false`,
  `true` in `BASELINE`.
- P0 component origin:
  `SplitKemAccepted(B,A,cts,Ks) ==> SenderSplitKemComponent(A,B,cts,Ks)`,
  `true` in `COMPONENT`.
- P1: `RecvDone(B,A,s,k) ==> SendDone(A,B,s,k)`, `false` in
  `BASELINE` and all currently recorded core leak targets.
- sender signing-key compromise: `LEAK_SIGSK_A` falsifies receiver secrecy;
  `LEAK_SIGSK_B` does not. The backward-compatible `LEAK_SIGSK` target is the
  AB alias and also falsifies receiver secrecy.
- receiver state compromise: `LEAK_RSKEMSK` falsifies receiver secrecy.

The leak cells marked `experimentally checked` remain experiments. For example,
`LEAK_KEMSK` being `true` does not prove security under every receiver
long-term-key compromise, and the mixed `LEAK_EKEMSK`/`LEAK_SSKEMSK`/
`LEAK_RSKEMSK` outcomes do not form one ephemeral-compromise theorem.

### 4.2 HMAC confirmation

Model: `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`

Actual log: `logs/variants/hmac-confirmation/proverif/summary.txt`

Named results:

- `HMAC_BASELINE`: sender secrecy `true`, receiver secrecy `true`, and
  `RecvDone ==> SendDone` `true`.
- `HMAC_COMPONENT`: `SplitKemAccepted ==> SenderSplitKemComponent` `true`.
- `HMAC_LEAK_SIGSK_A`: sender secrecy `true`, receiver secrecy `false`, and
  `RecvDone ==> SendDone` `false`.

No other HMAC compromise case has an actual result.

### 4.3 Tamarin V6 receiver/batch lifecycle

Model: `tamarin/kwaay_splitkem_batch_dynamic_v6.spthy`

Actual log: `logs/tamarin-v6/summary.txt`

Named lemmas:

- `slot_origin_without_early_compromise`: `VERIFIED`.
- `partnered_slot_key_not_attacker_known_without_early_compromise`: `VERIFIED`.
- `slot_key_known_requires_exception`: `VERIFIED`.
- `batch_complete_consumes_state`, `batch_fail_consumes_state`,
  `batch_end_token_single_use`, and `batch_fail_complete_exclusive`: `VERIFIED`.

The first two lemmas exclude early sender/receiver state compromise but permit
later compromise. Their early-compromise cells are `not applicable` because the
claim itself is conditional on its absence. `slot_key_known_requires_exception`
is the separate theorem that classifies early compromise and unpartnered slots.

### 4.4 Tamarin V7 lifecycle

Model: `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`

Actual log: `logs/tamarin-v7/summary.txt`

Named lemmas include:

- `slot_origin`
- `complete_requires_all_slots_done`
- `complete_requires_all_added_slots_processed`
- `no_slot_accept_after_complete`
- `no_slot_accept_after_fail`
- `no_slot_accept_after_close`
- `receiver_state_single_batch_end`

All are `VERIFIED`. V7 is a fixed four-slot terminal-lifecycle model and does
not replace V6's compromise/exception analysis. Therefore V7 compromise cells
without a dedicated lemma remain `unknown` or `not modeled`.

### 4.5 Replay original

Model: `tamarin/replay/kwaay_replay_original.spthy`

Recorded results: `tamarin/replay/README.md`

Named results:

- `one_send_two_accepts_exists`: `verified`.
- `same_message_accepted_at_most_once`: `falsified - found trace`.
- `full_message_unique_send`: `verified`.
- `receiver_accept_has_sender`: `verified`.
- `injective_receiver_accept`: `falsified - found trace`.
- `no_accept_after_close`, `receiver_state_single_batch`, and
  `receiver_state_single_batch_end`: `verified`.

The strengthened existence witness excludes every sender/receiver state
compromise event. It therefore proves a no-compromise P2 counterexample. It does
not decide a trace in which compromise actually occurs, so those cells are not
promoted beyond `unknown`.

## 5. Threat-boundary rules

The matrix enforces the following rules:

1. `BASELINE` and `COMPONENT` are no-compromise theorem targets.
2. `LEAK_*` and `HMAC_LEAK_SIGSK_A` are isolated experiments unless the query
   itself states and proves a complete exception theorem.
3. ProVerif leak targets do not distinguish early from late compromise.
4. V6 state-compromise theorems do not model signature-key or KEM-key compromise.
5. Replay original falsifies P2 without compromise but does not model the HMAC
   bridge, duplicate rejection, or composition impact.
6. Every HMAC-only replay, impact, fixed, and combined cell remains
   `not modeled` until a model exists and the tool actually completes.
7. Roadmap entries labeled “expected” or “must be true” do not change any cell.

## 6. Milestone ownership

| Milestone | Matrix cells it must change |
|---|---|
| M1 | HMAC-only replay P1/P2 no-compromise cells, plus only the explicitly selected compromise cases. |
| M2 | Original impact/composition P3 no-compromise cell and its explicit interface assumptions. |
| M3 | Fixed dedup P2 and fixed-impact P3 cells. |
| M4 | Combined P0 regression, P1, P2, P3, and the selected compromise cells. |
| M5 | Reproducible logs and final expected-versus-actual matrix freeze. |
