# Task Packet

## Purpose

这份文档定义 `image2-design-director` 在进入 prompt assembly 之前的统一任务包格式。

它的作用不是重复 intake，也不是重复 strategy，而是把两者合并成一个可直接交给后续阶段的执行对象。

一句话版本：

> intake 负责把需求收清楚，strategy 负责决定怎么做，task packet 负责把这两层结果压成一份可以稳定执行、稳定评估、稳定留痕的统一输入。

## Position In The Loop

这个 task packet 位于：

- `Stage 1. Requirement Intake`
- `Stage 2. Strategy Selection`

之后，服务于：

- `Stage 3. Prompt Assembly And Image Generation`
- `Stage 4. Evaluation And Scoring`
- runtime capture

## Why This Document Exists

如果没有 task packet，后续执行通常会遇到三类问题：

1. intake 信息有了，但写 prompt 时只用了其中一部分
2. strategy 已经判断过了，但执行时又按直觉重做一次
3. runtime 记录只留下 prompt 和结果，回看不到“为什么当时是这么做的”

task packet 的目标就是减少这三类断裂。

## What A Task Packet Must Contain

一次合格的 task packet 至少要能同时回答下面 5 个问题：

1. 用户原始想要什么
2. 我们理解后的交付目标是什么
3. 这轮任务的上下文边界是什么
4. 这轮决定怎么做，为什么这么做
5. 后续 prompt、评估和 runtime 应继承哪些字段

## Packet Structure

一个完整 task packet 由 6 个区块组成。

### 1. Request Block

保留用户原始输入，不做覆盖。

必须包含：

- `user_raw_request`

可选补充：

- `source_materials`
- `reference_assets`

### 2. Requirement Block

回答“这轮最终要交付什么”。

必须包含：

- `user_goal`
- `asset_type`
- `usage_context`
- `requirement_summary`
- `success_criteria`

### 3. Context Block

回答“这轮图像任务服务于什么语境”。

必须包含：

- `context_summary`

按需补充：

- `background_context`
- `brand_or_product_sources`
- `target_audience`
- `must_avoid`

### 4. Constraint Block

回答“这轮有哪些必须遵守的边界”。

按需包含：

- `fixed_text`
- `fixed_elements`
- `size_and_delivery_constraints`
- `direct_output_vs_post_process`

### 5. Strategy Block

回答“这轮决定怎么跑”。

必须包含：

- `domain_direction`
- `support_tier`
- `task_mode`
- `route`
- `candidate_mode`
- `output_mode`
- `delivery_involvement`
- `strategy_reasoning`

按需补充：

- `matched_profile`
- `profile_confidence`
- `generalization_strategy`
- `legacy_use_case`
- `question_budget`
- `repair_scope`
- `keep_unchanged`
- `route_override_reason`
- `strategy_conflicts`

### 6. Readiness Block

回答“这份任务包是否已经可以交给下一阶段”。

必须包含：

- `open_questions`
- `missing_critical_fields`
- `intake_confidence`
- `packet_readiness`

推荐值：

- `ready`
- `needs_brief`
- `blocked`

## Packet Design Rules

### 1. Preserve The Boundary Between Raw And Interpreted

必须同时保留：

- 原始请求
- 结构化理解

不要只保留我们整理后的版本，否则后面无法定位误解来源。

### 2. Keep Strategy Explicit

task packet 不能只留下内容字段，还必须把策略字段带进去。

否则到了 prompt assembly 阶段，执行者很容易重新按直觉做一遍策略判断。

### 3. Let Packet Readiness Control The Next Step

如果 packet 还不 ready，就不应该进入 prompt assembly。

推荐规则：

- `ready`: 进入 prompt assembly
- `needs_brief`: 先补 1 到 3 个高杠杆问题
- `blocked`: 当前不能继续，需用户补更多关键信息或重新定义目标

### 4. Keep Prompt Out Of The Packet

task packet 服务于 prompt，但 task packet 本身不是最终 prompt。

它不应包含：

- 最终 `final_prompt`
- 最终 `image_prompt`

否则 stage 2 和 stage 3 的边界会被打穿。

### 5. Preserve Packet Lineage

task packet 还应能回答：

- 这是从哪份 intake 来的
- 这是从哪份 strategy 结果来的
- 当前是第几轮任务包

否则到 runtime 和 repair 阶段，很容易只剩结果，不知道中间判断是怎么演化的。

## Minimum Packet Contract

下面这些字段构成最小可执行任务包。

| Block | Field | Required |
|---|---|---|
| request | `user_raw_request` | yes |
| requirement | `user_goal` | yes |
| requirement | `asset_type` | yes |
| requirement | `usage_context` | yes |
| requirement | `requirement_summary` | yes |
| requirement | `success_criteria` | yes |
| context | `context_summary` | yes |
| constraint | `direct_output_vs_post_process` | yes |
| strategy | `domain_direction` | yes |
| strategy | `support_tier` | yes |
| strategy | `task_mode` | yes |
| strategy | `route` | yes |
| strategy | `candidate_mode` | yes |
| strategy | `output_mode` | yes |
| strategy | `delivery_involvement` | yes |
| strategy | `strategy_reasoning` | yes |
| readiness | `packet_lineage` | yes |
| readiness | `open_questions` | yes |
| readiness | `missing_critical_fields` | yes |
| readiness | `intake_confidence` | yes |
| readiness | `packet_readiness` | yes |

## Packet Assembly Rules

task packet 不是独立发明的一层，它应由前两层稳定装配出来。

### From Intake

下面这些字段原则上直接继承自 intake：

- `user_raw_request`
- `source_materials`
- `reference_assets`
- `user_goal`
- `asset_type`
- `usage_context`
- `requirement_summary`
- `success_criteria`
- `context_summary`
- `background_context`
- `brand_or_product_sources`
- `target_audience`
- `must_avoid`
- `fixed_text`
- `fixed_elements`
- `size_and_delivery_constraints`
- `direct_output_vs_post_process`
- `open_questions`
- `missing_critical_fields`
- `intake_confidence`

### From Strategy

下面这些字段原则上直接继承自 strategy：

- `domain_direction`
- `matched_profile`
- `support_tier`
- `profile_confidence`
- `generalization_strategy`
- `legacy_use_case`
- `task_mode`
- `route`
- `candidate_mode`
- `output_mode`
- `delivery_involvement`
- `strategy_reasoning`
- `question_budget`
- `repair_scope`
- `keep_unchanged`
- `route_override_reason`
- `strategy_conflicts`

### Computed In Packet

下面这些字段应在 task packet 层生成，而不是直接从前两层照搬：

- `packet_readiness`
- `packet_lineage`

## Packet Variants

task packet 不是只有一种形态，至少要覆盖下面三类。

### 1. Fresh Packet

适用于：

- 首次生成
- 上下文清楚
- 当前重点是进入 prompt assembly

特点：

- `repair_scope` 为空
- `keep_unchanged` 通常为空

### 2. Repair Packet

适用于：

- 已有上一版结果
- 当前重点是修正而不是重新探索

特点：

- `task_mode = repair_iteration`
- `route = repair`
- `repair_scope` 必须明确
- `keep_unchanged` 必须明确

### 3. Delivery Packet

适用于：

- 主视觉已基本过线
- 当前重点转向文字、二维码、尺寸、导出版本

特点：

- `task_mode = delivery_refinement`
- `delivery_involvement = image-plus-delivery-ops`


## Packet Readiness Rules

### `ready`

可以判为 `ready`，当且仅当下面大部分都成立：

- 交付目标明确
- 使用位置明确
- 上下文边界明确
- 策略选择明确
- 缺失关键字段为空或接近为空
- 不需要额外补问才能做高质量输出

### `needs_brief`

满足下面任一项时，优先判为 `needs_brief`：

- 用途或资产类型仍模糊
- 成功标准不清楚
- 固定文本 / 固定元素要求不清楚
- 场景画像或 route 仍不稳

### `blocked`

满足下面任一项时，可判为 `blocked`：

- 用户目标本身冲突
- 上下文严重不足，且无法通过 1 到 3 个问题补齐
- 风险高，但关键信息长期缺失

## Packet Template

```yaml
request:
  user_raw_request: ""
  source_materials: []
  reference_assets: []

requirement:
  user_goal: ""
  asset_type: ""
  usage_context: ""
  requirement_summary: ""
  success_criteria: []

context:
  context_summary: ""
  background_context: ""
  brand_or_product_sources: []
  target_audience: ""
  must_avoid: []

constraints:
  fixed_text: []
  fixed_elements: []
  size_and_delivery_constraints: []
  direct_output_vs_post_process: "undecided"

strategy:
  domain_direction: ""
  matched_profile: ""
  support_tier: "standard"
  profile_confidence: "medium"
  generalization_strategy: ""
  legacy_use_case: ""
  task_mode: ""
  route: ""
  candidate_mode: ""
  output_mode: ""
  delivery_involvement: ""
  strategy_reasoning: []
  question_budget: 0
  repair_scope: ""
  keep_unchanged: []
  route_override_reason: ""
  strategy_conflicts: []

readiness:
  packet_lineage:
    intake_ref: ""
    strategy_ref: ""
    packet_version: 1
  open_questions: []
  missing_critical_fields: []
  intake_confidence: "medium"
  packet_readiness: "needs_brief"
```

## Example

```yaml
request:
  user_raw_request: "帮我给 ai-native-loop 做一张介绍 skill 的宣传图。"
  source_materials: []
  reference_assets: []

requirement:
  user_goal: "为项目介绍页和社媒发布准备一张可继续排版的主视觉。"
  asset_type: "project hero"
  usage_context: "docs / landing page / social announcement"
  requirement_summary: "需要一张更像真实项目物料的 hero 图，能体现 ai-native-loop 的协议闭环和 runtime memory 特征。"
  success_criteria:
    - "更像真实项目物料，而不是抽象概念图"
    - "需要能安全叠加后续中文标题"
    - "至少达到可对外展示的高质量草稿"

context:
  context_summary: "ai-native-loop 是协议型 workflow skill，核心语义是 input-execution-feedback-reinput loop、multi-agent collaboration、runtime capture 和经验复利。"
  background_context: "服务于已有项目 ai-native-loop，而不是纯概念视觉。"
  brand_or_product_sources:
    - "<related-project>/README.md"
    - "<related-project>/SKILL.md"
  target_audience: "会第一次接触这个 skill 的开发者和 AI-native workflow 用户"
  must_avoid:
    - "generic AI poster"
    - "excessive glow"
    - "dense baked-in English text"

constraints:
  fixed_text: []
  fixed_elements: []
  size_and_delivery_constraints:
    - "16:9 hero"
    - "需要预留后续中文标题区域"
  direct_output_vs_post_process: "visual_base_plus_post"

strategy:
  domain_direction: "project hero for an AI workflow skill"
  matched_profile: "social-creative"
  support_tier: "accelerated"
  profile_confidence: "high"
  generalization_strategy: "Use the validated social-creative profile as the primary accelerator while preserving project-specific protocol cues."
  legacy_use_case: "social-creative"
  task_mode: "fresh_generation"
  route: "direct"
  candidate_mode: "single-output"
  output_mode: "visual-base-plus-post"
  delivery_involvement: "image-only"
  strategy_reasoning:
    - "用途、资产类型和上下文都已经足够明确。"
    - "这是高价值项目 hero 图，后续需要中文标题落位，因此更适合先做视觉底图。"
  question_budget: 0
  repair_scope: ""
  keep_unchanged: []
  route_override_reason: ""
  strategy_conflicts: []

readiness:
  packet_lineage:
    intake_ref: "references/intake-schema.md"
    strategy_ref: "references/strategy-decision-tree.md"
    packet_version: 1
  open_questions: []
  missing_critical_fields: []
  intake_confidence: "high"
  packet_readiness: "ready"
```

## Repair Example

```yaml
request:
  user_raw_request: "上一版太像抽象概念图了，帮我修成更像真实项目 hero。"
  source_materials:
    - "/path/to/v1.png"
  reference_assets: []

requirement:
  user_goal: "把已有项目 hero 图修成更像真实项目介绍物料的版本。"
  asset_type: "project hero"
  usage_context: "docs / landing page / social announcement"
  requirement_summary: "保留原有整体气质，但让图像更像真实项目宣传资产，而不是抽象概念主视觉。"
  success_criteria:
    - "主体更像真实项目 hero"
    - "减少自带文本"
    - "保留后续中文标题落位空间"

context:
  context_summary: "当前任务基于已有第一版生成结果做修正，不是重新探索方向。"
  background_context: "服务于 ai-native-loop 项目。"
  brand_or_product_sources: []
  target_audience: "第一次接触项目的开发者和 workflow 用户"
  must_avoid:
    - "abstract concept-board feel"
    - "dense baked-in English text"

constraints:
  fixed_text: []
  fixed_elements: []
  size_and_delivery_constraints:
    - "16:9 hero"
  direct_output_vs_post_process: "visual_base_plus_post"

strategy:
  domain_direction: "project hero repair for an AI workflow skill"
  matched_profile: "social-creative"
  support_tier: "accelerated"
  profile_confidence: "high"
  generalization_strategy: "Stay inside the validated hero/promo profile and narrow the repair scope instead of reopening scene classification."
  legacy_use_case: "social-creative"
  task_mode: "repair_iteration"
  route: "repair"
  candidate_mode: "single-output"
  output_mode: "visual-base-plus-post"
  delivery_involvement: "image-only"
  strategy_reasoning:
    - "已有上一版结果，当前目标是最小纠偏而不是重新探索。"
  question_budget: 0
  repair_scope: "让画面更像真实项目 hero，减少抽象概念板感和内嵌文字。"
  keep_unchanged:
    - "克制的暗色气质"
    - "协议闭环语义"
  route_override_reason: ""
  strategy_conflicts: []

readiness:
  packet_lineage:
    intake_ref: "references/intake-schema.md"
    strategy_ref: "references/strategy-decision-tree.md"
    packet_version: 2
  open_questions: []
  missing_critical_fields: []
  intake_confidence: "high"
  packet_readiness: "ready"
```

## Packet Completion Checklist

### Must Be Present

- request、requirement、context、strategy、readiness 五块都存在
- route 和 output mode 已明确
- 成功标准已明确
- `packet_lineage` 已明确
- `packet_readiness` 已明确

### Must Not Happen

- 只有 intake 字段，没有 strategy 字段
- 已经写了最终 prompt，反而没有 packet
- 明明是 repair，却没有 repair_scope
- 明明有固定元素，却没有 constraints
- 当前是第几轮 task packet 都说不清

### Safe To Hand Off When

- 下一阶段执行者不需要重新猜用户目标
- 下一阶段执行者不需要重新猜策略
- runtime 能直接保留 packet 中的大部分关键信息

## Runtime Alignment

task packet 是后续 runtime capture 最值得保留的“中间层对象”。

相比只记录 prompt 和结果，它能额外保留：

- 需求理解
- 上下文边界
- 策略选择
- readiness 判断

后续 runtime capture schema 应优先支持：

- `requirement_summary`
- `context_summary`
- `strategy`
- `packet_readiness`

## What This Document Does Not Do

这份文档不负责：

- 定义 intake 的字段语义
- 定义 strategy decision rules
- 写最终 prompt
- 写评分卡

这些内容分别属于：

- `references/intake-schema.md`
- `references/strategy-decision-tree.md`
- `references/prompt-schema.md`
- `references/scorecard.md`
