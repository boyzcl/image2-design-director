# Repair Playbook

## Goal

repair 模式下，不靠“再来一版”碰运气，而是先判断失败发生在哪一层，再决定是微修、重对齐，还是直接重生成。

一句话版本：

> repair 现在先分 failure axis，再选 repair class；错的是细节才微修，错的是合同、信息口径或表达机制就先回上游。

## Failure Axis Before Repair Class

先判断失败属于哪一层：

1. `contract_failure`
2. `reliability_failure`
3. `representation_failure`
4. `delivery_viability_failure`
5. `craft_failure`

## General Rules

1. 先给失败归层
2. 一轮只改 1 到 2 个关键变量
3. 明确 `Change only` 和 `Keep unchanged`
4. 如果错在上游，不要只补 prompt
5. 如果 viability gate 已经 no-go，默认优先重生成

## Repair Class 1. `micro_repair`

适用于：

- 资产合同基本正确
- information reliability 已过线
- representation mode 基本正确
- 只是局部工艺、层级、有限 overlay 或文字纪律没过线

常见场景：

- 标题区层级还不够稳
- badge 或 CTA 太重
- 局部 overlay 擦到软保护区
- 语言细节跑偏但不影响整体 representation

输出模板：

```text
Repair class: micro_repair
Failure axis: <craft / delivery_viability / minor language>
Why it failed: <一句话根因>
Change only: <本轮只改什么>
Keep unchanged: <必须保持什么>
Prompt or delivery delta: <新增或替换的关键约束>
```

## Repair Class 2. `contract_realign`

适用于：

- 资产类型理解错
- 成品度理解错
- 语言策略理解错
- metric 或 claim 口径理解错
- 本该 hybrid / deterministic 的任务被误跑成模型直出

这类 repair 的第一步必须重建：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `metric_definition`
- `representation_mode`
- `acceptance_bar`

输出模板：

```text
Repair class: contract_realign
Failure axis: <contract / reliability / representation>
What was misread: <一句话>
Reset contract:
- Deliverable:
- Completion mode:
- Content language:
- Allowed text scope:
- Metric definition:
- Representation mode:
- Acceptance bar:
Next move: <new direct / hybrid render / deterministic render>
```

## When To Regenerate Instead Of Repair

下面情况默认优先重生成，而不是继续往当前图上补：

- `delivery_viability_failure` 且结果为 `overlay_not_allowed_regenerate`
- 主体区已经被占满
- dense info 需求与当前 representation 完全不匹配
- 继续补只会把图变得更不可信或更不可用

## Failure Types To Watch

### Brand / Promo Asset Drifted Into Base Visual

默认：

- `contract_failure`
- `contract_realign`

### Language Drift

默认：

- 若只影响细节，可 `micro_repair`
- 若牵动版式、成品度或事实表达，优先 `contract_realign`

### Wrong Metric Or Timeframe

例如：

- 用错比较口径
- 用错日期截点

默认：

- `reliability_failure`
- `contract_realign`

### Wrong Representation

例如：

- 数据 / 价格 / 排行图跳过 reliability gate
- 本应只替换 QR、Logo、Exact copy 或锁定数值，却把整张图交给后期工程重建
- 直出成品图被误降成底图或模板化 schematic

默认：

- `representation_failure`
- `contract_realign`

### Good-Looking But Not Usable

默认：

- 若核心原因是成品度错位，`contract_realign`
- 若核心原因是 overlay capacity 已耗尽，直接 `regenerate`
- 若只是局部工艺还差一点，`micro_repair`
