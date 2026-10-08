# Reference format audit

## Official requirement

已实际检查官方模板。模板第12节明确写明参考文献著录参考GB/T 7714—2005，并使用按正文首次出现顺序连续编码的方括号编号。

当前Word稿已保持LaTeX正文的首次引用顺序，共8条：

1. `cremers2023session`
2. `collins2024kwaay`
3. `collins2024kwaayfull`
4. `cohngordon2020signal`
5. `bhargavan2024pqxdh`
6. `meier2013tamarin`
7. `lupetti2006names`
8. `lowe1997hierarchy`

正文引用`[1]`–`[8]`与文末条目一一对应。

## Frozen BibTeX metadata inventory

| 编号 | 键 | 作者 | 题名 | 期刊/会议/机构 | 年 | 卷 | 期 | 页码 | DOI | URL | 状态 |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `cremers2023session` | 有 | 有 | 32nd USENIX Security Symposium | 2023 | — | — | 1235–1252 | — | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |
| 2 | `collins2024kwaay` | 有 | 有 | 33rd USENIX Security Symposium | 2024 | — | — | 433–450 | — | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |
| 3 | `collins2024kwaayfull` | 有 | 有 | Cryptology ePrint Archive, Paper 2024/120 | 2024 | — | — | 不适用 | — | 有 | 在线资源字段待按期刊口径最终规范化 |
| 4 | `cohngordon2020signal` | 有 | 有 | Journal of Cryptology | 2020 | 33 | — | 1914–1983 | 10.1007/s00145-020-09360-1 | 有 | 基本字段完整，期号需按权威元数据最终复核 |
| 5 | `bhargavan2024pqxdh` | 有 | 有 | 33rd USENIX Security Symposium | 2024 | — | — | 469–486 | — | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |
| 6 | `meier2013tamarin` | 有 | 有 | CAV 2013; LNCS 8044 | 2013 | — | — | 696–701 | 10.1007/978-3-642-39799-8_48 | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |
| 7 | `lupetti2006names` | 有 | 有 | WOSIS 2006 | 2006 | — | — | 185–194 | — | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |
| 8 | `lowe1997hierarchy` | 有 | 有 | 10th IEEE Computer Security Foundations Workshop | 1997 | — | — | 31–43 | 10.1109/CSFW.1997.596782 | 有 | `SOURCE_METADATA_PENDING`：出版地/出版者未写入BibTeX |

## Stage 1 format

- 正文已采用顺序编码制。
- 文末条目使用官方参考文献段落样式、7.5 pt、悬挂缩进。
- 当前条目由冻结BibTeX字段转换，未编造缺失的出版地、出版者、期号或DOI。
- 当前格式用于Word迁移和引用闭合检查，不声明已经完成最终GB/T 7714—2005编辑规范化。

## Follow-up

投稿前需要：

1. 按期刊当前编辑规则统一作者姓/名缩写、大小写、文献类型标识、出版地和出版者；
2. 用权威来源复核缺失字段；
3. 明确在线资源访问日期；
4. 检查GB/T 7714—2005与编辑部当前实际执行口径是否存在差异；
5. 最终复核正文引用与文末条目仍保持1:1对应。

状态：`GBT_REFERENCE_FORMAT_FINALIZATION_PENDING`

