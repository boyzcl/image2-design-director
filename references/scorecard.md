# Scorecard

## Purpose

把“像不像真实设计产物、信息是否可信、交付是否仍可用、当前是不是正确的 publication asset”收成可量化评分。

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
| intent_match | 8 | 结果是不是在解决用户要解决的问题 |
| asset_type_fidelity | 10 | 它是不是用户要的那类资产 |
| asset_identity_stability | 10 | 它是不是正确身份的资产，而不是内部工件冒充成品 |
| contract_alignment | 8 | 输出是否仍在原始交付物合同内 |
| information_reliability | 12 | 关键信息是否可信、口径是否清楚 |
| representation_fit | 8 | 这类内容是否由正确表达机制承载 |
| delivery_integrity | 10 | overlay / fixed elements / 导出后是否仍然稳定 |
| publication_argument_support | 10 | 这张图是否真正支撑文章论点 |
| publication_cleanliness | 8 | 是否清除了跨场景残留文案与 fixed elements |
| completion_readiness | 6 | 现在是不是用户可验收的完成状态 |
| language_alignment | 5 | 文案语言和文字纪律是否符合当前任务 |
| asset_credibility_and_craft | 5 | 是否像真实可工作的资产，且工艺干净 |

总分 = `sum(score / 5 * weight)`

## Result Bands

- `85-100`: `pass`
- `75-84`: `conditional_pass`
- `<75`: `fail`

## Hard Fail Rules

出现以下任一项时，即使总分高，也默认不能判 `pass`：

- `misleading_risk = high`
- 资产类型明显错误
- 资产身份明显错误
- 成品任务被做成底图
- 高事实敏感任务没有通过 reliability gate
- 精确数据仍依赖不可信模型文本
- delivery viability 已明确 no-go
- publication review 结果不是 `pass`
- 当前 `artifact_role != publication_asset`

## Dimension Notes

### `asset_identity_stability`

问：

- 当前结果是不是正确身份的资产
- benchmark candidate、delivery bundle artifact、overlay demo、exploratory repair output 有没有被误当最终图

低分示例：

- `text_safe_visual` 被直接拿去进正文
- A/B 候选图被误当最终封面

### `information_reliability`

问：

- metric、日期、claim 边界是否清楚
- evidence requirement 是否满足
- 如果未满足，是否执行了正确降级

### `representation_fit`

问：

- 这轮是否用了匹配的表达机制

低分示例：

- 数据 / 价格 / 排行图跳过 reliability gate
- 已锁定数值需要逐数一致，却没有做局部替换或复核
- 应该 complete asset 的文章图被误降成底图

### `delivery_integrity`

问：

- 交付后的图还能不能继续用
- overlay 是否侵入 protected regions
- 多层信息有没有把主视觉打散

### `publication_argument_support`

问：

- 这张图是否真正支撑文章论点
- 图像是在解释文章，还是在引入无关场景

### `publication_cleanliness`

问：

- 是否仍残留活动报名语义、CTA、二维码、badge、日期、fixed elements 或其他错场景元素

## Publication Readiness Review

文章图、editorial collateral、publication figure 在 scorecard 后必须再跑这一层。

它现在只判断 publication identity，不再单独代表最终发布通过。

### Review Outputs

- `pass`
  - 资产身份正确，可进入用户可见输出与正文
- `conditional_pass`
  - 仅可继续内部修订，不能给用户，也不能进入正文
- `fail`
  - 必须回到 repair / realign / regenerate

### Required Checks

必须显式评估：

1. `asset_identity_result`
   - 当前是不是正确的 publication asset
2. `argument_support_result`
   - 是否真正支持文章论点
3. `cross_scene_residue_result`
   - 是否仍有跨场景残留文案或 fixed elements
4. `artifact_role_check`
   - 当前 `artifact_role` 是否已是 `publication_asset`
5. `publication_blockers`
   - 未通过的具体阻塞项

### Hard Rule

`conditional_pass` 不算通过。

只有 `publication_readiness_review = pass` 时，当前图才允许进入下一层 `visual_quality_review`。

## Production Preflight

文章发表资产在生成前必须先跑 `production_preflight`。

### Required Outputs

- `production_preflight_result`
- `production_preflight_blockers`
- `production_preflight_warnings`
- `production_packet`

### Review Meaning

- `pass`
  - production route 与 figure role 匹配，可以进入生成
- `conditional_pass`
  - route 可继续内部修订，但不能直接进入最终生成
- `fail`
  - 必须回到 production packet 或 contract realign

## Visual Quality Review

`visual_quality_review` 评估图面质量，不评估资产身份。

### Dimensions

| Dimension | score_0_5 | Meaning |
|---|---:|---|
| `text_readability` | 0-5 | 文字是否清楚、无异常断行 |
| `typographic_craft` | 0-5 | 字体、行距、字号、层级是否成熟 |
| `layout_hierarchy` | 0-5 | 标题、主体、辅助信息是否稳定 |
| `semantic_clarity` | 0-5 | 读者能否理解图在表达什么 |
| `publication_argument_support_visual` | 0-5 | 图像本身是否支撑文章论点 |
| `series_consistency` | 0-5 | 同组图是否一致但不模板化 |
| `asset_distinctiveness` | 0-5 | 是否具备该图角色的独特性 |
| `polish_and_finish` | 0-5 | 是否像真实可发布资产 |

### Bands

- `85-100`: `pass`
- `70-84`: `conditional_pass`
- `<70`: `fail`

Hard blockers make the result `fail` even if the numeric score is higher:

- `broken_word`
- `broken_chinese_line`
- `paragraph_overload`
- `template_sameness`
- `weak_article_support`
- `internal_draft_look`

## Final Release Gate

最终用户可见输出必须通过 `final_release_gate`。

### Required Inputs

- `production_preflight_result`
- `publication_review_result`
- `visual_quality_review_result`
- `delivery_viability_result`
- `runtime_capture_present`

### Rule

`final_release_result = pass` requires all of:

- `production_preflight_result = pass`
- `publication_review_result = pass`
- `visual_quality_review_result = pass`
- `delivery_viability_result != overlay_not_allowed_regenerate`
- `runtime_capture_present = true`

如果任一项不成立，当前图最多是 `conditional_pass`，不能进入正文或作为成功样张。

## Recommended Output Format

```md
## Score

- total: 88 / 100
- result: pass
- misleading_risk: low
- hard_fail_reason: none

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 5 | 8 | 8 | 目标问题对齐 |
| asset_type_fidelity | 5 | 10 | 10 | 已是文章封面资产 |
| asset_identity_stability | 5 | 10 | 10 | 不是 benchmark 或内部 bundle 工件 |
| contract_alignment | 4 | 8 | 6.4 | 与合同一致 |
| information_reliability | 4 | 12 | 9.6 | 事实边界清楚 |
| representation_fit | 4 | 8 | 6.4 | hybrid 路径合理 |
| delivery_integrity | 4 | 10 | 8 | protected regions 保住了主体 |
| publication_argument_support | 5 | 10 | 10 | 直接服务文章主论点 |
| publication_cleanliness | 5 | 8 | 8 | 无残留 CTA / QR / badge |
| completion_readiness | 5 | 6 | 6 | 已是 complete_asset |
| language_alignment | 5 | 5 | 5 | 语言纪律正确 |
| asset_credibility_and_craft | 4 | 5 | 4 | 工艺干净可信 |

## Publication Readiness Review

- result: pass
- asset_identity_result: pass
- argument_support_result: pass
- cross_scene_residue_result: pass
- artifact_role_check: publication_asset
- publication_blockers: none
```
