# Intake Schema

## Purpose

这份文档定义 `image2-design-director` 的 intake 入口，不再只收资产合同，也要同步收：

- 信息合同
- 表达机制假设
- 交付约束

一句话版本：

> intake 的职责是把“要交什么资产、图里哪些信息可信、准备用什么表达机制、后续还能不能安全交付”收成一份可判断的入口，而不是提前写 prompt。

## Position In The Loop

这个 schema 对应：

1. `Requirement Intake`
2. `Asset Contract Lock`
3. `Information Reliability Gate` 的前置输入准备

它不负责最后决定 route，但必须为后续阶段提供足够明确的判断材料。

## Core Principles

### 1. Raw Request And Structured Understanding Must Stay Separate

必须同时保留：

- 用户原始请求
- 我们的结构化理解

否则后续无法区分“用户真这么说”还是“系统误解后补出来的意思”。

### 2. Asset Contract Before Style

先收清：

- 最终交付物类型
- 成品度
- 文案语言
- 允许文字范围
- 最终版式归属
- 验收标准

没有这层合同，就不应进入风格或 prompt family 讨论。

### 3. Information Contract Before Factual Expression

只要任务里存在任何可能被读者当成事实的信息，就要先收清：

- 这是哪类 claim
- 证据强度要求是什么
- 主线 metric 的定义是什么
- 截止日期是什么
- 如果证据不够，允许怎么降级表达

### 4. Representation Strategy Is Part Of Intake Handoff

intake 不必最终拍板，但必须初步判断：

- 更像模型直出
- 更像模型图像加轻量文字
- 更像程序化 / 确定性表达
- 还是明显要走混合路径

### 5. Ask Only High-Leverage Questions

如果需要补问，只问会显著改变下面 4 类结果的字段：

1. 资产合同
2. 信息可靠性
3. 表达机制
4. 交付可行性

## Intake Outputs

一次合格的 intake 至少应产出下面 6 个对象：

1. `raw_request`
   - 用户原话与素材入口
2. `requirement_summary`
   - 这轮最终要交什么
3. `asset_contract_snapshot`
   - 成品度、语言、允许文字、版式归属、验收标准
4. `information_contract_snapshot`
   - 事实敏感度、claim 类型、证据要求、metric 口径、日期截点、不确定性策略
5. `delivery_constraints_snapshot`
   - 固定元素、尺寸、protected regions、overlay 预期
6. `readiness_snapshot`
   - 缺失字段、开放问题、建议 route

## Minimum Intake Contract

### Required Core Fields

| Field | Required | Meaning |
|---|---|---|
| `user_raw_request` | yes | 用户原始请求 |
| `user_goal` | yes | 用户最终想完成什么 |
| `deliverable_type` | yes | 最终交付物类型 |
| `usage_context` | yes | 最终使用场景 |
| `requirement_summary` | yes | 结构化任务摘要 |
| `context_summary` | yes | 直接相关背景摘要 |
| `success_criteria` | yes | 用户视角的通过标准 |

### Asset Contract Fields

| Field | Required | Meaning |
|---|---|---|
| `asset_completion_mode` | yes | `complete_asset / base_visual / delivery_refinement / undecided` |
| `content_language` | yes | 默认文案语言 |
| `allowed_text_scope` | yes | 允许出现的可读文字范围 |
| `layout_owner` | yes | `model / post_process / hybrid` |
| `acceptance_bar` | yes | 怎样才算通过 |

### Information Reliability Fields

| Field | Required | Meaning |
|---|---|---|
| `factual_sensitivity` | yes | `low / medium / high` |
| `claim_type` | yes | `visual_analogy / factual / comparative / temporal / price / performance / mixed` |
| `evidence_requirement` | yes | `none / reference_provided / verify_before_render / exact_value_lock` |
| `metric_definition` | yes | 主线 metric 的定义；纯隐喻任务写 `not_applicable` |
| `as_of_date` | conditional | 时间、价格、对比、排行等任务的日期截点 |
| `uncertainty_policy` | yes | `visual_analogy_only / fact_with_disclaimer / stop_and_brief` 等 |
| `evidence_sources` | conditional | 来源、链接、附件、数据表或用户提供的证据入口 |

### Representation Handoff Fields

| Field | Required | Meaning |
|---|---|---|
| `representation_mode` | yes | `model_direct_visual / model_visual_with_limited_text / visual_base_plus_post / hybrid_visual_plus_deterministic_overlay / deterministic_render / undecided` |
| `primary_expression_system` | yes | `image_model / deterministic_renderer / hybrid` |
| `deterministic_render_needed` | yes | 是否需要确定性渲染承载关键内容 |
| `text_generation_tolerance` | yes | `none / decorative_only / headline_only / limited_structured_text / exact_text_not_allowed` |
| `numeric_render_strategy` | yes | `omit_numeric_claims / model_render_ok / overlay_exact_values / deterministic_chart` |

### Delivery Constraint Fields

| Field | Required When | Meaning |
|---|---|---|
| `fixed_text` | 有必须逐字正确文本时 | 必须保留的文字 |
| `fixed_elements` | 有二维码、logo、badge、价格牌等时 | 必须出现的固定元素 |
| `size_and_delivery_constraints` | 有尺寸、比例、导出要求时 | 交付约束 |
| `protected_regions` | 预计需要叠字或固定元素时 | 不可侵入区域 |
| `overlay_classes_expected` | 预计会做 overlay 时 | 允许进入的 overlay 类别 |
| `reference_assets` | 有参考图、旧版本、已有素材时 | 参考资产 |
| `source_materials` | 有截图、页面、PDF、附件时 | 输入素材 |
| `existing_generation_context` | 已有上一版或失败图时 | 当前 iteration 上下文 |
| `must_avoid` | 有明确禁区时 | 必须避免的方向 |

### Execution Handoff Fields

| Field | Required | Meaning |
|---|---|---|
| `open_questions` | yes | 仍可能影响结果的问题 |
| `missing_critical_fields` | yes | 仍缺的关键信息 |
| `intake_confidence` | yes | `low / medium / high` |
| `recommended_route_hint` | yes | `direct / brief-first / repair / contract_realign` |

## Field Guidance

### `deliverable_type`

写最终资产，不要写气氛词。

更推荐：

- `brand promo poster`
- `README hero`
- `social launch creative`
- `onboarding visual`
- `data-backed comparison visual`

### `factual_sensitivity`

判断的是：

- 观众会不会把这张图当成事实表达
- 错一项会不会造成误导

默认启发：

- 纯品牌氛围图通常是 `low`
- 带价格、日期、排行、性能结论时至少 `medium`
- 带精确数值、对比结论、时效口径时通常是 `high`

### `metric_definition`

不要只写“增长”“最强”“领先”。

更推荐：

- `7-day revenue growth rate`
- `BTC price in USD spot market`
- `monthly active users, global consumer app`

### `uncertainty_policy`

推荐只用能直接驱动行为的值：

- `visual_analogy_only`
- `fact_with_disclaimer`
- `stop_and_brief`

### `representation_mode`

这是表达机制，不是风格偏好。

示例：

- 品牌海报直出成品：`model_direct_visual`
- 需要 QR、logo 和精确 CTA：`visual_base_plus_post`
- 高事实敏感比较图：`hybrid_visual_plus_deterministic_overlay`
- 纯图表或精确数据板：`deterministic_render`

## Readiness Rules

- 如果 `asset contract` 不清，优先 `brief-first`
- 如果 `factual_sensitivity` 高但 `evidence_requirement` 未满足，不能进入普通 prompt assembly
- 如果预期 overlay 但 `protected_regions` 完全未知，默认不能把当前任务标成 delivery-ready
- 如果 `representation_mode = undecided` 且它会改变结果可用性，也应先补齐再继续
