# Related Work Source Map

## Verification Scope

This map records the external sources used by the Related Work draft. Metadata
and source-supported statements were checked against publisher, proceedings,
archive, DOI-registry, or standards-body records on 2026-09-01. Repository
documents remain internal drafting evidence and are not treated as external
scholarly citations.

## Verified Source-to-Claim Map

| ID | Citation | Relationship class | Problem studied | Relevant concept | Relation to RQ-v2 | What we may say | What we must NOT infer | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RW1 | Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh Nguyen, Nicolas Rolin, and Serge Vaudenay. “K-Waay: Fast and Deniable Post-Quantum X3DH without Ring Signatures.” *33rd USENIX Security Symposium (USENIX Security 24)*, pp. 433–450, 2024. | Direct prior work: protocol under study | Efficient, deniable, post-quantum X3DH-like key exchange without ring signatures | K-Waay, split-KEM, `BatchReceive` | RQ-v2 studies the identity semantics of the stated distinct-party condition at the `BatchReceive` boundary; it does not reanalyze the complete construction or computational proof. | K-Waay proposes a post-quantum, deniable X3DH-like protocol based on split-KEM techniques. The present work complements that contribution by focusing on a different abstraction boundary and the semantic role of a batch condition. | Do not infer that the original work omitted a required check, that its proof is incorrect, or that the current bounded prototypes revise its computational results. | [USENIX proceedings page](https://www.usenix.org/conference/usenixsecurity24/presentation/collins); [IACR ePrint 2024/120](https://eprint.iacr.org/2024/120). No DOI is listed in either verified record. |
| RW2 | Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. “The TAMARIN Prover for the Symbolic Analysis of Security Protocols.” In *Computer Aided Verification (CAV 2013)*, LNCS 8044, pp. 696–701, Springer, 2013. DOI: [10.1007/978-3-642-39799-8_48](https://doi.org/10.1007/978-3-642-39799-8_48). | Methodological foundation | Automated symbolic analysis of security protocols, adversary models, and properties | Tamarin, symbolic protocol analysis | RQ-v2 uses minimal Tamarin theories to encode admission rules and check reachability and correspondence-style trace properties. | Tamarin provides an automated symbolic framework for protocol, adversary, and property specifications. Its general analysis capabilities motivate the methodology used here. | Do not infer that the RQ-v2 theories model the complete protocol or that the tool's general support for unbounded symbolic analysis makes the current fixed-two-slot model unbounded. | [Springer publisher page](https://link.springer.com/chapter/10.1007/978-3-642-39799-8_48). |
| RW3 | Gavin Lowe. “A Hierarchy of Authentication Specifications.” In *Proceedings of the 10th Computer Security Foundations Workshop (CSFW 1997)*, pp. 31–43, IEEE Computer Society Press, 1997. DOI: [10.1109/CSFW.1997.596782](https://doi.org/10.1109/CSFW.1997.596782). | Background only: property vocabulary | A hierarchy separating forms of authentication, including non-injective and injective agreement | Agreement and one-to-one run correspondence | Lowe's distinction helps position occurrence injectivity as one particular correspondence dimension. RQ-v2 then separates that dimension from party uniqueness within one batch. | Classical authentication specifications distinguish agreement properties that do and do not require a one-to-one relationship between protocol runs. | Do not attribute `DistinctPartyPerBatch`, batch identity semantics, or the RQ-v2 comparison to Lowe; do not present RQ-v2's receiver-injectivity lemma as a full implementation of Lowe's agreement hierarchy. | [IEEE Xplore record](https://ieeexplore.ieee.org/document/596782); [IEEE Computer Society paper](https://conferences.computer.org/sp/pdfs/csf/1997/1997-lowe-hierarchy.pdf). |
| RW4 | Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon Millican, Emad Omara, and Katriel Cohn-Gordon. “The Messaging Layer Security (MLS) Protocol.” RFC 9420, IETF, July 2023. DOI: [10.17487/RFC9420](https://doi.org/10.17487/RFC9420). | Adjacent work | Efficient asynchronous group key establishment and evolution of authenticated group state | Member identity, group membership, epochs, group state | MLS provides adjacent context in which authenticated clients, members, and group state are explicitly related. RQ-v2 asks a narrower question about party-coordinate uniqueness across slots of one admitted `BatchReceive` batch. | MLS defines an epoch using a specific set of authenticated clients and defines a member through inclusion in the group's shared state. Its ratchet tree represents group membership. | Do not infer that MLS contains an equivalent batch invariant, addresses the same admission problem, or inherits the RQ-v2 result. | [RFC Editor: RFC 9420](https://www.rfc-editor.org/rfc/rfc9420.html). |

## Citation Boundaries

- RW1 supports the description of K-Waay's published contribution and protocol
  context. The RQ-v2 claim and bounded evidence remain this project's work.
- RW2 supports the symbolic-verification methodology, not the scope or outcome
  of any particular RQ-v2 lemma.
- RW3 supports the distinction between non-injective and injective agreement.
  The separation of occurrence injectivity from party uniqueness is the
  comparative observation of the RQ-v2 models.
- RW4 is adjacent membership-oriented context only. No transfer of results
  between MLS and RQ-v2 is asserted.
- The map makes no priority or literature-exhaustiveness claim.

