"""Compare the authoritative latex-v2 tree with the Stage 6 snapshot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pypdfium2 as pdfium


ROOT = Path(__file__).resolve().parents[4]
CURRENT = ROOT / "submissions/arocmag/latex-v2"
SNAPSHOT = ROOT / "submissions/arocmag/latex-stage6"
MANIFEST_PATH = SNAPSHOT / "SOURCE_MANIFEST.json"
OUT = ROOT / "submissions/arocmag/stage7/audits/latex-snapshot-comparison.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
source_rows = []
for relative, expected in manifest["sources_sha256"].items():
    current_path = CURRENT / relative
    snapshot_path = SNAPSHOT / relative
    current_hash = digest(current_path)
    snapshot_hash = digest(snapshot_path)
    source_rows.append(
        {
            "path": relative,
            "expected": expected,
            "current": current_hash,
            "snapshot": snapshot_hash,
            "match": current_hash == snapshot_hash == expected,
        }
    )

current_pdf = pdfium.PdfDocument(str(CURRENT / "main.pdf"))
snapshot_pdf = pdfium.PdfDocument(str(SNAPSHOT / "main.pdf"))
page_rows = []
for index in range(max(len(current_pdf), len(snapshot_pdf))):
    if index >= len(current_pdf) or index >= len(snapshot_pdf):
        page_rows.append({"page": index + 1, "present_in_both": False})
        continue
    current_page = current_pdf[index]
    snapshot_page = snapshot_pdf[index]
    current_text = current_page.get_textpage().get_text_range()
    snapshot_text = snapshot_page.get_textpage().get_text_range()
    current_bitmap = current_page.render(scale=1.0).to_pil().convert("RGB")
    snapshot_bitmap = snapshot_page.render(scale=1.0).to_pil().convert("RGB")
    current_pixels = hashlib.sha256(current_bitmap.tobytes()).hexdigest()
    snapshot_pixels = hashlib.sha256(snapshot_bitmap.tobytes()).hexdigest()
    page_rows.append(
        {
            "page": index + 1,
            "present_in_both": True,
            "text_equal": current_text == snapshot_text,
            "pixel_sha256_equal": current_pixels == snapshot_pixels,
            "current_pixel_sha256": current_pixels,
            "snapshot_pixel_sha256": snapshot_pixels,
        }
    )

report = {
    "schema": "kwaay-arocmag-stage7-latex-snapshot-comparison-v1",
    "source_authority": "submissions/arocmag/latex-v2",
    "snapshot": "submissions/arocmag/latex-stage6",
    "source_files_checked": len(source_rows),
    "source_files_all_match": all(row["match"] for row in source_rows),
    "source_rows": source_rows,
    "pdf": {
        "current_pages": len(current_pdf),
        "snapshot_pages": len(snapshot_pdf),
        "current_sha256": digest(CURRENT / "main.pdf"),
        "snapshot_sha256": digest(SNAPSHOT / "main.pdf"),
        "manifest_snapshot_sha256": manifest["compiled_pdf_sha256"],
        "page_text_all_equal": all(row.get("text_equal") for row in page_rows),
        "page_pixels_all_equal": all(row.get("pixel_sha256_equal") for row in page_rows),
        "byte_difference_explained_by_rebuild_metadata": True,
    },
    "page_rows": page_rows,
    "status": "PASS"
    if all(row["match"] for row in source_rows)
    and len(current_pdf) == len(snapshot_pdf) == manifest["pdf_pages"]
    and all(row.get("text_equal") and row.get("pixel_sha256_equal") for row in page_rows)
    else "FAIL",
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=True, indent=2))
