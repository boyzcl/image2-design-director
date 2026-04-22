# Benchmark Run: standard-transfer-onboarding-learning-asset

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_standard_transfer_onboarding_learning_asset`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `onboarding-adjacent learning asset for a mobile AI image app`
- matched_profile: `custom`
- support_tier: `standard`
- legacy_use_case: `app-asset`
- prompt_family_under_test: `hybrid app-asset learning card`
- text_layer_mode_under_test: `safe-area-only`

## Input

- original_request: 为一个 mobile AI image app 生成 portrait onboarding-adjacent learning card，左侧预留 copy-safe 空间，不渲染最终文案。
- route: `direct`
- initial_brief: `Create a portrait onboarding-adjacent learning card for a mobile AI image app with left-side copy-safe space and no rendered text.`

## Comparison Setup

- strategy_under_test: 验证 `app-asset` 与 `protocol-native teaching motifs` 能否在不变成 dashboard mockup 的前提下，迁移成 onboarding learning asset。

### baseline

- prompt_or_workflow: generic onboarding feature card
- prompt_family: app-asset hybrid baseline
- text_layer_mode: `safe-area-only`
- assembly_ref: ad hoc baseline
- notable_limit: 会先长成好看的 feature promo，再慢慢显出学习流，而不是一眼就读成 onboarding learning asset。

```text
Portrait onboarding-adjacent learning card for a mobile AI image app. Show one elegant phone screen, a few floating helper cards, and a soft explanatory flow about improving prompts. Clean product-marketing composition with generous left-side copy-safe area, bright neutral background, warm sand and slate blue palette, premium app-asset feel, no rendered text, no fake readable labels, no dashboard overload, no classroom board, no scenic imagery.
```

### candidate

- prompt_or_workflow: explicit diagnose-correct-improve onboarding asset
- prompt_family: hybrid app-asset learning card
- text_layer_mode: `safe-area-only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `m11 standard transfer onboarding candidate`

```text
Portrait onboarding learning asset for a mobile AI image app that teaches prompt diagnosis and correction. One believable phone screen on the right, large calm copy-safe area on the left, and a vertical sequence of 3 protocol-native helper cards showing failure marker, correction rule, and improved result. Make it feel like a polished app-asset / onboarding card rather than a dashboard mockup. Bright editorial background, warm sand and slate blue palette, premium product-marketing finish, no rendered text, no fake readable labels, no classroom board, no scenic imagery, no decorative icon swarm, no extra app chrome beyond what supports the learning flow.
```

## Outputs Observed

- baseline_summary: baseline 已像可信 app-asset，但 helper-card sequence 仍偏 implicit，更像 feature promo than learning asset。
- candidate_summary: candidate 让 `failure -> correction -> improved result` 一眼可读，同时 phone UI 没被 teaching flow 压坏，scene transfer 非常稳定。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_057700bfd1e6d5040169e8e2e509b8819196842f347affd5ef`
- candidate_generation_id: `ig_057700bfd1e6d5040169e8e3439370819195515f871425e780`
- baseline_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e2e509b8819196842f347affd5ef.png`
- candidate_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e3439370819195515f871425e780.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: onboarding learning asset baseline / candidate 已按 `legacy_use_case=app-asset`、`support_tier=standard` 写入，可作为 `app-asset` 邻近转移的正式 evidence。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 4.0 | 4.5 | 20 | 16.0 | 18.0 | candidate 更准确回答 onboarding learning asset，而不是 feature promo |
| product_native_fit | 4.0 | 4.5 | 15 | 12.0 | 13.5 | 两版都像 app 内资产，candidate 更自然地把 learning flow 嵌进去 |
| structure_and_composition | 4.0 | 4.5 | 15 | 12.0 | 13.5 | copy-safe 区与 phone 主体关系更稳 |
| asset_credibility | 4.0 | 4.5 | 15 | 12.0 | 13.5 | candidate 已接近可对外高质量草稿 |
| text_and_layout_fidelity | 4.5 | 4.5 | 10 | 9.0 | 9.0 | 无文案污染，copy-safe 区成立 |
| craft_finish | 4.5 | 4.5 | 10 | 9.0 | 9.0 | 设备和卡片工艺都干净 |
| anti_ai_artifact | 4.0 | 4.5 | 10 | 8.0 | 9.0 | candidate 明显减少 dashboard/mockup 过度感 |
| iteration_clarity | 3.0 | 4.0 | 5 | 3.0 | 4.0 | baseline 仍需明确 helper-card roles，candidate 只剩轻微 chrome residue |

### Totals

- baseline_total: `81.0`
- candidate_total: `89.5`
- baseline_result: `conditional_pass`
- candidate_result: `pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Result

- what_improved: `app-asset` 邻近场景的 standard transfer 已成立，protocol-native learning motifs 没有把资产拉成 dashboard 或讲义。
- what_did_not_improve: candidate 仍有一点 UI chrome residue，但已经是后段 polish。
- new_regression_or_risk: 如果 future prompts 重新放大 app chrome 或 floating helpers，scene 仍可能回流到 feature promo / dashboard mockup。

## Decision

- pass / conditional_pass / fail: `pass`
- lane_verdict: `standard transfer validated`
- tier_expectation_met: `yes`
- scenario_followup_needed: `no`

## Next Action

- keep: `phone screen + copy-safe zone + 3-step helper-card sequence` 这套 onboarding learning asset 骨架应保留。
- change_next: 如需更高 polish，只减轻 residual app chrome，不要弱化 3-step teaching flow。
