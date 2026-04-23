# Strategy Decision Tree

## Purpose

这份文档定义 `image2-design-director` 在 `Stage 2. Strategy Selection` 的显式决策树。

它回答的问题不是 prompt 怎么写，而是：

- 这次任务到底该怎么跑
- 是完整成品还是底图任务
- 默认文案语言是什么
- 先对齐交付物合同，还是先进入生成
- 失败后该做微修，还是重建合同

一句话版本：

> strategy 的职责不只是选 route，而是先确认“做的是不是对的资产”，再决定怎么生成。

## Core Decision Layers

策略判断分成 6 层，必须按顺序做。

### Layer 0. Confirm Scene Profiling

先确认：

- `domain_direction`
- `matched_profile`
- `support_tier`

### Layer 1. Confirm Asset Contract

再确认：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

### Layer 2. Identify Task Mode

判断这轮属于：

- `fresh_generation`
- `repair_iteration`
- `delivery_refinement`
- `benchmark_or_ab`

### Layer 3. Choose Route

在 `fresh_generation` 或 `repair_iteration` 下，再判断 route：

- `direct`
- `brief-first`
- `repair`
- `contract_realign`

### Layer 4. Choose Execution Mode

继续判断：

- `single-output`
- `multi-candidate`
- `direct_output`
- `visual_base_plus_post`

### Layer 5. Choose Delivery Involvement

最后判断：

- `image-only`
- `image-plus-delivery-ops`

## Decision Order

每次都按这个顺序判断：

1. 当前场景画像是什么
2. 最终交付物是什么
3. 这是成品还是底图
4. 默认文案语言是什么
5. 这轮是 fresh / repair / delivery / benchmark 哪一类
6. 是否需要重对齐合同
7. route 是什么
8. 是单图还是多候选
9. 是直出还是底图 + 后处理
10. 是否要把 delivery ops 一起纳入本轮

不要跳过前面的判断，直接根据直觉决定候选数、后处理或 repair 方式。

## Layer 0. Scene Profiling

这层沿用当前三件事：

- `domain_direction`
- `matched_profile`
- `support_tier`

当前加速档案仍是：

- `product-mockup`
- `social-creative`
- `ui-mockup`
- `app-asset`

但它们只是加速器，不是交付物合同。

## Layer 1. Asset Contract Decision

这层必须同时回答 6 个问题：

1. 这轮最终交付物类型是什么
2. 这是完整成品、底图，还是交付细化
3. 默认文案语言是什么
4. 允许出现哪些可读文字
5. 谁负责最终排版
6. 怎样才算用户可验收

### A. Completion-Sensitive Asset Types

以下任务默认按 `complete_asset` 处理，除非用户明确说先做底图：

- `brand promo poster`
- `brand poster`
- `launch poster`
- `project launch poster`
- `recruitment poster`
- `project intro poster`

### B. Base-Visual-Sensitive Asset Types

以下任务更容易默认走 `base_visual`：

- `README hero base`
- `text-safe background visual`
- `device scene for later layout`
- `visual plate`

### C. Content Language Rule

默认规则：

- 当前会话语言 = 默认文案语言

项目名、产品名、repo 名可保留原文，但 slogan / subtitle / CTA / supporting copy 默认跟随当前会话语言。

### D. Allowed Text Scope Rule

当任务涉及文字时，必须明确：

- 允许出现的可读文字只有哪些
- 是否允许额外小字
- 是否允许伪 UI 文案

如果没有锁定，就优先 `brief-first`。

## Layer 2. Task Mode Decision

### `repair_iteration`

满足以下任一项时，优先判为 `repair_iteration`：

- 用户明确说“上一版不对”
- 用户给出已有生成结果并要求调整
- `existing_generation_context` 非空

### `delivery_refinement`

满足以下大部分时，可判为 `delivery_refinement`：

- 主视觉方向已经过线
- 当前需求主要是叠字、二维码、logo、尺寸适配、版本导出

### `benchmark_or_ab`

满足以下任一项时，可判为 `benchmark_or_ab`：

- 当前目标是比较两种以上策略
- 用户明确想看多个候选再选

### `fresh_generation`

不属于上面三类时，默认视为 `fresh_generation`。

## Layer 3. Route Decision

### Route 1. `direct`

当下面大部分都成立时，选择 `direct`：

- 交付物类型明确
- 成品度明确
- 文案语言明确
- 允许文字范围明确
- 使用场景明确
- 成功标准明确

### Route 2. `brief-first`

当缺少少量关键字段，且这些字段会显著改变交付物合同或结果时，选择 `brief-first`。

高频触发条件：

- 这是成品还是底图不清楚
- 文案语言不清楚
- 允许文字范围不清楚
- 使用位置不清楚
- 用户的通过标准不清楚

### Route 3. `repair`

当资产类型和合同大体没错，只是细节、工艺、结构、文字纪律没过线时，选择 `repair`。

这类 repair 默认属于：

- `micro_repair`

### Route 4. `contract_realign`

当下面任一项成立时，优先选择 `contract_realign`：

- 用户明确指出“这不是我要的资产类型”
- 用户明确指出“这不是成品”
- 输出语言与当前任务语言不一致
- 品牌宣传图被误做成底图
- README hero 被误做成品牌海报
- 结果整体语义漂移到错误 domain

这类 route 的第一步不是改 prompt，而是重建：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `acceptance_bar`

## Layer 4. Execution Mode Decision

### `single-output`

默认用于：

- 品牌宣传图
- 项目海报
- 已有清晰合同的交付任务

### `multi-candidate`

默认用于：

- benchmark
- A/B 测试
- 用户明确要求看方向选择

### `direct_output`

适用于：

- 用户要完整成品
- 文本量可控
- 没有必须后置的固定元素
- 模型本轮承担最终排版

### `visual_base_plus_post`

适用于：

- 用户明确要底图
- 有二维码、logo、价格、CTA 等高精度元素
- 需要后续适配多尺寸
- 或当前明确由 `post_process / hybrid` 承担最后排版

### Important Override

不要因为任务“有文字”就自动滑向 `visual_base_plus_post`。

如果合同已经明确是：

- `complete_asset`
- `layout_owner = model`
- 文本范围有限且清晰

那应保留 `direct_output` 作为首选。

## Layer 5. Delivery Involvement

### `image-only`

适用于：

- 这轮结果就是最终图像
- 或虽可能后续再用，但本轮不处理精确落版

### `image-plus-delivery-ops`

适用于：

- 当前已经进入交付层
- 需要处理固定元素、导出版本、尺寸适配

## Default Heuristics

### Brand / Promo / Launch Assets

默认：

- `task_mode = fresh_generation`
- `route = direct`
- `candidate_mode = single-output`
- `output_mode = direct_output`

除非用户明确要求底图或高精度后处理链。

### User Says “This Is Not What I Asked For”

默认：

- 不进入普通 `repair`
- 先进入 `contract_realign`

## Strategy Output Checklist

一份合格的 strategy 输出至少应显式回答：

1. 交付物类型是什么
2. 成品还是底图
3. 文案语言是什么
4. 允许哪些文字
5. route 是什么
6. repair 如果发生，会是 `micro_repair` 还是 `contract_realign`
