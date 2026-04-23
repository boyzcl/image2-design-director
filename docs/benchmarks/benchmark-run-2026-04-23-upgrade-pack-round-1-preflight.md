# Benchmark Run: upgrade-pack-round-1-preflight

## Scope

- benchmark_ref: `docs/benchmarks/upgrade-benchmark-pack-2026-04-23.md`
- date: `2026-04-23`
- evaluator: `Codex`
- run_type: `preflight regression`
- note:
  - 这是一轮首轮回归启动记录，当前优先验证 gate、representation 选择与 overlay checker 行为。
  - 本轮不宣称已经完成真实出图质量 benchmark。
  - 真实 visual benchmark 下一轮再补。

## Method

本轮分成两部分：

1. `decision-layer regression`
   - 检查 3 个非 overlay 场景是否走对 `reliability gate` 和 `representation mode`
2. `tooling regression`
   - 对 `bm_overlay_delivery_viability` 直接执行 checker，验证 `allowed / with_limits / no_go`

## Summary

| Scenario ID | What Was Checked | Expected | Observed | Verdict |
|---|---|---|---|---|
| `bm_pure_visual_brand_asset` | 低事实负载任务的 gate 与 representation | 不被推向 deterministic | `visual_analogy_only` + `model_direct_visual` | `pass` |
| `bm_low_density_text_info_visual` | 有限文字直出 / 轻后置策略 | limited text 或 base+post | `fact_with_disclaimer` + `model_visual_with_limited_text` | `pass` |
| `bm_high_fact_sensitivity_data_visual` | 高事实敏感任务的路由 | hybrid 或 deterministic | `verified_fact` + `hybrid_visual_plus_deterministic_overlay` | `pass` |
| `bm_overlay_delivery_viability` | overlay viability checker | 能区分 go / with_limits / no_go | 三种状态均触发 | `pass` |

## Scenario 1. `bm_pure_visual_brand_asset`

### Input

- original_request:
  - “给 image2-design-director 做一张品牌发布图，中文主标题只有一句‘让深图更像设计团队会交付的资产’，不要数据图，不要价格，不要日期，不要二维码。”
- route_under_test: `direct`
- domain_direction: `brand promo poster for image2-design-director`
- matched_profile: `social-creative`
- support_tier: `standard`

### Expected Gate Decisions

- `factual_sensitivity = low`
- `reliability_gate_result = visual_analogy_only` 或低风险直接放行
- `representation_mode = model_direct_visual`
- `viability_check_required = false`

### Observed Decision

- `factual_sensitivity = low`
- `claim_type = visual_analogy`
- `reliability_gate_result = visual_analogy_only`
- `representation_mode = model_direct_visual`
- `primary_expression_system = image_model`
- `viability_check_required = false`

### Result

- what_passed:
  - 新架构没有把低事实负载品牌图误推向 deterministic 或 hybrid。
  - brand asset 仍然保持 complete-asset 优先。
- residual_risk:
  - 真实 visual run 还需验证中文短标题直出质量。
- verdict:
  - `pass`

## Scenario 2. `bm_low_density_text_info_visual`

### Input

- original_request:
  - “做一张 README 配套的 feature visual，图里允许一条中文主标题和一条英文 product name，不要长文案，后续可能还要适配 16:9 横版。”
- route_under_test: `direct`
- domain_direction: `feature visual for repo README and social reuse`
- matched_profile: `social-creative`
- support_tier: `standard`

### Expected Gate Decisions

- `factual_sensitivity = low` 或 `medium`
- `representation_mode = model_visual_with_limited_text` 或 `visual_base_plus_post`
- `language_alignment`、`completion_readiness` 不应回退

### Observed Decision

- `factual_sensitivity = medium`
- `claim_type = mixed`
- `reliability_gate_result = fact_with_disclaimer`
- `representation_mode = model_visual_with_limited_text`
- `text_generation_tolerance = headline_only`
- `numeric_render_strategy = omit_numeric_claims`
- `viability_check_required = true`

### Result

- what_passed:
  - 系统没有把“有限标题”任务自动推成纯 text-safe base。
  - 同时识别到未来有横版复用，保留了 viability gate 依赖。
- residual_risk:
  - 下一轮 visual run 需要验证 limited-text 直出与横版适配是否真的稳定。
- verdict:
  - `pass`

## Scenario 3. `bm_high_fact_sensitivity_data_visual`

### Input

- original_request:
  - “做一张 1:1 的加密市场对比图，比较 BTC 和 ETH 在 2026-04-23 的美元现货价格与 7 日变化率，图里要有主视觉，但精确数字必须可信。”
- route_under_test: `direct`
- domain_direction: `data-backed crypto comparison visual`
- matched_profile: `custom`
- support_tier: `standard`

### Expected Gate Decisions

- `factual_sensitivity = high`
- `reliability_gate_result != visual_analogy_only`
- `representation_mode = hybrid_visual_plus_deterministic_overlay` 或 `deterministic_render`

### Observed Decision

- `factual_sensitivity = high`
- `claim_type = comparative`
- `metric_definition = BTC and ETH USD spot price plus 7-day change rate`
- `as_of_date = 2026-04-23`
- `evidence_requirement = exact_value_lock`
- `reliability_gate_result = verified_fact`
- `representation_mode = hybrid_visual_plus_deterministic_overlay`
- `primary_expression_system = hybrid`
- `numeric_render_strategy = deterministic_chart`

### Result

- what_passed:
  - 高事实敏感任务不再默认靠模型写精确数字。
  - representation 层正确把主视觉与 exact-value layer 拆开。
- residual_risk:
  - 下一轮需要真实接一次数据源与 deterministic render，验证 end-to-end 链路。
- verdict:
  - `pass`

## Scenario 4. `bm_overlay_delivery_viability`

### Input

- original_request:
  - “已有一张活动主视觉，现在要补中文主标题、日期、CTA、badge 和二维码。主体人物不能被压，右下角原本有高光氛围区。”
- route_under_test: `delivery_refinement`
- domain_direction: `delivery refinement for event poster`
- matched_profile: `social-creative`
- support_tier: `standard`

### Tool Runs

直接调用 `delivery_viability_lib.evaluate_delivery_viability` 做 3 组检查：

#### Case A. Hard Collision

- candidate:
  - `title_panel`
- protected_region:
  - `subject_core (hard)`
- observed:
  - `delivery_viability = overlay_not_allowed_regenerate`
  - `collision_risk = high`
  - `continue_overlay_or_regenerate = regenerate`

#### Case B. Soft Collision

- candidate:
  - `footer_band`
- protected_region:
  - `ambient_glow (soft)`
- observed:
  - `delivery_viability = overlay_allowed_with_limits`
  - `collision_risk = medium`
  - `continue_overlay_or_regenerate = continue_with_limits`

#### Case C. Clean Overlay

- candidate:
  - `badge_zone`
- protected_region:
  - `subject_core (hard)`
- observed:
  - `delivery_viability = overlay_allowed`
  - `collision_risk = low`
  - `continue_overlay_or_regenerate = continue_overlay`

### Result

- what_passed:
  - checker 已经能稳定区分 `go / with_limits / no_go`
  - 硬保护区碰撞会被直接拦下
  - 软碰撞不会误判成完全失败，但会要求限缩
- residual_risk:
  - 当前还没有语义分割、字号下限和多尺寸 crop 复核
- verdict:
  - `pass`

## Upgrade-Package Verdict

- `information reliability gate`: `pass`
- `representation strategy`: `pass`
- `delivery viability gate`: `pass`
- `outcome accountability`: `pass on schema and evaluation surface`

## What This Round Proves

- 四层架构已经进入主决策链路，而不是停在文档口号。
- 高事实敏感任务与低事实负载任务已经出现明确分流。
- overlay checker 已经具备最小可用拦截能力。

## What Is Still Pending

- 真实 Image generation visual run
- hybrid path 的真实 deterministic overlay 验证
- scorecard 在真实输出图上的完整打分

## Next Action

- 先执行一轮真实 visual benchmark：
  - `bm_pure_visual_brand_asset`
  - `bm_high_fact_sensitivity_data_visual`
  - `bm_overlay_delivery_viability`
- 再把本轮 preflight judgment 补成完整 benchmark run 与 runtime capture
