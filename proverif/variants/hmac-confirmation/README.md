# K-Waay HMAC Confirmation ProVerif Variant

This directory contains an explicit key-confirmation variant derived from the
core final ProVerif model:

- source model: `kwaay_core_hmac_confirmation.cpp.pv`
- runner: `run-hmac-confirmation.sh`
- generated logs: `logs/variants/hmac-confirmation/proverif/`

The core final model `proverif/kwaay_core_final.cpp.pv` is not modified by this
variant. Tamarin models are also not modified.

## Design

This is an explicit HMAC key-confirmation experiment, not an AEAD variant.

The sender computes the ordinary Figure 7 core session key first:

```text
kSend = kdf(KL, KE, KS, sidAB)
```

Then it derives a confirmation key and emits an HMAC over the session id:

```text
tagAB = hmac(confirm_key(kSend), sidAB)
out(c, msg_confirm(m, tagAB))
```

The receiver inputs a `confirmed_message_tuple`, extracts the base message and
tag, recomputes the ordinary session key, and checks:

```text
tagFromNet = hmac(confirm_key(kRecv), sidBA)
```

Only after this check does the model emit:

```text
ReceiverKey(...)
RecvDone(...)
```

The tag binds confirmation to the transcript/session id. It does not encrypt
the message and does not model AEAD.

## Targets

This initial variant intentionally runs only three targets:

- `HMAC_BASELINE`
- `HMAC_COMPONENT`
- `HMAC_LEAK_SIGSK_A`

It does not immediately add all `LEAK_*` targets from the core final model.

`HMAC_BASELINE` keeps the baseline sanity, prekey, sender secrecy, receiver
secrecy, and agreement queries. In this variant, `RecvDone ==> SendDone` is
expected to be true because the receiver accepts only after the HMAC check.

`HMAC_COMPONENT` keeps the split-KEM component authenticity query:

```text
SplitKemAccepted ==> SenderSplitKemComponent
```

`HMAC_LEAK_SIGSK_A` is the first signature-key leak experiment for the HMAC
variant. It leaks only A's signature key and reuses the baseline query set.

## Current results

Current runner result:

- `HMAC_BASELINE`: OK. `RecvDone ==> SendDone` is true; sender secrecy and
  receiver secrecy are true.
- `HMAC_COMPONENT`: OK. `SplitKemAccepted ==> SenderSplitKemComponent` is true.
- `HMAC_LEAK_SIGSK_A`: OK as a ProVerif run. The leak experiment falsifies
  `RecvDone ==> SendDone` and receiver-side secrecy, while sender-side secrecy
  remains true.

## Run

From the repository root:

```bash
bash proverif/variants/hmac-confirmation/run-hmac-confirmation.sh
```

Or run a single target:

```bash
bash proverif/variants/hmac-confirmation/run-hmac-confirmation.sh HMAC_BASELINE
```

The summary is written to:

```text
logs/variants/hmac-confirmation/proverif/summary.txt
```
