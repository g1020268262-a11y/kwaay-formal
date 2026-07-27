# Schema notes

The JSON Schema files define individual TSV rows. Header order and cross-row
constraints (unique property IDs, source bindings, model/formula uniqueness,
scope rules, and composite policy) are enforced by
`scripts/artifact/verify_contract.py`. TSV values are UTF-8, tab-separated,
single-line strings with LF endings.

Expected rows carry separate historical expectation and M4 regression-matrix
bindings. Actual rows carry separate source, model, and evidence commit/tree
provenance. New source-run and composite tables are validated by
`scripts/artifact/source_runs.py`, including full manifest coverage and
raw-derived result reconstruction.

Source-run target rows bind each model to its historical `model_commit`,
`model_tree`, Git `model_blob`, and blob-byte `model_sha256`. Validation
requires the exact frozen bytes at `inputs/<model_commit>/<model_path>` and
re-extracts every Tamarin lemma or indexed ProVerif query from that input.

`evidence_storage` distinguishes committed Git evidence, external
manifest-bound evidence, and scope declarations. External source runs leave
`evidence_commit` and `evidence_tree` empty because their raw bundle is not in
the runner's `source_head`; `evidence_manifest_sha256` instead binds the
external `SHA256SUMS.txt`.
