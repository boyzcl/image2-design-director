# Runtime Schema V2

## Purpose

这份文档把 `image2-design-director` 当前 runtime capture / review / field note 的主字段正式收成 `schema v2`。

它要解决的不是“多几个字段”，而是让 scene generalization 之后的判断链条不再在 runtime 层断掉。

一句话版本：

> v2 的核心变化，是让 runtime 正式承接 `domain_direction + matched_profile + support_tier`，并把 `legacy_use_case` 降为兼容字段。

## Why V2 Exists

在 `m8_scene_generalization_and_portability` 之后，repo 层已经改成：

- `domain_direction`
- `matched_profile`
- `support_tier`

但如果 runtime 还只留下旧 `use_case`，就会出现 3 个问题：

1. benchmark 与 runtime 无法对齐
2. review / field note 无法区分“新场景探索”与“成熟档案复用”
3. profile 晋升无法建立在真实 capture 之上

## Canonical Entities

runtime v2 主要涉及 3 类记录：

1. `capture`
2. `review item`
3. `field note`

`repo candidate` 仍沿用 field note 的核心字段，再加回流判断即可。

## Shared Taxonomy Fields

下面这组字段在 v2 中被视为 scene-profile 主字段：

- `domain_direction`
- `matched_profile`
- `support_tier`

兼容字段：

- `legacy_use_case`

兼容规则：

- 新记录应优先写主字段
- 如果旧链路仍只提供 `use_case`，应把它映射到 `legacy_use_case`
- `legacy_use_case` 不能再替代主字段做新规则判断

## Capture Schema

### Required

- `schema_version`
- `timestamp`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
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

### Compatibility

- `legacy_use_case`
- `use_case`

如果旧记录只有 `use_case`，运行时应尽量补：

- `legacy_use_case = use_case`
- `matched_profile`
- `support_tier`

默认迁移策略应保守：

- 能确定只是在沿用旧四档案时，可把 `matched_profile` 补成对应档案
- `support_tier` 默认降一档按 `standard` 处理，直到有新的 review / benchmark 支撑

## Review Item Schema

review queue 中的每个条目至少应保留：

- `capture_file`
- `session_id`
- `scene`
- `schema_version`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `legacy_use_case`
- `promotion_hint`
- `timestamp`

目的不是重复 capture，而是让 review 阶段一眼知道：

- 这是成熟档案的回归问题
- 还是新场景的 exploratory 样本

## Field Note Schema

field note 至少应包含：

- `session_id`
- `schema_version`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `legacy_use_case`
- `route`
- `failure_class`
- `what_worked`
- `what_failed`
- `correction_rule`
- `next_input`

field note 不要求携带全部生成细节，但必须能回答：

1. 这是哪类场景
2. 当时命中了什么档案或没命中
3. 当前支持层级是什么
4. 主要 failure / intervention / next input 是什么

## Normalization Rules

### `matched_profile`

推荐值：

- `product-mockup`
- `social-creative`
- `ui-mockup`
- `app-asset`
- `custom`
- `none`

### `support_tier`

只使用：

- `accelerated`
- `standard`
- `exploratory`

不要把 host 支持层级和 scene 支持层级混写在一起。

### `legacy_use_case`

仅用于：

- 旧 capture 迁移
- 旧 benchmark / experiment 对照
- 回看旧链路时的语义映射

不要再用它作为新 benchmark、promotion 或 prompt 规则的主入口。

## Implementation Notes

当前 repo 的最小落地要求是：

1. capture 写入时自动补 `schema_version`
2. review queue 保留 scene-profile 主字段
3. field note 渲染保留 scene-profile 主字段
4. runtime context 查询支持按主字段过滤

## Relationship To Other Docs

- runtime 总说明：`references/runtime-memory.md`
- 晋升规则：`references/promotion-governance.md`
- profile 晋升：`docs/profile-promotion-policy.md`
- sync 边界：`docs/repo-installed-runtime-sync-contract.md`
