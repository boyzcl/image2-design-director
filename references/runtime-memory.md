# Runtime Memory

## Goal

让这个 skill 的经验不只记录“生成了什么图”，还记录：

- 为什么这轮信息被判定为可信或不可可信
- 为什么选择了这种 representation mode
- 为什么某一版还能继续交付，或必须回退
- 最终失败属于哪一层

## Layering Principle

- `repo`
  - 规则、模板、脚本、正式 references
- `host-installed copy`
  - 宿主真正加载的 skill 快照
- `runtime`
  - 本地经验、捕获、review、晋升

runtime 承接经验，不承接规则主副本编辑。

## Runtime Should Now Capture Four Layers

### 1. Scene Profile

- `domain_direction`
- `matched_profile`
- `support_tier`

### 2. Asset Contract

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

### 3. Information + Representation

- `factual_sensitivity`
- `claim_type`
- `evidence_requirement`
- `metric_definition`
- `as_of_date`
- `uncertainty_policy`
- `reliability_gate_result`
- `representation_mode`
- `primary_expression_system`
- `deterministic_render_needed`
- `text_generation_tolerance`
- `numeric_render_strategy`

### 4. Delivery + Accountability

- `delivery_viability_result`
- `collision_risk`
- `continue_overlay_or_regenerate`
- `information_reliability_score`
- `delivery_integrity_score`
- `misleading_risk`
- `hard_fail_reason`

## Capture Minimum Fields

建议 capture 至少包含：

- `schema_version`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
- 资产合同字段
- 信息与 representation 字段
- `route`
- `initial_brief`
- `final_prompt`
- `image_prompt`
- `image_generation_id`
- `image_output_paths`
- `result_status`
- `evaluation_summary`
- `failure_class`
- `promotion_hint`

推荐补充：

- `contract_alignment_result`
- `completion_readiness_result`
- `repair_class`
- `delivery_viability_result`
- `collision_risk`
- `information_reliability_score`
- `delivery_integrity_score`
- `misleading_risk`
- `hard_fail_reason`
- `score`

## Why This Matters

runtime 现在至少应能回答：

1. 这轮为什么被判成事实敏感或非事实敏感
2. 当时锁定的 metric 和日期是什么
3. 为什么选择了当前 representation mode
4. 为什么某一版 overlay 被允许或被拦下
5. 失败到底是 contract、reliability、representation 还是 viability failure

## Review And Field Notes Should Carry The Same Spine

review queue 与 field note 不应只保留结果摘要，也应尽量带上：

- `deliverable_type`
- `factual_sensitivity`
- `representation_mode`
- `delivery_viability_result`
- `misleading_risk`

否则 accountability 只停留在原始 capture，无法进入经验沉淀。
