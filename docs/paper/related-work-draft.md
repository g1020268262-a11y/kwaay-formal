# Related Work

## 1. K-Waay and Post-Quantum Asynchronous Key Exchange

K-Waay is the direct protocol context for this work. Collins et al. construct
an efficient, deniable, post-quantum X3DH-like deniable authenticated key
exchange from split-KEM techniques and introduce `BatchReceive` to model
receiver-side processing when ephemeral material is reused across several
inputs ([L1](https://www.usenix.org/conference/usenixsecurity24/presentation/collins)).
The K-Waay specification already states that, for a given `BatchReceive` call,
each input element corresponds to a different party. The present work does not
claim to discover that condition, correct the construction, or challenge the
computational proof. It instead asks what party-level interpretation the stated
condition maintains and whether its semantic necessity can be exhibited in a
bounded symbolic admission model.

This positioning separates two proof boundaries. K-Waay develops
computational security games and reductions for its DAKE and split-KEM
construction, including key indistinguishability, implicit authentication, and
deniability. RQ-v2 abstracts away those primitives and properties and compares
three admission semantics over a fixed-two-slot batch. Its evidence is
therefore not a full symbolic verification of K-Waay and does not transfer to
the computational guarantees established by Collins et al.

The broader asynchronous-messaging line reinforces this separation. Formal
analysis of Signal treats X3DH and the Double Ratchet as a multi-stage
authenticated key-exchange system ([L2](https://link.springer.com/article/10.1007/s00145-020-09360-1)),
while the X3DH specification explicitly distinguishes authentication,
protocol replay, key reuse, and identity binding
([L13](https://signal.org/docs/specifications/x3dh/)). Formal verification of
PQXDH translates a prose specification into ProVerif and CryptoVerif models
and makes the corresponding assumptions, ambiguities, and model boundaries
explicit ([L3](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan)).
These works share the asynchronous key-exchange setting and the need for
precise identity/session modeling; their main properties concern
cryptographic-session security, whereas RQ-v2 isolates party composition at
the `BatchReceive` admission boundary.

## 2. Formal Analyses of Secure Messaging

Formal secure-messaging research spans computational and symbolic methods.
The Signal analysis gives a computational account of X3DH and Double Ratchet
security ([L2](https://link.springer.com/article/10.1007/s00145-020-09360-1));
the PQXDH study uses both ProVerif and CryptoVerif to analyze authentication,
confidentiality, post-quantum forward secrecy, and co-deployment
([L3](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan));
and session-handling research uses Tamarin to study what happens when an
application composes several ratcheting chains into a conversation
([L4](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)).
Together, these analyses show why formalizing specification and application
details can reveal which assumptions belong to a security statement and where
an abstraction boundary lies. They do not imply that every modeled detail is
a vulnerability or that one verification method subsumes the others.

RQ-v2 uses Tamarin's multiset-rewriting trace framework
([L11](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48))
only to express a minimal admission lifecycle and its reachability and
correspondence properties. Tool choice is inherited methodology, not a
contribution. Although Tamarin supports substantially broader symbolic
analyses, the current prototypes explicitly encode one fixed-two-slot batch
and omit KEMs, signatures, HMAC computation, compromise, prekey cryptography,
Double Ratchet, and application behavior.

Secure-messaging taxonomies further distinguish trust establishment,
participant consistency, authentication, destination validation, speaker
consistency, and message-oriented properties
([L18](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf)).
RQ-v2 shares this discipline of separating property dimensions. Its target is
neither a general secure-messaging definition nor participant-list agreement;
it is the narrower question of whether two slots in one admitted batch retain
a distinct modeled-party interpretation.

## 3. Session- and Composition-Layer Security

A central lesson from composition research is that security established for a
component does not automatically determine the property of the object into
which that component is composed. In secure messaging, a conversation may
merge multiple individually protected ratcheting chains. The Tamarin analysis
of Signal's session-handling layer demonstrates that conversation-level
post-compromise security must therefore be analyzed separately from
single-session guarantees
([L4](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling)).
Analysis of healing across several groups similarly shows that update and
compromise effects depend on whether a user is represented through pairwise
channels or group-key state
([L20](https://www.usenix.org/conference/usenixsecurity21/presentation/cremers)).

General compositional-verification frameworks formalize the same methodological
concern through conditions such as protocol independence and preservation of
component properties in a multi-protocol environment
([L21](https://research.tue.nl/en/publications/a-framework-for-compositional-verification-of-security-protocols/)).
RQ-v2 is adjacent to this literature because it treats admission as a semantic
composition boundary: individually legitimate entries are composed into one
accepted `BatchReceive` batch. The shared dimension is the need to state and
check a composition condition. The objects and properties differ: prior work
studies session-to-conversation lifting, cross-group healing, or composition of
whole protocols, while RQ-v2 studies pairwise distinctness of modeled party
coordinates within one batch. Those studies do not prove
`DistinctPartyPerBatch`, and the RQ-v2 result does not establish their PCS or
protocol-independence properties.

## 4. Group Membership, State Consistency, and Administration

Secure group messaging separates several relationships that can otherwise be
collapsed under “membership.” TreeSync gives a formal and executable account
of MLS shared group state, including consistency, integrity, authentication,
and group-management operations
([L5](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez)).
Cryptographic administration adds authorization and membership-consistency
guarantees for administrator-controlled add and remove operations
([L6](https://www.usenix.org/system/files/usenixsecurity23-balbas.pdf)). Modular
analysis of MLS instead decomposes secure group messaging into cryptographic
components and derives a security predicate from the guarantees of those
components ([L7](https://eprint.iacr.org/2021/1083)). The secure-messaging
taxonomy places participant consistency alongside, but separately from,
authentication and message/transcript properties
([L18](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf)).

These works establish that member-indexed state, participant-list agreement,
membership authorization, and cryptographic group composition are substantive
security concerns. None of those notions is identical to RQ-v2's property.
Membership consistency asks whether parties share the intended view of a
group; administration asks who may change that group; TreeSync protects an
evolving group-state representation; and modular MLS concerns composition of
cryptographic primitives and predicates. `DistinctPartyPerBatch` instead
requires that two different positions of one admitted batch carry different
modeled party coordinates. RQ-v2 neither attributes this invariant to group
messaging nor transfers its bounded result to MLS or another group protocol.

## 5. Identity Binding, Names, and Authentication

Identity/name uniqueness is already recognized as a security-relevant semantic
assumption. Lupetti, Dillema, and Stabell-Kulø argue that principal names must
remain unique across appropriately correlated protocol sessions if those names
are to retain their intended meaning, and they discuss local and global means
of verifying that assumption
([L16](https://www.scitepress.org/papers/2006/24847/24847.pdf)). Chosen-name
analysis further shows that allowing an adversary to select or assign agent
names changes the formal attack surface and can produce type-flaw attacks
([L17](https://satoss.uni.lu/papers/CMR07.pdf)). These works limit RQ-v2's
novelty: the general idea that identity-bearing names require carefully scoped
semantic assumptions is not introduced here.

The specific identity relation is nevertheless different. The name-uniqueness
work concerns distinct and meaningful principal naming across correlated
sessions, particularly where one session's messages can be reused in another.
RQ-v2 assumes an explicit modeled party coordinate and asks whether the same
coordinate may occupy two different slots of one admitted batch. Its novelty
claim is therefore confined to normalizing and testing the K-Waay condition at
that boundary, not to identity uniqueness as a general concept.

Identity binding and authentication introduce further neighboring, but
non-equivalent, relations. Lowe's hierarchy distinguishes aliveness,
agreement, and injective agreement between protocol runs
([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)).
Formal misbinding analysis examines executions in which an endpoint, device,
or run becomes associated with the wrong identity
([L9](https://acris.aalto.fi/ws/portalfiles/portal/36903088/Sethi_Peltonen_Aura_Misbinding_Attacks_on_Secure_Device.pdf)).
UKS analysis for TLS with SDP likewise concerns a malicious binding between an
external identity and another endpoint's key, fingerprint, or session
([L15](https://www.rfc-editor.org/rfc/rfc8844.html)). RQ-v2's
repeated-party composition does not, on current evidence, establish that an
endpoint is bound to the wrong identity or that peers disagree about with whom
they share a key. **RQ-v2 is not established as a misbinding or UKS attack.**
The shared dimension is precise identity interpretation; the formal failure
relations remain distinct.

## 6. Replay, Deduplication, and Injectivity

Replay and injective correspondence are mature protocol-analysis concepts.
The X3DH specification discusses replayed initial messages, repeated
acceptance, and resulting key reuse as explicit security considerations
([L13](https://signal.org/docs/specifications/x3dh/)). Lowe's authentication
hierarchy characterizes injective agreement through a one-to-one relation
between relevant runs
([L10](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf)).
A later automated type-based analysis formalizes injective agreement through
unique matching begin/end resources and illustrates how one transmitted
message copied to two receiver processes violates that occurrence relation
([L19](https://www.sciencedirect.com/science/article/pii/S2352220815000528)).
RQ-v2 does not introduce injectivity or replay correspondence.

Its supported comparison concerns the boundary between occurrence and party
identity. In M-semantics, exact-message admission verifies
`receiver_accept_injective`: within the model's batch and receiver-state scope,
one matching sender occurrence cannot support two accept occurrences. At the
same time, `same_party_different_messages_batch_exists` is verified, so two
different messages and sender occurrences belonging to the same modeled party
can occupy the two slots. Thus, in this model, scoped occurrence injectivity
does not imply party-level batch uniqueness.

This result does not make message deduplication ineffective. Exact-message
deduplication controls message equality and, in the prototype, restores the
stated occurrence property. Party admission controls a separate coordinate,
`A1 != A2`. Authentication, integrity protection, replay handling, message
deduplication, and party uniqueness should therefore be evaluated against
their respective properties rather than treated as interchangeable repairs.

## 7. Positioning of This Work

Within the verified literature corpus and search scope, we found no work that
performs the complete `DistinctPartyPerBatch` removal, comparison, and
restoration analysis. This is a scoped search conclusion, not an exhaustive
claim about all literature. The closest prior work addresses the underlying
protocol, identity/name uniqueness, session composition, membership
consistency, or injective correspondence. Our analysis instead isolates their
intersection at the `BatchReceive` party-admission boundary.

Two contributions have strong support within that scope. First, RQ-v2 gives a
bounded formal analysis of K-Waay's already stated distinct-party
`BatchReceive` condition: R-semantics removes party-level admission,
P-semantics restores it, and the comparison records both an invalid
repeated-party composition and a reachable valid distinct-party batch. Second,
the M-semantics control demonstrates that scoped occurrence injectivity can
hold while party-level uniqueness still fails. Both statements are limited to
the symbolic fixed-two-slot admission models and their recorded properties.

Two further contributions require more moderate wording. The separation of
message-level uniqueness from party uniqueness is novel here only as the
controlled `BatchReceive` comparison; the abstract distinction between
messages and identities is established background. Likewise, treating the
different-party condition as a semantic invariant rather than prescribing a
specific enforcement check is a contribution of this K-Waay analysis, not a
new general concept of invariants or composition-layer security.

This positioning makes no claim that K-Waay omits its condition, that its
computational theorem is invalid, or that a deployed implementation violates
the invariant. It also makes no claim of cryptographic failure, misbinding,
UKS, `KEY`/`TEST` failure, arbitrary-length security, or unconditional
upper-layer impact.
