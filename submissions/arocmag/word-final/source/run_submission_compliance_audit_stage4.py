from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree
from PIL import Image, ImageChops
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[4]
WORD_ROOT = ROOT / "submissions" / "arocmag" / "word-final"
DOCX = WORD_ROOT / "K-Waay-AROCMAG-submission-stage4.docx"
STAGE3_DOCX = WORD_ROOT / "K-Waay-AROCMAG-submission-stage3.1.docx"
FORMULA_OUT = WORD_ROOT / "qa" / "stage4-formula-inventory.json"
COMPLIANCE_OUT = WORD_ROOT / "qa" / "stage4-submission-compliance-audit.json"
STAGE4_PAGES = WORD_ROOT / "qa" / "stage4-render-final"
STAGE3_PAGES = WORD_ROOT / "qa" / "stage3.1-render-final"
STAGE4_PDF = STAGE4_PAGES / "K-Waay-AROCMAG-submission-stage4-verified.pdf"
STAGE3_PDF = STAGE3_PAGES / "K-Waay-AROCMAG-submission-stage3.1-verified.pdf"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def xml_text(root: etree._Element) -> str:
    return "".join(root.xpath(".//w:t/text() | .//m:t/text()", namespaces=NS))


def formula_inventory(document_xml: bytes) -> dict:
    root = etree.fromstring(document_xml)
    objects = []
    displays = []
    object_index = 0
    for paragraph_index, paragraph in enumerate(root.xpath(".//w:p", namespaces=NS), 1):
        style_values = paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
        style_id = style_values[0] if style_values else None
        paragraph_text = xml_text(paragraph)
        math_objects = paragraph.xpath(".//m:oMath", namespaces=NS)
        is_display = style_id == "74"
        number_match = re.search(r"\(([1-3])\)\s*$", paragraph_text)
        if is_display:
            displays.append({
                "paragraph_index": paragraph_index,
                "number": int(number_match.group(1)) if number_match else None,
                "math_object_count": len(math_objects),
                "text": paragraph_text,
            })
        for math_index, math in enumerate(math_objects, 1):
            object_index += 1
            objects.append({
                "object_index": object_index,
                "paragraph_index": paragraph_index,
                "object_in_paragraph": math_index,
                "kind": "display-member" if is_display else "inline",
                "display_number": int(number_match.group(1)) if number_match else None,
                "math_text": "".join(math.xpath(".//m:t/text()", namespaces=NS)),
                "paragraph_context": paragraph_text,
            })
    result = {
        "format": "editable OMML",
        "mathtype_status": "MATHTYPE_CONVERSION_BLOCKED",
        "total_omml_objects": len(objects),
        "inline_omml_objects": sum(item["kind"] == "inline" for item in objects),
        "display_member_omml_objects": sum(item["kind"] == "display-member" for item in objects),
        "display_formula_paragraphs": len(displays),
        "numbered_display_formulas": sum(item["number"] is not None for item in displays),
        "unnumbered_display_formulas": sum(item["number"] is None for item in displays),
        "display_formulas": displays,
        "objects": objects,
    }
    return result


def page_comparison() -> list[dict]:
    comparisons = []
    for number in range(1, 7):
        previous_path = STAGE3_PAGES / f"verified-page-{number}.png"
        current_path = STAGE4_PAGES / f"verified-page-{number}.png"
        previous = Image.open(previous_path).convert("RGB")
        current = Image.open(current_path).convert("RGB")
        difference = ImageChops.difference(previous, current)
        bbox = difference.getbbox()
        comparisons.append({
            "page": number,
            "same_dimensions": previous.size == current.size,
            "pixel_identical": bbox is None,
            "difference_bbox": list(bbox) if bbox else None,
        })
    return comparisons


def pdf_text_comparison() -> list[dict]:
    previous = PdfReader(str(STAGE3_PDF))
    current = PdfReader(str(STAGE4_PDF))
    comparisons = []
    for number, (previous_page, current_page) in enumerate(zip(previous.pages, current.pages), 1):
        previous_text = re.sub(r"\s+", "", previous_page.extract_text() or "")
        current_text = re.sub(r"\s+", "", current_page.extract_text() or "")
        comparisons.append({
            "page": number,
            "text_identical": previous_text == current_text,
            "stage3_1_character_count": len(previous_text),
            "stage4_character_count": len(current_text),
        })
    return comparisons


def main() -> None:
    with zipfile.ZipFile(DOCX) as archive:
        bad_member = archive.testzip()
        names = archive.namelist()
        document_xml = archive.read("word/document.xml")
        formula_result = formula_inventory(document_xml)
        xml_parts = [
            name for name in names
            if name.endswith(".xml") and (
                name == "word/document.xml"
                or re.fullmatch(r"word/(?:header|footer)\d+\.xml", name)
                or name.startswith("docProps/")
            )
        ]
        xml_roots = []
        decoded_xml = []
        for name in xml_parts:
            data = archive.read(name)
            decoded_xml.append(data.decode("utf-8", "ignore"))
            try:
                xml_roots.append((name, etree.fromstring(data)))
            except etree.XMLSyntaxError:
                pass
        package_text = "\n".join(decoded_xml)

        comments_parts = [name for name in names if "comments" in name.lower() or name.endswith("people.xml")]
        tracked_counts = {
            "insertions": sum(len(root.xpath(".//w:ins", namespaces=NS)) for _, root in xml_roots),
            "deletions": sum(len(root.xpath(".//w:del", namespaces=NS)) for _, root in xml_roots),
            "moves_from": sum(len(root.xpath(".//w:moveFrom", namespaces=NS)) for _, root in xml_roots),
            "moves_to": sum(len(root.xpath(".//w:moveTo", namespaces=NS)) for _, root in xml_roots),
        }
        hidden_run_count = sum(
            len(root.xpath(".//w:rPr/w:vanish | .//w:rPr/w:webHidden", namespaces=NS))
            for _, root in xml_roots
        )
        external_relationship_parts = []
        for name in names:
            if name.endswith(".rels") and b'TargetMode="External"' in archive.read(name):
                external_relationship_parts.append(name)
        local_path_hits = sorted(set(re.findall(
            r"(?:[A-Za-z]:\\[^<\"']+|kwaay-formal|Users\\10202)", package_text, re.I
        )))

        doc = Document(DOCX)
        core = doc.core_properties
        referenced_images = []
        for shape in doc.inline_shapes:
            embed = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
            part = doc.part.rels[embed].target_part
            name = str(part.partname)
            data = part.blob
            image = Image.open(io.BytesIO(data))
            referenced_images.append({
                "part": name,
                "format": image.format,
                "pixels": list(image.size),
                "dpi": list(image.info.get("dpi", (None, None))),
                "metadata_keys": sorted(image.info.keys()),
                "sha256": hashlib.sha256(data).hexdigest().upper(),
            })

    formula_result["checks"] = {
        "total_is_99": formula_result["total_omml_objects"] == 99,
        "six_display_formulas": formula_result["display_formula_paragraphs"] == 6,
        "three_numbered": formula_result["numbered_display_formulas"] == 3,
        "three_unnumbered": formula_result["unnumbered_display_formulas"] == 3,
        "number_sequence": [item["number"] for item in formula_result["display_formulas"] if item["number"] is not None] == [1, 2, 3],
    }
    formula_result["all_pass"] = all(formula_result["checks"].values())
    FORMULA_OUT.write_text(json.dumps(formula_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    page_comparisons = page_comparison()
    text_comparisons = pdf_text_comparison()
    result = {
        "docx": str(DOCX.relative_to(ROOT)).replace("\\", "/"),
        "docx_sha256": sha256(DOCX),
        "stage3_1_docx_sha256": sha256(STAGE3_DOCX),
        "zip_integrity": bad_member is None,
        "core_properties": {
            "title": core.title,
            "subject": core.subject,
            "author": core.author,
            "last_modified_by": core.last_modified_by,
            "comments": core.comments,
        },
        "comments_or_people_parts": comments_parts,
        "tracked_change_counts": tracked_counts,
        "hidden_run_count": hidden_run_count,
        "external_relationship_parts": external_relationship_parts,
        "local_path_hits": local_path_hits,
        "referenced_paper_images": referenced_images,
        "figure_status": "VECTOR_GRAPHICS_PENDING",
        "formula_status": "MATHTYPE_CONVERSION_BLOCKED",
        "tool_availability": {
            "MathType": shutil.which("MathType") or shutil.which("MathType.exe"),
            "Inkscape": shutil.which("inkscape"),
            "pstoedit": shutil.which("pstoedit"),
            "dvisvgm": shutil.which("dvisvgm"),
            "pdftocairo": shutil.which("pdftocairo"),
        },
        "page_comparison_with_stage3_1": page_comparisons,
        "pdf_text_comparison_with_stage3_1": text_comparisons,
        "checks": {
            "zip_integrity": bad_member is None,
            "anonymous_core_properties": core.author == "Anonymous Author(s)" and core.last_modified_by == "Anonymous Author(s)",
            "no_comments": not comments_parts,
            "no_tracked_changes": not any(tracked_counts.values()),
            "no_hidden_text": hidden_run_count == 0,
            "no_external_relationships": not external_relationship_parts,
            "no_local_paths": not local_path_hits,
            "two_referenced_png_figures": len(referenced_images) == 2 and all(item["format"] == "PNG" for item in referenced_images),
            "formula_inventory_pass": formula_result["all_pass"],
            "six_same_size_rendered_pages": len(page_comparisons) == 6 and all(item["same_dimensions"] for item in page_comparisons),
            "only_page_one_text_changed": (
                len(text_comparisons) == 6
                and not text_comparisons[0]["text_identical"]
                and all(item["text_identical"] for item in text_comparisons[1:])
            ),
        },
    }
    result["all_internal_checks_pass"] = all(result["checks"].values())
    COMPLIANCE_OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "formula_inventory": str(FORMULA_OUT),
        "compliance_audit": str(COMPLIANCE_OUT),
        "formula_checks": formula_result["checks"],
        "compliance_checks": result["checks"],
        "all_internal_checks_pass": result["all_internal_checks_pass"],
    }, ensure_ascii=False, indent=2))
    if not formula_result["all_pass"] or not result["all_internal_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
