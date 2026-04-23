# Benchmark Run: upgrade-pack-round-1-real

## Purpose

这份 run 记录四层升级后的第一轮真实回归，而不是 preflight 逻辑演练。

本轮覆盖：

1. `bm_pure_visual_brand_asset`
2. `bm_low_density_text_info_visual`
3. `bm_high_fact_sensitivity_data_visual`
4. `bm_overlay_delivery_viability`

## Round Summary

| Scenario | Baseline | Candidate / Gate Result | Verdict |
|---|---:|---:|---|
| `bm_pure_visual_brand_asset` | `77.0` | `97.6` | `pass` |
| `bm_low_density_text_info_visual` | `61.0` | `91.2` | `pass` |
| `bm_high_fact_sensitivity_data_visual` | `57.8` | `85.0` | `pass` |
| `bm_overlay_delivery_viability` | `no_go / with_limits / allowed` all observed | checker + actual overlay both aligned | `pass` |

## Scenario 1. `bm_pure_visual_brand_asset`

### Scenario

- scenario_id: `bm_pure_visual_brand_asset`
- benchmark_ref: [upgrade-benchmark-pack-2026-04-23.md](./upgrade-benchmark-pack-2026-04-23.md)
- date: `2026-04-23`
- evaluator: `Codex + image2-design-director`
- domain_direction: `brand promo poster for image2-design-director`
- matched_profile: `social-creative`
- support_tier: `standard`
- prompt_family_under_test: `brand-complete-asset`
- representation_mode_under_test: `model_direct_visual`

### Input

- original_request: `给 image2-design-director 做一张品牌发布图，中文主标题只有一句“让深图更像设计团队会交付的资产”，不要数据图，不要价格，不要日期，不要二维码。`
- route: `direct`
- initial_brief: `complete_asset brand launch poster`
- factual_sensitivity: `low`
- claim_type: `visual_analogy`
- metric_definition: `none`
- as_of_date: `n/a`

### Gate Decisions

- reliability_gate_result: `visual_analogy_only`
- representation_mode: `model_direct_visual`
- viability_check_required: `false`
- expected_viability_result: `n/a`

### Comparison Setup

- strategy_under_test: `对比直接品牌感 prompt 与四层架构约束后的 complete-asset 品牌 prompt`

### baseline

- workflow: `直接让模型出带品牌氛围和标题的发布图`
- representation_mode: `model_direct_visual`
- notable_limit: `没有显式收紧文字纪律`

### candidate

- workflow: `明确 complete_asset、单标题纪律、禁止副标题和信息层`
- representation_mode: `model_direct_visual`
- notable_limit: `仍依赖模型直出中文标题工艺`

### Outputs Observed

- baseline_summary: `品牌氛围成立，主标题可读，但模型自行添加了副标题和底部信息层。`
- candidate_summary: `单标题纪律明显收紧，版式主次更像真实品牌发布成品。`
- baseline_generation_id: `ig_035338bba59d6b580169e9cf6ac86c8191b5543b91d8ea7ee5`
- candidate_generation_id: `ig_035338bba59d6b580169e9cfcba5548191abf26166c22d60c1`
- baseline_output_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9cf6ac86c8191b5543b91d8ea7ee5.png`
- candidate_output_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9cfcba5548191abf26166c22d60c1.png`
- baseline_viability_result: `n/a`
- candidate_viability_result: `n/a`

### Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `/Users/boyzcl/.codex/skills/image2-design-director/runtime/captures/2026-04-23.jsonl`
- runtime_reuse_observed: `scene= bm_pure_visual_brand_asset baseline / candidate`

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 4 | 5 | 10 | 8.0 | 10.0 | candidate 更像真正的品牌发布图 |
| asset_type_fidelity | 4 | 5 | 12 | 9.6 | 12.0 | baseline 有 concept board 倾向 |
| contract_alignment | 3 | 5 | 8 | 4.8 | 8.0 | baseline 多出未要求的信息层 |
| information_reliability | 5 | 5 | 15 | 15.0 | 15.0 | 无高事实风险 |
| representation_fit | 3 | 5 | 10 | 6.0 | 10.0 | candidate 真正守住低事实负载直出路径 |
| delivery_integrity | 3 | 4 | 12 | 7.2 | 9.6 | candidate 仍有中文字形工艺风险，但已可用 |
| completion_readiness | 4 | 5 | 8 | 6.4 | 8.0 | candidate 更接近交付成品 |
| language_alignment | 4 | 5 | 8 | 6.4 | 8.0 | candidate 只保留目标语言主标题 |
| structure_and_composition | 4 | 5 | 9 | 7.2 | 9.0 | candidate 留白更稳定 |
| asset_credibility_and_craft | 4 | 5 | 8 | 6.4 | 8.0 | candidate 更像真实品牌物料 |

### Totals

- baseline_total: `77.0`
- candidate_total: `97.6`
- baseline_result: `conditional_pass`
- candidate_result: `pass`
- misleading_risk_baseline: `low`
- misleading_risk_candidate: `low`
- hard_fail_reason_baseline: `none`
- hard_fail_reason_candidate: `none`

### Result

- what_improved: `单标题纪律、complete-asset 成品度、品牌发布感都明显提升。`
- what_did_not_improve: `中文标题仍不是完全发布级工艺，需要继续观察真实中文排字稳定性。`
- new_regression_or_risk: `none`

### Decision

- lane_verdict: `keep current direct brand lane`
- tier_expectation_met: `yes`
- scenario_followup_needed: `monitor Chinese title craft on later rounds`

## Scenario 2. `bm_low_density_text_info_visual`

### Scenario

- scenario_id: `bm_low_density_text_info_visual`
- benchmark_ref: [upgrade-benchmark-pack-2026-04-23.md](./upgrade-benchmark-pack-2026-04-23.md)
- date: `2026-04-23`
- evaluator: `Codex + image2-design-director`
- domain_direction: `feature visual for repo README and social reuse`
- matched_profile: `social-creative`
- support_tier: `standard`
- prompt_family_under_test: `limited-text feature visual`
- representation_mode_under_test: `model_visual_with_limited_text`

### Input

- original_request: `做一张 README 配套的 feature visual，图里允许一条中文主标题和一条英文 product name，不要长文案，后续可能还要适配 16:9 横版。`
- route: `direct`
- initial_brief: `README + social reusable feature visual`
- factual_sensitivity: `medium`
- claim_type: `mixed`
- metric_definition: `none`
- as_of_date: `n/a`

### Gate Decisions

- reliability_gate_result: `fact_with_disclaimer`
- representation_mode: `model_visual_with_limited_text`
- viability_check_required: `true`
- expected_viability_result: `future reuse should remain possible`

### Comparison Setup

- strategy_under_test: `对比普通 feature prompt 与 limited-text + future-crop aware 的结构化 prompt`

### baseline

- workflow: `模型直接做 README feature visual`
- representation_mode: `model_visual_with_limited_text`
- notable_limit: `没有把“只允许两处可读文本”写成硬约束`

### candidate

- workflow: `显式限制可读文字数量，并要求可横向延展构图`
- representation_mode: `model_visual_with_limited_text`
- notable_limit: `仍未进入真正的 deterministic multi-size export`

### Outputs Observed

- baseline_summary: `主标题与 product name 可读，但模型继续添加了多模块 copy 与信息条。`
- candidate_summary: `文本范围基本守住，且构图天然支持 16:9 延展。`
- baseline_generation_id: `ig_035338bba59d6b580169e9d02601b0819185bc8f295356c704`
- candidate_generation_id: `ig_035338bba59d6b580169e9d052bb2881919d82e639b65c8854`
- baseline_output_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9d02601b0819185bc8f295356c704.png`
- candidate_output_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9d052bb2881919d82e639b65c8854.png`
- baseline_viability_result: `latent risk`
- candidate_viability_result: `future reuse plausible`

### Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `/Users/boyzcl/.codex/skills/image2-design-director/runtime/captures/2026-04-23.jsonl`
- runtime_reuse_observed: `scene= bm_low_density_text_info_visual baseline / candidate`

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3 | 5 | 10 | 6.0 | 10.0 | candidate 更像 README feature asset |
| asset_type_fidelity | 4 | 5 | 12 | 9.6 | 12.0 | baseline 开始滑向信息板 |
| contract_alignment | 3 | 5 | 8 | 4.8 | 8.0 | candidate 守住“有限文字”合同 |
| information_reliability | 4 | 4 | 15 | 12.0 | 12.0 | 本任务无 exact data 风险 |
| representation_fit | 2 | 5 | 10 | 4.0 | 10.0 | candidate 对 limited-text 模式更贴合 |
| delivery_integrity | 2 | 4 | 12 | 4.8 | 9.6 | candidate 有更好的横版迁移余地 |
| completion_readiness | 3 | 5 | 8 | 4.8 | 8.0 | candidate 可直接进入 README / 社媒 |
| language_alignment | 3 | 5 | 8 | 4.8 | 8.0 | baseline 出现额外 copy zones |
| structure_and_composition | 3 | 4 | 9 | 5.4 | 7.2 | candidate 横向节奏更稳 |
| asset_credibility_and_craft | 3 | 4 | 8 | 4.8 | 6.4 | candidate 像真实产品视觉 |

### Totals

- baseline_total: `61.0`
- candidate_total: `91.2`
- baseline_result: `fail`
- candidate_result: `pass`
- misleading_risk_baseline: `low`
- misleading_risk_candidate: `low`
- hard_fail_reason_baseline: `none`
- hard_fail_reason_candidate: `none`

### Result

- what_improved: `limited-text 纪律、横向延展性、README 适配感都有明显提升。`
- what_did_not_improve: `这一轮还没有把多尺寸导出真正自动化。`
- new_regression_or_risk: `none`

### Decision

- lane_verdict: `keep model_visual_with_limited_text as preferred lane`
- tier_expectation_met: `yes`
- scenario_followup_needed: `true size adaptation should be tested in a later delivery pack`

## Scenario 3. `bm_high_fact_sensitivity_data_visual`

### Scenario

- scenario_id: `bm_high_fact_sensitivity_data_visual`
- benchmark_ref: [upgrade-benchmark-pack-2026-04-23.md](./upgrade-benchmark-pack-2026-04-23.md)
- date: `2026-04-23`
- evaluator: `Codex + image2-design-director`
- domain_direction: `data-backed crypto comparison visual`
- matched_profile: `custom`
- support_tier: `standard`
- prompt_family_under_test: `hybrid exact-value asset`
- representation_mode_under_test: `hybrid_visual_plus_deterministic_overlay`

### Input

- original_request: `做一张 1:1 的加密市场对比图，比较 BTC 和 ETH 在 2026-04-23 的美元现货价格与 7 日变化率，图里要有主视觉，但精确数字必须可信。`
- route: `direct`
- initial_brief: `exact-value crypto comparison poster`
- factual_sensitivity: `high`
- claim_type: `comparative`
- metric_definition: `BTC and ETH USD spot price plus 7-day change rate`
- as_of_date: `2026-04-23`

### Locked Source Data

- BTC: `$77,701.30`, `7D +3.7%`
- ETH: `$2,343.84`, `7D +0.5%`
- source_ref:
  - [CoinGecko BTC](https://www.coingecko.com/en/coins/bitcoin/usd)
  - [CoinGecko ETH](https://www.coingecko.com/en/coins/ethereum/usd)
- source_accessed_at: `2026-04-23`

### Gate Decisions

- reliability_gate_result: `verified_fact`
- representation_mode: `hybrid_visual_plus_deterministic_overlay`
- viability_check_required: `true`
- expected_viability_result: `overlay_allowed`

### Comparison Setup

- strategy_under_test: `对比“模型自己写精确数据”与“模型负责主视觉 + 确定性叠字承载 exact values”`

### baseline

- workflow: `模型直接生成完整对比数据海报`
- representation_mode: `model_visual_with_limited_text`
- notable_limit: `所有 exact-value layer 都由模型承担`

### candidate

- workflow: `模型先生成 text-safe comparison base，再用 bundle + overlay 脚本做 deterministic exact-value layer`
- representation_mode: `hybrid_visual_plus_deterministic_overlay`
- notable_limit: `当前 overlay 工艺仍偏 MVP`

### Outputs Observed

- baseline_summary: `主价与 7D 变化率被写出来了，但模型还自行补了市值、成交量、排行与走势图，形成高误导风险。`
- candidate_summary: `主视觉与 exact-value layer 被拆开；最终 overlay 版本保留锁定数字，且 viability gate 为绿灯。`
- baseline_generation_id: `ig_035338bba59d6b580169e9d0e994cc8191969e594153e07f29`
- candidate_generation_id: `delivery_ready_visual-v005`
- baseline_output_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9d0e994cc8191969e594153e07f29.png`
- candidate_output_ref: `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_high_fact_sensitivity_data_visual_bundle/assets/delivery_ready_visual/delivery_ready_visual-v005.png`
- baseline_viability_result: `n/a`
- candidate_viability_result: `overlay_allowed`

### Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `/Users/boyzcl/.codex/skills/image2-design-director/runtime/captures/2026-04-23.jsonl`
- runtime_reuse_observed: `scene= bm_high_fact_sensitivity_data_visual baseline / candidate_base / candidate_delivery_ready`

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 4 | 4 | 10 | 8.0 | 8.0 | 两者都尝试完成对比海报 |
| asset_type_fidelity | 4 | 4 | 12 | 9.6 | 9.6 | 形态都像数据海报 |
| contract_alignment | 3 | 5 | 8 | 4.8 | 8.0 | candidate 把“精确数字必须可信”落成了系统分工 |
| information_reliability | 1 | 5 | 15 | 3.0 | 15.0 | baseline 额外数据全未锁定 |
| representation_fit | 1 | 5 | 10 | 2.0 | 10.0 | candidate 正确进入 hybrid |
| delivery_integrity | 3 | 4 | 12 | 7.2 | 9.6 | candidate 已过 viability gate，但 overlay 工艺仍是 MVP |
| completion_readiness | 2 | 4 | 8 | 3.2 | 6.4 | baseline 因高误导风险不能算 ready |
| language_alignment | 4 | 4 | 8 | 6.4 | 6.4 | 两者语言一致 |
| structure_and_composition | 4 | 4 | 9 | 7.2 | 7.2 | candidate base 结构很稳 |
| asset_credibility_and_craft | 4 | 3 | 8 | 6.4 | 4.8 | candidate 当前输在 overlay 工艺，不输在可信性 |

### Totals

- baseline_total: `57.8`
- candidate_total: `85.0`
- baseline_result: `fail`
- candidate_result: `pass`
- misleading_risk_baseline: `high`
- misleading_risk_candidate: `low`
- hard_fail_reason_baseline: `high factual sensitivity asset still relied on model-generated exact data`
- hard_fail_reason_candidate: `none`

### Result

- what_improved: `高事实敏感任务终于不再默认靠模型写精确数字；representation layer 真正进入主链路。`
- what_did_not_improve: `overlay 工艺还没有完全达到发布级排版质量。`
- new_regression_or_risk: `none`

### Decision

- lane_verdict: `keep hybrid_visual_plus_deterministic_overlay as default exact-value lane`
- tier_expectation_met: `yes`
- scenario_followup_needed: `later rounds should improve deterministic overlay craft density and typography`

## Scenario 4. `bm_overlay_delivery_viability`

### Scenario

- scenario_id: `bm_overlay_delivery_viability`
- benchmark_ref: [upgrade-benchmark-pack-2026-04-23.md](./upgrade-benchmark-pack-2026-04-23.md)
- date: `2026-04-23`
- evaluator: `Codex + image2-design-director`
- domain_direction: `delivery refinement for event poster`
- matched_profile: `social-creative`
- support_tier: `standard`
- representation_mode_under_test: `visual_base_plus_post`

### Input

- original_request: `已有一张活动主视觉，现在要补中文主标题、日期、CTA、badge 和二维码。主体人物不能被压，右下角原本有高光氛围区。`
- route: `delivery_refinement`
- initial_brief: `overlay viability go / no-go validation on a real event-poster base`
- factual_sensitivity: `low`
- claim_type: `visual_analogy`

### Real Base Asset

- base_visual_ref: `/Users/boyzcl/.codex/generated_images/019db92d-4004-7742-a3bb-d2fc8e2728c3/ig_035338bba59d6b580169e9d32c09f48191a1a2b6967528295f.png`
- supporting_bundle_refs:
  - `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_overlay_delivery_viability_bundle`
  - `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_overlay_delivery_viability_soft_bundle`
  - `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_overlay_delivery_viability_clean_bundle`

### Case Matrix

| Case | Protected Region | Expected | Observed | Artifact |
|---|---|---|---|---|
| A hard collision | `subject_core hard` overlapping title zone | `overlay_not_allowed_regenerate` | `overlay_not_allowed_regenerate` | no output asset, command returned no-go |
| B soft collision | `ambient_glow soft` covering footer + QR zone | `overlay_allowed_with_limits` | `overlay_allowed_with_limits` | `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_overlay_delivery_viability_soft_bundle/assets/delivery_ready_visual/delivery_ready_visual-v001.png` |
| C clean overlay | `subject_core hard` isolated away from all overlay zones | `overlay_allowed` | `overlay_allowed` | `/Users/boyzcl/Documents/image2/image2-design-director/artifacts/benchmarks/2026-04-23-upgrade-pack-round-1/bm_overlay_delivery_viability_clean_bundle/assets/delivery_ready_visual/delivery_ready_visual-v001.png` |

### Key Observations

- Case A:
  - `hard_region_hits = 1`
  - `collision_risk = high`
  - `continue_overlay_or_regenerate = regenerate`
- Case B:
  - `soft_region_hits = 2`
  - `footer_band overlap_ratio_of_candidate = 0.2367`
  - `qr_zone overlap_ratio_of_candidate = 1.0`
  - `continue_overlay_or_regenerate = continue_with_limits`
- Case C:
  - `hard_region_hits = 0`
  - `soft_region_hits = 0`
  - `continue_overlay_or_regenerate = continue_overlay`

### Result

- what_passed: `go / with_limits / no_go 三种状态都在真实底图上跑通，并且与实际 overlay 结果一致。`
- what_did_not_improve: `当前 checker 仍是 box-level，而不是语义分割级。`
- new_regression_or_risk: `none`

### Decision

- lane_verdict: `keep delivery viability gate as mandatory before heavy overlay`
- tier_expectation_met: `yes`
- scenario_followup_needed: `add semantic segmentation and size-adaptation checks later`

## Regressions Found During This Real Run

### Fixed Immediately

1. `apply_delivery_overlay.py` 在没有 `qr_image` 时仍会画空白 QR panel。
2. `apply_delivery_overlay.py` 在没有 `cta_text` / `date_text` 时仍会画空白 footer band。
3. `apply_delivery_overlay.py` 的 overlay 输出文件名只有秒级时间戳；同一 bundle 快速并发 overlay 时可能撞路径。

### Files Touched

- `/Users/boyzcl/Documents/image2/image2-design-director/scripts/apply_delivery_overlay.py`

## Upgrade Verdict

- `information reliability gate`: `pass`
- `representation strategy layer`: `pass`
- `delivery viability gate`: `pass`
- `outcome accountability layer`: `pass`

## What This Round Now Proves

- 低事实负载品牌图没有被误推向 deterministic 路径，且成品感更强。
- limited-text 场景不再默认滑向“会自己长出很多字的信息板”。
- 高事实敏感任务已经出现真正的 `model base + deterministic exact-value layer` 分工。
- viability checker 不只是逻辑存在，而是能在真实底图上正确阻断 hard collision、放行 clean overlay，并对 soft collision 给出限制继续。

## Next Action

- keep: `四层主链路`
- change_next: `提升 deterministic overlay 的版式工艺，并把 size adaptation 纳入下一轮真实 benchmark`
