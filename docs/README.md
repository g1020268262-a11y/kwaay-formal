# Docs Index

这个目录记录 K-Waay 形式化分析相关文档。

当前文档按阶段和工具分开：

```text
docs/proverif/
docs/tamarin/
docs/cryptoverif/
docs/roadmap/
```

## ProVerif

`docs/proverif/` 记录已经完成的 K-Waay Figure 7 core ProVerif symbolic analysis。

核心入口：

- `proverif/current-stage-report.md`: ProVerif 阶段最终汇报稿。
- `proverif/formal-decision-memo.md`: ProVerif 阶段 query 分类、建模边界和工具分工。
- `proverif/paper-definition-alignment.md`: K-Waay 论文定义与 ProVerif query 的对齐说明。
- `proverif/proverif-file-inventory.md`: `proverif/` 目录下 `.pv` 文件用途清单。
- `proverif/protocol-map.md`: K-Waay Figure 7 core 对象地图。
- `proverif/threat-model.md`: 当前 public-channel attacker 和 compromise 假设。

实验记录：

- `proverif/ledgers/secrecy-trace-ledger.md`: session-key secrecy 和 compromise 实验记录。
- `proverif/ledgers/authentication-query-ledger.md`: authentication / correspondence 查询记录。

历史过程：

- `proverif/archive/`: 已被当前核心文档覆盖的早期计划、旧实验计划和历史 trace 记录。

## Tamarin

`docs/tamarin/` 用于后续 Tamarin 阶段。

Tamarin 主要负责：

- partnered / unpartnered session；
- BatchReceive；
- state consumption；
- compromise ordering；
- receiver-side exception theorem candidate。

当前还没有正式 Tamarin 模型。

## CryptoVerif

`docs/cryptoverif/` 用于后续 CryptoVerif 或 computational proof 阶段。

CryptoVerif / computational proof 主要负责：

- computational KIND game；
- real-or-random indistinguishability；
- KDF 3PRF hybrid；
- UNF-1KMA；
- IND-1BatchCCA；
- advantage bound。

当前还没有正式 CryptoVerif 模型。

## Roadmap

`docs/roadmap/` 记录跨工具路线计划。

- `roadmap/next-tool-plan.md`: ProVerif 阶段之后的 Tamarin / CryptoVerif 后续计划。

## 当前维护规则

- ProVerif 已完成内容写入 `docs/proverif/`。
- Tamarin 新内容写入 `docs/tamarin/`。
- CryptoVerif / computational proof 新内容写入 `docs/cryptoverif/`。
- 跨工具路线写入 `docs/roadmap/`。
- 不要把 Tamarin 或 CryptoVerif 文档继续混入 `docs/proverif/`。
- 新实验结果优先写入对应 ledger。
- 阶段性汇报写入对应工具目录下的 report。
