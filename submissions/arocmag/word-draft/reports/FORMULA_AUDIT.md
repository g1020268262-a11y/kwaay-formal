# 公式审计

- 行间公式块：27 个，已编号为（1）—（27）。
- 行内公式源片段：153 个。
- 写入格式：Office Math Markup Language（OMML），可在 Word/WPS 中编辑。
- 最终 OOXML 审计：`word/document.xml` 中共有 197 个 `m:oMath` 元素；WPS COM 复核结果同为 197 个 OMath。
- 原始 LaTeX：`source/formulas.json`。
- MathType 状态：当前环境未发现可自动批量转换并复核的 MathType 接口，尚未完成 MathType 对象转换。
- 交付判定影响：按照任务约束，最终状态必须为 `AROCMAG_WORD_DRAFT_INCOMPLETE`。

可编辑性审计采用 OOXML 中的 `m:oMath` 元素计数，并在最终 WPS 打开后复核 OMath 数量。最终 PDF 的公式（1）—（27）均完成逐页目视检查，没有越界或截断。OMML 中的数学内容使用期刊可读的 Unicode 数学符号；复杂多行式保持可编辑，但后续如获得 MathType 环境，仍需逐式转换和复核。
