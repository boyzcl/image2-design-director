# Runtime Memory

## Goal

让这个 skill 的经验不只记录“生成了什么图”，还记录：

- 为什么这轮信息被判定为可信或不可可信
- 为什么选择了这种 representation mode
- 为什么某一版还能继续交付，或必须回退
- 为什么某一版不能升格为 publication asset
- 最终失败属于哪一层

## Layering Principle

- `repo`
  - 规则、模板、脚本、正式 references
- `host-installed copy`
  - 宿主真正加载的 skill 快照
- `runtime`
  - 本地经验、捕获、review、晋升

runtime 承接经验，不承接规则主副本编辑。

## Runtime Should Now Capture Five Layers

### 1. Scene Profile

- `domain_direction`
- `matched_profile`
- `support_tier`
- `usage_context`

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

### 4. Delivery + Publication Identity

- `delivery_viability_result`
- `collision_risk`
- `continue_overlay_or_regenerate`
- `protected_regions`
- `artifact_role`
- `asset_identity_result`
- `publication_review_result`
- `production_packet`
- `production_preflight_result`
- `visual_quality_review_result`
- `final_release_result`
- `publication_blockers`
- `argument_support_result`
- `cross_scene_residue_result`

### 5. Accountability

- `information_reliability_score`
- `delivery_integrity_score`
- `misleading_risk`
- `hard_fail_reason`
- `score`
- `result_status`

## Capture Minimum Fields

建议 capture 至少包含：

- `schema_version`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `usage_context`
- 资产合同字段
- 信息与 representation 字段
- `route`
- `initial_brief`
- `final_prompt`
- `image_prompt`
- `image_generation_id`
- `image_output_paths`
- `artifact_role`
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
- `protected_regions`
- `publication_review_result`
- `publication_blockers`
- `asset_identity_result`
- `argument_support_result`
- `cross_scene_residue_result`
- `information_reliability_score`
- `delivery_integrity_score`
- `misleading_risk`
- `hard_fail_reason`
- `score`

## Asset Role Rules

推荐把当前结果显式标成：

- `artifact_role: internal_candidate`
- `artifact_role: review_candidate`
- `artifact_role: publication_asset`

默认映射：

- `benchmark candidate`
  - `internal_candidate`
- `delivery bundle artifact`
  - `internal_candidate`
- `overlay demo`
  - `internal_candidate`
- `exploratory repair output`
  - `internal_candidate` 或 `review_candidate`

只有当下面条件同时成立时，才可登记为 `publication_asset`：

- `asset_completion_mode = complete_asset`
- `publication_review_result = pass`
- `production_preflight_result = pass`
- `visual_quality_review_result = pass`
- `final_release_result = pass`
- `cross_scene_residue_result = pass`
- 当前结果不是 benchmark / demo / repair artifact

## Why This Matters

runtime 现在至少应能回答：

1. 这轮为什么被判成事实敏感或非事实敏感
2. 当时锁定的 metric 和日期是什么
3. 为什么选择了当前 representation mode
4. 为什么某一版 overlay 被允许或被拦下
5. 为什么当前图没有被判为 `publication_asset`
6. 失败到底是 contract、reliability、representation、viability 还是 publication identity failure

## Minimal Publication Metadata Example

```json
{
  "deliverable_type": "editorial_publication_visual",
  "usage_context": "wechat article editorial publication",
  "asset_completion_mode": "complete_asset",
  "artifact_role": "publication_asset",
  "protected_regions": [
    "title_region",
    "core_subject_region",
    "focus_information_region"
  ],
  "publication_review_result": "pass",
  "publication_blockers": []
}
```

如果当前 metadata 更接近下面这样：

```json
{
  "artifact_role": "internal_candidate",
  "publication_review_result": "conditional_pass"
}
```

那它仍只能停留在内部，不得给用户，不得进入正文。

## Minimal Benchmark Surface

为文章发表资产新增最小 regression 面：

- `bm_editorial_cover_publication_asset`
  - 验证 editorial cover 能稳定交成 `publication_asset`
- `bm_mechanism_figure_publication_asset`
  - 验证机制图不会停留在 text-safe 中间态
- `bm_workflow_evidence_publication_asset`
  - 验证 workflow / evidence figure 能通过 publication review，且无跨场景残留

这些 benchmark 的目标不是只看图漂不漂亮，而是验证：

- 资产身份是否稳定
- `complete_asset` 是否真的被落实
- publication review 是否能拦住中间稿和错场景图

## Review And Field Notes Should Carry The Same Spine

review queue 与 field note 不应只保留结果摘要，也应尽量带上：

- `deliverable_type`
- `usage_context`
- `factual_sensitivity`
- `representation_mode`
- `delivery_viability_result`
- `artifact_role`
- `publication_review_result`
- `misleading_risk`

否则 accountability 只停留在原始 capture，无法进入经验沉淀。
