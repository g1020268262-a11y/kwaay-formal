# Threat Model

## 1. Adversarial Surface

The analysis places the adversarial surface at the modeled `BatchReceive`
admission and composition boundary. A batch-composition adversary influences
the input vector supplied to that boundary, and the selected admission
semantics determine whether the resulting two-slot composition enters receiver
processing. The security question is therefore about identity-level batch
composition rather than failure of a cryptographic primitive.

## 2. Adversary Capabilities

Within the relaxed symbolic model, the batch-composition adversary can select
or arrange modeled entries, place and order them in the available batch slots,
and trigger executions admitted by R-semantics. When no party-uniqueness guard
exists, this includes reusing the same valid modeled protocol-principal
coordinate in multiple slots. The adversary thus supplies a composition of the
form

```text
slot 1 -> Party A
slot 2 -> Party A.
```

These capabilities operate over admissible symbolic inputs. They do not add a
new party identity or require the repeated coordinate to represent an
impersonated second party.

## 3. Capabilities Not Required

The repeated-party construction does not require recovery of secret keys,
breaking a KEM, forging signatures, forging an HMAC, impersonating a different
party, or modifying authenticated material. These statements delimit what the
construction relies upon; they do not assert that the current prototypes prove
the absence of those capabilities. Cryptographic operations and compromise
rules are outside the three admission prototypes.

## 4. Adversarial Goal

The adversary's modeled goal is not to recover a key or learn plaintext. It is
to form a same-batch repeated-party composition and have that composition
admitted when the identity guard is absent. In R-semantics, the bounded formal
consequence is reachable duplicate `ReceiverAccept` behavior: one matching
`Send(A,sid,m)` occurrence can correspond to two
`ReceiverAccept(A,sid,m,bid,rst)` occurrences in the same batch and
receiver-state context.

The associated semantic concern is loss of the intended party-level identity
interpretation. A batch expected to represent distinct modeled parties no
longer has that interpretation when one party coordinate occupies multiple
slots.

## 5. Attack/Consequence Chain

The threat model follows the canonical chain:

```text
DistinctPartyPerBatch removed
        -> same-batch repeated-party admission
        -> invalid batch composition
        -> duplicate receiver acceptance
        -> loss of intended party-level identity interpretation
```

The chain combines two evidence levels. The relaxed admission rule, the
repeated-party composition, and the duplicate-acceptance trace are supported
directly by the fixed-two-slot R-semantics model and its recorded Tamarin
results. Calling that composition invalid refers to its violation of the
specified party-level invariant. The final loss of identity interpretation is
the semantic conclusion drawn from those formal observations, not an
additional Tamarin event or lemma.

## 6. Excluded Consequences

The current threat model does not directly infer key compromise, loss of
secrecy, failure of `KEY` or `TEST` interfaces, correctness failure, an exploit
of a deployed implementation, duplicate installation, or corruption of
application-level state. The prototypes end at `ReceiverAccept` and do not
model output-key objects, consumer transitions, or application actions.

Historical composition evidence shows that upper-layer impact can be studied
under an explicit consumer assumption such as `C_install-v2`. That evidence is
not a consequence of the current threat model and is not part of the direct
RQ-v2 formal chain.

