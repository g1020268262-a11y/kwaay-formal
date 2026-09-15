# Venue migration

The current `venue/generic.tex` exists only for writing and review. Once a
submission target is selected, add an appropriate venue layer such as
`venue/acm.tex`, `venue/ieee.tex`, `venue/springer.tex`, or
`venue/elsevier.tex`. For Springer proceedings, use the current LNCS guidance
when that is the selected format.

Before migration, consult the target venue's official current author
instructions. The likely changes are:

- document class and class options;
- title, author, affiliation, anonymity, and other front matter;
- bibliography style and any mandated citation package;
- page-dependent figure and table placement or width.

Venue-specific commands stay in `venue/` or `preamble/metadata.tex`. Core
technical prose in `sections/*.tex` should not need wholesale rewriting merely
because the format changes. Any unavoidable class-specific content should be
wrapped behind a small, documented interface rather than spread through the
sections.
