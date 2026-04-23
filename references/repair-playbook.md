# Repair Playbook

## 目标

repair 模式下，不靠“再来一版”碰运气，而是先判断失败属于：

- `micro_repair`
- `contract_realign`

一句话版本：

> 如果错的是细节，就做微修；如果错的是任务理解，就先重建交付物合同。

## 总规则

1. 先给失败归类
2. 一轮只改 1 到 2 个关键变量
3. 明确 `Change only` 和 `Keep unchanged`
4. 如果错的是合同，不要直接补 prompt，先重对齐任务

## Repair Class 1. `micro_repair`

适用于：

- 资产类型对了
- 成品度对了
- 语言对了
- 但细节、结构、工艺、文字纪律没过线

常见场景：

- 中文标题控制不稳
- 版式层级还不够稳
- 主体对了，但工艺不够精

输出模板：

```text
Repair class: micro_repair
Failure class: <哪一类失败>
Why it failed: <一句话根因>
Change only: <本轮只改什么>
Keep unchanged: <必须保持什么>
Prompt delta: <本轮新增或替换的关键约束>
```

## Repair Class 2. `contract_realign`

适用于：

- 用户指出“这不是我要的资产类型”
- 用户指出“这不是成品”
- 用户指出“语言不对”
- 品牌语义漂移到错误 domain

这类 repair 的第一步必须是重建下面这些字段：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `acceptance_bar`

输出模板：

```text
Repair class: contract_realign
What was misread: <资产类型 / 成品度 / 语言 / 品牌语义>
Reset contract:
- Deliverable:
- Completion mode:
- Content language:
- Allowed text scope:
- Acceptance bar:
Next move: <重新生成还是进入新一轮 direct>
```

## Failure Types To Watch

### 1. Brand / Promo Asset Drifted Into Base Visual

默认：

- `contract_realign`

### 2. Language Drift

例如：

- 中文任务里自动切英文 slogan

默认：

- 若整体资产类型没错，可 `micro_repair`
- 若语言其实牵动整体版式和成品度，优先 `contract_realign`

### 3. Wrong Asset Type

例如：

- 品牌海报做成 README hero
- README hero 做成社媒海报

默认：

- `contract_realign`

### 4. Brand Semantics Drift

例如：

- 项目海报被补成建筑 / 地产 / 室内 / 材料板

默认：

- `contract_realign`

### 5. Good-Looking But Not Usable

默认：

- 若核心原因是成品度错位，`contract_realign`
- 若只是局部排版还差一点，`micro_repair`
