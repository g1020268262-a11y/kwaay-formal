# ProVerif Docs

这个目录记录 K-Waay Figure 7 core 的 ProVerif symbolic analysis。

## 当前状态

ProVerif core symbolic stage 已经完成。

当前完成范围：

- Figure 7 core；
- public-channel symbolic model；
- single receive approximation；
- baseline secrecy；
- compromise experiments；
- sender-side exception sanity check；
- split-KEM component authenticity；
- paper definition alignment。

当前不声称：

- 完整 K-Waay 协议安全；
- full BatchReceive；
- partnered / unpartnered 完整语义；
- computational KIND proof；
- UNF-1KMA / IND-1BatchCCA computational proof。

## 推荐阅读顺序

1. `current-stage-report.md`
2. `formal-decision-memo.md`
3. `paper-definition-alignment.md`
4. `proverif-file-inventory.md`
5. `ledgers/secrecy-trace-ledger.md`
6. `ledgers/authentication-query-ledger.md`

## 文件说明

- `current-stage-report.md`: ProVerif 阶段最终汇报稿。
- `formal-decision-memo.md`: query 分类和建模决策。
- `paper-definition-alignment.md`: 论文定义与 ProVerif query 对齐。
- `protocol-map.md`: 协议对象和符号映射。
- `threat-model.md`: 攻击者模型。
- `proverif-file-inventory.md`: `.pv` 文件用途清单。
- `ledgers/`: 实验结果记录。
- `archive/`: 早期计划和历史文档。
