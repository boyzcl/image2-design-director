# Task Packet

## Purpose

这份文档定义 `image2-design-director` 在进入 prompt assembly 或确定性渲染之前的统一任务包格式。

一句话版本：

> task packet 不是“需求摘要”，而是一份可执行的任务说明书，必须同时携带资产合同、信息合同、表达机制决定、交付 gate 要求，以及后续可追责的判断依据。

## Position In The Loop

task packet 位于：

1. `Requirement Intake`
2. `Asset Contract Lock`
3. `Information Reliability Gate`
4. `Representation Strategy Selection`

之后服务于：

- `Prompt / Render Assembly`
- `Evaluation And Scoring`
- `Delivery Viability Gate`
- runtime capture

## Packet Structure

一个完整 packet 由 8 个区块组成。

### 1. Request Block

保留原始输入，不做解释性改写。

必含：

- `user_raw_request`

按需补充：

- `source_materials`
- `reference_assets`
- `existing_generation_context`

### 2. Requirement Block

回答“这轮最终要交付什么”。

必含：

- `user_goal`
- `deliverable_type`
- `usage_context`
- `requirement_summary`
- `success_criteria`

### 3. Asset Contract Block

回答“这轮要交成什么状态的资产”。

必含：

- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

按需补充：

- `contract_risks`
- `language_override_reason`
- `completion_override_reason`

### 4. Information Reliability Block

回答“图里承载的信息是否可信，以及在什么边界内表达”。

必含：

- `factual_sensitivity`
- `claim_type`
- `evidence_requirement`
- `metric_definition`
- `uncertainty_policy`
- `reliability_gate_result`

按需补充：

- `as_of_date`
- `secondary_metrics`
- `evidence_sources`
- `information_risks`

### 5. Representation Block

回答“这轮信息应该由哪种表达机制承载”。

必含：

- `representation_mode`
- `primary_expression_system`
- `deterministic_render_needed`
- `text_generation_tolerance`
- `numeric_render_strategy`
- `representation_reasoning`

按需补充：

- `prompt_family`
- `deterministic_render_spec`
- `representation_fallback`

### 6. Delivery Block

回答“这轮交付怎么落，以及之后需不需要 viability gate”。

必含：

- `output_mode`
- `delivery_involvement`
- `viability_check_required`
- `allowed_overlay_classes`

按需补充：

- `fixed_text`
- `fixed_elements`
- `size_and_delivery_constraints`
- `protected_regions`
- `reserved_zones`
- `delivery_plan_notes`

### 7. Strategy Block

回答“这轮决定怎么跑”。

必含：

- `domain_direction`
- `support_tier`
- `task_mode`
- `route`
- `candidate_mode`
- `strategy_reasoning`

按需补充：

- `matched_profile`
- `profile_confidence`
- `legacy_use_case`
- `question_budget`
- `repair_class`
- `repair_scope`
- `keep_unchanged`
- `route_override_reason`
- `strategy_conflicts`

### 8. Readiness And Accountability Block

回答“是否可以进入下一阶段，以及后续按什么维度追责”。

必含：

- `packet_lineage`
- `open_questions`
- `missing_critical_fields`
- `intake_confidence`
- `packet_readiness`
- `evaluation_focus`

推荐值：

- `ready`
- `needs_brief`
- `blocked`

## Packet Design Rules

### 1. Preserve The Boundary Between Raw And Interpreted

必须同时保留：

- 原始请求
- 结构化判断

### 2. Information Contract Must Stay Explicit

packet 不能只说“要做什么图”，还必须说清：

- 关键信息是不是事实表达
- 证据强度够不够
- 允许的日期和 metric 口径是什么
- 如果不能验证，应如何降级

### 3. Representation Strategy Must Stay Explicit

packet 必须明确：

- 这轮主要靠模型直出、后置、确定性渲染还是混合路径

否则 prompt、overlay、scorecard 会继续各猜一次。

### 4. Delivery Viability Is A Formal Handoff Requirement

如果后续要叠字、放 QR、放 logo、放价格或图表，packet 必须显式说明：

- `viability_check_required`
- `allowed_overlay_classes`
- `protected_regions`

### 5. Keep Prompt Out Of The Packet

task packet 服务于 prompt 或 render spec，但自身不是最终 prompt。

## Minimum Packet Contract

| Block | Field | Required |
|---|---|---|
| request | `user_raw_request` | yes |
| requirement | `user_goal` | yes |
| requirement | `deliverable_type` | yes |
| requirement | `usage_context` | yes |
| requirement | `requirement_summary` | yes |
| requirement | `success_criteria` | yes |
| asset_contract | `asset_completion_mode` | yes |
| asset_contract | `content_language` | yes |
| asset_contract | `allowed_text_scope` | yes |
| asset_contract | `layout_owner` | yes |
| asset_contract | `acceptance_bar` | yes |
| information | `factual_sensitivity` | yes |
| information | `claim_type` | yes |
| information | `evidence_requirement` | yes |
| information | `metric_definition` | yes |
| information | `uncertainty_policy` | yes |
| information | `reliability_gate_result` | yes |
| representation | `representation_mode` | yes |
| representation | `primary_expression_system` | yes |
| representation | `deterministic_render_needed` | yes |
| representation | `text_generation_tolerance` | yes |
| representation | `numeric_render_strategy` | yes |
| delivery | `output_mode` | yes |
| delivery | `delivery_involvement` | yes |
| delivery | `viability_check_required` | yes |
| delivery | `allowed_overlay_classes` | yes |
| strategy | `domain_direction` | yes |
| strategy | `support_tier` | yes |
| strategy | `task_mode` | yes |
| strategy | `route` | yes |
| strategy | `candidate_mode` | yes |
| strategy | `strategy_reasoning` | yes |
| readiness | `packet_lineage` | yes |
| readiness | `open_questions` | yes |
| readiness | `missing_critical_fields` | yes |
| readiness | `intake_confidence` | yes |
| readiness | `packet_readiness` | yes |
| readiness | `evaluation_focus` | yes |

## Packet Readiness Rules

- `ready`
  - 资产合同已锁定，reliability gate 已给出可执行结果，representation mode 已明确
- `needs_brief`
  - 仍缺 1 到 3 个高杠杆字段
- `blocked`
  - 事实敏感任务无证据、核心 metric 未定义、或 delivery 约束缺失到无法继续

## Assembly Notes

### From Intake

原则上直接继承：

- 原始请求和素材
- 资产合同字段
- 信息合同字段
- delivery 约束字段
- `open_questions`
- `missing_critical_fields`
- `intake_confidence`

### From Strategy

原则上直接继承：

- `reliability_gate_result`
- `representation_mode`
- `output_mode`
- `viability_check_required`
- `route`
- `candidate_mode`
- `strategy_reasoning`

## Accountability Reminder

任何准备进入执行的 packet，都应能回答下面 4 个问题：

1. 这轮信息为什么可信，或为什么只允许做视觉隐喻
2. 为什么选择这种表达机制
3. 如果后续要 overlay，靠什么判断还能不能继续交付
4. 最终不过线时，失败会落在哪一层
