# Evaluation

## 1. Experimental / Verification Setup

The recorded RQ-v2 verification used Tamarin 1.12.0 with Maude 3.5.1 in a
WSL Ubuntu 24.04 environment. The recorded Tamarin executable was
`/home/linuxbrew/.linuxbrew/bin/tamarin-prover`, with the non-interactive path
`/home/linuxbrew/.linuxbrew/bin:/usr/bin:/bin`. Parsing used
`tamarin-prover --parse-only`, and lemma execution used
`tamarin-prover --prove`.

These results come from the previously executed verification documented in the
frozen prototype execution report. The current freeze package is provenance
packaging derived from that report, with `packaging_mode=existing-report-only`
and `prover_rerun=no`. No prover was rerun during this paper-writing phase.

## 2. Model Set

The evaluation compares three symbolic fixed-two-slot theories. R-semantics
omits party- and message-uniqueness checks at admission. M-semantics rejects an
equal-message pair and admits a pair guarded by `m1 != m2`. P-semantics rejects
an equal-party pair and admits a pair guarded by `A1 != A2`.

The theories share the party creation, sender origin, two-entry collection,
batch identifier, receiver-state coordinate, sequential slot processing, and
`ReceiverAccept` lifecycle. Their principal experimental difference is the
predicate applied at the admission decision.

## 3. Verification Results

Table 1 reports only properties recorded in the frozen execution report or
distinctions that follow directly from the corresponding admission rule.
“Not queried” means that the theory contains no dedicated lemma for that exact
property. A model-semantic entry is not presented as an independently verified
lemma.

| Property | R-semantics | M-semantics | P-semantics |
| --- | --- | --- | --- |
| Normal or valid batch reachability | `normal_relaxed_batch_exists`: verified — 10 steps | Not queried | `distinct_party_batch_exists`: verified — 17 steps |
| Same-party admission or rejection | Same-party admission allowed by model semantics; exact repeated entry witnessed below | Same-party/different-message admission verified — 16 steps; equal-message rejection verified — 4 steps | Same-party rejection verified — 5 steps |
| Exact-message rejection | Not applicable: R-semantics has no rejection branch | `repeated_message_rejection_exists`: verified — 4 steps | No message-specific lemma; rejection is selected by party equality |
| Same-party/different-message behavior | Permitted by model semantics; not separately queried | `same_party_different_messages_batch_exists`: verified — 16 steps | Same-party rejection with distinct messages is reachable — 5 steps |
| `receiver_accept_has_send` | Verified — 8 steps | Verified — 8 steps | Verified — 8 steps |
| `receiver_accept_injective` | Falsified; trace found — 13 steps | Verified — 33 steps | Verified — 33 steps |
| Accepted messages are distinct | Not queried | `accepted_batch_has_distinct_messages`: verified — 31 steps | Not queried |
| Accepted parties are distinct | Not established; the duplicate witness repeats the same party coordinate | Not established; same-party/different-message admission is verified | `accepted_batch_has_distinct_parties`: verified — 31 steps |

The table separates the two central dimensions. Occurrence injectivity asks
whether one matching sender occurrence can yield two acceptance occurrences in
the scoped batch context. Party uniqueness asks whether distinct accepted
slots carry distinct modeled party coordinates. The two properties do not have
the same outcome under M-semantics.

## 4. Relaxed Witness

In R-semantics, `one_send_two_accepts_exists` is verified with a 13-step trace.
The trace contains one `Send(A,sid,m)` occurrence and two
`ReceiverAccept(A,sid,m,bid,rst)` occurrences. The acceptances agree on `A`,
`sid`, `m`, `bid`, and `rst`, but occur at different timepoints. Consistently,
`receiver_accept_injective` is falsified with a trace found in 13 steps.

This witness is a bounded result for the relaxed two-slot abstraction. It is
not an execution satisfying the retained distinct-party admission condition,
and the direct observation ends at `ReceiverAccept`.

## 5. Message-Level Comparison

M-semantics makes exact duplicate rejection reachable:
`repeated_message_rejection_exists` is verified in 4 steps. At the same time,
`same_party_different_messages_batch_exists` is verified in 16 steps, showing
an admitted batch with `A1 = A2` and `m1 != m2`. Its
`receiver_accept_injective` lemma is verified in 33 steps.

Thus, the message-level restriction can restore the scoped one-Send/one-accept
occurrence property in this prototype while still not establishing party
uniqueness. The result is not a failure of message deduplication at its stated
message-level purpose; it demonstrates that occurrence injectivity and party
uniqueness are different properties.

## 6. Party-Level Restoration

P-semantics records `same_party_rejection_exists` as verified in 5 steps and
`accepted_batch_has_distinct_parties` as verified in 31 steps. The scoped
`receiver_accept_injective` lemma is also verified in 33 steps.

The restoration is non-vacuous. `distinct_party_batch_exists` is verified in
17 steps and exhibits two distinct parties, two legitimate sender occurrences,
one admitted batch, and two receiver acceptances. P-semantics therefore does
not obtain the invariant by rejecting every candidate batch. It is one modeled
restoration of `DistinctPartyPerBatch`, not a uniquely required enforcement
algorithm or location.

## 7. Reproducibility / Artifact Binding

The freeze package binds the evaluation to the following model hashes:

| Model | SHA-256 |
| --- | --- |
| `rqv2_relaxed.spthy` | `E5129575720020AA3F509782C2052FBF2114A540D013126F5A75D316CBABAF9D` |
| `rqv2_message_dedup.spthy` | `90A196F5DA5C244026596283D001376427880CD64C5BEA3C6CFDFD4CCBA99184` |
| `rqv2_party_admission.spthy` | `C35AF64CAC7F01182418CB999EA105214B8DA4F2295B670A9B3733F0BD976BBA` |

`environment.txt` records the reported toolchain and operating environment;
`verification-commands.txt` records the parse and prove invocations;
`models-sha256.txt` binds the three theories; and `freeze-manifest.tsv` maps
documents, models, results, and evidence roles. The RQ-v2 freeze package does
not include raw prover transcripts for these prototypes. It records model
hashes, commands, environment, and previously recorded results, but does not
constitute a fresh prover rerun.

