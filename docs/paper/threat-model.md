# Threat Model

## Scope

This document fixes the threat model for the K-Waay formal analysis in this repository.
It covers the symbolic analysis of the Figure 7 core, including:

- public-channel attacker behavior;
- sender / receiver prekey handling;
- explicit compromise experiments;
- receiver-side BatchReceive state and slot lifecycle.

It does not claim a full computational proof of K-Waay.

## Adversary

The baseline attacker is an active network adversary in the standard Dolev-Yao style:

- can eavesdrop, replay, drop, reorder, and inject messages;
- can substitute prekey bundles and core messages on the public channel;
- can drive concurrent protocol runs.

This matches the paper-level intuition that the protocol runs over an attacker-controlled network.

## Compromise model

The project separates the no-compromise baseline from explicit compromise experiments.
The main compromise dimensions are:

- sender-side state compromise;
- receiver-side state compromise;
- long-term key compromise;
- batch-level state consumption and compromise ordering.

In Tamarin, receiver state compromise is modeled explicitly with ordering-sensitive rules.
In ProVerif, compromise is split into dedicated leak / exception targets so that baseline secrecy is not confused with bad-case classification.

## Relation to the reference artifacts

### Compared with `pqxdh-analysis`

PQXDH allows long-term identity-key compromise and studies several compromise cases around IK, SPK, PQPK, and session independence.
Compared with that setting, this project is narrower and more symbolic:

- it does not try to reproduce the full PQXDH computational proof stack;
- it does not rely on the same DH-vs-KEM split threat-model distinction;
- it focuses on K-Waay Figure 7 core and on receiver-side state / batch semantics.

### Compared with `TLS13Tamarin`

TLS13Tamarin uses a standard Dolev-Yao attacker plus explicit reveal rules such as long-term key reveal and DH-exponent reveal.
This project follows the same active-network style, but extends the model toward:

- receiver-side state exposure;
- compromise ordering;
- BatchReceive slot and batch lifecycle reasoning.

## What is intentionally out of scope

- computational KIND;
- UNF-1KMA;
- IND-1BatchCCA;
- full deniability;
- full BatchReceive vector semantics;
- any claim that `RecvDone ==> SendDone` must hold in the baseline core model.

## Conclusion

The current threat model is reasonable for a symbolic analysis of the K-Waay core.
The main missing pieces are paper-level deniability and the full oracle-style game structure
(`STATE`, `KEY`, `REGISTER`, and the deniability experiment), which should be added only if the goal is to match the paper's formal game model exactly.
