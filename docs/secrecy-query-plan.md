# Secrecy Query Plan for K-Waay Core

## Purpose

This document plans the first ProVerif symbolic approximation of session-key secrecy for the K-Waay Figure 7 core model.

It is not a replacement for the paper's computational KIND-style security game.

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

## Current Known Results

- Q0 HonestRun: reachable
- Q1-exact RecvDone-to-SendDone agreement: false, kept as diagnostic
- Q1a RecvDone implies SenderPrekeyVerified: true
- Q1b RecvDone implies ReceiverPrekeyVerified: true

## Why secrecy needs a careful design

A naive query such as:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> not attacker(k).
```

is not the right first query shape for the current public-channel core model.

Reasons:

- The exact `RecvDone ==> SendDone` correspondence is intentionally false in this model.
- Public-channel ciphertext replacement can create receiver sessions that are not partnered with a sender session.
- The current model has no compromise exceptions, so a secrecy query must first target the honest core case.
- ProVerif reachability/correspondence queries are symbolic approximations, not the paper's full computational KIND game.

## First Secrecy Target

The first secrecy target should be the session key from the honest core run, under no compromise.

The model should keep:

- Figure 7 message structure: `m = (ct_l, ct_k, ct_s)`
- public-channel delivery of prekeys and message tuples
- no AEAD, MAC, tag, key confirmation, or application message

The first query should ask whether the attacker learns the session key emitted by an honest-run event.

## Proposed Event Strategy

Add a dedicated event for the key whose secrecy is being checked, for example:

```text
SecretKeyTest(k)
```

This is only a design marker. The `.pv` file should later choose the exact event name and placement.

Candidate placement:

- After the receiver computes `kRecv`.
- Before or next to `HonestRun(kRecv)`.
- Only in the no-compromise core process.

Purpose:

- Keep Q0 `HonestRun` as a reachability marker.
- Use a separate event for Q2 secrecy so traces are easier to read.
- Avoid overloading `RecvDone` with both agreement and secrecy meaning.

## Proposed Query Shape

For a first no-compromise symbolic approximation, use an event-guarded secrecy query shape:

```text
If SecretKeyTest(k) occurs, attacker(k) should be false.
```

This should be added only after the model has a clear event marking the tested key.

## Expected Interpretation

If the query is true:

- The symbolic model did not find a way to derive the marked session key in the no-compromise core setting.
- This is useful evidence for the current abstraction.
- It is not a proof of the paper's full computational KIND security game.

If the query is false:

- Record the trace in `docs/trace-ledger.md`.
- Classify it before changing the model.
- Decide whether it is expected false, model artifact, possible protocol issue, or normal bad case.
- Do not immediately add AEAD, MAC, tag, or key confirmation to the Figure 7 core.

## Out of Scope for First Q2

- compromise exceptions
- adaptive compromise
- expose oracle modeling
- full BatchReceive
- receiver-side prekey reuse
- computational KIND game equivalence
- AEAD, MAC, tag, or key confirmation

## Follow-Up Plan

1. Add a secrecy-marker event in `proverif/kwaay-core-public-channel.pv`.
2. Add one no-compromise symbolic secrecy query.
3. Run ProVerif and record the result.
4. If false, add a new trace-ledger entry before changing the model.
5. Only after the honest core query is understood, design compromise-aware variants.
