#!/usr/bin/env python3
"""Mechanically build the frozen M5 Commit A TSV contracts."""

from __future__ import annotations

import argparse
from pathlib import Path

from contract import (
    BASE_COMMIT,
    CLAIM_HEADER,
    EXPECTED_HEADER,
    FROZEN_HEADER,
    M4_BASELINE,
    PAPER_HEADER,
    ContractError,
    extract_proverif_queries,
    extract_tamarin_lemma,
    formula_sha,
    git_blob,
    git_blob_oid,
    parse_proverif_summary,
    read_git_tsv,
    repo_root,
    sha256,
    write_tsv,
)


M4_RUNNER = "tamarin/milestones/run-m4-hmac-dedup.sh"
M4_MATRIX = "logs/tamarin-m4-hmac-dedup/source-run1/canonical-target-matrix.tsv"
M4_FORMULAS = "logs/tamarin-m4-hmac-dedup/source-run1/formula-bodies.tsv"
M4_MEMORY = "Run1 systemd MemoryMax=16384MB; Run2 MemoryMax=49152MB; MemorySwapMax=0"
M4_SCOPE_TARGETS = {
    ("original", "BASELINE"), ("original", "COMPONENT"),
    ("hmac", "HMAC_BASELINE"), ("hmac", "HMAC_COMPONENT"),
    ("hmac", "HMAC_LEAK_SIGSK_A"),
}
SEMANTICS_HEADER = [
    "property_id", "tool", "suite", "target_id", "query_or_lemma",
    "property_kind", "expected_status",
]
PROVERIF_TARGET_HEADER = [
    "family", "suite", "target_id", "model_path", "query_count",
    "inherited", "m4_execution_scope",
]
PV_EXPECTATION_COMMITS = {
    "original": "4e91fdee3b4d635551aa24780e2f8f81736d2e75",
    "hmac": "9c18a64aa304639cea2ee7239ce1d3692ae2bd19",
}
PV_THREAT_MATRIX_COMMIT = BASE_COMMIT
HISTORICAL_EXPECTATION = {
    "v6": ("tamarin/milestones/run-m3-dedup.sh", "282532fd922f3a7f7928f3772b3325fe06785730"),
    "v7": ("tamarin/milestones/run-m3-dedup.sh", "282532fd922f3a7f7928f3772b3325fe06785730"),
    "original-replay": ("docs/milestones/M1-completion.md", "024c1c625ad5d924c364df5b67b4708dad3901f7"),
    "hmac-replay": ("docs/milestones/M1-completion.md", "024c1c625ad5d924c364df5b67b4708dad3901f7"),
    "original-impact": ("tamarin/impact/run-impact-original.sh", "841feabd908a01bdc68669ad99253a6755820389"),
    "fixed-replay": ("tamarin/milestones/run-m3-dedup.sh", "282532fd922f3a7f7928f3772b3325fe06785730"),
    "fixed-impact": ("tamarin/milestones/run-m3-dedup.sh", "282532fd922f3a7f7928f3772b3325fe06785730"),
    "combined-replay": (M4_RUNNER, M4_BASELINE),
    "combined-impact": (M4_RUNNER, M4_BASELINE),
}

SUITES = {
    "combined-replay": ("M4", "tamarin/replay/kwaay_replay_hmac_dedup.spthy", "P3"),
    "combined-impact": ("M4", "tamarin/impact/kwaay_impact_hmac_dedup.spthy", "P3"),
    "original-replay": ("M1", "tamarin/replay/kwaay_replay_original.spthy", "P2"),
    "hmac-replay": ("M1", "tamarin/replay/kwaay_replay_hmac_only.spthy", "P1"),
    "original-impact": ("M2", "tamarin/impact/kwaay_impact_original.spthy", "P2"),
    "fixed-replay": ("M3", "tamarin/replay/kwaay_replay_fixed.spthy", "P3"),
    "fixed-impact": ("M3", "tamarin/impact/kwaay_impact_fixed.spthy", "P3"),
    "v6": ("M0", "tamarin/kwaay_splitkem_batch_dynamic_v6.spthy", "P0-O"),
    "v7": ("M0", "tamarin/kwaay_splitkem_batch_dynamic_v7.spthy", "P0-O"),
}

PV_TARGETS = {
    "original": {
        "BASELINE": (
            "logs/final/proverif/generated/BASELINE.pv",
            ["false", "false", "true", "true", "true", "true"],
        ),
        "COMPONENT": (
            "logs/final/proverif/generated/COMPONENT.pv",
            ["true"],
        ),
        "EXCEPTION_CHOICE": (
            "logs/final/proverif/generated/EXCEPTION_CHOICE.pv",
            ["false", "false", "true", "true", "false", "false", "true"],
        ),
        "RECEIVER_EXCEPTION_CLASSIFICATION": (
            "logs/final/proverif/generated/RECEIVER_EXCEPTION_CLASSIFICATION.pv",
            ["true", "false"],
        ),
        "LEAK_SIGSK_A": (
            "logs/final/proverif/generated/LEAK_SIGSK_A.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
        "LEAK_SIGSK_B": (
            "logs/final/proverif/generated/LEAK_SIGSK_B.pv",
            ["false", "false", "true", "true", "true", "true"],
        ),
        "LEAK_SIGSK_AB": (
            "logs/final/proverif/generated/LEAK_SIGSK_AB.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
        "LEAK_SIGSK": (
            "logs/final/proverif/generated/LEAK_SIGSK.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
        "LEAK_KEMSK": (
            "logs/final/proverif/generated/LEAK_KEMSK.pv",
            ["false", "false", "true", "true", "true", "true"],
        ),
        "LEAK_EKEMSK": (
            "logs/final/proverif/generated/LEAK_EKEMSK.pv",
            ["false", "false", "true", "true", "true", "true"],
        ),
        "LEAK_RSKEMSK": (
            "logs/final/proverif/generated/LEAK_RSKEMSK.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
        "LEAK_SSKEMSK": (
            "logs/final/proverif/generated/LEAK_SSKEMSK.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
        "LEAK_KEMSK_EKEMSK": (
            "logs/final/proverif/generated/LEAK_KEMSK_EKEMSK.pv",
            ["false", "false", "true", "true", "true", "true"],
        ),
        "LEAK_ALL_RECEIVER_SECRETS": (
            "logs/final/proverif/generated/LEAK_ALL_RECEIVER_SECRETS.pv",
            ["false", "false", "true", "true", "false", "false"],
        ),
    },
    "hmac": {
        "HMAC_BASELINE": (
            "logs/variants/hmac-confirmation/proverif/generated/HMAC_BASELINE.pv",
            ["false", "true", "true", "true", "true", "true"],
        ),
        "HMAC_COMPONENT": (
            "logs/variants/hmac-confirmation/proverif/generated/HMAC_COMPONENT.pv",
            ["true"],
        ),
        "HMAC_LEAK_SIGSK_A": (
            "logs/variants/hmac-confirmation/proverif/generated/HMAC_LEAK_SIGSK_A.pv",
            ["false", "false", "true", "true", "true", "false"],
        ),
    },
}


def paper_rows() -> list[dict[str, str]]:
    limitation = "symbolic fixed-two-slot scope; see indexed claim documents"
    rows = [
        ("pv-original-source", "proverif/kwaay_core_final.cpp.pv", "model", "M0", "paper-mainline", "authoritative", "logs/final/proverif/summary.txt", "symbolic ProVerif abstraction"),
        ("pv-hmac-source", "proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv", "model", "M1", "paper-mainline", "authoritative", "logs/variants/hmac-confirmation/proverif/summary.txt", "HMAC confirmation only; not AEAD"),
        ("tamarin-v6", "tamarin/kwaay_splitkem_batch_dynamic_v6.spthy", "model", "M0", "regression-only", "authoritative", "logs/tamarin-v6/summary.txt", limitation),
        ("tamarin-v7", "tamarin/kwaay_splitkem_batch_dynamic_v7.spthy", "model", "M0", "regression-only", "authoritative", "logs/tamarin-v7/summary.txt", limitation),
        ("replay-original", "tamarin/replay/kwaay_replay_original.spthy", "model", "M1", "paper-mainline", "authoritative", "logs/tamarin-replay-hmac-only/original-regression-summary.txt", limitation),
        ("replay-hmac", "tamarin/replay/kwaay_replay_hmac_only.spthy", "model", "M1", "paper-mainline", "authoritative", "logs/tamarin-replay-hmac-only/summary.txt", "same receiver state and exact base-message identity"),
        ("impact-original", "tamarin/impact/kwaay_impact_original.spthy", "model", "M2", "paper-mainline", "authoritative", "logs/tamarin-impact-original/summary.txt", "C_install-v2 conditional interface"),
        ("replay-fixed", "tamarin/replay/kwaay_replay_fixed.spthy", "model", "M3", "paper-mainline", "authoritative", "logs/tamarin-m3-closeout/composite-result-vector.tsv", limitation),
        ("impact-fixed", "tamarin/impact/kwaay_impact_fixed.spthy", "model", "M3", "paper-mainline", "authoritative", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "C_install-v2 conditional interface"),
        ("replay-combined", "tamarin/replay/kwaay_replay_hmac_dedup.spthy", "model", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", limitation),
        ("impact-combined", "tamarin/impact/kwaay_impact_hmac_dedup.spthy", "model", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "C_install-v2 conditional interface"),
        ("m1-runner", "tamarin/replay/run-hmac-only.sh", "runner", "M1", "regression-only", "authoritative", "logs/tamarin-replay-hmac-only/summary.txt", "legacy runner; not called in-place"),
        ("m2-runner", "tamarin/impact/run-impact-original.sh", "runner", "M2", "regression-only", "authoritative", "logs/tamarin-impact-original/summary.txt", "legacy runner; not called in-place"),
        ("m3-runner", "tamarin/milestones/run-m3-dedup.sh", "runner", "M3", "regression-only", "authoritative", "logs/tamarin-m3-closeout/closeout-summary.txt", "legacy runner; not called in-place"),
        ("m4-runner", M4_RUNNER, "runner", "M4", "regression-only", "authoritative", "logs/tamarin-m4-hmac-dedup/composite-summary.txt", "frozen Tamarin-only policy source"),
        ("m1-summary", "logs/tamarin-replay-hmac-only/summary.txt", "evidence", "M1", "paper-mainline", "authoritative", "logs/tamarin-replay-hmac-only/summary.txt", "single committed historical run"),
        ("m1-raw", "logs/tamarin-replay-hmac-only/raw.out", "raw-evidence", "M1", "paper-mainline", "authoritative", "logs/tamarin-replay-hmac-only/summary.txt", "raw HMAC-only replay result"),
        ("m1-versions", "logs/tamarin-replay-hmac-only/versions.txt", "provenance", "M1", "paper-mainline", "authoritative", "logs/tamarin-replay-hmac-only/summary.txt", "historical tool versions"),
        ("m2-summary", "logs/tamarin-impact-original/summary.txt", "evidence", "M2", "paper-mainline", "authoritative", "logs/tamarin-impact-original/SHA256SUMS.txt", "single committed historical run"),
        ("m2-aggregate", "logs/tamarin-impact-original/aggregate-results.tsv", "evidence", "M2", "paper-mainline", "generated", "logs/tamarin-impact-original/SHA256SUMS.txt", "raw-to-summary index"),
        ("m2-manifest", "logs/tamarin-impact-original/SHA256SUMS.txt", "manifest", "M2", "paper-mainline", "authoritative", "logs/tamarin-impact-original/SHA256SUMS.txt", "SHA-256 manifest"),
        ("m3-summary", "logs/tamarin-m3-closeout/closeout-summary.txt", "evidence", "M3", "paper-mainline", "authoritative", "logs/tamarin-m3-closeout/SHA256SUMS.txt", "transparent two-run composite"),
        ("m3-selection", "logs/tamarin-m3-closeout/composite-selection.tsv", "evidence", "M3", "paper-mainline", "generated", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "Run 2 primary; Run 1 fallback"),
        ("m3-vector", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "evidence", "M3", "paper-mainline", "generated", "logs/tamarin-m3-closeout/closeout-summary.txt", "196-target transparent composite"),
        ("m3-manifest", "logs/tamarin-m3-closeout/SHA256SUMS.txt", "manifest", "M3", "paper-mainline", "authoritative", "logs/tamarin-m3-closeout/SHA256SUMS.txt", "composite raw-to-summary binding"),
        ("m3-source-manifests", "logs/tamarin-m3-closeout/source-manifests.txt", "provenance", "M3", "paper-mainline", "authoritative", "logs/tamarin-m3-closeout/SHA256SUMS.txt", "two source-run manifest binding"),
        ("m4-summary", "logs/tamarin-m4-hmac-dedup/composite-summary.txt", "evidence", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt", "no single 296/296 terminal source run"),
        ("m4-selection", "logs/tamarin-m4-hmac-dedup/composite-selection.tsv", "evidence", "M4", "paper-mainline", "generated", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "Run 1 primary; Run 2 fallback"),
        ("m4-vector", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "evidence", "M4", "paper-mainline", "generated", "logs/tamarin-m4-hmac-dedup/composite-summary.txt", "296-target Tamarin-only composite"),
        ("m4-manifest", "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt", "manifest", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt", "659-entry composite raw-to-summary binding"),
        ("m4-run1-aggregate", "logs/tamarin-m4-hmac-dedup/source-run1/aggregate.tsv", "source-evidence", "M4", "paper-mainline", "generated", "logs/tamarin-m4-hmac-dedup/source-run1/SHA256SUMS.txt", "complete 296-target source invocation; 294 terminal"),
        ("m4-run1-status", "logs/tamarin-m4-hmac-dedup/source-run1/source-run-status.txt", "source-status", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/source-run1/SHA256SUMS.txt", "VALID is structural qualification, not 296 terminal"),
        ("m4-run1-manifest", "logs/tamarin-m4-hmac-dedup/source-run1/SHA256SUMS.txt", "manifest", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt", "327-entry source-run manifest"),
        ("m4-run1-provenance", "logs/tamarin-m4-hmac-dedup/source-run1/provenance.txt", "provenance", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/source-run1/SHA256SUMS.txt", "Commit A/tool/resource binding"),
        ("m4-run2-aggregate", "logs/tamarin-m4-hmac-dedup/source-run2/aggregate.tsv", "source-evidence", "M4", "paper-mainline", "generated", "logs/tamarin-m4-hmac-dedup/source-run2/SHA256SUMS.txt", "complete 296-target source invocation; 291 terminal"),
        ("m4-run2-status", "logs/tamarin-m4-hmac-dedup/source-run2/source-run-status.txt", "source-status", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/source-run2/SHA256SUMS.txt", "VALID is structural qualification, not 296 terminal"),
        ("m4-run2-manifest", "logs/tamarin-m4-hmac-dedup/source-run2/SHA256SUMS.txt", "manifest", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt", "327-entry source-run manifest"),
        ("m4-run2-provenance", "logs/tamarin-m4-hmac-dedup/source-run2/provenance.txt", "provenance", "M4", "paper-mainline", "authoritative", "logs/tamarin-m4-hmac-dedup/source-run2/SHA256SUMS.txt", "Commit A/tool/resource binding"),
        ("v6-summary", "logs/tamarin-v6/summary.txt", "evidence", "M0", "regression-only", "authoritative", "logs/tamarin-v6/summary.txt", "no standalone M0 completion record"),
        ("v7-summary", "logs/tamarin-v7/summary.txt", "evidence", "M0", "regression-only", "authoritative", "logs/tamarin-v7/summary.txt", "no standalone M0 completion record"),
        ("pv-original-summary", "logs/final/proverif/summary.txt", "evidence", "M0", "paper-mainline", "authoritative", "logs/final/proverif/summary.txt", "inherited by M4; not rerun in M4"),
        ("pv-hmac-summary", "logs/variants/hmac-confirmation/proverif/summary.txt", "evidence", "M1", "paper-mainline", "authoritative", "logs/variants/hmac-confirmation/proverif/summary.txt", "inherited by M4; not rerun in M4"),
        ("claim-hierarchy", "docs/claim-hierarchy.md", "claim-source", "M4", "paper-mainline", "authoritative", "docs/claim-hierarchy.md", "statement boundary authority"),
        ("threat-matrix", "docs/threat-compromise-matrix.md", "claim-source", "M4", "paper-mainline", "authoritative", "docs/threat-compromise-matrix.md", "threat assumptions authority"),
        ("model-mapping", "docs/model-mapping.md", "claim-source", "M4", "paper-mainline", "authoritative", "docs/model-mapping.md", "model/query/lemma mapping authority"),
        ("m1-completion", "docs/milestones/M1-completion.md", "completion", "M1", "paper-mainline", "authoritative", "docs/milestones/M1-completion.md", "milestone record"),
        ("m2-completion", "docs/milestones/M2-completion.md", "completion", "M2", "paper-mainline", "authoritative", "docs/milestones/M2-completion.md", "milestone record"),
        ("m3-completion", "docs/milestones/M3-completion.md", "completion", "M3", "paper-mainline", "authoritative", "docs/milestones/M3-completion.md", "milestone record"),
        ("m4-completion", "docs/milestones/M4-completion.md", "completion", "M4", "paper-mainline", "authoritative", "docs/milestones/M4-completion.md", "milestone record"),
    ]
    for family, targets in PV_TARGETS.items():
        milestone = "M0" if family == "original" else "M1"
        for target, (path, _) in targets.items():
            rows.append((
                f"pv-{family}-{target.lower().replace('_', '-')}",
                path, "generated-model", milestone, "regression-only", "generated",
                "logs/final/proverif/summary.txt" if family == "original" else "logs/variants/hmac-confirmation/proverif/summary.txt",
                "exact preprocessed target model",
            ))
    return [
        dict(zip(PAPER_HEADER, [*row[:7], "frozen", row[7]]))
        for row in rows
    ]


POSITIVE_ATTACK_PAIRS = {
    ("original-replay", "one_send_two_accepts_exists"),
    ("original-impact", "one_send_two_accepts_exists"),
    ("original-impact", "one_send_two_accepts_two_installs_exists"),
    ("hmac-replay", "one_confirmed_send_two_accepts_exists"),
}
FALSIFIED_UNIVERSAL_PAIRS = {
    ("original-replay", "same_message_accepted_at_most_once"),
    ("original-replay", "injective_receiver_accept"),
    ("hmac-replay", "confirmed_message_accepted_at_most_once"),
    ("hmac-replay", "injective_confirmed_receiver_accept"),
    ("original-impact", "same_message_accepted_at_most_once"),
    ("original-impact", "injective_receiver_accept"),
    ("original-impact", "unique_install_within_completed_consumer"),
}
BLOCKED_ATTACK_PAIRS = {
    ("fixed-replay", "one_send_two_accepts_exists"),
    ("fixed-impact", "one_send_two_accepts_exists"),
    ("fixed-impact", "one_send_two_accepts_two_installs_exists"),
    ("combined-replay", "one_confirmed_send_two_accepts_exists"),
    ("combined-impact", "one_confirmed_send_two_accepts_exists"),
    ("combined-impact", "one_confirmed_send_two_accepts_two_installs_exists"),
    ("combined-impact", "legacy_same_confirmed_message_consumer_complete_exists"),
}
NON_VACUITY_TARGETS = {
    "normal_single_accept", "normal_batch_complete", "normal_confirmed_single_accept",
    "normal_confirmed_batch_complete", "normal_one_accept_one_install",
    "normal_consumer_complete", "normal_one_confirmed_accept_one_install",
    "normal_distinct_batch_complete", "normal_distinct_consumer_complete",
    "normal_distinct_fail_slot1_exists", "normal_distinct_fail_slot2_exists",
    "normal_two_distinct_valid_confirmed_accepts_complete",
    "normal_two_distinct_valid_confirmed_outputs_consumer_complete",
    "duplicate_batch_fail_exists", "duplicate_same_base_different_tag_fail_exists",
    "hmac_failure_slot1_exists", "hmac_failure_slot2_after_prior_accept_exists",
    "hmac_failure_slot2_after_prior_accept_replay_exists",
    "executable_add_slot", "executable_seal_batch", "executable_process_slot",
    "executable_batch_complete", "executable_batch_fail",
    "executable_four_slots_added", "executable_four_slots_processed",
}
STRUCTURAL_TARGETS = {
    "confirmed_receiver_accept_has_sender", "receiver_accept_has_sender",
    "confirmed_receiver_accept_has_output", "receiver_accept_has_output",
    "accept_output_has_same_time_accept", "accept_output_has_same_time_confirmed_accept",
    "install_has_prior_accept", "install_session_has_interface_origin",
    "install_from_accept_has_session", "install_event_has_single_source",
    "install_requires_batch_complete", "consumer_complete_requires_all_outputs_installed",
    "confirmed_accept_requires_valid_tag", "confirmed_accept_requires_hmac_validated",
    "slot_origin", "slot_origin_without_early_compromise",
    "slot_key_known_requires_exception",
}
DIRECT_THEOREM_TARGETS = {
    "same_message_accepted_at_most_once", "confirmed_message_accepted_at_most_once",
    "confirmed_base_message_accepted_at_most_once", "injective_receiver_accept",
    "injective_confirmed_receiver_accept", "full_message_unique_send",
    "confirmed_message_unique_send", "receiver_accept_has_unique_output",
    "confirmed_receiver_accept_has_unique_output", "accept_id_unique",
    "install_handle_unique", "accept_output_installed_at_most_once",
    "distinct_accept_sources_have_distinct_handles",
    "unique_install_within_completed_consumer",
    "partnered_slot_key_not_attacker_known_without_early_compromise",
    "hmac_failed_slot_has_no_accept", "duplicate_batch_has_no_accept",
    "duplicate_batch_has_no_accept_output", "duplicate_batch_has_no_install",
    "duplicate_detected_before_any_accept", "no_consumer_after_failed_batch",
}
CONDITIONAL_INSTALL_TARGETS = {
    "consumer_complete_single_use", "no_install_after_consumer_close",
}


def property_kind(suite: str, target: str) -> str:
    pair = (suite, target)
    if pair in POSITIVE_ATTACK_PAIRS:
        return "positive_attack_witness"
    if pair in FALSIFIED_UNIVERSAL_PAIRS:
        return "falsified_universal_property"
    if pair in BLOCKED_ATTACK_PAIRS:
        return "blocked_attack_witness_regression"
    if target in NON_VACUITY_TARGETS:
        return "non_vacuity"
    if target in STRUCTURAL_TARGETS:
        return "structural_result"
    if target in CONDITIONAL_INSTALL_TARGETS:
        return "conditional_C_install_v2"
    if target in DIRECT_THEOREM_TARGETS:
        return "direct_theorem"
    return "regression"


def tamarin_rows(root: Path) -> list[dict[str, str]]:
    matrix = read_git_tsv(
        root, BASE_COMMIT, M4_MATRIX, ["suite", "target", "expected_status"]
    )
    formulas = read_git_tsv(
        root, BASE_COMMIT, M4_FORMULAS,
        ["suite", "target", "formula_body_sha256"],
    )
    recorded = {(row["suite"], row["target"]): row["formula_body_sha256"] for row in formulas}
    rows: list[dict[str, str]] = []
    for item in matrix:
        suite, target, expected = (
            item["suite"], item["target"], item["expected_status"]
        )
        source_path, source_commit = HISTORICAL_EXPECTATION[suite]
        source_blob = git_blob_oid(root, source_commit, source_path)
        milestone, model_path, claim = SUITES[suite]
        formula = extract_tamarin_lemma(git_blob(root, BASE_COMMIT, model_path), target)
        digest = formula_sha(formula)
        if recorded.get((suite, target)) != digest:
            raise ContractError(f"M4 formula digest conflict: {suite}/{target}")
        conditional = "C_install-v2" if suite.endswith("impact") else "none"
        rows.append({
            "schema_version": "1",
            "property_id": f"tam-{suite}-{target}",
            "claim_id": claim,
            "milestone": milestone,
            "tool": "tamarin-prover",
            "suite": suite,
            "target_id": target,
            "model_path": model_path,
            "query_or_lemma": target,
            "formula_sha256": digest,
            "property_kind": property_kind(suite, target),
            "expected_status": expected,
            "expected_evidence_class": "m4-transparent-composite",
            "execution_scope": "direct",
            "conditional_interface": conditional,
            "required": "true",
            "timeout_seconds": "300",
            "memory_policy": M4_MEMORY,
            "expectation_source_path": source_path,
            "expectation_source_commit": source_commit,
            "expectation_source_blob": source_blob,
            "regression_matrix_path": M4_MATRIX,
            "regression_matrix_commit": BASE_COMMIT,
            "regression_matrix_blob": git_blob_oid(root, BASE_COMMIT, M4_MATRIX),
            "notes": "historical milestone authority plus independent M4 296-row regression binding",
        })
    return rows


PV_SEMANTIC_PROFILES = {
    "original-q6-direct": [
        ("P0-O", "non_vacuity"), ("P1", "falsified_universal_property"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "direct_theorem"), ("P0-S", "direct_theorem"),
    ],
    "original-q6-falsified": [
        ("P0-O", "non_vacuity"), ("P1", "falsified_universal_property"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "direct_theorem"), ("P0-S", "falsified_universal_property"),
    ],
    "original-both-secrecy-falsified": [
        ("P0-O", "non_vacuity"), ("P1", "falsified_universal_property"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "falsified_universal_property"),
        ("P0-S", "falsified_universal_property"),
    ],
    "exception-choice": [
        ("P0-O", "non_vacuity"), ("P1", "falsified_universal_property"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "falsified_universal_property"),
        ("P0-S", "falsified_universal_property"),
        ("P0-S", "direct_theorem"),
    ],
    "receiver-exception": [
        ("P0-S", "direct_theorem"), ("P0-S", "falsified_universal_property"),
    ],
    "component": [("P0-O", "structural_result")],
    "hmac-baseline": [
        ("P0-O", "non_vacuity"), ("P1", "direct_theorem"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "direct_theorem"), ("P0-S", "direct_theorem"),
    ],
    "hmac-leak-sigsk-a": [
        ("P0-O", "non_vacuity"), ("P1", "falsified_universal_property"),
        ("P0-O", "structural_result"), ("P0-O", "structural_result"),
        ("P0-S", "direct_theorem"), ("P0-S", "falsified_universal_property"),
    ],
}
PV_TARGET_PROFILES = {
    ("original", "BASELINE"): "original-q6-direct",
    ("original", "COMPONENT"): "component",
    ("original", "EXCEPTION_CHOICE"): "exception-choice",
    ("original", "RECEIVER_EXCEPTION_CLASSIFICATION"): "receiver-exception",
    ("original", "LEAK_SIGSK_A"): "original-q6-falsified",
    ("original", "LEAK_SIGSK_B"): "original-q6-direct",
    ("original", "LEAK_SIGSK_AB"): "original-q6-falsified",
    ("original", "LEAK_SIGSK"): "original-q6-falsified",
    ("original", "LEAK_KEMSK"): "original-q6-direct",
    ("original", "LEAK_EKEMSK"): "original-q6-direct",
    ("original", "LEAK_RSKEMSK"): "original-q6-falsified",
    ("original", "LEAK_SSKEMSK"): "original-q6-falsified",
    ("original", "LEAK_KEMSK_EKEMSK"): "original-q6-direct",
    ("original", "LEAK_ALL_RECEIVER_SECRETS"): "original-both-secrecy-falsified",
    ("hmac", "HMAC_BASELINE"): "hmac-baseline",
    ("hmac", "HMAC_COMPONENT"): "component",
    ("hmac", "HMAC_LEAK_SIGSK_A"): "hmac-leak-sigsk-a",
}


def pv_claim(family: str, target: str, query_number: int) -> tuple[str, str]:
    """Return an explicit reviewed semantic assignment; inspect no result text."""
    try:
        profile = PV_SEMANTIC_PROFILES[PV_TARGET_PROFILES[(family, target)]]
        return profile[query_number - 1]
    except (KeyError, IndexError) as exc:
        raise ContractError(
            f"missing explicit ProVerif semantic mapping: "
            f"{family}/{target}/q{query_number:02d}"
        ) from exc


def proverif_rows(root: Path) -> list[dict[str, str]]:
    original_summary = parse_proverif_summary(
        git_blob(root, BASE_COMMIT, "logs/final/proverif/summary.txt")
    )
    hmac_summary = parse_proverif_summary(
        git_blob(root, BASE_COMMIT, "logs/variants/hmac-confirmation/proverif/summary.txt")
    )
    actual = {"original": original_summary, "hmac": hmac_summary}
    source_path = {
        "original": "docs/proverif-final-results.md",
        "hmac": "proverif/variants/hmac-confirmation/README.md",
    }
    rows: list[dict[str, str]] = []
    for family, targets in PV_TARGETS.items():
        milestone = "M0" if family == "original" else "M1"
        suite = f"proverif-{family}"
        for target, (model_path, expected_statuses) in targets.items():
            queries = extract_proverif_queries(git_blob(root, BASE_COMMIT, model_path))
            if len(queries) != len(expected_statuses):
                raise ContractError(f"query/expectation count conflict for {target}")
            if actual[family].get(target) != expected_statuses:
                raise ContractError(f"committed ProVerif actual conflicts with expectation for {target}")
            if family == "original" and target in {"LEAK_SIGSK_A", "LEAK_SIGSK_B", "LEAK_SIGSK_AB"}:
                expectation_path = "docs/threat-compromise-matrix.md"
                expectation_commit = PV_THREAT_MATRIX_COMMIT
            else:
                expectation_path = source_path[family]
                expectation_commit = PV_EXPECTATION_COMMITS[family]
            expectation_blob = git_blob_oid(root, expectation_commit, expectation_path)
            summary_path = (
                "logs/final/proverif/summary.txt"
                if family == "original"
                else "logs/variants/hmac-confirmation/proverif/summary.txt"
            )
            for number, (query, expected) in enumerate(
                zip(queries, expected_statuses, strict=True), 1
            ):
                claim, kind = pv_claim(family, target, number)
                common = {
                    "schema_version": "1",
                    "claim_id": claim,
                    "tool": "proverif",
                    "suite": suite,
                    "target_id": target,
                    "model_path": model_path,
                    "query_or_lemma": query,
                    "formula_sha256": formula_sha(query),
                    "property_kind": kind,
                    "conditional_interface": "none",
                    "required": "true",
                    "timeout_seconds": "300",
                    "memory_policy": "no committed memory cap; compatibility untested",
                    "regression_matrix_path": summary_path,
                    "regression_matrix_commit": BASE_COMMIT,
                    "regression_matrix_blob": git_blob_oid(root, BASE_COMMIT, summary_path),
                }
                rows.append({
                    **common,
                    "property_id": f"pv-{family}-{target.lower()}-q{number:02d}",
                    "milestone": milestone,
                    "expected_status": expected,
                    "expected_evidence_class": "committed-inherited-evidence",
                    "execution_scope": "inherited",
                    "expectation_source_path": expectation_path,
                    "expectation_source_commit": expectation_commit,
                    "expectation_source_blob": expectation_blob,
                    "notes": "prior committed ProVerif evidence; independent of M4 execution scope",
                })
                if (family, target) in M4_SCOPE_TARGETS:
                    rows.append({
                        **common,
                        "property_id": f"m4-pv-{family}-{target.lower()}-q{number:02d}",
                        "milestone": "M4",
                        "property_kind": "scope_declaration",
                        "expected_status": "not_run_out_of_scope",
                        "expected_evidence_class": "scope-declaration",
                        "execution_scope": "tamarin-only",
                        "expectation_source_path": M4_RUNNER,
                        "expectation_source_commit": M4_BASELINE,
                        "expectation_source_blob": git_blob_oid(root, M4_BASELINE, M4_RUNNER),
                        "regression_matrix_path": M4_RUNNER,
                        "regression_matrix_commit": M4_BASELINE,
                        "regression_matrix_blob": git_blob_oid(root, M4_BASELINE, M4_RUNNER),
                        "notes": "M4 execution-scope declaration; independent inherited row retained",
                    })
    return rows


def claim_rows() -> list[dict[str, str]]:
    refs = {
        "assumptions_ref": "docs/threat-compromise-matrix.md",
        "limitations_ref": "docs/model-mapping.md",
        "allowed_statement_ref": "docs/claim-hierarchy.md",
        "prohibited_statement_ref": "docs/claim-hierarchy.md",
    }
    data = [
        ("P0-S", "paper-mainline", "pv-original-baseline-q05", "inherited evidence", "logs/final/proverif/generated/BASELINE.pv", "logs/final/proverif/summary.txt", "true"),
        ("P0-O", "paper-mainline", "pv-original-component-q01", "structural result", "logs/final/proverif/generated/COMPONENT.pv", "logs/final/proverif/summary.txt", "true"),
        ("P1", "paper-mainline", "pv-original-baseline-q02", "falsified universal property", "logs/final/proverif/generated/BASELINE.pv", "logs/final/proverif/summary.txt", "false"),
        ("P1", "paper-mainline", "pv-hmac-hmac_baseline-q02", "direct theorem", "logs/variants/hmac-confirmation/proverif/generated/HMAC_BASELINE.pv", "logs/variants/hmac-confirmation/proverif/summary.txt", "true"),
        ("P1", "paper-mainline", "pv-hmac-hmac_leak_sigsk_a-q02", "falsified universal property", "logs/variants/hmac-confirmation/proverif/generated/HMAC_LEAK_SIGSK_A.pv", "logs/variants/hmac-confirmation/proverif/summary.txt", "false"),
        ("P2", "paper-mainline", "tam-original-replay-one_send_two_accepts_exists", "positive attack witness", "tamarin/replay/kwaay_replay_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P2", "paper-mainline", "tam-original-replay-same_message_accepted_at_most_once", "falsified universal property", "tamarin/replay/kwaay_replay_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "falsified"),
        ("P2", "paper-mainline", "tam-original-replay-receiver_accept_has_sender", "direct theorem", "tamarin/replay/kwaay_replay_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P2", "paper-mainline", "tam-original-replay-normal_single_accept", "non-vacuity result", "tamarin/replay/kwaay_replay_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P2", "paper-mainline", "tam-original-impact-one_send_two_accepts_two_installs_exists", "positive attack witness", "tamarin/impact/kwaay_impact_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P2", "paper-mainline", "tam-original-impact-unique_install_within_completed_consumer", "falsified universal property", "tamarin/impact/kwaay_impact_original.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "falsified"),
        ("P3", "paper-mainline", "tam-fixed-replay-one_send_two_accepts_exists", "blocked attack witness regression", "tamarin/replay/kwaay_replay_fixed.spthy", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "falsified"),
        ("P3", "paper-mainline", "tam-fixed-replay-same_message_accepted_at_most_once", "direct theorem", "tamarin/replay/kwaay_replay_fixed.spthy", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "verified"),
        ("P3", "paper-mainline", "tam-fixed-impact-unique_install_within_completed_consumer", "conditional C_install-v2 result", "tamarin/impact/kwaay_impact_fixed.spthy", "logs/tamarin-m3-closeout/composite-result-vector.tsv", "verified"),
        ("P3", "paper-mainline", "tam-combined-replay-confirmed_message_accepted_at_most_once", "transparent composite", "tamarin/replay/kwaay_replay_hmac_dedup.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P3", "paper-mainline", "tam-combined-impact-unique_install_within_completed_consumer", "conditional C_install-v2 result", "tamarin/impact/kwaay_impact_hmac_dedup.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("P3", "regression-only", "tam-v6-executable_seal_batch", "regression", "tamarin/kwaay_splitkem_batch_dynamic_v6.spthy", "logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv", "verified"),
        ("M4-SCOPE", "paper-mainline", "m4-pv-original-baseline-q02", "scope declaration", "logs/final/proverif/generated/BASELINE.pv", "artifact/results/expected-results.tsv", "not_run_out_of_scope"),
    ]
    return [
        {
            "claim_id": claim,
            "paper_class": paper_class,
            "property_id": property_id,
            "evidence_role": role,
            "model_path": model,
            "evidence_path": evidence,
            **refs,
            "status": status,
        }
        for claim, paper_class, property_id, role, model, evidence, status in data
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare generated bytes without writing")
    args = parser.parse_args()
    root = repo_root()
    paper = paper_rows()
    expected = tamarin_rows(root) + proverif_rows(root)
    claims = claim_rows()
    proverif_targets = []
    for family, targets in PV_TARGETS.items():
        for target, (model_path, _) in targets.items():
            proverif_targets.append({
                "family": family,
                "suite": f"proverif-{family}",
                "target_id": target,
                "model_path": model_path,
                "query_count": str(len(extract_proverif_queries(git_blob(root, BASE_COMMIT, model_path)))),
                "inherited": "true",
                "m4_execution_scope": "true" if (family, target) in M4_SCOPE_TARGETS else "false",
            })
    frozen = []
    for row in paper:
        path = row["path"]
        data = git_blob(root, BASE_COMMIT, path)
        frozen.append({
            "path": path,
            "source_commit": BASE_COMMIT,
            "git_blob": git_blob_oid(root, BASE_COMMIT, path),
            "blob_sha256": sha256(data),
            "content_role": f"{row['artifact_class']}:{row['paper_role']}",
        })
    targets = [
        (root / "artifact/manifest/paper-mainline.tsv", PAPER_HEADER, paper),
        (root / "artifact/manifest/frozen-inputs.tsv", FROZEN_HEADER, frozen),
        (root / "artifact/results/expected-results.tsv", EXPECTED_HEADER, expected),
        (
            root / "artifact/manifest/property-semantics.tsv",
            SEMANTICS_HEADER,
            [{field: row[field] for field in SEMANTICS_HEADER} for row in expected],
        ),
        (
            root / "artifact/manifest/proverif-targets.tsv",
            PROVERIF_TARGET_HEADER,
            proverif_targets,
        ),
        (root / "artifact/results/claim-evidence.tsv", CLAIM_HEADER, claims),
    ]
    if args.check:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            for target, header, rows in targets:
                candidate = Path(tmp) / target.name
                write_tsv(candidate, header, rows)
                if not target.exists() or target.read_bytes() != candidate.read_bytes():
                    raise ContractError(f"generated contract is stale: {target.relative_to(root)}")
    else:
        for target, header, rows in targets:
            write_tsv(target, header, rows)
    print(
        f"paper_mainline_rows={len(paper)} frozen_rows={len(frozen)} "
        f"expected_rows={len(expected)} claim_rows={len(claims)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
