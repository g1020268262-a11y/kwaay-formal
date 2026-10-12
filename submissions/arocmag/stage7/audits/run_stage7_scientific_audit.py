"""Read-only Stage 7 consistency audit for the frozen R/M/P evidence.

This script parses saved model sources, saved proof stdout, saved trace-audit
text, and the frozen manuscript.  It does not invoke a prover.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "submissions/arocmag/stage7/audits/scientific-consistency-audit.json"
LROOT = ROOT / "submissions/arocmag/latex-v2"
EVIDENCE = ROOT / "reviews/2026-09-16-evidence"
BINDINGS = json.loads(
    (ROOT / "submissions/arocmag/word-final/qa/stage6/result-bindings.json").read_text(
        encoding="utf-8"
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def entry(status: str, evidence: object, detail: str = "") -> dict[str, object]:
    return {"status": status, "evidence": evidence, "detail": detail}


models = {
    "rqv2_relaxed": ROOT / "tamarin/rq-v2-minimal/rqv2_relaxed.spthy",
    "rqv2_message_dedup": ROOT / "tamarin/rq-v2-minimal/rqv2_message_dedup.spthy",
    "rqv2_party_admission": ROOT / "tamarin/rq-v2-minimal/rqv2_party_admission.spthy",
}

model_text = {name: path.read_text(encoding="utf-8") for name, path in models.items()}
model_hashes = {name: sha256(path) for name, path in models.items()}

lemma_records = []
source_mismatches = []
stdout_mismatches = []
for binding in BINDINGS:
    source = model_text[binding["model"]]
    pattern = re.compile(
        rf"(?ms)^lemma\s+{re.escape(binding['lemma'])}:\s*(?P<body>.*?)(?=^lemma\s+|^end\s*$)"
    )
    match = pattern.search(source)
    if match is None:
        source_mismatches.append({"lemma": binding["lemma"], "reason": "missing"})
        continue
    block = match.group("body")
    actual_type = "exists-trace" if re.search(r"(?m)^\s*exists-trace\s*$", block) else "all-traces"
    actual_quantifier = "Ex" if re.search(r'"\s*Ex\b', block) else "All" if re.search(r'"\s*All\b', block) else "UNKNOWN"
    expected_quantifier = "Ex" if binding["type"] == "exists-trace" else "All"
    if actual_type != binding["type"] or actual_quantifier != expected_quantifier:
        source_mismatches.append(
            {
                "lemma": binding["lemma"],
                "expected_type": binding["type"],
                "actual_type": actual_type,
                "expected_quantifier": expected_quantifier,
                "actual_quantifier": actual_quantifier,
            }
        )
    stdout_path = EVIDENCE / f"{binding['model']}-prove.stdout.txt"
    stdout = stdout_path.read_text(encoding="utf-8")
    output_pattern = re.compile(
        re.escape(binding["lemma"])
        + r" \("
        + re.escape(binding["type"])
        + r"\): "
        + re.escape(binding["status"])
        + r"(?: - found trace)? \("
        + re.escape(binding["steps"])
        + r" steps\)"
    )
    if not output_pattern.search(stdout):
        stdout_mismatches.append(binding["lemma"])
    lemma_records.append(
        {
            "model": binding["model"],
            "lemma": binding["lemma"],
            "type": actual_type,
            "quantifier": actual_quantifier,
            "status": binding["status"],
            "steps": int(binding["steps"]),
            "source_block_sha256": hashlib.sha256(block.encode("utf-8")).hexdigest().upper(),
            "stdout": str(stdout_path.relative_to(ROOT)).replace("\\", "/"),
        }
    )

admission_checks = {
    "R_unconstrained": (
        "rule AdmitRelaxedBatch:" in model_text["rqv2_relaxed"]
        and "Neq(m1,m2)" not in model_text["rqv2_relaxed"]
        and "Neq(A1,A2)" not in model_text["rqv2_relaxed"]
    ),
    "M_message_distinct": (
        "rule AdmitDistinctMessages:" in model_text["rqv2_message_dedup"]
        and "Neq(m1,m2)" in model_text["rqv2_message_dedup"]
    ),
    "P_party_distinct": (
        "rule AdmitDistinctParties:" in model_text["rqv2_party_admission"]
        and "Neq(A1,A2)" in model_text["rqv2_party_admission"]
    ),
}

common_lifecycle_tokens = [
    "rule SendMessage:",
    "rule CollectSlot1:",
    "rule CollectSlot2:",
    "rule ProcessSlot1:",
    "rule ProcessSlot2:",
    "BatchReceive(bid,rst)",
    "ReceiverAccept(",
    "!Sent(",
]
common_lifecycle = {
    model: [token for token in common_lifecycle_tokens if token not in source]
    for model, source in model_text.items()
}

trace_summary = (EVIDENCE / "trace-audit-summary.txt").read_text(encoding="utf-8")
trace_checks = {
    "R_one_origin_two_accepts": all(
        token in trace_summary
        for token in [
            "one_send_two_accepts_exists",
            "#r1 ProcessSlot1 | ReceiverAccept( ~a, ~sid, ~m, ~bid, ~rst )",
            "#r2 ProcessSlot2 | ReceiverAccept( ~a, ~sid, ~m, ~bid, ~rst )",
            "#s SendMessage | Send( ~a, ~sid, ~m )",
        ]
    ),
    "M_same_party_distinct_messages": all(
        token in trace_summary
        for token in [
            "same_party_different_messages_batch_exists",
            "#s1 SendMessage | Send( ~a, ~sid, ~m )",
            "#s2 SendMessage | Send( ~a, ~sid.1, ~m.1 )",
        ]
    ),
    "P_nonvacuous_distinct_party": all(
        token in trace_summary
        for token in [
            "distinct_party_batch_exists",
            "#r1 ProcessSlot1 | ReceiverAccept( ~a, ~sid, ~m, ~bid, ~rst )",
            "#r2 ProcessSlot2 | ReceiverAccept( ~a.1, ~sid.1, ~m.1, ~bid, ~rst )",
        ]
    ),
}

manuscript_parts = [
    (LROOT / "sections" / name).read_text(encoding="utf-8")
    for name in [
        "00-abstract.tex",
        "01-introduction.tex",
        "02-problem.tex",
        "03-formal-modeling.tex",
        "04-formal-analysis.tex",
        "05-discussion.tex",
        "06-conclusion.tex",
    ]
]
manuscript = "\n".join(manuscript_parts)
boundary_checks = {
    "receiver_accept_is_abstract": all(
        token in manuscript
        for token in ["不等同于网络输入", "不等同于", "ReceiverAccept"]
    ),
    "sent_is_idealized_origin": all(
        token in manuscript for token in ["理想化", "!Sent", "不实现真实签名或认证过程"]
    ),
    "fixed_two_slot_limit": "固定两槽" in manuscript and "任意批次长度" in manuscript,
    "manual_semantic_derivation_labelled": all(
        token in manuscript for token in ["人工迹语义推导", "不是新增的Tamarin lemma"]
    ),
    "machine_witness_for_M_not_P": "same_party_different_messages_batch_exists" in manuscript,
    "no_M0_M5_import": not re.search(r"\bM[0-5]\b", manuscript),
    "no_deployed_attack_claim": bool(re.search(r"不能推[导出]密钥泄露", manuscript))
    and "也不表明实际实现遗漏了原有条件" in manuscript,
}

status_counter = Counter(binding["status"] for binding in BINDINGS)
type_counter = Counter(binding["type"] for binding in BINDINGS)
checks = {
    "model_admission_conditions": entry(
        "PASS" if all(admission_checks.values()) else "FAIL", admission_checks
    ),
    "common_lifecycle": entry(
        "PASS" if all(not missing for missing in common_lifecycle.values()) else "FAIL",
        common_lifecycle,
    ),
    "lemma_source_quantifiers": entry(
        "PASS" if len(lemma_records) == 14 and not source_mismatches else "FAIL",
        {"records": len(lemma_records), "mismatches": source_mismatches},
    ),
    "saved_stdout_results": entry(
        "PASS"
        if not stdout_mismatches
        and status_counter == {"verified": 13, "falsified": 1}
        and type_counter == {"all-traces": 8, "exists-trace": 6}
        else "FAIL",
        {
            "result_counts": dict(status_counter),
            "quantifier_counts": dict(type_counter),
            "stdout_mismatches": stdout_mismatches,
        },
    ),
    "trace_witness_mapping": entry(
        "PASS" if all(trace_checks.values()) else "FAIL", trace_checks
    ),
    "manuscript_boundaries": entry(
        "PASS" if all(boundary_checks.values()) else "FAIL", boundary_checks
    ),
}

report = {
    "schema": "kwaay-arocmag-stage7-scientific-audit-v1",
    "method": "saved-source/stdout/trace/manuscript parse only; no prover invocation",
    "model_hashes": model_hashes,
    "checks": checks,
    "summary": dict(Counter(item["status"] for item in checks.values())),
    "lemma_records": lemma_records,
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=True, indent=2))
