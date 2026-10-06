# FORMULA AUDIT V2

## 状态

MATH_TYPE_CONVERSION_BLOCKED

当前 Windows 环境未发现可调用的 MathType：常见 Program Files、ProgramData、用户 AppData 路径无 MathType/Design Science/WIRIS 文件，卸载注册表、Word Add-ins 注册表、命令入口与相关进程也均无匹配项。因此未伪造 MathType OLE 对象，也未把公式转成图片。

## 保留项

- v2 保留 197 个可编辑 OMML 数学对象。
- 27 个编号行间公式及其编号保持不变。
- `source/formulas.json` 保留且未改写。
- 量词与关系符号（∀、∃、⇒、⇔、≠）、上下标、时间点和多行公式继续由 OMML 表示。

由于期刊要求 MathType 而当前环境无法执行真实转换，本稿不能标记为投稿就绪。
