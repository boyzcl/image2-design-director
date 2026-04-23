# Information Reliability Gate

## Purpose

这份文档定义 `image2-design-director` 在生成前如何判断信息是否可靠到值得被图像表达。

一句话版本：

> 不是看见“最新”才想起去验证，而是只要图里承载事实、时间、价格、比较或结论，就先判断信息可靠性，再决定能不能继续画。

## When To Trigger

满足以下任一项时进入：

- 图中会出现价格、日期、排行、涨跌、对比、性能、市场结论
- 用户请求信息图、数据图、对比图、带结论宣传图
- 任何 claim 可能被读者当成“这是事实”

## Required Questions

1. `factual_sensitivity` 是多少
2. `claim_type` 是什么
3. `metric_definition` 是否明确
4. `as_of_date` 是否锁定
5. `evidence_requirement` 是否满足
6. 证据不足时走什么 `uncertainty_policy`

## Output Values

### `verified_fact`

适用于：

- 主线 claim 已有足够证据
- metric 和日期已锁定
- 可以继续进入 representation selection

### `fact_with_disclaimer`

适用于：

- 信息基本可信，但仍需显式标注边界、日期或不确定性

### `visual_analogy_only`

适用于：

- 用户要的是“表达趋势或气质”
- 精确 claim 不可验证
- 任务仍可用视觉隐喻完成

动作：

- 移除精确数值、排行、价格和过强结论

### `blocked_needs_brief`

适用于：

- 高事实敏感任务缺少证据
- metric 定义本身含糊
- 日期或口径不清会显著改变结论

动作：

- 不进入常规 prompt assembly

## Evidence Policy

### `none`

只适用于：

- 纯视觉品牌任务
- 无事实承诺的隐喻图

### `reference_provided`

适用于：

- 用户已给页面、表格、截图、官方资料

### `verify_before_render`

适用于：

- 时间敏感、价格敏感、对比敏感任务

### `exact_value_lock`

适用于：

- 图中要出现精确数字
- 这些数字会直接影响读者判断

## Hard Rules

- 不要用关键词代替 gate
- 不要把“模型也许能写对”当成 evidence
- 信息验证不过线时，优先降级表达或停止，而不是换个好看的 prompt 继续赌
