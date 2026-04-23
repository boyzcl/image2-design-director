# Upgrade Benchmark Pack 2026-04-23

## Purpose

这份文档定义本轮四层架构升级后的最小 benchmark surface。

目标不是覆盖所有任务，而是验证新加的 4 个能力层都真的起作用：

1. `information reliability gate`
2. `representation strategy`
3. `delivery viability gate`
4. `outcome accountability`

## Minimum Benchmark Set

### 1. `bm_pure_visual_brand_asset`

目标：

- 验证低事实负载任务不会被过度程序化

预期：

- `reliability_gate_result = visual_analogy_only` 或低风险直接放行
- `representation_mode = model_direct_visual`
- 不触发 viability gate 依赖

### 2. `bm_low_density_text_info_visual`

目标：

- 验证有限文字直出和完整资产合同是否仍稳定

预期：

- `representation_mode = model_visual_with_limited_text` 或 `visual_base_plus_post`
- scorecard 中 `language_alignment`、`completion_readiness` 不应回退

### 3. `bm_high_fact_sensitivity_data_visual`

目标：

- 验证高事实敏感任务会进入 reliability gate，并选择 hybrid 或 deterministic 路径

预期：

- `factual_sensitivity = high`
- `reliability_gate_result != visual_analogy_only`，除非明确降级
- `representation_mode = hybrid_visual_plus_deterministic_overlay` 或 `deterministic_render`

### 4. `bm_overlay_delivery_viability`

目标：

- 验证已有图进入 overlay 前会被 viability gate 检查

预期：

- 至少出现一组 `overlay_allowed_with_limits` 或 `overlay_not_allowed_regenerate`
- checker 能拦住明显 protected-region 冲突

## What Each Run Must Record

每一条 benchmark run 至少记录：

- 原始请求
- reliability gate 结果
- representation mode
- viability gate 结果
- scorecard
- `misleading_risk`
- `hard_fail_reason`

## Pass Criteria For This Upgrade

- 低事实负载品牌图没有被错误推向 deterministic 路径
- 高事实敏感任务不再默认靠模型写精确数字
- overlay checker 至少拦住一组明显冲突
- scorecard 能区分“好看但不可信”和“可信但不可用”
