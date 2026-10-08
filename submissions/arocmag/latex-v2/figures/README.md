# Figure plan

Fig.1 frozen after semantic/hierarchy review and artifact rebuild.

Its information requirements come from
`submissions/arocmag/style-study/FINAL_CHINESE_PAPER_BLUEPRINT.md`.

The editable TikZ source is `fig1-two-slot-lifecycle.tex`; the standalone
review source and PDF are `fig1-preview.tex` and `fig1-preview.pdf`.
Reference and design decisions are recorded in `FIG1_REFERENCE_ANALYSIS.md`
and `FIG1_DESIGN_REPORT.md`; the latter records the semantic and visual-hierarchy patch.

Fig.2 ready for review: `AROCMAG_FIG2_READY_FOR_REVIEW`.

The editable TikZ source is `fig2-duplicate-acceptance-trace.tex`; the 8.2cm
standalone review source and PDF are `fig2-preview.tex` and `fig2-preview.pdf`.
Actual PDF figure research is recorded in `FIG2_REFERENCE_ANALYSIS.md`;
element-by-element model/graph mappings, scope and QA are recorded in
`FIG2_DESIGN_REPORT.md`. `fig2-qa/` preserves the build logs, static graph checks,
gray-scale review renderings and the two external reference PDFs.

Required content:

- one Send source matching the complete tuple;
- same A, oid, m in both collected entries and acceptance events;
- same bid, rst in both acceptance events;
- two distinct ReceiverAccept events;
- s < b < r1 < r2, in particular r1 < r2;
- reconstructed analytical trace, based on the model and recorded witness;
- not a full K-Waay attack or a raw historical log screenshot.

Source: `rqv2_relaxed.spthy`, lemma `one_send_two_accepts_exists`, and
`reviews/2026-09-16-evidence/trace-audit-summary.txt` (relaxed duplicate witness).
Only the related event projection is displayed; unrelated Send events in an
exported graph must not be added to the core chain. The matching Send is unique
for this exact tuple, not necessarily the only Send in the complete trace.

Section 3.1 now replaces the Fig.2 placeholder comments with the formal figure,
one figure-reference sentence and a short evidence/projection note.
Standalone and full XeLaTeX builds pass with zero undefined references,
undefined citations, missing glyphs and overfull boxes. Fig.1 assets remain frozen.

