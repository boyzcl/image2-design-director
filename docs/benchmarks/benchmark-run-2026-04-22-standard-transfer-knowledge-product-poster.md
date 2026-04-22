# Benchmark Run: standard-transfer-knowledge-product-poster

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_standard_transfer_knowledge_product_poster`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `knowledge-product poster for an AI design-operations field guide`
- matched_profile: `custom`
- support_tier: `standard`
- legacy_use_case: `social-creative`
- prompt_family_under_test: `structured protocol-native poster`
- text_layer_mode_under_test: `safe-area-only`

## Input

- original_request: 为一个 AI design-operations field guide 生成 square knowledge-product launch poster，顶部预留标题安全区，不渲染最终标题文字。
- route: `direct`
- initial_brief: `Create a square launch poster for an AI design-operations field guide with a top title-safe zone and no rendered text.`

## Comparison Setup

- strategy_under_test: 验证 `protocol-native editorial collateral` 规则是否能从 exploratory scene 迁移到更接近 `social-creative / knowledge-product poster` 的标准转移场景。

### baseline

- prompt_or_workflow: generic field-guide poster
- prompt_family: lightweight structured poster
- text_layer_mode: `safe-area-only`
- assembly_ref: ad hoc baseline
- notable_limit: 虽然 field-guide 资产身份成立，但 supporting cards 容易回落到 generic sample board。

```text
Square knowledge-product poster for an AI design-operations field guide. Clean premium launch-style poster with one central book-like cover plate, surrounding abstract cards, thin arrows, and calm editorial energy. Bright warm background, slate blue and muted sand palette, top-third title-safe zone with no rendered text, polished information-design atmosphere, no fake readable labels, no scenic imagery, no dashboard screenshot, no classroom board.
```

### candidate

- prompt_or_workflow: protocol-native knowledge collateral prompt
- prompt_family: structured protocol-native poster
- text_layer_mode: `safe-area-only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `m11 standard transfer knowledge-product candidate`

```text
Square launch poster for a knowledge product: an AI design-operations field guide. Make it feel like premium protocol-native collateral, not a generic book ad. One central field-guide cover plate grows out of a brief packet card, route trace, score chips, and prompt assembly fragments, with only 2 to 3 supporting knowledge cards. Clear top-third title-safe zone with no rendered text. Bright editorial background, warm paper texture, slate blue plus muted sand palette, refined print-design feel, believable productized knowledge asset. No scenic samples, no dashboard UI, no classroom board, no fake readable labels, no decorative icon swarm, no consumer product semantics.
```

## Outputs Observed

- baseline_summary: baseline 已经达到可用工作稿水平，field-guide cover 可信，但右侧 supporting cards 仍带 generic sample board 残影。
- candidate_summary: candidate 把 scene 从“book ad”拉成 `protocol-native knowledge collateral`，cover 资产、supporting cards、title-safe zone 三件事都稳定下来。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_057700bfd1e6d5040169e8e162716081919bb217c3818f0831`
- candidate_generation_id: `ig_057700bfd1e6d5040169e8e1d845e08191bdaeac1373957ed6`
- baseline_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e162716081919bb217c3818f0831.png`
- candidate_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8e1d845e08191bdaeac1373957ed6.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: knowledge-product poster baseline / candidate 已以 `matched_profile=custom`、`support_tier=standard` 写入，可直接进入 standard transfer grouped review。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 4.0 | 4.5 | 20 | 16.0 | 18.0 | candidate 更像 knowledge-product launch asset，而不只是 book-like poster |
| product_native_fit | 3.5 | 4.5 | 15 | 10.5 | 13.5 | packet / route / score / assembly 语义被成功迁移到 knowledge collateral |
| structure_and_composition | 4.0 | 4.5 | 15 | 12.0 | 13.5 | candidate 的模块数更克制，cover hierarchy 更稳 |
| asset_credibility | 4.0 | 4.5 | 15 | 12.0 | 13.5 | baseline 已可工作，candidate 已接近对外高质量草稿 |
| text_and_layout_fidelity | 4.5 | 4.5 | 10 | 9.0 | 9.0 | title-safe zone 在两版里都很稳定 |
| craft_finish | 4.5 | 4.5 | 10 | 9.0 | 9.0 | 两版工艺都干净 |
| anti_ai_artifact | 3.5 | 4.5 | 10 | 7.0 | 9.0 | candidate 显著减少了 generic sample drift |
| iteration_clarity | 2.5 | 4.0 | 5 | 2.5 | 4.0 | baseline 还能再收紧 supporting cards，candidate 已只剩轻微 ornamental flow excess |

### Totals

- baseline_total: `78.0`
- candidate_total: `89.5`
- baseline_result: `conditional_pass`
- candidate_result: `pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Result

- what_improved: `protocol-native editorial collateral` 规则已成功迁移到 knowledge-product poster 这一标准转移场景，不再只在 exploratory cover / poster 上成立。
- what_did_not_improve: candidate 仍留少量 ornamental flow energy，但已不是 scene-level 风险。
- new_regression_or_risk: 如果 future prompt 重新放大“book ad”语义，supporting knowledge cards 仍可能回落到 generic sample board。

## Decision

- pass / conditional_pass / fail: `pass`
- lane_verdict: `standard transfer validated`
- tier_expectation_met: `yes`
- scenario_followup_needed: `no`

## Next Action

- keep: `field-guide cover plate + brief packet / route trace / score chips / prompt assembly fragments` 这套知识产品 collateral 骨架应保留。
- change_next: 如需更高 polish，只压 residual ornamental flow，不要改 scene identity。
