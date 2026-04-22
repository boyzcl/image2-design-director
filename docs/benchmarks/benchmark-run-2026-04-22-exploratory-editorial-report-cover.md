# Benchmark Run: exploratory-editorial-report-cover

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_exploratory_editorial_report_cover`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `editorial report cover for an AI design-operations system`
- matched_profile: `none`
- support_tier: `exploratory`
- legacy_use_case: `none`
- prompt_family_under_test: `hybrid structured editorial cover`
- text_layer_mode_under_test: `safe-area-only`

## Input

- original_request: 为一个 AI design-operations system 生成一张 portrait editorial report cover，顶部预留 masthead 安全区，不渲染最终标题文字。
- route: `direct`
- initial_brief: `Create a portrait editorial report cover for an AI design-operations system with a masthead-safe band and no rendered title text.`

## Comparison Setup

- strategy_under_test: 验证 unmatched scene 在 `editorial / report cover` 这一资产类型上，能否从泛抽象封面推进到带 protocol-native 机制语义的正式封面稿。

### baseline

- prompt_or_workflow: generic editorial cover with abstract cards
- prompt_family: lightweight exploratory editorial cover
- text_layer_mode: `safe-area-only`
- assembly_ref: ad hoc baseline
- notable_limit: 容易长成“高级抽象封面”，但机制型系统语义太弱，不能证明 scene profiling 已经迁移到 report cover。

```text
Portrait editorial report cover for an AI design-operations system. Clean premium cover composition with a restrained central visual made of layered abstract cards, thin route lines, evaluation dots, and one polished final asset plate. Large quiet masthead-safe band in the upper area with no rendered title text. Bright warm paper-like background, slate blue plus soft sand palette, sophisticated magazine/report design, minimal and credible, no fake typography, no dashboard UI, no scenic photography, no device mockup, no classroom scene.
```

### candidate

- prompt_or_workflow: protocol-native editorial cover prompt
- prompt_family: hybrid structured editorial cover
- text_layer_mode: `safe-area-only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `m11 exploratory editorial cover candidate`

```text
Portrait editorial report cover for a field report about an AI design-operations system. Sophisticated magazine-quality cover design with one clear mechanism flow: a rough brief packet card evolves into a route trace, evaluation score chips, prompt assembly fragments, and a final neutral report-cover plate. Large quiet masthead-safe band across the upper area with no rendered title text. The final plate must read as editorial report collateral, not abstract art, not a scenic image, not a dashboard screenshot. Show 3 to 4 protocol-native cards with subtle labels only as non-readable placeholder marks, elegant thin connectors, believable cover hierarchy, bright warm paper background, slate blue plus muted sand palette, restrained premium finish, no fake typography, no device mockup, no classroom board, no consumer product styling.
```

## Outputs Observed

- baseline_summary: 基线图已经有可信封面气质和干净 masthead-safe 区，但左侧卡片更像抽象设计练习，机制链路仍偏弱。
- candidate_summary: 候选图把 `brief packet -> route trace -> score chips -> report-cover plate` 拉成可读流程，同时保住了正式封面 identity，已经不像 generic art cover。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_057700bfd1e6d5040169e8dada13dc8191a6a7a95d7e31cf27`
- candidate_generation_id: `ig_057700bfd1e6d5040169e8db9661148191a2e5f8d0c4cb29e3`
- baseline_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8dada13dc8191a6a7a95d7e31cf27.png`
- candidate_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8db9661148191a2e5f8d0c4cb29e3.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: editorial cover baseline / candidate 两条 capture 已按 `matched_profile=none` 和 `support_tier=exploratory` 写入，可直接加入后续 grouped review。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3.0 | 4.0 | 20 | 12.0 | 16.0 | candidate 更明确回答“AI design-operations report cover”，不再只是高级抽象封面 |
| product_native_fit | 2.5 | 4.0 | 15 | 7.5 | 12.0 | protocol-native cards 和 report plate 让 candidate 更像系统自己的封面资产 |
| structure_and_composition | 4.0 | 4.5 | 15 | 12.0 | 13.5 | 两版都保住了顶部安全区，candidate 的 cover hierarchy 更完整 |
| asset_credibility | 3.0 | 4.0 | 15 | 9.0 | 12.0 | baseline 是漂亮封面草图，candidate 已接近真实 editorial cover 工作稿 |
| text_and_layout_fidelity | 4.5 | 4.5 | 10 | 9.0 | 9.0 | masthead-safe band 在两版里都非常稳定 |
| craft_finish | 4.5 | 4.5 | 10 | 9.0 | 9.0 | 工艺都干净，candidate 没因为语义加深而变脏 |
| anti_ai_artifact | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 两版都没有明显 AI poster 杂讯，candidate 仍留少量抽象 art-card 残影 |
| iteration_clarity | 1.0 | 4.0 | 5 | 1.0 | 4.0 | candidate 已经把下一轮变量收束到 subordinate card identity，而 baseline 仍较模糊 |

### Totals

- baseline_total: `67.5`
- candidate_total: `83.5`
- baseline_result: `fail`
- candidate_result: `conditional_pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Result

- what_improved: editorial cover 这一 unmatched scene 已被证明不需要退回 generic abstraction，只要把 protocol-native 机制对象写实，就能明显提升 cover identity 和 scene specificity。
- what_did_not_improve: subordinate cards 仍有一点 gallery-like 抽象封面残影，还没有完全变成 report-native supporting fragments。
- new_regression_or_risk: 一旦追求“高级封面感”，模型仍可能把 supporting cards 做得太像抽象艺术 study，而不是系统证据卡。

## Decision

- pass / conditional_pass / fail: `conditional_pass`
- lane_verdict: `exploratory lane validated and near standard-threshold behavior`
- tier_expectation_met: `yes`
- scenario_followup_needed: `yes`

## Next Action

- keep: `masthead-safe cover skeleton + brief packet / route trace / score chips / report-cover plate` 这套 editorial collateral 骨架应保留。
- change_next: 如果继续 refine，只收紧 subordinate cards，让它们更像 report fragments 和 supporting evidence，而不是抽象 art-card study。
