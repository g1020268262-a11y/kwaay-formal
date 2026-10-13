"""One-time, scope-checked migration of approved chapters into the Word working copy.

Uses the retained Stage 6 package, not a blank document. All unchanged package
parts and all body blocks outside chapters 1/2 are preserved. Run with the Codex
bundled Python and a temporary dependency directory containing latex2mathml
3.81.1 and mathml2omml 0.0.2. The explicit working hash prevents overwriting an
uninspected revision. This is not a whole-manuscript regeneration command.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "submissions/arocmag/word-final"
BASE = OUT / "K-Waay-AROCMAG-submission-stage6.docx"
WORK = OUT / "K-Waay-AROCMAG-submission-working.docx"
TEX = ROOT / "submissions/arocmag/latex-v2/sections"
QA = OUT / "qa/working-chapters12"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}
XML = "http://www.w3.org/XML/1998/namespace"
BASE_SHA = "2c07651db11cb41cd5f44a624db1777875adadeebe01b4808d6b45015054390f"
SOURCES = ["02-problem.tex", "03-formal-modeling.tex"]
TITLES = ["K-Waay协议及安全问题", "形式化建模与安全性质"]
STATUS = "部分更新工作稿：第1、2章已更新；后续章节尚待衔接；非最终可投稿版本。"
REFS = {
    "eq:core-transcript": "1", "eq:batch-vector": "2", "eq:party-distinct": "3",
    "eq:core-events": "4", "eq:tamarin-accept": "5", "eq:property-p1": "6",
    "eq:property-p2": "7", "tab:security-goal-map": "1",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def q(prefix: str, name: str) -> str:
    return "{" + NS[prefix] + "}" + name


def text(el) -> str:
    return "".join(el.xpath(".//w:t/text()|.//m:t/text()", namespaces=NS))


def canonical(el) -> bytes:
    return etree.tostring(el, method="c14n")


def child(parent, prefix, name, value=None):
    el = etree.SubElement(parent, q(prefix, name))
    if value is not None:
        el.set(q(prefix, "val"), str(value))
    return el


def group(src: str, start: int):
    if src[start] != "{":
        raise ValueError("Expected a LaTeX brace group")
    depth = 1
    end = start + 1
    while end < len(src) and depth:
        depth += (src[end] == "{") - (src[end] == "}")
        end += 1
    if depth:
        raise ValueError("Unbalanced LaTeX braces")
    return src[start + 1:end - 1], end


class Migration:
    def __init__(self, package, math_deps):
        sys.path.insert(0, str(math_deps))
        from latex2mathml.converter import convert as to_mathml
        from mathml2omml import convert as to_omml
        self.to_mathml, self.to_omml = to_mathml, to_omml
        self.package = package
        self.root = etree.fromstring(package["word/document.xml"])
        self.body = self.root.find("w:body", NS)
        self.original = list(self.body)
        self.start = self.find_heading("K-Waay批次准入与参与方互异问题")
        self.end = self.find_heading("形式化验证与结果分析")
        self.h1 = self.original[self.start]
        self.h2 = self.original[self.start + 1]
        self.prose = self.original[self.start + 2]
        self.display = next(b for b in self.original[self.start:self.end]
                            if b.xpath("./w:pPr/w:pStyle[@w:val='74']", namespaces=NS))
        self.caption = next(b for b in self.original[self.start:self.end]
                            if text(b).startswith("表 1"))
        self.table_base = next(b for b in self.original[self.start:self.end]
                               if b.tag == q("w", "tbl") and
                               len(b.find("w:tr", NS).findall("w:tc", NS)) == 4)
        self.close_two = next(b for b in self.original[self.start:self.end]
                              if b.xpath("./w:pPr/w:sectPr/w:cols[@w:num='2']", namespaces=NS))
        self.close_one = next(b for b in self.original[self.start:self.end]
                              if b.xpath("./w:pPr/w:sectPr/w:cols[@w:num='1']", namespaces=NS))
        self.cites = {x["key"]: str(x["number"]) for x in
                      json.loads((OUT / "source/citation-order-stage6.json").read_text("utf-8"))}
        self.math_records = []
        self.blocks = []
        self.source_records = []
        self.table_rows = []

    def find_heading(self, title):
        matches = [i for i, b in enumerate(self.body)
                   if text(b) == title and b.xpath("./w:pPr/w:pStyle[@w:val='65']", namespaces=NS)]
        if len(matches) != 1:
            raise ValueError("Ambiguous heading: " + title)
        return matches[0]

    def blank(self, template):
        el = copy.deepcopy(template)
        for c in list(el):
            if c.tag != q("w", "pPr"):
                el.remove(c)
        return el

    def run(self, p, value, template=None, italic=False, size=None):
        if not value:
            return
        r = child(p, "w", "r")
        tr = (template if template is not None else self.prose).find("w:r/w:rPr", NS)
        if tr is not None:
            r.append(copy.deepcopy(tr))
        rp = r.find("w:rPr", NS)
        if rp is None:
            rp = etree.Element(q("w", "rPr")); r.insert(0, rp)
        if italic:
            old = rp.find("w:i", NS)
            if old is None:
                child(rp, "w", "i")
            else:
                old.set(q("w", "val"), "1")
        if size is not None:
            old = rp.find("w:sz", NS)
            if old is None:
                child(rp, "w", "sz", int(size * 2))
            else:
                old.set(q("w", "val"), str(int(size * 2)))
        t = child(r, "w", "t")
        t.set("{" + XML + "}space", "preserve")
        t.text = value

    def math(self, latex: str, display=False):
        clean = latex.strip()
        mml = self.to_mathml(clean, display="block" if display else "inline")
        raw = self.to_omml(mml)
        holder = etree.fromstring((f'<root xmlns:m="{M}" xmlns:w="{W}">' + raw + '</root>').encode())
        om = holder[0]
        for r in om.xpath(".//m:r", namespaces=NS):
            wrp = r.find("w:rPr", NS)
            if wrp is None:
                wrp = etree.Element(q("w", "rPr"))
                insert = 1 if len(r) and r[0].tag == q("m", "rPr") else 0
                r.insert(insert, wrp)
            fonts = etree.SubElement(wrp, q("w", "rFonts"))
            fonts.set(q("w", "ascii"), "Cambria Math")
            fonts.set(q("w", "hAnsi"), "Cambria Math")
            fonts.set(q("w", "eastAsia"), "宋体")
            child(wrp, "w", "sz", 18)
            child(wrp, "w", "color", "000000")
        self.math_records.append({"latex": clean, "display": display,
                                  "omml_text": "".join(om.xpath(".//m:t/text()", namespaces=NS)),
                                  "structured_scripts": len(om.xpath(".//m:sSub|.//m:sSup|.//m:sSubSup", namespaces=NS))})
        return om

    def inline(self, p, src, italic=False, template=None, size=None):
        pos = 0
        plain = []

        def flush():
            if plain:
                self.run(p, "".join(plain), template=template, italic=italic, size=size)
                plain.clear()

        macros = {"kwaay": "K-Waay", "batchreceive": "BatchReceive"}
        while pos < len(src):
            c = src[pos]
            if c == "$":
                flush()
                end = src.find("$", pos + 1)
                if end < 0:
                    raise ValueError("Unbalanced inline math")
                p.append(self.math(src[pos + 1:end])); pos = end + 1
            elif c == "\\":
                match = re.match(r"\\([A-Za-z]+)", src[pos:])
                if not match:
                    plain.append(src[pos + 1]); pos += 2; continue
                cmd = match[1]; end = pos + len(match[0])
                if cmd in macros:
                    plain.append(macros[cmd]); pos = end
                elif cmd in ("cite", "eqref", "ref", "emph", "texttt", "textsf", "textbf"):
                    value, end = group(src, end)
                    if cmd == "cite":
                        plain.append("[" + ",".join(self.cites[x.strip()] for x in value.split(",")) + "]")
                    elif cmd in ("ref", "eqref"):
                        result = REFS[value]
                        plain.append("(" + result + ")" if cmd == "eqref" else result)
                    else:
                        flush(); self.inline(p, value, italic=italic or cmd == "emph", template=template, size=size)
                    pos = end
                else:
                    raise ValueError("Unsupported prose command: " + cmd)
            elif c == "~":
                plain.append(" "); pos += 1
            else:
                plain.append(c); pos += 1
        flush()

    def paragraph(self, src, template=None):
        p = self.blank(template if template is not None else self.prose)
        self.inline(p, src, template=template)
        return p

    def equation(self, raw, label):
        clean = re.sub(r"\\label\{[^}]+\}", "", raw).strip()
        clean = clean.replace(r"\begin{aligned}", "").replace(r"\end{aligned}", "").replace("&", "")
        lines = [x.strip() for x in clean.split(r"\\") if x.strip()]
        # Only layout line breaks are added to long expressions; all tokens
        # and their order remain identical to the approved equation.
        if label == "eq:core-transcript":
            sidline = lines[1]
            split = sidline.index("prekey_A")
            lines[1:2] = [sidline[:split], sidline[split:]]
        elif label == "eq:party-distinct":
            cut = clean.index(r"\forall")
            lines = [clean[:cut].strip(), clean[cut:].strip()]
        elif label == "eq:core-events":
            lines = [x.strip() for x in clean.split(r"\qquad")]
        elif label == "eq:property-p1":
            cut = clean.index(r"\exists")
            lines = [clean[:cut].strip(), clean[cut:].strip()]
        elif label == "eq:property-p2":
            cut = clean.index(r"\Longrightarrow")
            lines = [clean[:cut].strip(), clean[cut:].strip()]
        p = self.blank(self.display)
        for i, line in enumerate(lines):
            if i:
                child(child(p, "w", "r"), "w", "br")
            p.append(self.math(line, display=True))
        nr = child(p, "w", "r")
        base_rpr = self.display.find("w:r/w:rPr", NS)
        if base_rpr is not None:
            nr.append(copy.deepcopy(base_rpr))
        child(nr, "w", "tab")
        t = child(nr, "w", "t"); t.text = "(" + REFS[label] + ")"
        self.source_records.append({"kind": "equation", "label": label, "number": REFS[label],
                                    "source_latex": clean, "layout_lines": lines})
        return p

    def table(self, rows):
        if len(rows) != 7 or any(len(row) != 4 for row in rows):
            raise ValueError("Table 1 must contain one header and six four-column rows")
        tbl = copy.deepcopy(self.table_base)
        prototypes = tbl.findall("w:tr", NS)
        header, middle, last = prototypes[0], prototypes[1], prototypes[-1]
        for row in prototypes:
            tbl.remove(row)
        widths = [1077, 3288, 1304, 3288]  # 1.9 / 5.8 / 2.3 / 5.8 cm; baseline total 15.8 cm.
        grid = tbl.find("w:tblGrid", NS)
        for c, width in zip(grid, widths):
            c.set(q("w", "w"), str(width))
        for i, values in enumerate(rows):
            row = copy.deepcopy(header if i == 0 else last if i == len(rows) - 1 else middle)
            for j, (cell, value) in enumerate(zip(row.findall("w:tc", NS), values)):
                cell.find("w:tcPr/w:tcW", NS).set(q("w", "w"), str(widths[j]))
                pp = cell.find("w:p", NS)
                p = self.blank(pp)
                # Clone the baseline cell run formatting (7.5 pt), not the body run.
                self.inline(p, value, template=pp)
                for old in list(cell):
                    if old.tag != q("w", "tcPr"):
                        cell.remove(old)
                cell.append(p)
            tbl.append(row)
        self.table_rows = rows
        return tbl

    def consume(self, src, title):
        src = "\n".join(line for line in src.splitlines() if not line.lstrip().startswith("%"))
        lines = src.splitlines(); i = 0; paragraph = []
        self.blocks.append(self.paragraph(title, self.h1))

        def flush():
            if paragraph:
                value = " ".join(x.strip() for x in paragraph).strip()
                self.blocks.append(self.paragraph(value))
                self.source_records.append({"kind": "paragraph", "source": value})
                paragraph.clear()

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                flush(); i += 1; continue
            if line.startswith(r"\label{"):
                i += 1; continue
            if line.startswith(r"\subsection{"):
                flush(); value, _ = group(line, len(r"\subsection"))
                self.blocks.append(self.paragraph(value, self.h2)); i += 1; continue
            if line == r"\begin{equation}":
                flush(); end = i + 1
                while lines[end].strip() != r"\end{equation}":
                    end += 1
                raw = "\n".join(lines[i + 1:end])
                label = re.search(r"\\label\{([^}]+)\}", raw)[1]
                self.blocks.append(self.equation(raw, label)); i = end + 1; continue
            if line == r"\begin{center}":
                flush(); end = i + 1
                while lines[end].strip() != r"\end{center}":
                    end += 1
                raw = "\n".join(lines[i + 1:end])
                caption = re.search(r"\\captionof\{table\}\{([^}]+)\}", raw)[1]
                data = raw.split(r"\toprule", 1)[1].split(r"\bottomrule", 1)[0]
                data = data.replace(r"\midrule", "").strip()
                rows = [[c.strip() for c in row.split("&")] for row in data.split(r"\\") if row.strip()]
                self.blocks.extend([copy.deepcopy(self.close_two),
                                    self.paragraph("表 1　" + caption, self.caption),
                                    self.table(rows), copy.deepcopy(self.close_one)])
                i = end + 1; continue
            if line.startswith(r"\begin{") or line.startswith(r"\end{"):
                raise ValueError("Unsupported environment in approved chapter: " + line)
            paragraph.append(line); i += 1
        flush()
        # Chinese-character coverage is an independent check of the mechanical prose
        # conversion; numerical citations and structured math are audited separately.
        expected_zh = "".join(re.findall(r"[\u4e00-\u9fff]", src))
        return expected_zh

    def build(self, sources):
        for source, title in zip(sources, TITLES):
            begin = len(self.blocks)
            expected = self.consume(source, title)
            coverage_text = "".join(re.sub(r"^表\s*1\s*", "", text(b))
                                    if b.xpath("./w:pPr/w:pStyle[@w:val='77']", namespaces=NS) else text(b)
                                    for b in self.blocks[begin + 1:])
            actual = "".join(re.findall(r"[\u4e00-\u9fff]", coverage_text))
            if expected != actual:
                raise AssertionError("Approved Chinese prose/table coverage mismatch")
        prefix = self.original[:self.start]; suffix = self.original[self.end:]
        for b in self.original[self.start:self.end]:
            self.body.remove(b)
        for offset, b in enumerate(self.blocks):
            self.body.insert(self.start + offset, b)
        # A visible status line is editorial metadata, not added academic prose.
        status = self.paragraph(STATUS, self.caption)
        rp = status.find("w:pPr", NS)
        spacing = rp.find("w:spacing", NS)
        if spacing is None:
            spacing = etree.SubElement(rp, q("w", "spacing"))
        spacing.set(q("w", "before"), "0"); spacing.set(q("w", "after"), "20")
        self.body.insert(1, status)
        after = list(self.body)
        if [canonical(b) for b in prefix] != [canonical(b) for b in after[:1] + after[2:self.start + 1]]:
            raise AssertionError("Front matter/introduction changed relative to Stage 6")
        if [canonical(b) for b in suffix] != [canonical(b) for b in after[self.start + 1 + len(self.blocks):]]:
            raise AssertionError("Chapter 3 onwards changed relative to Stage 6")
        core = etree.fromstring(self.package["docProps/core.xml"])
        for e in core:
            if etree.QName(e).localname == "subject":
                e.text = "AROCMAG partial working manuscript, approved chapters 1 and 2 updated"
            if etree.QName(e).localname == "description":
                e.text = "Partial update only; subsequent chapters require alignment. Native editable OMML, not MathType OLE. Not submission-ready."
        result = dict(self.package)
        result["word/document.xml"] = etree.tostring(self.root, xml_declaration=True, encoding="UTF-8", standalone=True)
        result["docProps/core.xml"] = etree.tostring(core, xml_declaration=True, encoding="UTF-8", standalone=True)
        unchanged = [k for k in self.package if k not in ("word/document.xml", "docProps/core.xml")]
        if any(result[k] != self.package[k] for k in unchanged):
            raise AssertionError("Preserve-only package part changed")
        return result, {
            "front_matter_and_introduction_blocks_preserved": len(prefix),
            "chapter3_onwards_blocks_preserved": len(suffix),
            "chapter3_onwards_c14n_sha256": sha(b"".join(canonical(b) for b in suffix)),
            "unchanged_package_parts": unchanged,
            "changed_package_parts": ["word/document.xml", "docProps/core.xml"],
            "tables": len(self.root.xpath(".//w:tbl", namespaces=NS)),
            "omml": len(self.root.xpath(".//m:oMath", namespaces=NS)),
            "new_omml": len(self.math_records),
            "new_structured_script_objects": sum(x["structured_scripts"] for x in self.math_records),
            "sections": len(self.root.xpath(".//w:sectPr", namespaces=NS)),
            "new_table_rows": self.table_rows,
            "new_equations": [x for x in self.source_records if x["kind"] == "equation"],
            "math_format": "native editable OMML, NOT MathType OLE",
            "status": STATUS,
            "prose_coverage": "Chinese characters in both approved sources match converted chapter blocks exactly",
        }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--math-deps", type=Path, required=True)
    ap.add_argument("--expected-working-sha", required=True)
    args = ap.parse_args()
    if sha(BASE.read_bytes()) != BASE_SHA:
        raise RuntimeError("Retained Stage 6 reference differs from the inspected baseline")
    before = sha(WORK.read_bytes())
    if before != args.expected_working_sha.lower():
        raise RuntimeError("Working DOCX differs from the explicitly inspected revision; refusing overwrite")
    with zipfile.ZipFile(BASE) as z:
        package = {n: z.read(n) for n in z.namelist()}
    sources = [(TEX / p).read_text("utf-8") for p in SOURCES]
    migration = Migration(package, args.math_deps)
    result, manifest = migration.build(sources)
    tmp = WORK.with_name(WORK.stem + ".candidate.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in result.items():
            z.writestr(n, data)
    with zipfile.ZipFile(tmp) as z:
        if z.testzip() is not None:
            raise AssertionError("DOCX ZIP integrity failed")
        for n in manifest["unchanged_package_parts"]:
            if z.read(n) != package[n]:
                raise AssertionError("Serialized package-part preservation failed: " + n)
    tmp.replace(WORK)
    QA.mkdir(parents=True, exist_ok=True)
    manifest.update({"baseline_stage6_sha256": BASE_SHA,
                     "previous_working_sha256": before,
                     "working_sha256": sha(WORK.read_bytes()),
                     "sources": {n: sha((TEX / n).read_bytes()) for n in SOURCES},
                     "dependencies": {"latex2mathml": "3.81.1", "mathml2omml": "0.0.2"}})
    (QA / "build-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8")
    (QA / "formula-conversion.json").write_text(json.dumps(migration.math_records, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
