# Security Analysis

## 1. Analysis Questions

The analysis compares the three admission semantics through three questions.

**Q1 — Repeated-party composition.** When `DistinctPartyPerBatch` is removed,
is a same-batch composition containing the same modeled party in multiple slots
reachable under the relaxed admission semantics?

**Q2 — Duplicate receiver acceptance.** Under that relaxed semantics, is there
a reachable trace in which one matching `Send(A,sid,m)` occurrence corresponds
to two distinct `ReceiverAccept(A,sid,m,bid,rst)` occurrences in the same batch
and receiver-state context?

**Q3 — Identity-coordinate comparison.** Do a message-level restriction and a
party-level restriction yield different results for same-party admission,
scoped receiver-occurrence injectivity, and preservation of the intended batch
identity semantics?

The questions separate two evidence classes. Model rules directly define which
candidate pairs are admitted or rejected. Tamarin lemma outcomes establish the
recorded reachability and all-traces properties. The analysis does not treat an
unqueried behavior as a separately verified theorem.

## 2. Relaxed Model Result

All four recorded relaxed-model obligations terminate with the following
outcomes:

| Lemma | Recorded status |
| --- | --- |
| `normal_relaxed_batch_exists` | verified — 10 steps |
| `one_send_two_accepts_exists` | verified — 13 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | falsified; trace found — 13 steps |

The positive existence result and the falsified injectivity result identify the
same bounded behavior. The trace contains one matching sender occurrence

```text
Send(A,sid,m) @ s
```

followed by admission of one batch and two acceptance occurrences

```text
ReceiverAccept(A,sid,m,bid,rst) @ r1
ReceiverAccept(A,sid,m,bid,rst) @ r2
```

with `s < r1 < r2`. The two acceptances agree on party, session, message,
batch, and receiver-state coordinates, but occur at different timepoints. The
existence formula additionally requires that every matching
`Send(A,sid,m)` occurrence is the same occurrence `s`; unrelated sends with
other session or message coordinates are outside that uniqueness condition.

This is a bounded counterexample to `receiver_accept_injective` in the relaxed
two-slot model. It is not an execution satisfying the original distinct-party
`BatchReceive` precondition. The result establishes Q1 through the relaxed
admission rule and Q2 through the verified witness and falsified universal
property.

## 3. Message-Dedup Result

The message-deduplication model records the following outcomes:

| Lemma | Recorded status |
| --- | --- |
| `repeated_message_rejection_exists` | verified — 4 steps |
| `same_party_different_messages_batch_exists` | verified — 16 steps |
| `accepted_batch_has_distinct_messages` | verified — 31 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | verified — 33 steps |

These results show that M-semantics enforces its stated message-level
condition. A repeated exact message can reach the rejection branch, and two
distinct accept occurrences in one admitted batch have different message
coordinates. The scoped receiver-occurrence injectivity property is also
verified: the model has no trace in which one matching send tuple gives rise to
two distinct accept occurrences under the lemma's batch and receiver-state
coordinates.

However, `same_party_different_messages_batch_exists` provides a separate
positive trace. It contains two legitimate send occurrences

```text
Send(A,sid1,m1)
Send(A,sid2,m2)
```

with `sid1 != sid2` and `m1 != m2`, followed by one admitted batch and one
acceptance for each entry. Both entries carry party coordinate `A`. Thus,
M-semantics restores scoped occurrence injectivity for an exact send tuple but
does not establish `DistinctPartyPerBatch`. This is a coordinate distinction,
not a conclusion that message deduplication is ineffective for its stated
message-level purpose.

## 4. Party-Admission Result

The party-admission model records five verified outcomes:

| Lemma | Recorded status |
| --- | --- |
| `same_party_rejection_exists` | verified — 5 steps |
| `distinct_party_batch_exists` | verified — 17 steps |
| `accepted_batch_has_distinct_parties` | verified — 31 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | verified — 33 steps |

The rejection witness contains two different messages and sessions belonging
to the same modeled party and reaches `Reject(bid,rst)`. The universal
`accepted_batch_has_distinct_parties` result establishes that two distinct
accept occurrences from one admitted batch carry different party coordinates.
The scoped sender-origin and receiver-injectivity properties are also
verified.

The safety result is not obtained by preventing every batch. The verified
`distinct_party_batch_exists` lemma exhibits two distinct modeled parties, two
legitimate send occurrences, one admitted batch, and two receiver-accept
occurrences. P-semantics therefore both excludes same-party composition at the
modeled admission boundary and preserves a reachable valid distinct-party
execution. The rejection result is a reachability result; it does not assert
that every collected invalid pair must eventually take the enabled rejection
rule.

## 5. Comparative Result

Table 1 separates recorded lemma outcomes from behavior defined directly by an
admission rule. “Not separately queried” means that the corresponding theory
contains no dedicated lemma for that exact row; it is not reported as a proved
property.

| Property | R-semantics | M-semantics | P-semantics |
| --- | --- | --- | --- |
| Repeated exact message rejected | No: the verified one-send/two-accept witness admits the repeated tuple | Yes: rejection reachability verified; accepted messages proved distinct | Rejected when the party coordinate repeats by the party-rejection rule; no message-specific lemma |
| Same-party/different-message admitted | Permitted by the unguarded admission rule; not separately queried | Yes: verified by `same_party_different_messages_batch_exists` | No: same-party rejection with different messages is verified |
| Distinct-party invariant | Not enforced; the verified repeated tuple carries the same party twice | Not enforced; same-party/different-message admission is verified | Verified by `accepted_batch_has_distinct_parties` |
| One-send/two-accept duplicate witness | Reachable: `one_send_two_accepts_exists` verified | Excluded by the verified scoped injectivity lemma | Excluded by the verified scoped injectivity lemma |
| Scoped receiver injectivity | Falsified | Verified | Verified |
| Valid distinct-party batch reachability | General relaxed reachability verified, but no dedicated distinct-party lemma | No dedicated distinct-party reachability lemma | Verified by `distinct_party_batch_exists` |

The comparison answers Q3. Message-level admission is sufficient for the
modeled exact-message and scoped occurrence properties, but it leaves
same-party/different-message composition reachable. Party-level admission
checks the coordinate named by `DistinctPartyPerBatch`, verifies the admitted-
batch identity property, and retains non-vacuous valid behavior.

## 6. Interpretation

The direct formal evidence establishes the following bounded statements:

- R-semantics admits repeated-party input because it contains no party guard;
- repeated-party composition and a one-send/two-accept witness are reachable in
  the relaxed model;
- M-semantics distinguishes messages and verifies scoped receiver-occurrence
  injectivity while retaining same-party/different-message admission;
- P-semantics rejects a same-party pair, verifies distinct parties in admitted
  batches, and preserves a reachable valid distinct-party batch; and
- message identity and party identity are different coordinates for the
  admission question.

The intended party-level identity interpretation is the semantic reading of
these results: a batch expected to represent distinct modeled parties loses
that interpretation when the same party occupies multiple slots. The current
prototypes do not contain output-key objects, `KEY` or `TEST` operations, or
key-correctness relations. Accordingly, the formal analysis stops at admission,
rejection, and receiver acceptance rather than making conclusions about those
unmodeled interfaces.

## 7. Result Boundary

Direct RQ-v2 formal evidence ends at `ReceiverAccept`. The three prototypes do
not contain an application consumer, an installation transition, or an upper-
layer session action. Two receiver-accept occurrences therefore do not by
themselves establish duplicate consumption, installation, or application
effects.

Historical `C_install-v2` results may be discussed only as a conditional
composition example with their own assumptions and historical evidence role.
They are not results of the current RQ-v2 admission prototypes and are not part
of the direct chain established in this section.

All lemma names and statuses in this section are taken from
[`prototype-execution-report.md`](../rq-v2/prototype-execution-report.md). The
claim scope and excluded inferences follow
[`contribution-evidence-map.md`](contribution-evidence-map.md) and the canonical
argument sequence in
[`rq-v2-complete-argument-map.md`](../rq-v2/rq-v2-complete-argument-map.md).
