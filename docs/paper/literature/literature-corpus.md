# RQ-v2 Verified Literature Corpus

## Scope and Counting

This corpus was assembled for novelty positioning of the frozen RQ-v2 claim:
the necessity of `DistinctPartyPerBatch` for the intended party-level identity
interpretation of one admitted, fixed-two-slot `BatchReceive` batch. It does not
change that claim or extend the formal evidence.

- Verified research works: **21**
- Peer-reviewed academic works: **17**
- Standards and protocol specifications: **4** (`L12`--`L15`)
- Conference and extended journal versions of the Sethi--Peltonen--Aura
  misbinding study are counted once (`L9`).
- Entry into this corpus requires bibliographic verification from a publisher,
  standards body, author/institutional copy, or official protocol page, plus
  inspection of the abstract and the sections identified below.

Collision levels mean: `NONE` = background only; `LOW` = adjacent vocabulary or
method; `MEDIUM` = a substantive overlap that must be distinguished in the
paper; `HIGH` = the same research chain or a likely direct priority conflict.
No included work is classified `HIGH`.

## A. Direct Protocol and Secure-Messaging Context

### L1 — Collins et al., K-Waay

- **Full citation:** Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh
  Nguyen, Nicolas Rolin, and Serge Vaudenay. “K-Waay: Fast and Deniable
  Post-Quantum X3DH without Ring Signatures.” *33rd USENIX Security Symposium*,
  2024, pp. 433–450. Full version: IACR ePrint 2024/120.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2024.
- **Research problem:** Efficient deniable post-quantum asynchronous key
  agreement with receiver-side ephemeral-key reuse.
- **Protocol/system:** K-Waay; X3DH-like DAKE using split-KEM.
- **Formal method:** Computational security games and reductions, including
  KIND, deniability, split-KEM unforgeability, and `IND-1BatchCCA`.
- **Security/property target:** Key indistinguishability, implicit
  authentication, deniability, and safe ephemeral-key reuse in the stated
  game.
- **Identity dimension:** Parties and partner/session identifiers in a
  multi-sender `BatchReceive` interface.
- **Closest relation to RQ-v2:** The paper defines `BatchReceive` over a vector
  and explicitly assumes that every element of a given call corresponds to a
  different party. This is the natural-language condition normalized by
  RQ-v2.
- **Key difference:** The security theorem is conditional on that construction
  and assumption. The inspected paper does not remove the condition, compare
  party uniqueness with message deduplication, or prove the condition's
  semantic necessity by a relaxed/party-admission symbolic comparison.
- **Use in our paper:** Direct protocol source, exact origin and scope of the
  condition, and boundary between K-Waay's computational proof and RQ-v2's
  bounded admission analysis.
- **Collision level:** `MEDIUM` — exact protocol and condition, but not the same
  necessity analysis.
- **Content checked:** Abstract; contributions; DAKE syntax; Sections 4.1–4.2;
  K-Waay construction around Figure 10; the different-party assumption; and
  the security theorem.
- **Primary source:** [USENIX publication page](https://www.usenix.org/conference/usenixsecurity24/presentation/collins);
  [full version, IACR ePrint 2024/120](https://eprint.iacr.org/2024/120).

### L2 — Cohn-Gordon et al., Formal Signal Analysis

- **Full citation:** Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke
  Garratt, and Douglas Stebila. “A Formal Security Analysis of the Signal
  Messaging Protocol.” *Journal of Cryptology* 33, 2020, pp. 1914–1983.
  DOI: 10.1007/s00145-020-09360-1.
- **Venue quality/type:** Peer-reviewed cryptography journal; extended work
  following the EuroS&P 2017 version.
- **Year:** 2020.
- **Research problem:** Establish formal security guarantees for Signal's
  X3DH and Double Ratchet as a multi-stage authenticated key-exchange system.
- **Protocol/system:** Signal X3DH and Double Ratchet.
- **Formal method:** Computational multi-stage AKE model and proofs based on a
  formal protocol description derived from the implementation.
- **Security/property target:** Authentication and key-security properties,
  including forward- and post-compromise-oriented guarantees at the modeled
  cryptographic-session layer.
- **Identity dimension:** Peer agreement and session/ratchet-chain identity.
- **Closest relation to RQ-v2:** Demonstrates rigorous analysis of an
  asynchronous secure-messaging handshake and its session evolution.
- **Key difference:** It studies cryptographic session security, not identity
  uniqueness among components of one receiver batch.
- **Use in our paper:** Separate lower-level session guarantees from RQ-v2's
  admission composition semantics.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, protocol scope, multi-stage model, and stated
  security results.
- **Primary source:** [Springer journal article](https://link.springer.com/article/10.1007/s00145-020-09360-1).

### L3 — Bhargavan et al., PQXDH Formal Verification

- **Full citation:** Karthikeyan Bhargavan, Charlie Jacomme, Franziskus Kiefer,
  and Rolfe Schmidt. “Formal Verification of the PQXDH Post-Quantum Key
  Agreement Protocol for End-to-End Secure Messaging.” *33rd USENIX Security
  Symposium*, 2024, pp. 469–486.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2024.
- **Research problem:** Convert the English PQXDH specification into precise
  formal models and verify its security and co-deployment behavior.
- **Protocol/system:** Signal PQXDH.
- **Formal method:** ProVerif and CryptoVerif models.
- **Security/property target:** Authentication, confidentiality,
  post-quantum forward secrecy, and co-deployment properties.
- **Identity dimension:** Initiator/responder identities and keys bound to an
  asynchronous handshake.
- **Closest relation to RQ-v2:** Shows that formalizing a specification-level
  detail can expose assumptions and ambiguities that are invisible in a
  high-level cryptographic narrative.
- **Key difference:** Its targets are PQXDH cryptographic security and
  specification fidelity, not repeated-party batch admission.
- **Use in our paper:** Methodological precedent for a narrowly scoped formal
  study of a specification-level condition.
- **Collision level:** `LOW`.
- **Content checked:** Abstract; formal-model methodology; security goals;
  specification findings; and model boundaries.
- **Primary source:** [USENIX publication page](https://www.usenix.org/conference/usenixsecurity24/presentation/bhargavan).

### L13 — Marlinspike and Perrin, X3DH Specification

- **Full citation:** Moxie Marlinspike and Trevor Perrin. “The X3DH Key
  Agreement Protocol.” Signal specification, Revision 1, 4 November 2016.
- **Venue quality/type:** Protocol specification; not counted as a
  peer-reviewed paper.
- **Year:** 2016.
- **Research problem:** Specify asynchronous mutually authenticated key
  agreement using identity keys, signed prekeys, and optional one-time prekeys.
- **Protocol/system:** X3DH.
- **Formal method:** Normative algorithm and security-considerations text; no
  machine-checked proof in this document.
- **Security/property target:** Mutual authentication, forward secrecy,
  deniability, replay/key-reuse handling, server trust, and identity binding.
- **Identity dimension:** Binding of identity keys and auxiliary identity data
  to a two-party handshake.
- **Closest relation to RQ-v2:** Clarifies that replay, prekey reuse, and
  identity binding are separate protocol dimensions.
- **Key difference:** It has no batch of multiple claimed senders and no
  within-batch party-distinctness property.
- **Use in our paper:** Protocol background and a careful separation of replay
  and identity-binding terminology from party uniqueness.
- **Collision level:** `NONE`.
- **Content checked:** Sections 2–3 and Security Considerations 4.1–4.8,
  especially protocol replay, key reuse, and identity binding.
- **Primary source:** [Signal X3DH specification](https://signal.org/docs/specifications/x3dh/).

### L14 — Kret and Schmidt, PQXDH Specification

- **Full citation:** Ehren Kret and Rolfe Schmidt. “The PQXDH Key Agreement
  Protocol.” Signal specification, Revision 3, 24 May 2023; updated 23 January
  2024.
- **Venue quality/type:** Protocol specification; not counted as a
  peer-reviewed paper.
- **Year:** 2023/2024.
- **Research problem:** Specify an asynchronous post-quantum X3DH extension
  combining elliptic-curve and post-quantum KEM material.
- **Protocol/system:** PQXDH.
- **Formal method:** Normative algorithm and security-considerations text.
- **Security/property target:** Authentication, post-quantum forward secrecy,
  replay/key-reuse handling, deniability, identity binding, KEM
  re-encapsulation resistance, and key identifiers.
- **Identity dimension:** Two-party identity/public-key binding and session/key
  separation.
- **Closest relation to RQ-v2:** Provides adjacent vocabulary for replay,
  reuse, identities, and asynchronous prekey processing.
- **Key difference:** It does not define a multi-party receiver batch or a
  party-coordinate uniqueness invariant.
- **Use in our paper:** Background and a boundary against conflating replay or
  key reuse with same-batch party composition.
- **Collision level:** `NONE`.
- **Content checked:** Protocol overview and Security Considerations 4.1–4.13,
  especially replay, key reuse, identity binding, KEM re-encapsulation, and key
  identifiers.
- **Primary source:** [Signal PQXDH specification](https://signal.org/docs/specifications/pqxdh/).

## B. Composition, Session, and Membership Semantics

### L4 — Cremers, Jacomme, and Naska, Session Handling

- **Full citation:** Cas Cremers, Charlie Jacomme, and Aurora Naska. “Formal
  Analysis of Session-Handling in Secure Messaging: Lifting Security from
  Sessions to Conversations.” *32nd USENIX Security Symposium*, 2023,
  pp. 1235–1252.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2023.
- **Research problem:** Determine whether security established for a single
  ratcheting chain lifts through the application's management and merging of
  multiple sessions into a conversation.
- **Protocol/system:** Signal/Sesame session handling and Double Ratchet
  abstractions.
- **Formal method:** Tamarin symbolic modeling plus experimental scenarios.
- **Security/property target:** Conversation-level post-compromise security and
  clone detection.
- **Identity dimension:** Devices, sessions/ratcheting chains, and their
  composition into a conversation.
- **Closest relation to RQ-v2:** Strong precedent that a layer which composes
  secure lower-level objects has independent semantics worthy of formal
  analysis.
- **Key difference:** It analyzes session-to-conversation composition and PCS,
  not party-coordinate uniqueness across one `BatchReceive` input vector.
- **Use in our paper:** Primary response to “this is merely a precondition”:
  explicit composition conditions can determine the meaning of higher-layer
  security claims.
- **Collision level:** `MEDIUM`.
- **Content checked:** Introduction, motivation, abstraction/model, related
  work, results, and limitations.
- **Primary source:** [USENIX publication page](https://www.usenix.org/conference/usenixsecurity23/presentation/cremers-session-handling).

### L5 — Wallez et al., TreeSync

- **Full citation:** Théophile Wallez, Jonathan Protzenko, Benjamin Beurdouche,
  and Karthikeyan Bhargavan. “TreeSync: Authenticated Group Management for
  Messaging Layer Security.” *32nd USENIX Security Symposium*, 2023,
  pp. 1217–1233.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2023.
- **Research problem:** Give a precise, executable, verified account of MLS
  shared group-state and tree synchronization.
- **Protocol/system:** MLS TreeSync.
- **Formal method:** F* executable specification and DY* symbolic proofs.
- **Security/property target:** Group-state consistency, integrity,
  authentication, and correct group-management operations.
- **Identity dimension:** Members/clients represented in shared group state.
- **Closest relation to RQ-v2:** Treats member relationships and consistency as
  semantic properties of a structured protocol state.
- **Key difference:** TreeSync concerns agreement on evolving group state; it
  does not require distinct parties across slots of one K-Waay receiver batch.
- **Use in our paper:** Adjacent formal group-management work and a precise
  contrast between group consistency and within-batch uniqueness.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, group-management model, formal specification,
  stated consistency/integrity/authentication guarantees, and composition with
  MLS.
- **Primary source:** [USENIX publication page](https://www.usenix.org/conference/usenixsecurity23/presentation/wallez).

### L6 — Balbás, Collins, and Vaudenay, Cryptographic Administration

- **Full citation:** David Balbás, Daniel Collins, and Serge Vaudenay.
  “Cryptographic Administration for Secure Group Messaging.” *32nd USENIX
  Security Symposium*, 2023, pp. 1253–1270.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2023.
- **Research problem:** Provide cryptographic guarantees for authorization and
  administration of dynamic group membership.
- **Protocol/system:** Administrated continuous group key agreement (A-CGKA)
  and an MLS-oriented construction.
- **Formal method:** Game-based definitions, modular constructions, and
  reductions.
- **Security/property target:** Authorized add/remove operations, membership
  consistency, and protection of group membership/control messages.
- **Identity dimension:** Group members and administrators over membership
  transitions.
- **Closest relation to RQ-v2:** Makes membership semantics a formal security
  target rather than leaving it solely to an application check.
- **Key difference:** It analyzes long-lived group administration and
  authorization, not the distinctness of entries inside one batch.
- **Use in our paper:** Position RQ-v2 next to, but not as an instance of,
  membership-administration security.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, group-administration motivation, three stated
  membership aspects, A-CGKA abstraction, and security scope.
- **Primary source:** [USENIX paper](https://www.usenix.org/system/files/usenixsecurity23-balbas.pdf).

### L7 — Alwen et al., Modular MLS

- **Full citation:** Joël Alwen, Sandro Coretti, Yevgeniy Dodis, and Yiannis
  Tselekounis. “Modular Design of Secure Group Messaging Protocols and the
  Security of MLS.” *ACM CCS 2021*, pp. 1463–1483.
  DOI: 10.1145/3460120.3484820.
- **Venue quality/type:** ACM CCS; peer-reviewed security conference.
- **Year:** 2021.
- **Research problem:** Define security for full secure group messaging and
  derive MLS security compositionally from cryptographic components.
- **Protocol/system:** MLS, TreeKEM/RTreeKEM, CGKA, and forward-secure group
  AEAD.
- **Formal method:** Game-based modular definitions, safety predicates, and
  composition reductions.
- **Security/property target:** Full secure-group-messaging confidentiality and
  authenticity expressed through component security predicates.
- **Identity dimension:** Members and epochs appear in group security state,
  but the main abstraction is cryptographic component composition.
- **Closest relation to RQ-v2:** Both isolate a component boundary and ask what
  a composed object can mean securely.
- **Key difference:** The MLS work composes cryptographic primitives and
  predicates; it does not analyze repeated identity coordinates inside one
  batch input.
- **Use in our paper:** Broader composition framework and contrast with
  RQ-v2's narrower admission-semantic decomposition.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, SGM security predicate, three-component MLS
  decomposition, and composition result.
- **Primary source:** [IACR ePrint 2021/1083](https://eprint.iacr.org/2021/1083).

### L8 — Alwen et al., Continuous Group Key Agreement

- **Full citation:** Joël Alwen, Sandro Coretti, Daniel Jost, and Marta
  Mularczyk. “Continuous Group Key Agreement with Active Security.” *TCC 2020*,
  LNCS 12552, pp. 261–290. DOI: 10.1007/978-3-030-64378-2_10.
- **Venue quality/type:** TCC; peer-reviewed cryptography conference.
- **Year:** 2020.
- **Research problem:** Establish active security for long-lived dynamic group
  key agreement without a trusted group manager.
- **Protocol/system:** CGKA with dynamic membership; foundational context for
  TreeKEM/MLS.
- **Formal method:** Game-based definitions, constructions, and proofs.
- **Security/property target:** Forward secrecy, post-compromise security, and
  active security under membership updates.
- **Identity dimension:** Dynamic group members over epochs.
- **Closest relation to RQ-v2:** Formalizes security around changing participant
  sets.
- **Key difference:** Its unit is a dynamic group and cryptographic key state,
  not party distinctness among simultaneous batch components.
- **Use in our paper:** Background for the group-membership line of related
  work.
- **Collision level:** `NONE`.
- **Content checked:** Abstract, CGKA problem, dynamic membership, active
  security, and connection to secure group messaging.
- **Primary source:** [ETH Zürich publication page](https://crypto.ethz.ch/publications/ACJM20.html).

### L12 — Barnes et al., MLS Protocol

- **Full citation:** Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon
  Millican, Emad Omara, and Katriel Cohn-Gordon. “The Messaging Layer Security
  (MLS) Protocol.” RFC 9420, July 2023. DOI: 10.17487/RFC9420.
- **Venue quality/type:** IETF Standards Track RFC; not counted as a
  peer-reviewed paper.
- **Year:** 2023.
- **Research problem:** Standardize efficient asynchronous group key
  establishment and authenticated messaging with dynamic membership.
- **Protocol/system:** MLS.
- **Formal method:** Normative protocol specification; no single proof method
  in the RFC itself.
- **Security/property target:** Group authentication, confidentiality,
  forward secrecy, and post-compromise security across epochs.
- **Identity dimension:** Authenticated clients, members, leaves, and epoch
  group state.
- **Closest relation to RQ-v2:** Shows a protocol state whose interpretation is
  explicitly membership-indexed.
- **Key difference:** An MLS member/client and ratchet-tree state are not the
  RQ-v2 `BatchReceive` party coordinate or fixed-two-slot batch.
- **Use in our paper:** Standards context and terminology boundary.
- **Collision level:** `NONE`.
- **Content checked:** Architecture and terminology, group state, members,
  ratchet tree, proposals/commits, and security considerations.
- **Primary source:** [RFC Editor HTML](https://www.rfc-editor.org/rfc/rfc9420.html).

### L18 — Unger et al., SoK: Secure Messaging

- **Full citation:** Nik Unger, Sergej Dechand, Joseph Bonneau, Sascha Fahl,
  Henning Perl, Ian Goldberg, and Matthew Smith. “SoK: Secure Messaging.” *2015
  IEEE Symposium on Security and Privacy*, pp. 232–249.
  DOI: 10.1109/SP.2015.22.
- **Venue quality/type:** IEEE S&P; peer-reviewed systematization paper.
- **Year:** 2015.
- **Research problem:** Systematize secure-messaging goals, designs, and
  trade-offs.
- **Protocol/system:** Secure messaging broadly, including group conversation
  security.
- **Formal method:** Comparative systematization and property definitions, not
  a machine-checked protocol proof.
- **Security/property target:** Trust establishment, conversation security, and
  transport privacy; participant consistency is defined as agreement among
  honest parties on the participant list.
- **Identity dimension:** Conversation participants and their shared view.
- **Closest relation to RQ-v2:** Provides established participant-consistency
  vocabulary and separates it from message/speaker/transcript properties.
- **Key difference:** Participant consistency is inter-party agreement about a
  group list, not intra-batch pairwise distinctness of party coordinates.
- **Use in our paper:** Taxonomic support for keeping participant identity and
  message-level properties separate.
- **Collision level:** `MEDIUM`.
- **Content checked:** Abstract, contributions, conversation-security property
  definitions, especially participant consistency, destination validation, and
  speaker consistency.
- **Primary source:** [author-hosted extended paper](https://people.eecs.berkeley.edu/~raluca/cs261-f15/readings/sok_secure_messaging.pdf).

### L20 — Cremers, Hale, and Kohbrok, Cross-Group Healing

- **Full citation:** Cas Cremers, Britta Hale, and Konrad Kohbrok. “The
  Complexities of Healing in Secure Group Messaging: Why Cross-Group Effects
  Matter.” *30th USENIX Security Symposium*, 2021, pp. 1847–1864.
- **Venue quality/type:** USENIX Security; peer-reviewed security conference.
- **Year:** 2021.
- **Research problem:** Determine how post-compromise healing behaves when one
  user participates in several groups.
- **Protocol/system:** Signal-style pairwise channels, ART, TreeKEM, and an MLS
  draft.
- **Formal method:** Formal game-based security definitions, constructions,
  and cross-group scenario analysis.
- **Security/property target:** Cross-group post-compromise confidentiality and
  authentication healing.
- **Identity dimension:** A user represented across concurrent and future
  groups.
- **Closest relation to RQ-v2:** Shows that identity/context composition across
  containers can change the property obtained from a secure component.
- **Key difference:** Cross-group healing concerns shared compromise/update
  effects, not duplicate party coordinates within one batch.
- **Use in our paper:** Composition-layer precedent and scope contrast.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, individual-groups versus pairwise-channels
  comparison, cross-group results, contributions, and formal security scope.
- **Primary source:** [USENIX publication page](https://www.usenix.org/conference/usenixsecurity21/presentation/cremers).

### L21 — Andova et al., Compositional Verification Framework

- **Full citation:** Suzana Andova, Cas Cremers, Kristian Gjøsteen, Sjouke
  Mauw, Stig F. Mjølsnes, and Saša Radomirović. “A Framework for Compositional
  Verification of Security Protocols.” *Information and Computation* 206(2–4),
  2008, pp. 425–459. DOI: 10.1016/j.ic.2007.07.002.
- **Venue quality/type:** Peer-reviewed formal-methods journal.
- **Year:** 2008.
- **Research problem:** Make verification of large protocols tractable by
  proving component properties and conditions for safe composition.
- **Protocol/system:** General security protocols; WiMAX case study.
- **Formal method:** Trace semantics, protocol-independence theorems, and
  automated component analysis.
- **Security/property target:** Preservation of authentication and secrecy
  under protocol composition.
- **Identity dimension:** Agents and sessions across component protocols.
- **Closest relation to RQ-v2:** Establishes that composition conditions are
  substantive proof obligations rather than incidental syntax.
- **Key difference:** It composes whole protocols and proves independence
  results; it does not study identity uniqueness within a data batch.
- **Use in our paper:** General formal-composition background.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, composition motivation, protocol independence,
  theorem scope, and WiMAX application.
- **Primary source:** [peer-reviewed institutional record and manuscript](https://research.tue.nl/en/publications/a-framework-for-compositional-verification-of-security-protocols/).

## C. Identity Binding, Authentication, and Correspondence

### L9 — Sethi, Peltonen, and Aura, Misbinding

- **Full citation:** Mohit Sethi, Aleksi Peltonen, and Tuomas Aura. “Misbinding
  Attacks on Secure Device Pairing and Bootstrapping.” *AsiaCCS 2019*,
  pp. 453–464. DOI: 10.1145/3321705.3329813. Extended as “Formal Verification
  of Misbinding Attacks on Secure Device Pairing and Bootstrapping,” *Journal
  of Information Security and Applications* 51 (2020), article 102461,
  DOI: 10.1016/j.jisa.2020.102461. Counted as one research work.
- **Venue quality/type:** Peer-reviewed security conference plus extended
  peer-reviewed journal article.
- **Year:** 2019/2020.
- **Research problem:** Analyze how a compromised legitimate participant can
  cause an honest endpoint or user to associate a protocol endpoint with the
  wrong identity.
- **Protocol/system:** Secure device pairing, Bluetooth, and IoT device
  bootstrapping.
- **Formal method:** Applied pi calculus/ProVerif with correspondence
  properties and case-study models.
- **Security/property target:** Correct association between protocol
  participants, devices, users, and identities.
- **Identity dimension:** Endpoint-to-identity association.
- **Closest relation to RQ-v2:** Both require precise separation between an
  accepted protocol object and its intended party interpretation.
- **Key difference:** Misbinding maps an endpoint/key/session to the wrong
  identity; RQ-v2 admits the same modeled party twice in one batch. The RQ-v2
  trace is not thereby a misbinding or UKS attack.
- **Use in our paper:** Define the boundary between identity binding and party
  uniqueness, and motivate correspondence-level identity reasoning.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, attacker role, pairing/bootstrapping cases,
  correspondence properties, ProVerif analysis, and double-misbinding result.
- **Primary source:** [AsiaCCS author/institutional paper](https://acris.aalto.fi/ws/portalfiles/portal/36903088/Sethi_Peltonen_Aura_Misbinding_Attacks_on_Secure_Device.pdf);
  [journal version](https://www.sciencedirect.com/science/article/pii/S2214212619307215).

### L10 — Lowe, Authentication Hierarchy

- **Full citation:** Gavin Lowe. “A Hierarchy of Authentication
  Specifications.” *10th IEEE Computer Security Foundations Workshop*, 1997,
  pp. 31–43. DOI: 10.1109/CSFW.1997.596782.
- **Venue quality/type:** CSFW/CSF; peer-reviewed foundational formal-security
  conference.
- **Year:** 1997.
- **Research problem:** Clarify increasingly strong authentication agreement
  properties.
- **Protocol/system:** General authentication protocols.
- **Formal method:** Trace-based definitions and implication hierarchy.
- **Security/property target:** Aliveness, weak agreement, non-injective
  agreement, and injective agreement.
- **Identity dimension:** One-to-one correspondence between protocol runs and
  agreement on peer/data.
- **Closest relation to RQ-v2:** Supplies the precise vocabulary for the
  occurrence-injectivity dimension measured by the prototypes.
- **Key difference:** Injective agreement is not a predicate that two slots in
  one batch contain different parties.
- **Use in our paper:** Prevent overloading “injective” as a synonym for
  party-level uniqueness.
- **Collision level:** `LOW`.
- **Content checked:** Authentication hierarchy and injective/non-injective
  agreement definitions.
- **Primary source:** [IEEE Computer Society author copy](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf).

### L11 — Meier et al., Tamarin

- **Full citation:** Simon Meier, Benedikt Schmidt, Cas Cremers, and David
  Basin. “The TAMARIN Prover for the Symbolic Analysis of Security Protocols.”
  *CAV 2013*, LNCS 8044, pp. 696–701.
  DOI: 10.1007/978-3-642-39799-8_48.
- **Venue quality/type:** CAV; peer-reviewed formal-verification conference.
- **Year:** 2013.
- **Research problem:** Automate symbolic analysis of protocols with complex
  state and unbounded sessions.
- **Protocol/system:** General security protocols.
- **Formal method:** Multiset-rewriting trace semantics and constraint solving
  in Tamarin.
- **Security/property target:** Trace properties and observational
  equivalence-style analyses supported by the tool.
- **Identity dimension:** Whatever agent/session/event coordinates a model
  explicitly encodes.
- **Closest relation to RQ-v2:** Methodological basis of the three RQ-v2
  prototypes.
- **Key difference:** Tamarin's general capability does not enlarge the current
  fixed-two-slot model or supply the RQ-v2 claim by itself.
- **Use in our paper:** Tool and symbolic-method citation.
- **Collision level:** `NONE`.
- **Content checked:** Tool architecture, multiset-rewriting model, adversary
  model, and automation scope.
- **Primary source:** [Springer CAV chapter](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48).

### L15 — Thomson and Rescorla, TLS/SDP UKS

- **Full citation:** Martin Thomson and Eric Rescorla. “Unknown Key-Share
  Attacks on Uses of TLS with the Session Description Protocol (SDP).” RFC
  8844, January 2021. DOI: 10.17487/RFC8844.
- **Venue quality/type:** IETF Standards Track RFC; not counted as a
  peer-reviewed paper.
- **Year:** 2021.
- **Research problem:** Prevent an attacker from binding an identity it
  controls to another endpoint's TLS/DTLS key or fingerprint.
- **Protocol/system:** TLS/DTLS-SRTP with SDP, WebRTC identity, and SIP
  identity.
- **Formal method:** Standards security analysis and specified TLS extensions.
- **Security/property target:** Correct external identity and session binding;
  UKS mitigation.
- **Identity dimension:** External identity-to-key/fingerprint/session binding.
- **Closest relation to RQ-v2:** Sharpens the distinction between an identity
  binding error and a party-cardinality/uniqueness error.
- **Key difference:** The attacker creates peer-identity confusion; RQ-v2 does
  not establish peer confusion or a UKS attack.
- **Use in our paper:** Terminological boundary and non-claim.
- **Collision level:** `NONE`.
- **Content checked:** Abstract, Sections 1–4, identity-binding attack,
  fingerprint attack, and unique-session-identity mitigation.
- **Primary source:** [RFC Editor HTML](https://www.rfc-editor.org/rfc/rfc8844.html).

### L16 — Lupetti, Dillema, and Stabell-Kulø, Names in Protocols

- **Full citation:** Simone Lupetti, Feike W. Dillema, and Tage Stabell-Kulø.
  “Names in Cryptographic Protocols.” *4th International Workshop on Security
  in Information Systems (WOSIS 2006)*, pp. 185–194.
- **Venue quality/type:** Peer-reviewed workshop paper.
- **Year:** 2006.
- **Research problem:** Identify environmental assumptions required for names
  to play their intended role in cryptographic protocols.
- **Protocol/system:** General cryptographic protocols, illustrated through
  established authentication examples.
- **Formal method:** Conceptual protocol analysis with local/global mechanisms
  for verifying name uniqueness; no machine-checked necessity experiment.
- **Security/property target:** Uniqueness of principal names across correlated
  sessions in which messages can be reused.
- **Identity dimension:** Principal names and their uniqueness across
  correlated sessions.
- **Closest relation to RQ-v2:** Directly argues that identity-bearing names can
  require a scoped uniqueness assumption and that enforcement has external
  costs.
- **Key difference:** It concerns distinct names for distinct principals and
  name ambiguity across correlated sessions. It does not require different
  components of one batch to denote different parties, remove such a batch
  condition, compare message and party uniqueness, or produce the RQ-v2 trace
  comparison.
- **Use in our paper:** Mandatory closest-prior-work discussion; it limits any
  broad claim that treating identity uniqueness as a semantic assumption is
  itself new.
- **Collision level:** `MEDIUM`.
- **Content checked:** Abstract, motivating protocol examples, uniqueness
  principle, correlated-session scope, and local/global verification
  mechanisms.
- **Primary source:** [SciTePress paper](https://www.scitepress.org/papers/2006/24847/24847.pdf).

### L17 — Ceelen, Mauw, and Radomirović, Chosen-Name Attacks

- **Full citation:** Pieter Ceelen, Sjouke Mauw, and Saša Radomirović.
  “Chosen-Name Attacks: An Overlooked Class of Type-Flaw Attacks.” *Electronic
  Notes in Theoretical Computer Science* 197(2), 2008, pp. 31–43.
  DOI: 10.1016/j.entcs.2007.12.015.
- **Venue quality/type:** Peer-reviewed journal/workshop proceedings article.
- **Year:** 2008.
- **Research problem:** Model an intruder that dynamically chooses or assigns
  agent names and identify the resulting type-flaw attacks.
- **Protocol/system:** General Dolev–Yao protocol models and authentication
  examples.
- **Formal method:** Dolev–Yao operational semantics, attack classification,
  and analysis of implications for automated verification.
- **Security/property target:** Resistance to selected-name and assigned-name
  type-flaw attacks.
- **Identity dimension:** Dynamic agent-name assignment and name/message type
  confusion.
- **Closest relation to RQ-v2:** Warns that a formal model's treatment of agent
  identities is itself a security-relevant modeling choice.
- **Key difference:** It changes the adversary's ability to synthesize names;
  RQ-v2 keeps a party coordinate and studies duplicate use of that coordinate
  in one batch.
- **Use in our paper:** Identity-modeling background and scope contrast.
- **Collision level:** `LOW`.
- **Content checked:** Abstract, intruder capability, selected/assigned-name
  classes, protocol examples, and consequences for verification tools.
- **Primary source:** [University of Luxembourg author paper](https://satoss.uni.lu/papers/CMR07.pdf).

### L19 — Sattarzadeh and Fallah, Injective Agreement

- **Full citation:** B. Sattarzadeh and M. S. Fallah. “Automated Type-Based
  Analysis of Injective Agreement in the Presence of Compromised Principals.”
  *Journal of Logical and Algebraic Methods in Programming* 84(5), 2015,
  pp. 576–610. DOI: 10.1016/j.jlamp.2015.06.002.
- **Venue quality/type:** Peer-reviewed formal-methods journal.
- **Year:** 2015.
- **Research problem:** Automatically prove injective agreement for
  authentication protocols under dynamically compromised principals.
- **Protocol/system:** General authentication protocols in a spi-calculus
  language.
- **Formal method:** Sound type system and automated type reconstruction.
- **Security/property target:** Injective agreement/correspondence and replay
  exclusion.
- **Identity dimension:** Unique matching between begin/send and end/receive
  occurrences, with agreement on principals, roles, and data.
- **Closest relation to RQ-v2:** Its explanatory example has one send copied to
  two receivers, precisely illustrating why occurrence injectivity consumes a
  unique begin event.
- **Key difference:** It establishes message/run correspondence, not distinct
  party coordinates across two separately originated, different-message slots.
  It therefore supports, rather than collapses, RQ-v2's separation of scoped
  occurrence injectivity from party uniqueness.
- **Use in our paper:** Closest formal vocabulary for the duplicate-acceptance
  result and the M-semantics contrast.
- **Collision level:** `MEDIUM`.
- **Content checked:** Abstract, operational semantics, robust safety,
  begin/end resource interpretation, copied-message example, and injective
  agreement scope.
- **Primary source:** [publisher article](https://www.sciencedirect.com/science/article/pii/S2352220815000528).

## Search-Scope Record

The collision search covered seven query families rather than title-only
matching:

1. batch protocol/processing/admission with participant identity;
2. party or participant uniqueness and “distinct parties” conditions;
3. identity invariants and participant consistency;
4. identity misbinding, UKS, and correspondence assertions;
5. group-membership consistency and formal group management;
6. protocol/session/conversation composition and Tamarin session handling;
7. replay, deduplication, duplicate acceptance/processing, and injectivity.

The most important non-seed hits were `L16`, `L17`, `L18`, `L19`, `L20`, and
`L21`. `L16` and `L19` materially narrow the novelty language: principal-name
uniqueness and occurrence injectivity are established topics. Within the
verified sources, however, neither work carries out the complete RQ-v2 chain:

```text
distinct-party condition on one batch/vector
        -> condition removed
        -> repeated-party composition
        -> message uniqueness compared with party uniqueness
        -> bounded formal necessity/restoration comparison
```

Absence of a direct collision in this bounded search is not evidence that no
such work exists outside the verified corpus.
