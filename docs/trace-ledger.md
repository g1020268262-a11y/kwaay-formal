# Trace Ledger

## Purpose

This file records ProVerif false queries, diagnostic traces, and model artifacts for the K-Waay core analysis.

Each entry should classify the result as one of:

- expected false
- model artifact
- possible protocol issue
- normal bad case

The goal is to avoid treating every false query as a protocol attack.

## Current Model Boundary

- Model file: proverif/kwaay-core-public-channel.pv
- Protocol target: original K-Waay Figure 7 core
- Message structure: m = (ct_l, ct_k, ct_s)
- No AEAD
- No MAC
- No tag
- No key confirmation
- No full BatchReceive
- No compromise exceptions yet

## TR-001: Exact receiver agreement fails in public-channel core

### Metadata

- Trace ID: TR-001
- Date: TODO
- Model file: proverif/kwaay-core-public-channel.pv
- Query type: correspondence / authentication diagnostic
- Classification: expected false
- Status: documented, not fixed by modifying Figure 7 core

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

### Result

```text
RESULT event(RecvDone(B_1,A_1,s,k)) ==> event(SendDone(A_1,B_1,s,k)) is false.
```

### Trace Shape

- The sender emits a Figure 7 core message `m = msg(ct_l, ct_k, ct_s)`.
- The public channel lets the adversary provide a modified `mFromNet`.
- One KEM ciphertext can differ, for example `ct_k`.
- The receiver computes `RecvDone(B,A,s,k)` for a session key not matched by `SendDone(A,B,s,k)`.

### Interpretation

- This is an expected false diagnostic query for the public-channel Figure 7 core model.
- It shows that exact session agreement is stronger than the current core model.
- It should not be fixed by adding AEAD, MAC, tag, key confirmation, or application payload to `m`.
- This entry does not claim a K-Waay protocol vulnerability.

### Related Passing Queries

- Q0 HonestRun reachability is true.
- Structural sender prekey verification before `RecvDone` is true.
- Structural receiver prekey verification before `RecvDone` is true.

### Follow-Up

- Keep Figure 7 core unchanged.
- Use this trace as a diagnostic baseline for later model variants.
- If later variants add non-core mechanisms, record them as separate model boundaries.
