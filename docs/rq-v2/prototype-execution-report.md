# RQ-v2 Prototype Execution Report

## Environment

The prototypes were executed in the existing WSL Ubuntu 24.04 verification
environment.

```text
Tamarin version: 1.12.0
Maude version:   3.5.1
Tamarin path:    /home/linuxbrew/.linuxbrew/bin/tamarin-prover
```

The non-interactive WSL runs used:

```text
PATH=/home/linuxbrew/.linuxbrew/bin:/usr/bin:/bin
```

Parsing was checked with `tamarin-prover --parse-only`. Lemmas were executed
with `tamarin-prover --prove`. No model was changed during this execution
audit.

Execution-input SHA-256 values were:

| Model | SHA-256 |
| --- | --- |
| `rqv2_relaxed.spthy` | `E5129575720020AA3F509782C2052FBF2114A540D013126F5A75D316CBABAF9D` |
| `rqv2_message_dedup.spthy` | `90A196F5DA5C244026596283D001376427880CD64C5BEA3C6CFDFD4CCBA99184` |
| `rqv2_party_admission.spthy` | `C35AF64CAC7F01182418CB999EA105214B8DA4F2295B670A9B3733F0BD976BBA` |

These are exploratory symbolic prototypes. They do not model KEMs,
signatures, HMAC, compromise, prekey cryptography, Double Ratchet, an
implementation, or deployed K-Waay behavior.

The prototypes study one identity-level rule:

```text
same batch:
  slot1.party != slot2.party
```

The rule does not prohibit one party from creating multiple sessions or
messages, or from participating in different batches. HMAC is outside this
admission comparison: authenticity, integrity, or confirmation does not replace
party-level admission.

## Model Parsing

| Model | Parse |
| --- | --- |
| `rqv2_relaxed.spthy` | PASS — syntax valid; no parser error; no imports |
| `rqv2_message_dedup.spthy` | PASS — syntax valid; no parser error; no imports |
| `rqv2_party_admission.spthy` | PASS — syntax valid; no parser error; no imports |

## Relaxed Result

### Lemma results

| Lemma | Tamarin status |
| --- | --- |
| `normal_relaxed_batch_exists` | verified — 10 steps |
| `one_send_two_accepts_exists` | verified — 13 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | falsified; trace found — 13 steps |

### Result

Duplicate occurrence-level acceptance exists in this bounded relaxed model.
The falsified injectivity lemma and the positive existence lemma agree.

The counterexample structure is:

```text
CreateParty(A)
    |
    v
Send(A, sid, m)
    |
    +-- Out(<A,sid,m>) -- replay/deliver --> batch slot 1
    |
    +-- Out(<A,sid,m>) -- replay/deliver --> batch slot 2
                                             |
                                             v
                                  BatchReceive(bid,rst)
                                             |
                       +---------------------+---------------------+
                       v                                           v
ReceiverAccept(A,sid,m,bid,rst) @ r1    ReceiverAccept(A,sid,m,bid,rst) @ r2
```

The two accept events have the same party, session, message, batch, and
receiver-state coordinates, but different event occurrences `r1 < r2`. Both
use the same persistent `Sent(A,sid,m)` origin fact. The
`one_send_two_accepts_exists` formula additionally requires that the matching
`Send(A,sid,m)` tuple has one unique send occurrence. It does not exclude
unrelated sends with different session/message coordinates.

This is a result about the relaxed two-slot abstraction, not a counterexample
to executions satisfying K-Waay's stated distinct-party `BatchReceive`
precondition.

## Auxiliary Message Dedup Result

### Lemma results

| Lemma | Tamarin status |
| --- | --- |
| `repeated_message_rejection_exists` | verified — 4 steps |
| `same_party_different_messages_batch_exists` | verified — 16 steps |
| `accepted_batch_has_distinct_messages` | verified — 31 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | verified — 33 steps |

### Result

Message-level deduplication rejects a repeated exact message, but it does not
enforce party-level uniqueness. This model is an auxiliary comparison, not the
main RQ-v2 problem or contribution.

The positive same-party/different-message trace has the following structure:

```text
Party A
  |
  +-- Send(A,sid1,m1) --+
  |                     |
  +-- Send(A,sid2,m2) --+--> BatchReceive(bid,rst)
                               where sid1 != sid2 and m1 != m2
                                      |
                         +------------+------------+
                         v                         v
                  ReceiverAccept 1          ReceiverAccept 2
```

Both accepted entries have party `A`, so M-semantics admits a batch that
violates `DistinctPartyPerBatch`. Therefore message identity is insufficient
as a substitute for party identity.

However, the two accepts correspond to two different legitimate Send
occurrences, not one Send occurrence accepted twice. Accordingly,
`receiver_accept_injective` is verified in this model. The trace is a
party-uniqueness counterexample, not an occurrence-injectivity counterexample.

## Party-Level Batch Identity Result

### Lemma results

| Lemma | Tamarin status |
| --- | --- |
| `same_party_rejection_exists` | verified — 5 steps |
| `distinct_party_batch_exists` | verified — 17 steps |
| `accepted_batch_has_distinct_parties` | verified — 31 steps |
| `receiver_accept_has_send` | verified — 8 steps |
| `receiver_accept_injective` | verified — 33 steps |

### Result

Within this two-slot model, party-level admission restores the intended batch
identity semantics: no admitted batch can produce two distinct receiver
accepts for the same party. The all-traces
`accepted_batch_has_distinct_parties` lemma is verified, and the explicit
same-party rejection branch is reachable.

The result is not vacuous: `distinct_party_batch_exists` is verified and
exhibits two different parties, two legitimate Send occurrences, one admitted
batch, and two ReceiverAccept occurrences. Thus the model does not obtain its
safety result by prohibiting every batch.

The current lemmas establish safety plus reachability of a rejection trace.
They do not establish a liveness property requiring every collected invalid
batch to progress to a `Reject` event; a trace may stop before taking an
enabled rule. No such liveness claim is made here.

## RQ-v2 Narrative Conclusion

**Assessment: `SUPPORTS_IDENTITY_INVARIANT_NECESSITY_ANALYSIS`**

The primary result is about batch identity semantics:

1. Removing party-level admission in R-semantics permits the same party to
   occupy two slots of one batch. In the realized exact-repeated-entry trace,
   that invalid batch composition produces two receiver-accept occurrences
   for one Send origin.
2. P-semantics rejects same-party batch composition, verifies that accepted
   batches have distinct parties, and preserves reachable valid
   distinct-party batches. Within this bounded abstraction, party admission
   therefore restores the intended batch identity semantics.
3. M-semantics is an auxiliary comparison. It rejects exact-message repetition
   and verifies the scoped occurrence-injectivity lemma, yet still admits two
   different messages from the same party. It therefore does not enforce
   `DistinctPartyPerBatch`.

The prototype consequently supports the RQ-v2 claim direction that
`DistinctPartyPerBatch` is necessary for the intended party-level batch
identity semantics. It does **not** claim that party admission is uniquely
necessary for occurrence injectivity: the M-semantics result demonstrates why
scoped occurrence injectivity is a supporting property rather than the final
contribution.

The main consequence chain supported at this layer is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance is reachable
```

These prototypes do not model upper-layer consumption or installation. Any
extension from duplicate receiver acceptance to duplicate consumption or
installation must remain conditional on an explicit composition boundary such
as `C_install-v2`; it is not implied by two `ReceiverAccept` events alone.

### Model-design audit findings

- No parser, well-formedness, or proof-execution error was observed.
- "Duplicate receiver acceptance" in the relaxed witness means that one Send
  occurrence has two receiver-accept occurrences. A same-party/different-
  message batch is separately an identity-invariant violation and need not be
  an occurrence-injectivity violation.
- Messages and session identifiers are fresh per `SendMessage` rule firing.
  This is a deliberate minimal-prototype assumption and must not be silently
  generalized to a full K-Waay model.
- Prekeys are omitted rather than equated with party identity. Consequently,
  the prototypes cannot answer prekey-level or key-rotation questions.
- The `Neq` restriction is the symbolic guard used for exact inequality in the
  M- and P-semantics admission branches; it is not a cryptographic or
  implementation mechanism.
- Whole-batch rejection is the prototype choice. Its implementation location
  and concrete failure behavior remain unspecified.
