# Research Problem

**Status:** Frozen current RQ-v2 research statement.

K-Waay's `BatchReceive` semantics require the entries admitted into one batch
to correspond to distinct parties. RQ-v2 names this identity-level invariant
`DistinctPartyPerBatch` and studies whether it is necessary for the intended
party-level batch identity semantics.

The problem is not ordinary message authentication or exact-message replay
filtering. Party identity, message identity, session identity, slot identity,
and batch identity are separate coordinates. In this research line, `A` is the
modeled protocol-principal identity coordinate. It is not asserted to equal a
deployed real-world party identifier, database record, API object, or other
implementation representation.

The consequence chain under study is:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> conditional upper-layer duplicate consumption/install impact
```

# Research Question

Within the stated symbolic admission model, does removing
`DistinctPartyPerBatch` admit an invalid batch in which one modeled party
occupies two distinct slots, with duplicate receiver acceptance as a reachable
consequence, and does party-level admission restore the intended batch identity
semantics while preserving reachable valid distinct-party batches?

# Main Claim

The current bounded evidence supports the scoped claim that
`DistinctPartyPerBatch` is necessary for the intended party-level batch
identity semantics of the modeled `BatchReceive` boundary.

When the invariant is removed in R-semantics, same-batch repeated-party
composition is admitted and a trace with one Send occurrence and two receiver-
accept occurrences is reachable. In P-semantics, same-party composition is
rejected, every admitted batch has distinct modeled parties, and a valid
distinct-party batch remains reachable. The comparison therefore treats
`DistinctPartyPerBatch` as a substantive identity-level safety invariant, not
as a semantically empty input restriction.

# Supporting Claims

1. **Identity separation.** Message equality or inequality does not determine
   party equality or inequality. Exact-message checks and party-level admission
   constrain different coordinates.
2. **Relaxed admission consequence.** Removing party-level admission permits
   same-batch repeated-party composition; the bounded relaxed model contains a
   reachable duplicate-acceptance witness.
3. **Party-level restoration.** The party-admission model restores the intended
   batch identity semantics within the modeled boundary and retains a reachable
   valid distinct-party execution.
4. **Message-dedup comparison.** Exact-message deduplication rejects a repeated
   exact message and can satisfy scoped occurrence injectivity, but it still
   permits two different messages from the same party in one batch. It is an
   auxiliary comparison, not the main contribution or a substitute for
   `DistinctPartyPerBatch`.
5. **HMAC separation.** HMAC may support message authenticity, integrity, or
   confirmation. It does not establish party uniqueness, party admission, or
   replay prevention by itself.
6. **Conditional impact.** Duplicate receiver acceptance can imply duplicate
   upper-layer consumption or installation only under an explicit composition
   interface that independently consumes each accepted output.

# Model Scope

- The current RQ-v2 prototypes are symbolic, fixed-two-slot admission models.
- `A` denotes the modeled protocol-principal identity coordinate only; the
  models do not identify an implementation enforcement location or deployed
  party representation.
- R-semantics omits the party-level admission guard. M-semantics compares exact
  message identities. P-semantics compares modeled party identities.
- The duplicate-acceptance witness is scoped to one batch and receiver state,
  with one Send occurrence and two receiver-accept occurrences.
- The prototypes use abstract Send, admission, accept, and reject events. They
  do not model KEMs, signatures, HMAC computation, compromise, prekey
  cryptography, Double Ratchet, an application, or deployed K-Waay behavior.
- Whole-batch rejection is the current prototype choice. The concrete caller,
  server, client, or batching-service implementation of that choice is not
  specified.
- The verified rejection traces establish reachability, not liveness requiring
  every collected invalid batch to progress to rejection.

# Non-Claims

This research statement does **not** claim any of the following:

- "K-Waay is broken" or that a deployed K-Waay implementation omits the
  invariant;
- HMAC solves or prevents replay;
- exact-message deduplication replaces party admission;
- party admission uniquely restores occurrence injectivity;
- occurrence injectivity is the final research contribution;
- every same-party pair across sessions, messages, or different batches is a
  violation;
- duplicate receiver acceptance unconditionally causes duplicate consumption,
  installation, session cloning, or application impact;
- arbitrary-length, cross-batch, rollback, restart, compromise-resilient,
  computational-security, or deployed-system guarantees;
- a unique implementation mechanism or enforcement location for
  `DistinctPartyPerBatch`.

# Evidence Boundary

The current semantic authority is
[`g2-admission-semantics.md`](g2-admission-semantics.md). The current execution
record is [`prototype-execution-report.md`](prototype-execution-report.md).
The supporting prototype models are:

- `tamarin/rq-v2-minimal/rqv2_relaxed.spthy`;
- `tamarin/rq-v2-minimal/rqv2_message_dedup.spthy`;
- `tamarin/rq-v2-minimal/rqv2_party_admission.spthy`.

The result boundary is:

| Role | Direct evidence | Status |
| --- | --- | --- |
| relaxed duplicate acceptance | `one_send_two_accepts_exists`; `receiver_accept_injective` | verified witness; falsified injectivity |
| message-dedup auxiliary comparison | `repeated_message_rejection_exists`; `same_party_different_messages_batch_exists`; `receiver_accept_injective` | verified; verified; verified |
| party-level batch identity | `same_party_rejection_exists`; `distinct_party_batch_exists`; `accepted_batch_has_distinct_parties` | verified; verified; verified |
| upper-layer consumption/install impact | no current RQ-v2 prototype property | conditional only; not modeled in the current prototypes |

The current RQ-v2 prototype evidence therefore terminates at duplicate receiver
acceptance. Any consumption/install conclusion requires a separately stated
composition boundary such as `C_install-v2`. Frozen M0-M5 HMAC, replay, dedup,
combined, and impact artifacts remain historical evidence and are not the
current RQ-v2 claim authority.

# Future Work Boundary

Future work may extend the research only by making its additional assumptions
and evidence explicit. Candidate extensions include:

- mapping the abstract admission decision to an auditable caller, server,
  client, batching service, or implementation interface;
- defining and verifying an RQ-v2 upper-layer composition model before making
  consumption or installation claims;
- generalizing beyond the fixed two-slot abstraction without silently treating
  the bounded result as an arbitrary-length theorem;
- studying cross-batch, rollback, restart, concurrency, or state-reuse
  behavior;
- adding liveness obligations for invalid-batch rejection;
- analyzing compromise and computational cryptographic assumptions separately
  from the identity-admission invariant;
- validating whether deployed K-Waay code or an integration actually enforces
  the specification-level identity constraint.

Future extensions must not retroactively broaden the claims established by the
current bounded prototypes.
