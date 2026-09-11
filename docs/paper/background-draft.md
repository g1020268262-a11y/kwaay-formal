# Background

## 1. BatchReceive Abstraction

The part of K-Waay relevant to this work is the `BatchReceive` abstraction: a
single receiver-side operation processes multiple entries as one batch. The
batch does more than collect independent inputs. Its slots jointly describe
which modeled parties contribute to one admitted receiver execution, so the
relationship among entries is part of the batch semantics.

We isolate this admission and composition boundary rather than reconstructing
the complete protocol. In particular, the present background does not require
the full KEM construction, Double Ratchet processing, every protocol message,
or algorithmic details unrelated to the identity condition. The later formal
model represents a symbolic fixed-two-slot instance of this abstraction.

## 2. Batch Entries and Party Association

For the analysis, we write an abstract batch entry as

```text
E = (A, sid, m),
```

where `A` is the modeled protocol-principal coordinate, `sid` is a sender
session or sender-occurrence coordinate, and `m` is a message coordinate. This
tuple is our symbolic abstraction of the information needed to distinguish
identity dimensions at admission. It is not presented as a wire-format tuple
or as notation used verbatim by the original protocol description.

The association between an entry and a party is expressed by
`party(E) = A`. The coordinate `A` is a formal protocol-principal identifier;
it is not identified with an account record, API object, public-key encoding,
or other deployed representation. Likewise, `sid` and `m` remain separate
from `A`, even when they originate from an execution associated with that
party.

## 3. Identity Hierarchy

The model distinguishes six identity dimensions. Party identity identifies a
modeled protocol principal. Session identity distinguishes sender sessions or
occurrences, message identity distinguishes produced messages, and slot
identity distinguishes positions within a batch. Batch identity identifies one
batch execution, while receiver-state identity identifies the receiver state
associated with that execution.

These coordinates do not collapse into one another. The same party can have
multiple sessions, produce multiple messages, and participate in different
batches. A party can also occupy different slot numbers across different
batches. Consequently, different sessions, messages, or slots do not imply
different parties. The condition studied here is narrower: it relates distinct
slots *within one admitted batch*. It neither imposes global uniqueness on a
party nor prevents that party from participating again in another batch.

## 4. Distinct-Party Batch Condition

We give the distinct-party condition the normalized name
`DistinctPartyPerBatch`. For entries `E_i` and `E_j` in one admitted batch, it
requires

```text
i != j  =>  party(E_i) != party(E_j).
```

Thus, two different positions in one admitted batch must represent two
different modeled protocol-principal coordinates. The name and formula are the
paper's formal normalization of the protocol's natural-language distinct-party
condition; we do not attribute this exact identifier or mathematical notation
to the original authors.

`DistinctPartyPerBatch` is an identity-level invariant because it determines
the party interpretation of the batch as a whole. The machine-checked
prototypes instantiate the condition for exactly two slots. The general
notation above defines the semantic condition but does not claim an
arbitrary-size proof.

## 5. Related Security Dimensions

Authentication, integrity, replay handling, message deduplication, and
explicit confirmation constrain relations other than same-batch party
uniqueness. Authentication and integrity can relate a message to an origin and
protect authenticated material. Replay handling and deduplication can constrain
reuse or equality of messages. An HMAC can contribute authenticity, integrity,
or confirmation evidence under its surrounding protocol assumptions. None of
these descriptions makes a judgment that those mechanisms fail at their stated
purposes.

The distinction needed for RQ-v2 is logical: message inequality does not imply
party inequality. Two entries can satisfy `m1 != m2` while also satisfying
`A1 = A2`. A message-level condition therefore cannot, by that condition alone,
establish `DistinctPartyPerBatch`. Earlier repository work involving HMAC or
replay remains historical background; the direct evidence for the present
question comes from the frozen R-, M-, and P-semantics admission prototypes.

