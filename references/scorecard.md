# Scorecard

## Purpose

把“像不像真实设计产物、信息是否可信、交付是否仍可用”收成可量化评分。

## Scoring Anchors

- `0` 不成立，明显失真或跑偏
- `1` 问题严重，基本不可用
- `2` 勉强有方向，但明显不过线
- `3` 可作为内部工作稿
- `4` 可作为高质量外部草稿
- `5` 接近发布级或当前阶段最优解

## Total Structure

| Dimension | Weight | 核心问题 |
|---|---:|---|
| intent_match | 10 | 结果是不是在解决用户要解决的问题 |
| asset_type_fidelity | 12 | 它是不是用户要的那类资产 |
| contract_alignment | 8 | 输出是否仍在原始交付物合同内 |
| information_reliability | 15 | 关键信息是否可信、口径是否清楚 |
| representation_fit | 10 | 这类内容是否由正确表达机制承载 |
| delivery_integrity | 12 | overlay / fixed elements / 导出后是否仍然稳定 |
| completion_readiness | 8 | 现在是不是用户可验收的完成状态 |
| language_alignment | 8 | 文案语言和文字纪律是否符合当前任务 |
| structure_and_composition | 9 | 构图、栅格、留白、主次是否稳定 |
| asset_credibility_and_craft | 8 | 是否像真实可工作的资产，且工艺干净 |

总分 = `sum(score / 5 * weight)`

## Result Bands

- `85-100`: `pass`
- `75-84`: `conditional_pass`
- `<75`: `fail`

## Hard Fail Rules

出现以下任一项时，即使总分高，也默认不能判 `pass`：

- `misleading_risk = high`
- 资产类型明显错误
- 成品任务被做成底图
- 高事实敏感任务没有通过 reliability gate
- 精确数据仍依赖不可信模型文本
- delivery viability 已明确 no-go

## Dimension Notes

### `information_reliability`

问：

- metric、日期、claim 边界是否清楚
- evidence requirement 是否满足
- 如果未满足，是否执行了正确降级

### `representation_fit`

问：

- 这轮是否用了匹配的表达机制

低分示例：

- 应该 deterministic 的图表却交给了模型直出
- 应该 complete asset 的品牌图被误降成底图

### `delivery_integrity`

问：

- 交付后的图还能不能继续用
- overlay 是否侵入 protected regions
- 多层信息有没有把主视觉打散

## Recommended Output Format

```md
## Score

- total: 84 / 100
- result: conditional_pass
- misleading_risk: low
- hard_fail_reason: none

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4 | 10 | 8 | 任务目标基本对齐 |
| asset_type_fidelity | 4 | 12 | 9.6 | 已像目标资产 |
| contract_alignment | 4 | 8 | 6.4 | 仍在合同边界内 |
| information_reliability | 3 | 15 | 9 | 数值口径已锁，但日期免责声明还不够显式 |
| representation_fit | 4 | 10 | 8 | hybrid 路径基本正确 |
| delivery_integrity | 3 | 12 | 7.2 | footer 区有点拥挤 |
| completion_readiness | 4 | 8 | 6.4 | 可作为高质量草稿 |
| language_alignment | 5 | 8 | 8 | 语言纪律正确 |
| structure_and_composition | 4 | 9 | 7.2 | 主次稳定 |
| asset_credibility_and_craft | 4 | 8 | 6.4 | 像真实产物，工艺较干净 |
```
