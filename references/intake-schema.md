# Intake Schema

## Purpose

这份文档定义 `image2-design-director` 的 intake 入口，不再只收资产合同，也要同步收：

- 信息合同
- 表达机制假设
- 交付约束
- 资产身份与发表状态

一句话版本：

> intake 的职责是把“要交什么资产、图里哪些信息可信、准备用什么表达机制、后续还能不能安全交付、当前结果最终是不是 publication asset”收成一份可判断的入口，而不是提前写 prompt。

## Position In The Loop

这个 schema 对应：

1. `Requirement Intake`
2. `Asset Contract Lock`
3. `Information Reliability Gate` 的前置输入准备
4. `Publication Identity Guard` 的前置输入准备

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

### 4. Publication Identity Is Part Of Intake

如果任务会进入正文、封面、文中插图、机制图、证据图或任何发表场景，intake 必须先回答：

- 当前目标是不是 `publication_asset`
- 哪些产物只允许停留在 `internal_candidate` 或 `review_candidate`
- 有没有跨场景残留文案、CTA、二维码、日期、badge 等禁入元素

### 5. Representation Strategy Is Part Of Intake Handoff

intake 不必最终拍板，但必须初步判断：

- 更像模型直出
- 更像模型图像加轻量文字
- 更像程序化 / 确定性表达
- 还是明显要走混合路径

### 6. Ask Only High-Leverage Questions

如果需要补问，只问会显著改变下面 5 类结果的字段：

1. 资产合同
2. 信息可靠性
3. 表达机制
4. 交付可行性
5. 发表资产身份

## Intake Outputs

一次合格的 intake 至少应产出下面 7 个对象：

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
6. `asset_identity_snapshot`
   - 目标 artifact role、内部工件边界、publication 风险
7. `readiness_snapshot`
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
| `protected_regions` | 预计需要叠字或 fixed elements 时 | 不可侵入区域 |
| `overlay_classes_expected` | 预计会做 overlay 时 | 允许进入的 overlay 类别 |
| `reference_assets` | 有参考图、旧版本、已有素材时 | 参考资产 |
| `source_materials` | 有截图、页面、PDF、附件时 | 输入素材 |
| `existing_generation_context` | 已有上一版或失败图时 | 当前 iteration 上下文 |
| `must_avoid` | 有明确禁区时 | 必须避免的方向 |

### Asset Identity Fields

| Field | Required | Meaning |
|---|---|---|
| `target_artifact_role` | yes | `internal_candidate / review_candidate / publication_asset` |
| `publication_intent` | yes | 是否预期进入文章正文、封面、图注或对外发表 |
| `cross_scene_residue_forbidden` | yes | 是否禁止跨场景残留 CTA / 报名 / 二维码 / badge / 日期等 |
| `internal_only_artifact_classes` | yes | 当前任务中哪些产物只能算内部工件 |
| `publication_review_required` | yes | 是否要求走 `publication_readiness_review` |

### Execution Handoff Fields

| Field | Required | Meaning |
|---|---|---|
| `open_questions` | yes | 仍可能影响结果的问题 |
| `missing_critical_fields` | yes | 仍缺的关键信息 |
| `intake_confidence` | yes | `low / medium / high` |
| `recommended_route_hint` | yes | `direct / brief-first / repair / contract_realign` |

## Scene Profiles

### `wechat_article_editorial_visual_set`

用于：

- 微信公众号封面配图
- 正文机制图
- 文中证据图
- 同一篇文章的一组 editorial collateral

默认合同：

- `deliverable_type: wechat_article_editorial_visual_set`
- `usage_context: wechat article editorial publication`
- `asset_completion_mode: complete_asset`
- `allowed_text_scope: article-owned editorial text only`
- `layout_owner: hybrid`
- `acceptance_bar: publication_ready_editorial_asset`
- `target_artifact_role: publication_asset`
- `publication_review_required: yes`

默认解释：

- 默认交付成品图，不是 `title-safe`、`text-safe`、`masthead-safe` 中间稿
- 可以存在内部 bundle 或 overlay 过程，但这些默认不等于最终交付物
- 除非文章明确需要，否则默认禁止 event poster 语义、报名文案、二维码、CTA、日期、badge

### `editorial_publication_visual`

用于：

- 单张文章主图
- 专栏头图
- 报告式 editorial figure
- 机制解释图、workflow evidence figure

默认合同：

- `deliverable_type: editorial_publication_visual`
- `usage_context: editorial publication`
- `asset_completion_mode: complete_asset`
- `allowed_text_scope: article-owned editorial text only`
- `layout_owner: hybrid`
- `acceptance_bar: publication_ready_editorial_asset`
- `target_artifact_role: publication_asset`
- `publication_review_required: yes`

默认解释：

- 默认交付面向读者可见的成品图
- 只有通过 publication review 的版本才可进入正文
- 中间态只能停留在内部工件层

## Field Guidance

### `deliverable_type`

写最终资产，不要写气氛词。

更推荐：

- `brand promo poster`
- `README hero`
- `social launch creative`
- `onboarding visual`
- `data-backed comparison visual`
- `wechat_article_editorial_visual_set`
- `editorial_publication_visual`

### `usage_context`

写最终出现在哪里，而不是只写“做一张图”。

更推荐：

- `wechat article editorial publication`
- `editorial publication`
- `social campaign launch`
- `README homepage hero`

### `allowed_text_scope`

必须写成“哪些文字能出现，哪些不能出现”。

文章场景默认推荐：

- `article title / subtitle / figure label / short editorial explainer only`

默认不包含：

- event signup CTA
- 报名按钮语义
- 二维码
- 活动日期
- badge
- 与文章无关的口号或品牌固定件

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

### `protected_regions`

如果任务会进入 editorial overlay，最少要声明：

- `title_region`
- `core_subject_region`
- `focus_information_region`

没有这些区域时，只能说做了基础 box-level coverage，不能 claim 已完成完整碰撞检测。

### `target_artifact_role`

默认语义：

- `internal_candidate`
  - benchmark candidate、overlay demo、delivery bundle artifact、exploratory repair output
- `review_candidate`
  - 已可进入内部评审，但还不能对用户可见
- `publication_asset`
  - 通过 publication review，可进入正文或对外发表

## Readiness Rules

- 如果 `asset contract` 不清，优先 `brief-first`
- 如果 `factual_sensitivity` 高但 `evidence_requirement` 未满足，不能进入普通 prompt assembly
- 如果预期 overlay 但 `protected_regions` 完全未知，默认不能把当前任务标成 delivery-ready
- 如果 `representation_mode = undecided` 且它会改变结果可用性，也应先补齐再继续
- 如果 `usage_context` 是文章或 editorial publication，但 `asset_completion_mode` 不是 `complete_asset`，默认不能判成最终交付
- 如果 `target_artifact_role != publication_asset`，当前版本默认不能给用户，也不能进入正文
