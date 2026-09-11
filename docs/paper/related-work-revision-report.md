# Related Work Final Revision Report

## 1. References Used

The revised Related Work cites 18 works. Every cited work has
`source_verified=yes` in
[`literature/citation-verification.tsv`](literature/citation-verification.tsv).

| ID | Role in the revision |
| --- | --- |
| L1 | Direct K-Waay protocol source and stated different-party `BatchReceive` condition |
| L2 | Computational formal analysis of Signal/X3DH/Double Ratchet |
| L3 | ProVerif/CryptoVerif analysis of PQXDH and specification-boundary precedent |
| L4 | Session-to-conversation composition and Tamarin application-layer analysis |
| L5 | TreeSync shared group-state consistency and authentication |
| L6 | Cryptographic membership administration and authorization |
| L7 | Modular secure-group-messaging and MLS component composition |
| L9 | Formal identity-misbinding correspondence and its boundary from RQ-v2 |
| L10 | Authentication hierarchy and injective/non-injective agreement vocabulary |
| L11 | Tamarin symbolic methodology |
| L13 | X3DH replay, key-reuse, and identity-binding specification context |
| L15 | UKS/identity-binding definition and non-equivalence boundary |
| L16 | Principal-name uniqueness as an established semantic assumption |
| L17 | Chosen-name adversary and identity-modeling boundary |
| L18 | Secure-messaging taxonomy and participant-consistency distinction |
| L19 | Formal injective correspondence and duplicate-receive example |
| L20 | Cross-group composition effects on post-compromise healing |
| L21 | General compositional-verification framework |

The conference and extended journal versions represented by L9 are treated as
one research work and are not counted twice.

## 2. References Omitted and Reason

| ID | Reason omitted from the Related Work body |
| --- | --- |
| L8 | CGKA is verified background, but its dynamic-membership role is already represented more directly by L6 and L7 for this paper's comparison. |
| L12 | RFC 9420 is verified standards context, but the revised section relies on peer-reviewed TreeSync, cryptographic administration, and modular MLS sources for the group-state comparison. |
| L14 | The PQXDH specification is verified background, but L3 directly supplies the needed formal PQXDH discussion; L13 is retained because its replay and identity-binding sections are used explicitly. |

Omission does not question source quality or verification status. It keeps the
body within the requested approximately 12–18-work range and avoids citation
stacking where another verified source supports the exact comparison made.

## 3. Closest Prior Works

The closest works are:

1. **L1, K-Waay:** exact protocol and stated different-party condition, but no
   removal/comparison/restoration necessity analysis.
2. **L4, Session Handling:** strongest methodological precedent for treating a
   composition layer as an independent formal object; different object and PCS
   property.
3. **L16, Names in Cryptographic Protocols:** establishes that scoped
   identity/name uniqueness is already a security-relevant semantic
   assumption; different correlated-session and naming scope.
4. **L19, Injective-Agreement Analysis:** supplies the formal occurrence-level
   duplicate-receive relation; does not establish party uniqueness.
5. **L5, TreeSync:** formal member-indexed group-state consistency; not
   within-batch pairwise party distinctness.

## 4. Collision Handling

The revision explicitly handles all four potential-collision classes recorded
in the novelty analysis:

- K-Waay receives credit for stating the condition; RQ-v2 is positioned as a
  bounded semantic necessity analysis rather than discovery or repair.
- L16 limits any general identity-uniqueness novelty claim.
- L18 separates participant-list consistency from intra-batch distinctness.
- L19 establishes injectivity as prior vocabulary and makes the RQ-v2 novelty
  the M-semantics divergence rather than injectivity itself.

The body uses the scoped statement that, within the verified corpus and search
scope, no work was found performing the complete removal, comparison, and
restoration analysis. It does not convert that search result into an exhaustive
priority claim.

## 5. Strong Novelty Statements

- **N1 — Supported:** bounded formal analysis of K-Waay's stated
  distinct-party `BatchReceive` condition through the R/P comparison.
- **N3 — Supported:** controlled demonstration that scoped
  `receiver_accept_injective` can be verified while
  `same_party_different_messages_batch_exists` is also verified under
  M-semantics.

Both statements retain the symbolic fixed-two-slot and admission-boundary
limitations.

## 6. Moderate Novelty Statements

- **N2 — Partially supported:** the paper contributes a concrete
  message-versus-party admission comparison for `BatchReceive`, not the
  abstract distinction between messages and identities.
- **N4 — Partially supported:** the paper normalizes and analyzes this K-Waay
  condition as a semantic invariant without prescribing an enforcement
  location; it does not introduce the general concept of composition-layer
  invariants.

## 7. Removed or Softened Novelty Claims

The revision removes or precludes the following implications:

- that RQ-v2 discovered K-Waay's different-party condition;
- that identity/name uniqueness is a new concept;
- that injective agreement is introduced by RQ-v2;
- that composition-layer analysis originates with this work;
- that group-membership consistency and party uniqueness are the same
  property;
- that repeated-party composition is a misbinding or UKS attack;
- that the literature search proves universal absence of related work;
- that K-Waay's computational proof is wrong or repaired by RQ-v2.

## 8. Citation Verification Status

- Cited research works: **18**
- Cited works with `source_verified=yes`: **18**
- Unsupported citations: **0**
- Unverified citations: **0**
- Conference/journal duplicate counting: **0**
- Potential collision classes left unaddressed: **0**
- Improperly ignored direct collisions: **0**
- First-work or exhaustive-priority claims: **0**

The citations and metadata were selected without changing
[`literature/citation-verification.tsv`](literature/citation-verification.tsv).

## 9. Cross-Paper Consistency Check

The following drafts were checked without modification:

- `introduction-draft.md`
- `background-draft.md`
- `problem-statement-draft.md`
- `discussion-draft.md`

No statement in those files was found that presents identity uniqueness as a
new general concept, injective agreement as introduced here, composition-layer
analysis as originating here, group membership as equivalent to party
uniqueness, repeated-party composition as misbinding/UKS, or K-Waay's stated
condition as an RQ-v2 discovery.

## 10. Related-Work Completeness Verdict

**RELATED_WORK_READY**

The revised section covers the direct protocol source, formal secure-messaging
analyses, session/composition security, group membership and administration,
identity/name semantics, misbinding/UKS boundaries, and replay/injective
correspondence. Its novelty tiers and collision language match the verified
literature corpus and frozen RQ-v2 claim boundary.
