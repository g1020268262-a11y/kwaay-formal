# Tamarin Docs

这个目录用于后续 K-Waay Tamarin 阶段。

## 目标

Tamarin 阶段用于补充 ProVerif 不自然表达的状态和时间顺序问题。

重点包括：

- partnered / unpartnered session；
- BatchReceive；
- batch slot；
- receiver vector identifiers；
- state consumption；
- one-time prekey use；
- compromise ordering；
- receiver-side exception theorem candidate。

## 当前状态

当前还没有正式 Tamarin 模型。

下一步建议先写：

```text
tamarin-prestudy-plan.md
```

不要直接开始完整 K-Waay `.spthy` 模型。

## 推荐第一阶段

先做 toy model：

- 生成 state；
- 使用 state；
- 消耗 state；
- 泄露 state；
- 区分 compromise before / after accept。

然后再迁移到 K-Waay BatchReceive。
