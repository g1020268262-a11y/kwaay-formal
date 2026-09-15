# K-Waay RQ-v2 manuscript

This directory is a venue-neutral LaTeX manuscript scaffold. It separates the
technical paper content from submission-specific formatting and front matter.
The source drafts under `docs/paper/` remain writing material rather than final
manuscript prose.

## Build

From this directory:

```text
latexmk -pdf main.tex
```

## Clean

```text
latexmk -C
```

## Directory roles

- `venue/` owns the document class and venue-facing format layer.
- `preamble/` owns common packages, semantic macros, and metadata.
- `sections/` owns venue-neutral manuscript content.
- `figures/` and `tables/` own reusable visual and tabular components.
- `bibliography/` contains BibTeX-compatible, source-verified records.
- `appendix/` contains detailed trace, property, and reproducibility material.
- `notes/` records the source map, writing plan, structure rationale, and
  future venue migration work.

## Anonymous mode

`preamble/metadata.tex` defines an `\ifanonymous` switch. The scaffold defaults
to anonymous mode and contains no real author identity. Change only the switch
and the non-anonymous placeholder when author metadata is ready.

## Figures and tables

TikZ sources are included with `\input{figures/tikz/...}`. PDF figures, when
needed, belong in `figures/pdf/` and should be included with portable
`\includegraphics` commands. Shared result tables live under `tables/`.

## Citation workflow

Use stable descriptive citation keys from `bibliography/references.bib`; do not
use source-map labels such as `L1`. The initial records are converted only from
rows marked `source_verified=yes` in
`docs/paper/literature/citation-verification.tsv`. Resolve any BibTeX `TODO`
before final submission rather than guessing metadata.

## Appendix

`appendix/appendix.tex` switches to appendix mode and assembles detailed trace,
model-property, and reproducibility placeholders. Keep the main text focused on
the paper's argument and move only supporting detail to these files.

## Venue migration

`venue/generic.tex` is **not a submission template**. After selecting a venue,
create a dedicated format file and follow the venue's current official author
instructions. Core files under `sections/` should not be rewritten merely to
accommodate ACM, IEEE, LNCS/Springer, or Elsevier front matter.

## Evidence discipline

Machine-checked claims must match the bounded RQ-v2 model and recorded outcomes.
Keep party identity, message identity, session identity, slot identity, and
occurrence injectivity distinct. Do not turn an admission-level counterexample
into a claim about key compromise, deployment behavior, or a cryptographic
break.
