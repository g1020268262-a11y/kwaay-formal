# Related Work Revision Plan

## Purpose

This plan revises the paper's Related Work structure against the verified
literature corpus without editing `docs/paper/related-work-draft.md`. The
current draft has a sound claim boundary, but its four external sources are
insufficient for novelty positioning. The revision should preserve the
existing bounded language while replacing broad unsourced summaries with
source-specific comparisons.

## 1. K-Waay and Post-Quantum Asynchronous Key Exchange

**Core sources:** `L1` K-Waay, `L2` formal Signal analysis, `L3` PQXDH formal
verification, `L13` X3DH specification, `L14` PQXDH specification.

**Write:**

- State K-Waay's actual contribution: a deniable post-quantum X3DH-like DAKE,
  split-KEM security notions/construction, receiver-side ephemeral-key reuse,
  and computational proofs.
- Quote by paraphrase the exact scope of `BatchReceive`: vector inputs and the
  statement that each element of a call corresponds to a different party.
- State that the K-Waay theorem uses the construction under its model; do not
  say its authors prove the necessity of the different-party condition.
- Contrast X3DH/PQXDH replay, key reuse, and identity binding with
  same-batch party uniqueness.
- Use PQXDH verification as precedent for making prose-level specification
  details precise, not as evidence about RQ-v2's result.

**Current-draft action:**

- Lines 3–17, “K-Waay and Post-Quantum X3DH”: **EXPAND**. Keep the existing
  scope boundary and split-KEM summary, add the verified condition and theorem
  boundary, and integrate `L2`, `L3`, `L13`, and `L14`.

## 2. Formal Analyses of Secure Messaging

**Core sources:** `L2` formal Signal analysis, `L3` PQXDH verification, `L4`
session handling, `L11` Tamarin, `L18` SoK: Secure Messaging.

**Write:**

- Separate computational analyses of X3DH/Double Ratchet from symbolic analyses
  of application/session handling.
- Explain that ProVerif, CryptoVerif, and Tamarin support different proof
  styles; do not treat tool choice as novelty.
- Use the SoK taxonomy to distinguish authentication, participant consistency,
  speaker consistency, and message-oriented properties.
- Preserve the statement that RQ-v2 is a fixed-two-slot symbolic prototype,
  not a full K-Waay verification.

**Current-draft action:**

- Lines 19–32, “Symbolic Protocol Verification”: **EXPAND**. Keep the Tamarin
  boundary; add the computational/symbolic secure-messaging context.

## 3. Session- and Composition-Layer Security

**Core sources:** `L4` session handling, `L20` cross-group healing, `L21`
compositional verification.

**Write:**

- Explain the session-handling result that secure ratcheting chains do not
  automatically give the same guarantee after application-level composition
  into a conversation.
- Add the cross-group result as another example where context composition
  changes a security guarantee.
- Cite the general compositional-verification framework for the principle that
  composition conditions are proof obligations.
- Position RQ-v2 as a narrower admission-composition analysis. Do not imply
  that its property is PCS, protocol independence, or cross-group healing.

**Current-draft action:**

- No dedicated current section: **ADD** between the present Sections 2 and 3.
  This is the most important missing reviewer-facing context.

## 4. Group Membership, State Consistency, and Administration

**Core sources:** `L5` TreeSync, `L6` cryptographic administration, `L7`
modular MLS, `L8` CGKA, `L12` RFC 9420, `L18` SoK.

**Write:**

- Distinguish participant-list agreement, authenticated shared group state,
  membership-update authorization, and cryptographic component composition.
- Explain that these works make member-indexed state explicit and formally
  meaningful.
- State the non-equivalence: group/member state consistency is not pairwise
  distinctness of party coordinates across positions in one receiver batch.

**Current-draft action:**

- Lines 52–64, “Group Membership and Identity”: **REWRITE**. Retain the
  non-transfer boundary, but replace the RFC-only treatment with the verified
  academic line from CGKA through modular MLS, TreeSync, and A-CGKA.

## 5. Identity Binding, Names, and Authentication

**Core sources:** `L9` misbinding, `L10` Lowe, `L15` RFC 8844, `L16` names in
protocols, `L17` chosen-name attacks.

**Write:**

- Define identity binding/misbinding as an association between an identity and
  an endpoint, key, fingerprint, or protocol run.
- Explain Lowe's agreement hierarchy as occurrence/run correspondence
  vocabulary.
- Give `L16` prominent treatment because it directly studies scoped uniqueness
  of principal names as a semantic assumption.
- Use chosen-name attacks to show that an adversary's ability to select agent
  names is a modeling decision.
- State clearly that RQ-v2's repeated-party batch is neither a misbinding nor a
  UKS attack on current evidence.

**Current-draft action:**

- Lines 34–50, “Authentication and Injectivity”: **EXPAND** and split into two
  subsections: agreement/injectivity and identity binding/name semantics.

## 6. Replay, Deduplication, Duplicate Processing, and Injectivity

**Core sources:** `L10` Lowe, `L13` X3DH specification, `L14` PQXDH
specification, `L19` automated injective-agreement analysis.

**Write:**

- Use X3DH/PQXDH to describe replay and key reuse as protocol-level concerns,
  without claiming those specifications solve the RQ-v2 property.
- Use `L19`'s one-send/two-receive example to define why injective
  correspondence excludes a class of replay duplication.
- Then state the RQ-v2 distinction: M-semantics can satisfy the scoped
  occurrence-injectivity property while allowing a same-party/different-message
  batch.
- Preserve the non-claim that message deduplication and authentication remain
  useful for their own dimensions.

**Current-draft action:**

- Lines 66–82, “Replay, Deduplication, and Authentication”: **REWRITE**. The
  semantic distinction is correct, but the section needs external scholarly
  support and must no longer rely on repository history as its literature
  context.

## 7. Positioning of RQ-v2

**Core sources:** All closest works, especially `L1`, `L4`, `L16`, `L19`,
`L5`, `L3`, and `L9`.

**Write:**

- End with the exact gap: no verified work performs the complete K-Waay
  `DistinctPartyPerBatch` removal, repeated-party composition,
  message-versus-party comparison, and party-admission restoration chain.
- Present N1 and N3 as supported scoped novelty; present N2 and N4 as moderate,
  protocol-specific novelty with clear antecedents.
- Include “within the verified corpus/search scope” in the collision statement.
- Repeat the fixed-two-slot, symbolic, admission-boundary limitation.
- Exclude literature-priority superlatives and any claim of deployed,
  cryptographic, `KEY`/`TEST`, or upper-layer failure.

**Current-draft action:**

- Lines 84–98, “Positioning of This Work”: **REWRITE**. The present paragraph
  has the right boundary but must name the closest works, disclose the
  potential collisions, and make the novelty tier explicit.

## Paragraph-Level Disposition of the Current Draft

| Current lines | Current content | Action | Reason |
| --- | --- | --- | --- |
| 3–10 | K-Waay construction and `BatchReceive` | **KEEP + EXPAND** | Accurate, but add the verified different-party assumption and formal theorem scope. |
| 12–17 | RQ-v2 abstraction boundary | **KEEP** | Correctly excludes split-KEM reanalysis and focuses on party interpretation. |
| 19–25 | Tamarin methodology | **KEEP + EXPAND** | Accurate; add ProVerif/CryptoVerif and computational secure-messaging analyses. |
| 27–32 | Fixed-two-slot scope | **KEEP** | Essential model boundary. |
| 34–40 | Lowe and injectivity vocabulary | **KEEP + EXPAND** | Add `L19` and distinguish identity-binding/name work. |
| 42–50 | M-semantics divergence | **KEEP** | Evidence-aligned and central; connect it to `L19`. |
| 52–64 | RFC-only group membership discussion | **REWRITE** | Replace narrow standards-only context with TreeSync, A-CGKA, modular MLS, CGKA, and SoK. |
| 66–73 | Replay/dedup/party distinction | **KEEP + EXPAND** | Semantically sound; add X3DH/PQXDH and injectivity sources. |
| 75–82 | Non-overclaim and repository-history note | **REWRITE** | Keep the non-overclaim, but external literature—not internal historical artifacts—must ground Related Work. |
| 84–98 | Overall positioning | **REWRITE** | Add closest-work comparisons, collision verdict, and supported/moderate novelty tiers. |

No current paragraph requires **REMOVE** solely for incorrect claims. Structural
rewriting should absorb the short standalone Tamarin and RFC treatments into a
literature-complete narrative rather than delete their valid content.

## Assembly Order

The recommended Related Work order is:

1. K-Waay and post-quantum asynchronous key exchange;
2. formal analyses of secure messaging;
3. session- and composition-layer security;
4. group membership, state consistency, and administration;
5. identity binding, names, and authentication;
6. replay, deduplication, duplicate processing, and injectivity;
7. positioning of RQ-v2.

This order moves from the direct protocol through the closest semantic and
formal neighbors to the final scoped gap. It does not change the frozen RQ-v2
authority or the existing draft during this phase.
