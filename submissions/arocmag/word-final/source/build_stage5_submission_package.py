from __future__ import annotations

import csv
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[4]
WORD_ROOT = ROOT / "submissions" / "arocmag" / "word-final"
STAGE4_DOCX = WORD_ROOT / "K-Waay-AROCMAG-submission-stage4.docx"
FORMULA_INVENTORY = WORD_ROOT / "qa" / "stage4-formula-inventory.json"
DISPLAY_FORMULAS = WORD_ROOT / "formulas" / "formulas-stage4.json"
PACKAGE = WORD_ROOT / "stage5-submission-package"
STAGE5_DOCX = PACKAGE / "K-Waay-AROCMAG-submission-stage5-author-confirmation.docx"


def set_core_text(root: ET.Element, tag: str, value: str) -> None:
    node = root.find(tag)
    if node is None:
        node = ET.SubElement(root, tag)
    node.text = value


def copy_docx_with_stage5_metadata() -> None:
    cp = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    dc = "http://purl.org/dc/elements/1.1/"
    ET.register_namespace("cp", cp)
    ET.register_namespace("dc", dc)
    ET.register_namespace("dcterms", "http://purl.org/dc/terms/")
    ET.register_namespace("dcmitype", "http://purl.org/dc/dcmitype/")
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    with zipfile.ZipFile(STAGE4_DOCX, "r") as source, zipfile.ZipFile(
        STAGE5_DOCX, "w", zipfile.ZIP_DEFLATED
    ) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "docProps/core.xml":
                core = ET.fromstring(data)
                set_core_text(core, f"{{{dc}}}creator", "Anonymous Author(s)")
                set_core_text(core, f"{{{cp}}}lastModifiedBy", "Anonymous Author(s)")
                set_core_text(
                    core,
                    f"{{{dc}}}subject",
                    "Anonymous AROCMAG Stage 5 author-confirmation manuscript",
                )
                set_core_text(
                    core,
                    f"{{{dc}}}description",
                    "Stage 5 author-confirmation copy; scientific body preserved from Stage 4; author metadata and MathType conversion pending.",
                )
                data = ET.tostring(core, encoding="utf-8", xml_declaration=True)
            target.writestr(item, data)


def write_formula_checklist() -> None:
    inventory = json.loads(FORMULA_INVENTORY.read_text(encoding="utf-8"))
    csv_path = PACKAGE / "FORMULA_VERIFICATION_CHECKLIST.csv"
    fields = [
        "object_index",
        "kind",
        "paragraph_index",
        "display_number",
        "math_text",
        "paragraph_context",
        "mathtype_converted",
        "editable_in_mathtype",
        "symbols_verified",
        "visual_verified",
        "notes",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for item in inventory["objects"]:
            writer.writerow({
                "object_index": item["object_index"],
                "kind": item["kind"],
                "paragraph_index": item["paragraph_index"],
                "display_number": item["display_number"] if item["display_number"] is not None else "",
                "math_text": item["math_text"],
                "paragraph_context": re.sub(r"\s+", " ", item["paragraph_context"]).strip(),
                "mathtype_converted": "[ ]",
                "editable_in_mathtype": "[ ]",
                "symbols_verified": "[ ]",
                "visual_verified": "[ ]",
                "notes": "",
            })

    display_records = json.loads(DISPLAY_FORMULAS.read_text(encoding="utf-8"))
    blocks = []
    for index, record in enumerate(display_records, 1):
        label = f"式({record['number']})" if record["number"] is not None else "未编号展示公式"
        blocks.append(
            f"### {index}. {label} — `{record['source']}`\n\n"
            f"```latex\n{record['latex']}\n```\n\n"
            "- [ ] 已转换为真正的 MathType 对象\n"
            "- [ ] 双击后由 MathType 打开并可编辑\n"
            "- [ ] 与 LaTeX 源逐字符核对\n"
            "- [ ] 编号、居中、字号和行距正确\n"
            "- [ ] Word 导出 PDF 后无裁切或符号替换\n"
        )
    guide = f"""# Stage 5 公式核对指南

## 当前真实状态

- 当前稿件含 99 个可编辑 OMML 数学对象：86 个行内对象、13 个展示公式成员。
- 展示公式段落共 6 项，其中编号公式 3 项、未编号公式 3 项。
- 当前环境未检测到真正的 MathType 转换链，因此状态保持为 `MATHTYPE_CONVERSION_BLOCKED`。
- `FORMULA_VERIFICATION_CHECKLIST.csv` 已逐项列出 99 个对象，并预留转换、可编辑性、符号和视觉核对栏。

## Microsoft Word + MathType 6.9d 人工转换流程

1. 将整个 `stage5-submission-package` 复制到不受 Git 跟踪的私有目录，在副本上操作。
2. 使用 Microsoft Word 打开 Stage 5 Word，先确认 MathType 6.9d 选项卡和 `Convert Equations` 命令真实可用。
3. 另存为带 `-mathtype-private` 后缀的新文件，不覆盖本包中的 OMML 基线。
4. 打开 **MathType → Convert Equations**：来源勾选 `Word 2007 and later (OMML) equations`，`Range` 选 `Whole document`，目标选 `MathType equations (OLE objects)`。
5. 转换完成对话框必须报告 99 项。保存、关闭并重新打开副本后，剩余 OMML 应为 0，MathType OLE/embedding 对象应为 99；任一数量不符都保持阻塞。
6. 依 `FORMULA_VERIFICATION_CHECKLIST.csv` 的 1—99 顺序核对；每个对象必须能够双击进入 MathType 编辑器，不能只凭外观判断。
7. 重点检查 `⇏`、`⇒`、`⇔`、`≜`、`≠`、`≤`、`≥`、`∧`、`…`、`τ`、Unicode 上下标、$P_\\tau$、$M_\\tau$、$I_\\tau$、`ReceiverAccept`、`DistinctPartyPerBatch` 和时间关系；当前 99 个 OMML 中没有 `∃`。
8. 重点逐行核对含 4 个对象的段落 133 和含 5 个对象的段落 142（式(3)），确认换行、正体算子和 Unicode 下标没有漂移；再核对其余 4 个展示公式及 (1)—(3) 编号。
9. 更新域并重新分页，用 Microsoft Word 导出 PDF；逐页检查六页，特别检查首页、式(1)—(3)、表4和末页参考文献。
10. 只有全部 99 行的四个核对栏均已勾选，且最终 PDF 通过视觉检查，才可将状态改为 MathType 已完成。

## 六项展示公式

{''.join(blocks)}
## 禁止做法

- 不得把公式转成图片并称为 MathType。
- 不得把 OMML、OLE 占位或扩展名修改称为 MathType 转换完成。
- 不得只检查 6 个展示公式而忽略 86 个行内对象。
- 不得在未完成双击编辑验证和 PDF 复核时标记转换完成。
"""
    (PACKAGE / "FORMULA_VERIFICATION_GUIDE.md").write_text(guide, encoding="utf-8")


def write_author_form() -> None:
    text = """# 作者信息私下收集表（未填写模板）

> **隐私要求：不要直接填写并提交本仓库中的此文件。** 请先复制到不受 Git 跟踪的私有目录，再填写真实姓名、手机号、私人邮箱、身份证明或其他敏感信息。填妥副本不得提交到公开 GitHub 仓库。

## A. 稿件与投稿类型

- 稿件中文题名：K-Waay批次准入中参与方互异条件的形式化分析
- 稿件英文题名：Formal Analysis of the Distinct-Party Condition in K-Waay Batch Admission
- 投稿栏目/专题：`[私下填写]`
- 月刊或其他类型：`[私下填写]`
- 投稿系统是否要求实名稿、匿名稿或两套文件：`[登录系统后确认]`
- 负责投稿的作者：`[私下填写]`

## B. 作者顺序与身份

请为每位作者复制一份下列字段，并确保所有作者书面确认顺序和单位：

- 作者序号：`[ ]`
- 中文姓名：`[私下填写]`
- 英文姓名及拼写：`[私下填写]`
- 所属单位编号：`[私下填写]`
- 是否第一作者：`[是/否]`
- 是否通信作者：`[是/否]`
- CCF会员身份及会员号（如适用）：`[私下填写]`
- ORCID（如需）：`[私下填写]`

## C. 作者单位

- 中文单位全称：`[私下填写]`
- 英文单位全称：`[私下填写]`
- 院系/实验室：`[私下填写]`
- 城市：`[私下填写]`
- 邮政编码：`[私下填写]`
- 国家/地区：`[私下填写]`
- 单位排序与作者映射：`[私下填写]`

## D. 联系方式（敏感信息）

- 通信作者常用邮箱：`[仅在私下副本填写]`
- 联系手机号：`[仅在投稿系统或私下副本填写]`
- 备用邮箱/电话（若系统要求）：`[仅在私下副本填写]`
- 通信地址：`[仅在私下副本填写]`

## E. 基金与作者简介

- 基金中文名称：`[私下填写；没有则明确写“无”]`
- 基金项目编号：`[私下填写]`
- 基金英文名称：`[私下填写]`
- 作者简介字段是否为初投必填：`[投稿系统确认]`
- 作者简介：`[若必填，在私下副本填写]`

## F. 首页和分类元数据

- 中图分类号：`[依据官网TP类表，由作者确认]`
- 文献标志码：当前官方模板未显示为作者必填；仅在投稿系统或编辑部明确要求时填写，不自行编造。
- 文章编号：当前官方模板未显示为作者必填；仅在投稿系统或编辑部明确要求时填写，不自行编造。
- 关键词中英文是否最终确认：`[是/否]`
- 匿名稿中是否需删除基金、致谢和可识别链接：`[投稿系统确认]`

## G. 作者共同确认

- [ ] 全体作者同意题名、署名顺序和单位顺序。
- [ ] 全体作者审阅并同意投稿版本。
- [ ] 稿件不存在一稿多投、抄袭、数据或证据伪造。
- [ ] 引用和复核材料不泄露不应公开的个人信息。
- [ ] 填写后的私密副本未进入公开 Git 仓库。
- [ ] 最终点击“提交”由获授权的作者本人完成。
"""
    (PACKAGE / "AUTHOR_INFORMATION_COLLECTION_FORM.md").write_text(text, encoding="utf-8")


def write_compliance_report() -> None:
    text = """# Stage 5 投稿规范检查报告

## 当前官方依据

- 投稿模板：https://www.arocmag.cn/info/instruction/template
- 摘要要求：https://www.arocmag.cn/info/instruction/abstract-instruction
- 投稿须知：https://www.arocmag.cn/info/instruction/instructions
- TP类中图分类号：https://www.arocmag.cn/info/instruction/clc

核对日期：2026-10-10。官网公开页面要求通过投稿系统提交，并优先使用 doc/docx；公式使用 MathType，图表尽可能使用矢量图。公开页面未明确说明初投稿件是否匿名或双盲，因此必须在登录后的实际投稿表单中确认。

## 已通过

- Stage 5 Word 的正文、页眉页脚、样式、表格、图片和公式部件均从已审查的 Stage 4 保留。
- Word 保持 99 个可编辑 OMML 对象、6 个展示公式、4 张表、2 幅图和 8 条参考文献。
- 两图继续使用经过实际渲染核验的 360 dpi PNG；官网矢量图措辞为“尽可能”，未升级为绝对阻塞。
- 文件核心作者属性保持 `Anonymous Author(s)`；无批注、修订记录、隐藏文本、外部关系和本地路径。
- 未加入任何真实姓名、手机号、私人邮箱或其他个人敏感信息。
- 科学内容仍为 Stage 4 冻结版本；未修改 RQ、模型、lemma、14项结果或适用边界。

## 当前阻塞

- `MATHTYPE_CONVERSION_BLOCKED`：本机没有 Microsoft Word 桌面版和真正的 MathType 软件；WPS 不能替代这项验收。
- 真实作者、单位、基金、通信作者和联系方式尚未提供。
- 匿名/实名文件要求需在投稿系统中确认。
- 最终稿尚未在目标 Microsoft Word 版本和投稿系统生成的 PDF 中复核。

## 当前状态

`SUBMISSION_PACKAGE_PREPARED_WITH_BLOCKERS`
"""
    (PACKAGE / "SUBMISSION_COMPLIANCE_REPORT.md").write_text(text, encoding="utf-8")


def write_system_checklist() -> None:
    text = """# 《计算机应用研究》投稿系统操作检查表

## 1. 登录前

- [ ] 在私有目录完成作者信息收集，未把填妥表格提交到公开仓库。
- [ ] 确认由哪位作者负责投稿，并获得全体作者授权。
- [ ] 准备最终实名稿或匿名稿；不要同时混用两套元数据。
- [ ] 确认 MathType 是否必须在初投文件中完成。
- [ ] 使用 Microsoft Word 打开最终副本、更新域、重新分页并导出 PDF。

## 2. 登录后先确认规则

- [ ] 截图或记录系统对匿名/实名文件的明确说明。
- [ ] 确认系统接受 `.docx`，以及是否另需 PDF。
- [ ] 确认作者简介、基金、中图分类号、通信作者和手机号是否为必填。
- [ ] 确认是否需要删除匿名稿中的基金、单位、自引线索或复核材料链接。
- [ ] 确认图形格式和 MathType 是否存在上传端硬性检测。

## 3. 录入元数据

- [ ] 中英文题名与 Word 完全一致。
- [ ] 中英文摘要与 Word 完全一致；中文 212 个汉字，英文 139 words。
- [ ] 中英文关键词与 Word 完全一致。
- [ ] 作者中英文姓名、顺序和单位映射经全体作者确认。
- [ ] 第一作者、通信作者、邮箱和手机号正确。
- [ ] 基金名称和编号与证明材料一致；无基金时按系统规则填写。
- [ ] 中图分类号依据官网 TP 类表确认，未猜测文章编号或编辑字段。
- [ ] CCF会员身份和会员号仅在真实适用时填写。

## 4. 上传文件

- [ ] 上传的是私有最终副本，不是带未处理占位的公开基线。
- [ ] 匿名稿核心属性、正文、页眉页脚、图片元数据和文件名均无身份信息。
- [ ] 实名稿作者、单位、基金、简介和通信信息与系统字段一致。
- [ ] 公式均可编辑；若要求 MathType，99 个对象已完成逐项核对。
- [ ] 图1和图2清晰，中文、公式、箭头、虚线和框线无损。

## 5. 投稿系统生成预览

- [ ] 总页数、纸张、页边距、单双栏和末页顺序正确。
- [ ] 首页题名、作者、摘要、关键词和分类字段完整。
- [ ] 式(1)—(3)及3个未编号展示公式无缺符、错位或裁切。
- [ ] 4张表、2幅图及图表题完整。
- [ ] 8条参考文献和正文引用顺序正确。
- [ ] 第4页中文字距、第5页长lemma换行、末页参考文献排版没有回退。
- [ ] 下载系统生成 PDF，与本地 Microsoft Word PDF 逐页对照。

## 6. 最终提交

- [ ] 全体作者完成最后确认。
- [ ] 投稿作者本人检查声明、版权和保密选项。
- [ ] 人工点击最终提交；本项目脚本不会自动提交。
- [ ] 保存稿件编号、提交时间、回执邮件和最终上传文件的哈希。
"""
    (PACKAGE / "SUBMISSION_SYSTEM_OPERATION_CHECKLIST.md").write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# Stage 5 最终投稿准备包

本目录用于作者最终确认，不表示论文已投稿，也不表示全部投稿条件已经满足。

## 文件

- `K-Waay-AROCMAG-submission-stage5-author-confirmation.docx`：待作者确认的匿名占位 Word；科学正文来自冻结 Stage 4。
- `K-Waay-AROCMAG-submission-stage5-preview.pdf`：WPS 实际打开上述 Word 后导出的页面预览。
- `FORMULA_VERIFICATION_CHECKLIST.csv`：99 个 OMML 对象的逐项人工核对表。
- `FORMULA_VERIFICATION_GUIDE.md`：Microsoft Word + MathType 操作与六项展示公式对照。
- `AUTHOR_INFORMATION_COLLECTION_FORM.md`：不含真实个人信息的私下收集模板；填写后的副本不得提交公开仓库。
- `SUBMISSION_COMPLIANCE_REPORT.md`：本包规范状态和阻塞项。
- `SUBMISSION_SYSTEM_OPERATION_CHECKLIST.md`：登录投稿系统后的人工操作和最终预览清单。
- `PACKAGE_MANIFEST.json`：文件哈希、结构核验和最终状态。

## 使用顺序

1. 阅读规范报告和阻塞项。
2. 在私有目录填写作者信息表。
3. 登录投稿系统确认实名/匿名、MathType和图形要求。
4. 如需 MathType，在私有 Word 副本中转换并完成99项核对。
5. 补齐真实元数据，使用 Microsoft Word 导出并逐页检查。
6. 依投稿系统检查表人工录入、上传、预览和提交。

当前状态：`SUBMISSION_PACKAGE_PREPARED_WITH_BLOCKERS`
"""
    (PACKAGE / "PACKAGE_README.md").write_text(text, encoding="utf-8")


def main() -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    copy_docx_with_stage5_metadata()
    write_formula_checklist()
    write_author_form()
    write_compliance_report()
    write_system_checklist()
    write_readme()
    print(json.dumps({
        "package": str(PACKAGE),
        "docx": str(STAGE5_DOCX),
        "formula_objects": 99,
        "status": "SUBMISSION_PACKAGE_PREPARED_WITH_BLOCKERS",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
