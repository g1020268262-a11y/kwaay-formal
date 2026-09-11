# Limitations

## 1. Bounded Two-Slot Model

The machine-checked results cover symbolic fixed-two-slot batches only. The
general formula for `DistinctPartyPerBatch` defines the intended semantic
condition over distinct positions, but the current evidence does not prove the
property or the comparative results for arbitrary `n`.

## 2. Admission-Level Abstraction

The prototypes isolate `BatchReceive` admission and the resulting
`ReceiverAccept` lifecycle. They do not model the complete KEM construction,
signatures, HMAC computation, prekey cryptography, key derivation, Double
Ratchet state, or application behavior. Consequently, the analysis does not
connect admission outcomes to complete cryptographic or application
executions.

## 3. No Cryptographic Security Claim

The results do not prove loss of secrecy, authentication failure, IND-CCA
failure, key compromise, failure of `KEY` or `TEST` interfaces, or correctness
failure. Cryptographic primitives, output-key objects, security queries, and
key-correctness relations are absent from the current prototypes.

## 4. No Deployment Claim

The repository does not provide complete public implementation-enforcement
evidence for the RQ-v2 admission invariant. The paper therefore does not claim
a vulnerability in a deployed system, an implementation defect, or real-world
exploitability. Its scope is specification- and integration-level invariant
analysis.

## 5. No Arbitrary Execution-Theory Generalization

The current results do not establish cross-batch, rollback, restart,
concurrency, arbitrary batching, long-term compromise, or distributed
enforcement properties. They also do not analyze how independently maintained
state across multiple components would affect the invariant.

## 6. Rejection Reachability vs Liveness

`same_party_rejection_exists` establishes that the P-semantics rejection
branch is reachable. It does not prove that every collected invalid batch must
eventually produce a `Reject` event. A symbolic trace can stop before an
enabled transition is taken, and the current theory includes no fairness or
liveness requirement that closes this gap.

## 7. Enforcement Mechanism

P-semantics presents one restoration model in which party coordinates are
compared at admission. The evidence does not show that this is the only
algorithm, the only placement, or the only engineering realization capable of
maintaining `DistinctPartyPerBatch`.

## 8. Artifact Limitation

The RQ-v2 freeze package preserves the three models' hashes, the recorded parse
and proof commands, the reported Tamarin/Maude/OS environment, the evidence
manifest, and the results transcribed from the earlier prototype execution
report. It does not include raw prover transcripts for these prototypes and
does not include a newly generated independent proof transcript from this
paper-writing phase. The package therefore supports provenance and
traceability of the recorded evidence, not a claim of an independently
repeated verification run.

