# Scorecard

## 目的

把“像不像真实设计产物、像不像用户真正要的资产”收成可量化评分。

## 评分锚点

- `0` 不成立，明显失真或跑偏
- `1` 问题严重，基本不可用
- `2` 勉强有方向，但明显不过线
- `3` 可作为内部工作稿
- `4` 可作为对外高质量草稿
- `5` 接近发布级或当前阶段最优解

## 总分结构

| Dimension | Weight | 核心问题 |
|---|---:|---|
| intent_match | 15 | 结果是不是在解决用户要解决的问题 |
| asset_type_fidelity | 15 | 它是不是用户要的那类资产 |
| contract_alignment | 10 | 输出是否仍在原始交付物合同内 |
| completion_readiness | 10 | 现在是不是用户可验收的完成状态 |
| language_alignment | 10 | 文案语言和文字策略是否符合当前任务 |
| product_native_fit | 10 | 是否像目标产品/品牌自己长出来的资产 |
| structure_and_composition | 10 | 构图、栅格、留白、主次是否稳定 |
| asset_credibility | 10 | 是否像真实可工作的产品图 / 传播图 / UI 图 |
| craft_finish | 5 | 工艺是否干净 |
| anti_ai_artifact | 5 | 是否存在明显 AI 味和结构幻觉 |

总分 = `sum(score / 5 * weight)`

## 过线规则

- `85-100`: `pass`
- `75-84`: `conditional_pass`
- `<75`: `fail`

## 一票否决红旗

出现以下任一项时，即使总分高，也默认不能判 `pass`：

- 资产类型明显错误
- 成品任务被做成底图
- 文案语言与任务语言明显不一致
- 文本块明显失真或不完整
- 结果“好看但没法用”

## 维度解释

### `asset_type_fidelity`

问：

- 这是不是用户要的资产，而不只是“相关图像”

### `contract_alignment`

问：

- 输出是否仍在：
  - `deliverable_type`
  - `asset_completion_mode`
  - `allowed_text_scope`
  - `acceptance_bar`

定义的边界之内

### `completion_readiness`

问：

- 用户现在能不能直接拿去用

### `language_alignment`

问：

- 文案语言是否跟随当前任务
- 是否出现不该有的额外语言噪音

## 推荐输出格式

```md
## Score

- total: 82 / 100
- result: conditional_pass

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4 | 15 | 12 | 目标方向基本正确 |
| asset_type_fidelity | 3 | 15 | 9 | 还偏 hero base，不够像完整品牌海报 |
| contract_alignment | 3 | 10 | 6 | 结果仍有半成品倾向 |
| completion_readiness | 2 | 10 | 4 | 不能直接拿去发 |
| language_alignment | 5 | 10 | 10 | 文案语言正确 |
| product_native_fit | 4 | 10 | 8 | 已有项目系统感 |
| structure_and_composition | 4 | 10 | 8 | 主次关系稳定 |
| asset_credibility | 4 | 10 | 8 | 像高质量工作稿 |
| craft_finish | 4 | 5 | 4 | 工艺较干净 |
| anti_ai_artifact | 4 | 5 | 4 | AI 味较低 |
```
