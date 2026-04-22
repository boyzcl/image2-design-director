# Benchmark Run: delivery-heavy-event-signup-poster

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_delivery_heavy_event_signup_poster`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `event signup poster base for an AI image prompt clinic`
- matched_profile: `custom`
- support_tier: `standard`
- legacy_use_case: `social-creative`
- prompt_family_under_test: `delivery-aware launch poster`
- text_layer_mode_under_test: `text_safe_only`

## Input

- original_request: 为一个 AI image prompt clinic 生成 square 报名海报底图，后续必须承载主标题、日期、CTA、二维码、logo，并要适配多尺寸。
- route: `direct`
- initial_brief: `Create a square event signup poster base for an AI image prompt clinic that will later need title, date, CTA, QR, logo, and multiple output sizes.`

## Comparison Setup

- strategy_under_test: 验证当前 skill 是否已经能稳定产出真正可进入 delivery ops 的 `text_safe_visual`，而不是只产出“看起来不错”的 `raw_visual`。

### baseline

- prompt_or_workflow: generic event poster base
- prompt_family: launch-poster baseline
- text_layer_mode: `none`
- assembly_ref: ad hoc baseline
- notable_limit: 视觉方向对，但 delivery zones 没被显式规划，后续固定元素与多尺寸会高风险冲突。

```text
Square event signup poster base for an AI image prompt clinic. Bold product-marketing atmosphere with one central abstract protocol-native visual, energetic but clean composition, bright warm background, slate blue and warm sand palette. Make it feel like a premium launch poster. No rendered text required. No readable labels. No fake QR code. No explicit logo. No classroom board, no dashboard screenshot, no scenic image.
```

### candidate

- prompt_or_workflow: delivery-aware text-safe poster base
- prompt_family: delivery-aware launch poster
- text_layer_mode: `text_safe_only`
- assembly_ref: `references/delivery-ops.md` + `references/text-overlay-policy.md` + `references/fixed-element-placement.md`
- version: `m11 delivery-heavy candidate`

```text
Square text-safe event signup poster base for an AI image prompt clinic. This image is meant to become a delivery-ready poster after precise text and fixed-element overlay. Reserve a strong clean top title zone, a quiet bottom-right QR-code zone with high-contrast empty space, a small stable top-left logo zone, and a bottom band that can hold date plus CTA without fighting the main visual. Keep one central protocol-native transformation motif built from brief packet fragments, route lines, score dots, and one improved neutral asset preview. Bright editorial background, warm paper texture, slate blue plus muted sand palette, premium campaign feel, no rendered text, no fake QR code, no fake logo, no readable labels, no classroom board, no dashboard UI, no scenic imagery.
```

## Outputs Observed

- baseline_summary: baseline 是一张可评估 `raw_visual`，海报感足够，但没有可靠 QR quiet zone、logo zone 和 CTA/date band。
- candidate_summary: candidate 已是明确的 `text_safe_visual`，logo、QR、CTA/date 的承载区都长出来了，但仍未进入真正的 `delivery_ready_visual`。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_057700bfd1e6d5040169e8e3b3794c819195fdb61ff5eba125`
- candidate_generation_id: `ig_057700bfd1e6d5040169e8e52fcf188191aaf038f639f75889`
- baseline_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e3b3794c819195fdb61ff5eba125.png`
- candidate_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e52fcf188191aaf038f639f75889.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: delivery-heavy baseline / candidate 已写入 runtime，可直接用于 delivery-layer friction 聚合。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3.5 | 4.5 | 20 | 14.0 | 18.0 | candidate 更符合“报名海报底图”，而不是只是一张视觉海报 |
| product_native_fit | 4.0 | 4.0 | 15 | 12.0 | 12.0 | 两版都像项目系统自己的 poster base |
| structure_and_composition | 3.5 | 4.5 | 15 | 10.5 | 13.5 | candidate 明显把 delivery zones 纳入构图本体 |
| asset_credibility | 3.5 | 4.0 | 15 | 10.5 | 12.0 | candidate 作为 text-safe base 很可信，但还不能算最终成品 |
| text_and_layout_fidelity | 2.5 | 4.5 | 10 | 5.0 | 9.0 | baseline 没给后续叠字留足 structure，candidate 已显式规划 |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 两版工艺都干净 |
| anti_ai_artifact | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 两版都没有明显 AI 杂讯 |
| iteration_clarity | 3.0 | 5.0 | 5 | 3.0 | 5.0 | candidate 已非常明确：下一步是 overlay + size adaptation，而不是继续盲目重生成 |

### Totals

- baseline_total: `71.0`
- candidate_total: `85.5`
- baseline_result: `fail`
- candidate_result: `pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Delivery State Judgment

- baseline_delivery_state: `raw_visual`
- candidate_delivery_state: `text_safe_visual`
- candidate_can_be_called_delivery_ready_now: `no`
- blocking_items_for_delivery_ready:
  - precise title/date/CTA overlay not applied
  - QR code not yet inserted as a real functional element
  - logo not yet inserted as a real identity element
  - crop-aware size variants not yet produced

## Result

- what_improved: candidate 首次把 delivery-critical zones 变成构图内建的一部分，而不是交付阶段临时找地方塞。
- what_did_not_improve: 当前链路还不能低摩擦地把 `text_safe_visual` 自动推进成 `delivery_ready_visual`。
- new_regression_or_risk: 如果没有版本化与 overlay 工具化，这类任务很容易在交付阶段重新破坏已经成立的主视觉。

## Decision

- pass / conditional_pass / fail: `pass`
- lane_verdict: `delivery-heavy validation succeeded`
- tier_expectation_met: `yes`
- scenario_followup_needed: `yes`

## Next Action

- keep: `top title zone + top-left logo zone + bottom-right QR quiet zone + bottom CTA/date band` 这一组 delivery-aware reserved zones 应保留。
- change_next: 下一步默认不再是继续生成，而是进入 delivery ops，把 `raw_visual / text_safe_visual / delivery_ready_visual` 版本化，并补 fixed-element overlay 与 size adaptation。
