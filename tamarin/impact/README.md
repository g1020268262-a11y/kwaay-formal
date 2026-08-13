# M2 conditional impact over the frozen relaxed duplicate-input model

This directory contains the bounded conditional impact model for **P3 under
`C_install-v2`**. It is derived from the frozen relaxed duplicate-input replay
model but is a separate theory.

> **Current interpretation notice.** The lower-layer model permits the same
> modeled sender identity `A` and the same complete message in multiple slots.
> The K-Waay full specification states a distinct-party-per-`BatchReceive`
> precondition. The exact mapping from `A` to the specification-level notion of
> party remains a Stage-0 modeling question. The result is conditional
> integration-impact evidence over that relaxed input domain, not an original-
> protocol or deployed-implementation duplicate-install claim.

The recorded result is a **conditional duplicate-install witness** and
**conditional local-handle duplication**.  The model does not establish two
real sessions, real session cloning, Double Ratchet duplication, an application
exploit, or that deployed K-Waay necessarily behaves this way.

## Baseline and scope

The frozen relaxed lower-layer baseline is:

```text
tamarin/replay/kwaay_replay_original.spthy
```

The impact variant preserves the original message construction and the action
signatures and meanings of:

```tamarin
SenderSession(A,B,m,sid,k)
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
BatchComplete(B,bid,rst)
CompromiseReceiverState(B,rst)
CompromiseSenderState(A,sst)
```

It remains a fixed-two-slot symbolic abstraction.  `idx` is batch slot
context, `sid` is the protocol session identifier, `aid` is a fresh accepted
output occurrence identifier, and `h` is a fresh symbolic local installation
handle.

## Frozen `C_install-v2`

`C_install-v2` is the explicit composition boundary for this model:

```text
C1:
Every installation has an earlier complete-parameter-matching
accept-output source.

C2a:
Each accepted-output source is installed at most once.

C2b:
If ConsumerComplete occurs, every successful output belonging to
that consumer has been installed exactly once.

The model proves C2b compositionally: `consumer_complete_requires_all_outputs_installed`
proves completion-gated totality, while `accept_output_installed_at_most_once`
supplies the at-most-once half.  Their conjunction is the stated exactly-once
claim; no future-install restriction is used.

C2c:
A normal accept-install-consumer-complete execution is reachable.

C3:
Each installation creates a fresh local handle.

C4:
InstallSession can only be emitted by the designated installation
interface rules.

C5:
At least one matching accept/install pair is reachable.
This does not mean that the whole trace contains only one accept
or only one install.

C6:
Installations from distinct accept-source occurrences use distinct
local handles.

C7:
The modeled bounded consumer independently invokes installation for
each successful batch output and does not merge or deduplicate by
sid, message, peer, or key.

C8:
C7 is an explicit composition assumption, not an established fact
about deployed K-Waay.
```

There is no repository evidence that every `BatchReceive` output is installed
independently by a deployed upper layer.  Consequently every M2 installation
claim remains conditional on `C_install-v2`.

The model uses no restriction that forces a future installation.  At-most-once
is a universal safety property; totality is checked only after
`ConsumerComplete`; non-vacuity is checked by exists-trace lemmas.

## Accept-source provenance and consumer

Each successful `ProcessSlotN` occurrence creates a fresh `aid`, emits
`ReceiverAccept` and `AcceptOutputCreated` at the same timepoint, and creates
one linear `AcceptedOutput`.  `aid` does not enter the protocol message, `sid`,
or `k`.

The existence and uniqueness obligations are deliberately separate:
`receiver_accept_has_output` proves that every successful accept emits a source,
`receiver_accept_has_unique_output` proves at most one source at that rule
timepoint, and `accept_id_unique` proves that one fresh `aid` identifies only
one complete, full-parameter accept-output occurrence.  This avoids encoding
uniqueness as a nested future/existential condition.

Only successful `CompleteBatch` creates `ConsumerStage0`; failure paths never
start a consumer.  `InstallAcceptedOutputFirst` may choose either output token.
`InstallAcceptedOutputSecond` consumes the remaining token.  This generic
two-stage design permits either consumption order and does not select outputs
by slot number.

Both installation rules consume one linear token, use `Fr(~h)`, emit exactly
one `InstallFromAccept` and one `InstallSession`, and advance the linear
consumer stage.  `CompleteConsumer` requires both `InstalledOutput` records,
emits `ConsumerComplete`, and leaves `ClosedConsumer`.  `ConsumerComplete` is
only the completion of this bounded composition abstraction, not a real
application completion event.

The interface correspondence is checked in both directions:
`install_session_has_interface_origin` requires every `InstallSession` to have
a same-time `InstallFromAccept` provenance event, while
`install_from_accept_has_session` requires every provenance event to carry the
same-time `InstallSession(B,h,A,sid,k)` event.  Both core impact properties also
query the two `InstallSession` occurrences directly while retaining their
full-parameter `InstallFromAccept` premises.

The original `BatchClosed` occurs with `BatchComplete`; the later terminal
event for the modeled upper-layer lifecycle is `ConsumerComplete`.  The lemma
`no_install_after_consumer_close` refers to this consumer close.

## Proof obligations

The 19 composition lemmas cover provenance, bidirectional installation-interface
correspondence, installation/source injectivity, completion-gated lifecycle,
normal executability, a positive conditional witness, and a universal
unique-install property.  Together with the frozen 18 lower-layer lemmas, the
impact theory contains 37 lemmas.  The pre-run design expectation is that the
positive witness is reachable and that `unique_install_within_completed_consumer`
has a counterexample.  These are expectations only; actual results are taken
exclusively from Tamarin raw output.

The theory also retains the original 18 lower-layer lemmas with unchanged
formulas.  The runner independently re-runs the frozen original model so the
selected result vectors can be compared.  Matching this selected regression
does not prove full trace equivalence.

## Runner and evidence

Run only from a clean commit that already contains both the model and runner:

```bash
bash tamarin/impact/run-impact-original.sh
```

The runner derives the repository root from its own resolved path, rejects
`KWAAY_REPO_ROOT`, rejects a dirty worktree, refuses to overwrite an existing
evidence directory, verifies that model and runner are tracked by `HEAD`, and
records Git blob OIDs, working-tree SHA-256 values, EOL detection, tool
versions, exact commands, command exit statuses, and post-run status.

The formal runner proves the 37 impact lemmas in their frozen order using 37
sequential, independent selected-proof invocations.  Each invocation passes
`--prove=<exact-lemma-name>` and writes its unmodified output to
`logs/tamarin-impact-original/proofs/<lemma>.out`.  The runner validates only
the selected target in each output, rejects a target that is missing,
duplicated, nonterminal, or accompanied by any other terminal lemma, and
mechanically builds `aggregate-results.tsv` from those 37 outputs.  A failed
invocation does not prevent the remaining selected proofs from running, but it
does make the final runner status nonzero.

This execution layout avoids depending on the single multi-lemma proof
invocation behavior observed for this model with the validated Tamarin 1.12.0
toolchain.  It does not change the model, any lemma, the expected result vector,
or the proof standard, and it is not a claim about Tamarin behavior in general.
The positive-witness and negative-property JSON/DOT exports remain separate
formal invocations from the corresponding selected proofs in `proofs/`.

Tamarin 1.12.0 on the validated local toolchain advertises `--output-json` and
`--output-dot`.  The runner checks those options again before execution and
fails rather than fabricating unsupported trace formats.  `SHA256SUMS.txt` is
generated last, recursively includes the `proofs/` outputs and every other
evidence file, and excludes itself; the later evidence Git tree binds the
manifest file itself.

The impact theory exceeds Tamarin's default derivation-check time budget on
this toolchain.  Proof and trace commands therefore use
`--derivcheck-timeout=0`; evidence is acceptable only when the raw output says
that all wellformedness checks succeeded.

## Explicitly out of scope

- batch-local deduplication, `SeenSid`, or `SeenMessage`;
- duplicate rejection or atomic batch-failure hardening;
- HMAC+dedup or HMAC impact counterparts;
- Double Ratchet or application state/actions;
- payment, authorization, or deployed exploit claims;
- arbitrary-length batches, computational security, or a complete compromise
  matrix.
