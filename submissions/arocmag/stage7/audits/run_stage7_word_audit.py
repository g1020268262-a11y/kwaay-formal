"""Stage 7 read-only audit for the frozen AROCMAG Word manuscript.

The script reads the tracked DOCX bytes from Git so the audit remains possible
while WPS holds the working-tree file open.  It never invokes Tamarin or
ProVerif and never rewrites the manuscript.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
import unicodedata
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[4]
STAGE7 = ROOT / "submissions/arocmag/stage7"
QA = STAGE7 / "qa"
AUDITS = STAGE7 / "audits"
DOCX_REL = "submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage6.docx"
DOCX = ROOT / DOCX_REL
WPS_PDF = ROOT / "submissions/arocmag/word-final/K-Waay-AROCMAG-submission-stage6-preview.pdf"
STAGE6_QA = ROOT / "submissions/arocmag/word-final/qa/stage6"
LROOT = ROOT / "submissions/arocmag/latex-v2"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "o": "urn:schemas-microsoft-com:office:office",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def git_bytes(path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", f"HEAD:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def text(node: etree._Element) -> str:
    return "".join(node.xpath(".//w:t/text()|.//m:t/text()", namespaces=NS))


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return re.sub(r"[\s\u200b\u00ad]", "", value)


def style(paragraph: etree._Element) -> str:
    return paragraph.xpath("string(./w:pPr/w:pStyle/@w:val)", namespaces=NS)


def result(status: str, evidence: object, detail: str = "") -> dict[str, object]:
    return {"status": status, "evidence": evidence, "detail": detail}


AUDITS.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)

docx_bytes = git_bytes(DOCX_REL)
with zipfile.ZipFile(io.BytesIO(docx_bytes)) as package:
    bad_member = package.testzip()
    parts = {name: package.read(name) for name in package.namelist()}

document = etree.fromstring(parts["word/document.xml"])
body = document.find("w:body", NS)
paragraphs = body.findall("w:p", NS)
tables = body.findall("w:tbl", NS)

formula_nodes = document.xpath(".//m:oMath", namespaces=NS)
formula_text = [text(node) for node in formula_nodes]
with (STAGE6_QA / "FORMULA_CHECKLIST_STAGE6.csv").open(
    encoding="utf-8-sig", newline=""
) as handle:
    old_formula_rows = list(csv.DictReader(handle))
expected_formula_text = [row["visible_math"] for row in old_formula_rows]
formula_mismatches = [
    index
    for index, (actual, expected) in enumerate(
        zip(formula_text, expected_formula_text), start=1
    )
    if norm(actual) != norm(expected)
]
if len(formula_text) != len(expected_formula_text):
    formula_mismatches.extend(
        range(min(len(formula_text), len(expected_formula_text)) + 1,
              max(len(formula_text), len(expected_formula_text)) + 1)
    )

display_paragraphs = [p for p in paragraphs if style(p) == "74"]
display_labels = []
for paragraph in display_paragraphs:
    match = re.search(r"\(([1-3])\)", text(paragraph))
    if match:
        display_labels.append(f"({match.group(1)})")

with (QA / "FORMULA_CHECKLIST_STAGE7.csv").open(
    "w", encoding="utf-8-sig", newline=""
) as handle:
    writer = csv.writer(handle)
    writer.writerow(
        ["index", "visible_math", "format", "external_status", "stage6_match"]
    )
    for index, value in enumerate(formula_text, start=1):
        writer.writerow(
            [
                index,
                value,
                "OMML",
                "MATHTYPE_CONVERSION_BLOCKED",
                "PASS" if index not in formula_mismatches else "FAIL",
            ]
        )

relationships = etree.fromstring(parts["word/_rels/document.xml.rels"])
rels = {
    rel.get("Id"): rel
    for rel in relationships
    if rel.get("Id") is not None
}
embedded_targets = []
for blip in document.xpath(".//a:blip", namespaces=NS):
    rel_id = blip.get(f"{{{NS['r']}}}embed")
    rel = rels.get(rel_id)
    if rel is not None:
        embedded_targets.append(rel.get("Target"))

media = []
for target in embedded_targets:
    part = "word/" + target.replace("\\", "/")
    data = parts.get(part)
    entry: dict[str, object] = {"part": part, "sha256": sha256(data or b"")}
    if data:
        try:
            with Image.open(io.BytesIO(data)) as image:
                entry.update(
                    {
                        "format": image.format,
                        "pixels": list(image.size),
                        "dpi": list(image.info.get("dpi", (None, None))),
                    }
                )
        except Exception as exc:  # pragma: no cover - diagnostic only
            entry["read_error"] = str(exc)
    media.append(entry)

core = etree.fromstring(parts["docProps/core.xml"])
core_metadata = {
    "creator": core.xpath("string(./dc:creator)", namespaces=NS),
    "last_modified_by": core.xpath("string(./cp:lastModifiedBy)", namespaces=NS),
    "title": core.xpath("string(./dc:title)", namespaces=NS),
    "subject": core.xpath("string(./dc:subject)", namespaces=NS),
    "keywords": core.xpath("string(./cp:keywords)", namespaces=NS),
}

story_xml = {
    name: etree.fromstring(data)
    for name, data in parts.items()
    if name.startswith("word/") and name.endswith(".xml")
}
tracked_changes = sum(
    len(tree.xpath(".//w:ins|.//w:del|.//w:moveFrom|.//w:moveTo", namespaces=NS))
    for tree in story_xml.values()
)
hidden_runs = sum(
    len(tree.xpath(".//w:vanish|.//w:webHidden", namespaces=NS))
    for tree in story_xml.values()
)
comment_parts = sorted(name for name in parts if "comments" in name.lower())
ole_parts = sorted(name for name in parts if name.startswith("word/embeddings/"))
ole_nodes = len(document.xpath(".//w:object|.//o:OLEObject", namespaces=NS))
ole_relationships = [
    {"id": rel.get("Id"), "target": rel.get("Target"), "type": rel.get("Type")}
    for rel in relationships
    if (rel.get("Type") or "").endswith("/oleObject")
]
external_relationships = [
    {"id": rel.get("Id"), "target": rel.get("Target"), "type": rel.get("Type")}
    for rel in relationships
    if rel.get("TargetMode") == "External"
]

xml_text = "\n".join(
    data.decode("utf-8", "ignore")
    for name, data in parts.items()
    if name.endswith((".xml", ".rels"))
)
local_path_hits = sorted(
    set(
        re.findall(
            r"(?:file:///|[A-Za-z]:\\\\)[^\"'<>\s]+",
            xml_text,
            flags=re.IGNORECASE,
        )
    )
)

section_properties = document.xpath(".//w:sectPr", namespaces=NS)
sections = []
for sect in section_properties:
    page_size = sect.find("w:pgSz", NS)
    margins = sect.find("w:pgMar", NS)
    columns = sect.find("w:cols", NS)
    sections.append(
        {
            "page_width_twips": int(page_size.get(f"{{{NS['w']}}}w")) if page_size is not None else None,
            "page_height_twips": int(page_size.get(f"{{{NS['w']}}}h")) if page_size is not None else None,
            "columns": int(columns.get(f"{{{NS['w']}}}num", "1")) if columns is not None else 1,
            "margin_top_twips": int(margins.get(f"{{{NS['w']}}}top")) if margins is not None else None,
            "margin_bottom_twips": int(margins.get(f"{{{NS['w']}}}bottom")) if margins is not None else None,
            "margin_left_twips": int(margins.get(f"{{{NS['w']}}}left")) if margins is not None else None,
            "margin_right_twips": int(margins.get(f"{{{NS['w']}}}right")) if margins is not None else None,
        }
    )

bindings = json.loads((STAGE6_QA / "result-bindings.json").read_text(encoding="utf-8"))
result_rows = [
    [norm(text(cell)) for cell in row.findall("w:tc", NS)]
    for row in tables[-1].findall("w:tr", NS)
][1:]
binding_mismatches = []
model_symbols = {
    "rqv2_relaxed": "R",
    "rqv2_message_dedup": "M",
    "rqv2_party_admission": "P",
}
for row, binding in zip(result_rows, bindings):
    expected = [
        model_symbols[binding["model"]],
        binding["lemma"],
        binding["type"],
        binding["status"],
        binding["steps"],
    ]
    if row[:5] != [norm(value) for value in expected]:
        binding_mismatches.append(binding["lemma"])

source_manifest = json.loads(
    (ROOT / "submissions/arocmag/word-final/qa/stage6/build-manifest.json").read_text(
        encoding="utf-8"
    )
)
source_hash_mismatches = []
for relative, expected in source_manifest["source_hashes"].items():
    actual = sha256((ROOT / relative).read_bytes())
    if actual != expected.upper():
        source_hash_mismatches.append(relative)

protected = json.loads((STAGE6_QA / "baseline.json").read_text(encoding="utf-8"))[
    "protected_sha256"
]
protected_mismatches = []
for relative, expected in protected.items():
    path = ROOT / relative
    if not path.exists() or sha256(path.read_bytes()) != expected.upper():
        protected_mismatches.append(relative)

required_formula_tokens = [
    "∀",
    "⇒",
    "⇔",
    "⇏",
    "≠",
    "τ",
    "ReceiverAccept",
    "BatchReceive",
    "Send",
    "DistinctPartyPerBatch",
]
joined_formula_text = "\n".join(formula_text)
missing_formula_tokens = [
    token for token in required_formula_tokens if token not in joined_formula_text
]

reference_paragraphs = [p for p in paragraphs if style(p) == "84"]
chapter_count = sum(style(p) == "65" for p in paragraphs)
subsection_count = sum(style(p) == "66" for p in paragraphs)
rq_text = [text(p) for p in paragraphs if text(p).startswith(("RQ1", "RQ2", "RQ3"))]
status_counter = Counter(row[3] for row in result_rows)

wps_pages = len(PdfReader(str(WPS_PDF)).pages)

checks = {
    "docx_git_blob_and_stage6_hash": result(
        "PASS" if sha256(docx_bytes) == source_manifest["stage6_sha256"].upper() else "FAIL",
        {
            "sha256": sha256(docx_bytes),
            "expected": source_manifest["stage6_sha256"].upper(),
        },
    ),
    "docx_zip_integrity": result("PASS" if bad_member is None else "FAIL", bad_member),
    "formula_sequence": result(
        "PASS" if len(formula_nodes) == 110 and not formula_mismatches else "FAIL",
        {"actual": len(formula_nodes), "expected": 110, "mismatches": formula_mismatches},
    ),
    "formula_display_grouping": result(
        "PASS" if len(display_paragraphs) == 7 else "FAIL",
        {"display_paragraphs": len(display_paragraphs)},
    ),
    "numbered_formula_labels": result(
        "PASS" if display_labels == ["(1)", "(2)", "(3)"] else "FAIL",
        display_labels,
    ),
    "formula_symbols_and_event_names": result(
        "PASS" if not missing_formula_tokens else "FAIL",
        {"required": required_formula_tokens, "missing": missing_formula_tokens},
    ),
    "mathtype_objects": result(
        "BLOCKED",
        {
            "omml": len(formula_nodes),
            "ole_parts": ole_parts,
            "ole_nodes": ole_nodes,
            "ole_relationships": ole_relationships,
        },
        "No real MathType/OLE equation objects were found; the 110 equations remain editable OMML.",
    ),
    "document_structure": result(
        "PASS"
        if (chapter_count, subsection_count, len(tables), len(embedded_targets), len(reference_paragraphs))
        == (6, 13, 6, 2, 8)
        else "FAIL",
        {
            "chapters": chapter_count,
            "subsections": subsection_count,
            "tables": len(tables),
            "figures": len(embedded_targets),
            "references": len(reference_paragraphs),
            "rq_count": len(rq_text),
        },
    ),
    "result_table": result(
        "PASS"
        if len(result_rows) == 14
        and not binding_mismatches
        and status_counter == {"verified": 13, "falsified": 1}
        else "FAIL",
        {
            "rows": len(result_rows),
            "status_counts": dict(status_counter),
            "binding_mismatches": binding_mismatches,
        },
    ),
    "source_hashes": result(
        "PASS" if not source_hash_mismatches else "FAIL",
        {"checked": len(source_manifest["source_hashes"]), "mismatches": source_hash_mismatches},
    ),
    "protected_evidence_hashes": result(
        "PASS" if not protected_mismatches else "FAIL",
        {"checked": len(protected), "mismatches": protected_mismatches},
    ),
    "review_markup_and_hidden_content": result(
        "PASS" if not comment_parts and not tracked_changes and not hidden_runs else "FAIL",
        {
            "comment_parts": comment_parts,
            "tracked_changes": tracked_changes,
            "hidden_runs": hidden_runs,
        },
    ),
    "external_links_and_local_paths": result(
        "PASS" if not external_relationships and not local_path_hits else "FAIL",
        {
            "external_relationships": external_relationships,
            "local_path_hits": local_path_hits,
        },
    ),
    "anonymous_metadata": result(
        "PASS"
        if core_metadata["creator"] == "Anonymous Author(s)"
        and core_metadata["last_modified_by"] == "Anonymous Author(s)"
        else "FAIL",
        core_metadata,
    ),
    "page_setup": result(
        "PASS"
        if sections
        and all(
            section["page_width_twips"] == 11906
            and section["page_height_twips"] == 16838
            for section in sections
        )
        else "FAIL",
        {"section_count": len(sections), "sections": sections},
    ),
    "embedded_figures": result(
        "PASS"
        if len(media) == 2
        and all(entry.get("format") == "PNG" for entry in media)
        and all((entry.get("dpi") or [None])[0] and (entry.get("dpi") or [0])[0] >= 350 for entry in media)
        else "FAIL",
        media,
        "Article figures are embedded PNG files; this check does not claim vector graphics.",
    ),
    "wps_preview": result(
        "PASS" if wps_pages == 7 else "FAIL",
        {"pages": wps_pages, "sha256": sha256(WPS_PDF.read_bytes())},
        "The PDF producer is WPS Writer. Visual acceptance is recorded separately after page-by-page inspection.",
    ),
    "microsoft_word_render": result(
        "BLOCKED",
        {"microsoft_word_discovered": False},
        "Microsoft Word was not returned by the installed-app inventory.",
    ),
}

report = {
    "schema": "kwaay-arocmag-stage7-word-audit-v1",
    "source": {"path": DOCX_REL, "git_ref": "HEAD", "sha256": sha256(docx_bytes)},
    "formula_checklist": "submissions/arocmag/stage7/qa/FORMULA_CHECKLIST_STAGE7.csv",
    "checks": checks,
    "summary": dict(Counter(item["status"] for item in checks.values())),
    "media": media,
    "metadata": core_metadata,
}

(AUDITS / "word-structure-audit.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(report, ensure_ascii=True, indent=2))
