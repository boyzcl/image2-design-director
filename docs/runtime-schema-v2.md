# Runtime Schema V2

## Purpose

这份文档把 `image2-design-director` 当前 runtime capture / review / field note 的主字段正式收成 `schema v2`。

当前 v2 不只承接 scene profile，也应承接 asset contract 判断。

一句话版本：

> runtime 不应只记“怎么生成了图”，还应记“当时理解的交付物合同是什么，以及这份合同有没有被满足”。

## Shared Taxonomy Fields

scene-profile 主字段：

- `domain_direction`
- `matched_profile`
- `support_tier`

asset-contract 主字段：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

兼容字段：

- `legacy_use_case`

## Capture Schema

### Required

- `schema_version`
- `timestamp`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`
- `route`
- `initial_brief`
- `final_prompt`
- `image_prompt`
- `result_status`
- `evaluation_summary`

### Strongly Recommended

- `image_generation_id`
- `image_output_paths`
- `image_generation_dir`
- `failure_class`
- `what_worked`
- `what_failed`
- `correction_rule`
- `next_input`
- `promotion_hint`
- `contract_alignment_result`
- `completion_readiness_result`
- `repair_class`

## Review Item Schema

review queue 中的每个条目至少应保留：

- `capture_file`
- `session_id`
- `scene`
- `schema_version`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `promotion_hint`
- `timestamp`

## Field Note Schema

field note 至少应包含：

- `session_id`
- `schema_version`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `route`
- `failure_class`
- `what_worked`
- `what_failed`
- `correction_rule`
- `next_input`
- `repair_class`

## Normalization Rules

### `asset_completion_mode`

只使用：

- `complete_asset`
- `base_visual`
- `delivery_refinement`

### `content_language`

使用明确语言值，例如：

- `zh-CN`
- `en`

不要写模糊值：

- `same as user`

### `contract_alignment_result`

推荐值：

- `aligned`
- `partially_aligned`
- `misaligned`

### `completion_readiness_result`

推荐值：

- `ready`
- `workable_draft`
- `base_only`
- `not_ready`

## Implementation Notes

当前最小落地要求是：

1. capture 写入时保留 scene-profile 与 asset-contract 主字段
2. review queue 保留这两层字段
3. field note 渲染保留这两层字段
4. runtime context 查询后续应支持按合同字段过滤

## Relationship To Other Docs

- runtime 总说明：`references/runtime-memory.md`
- 晋升规则：`references/promotion-governance.md`
- sync 边界：`docs/repo-installed-runtime-sync-contract.md`
