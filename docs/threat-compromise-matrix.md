# K-Waay Threat and Compromise Matrix

## 1. Purpose and status vocabulary

This document freezes the repository's current threat/compromise evidence
without turning isolated experiments into general compromise theorems. A row
always names one exact artifact and one exact property.

Every matrix status cell uses exactly one of:

- `proved`
- `falsified`
- `experimentally checked`
- `not modeled`
- `not applicable`
- `unknown`

`proved` requires a completed universal query/lemma for the exact cell.
`falsified` requires a completed counterexample or verified attack witness.
`experimentally checked` records a concrete target whose direction is given
separately in the experiment ledger. `unknown` means related structure exists
but no result decides the exact cell. “No attack found” is not `proved`.

## 2. Orthogonal compromise dimensions

### 2.1 Material

| Material | Repository representation |
|---|---|
| sender authentication key | A's signature key; core `LEAK_SIGSK_A`, HMAC `HMAC_LEAK_SIGSK_A` |
| receiver authentication key | B's signature key; core `LEAK_SIGSK_B` |
| receiver long-term KEM key | B's long-term KEM secret; core `LEAK_KEMSK` |
| receiver ephemeral KEM state | B's ephemeral KEM secret/state; core `LEAK_EKEMSK` |
| sender split-KEM state | sender split-KEM state; core `LEAK_SSKEMSK`, Tamarin `CompromiseSenderState` |
| receiver split-KEM state | receiver split-KEM/batch state; core `LEAK_RSKEMSK`, Tamarin `CompromiseReceiverState` |

Combined targets such as `LEAK_SIGSK_AB`,
`LEAK_KEMSK_EKEMSK`, and `LEAK_ALL_RECEIVER_SECRETS` are recorded as
their exact combinations in the experiment ledger. They are not promoted to a
theorem for any individual material class.

### 2.2 Timing

| Timing class | Meaning |
|---|---|
| no compromise anywhere | The target/model excludes every relevant compromise event throughout the witness, or contains no leak/compromise process at all. |
| no early compromise, later compromise permitted | The formula excludes compromise only before the target event. It does not require a later compromise to occur. |
| compromise before target event | A relevant compromise occurrence is ordered strictly before the target event. |
| compromise after target event | A relevant compromise occurrence is ordered strictly after the target event. |
| timing not represented | The model exposes material without an event-order claim. This is the case for the concurrent ProVerif leak processes. |

“No compromise before the target” must never be described as “no compromise
anywhere.” A theorem that syntactically permits later compromise is not a
dedicated late-compromise reachability result.

## 3. Material coverage matrix

The direction of every `experimentally checked` cell appears in section 5.

| Exact artifact | Exact property | sender authentication key | receiver authentication key | receiver long-term KEM key | receiver ephemeral KEM state | sender split-KEM state | receiver split-KEM state |
|---|---|---|---|---|---|---|---|
| ProVerif final core — original Figure-7 no-batch abstraction | P0-S sender-key secrecy | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked |
| ProVerif final core — original Figure-7 no-batch abstraction | P0-S receiver-key secrecy | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked |
| ProVerif final core — original Figure-7 no-batch abstraction | P0-O component origin | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| ProVerif final core — original Figure-7 no-batch abstraction | P1 `RecvDone ==> SendDone` | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked | experimentally checked |
| ProVerif HMAC confirmation — no-batch abstraction | P0-S sender-key secrecy | experimentally checked | not modeled | not modeled | not modeled | not modeled | not modeled |
| ProVerif HMAC confirmation — no-batch abstraction | P0-S receiver-key secrecy | experimentally checked | not modeled | not modeled | not modeled | not modeled | not modeled |
| ProVerif HMAC confirmation — no-batch abstraction | P0-O component origin | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| ProVerif HMAC confirmation — no-batch abstraction | P1 `RecvDone ==> SendDone` | experimentally checked | not modeled | not modeled | not modeled | not modeled | not modeled |
| Tamarin receiver/batch lifecycle V6 | P0-O `slot_origin_without_early_compromise` | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| Tamarin receiver/batch lifecycle V6 | partnered key secrecy `partnered_slot_key_not_attacker_known_without_early_compromise` | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| Tamarin receiver/batch lifecycle V6 | `slot_key_known_requires_exception` branch reachability | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| Tamarin receiver/batch lifecycle V7 | P0-O `slot_origin` | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| Tamarin replay original — fixed two-slot replay abstraction | P2 one-send-one-accept | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| HMAC-only replay bridge | P2 occurrence injectivity | not modeled | not modeled | not modeled | not modeled | unknown | unknown |
| impact/composition model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup model | P2 | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup impact model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined model | P0-S/P0-O/P1/P2 | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined impact model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled | not modeled |

The V6 universal exception classification is verified as a whole:
attacker-known receiver keys require an unpartnered slot or an early
sender/receiver state-compromise explanation. The material cells remain
`unknown` because neither individual compromise disjunct has an independently
checked reachability trace.

## 4. Timing coverage matrix

| Exact artifact | Exact property | no compromise anywhere | no early compromise, later compromise permitted | compromise before target event | compromise after target event | timing not represented |
|---|---|---|---|---|---|---|
| ProVerif final core — original Figure-7 no-batch abstraction | P0-S baseline secrecy | proved | not modeled | not modeled | not modeled | experimentally checked |
| ProVerif final core — original Figure-7 no-batch abstraction | P0-O component origin | proved | not modeled | not modeled | not modeled | not modeled |
| ProVerif final core — original Figure-7 no-batch abstraction | P1 `RecvDone ==> SendDone` | falsified | not modeled | not modeled | not modeled | experimentally checked |
| ProVerif HMAC confirmation — no-batch abstraction | P0-S baseline secrecy | proved | not modeled | not modeled | not modeled | experimentally checked |
| ProVerif HMAC confirmation — no-batch abstraction | P0-O component origin | proved | not modeled | not modeled | not modeled | not modeled |
| ProVerif HMAC confirmation — no-batch abstraction | P1 `RecvDone ==> SendDone` | proved | not modeled | not modeled | not modeled | experimentally checked |
| Tamarin receiver/batch lifecycle V6 | P0-O `slot_origin_without_early_compromise` | proved | proved | not applicable | unknown | not applicable |
| Tamarin receiver/batch lifecycle V6 | partnered key secrecy `partnered_slot_key_not_attacker_known_without_early_compromise` | proved | proved | not applicable | unknown | not applicable |
| Tamarin receiver/batch lifecycle V6 | `slot_key_known_requires_exception` branch reachability | unknown | unknown | unknown | unknown | not applicable |
| Tamarin receiver/batch lifecycle V7 | P0-O `slot_origin` | proved | unknown | unknown | unknown | not applicable |
| Tamarin receiver/batch lifecycle V7 | terminal lifecycle | proved | unknown | unknown | unknown | not applicable |
| Tamarin replay original — fixed two-slot replay abstraction | P2 one-send-one-accept | falsified | falsified | unknown | unknown | not applicable |
| Tamarin replay original — fixed two-slot replay abstraction | terminal lifecycle | proved | unknown | unknown | unknown | not applicable |
| HMAC-only replay bridge | matching existence/order | proved | proved | unknown | unknown | not applicable |
| HMAC-only replay bridge | P2 occurrence injectivity | falsified | falsified | unknown | unknown | not applicable |
| HMAC-only replay bridge | terminal lifecycle | proved | unknown | unknown | unknown | not applicable |
| impact/composition model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup model | P2 | not modeled | not modeled | not modeled | not modeled | not modeled |
| fixed dedup impact model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined model | P0-S/P0-O/P1/P2 | not modeled | not modeled | not modeled | not modeled | not modeled |
| HMAC+dedup combined impact model | P3 under `C_install` | not modeled | not modeled | not modeled | not modeled | not modeled |

For the two V6 “without early compromise” lemmas, `proved` in the second
timing column means only “exclude early compromise and permit later compromise
syntactically.” The `unknown` after-target cells record that no dedicated
late-compromise exists-trace was checked.

The original and HMAC-only replay P2 counterexamples both exclude
`CompromiseReceiverState` and `CompromiseSenderState` everywhere. They
therefore falsify P2 in the no-compromise subset as well as the broader class
that merely permits later compromise; neither shows a trace in which later
compromise actually occurs. The HMAC bridge has no independent result for
authentication-key, KEM-material, or computational HMAC compromise.

## 5. Experiment-direction ledger

The core leak processes run concurrently with protocol sessions. Their timing
capability is therefore always `timing not represented`.

| Exact artifact and target | Exact property/query | Material | Timing capability | Direction | Baseline status | Is compromise required for the counterexample? | Evidence |
|---|---|---|---|---|---|---|---|
| ProVerif final core — `RECEIVER_EXCEPTION_CLASSIFICATION` | P0-S sender and receiver secrecy | sender + receiver split-KEM state classification target | timing not represented | mixed: sender held; receiver failed | both held | receiver failure: not established; baseline held | `logs/final/proverif/summary.txt` |
| ProVerif final core — `EXCEPTION_CHOICE` | P0-S sender/receiver secrecy; P1; sender exception query | receiver long-term KEM + receiver ephemeral KEM + receiver split-KEM state | timing not represented | mixed: both secrecy queries failed; P1 failed; exception query held | secrecy held; P1 falsified | P1: no; secrecy failures: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_SIGSK_A` | P0-S sender/receiver secrecy; P1 | sender authentication key | timing not represented | mixed: sender held; receiver failed; P1 failed | secrecy held; P1 falsified | P1: no; receiver secrecy: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_SIGSK_B` | P0-S sender/receiver secrecy; P1 | receiver authentication key | timing not represented | mixed: both secrecy queries held; P1 failed | secrecy held; P1 falsified | P1: no; no secrecy counterexample | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_SIGSK_AB` | P0-S sender/receiver secrecy; P1 | sender + receiver authentication keys | timing not represented | mixed: sender held; receiver failed; P1 failed | secrecy held; P1 falsified | P1: no; receiver secrecy: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_SIGSK` | same queries as `LEAK_SIGSK_AB` | sender + receiver authentication keys; backward-compatible alias | timing not represented | mixed: sender held; receiver failed; P1 failed | secrecy held; P1 falsified | P1: no; receiver secrecy: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_KEMSK` | P0-S sender/receiver secrecy; P1 | receiver long-term KEM key | timing not represented | mixed: both secrecy queries held; P1 failed | secrecy held; P1 falsified | P1: no; no secrecy counterexample | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_EKEMSK` | P0-S sender/receiver secrecy; P1 | receiver ephemeral KEM state | timing not represented | mixed: both secrecy queries held; P1 failed | secrecy held; P1 falsified | P1: no; no secrecy counterexample | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_RSKEMSK` | P0-S sender/receiver secrecy; P1 | receiver split-KEM state | timing not represented | mixed: sender held; receiver failed; P1 failed | secrecy held; P1 falsified | P1: no; receiver secrecy: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_SSKEMSK` | P0-S sender/receiver secrecy; P1 | sender split-KEM state | timing not represented | mixed: sender held; receiver failed; P1 failed | secrecy held; P1 falsified | P1: no; receiver secrecy: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_KEMSK_EKEMSK` | P0-S sender/receiver secrecy; P1 | receiver long-term + ephemeral KEM material | timing not represented | mixed: both secrecy queries held; P1 failed | secrecy held; P1 falsified | P1: no; no secrecy counterexample | `logs/final/proverif/summary.txt` |
| ProVerif final core — `LEAK_ALL_RECEIVER_SECRETS` | P0-S sender/receiver secrecy; P1 | receiver long-term KEM + ephemeral KEM + split-KEM state | timing not represented | failed: both secrecy queries and P1 failed | secrecy held; P1 falsified | P1: no; secrecy failures: not established from baseline comparison alone | `logs/final/proverif/summary.txt` |
| ProVerif HMAC confirmation — `HMAC_LEAK_SIGSK_A` | P0-S sender/receiver secrecy; P1 | sender authentication key | timing not represented | mixed: sender held; receiver failed; P1 failed | all three held | not established as a complete compromise theorem; only this target was checked | `logs/variants/hmac-confirmation/proverif/summary.txt` |
| Tamarin replay original — `one_send_two_accepts_exists`, `injective_receiver_accept` | P2 occurrence injectivity | no material compromise occurs | no compromise anywhere | failed: attack witness verified; injectivity falsified | baseline falsified | no; compromise explicitly excluded everywhere | `tamarin/replay/README.md` |
| HMAC-only replay bridge — `one_confirmed_send_two_accepts_exists`, `injective_confirmed_receiver_accept` | P2 occurrence injectivity | no material compromise occurs | no compromise anywhere | failed: attack witness verified; injectivity falsified | matching existence and normal path held | no; compromise explicitly excluded everywhere | `logs/tamarin-replay-hmac-only/summary.txt`, `attack-trace.out` |

For every core leak row, P1 is
`baseline-falsified; compromise not required`. For replay P2, the same
classification applies. HMAC P1 differs: its baseline held and the single
`HMAC_LEAK_SIGSK_A` target failed, but this one experiment must not be
generalized to the complete sender-authentication-key compromise class.

## 6. Named evidence and non-vacuity

### 6.1 ProVerif final core — original Figure-7 no-batch abstraction

Model: `proverif/kwaay_core_final.cpp.pv`

Log: `logs/final/proverif/summary.txt`

- P0-S: sender and receiver secrecy queries are `true` in `BASELINE`.
- P0-O: `SplitKemAccepted ==> SenderSplitKemComponent` is `true` in
  `COMPONENT`.
- P1: `RecvDone ==> SendDone` is `false` in `BASELINE`.
- `HonestRun` is reachable in `BASELINE`.
- P0-O currently has cross-target non-vacuity support only: `COMPONENT`
  has no target-local reachability query.

### 6.2 ProVerif HMAC confirmation — no-batch abstraction

Model: `proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`

Log: `logs/variants/hmac-confirmation/proverif/summary.txt`

- `HMAC_BASELINE`: P0-S and P1 held; `HonestRun` is reachable.
- `HMAC_COMPONENT`: P0-O held, with cross-target rather than target-local
  non-vacuity support.
- `HMAC_LEAK_SIGSK_A`: P1 and receiver secrecy failed; sender secrecy held.
- No other HMAC compromise material has an actual target or result.

### 6.3 Tamarin receiver/batch lifecycle V6

Model: `tamarin/kwaay_splitkem_batch_dynamic_v6.spthy`

Log: `logs/tamarin-v6/summary.txt`

- `slot_origin_without_early_compromise`: `VERIFIED`.
- `partnered_slot_key_not_attacker_known_without_early_compromise`:
  `VERIFIED`.
- `slot_key_known_requires_exception`: `VERIFIED`.
- `executable_add_slot`, `executable_seal_batch`,
  `executable_process_slot`, `executable_batch_complete`, and
  `executable_batch_fail`: `VERIFIED`.

The executability lemmas establish generic lifecycle reachability. They do not
independently establish either exception disjunct or a target-before-late-
compromise witness. Those branch-specific reachability questions remain
`unknown` / not independently checked.

### 6.4 Tamarin receiver/batch lifecycle V7

Model: `tamarin/kwaay_splitkem_batch_dynamic_v7.spthy`

Log: `logs/tamarin-v7/summary.txt`

`slot_origin` and the selected terminal-lifecycle lemmas are `VERIFIED`;
the five existing executability lemmas are also `VERIFIED`. V7 has
compromise events but no dedicated compromise-conditioned result supporting a
compromise claim. Its compromise coverage therefore remains `unknown` or
`not modeled`.

### 6.5 Tamarin replay original — fixed two-slot replay abstraction

Model: `tamarin/replay/kwaay_replay_original.spthy`

Recorded results: `tamarin/replay/README.md`

- matching existence/order: `receiver_accept_has_sender`, `verified`;
- occurrence injectivity: `injective_receiver_accept`, `falsified`;
- normal-path executability: `normal_single_accept`, `verified`;
- lifecycle sanity: `normal_batch_complete`, `verified`;
- attack witness: `one_send_two_accepts_exists`, `verified`.

The exists-trace lemmas establish reachability, not universal security.

### 6.6 HMAC-only replay bridge — fixed two-slot confirmed-message abstraction

Model: `tamarin/replay/kwaay_replay_hmac_only.spthy`

README: `tamarin/replay/README-hmac-only.md`

Raw evidence: `logs/tamarin-replay-hmac-only/`

- matching existence/order: `confirmed_receiver_accept_has_sender`, `verified`;
- sender occurrence disambiguation: `confirmed_message_unique_send`, `verified`;
- normal-path non-vacuity: `normal_confirmed_single_accept`, `verified`;
- normal batch completion: `normal_confirmed_batch_complete`, `verified`;
- attack witness: `one_confirmed_send_two_accepts_exists`, `verified`;
- at-most-once acceptance: `confirmed_message_accepted_at_most_once`, `falsified`;
- occurrence injectivity: `injective_confirmed_receiver_accept`, `falsified`;
- all selected lifecycle/state-consumption lemmas: `verified`.

The witness uses one matching `ConfirmedSend`, two distinct accept timepoints
and slot indices, the same `A,B,bid,rst,m,sid,k,tag`, and the same public
`<m,hmac(confirm_key(k),sid)>`, with both accepts before `BatchComplete`.
No sender/receiver state compromise occurs. `HonestSession` makes the matching
existence theorem largely structural, so this artifact is a replay/occurrence
bridge rather than independent HMAC P1 or computational-security evidence.

## 7. Milestone ownership

| Milestone | Evidence it may add |
|---|---|
| M1 | ✅ HMAC-only replay bridge matching/P2, non-vacuity, lifecycle, no-compromise witness, regressions, and raw logs. |
| M2 | The first P3 under `C_install` composition model and its interface assumptions. |
| M3 | Fixed dedup P2 and fixed-impact P3 under `C_install`. |
| M4 | Combined P0-S/P0-O regressions, P1/P2, P3 under `C_install`, and selected compromise targets. |
| M5 | Reproducible logs and the final expected-versus-actual freeze. |

M1 HMAC replay cells now record completed actual results. Impact/P3, fixed
dedup, and combined cells remain `not modeled` until their own artifacts and
completed runs exist.
