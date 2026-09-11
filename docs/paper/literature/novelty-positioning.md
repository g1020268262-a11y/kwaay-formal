# Literature Review Verdict

The verified corpus supports proceeding with a narrowly positioned RQ-v2
paper. The contribution is not a new cryptographic primitive, a new general
notion of identity uniqueness, or a new definition of injective agreement. It
is a bounded formal necessity analysis of K-Waay's stated distinct-party
`BatchReceive` condition, with an explicit separation between party identity,
message identity, and occurrence injectivity.

The corpus contains 21 verified works: 17 peer-reviewed academic works and 4
standards/protocol specifications. Seven collision-search families were
examined. Four works require explicit differentiation because they overlap a
substantial part of the vocabulary or reasoning (`L1`, `L16`, `L18`, and
`L19`), but none covers the complete RQ-v2 research chain.

## 1. Closest Prior Works

### 1.1 K-Waay (`L1`)

K-Waay is the direct protocol source. It defines a `BatchReceive` interface
whose vector entries include a claimed sender public key, prekey bundle, and
message; it explains receiver-side batching when ephemeral material is reused;
and it states that each element of one `BatchReceive` call corresponds to a
different party. Its formal contribution is a computational DAKE and split-KEM
security analysis, including key indistinguishability and deniability.

The inspected theorem is conditional on the construction and its game. The
paper does not remove the different-party condition, characterize the resulting
repeated-party composition, compare message deduplication with party admission,
or give the R/M/P symbolic necessity comparison. RQ-v2 must describe itself as
an analysis of a stated K-Waay condition, not as a correction of K-Waay's proof.

### 1.2 Session Handling in Secure Messaging (`L4`)

Cremers, Jacomme, and Naska show that security of X3DH/Double Ratchet building
blocks does not automatically determine the security of a conversation formed
by an application that manages and merges several ratcheting chains. Their
Tamarin model elevates the session-handling layer to a separate formal object.

This is the strongest methodological precedent for RQ-v2. The shared lesson is
that composition semantics above a cryptographic building block can carry an
independent proof obligation. The analyzed objects remain different: their
work studies session-to-conversation composition and PCS, whereas RQ-v2 studies
party-coordinate composition inside one fixed-two-slot receiver batch.

### 1.3 Names in Cryptographic Protocols (`L16`)

Lupetti, Dillema, and Stabell-Kulø argue that principal names must be unique
within an appropriate correlated-session scope if they are to retain their
intended protocol meaning. They also distinguish local and global ways to
verify that environmental assumption.

This work prevents a broad novelty claim that identity uniqueness as a
security-relevant semantic assumption is new. Its scope, however, is uniqueness
of names for principals across correlated sessions, especially where messages
may be reused. It does not impose pairwise distinct parties across entries of
one batch, remove a batch condition, or compare message-level and party-level
admission in a machine-checked model.

### 1.4 Automated Injective-Agreement Analysis (`L19`)

Sattarzadeh and Fallah formalize injective correspondence by consuming a unique
matching begin event for each end event. Their example of one message copied to
two receiver processes closely matches the occurrence-level shape of RQ-v2's
relaxed duplicate-acceptance witness.

The property dimension is nonetheless different from party uniqueness. A
model can preserve one-to-one send/accept correspondence while admitting two
different messages from the same party. That is exactly the distinction made
by RQ-v2's M-semantics result. The literature therefore supplies established
injectivity semantics; RQ-v2 contributes the controlled separation from
party-level batch identity in this protocol setting.

### 1.5 TreeSync (`L5`)

TreeSync gives a formal, executable account of authenticated group-management
state, consistency, and integrity for MLS. It establishes that membership- and
identity-bearing structured state can be a formal security object.

TreeSync's shared group-state consistency is not the same invariant as
within-one-batch party-coordinate uniqueness. RQ-v2 should cite it as adjacent
group/membership semantics, not as an antecedent or validation of
`DistinctPartyPerBatch`.

### 1.6 PQXDH Formal Verification (`L3`)

Bhargavan et al. translate a prose protocol specification into ProVerif and
CryptoVerif models, reveal specification ambiguities, and verify scoped
authentication and secrecy properties. This work supports the methodological
legitimacy of isolating a consequential specification-level detail.

Its object is the PQXDH handshake and cryptographic security. It neither uses a
multi-sender receiver batch nor analyzes party uniqueness.

### 1.7 Misbinding Analysis (`L9`)

Sethi, Peltonen, and Aura formalize cases where a compromised legitimate
participant causes a victim to associate an endpoint or protocol run with the
wrong identity. The work is close in its insistence that accepted protocol
objects retain the intended identity interpretation.

The failure relation differs. Misbinding and UKS concern an incorrect
identity-to-endpoint/key/session association; RQ-v2 concerns repeated use of
the same modeled party coordinate in two slots. The RQ-v2 witness must not be
labeled a misbinding or UKS attack without an additional matching definition
and evidence.

### 1.8 SoK: Secure Messaging (`L18`)

Unger et al. define participant consistency as agreement among honest parties
on the participant list and distinguish it from speaker consistency,
destination validation, authentication, and message-oriented properties. This
taxonomy supports RQ-v2's insistence on separating identity dimensions.

Participant-list agreement does not imply that two positions inside a batch
represent different parties. It is an adjacent property family, not the same
claim.

## 2. Similarity Matrix

| Work | Identity dimension | Composition layer | Formal method | Main property | Same as RQ-v2? | Difference |
| --- | --- | --- | --- | --- | --- | --- |
| K-Waay (`L1`) | Parties and partner/session identifiers | Multi-sender `BatchReceive` | Computational games and reductions | KIND, deniability, split-KEM security | No | States the different-party assumption but does not remove it or prove its semantic necessity. |
| Session Handling (`L4`) | Devices, sessions, conversations | Sessions merged into a conversation | Tamarin | Conversation-level PCS and clone detection | No | Same composition-layer motivation; different object and security property. |
| Names in Cryptographic Protocols (`L16`) | Principal-name uniqueness | Correlated protocol sessions | Conceptual protocol analysis | Names remain unique and meaningful | No | Names for distinct principals across sessions, not distinct parties across batch slots. |
| Injective-Agreement Analysis (`L19`) | Unique matching run/occurrence | Send/receive correspondence | Spi-calculus type system | Injective agreement and replay exclusion | No | Message/run injectivity can hold while same-party/different-message batch composition remains possible. |
| TreeSync (`L5`) | Members/clients in shared state | Group-management tree and epochs | F* and DY* | State consistency, integrity, authentication | No | Group-state agreement, not within-batch party cardinality. |
| PQXDH Verification (`L3`) | Initiator/responder identity and keys | Asynchronous handshake specification | ProVerif and CryptoVerif | Authentication and secrecy | No | Specification formalization precedent; no batch-composition invariant. |
| Misbinding (`L9`) | Endpoint-to-identity association | Pairing/bootstrap workflow | Applied pi calculus/ProVerif | Correct identity correspondence | No | Wrong association is distinct from repeated use of one correct party coordinate. |
| SoK: Secure Messaging (`L18`) | Participant-list view | Conversation security | Property systematization | Participant consistency and other messaging goals | No | Agreement on a participant list does not impose pairwise distinct batch entries. |

## 3. Collision Analysis

### Search evidence

The search tested the complete target, not merely shared keywords. Candidate
works were checked for all of the following:

1. a batch, group, or vector whose different components must denote different
   parties;
2. removal of that distinct-party restriction;
3. a resulting repeated-party composition;
4. an explicit comparison between message uniqueness and party uniqueness;
5. a formal necessity/restoration argument.

The active query families covered batch admission/processing, party and
participant uniqueness, identity invariants/consistency, misbinding/UKS,
group-membership consistency, session/protocol composition, and
replay/deduplication/injectivity/duplicate processing. The closest collision
candidates are:

| Candidate | Overlap | Missing from candidate | Assessment |
| --- | --- | --- | --- |
| K-Waay (`L1`) | Exact protocol, `BatchReceive`, and different-party condition | No removal/necessity comparison; no message-dedup control | `POTENTIAL COLLISION` at source-condition level only |
| Names in Cryptographic Protocols (`L16`) | Scoped uniqueness of identity-bearing names as a semantic assumption | Different scope and object; no batch/vector experiment | `POTENTIAL COLLISION` at conceptual-invariant level only |
| SoK: Secure Messaging (`L18`) | Participant consistency separated from message properties | Inter-party list agreement rather than intra-batch distinctness | `POTENTIAL COLLISION` at taxonomy level only |
| Injective-Agreement Analysis (`L19`) | One send copied to two receives; precise replay/injectivity semantics | No party-uniqueness predicate or same-party/different-message comparison | `POTENTIAL COLLISION` at occurrence-property level only |

### Verdict

**NO DIRECT COLLISION FOUND**

Within the verified corpus/search scope, no work was found that performs the
complete `DistinctPartyPerBatch`-style invariant necessity analysis for
K-Waay: removing the same-batch distinct-party condition, deriving
repeated-party batch composition and duplicate acceptance, contrasting
message-level deduplication with party-level uniqueness, and demonstrating a
party-admission restoration in a bounded formal model.

This verdict is scoped evidence, not a universal literature-exhaustion claim.
The four potential collisions above must be discussed in Related Work so that
the paper does not obtain novelty merely by renaming established concepts.

## 4. Novelty That Is Actually Supportable

### A. Strong novelty

#### N1 — Applying formal analysis to K-Waay's distinct-party `BatchReceive` condition

**Status: `SUPPORTED`**

K-Waay states the condition and proves computational security for its DAKE
construction, but the inspected source does not conduct the RQ-v2
removal/restoration experiment. None of the other verified works targets this
K-Waay condition. The support is limited to the bounded symbolic
fixed-two-slot admission model and must not be generalized to full K-Waay or a
deployed system.

#### N3 — Showing scoped occurrence injectivity can hold while party uniqueness fails

**Status: `SUPPORTED`**

Lowe (`L10`) and Sattarzadeh--Fallah (`L19`) establish the meaning of
occurrence/run injectivity. The RQ-v2 M-semantics evidence adds the
protocol-specific separation: exact-message admission verifies the scoped
`receiver_accept_injective` property while a same-party/different-message batch
remains reachable. No verified prior work gives this exact controlled
comparison for `BatchReceive`.

### B. Moderate novelty

#### N2 — Separating party uniqueness from message-level deduplication

**Status: `PARTIALLY SUPPORTED`**

The RQ-v2 comparison provides direct bounded evidence that `m1 != m2` does not
imply `A1 != A2`, and its M-semantics model makes the distinction operational.
However, secure-messaging taxonomies, replay/injectivity work, and
identity-binding literature already distinguish participant properties from
message/run properties. The defensible novelty is the explicit K-Waay
`BatchReceive` model comparison, not the abstract observation that identities
and messages are different objects.

#### N4 — Treating same-batch party distinctness as a semantic invariant rather than a specific implementation check

**Status: `PARTIALLY SUPPORTED`**

The RQ-v2 semantic contract and R/P comparison support this treatment for the
modeled boundary. Session-handling (`L4`), name uniqueness (`L16`), TreeSync
(`L5`), and compositional verification (`L21`) already establish the broader
idea that interface conditions and composition semantics can be security
relevant. The supportable contribution is the particular normalization and
analysis of K-Waay's condition, not the general invariant-versus-check framing.

### C. Not novel

The following must be presented as inherited method or vocabulary, not RQ-v2
novelty:

- symbolic protocol analysis with Tamarin (`L11`);
- injective versus non-injective agreement (`L10`, `L19`);
- the general importance of identity/name binding (`L9`, `L15`–`L17`);
- participant or membership consistency in secure group messaging (`L5`,
  `L6`, `L12`, `L18`);
- the observation that higher-layer composition can invalidate a property of
  a lower-level building block (`L4`, `L20`, `L21`).

## 5. Reviewer Positioning

**Reviewer question:** “Is this merely checking an explicit precondition?”

**Literature-grounded answer:** The paper should concede that the
different-party condition is explicit in K-Waay and that RQ-v2 does not expose
a violation of executions satisfying it. The contribution is instead to make
the condition's semantic role and necessity explicit at a separate admission
boundary.

Session-handling work shows why this is a legitimate formal-analysis target:
properties of secure lower-level sessions do not automatically lift through a
layer that composes them into a conversation. RQ-v2 applies the same kind of
layer discipline to a different object—entries composed into a receiver batch.
It asks which identity relation the batch is intended to preserve and what
happens in the bounded model when that relation is removed.

TreeSync and cryptographic-administration work show that membership-bearing
state and update semantics can be formal security objects, but their
consistency and authorization properties do not subsume within-batch
party-coordinate distinctness. PQXDH verification shows that formalizing a
seemingly local prose-level specification detail can expose the exact
assumptions on which a security statement depends; it does not imply that every
such detail is a vulnerability.

Misbinding work supplies the necessary caution on identity terminology. RQ-v2
does not show that an endpoint is bound to the wrong identity. It shows that
one modeled party coordinate can occupy two slots when a distinct-party
admission condition is removed. Similarly, injective-agreement literature
explains the duplicate-acceptance witness but does not replace the party-level
property: RQ-v2's message-dedup model is the evidence that the two dimensions
can diverge.

The reviewer-facing value is therefore the controlled necessity comparison:
R-semantics admits the invalid identity composition, M-semantics restores a
message/occurrence property without restoring party uniqueness, and
P-semantics restores the intended party interpretation while retaining a
reachable valid batch. This answer remains explicitly bounded and does not
claim a deployed flaw, a cryptographic break, or failure of K-Waay's stated
security theorem.

## 6. Safe Novelty Language

The following statements are supported for paper use:

1. “We isolate K-Waay's stated distinct-party `BatchReceive` condition as a
   party-level identity invariant and analyze its semantic role in a bounded
   symbolic fixed-two-slot admission model.”
2. “We provide a controlled comparison in which removing party-level admission
   permits repeated-party batch composition, while party-level admission
   restores the intended distinct-party interpretation and retains a reachable
   valid batch.”
3. “We distinguish exact-message deduplication and scoped occurrence
   injectivity from party uniqueness: in the message-deduplication model,
   occurrence injectivity holds although a same-party/different-message batch
   remains reachable.”
4. “Within the examined literature, the closest work studies K-Waay's
   cryptographic construction, session/conversation composition, principal-name
   uniqueness, participant consistency, identity binding, or injective
   correspondence; our analysis focuses on their intersection at the
   `BatchReceive` party-admission boundary.”

These statements do not assert literature priority beyond the examined scope,
deployed behavior, cryptographic failure, `KEY`/`TEST` failure, or consequences
outside the current acceptance boundary.
