# Structure rationale

The research-preparation outline treated Background, Problem Statement, Threat
Model, Formal Model, Formal Analysis, Evaluation, Discussion, Limitations, and
Related Work as nearly parallel blocks. The manuscript instead uses a connected
formal-analysis reader flow:

1. Protocol and identity problem
2. Security objective and adversarial boundary
3. Formal modeling methodology
4. Formal analysis and counterexample traces
5. Discussion, design implications, and principal limitations
6. Related work
7. Conclusion

This change reflects six writing decisions:

1. Formal-analysis papers normally establish the protocol object and security
   objective before presenting the model.
2. The threat model is inseparable from the property being claimed, so both
   belong in one section.
3. Modeling choices must precede machine-checked results to keep method and
   evidence legible.
4. This work has no independent empirical or performance evaluation; a
   systems-style Evaluation section would mischaracterize the evidence.
5. The attack trace is a bounded formal-analysis result, not a separate claim
   about a real-world deployed attack.
6. The main limitations qualify the interpretation of the results and therefore
   close the Discussion rather than occupying a thin standalone section.
7. Reproducibility is infrastructure rather than a separate narrative stage:
   Section 5 states the concise verification environment, while the appendix
   carries commands, hashes, exact lemmas, and detailed traces.
8. Related work remains a separate late section, followed by a short Conclusion;
   this supports clear positioning and later venue adaptation.

The resulting argument asks what semantic obligation K-Waay's stated
distinct-party condition carries, whether message/occurrence controls can
substitute for it, and what the controlled comparison establishes and does not
establish. Internal R/M/P labels are not the conceptual center of that argument.

The final reader-facing structure therefore has eight numbered sections. This
matches the technical narrative more closely than preserving a ninth section
whose only function would be to repeat limitations and artifact mechanics.
