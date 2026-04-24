# Publication Asset Production Protocol

## Purpose

这份文档定义文章配图、公众号头图、机制图和 workflow evidence 图在生成前应该如何被生产。

它补的是 production side，不是 review side：

> review 负责拦住坏结果；production protocol 负责让 Agent 一开始就走对路线。

当前路线结论：

> Image2 直出完整资产是默认主路径；后期只负责二维码、Logo、Exact copy、已锁定数值和多尺寸适配等确定性补丁。不要把后期工程升级成默认图片制作路线。

## Required Production Packet

每个 editorial publication asset 在 prompt assembly、Image2 调用、确定性渲染或 overlay 前，必须先形成 `production_packet`。

最小字段：

```yaml
figure_role: editorial_cover | mechanism_figure | workflow_evidence
asset_goal: short statement of the article argument this asset supports
representation_mode: model_direct_visual | model_visual_with_limited_text | visual_base_plus_post | hybrid_visual_plus_deterministic_overlay | deterministic_render
layout_owner: model | deterministic_renderer | hybrid
text_owner: model | deterministic_overlay | deterministic_renderer
text_budget:
  headline: 1
  subtitle: 0-1
  node_labels: 0-8
  paragraphs: 0
visual_structure: short structure description
required_visual_evidence:
  - optional evidence object names
postprocess_scope:
  - none by default
  - qr_code
  - logo
  - exact_copy
  - locked_value_replacement
  - export_adaptation
forbidden_drift:
  - benchmark artifact
  - generic README hero
candidate_policy: single | multi_candidate
repair_policy: micro_repair | regenerate | contract_realign
```

## Direct-First Classification

Default to Image2 complete-asset direct output for:

- `editorial_cover`
- `base_visual`
- `mechanism_figure`
- `workflow_evidence`
- `advance_figure`
- `evidence_figure`
- `data_figure`
- `price_figure`
- `ranking_figure`

Route to surgical post-processing only for:

- QR code
- Logo / brand lockup
- exact copy that must be identical
- confirmed value replacement for price, date, ranking, or metric labels
- export crop / resize / padding adaptation

Full deterministic rendering is an explicit exception, not the default. Use it when the user asks for a programmatic chart/table, when compliance requires exact reproduced values across the whole asset, or when Image2 candidates have already failed visual or information viability.

## Figure Role Defaults

### `editorial_cover`

Default production route:

- `representation_mode = model_direct_visual` or `model_visual_with_limited_text`
- `layout_owner = model`
- `text_owner = model` for the first candidate set
- `candidate_policy = multi_candidate`
- `postprocess_scope = exact_copy` only if the title must be replaced or locked after review

Text budget:

- one headline
- zero or one subtitle
- no paragraph body
- no dense labels

Production rule:

> The image model should create the finished cover, including the core title treatment. Deterministic overlay is only for surgical exact-copy replacement after a strong direct candidate exists.

Common no-go routes:

- pure deterministic schematic cover without explicit override
- post-processing that rebuilds the cover layout
- model-rendered long paragraph copy
- report-page layout that lacks cover tension

### `mechanism_figure`

Default production route:

- `representation_mode = model_direct_visual` or `model_visual_with_limited_text`
- `layout_owner = model`
- `text_owner = model` for short labels, `deterministic_overlay` only for exact-label repair
- `candidate_policy = multi_candidate` unless the user explicitly requests a strict schematic

Text budget:

- one headline
- optional short subtitle
- 4 to 8 node labels
- no paragraphs inside cards

Production rule:

> The image should explain the mechanism as a finished publication figure. Use post-processing only to replace exact labels, not to design the whole figure.

Common no-go routes:

- paragraph-heavy cards
- broken English labels
- decorative workflow board with unclear mechanism
- using the model to render dense exact Chinese text
- deterministic schematic output that is visibly weaker than a direct Image2 candidate

### `workflow_evidence`

Default production route:

- `representation_mode = model_direct_visual` or `model_visual_with_limited_text`
- `layout_owner = model`
- `text_owner = model` for short labels, `deterministic_overlay` only for exact-label repair
- `candidate_policy = multi_candidate`

Text budget:

- one headline
- zero or one subtitle
- up to three short section labels
- no paragraph body

Required evidence objects:

- `runtime_capture`
- `scorecard`
- `delivery_bundle`
- `route_trace`
- `accepted_asset_state`

Production rule:

> The visual must be a finished Image2 publication asset that shows concrete workflow evidence, not a weak schematic that was made controllable by post-processing.

Common no-go routes:

- generic README hero
- abstract radar target as the main proof
- device cluster without workflow artifacts
- publication assets shown as empty frames only
- post-processing used as the primary source of visual quality

### `data_figure`, `price_figure`, `ranking_figure`

Default production route:

- `representation_mode = model_direct_visual` or `model_visual_with_limited_text`
- `layout_owner = model`
- `text_owner = model` for broad labels, `deterministic_overlay` only for confirmed exact values
- `candidate_policy = multi_candidate`

Production rule:

> First ask Image2 for a finished editorial data, price, or ranking visual after the reliability gate has locked the information contract. Then surgically replace only the values or labels that must be exact.

Common no-go routes:

- skipping the reliability gate
- letting invented model numbers stand as verified facts
- defaulting to a plain deterministic table when the user asked for a publication visual
- rebuilding the whole image in post just because it contains data

## Production Preflight

Before generating, run `production_preflight`.

It returns:

- `pass`
- `conditional_pass`
- `fail`

### Hard Blockers

- missing `figure_role`
- missing `asset_goal`
- unsupported `representation_mode`
- `editorial_cover` with pure `deterministic_render` and no explicit override
- `mechanism_figure` with paragraph budget above zero
- `mechanism_figure` with model-owned dense text
- `workflow_evidence` missing required evidence objects
- post-processing scope includes full layout rebuild without explicit override
- data, price, or ranking figure skips `information_reliability_gate`
- missing `forbidden_drift`
- `multi_candidate` required but not selected

### Conditional Blockers

- subtitle budget above one
- node label budget too high
- visual structure too vague
- repair policy missing

## Relationship To Review

Passing production preflight does not mean the output is good. It only means the production route is valid.

The output must still pass:

- `delivery_viability_gate`
- `publication_identity_review`
- `visual_quality_review`
- `final_release_gate`

## Runtime Requirement

The selected production packet must be stored in bundle metadata and runtime capture. If a production packet is missing, the final release gate cannot return `pass`.
