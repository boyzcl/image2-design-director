# Task Packet

## Purpose

这份文档定义 `image2-design-director` 在进入 prompt assembly 之前的统一任务包格式。

它的作用不是重复 intake，也不是重复 strategy，而是把两者压成一份可以稳定执行、稳定评估、稳定留痕的统一输入。

一句话版本：

> intake 负责把需求和交付物合同收清楚，strategy 负责决定怎么跑，task packet 负责把它们压成一份可执行资产说明书。

## Position In The Loop

这个 task packet 位于：

- `Stage 1. Requirement Intake`
- `Stage 2. Strategy Selection`

之后，服务于：

- `Stage 3. Prompt Assembly And Image Generation`
- `Stage 4. Evaluation And Scoring`
- runtime capture

## Packet Structure

一个完整 task packet 由 7 个区块组成。

### 1. Request Block

保留用户原始输入。

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
- `deliverable_type`
- `usage_context`
- `requirement_summary`
- `success_criteria`

### 3. Asset Contract Block

回答“这轮要交成什么状态的资产，以及交付边界是什么”。

必须包含：

- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

按需补充：

- `contract_risks`
- `language_override_reason`
- `completion_override_reason`

### 4. Context Block

回答“这轮图像任务服务于什么语境”。

必须包含：

- `context_summary`

按需补充：

- `background_context`
- `brand_or_product_sources`
- `target_audience`
- `must_avoid`

### 5. Constraint Block

回答“这轮有哪些必须遵守的边界”。

按需包含：

- `fixed_text`
- `fixed_elements`
- `size_and_delivery_constraints`
- `direct_output_vs_post_process`

### 6. Strategy Block

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
- `repair_class`
- `repair_scope`
- `keep_unchanged`
- `route_override_reason`
- `strategy_conflicts`

### 7. Readiness Block

回答“这份任务包是否已经可以交给下一阶段”。

必须包含：

- `packet_lineage`
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

### 2. Asset Contract Must Stay Explicit

task packet 不能只留下“要做什么图”，还必须留下：

- 这是不是成品
- 文字语言是什么
- 允许哪些文字
- 由谁完成最终排版
- 怎样才算用户可验收

否则 prompt、evaluation、repair 会持续各自重新猜一次。

### 3. Keep Strategy Explicit

task packet 不能只留下内容字段，还必须把策略字段带进去。

### 4. Let Packet Readiness Control The Next Step

- `ready`: 进入 prompt assembly
- `needs_brief`: 先补 1 到 3 个高杠杆问题
- `blocked`: 当前不能继续

### 5. Keep Prompt Out Of The Packet

task packet 服务于 prompt，但 task packet 本身不是最终 prompt。

它不应包含：

- `final_prompt`
- `image_prompt`

## Minimum Packet Contract

| Block | Field | Required |
|---|---|---|
| request | `user_raw_request` | yes |
| requirement | `user_goal` | yes |
| requirement | `asset_type` | yes |
| requirement | `deliverable_type` | yes |
| requirement | `usage_context` | yes |
| requirement | `requirement_summary` | yes |
| requirement | `success_criteria` | yes |
| asset_contract | `asset_completion_mode` | yes |
| asset_contract | `content_language` | yes |
| asset_contract | `allowed_text_scope` | yes |
| asset_contract | `layout_owner` | yes |
| asset_contract | `acceptance_bar` | yes |
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

### From Intake

原则上直接继承：

- `user_raw_request`
- `source_materials`
- `reference_assets`
- `user_goal`
- `asset_type`
- `deliverable_type`
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
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `final_layout_owner`
- `acceptance_bar`
- `open_questions`
- `missing_critical_fields`
- `intake_confidence`

### From Strategy

原则上直接继承：

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
- `repair_class`
- `repair_scope`
- `keep_unchanged`
- `route_override_reason`
- `strategy_conflicts`

## Example Packet

```yaml
request:
  user_raw_request: "给这个 skill 做一张完整可用的品牌宣传图。"

requirement:
  user_goal: "产出一张可直接用于仓库宣传和公开发布的品牌海报。"
  asset_type: "brand poster"
  deliverable_type: "brand promo poster"
  usage_context: "GitHub repo / social launch / project intro"
  requirement_summary: "需要完整可用的品牌宣传海报，而不是待补字底图。"
  success_criteria:
    - "必须是可直接使用的成品海报"
    - "文字语言必须跟随当前中文会话"
    - "不能漂移成建筑、地产或材料板语义"

asset_contract:
  asset_completion_mode: "complete_asset"
  content_language: "zh-CN"
  allowed_text_scope: "only project name + one Chinese slogan + one Chinese subtitle"
  layout_owner: "model"
  acceptance_bar: "图像应作为完整品牌成品海报直接可用。"
  contract_risks:
    - "系统可能错误滑向 text-safe base"
    - "系统可能错误切到英文文案"

context:
  context_summary: "这是一个 AI design-director layer，用于把模糊图像需求推进到可交付资产。"
  must_avoid:
    - "architecture board"
    - "real-estate semantics"
    - "extra English microtext"

constraints:
  fixed_text:
    - "image2-design-director"
    - "让 Prompt 真正能交付"
    - "把模糊需求变成可用的设计资产"
  direct_output_vs_post_process: "direct_output"

strategy:
  domain_direction: "brand promo poster for an AI design-director skill"
  matched_profile: "social-creative"
  support_tier: "accelerated"
  task_mode: "fresh_generation"
  route: "direct"
  candidate_mode: "single-output"
  output_mode: "direct_output"
  delivery_involvement: "image-only"
  strategy_reasoning:
    - "用户要的是完整可用成品，不是底图。"
    - "文案语言已明确，且允许文本范围已锁定。"

readiness:
  packet_lineage:
    intake_version: "v-next"
    strategy_version: "v-next"
  open_questions: []
  missing_critical_fields: []
  intake_confidence: "high"
  packet_readiness: "ready"
```
