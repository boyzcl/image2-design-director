# Benchmark Run: exploratory-protocol-visual

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_exploratory_protocol_visual`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `protocol explainer poster for an AI workflow system`
- matched_profile: `none`
- support_tier: `exploratory`
- legacy_use_case: `none`
- prompt_family_under_test: `custom exploratory poster`
- text_layer_mode_under_test: `safe-area-only`

## Input

- original_request: 为一个 AI workflow system 生成一张 square protocol explainer poster，顶部预留标题安全区，不渲染最终标题文字。
- route: `direct`
- initial_brief: `Create a square protocol explainer poster for an AI workflow system with title-safe space and no rendered text.`

## Comparison Setup

- strategy_under_test: 用 protocol-native 中间链路替代泛化 pipeline 语言，验证 unmatched scene 首轮是否能达到 `60+` 的可诊断起点。

### baseline

- prompt_or_workflow: generic transformation poster
- prompt_family: lightweight exploratory poster
- text_layer_mode: `safe-area-only`
- assembly_ref: ad hoc baseline
- notable_limit: 容易滑成泛化“图像生成变换”海报，而不是 protocol-native 解释型资产

```text
A square product-design poster for an AI workflow system. Show a clean transformation from a rough request into a polished visual pipeline with layered cards, abstract arrows, interface panels, and a final deliverable board. Bright neutral editorial background with blue accents, generous top-third title-safe area, premium and minimal, no rendered text, no logos, no sci-fi clutter.
```

### candidate

- prompt_or_workflow: protocol-native exploratory prompt
- prompt_family: custom exploratory poster
- text_layer_mode: `safe-area-only`
- assembly_ref: `docs/benchmarks/generalized-benchmark-surface.md` + `docs/runtime-schema-v2.md`
- version: `m9 exploratory validation candidate`

```text
A clean square poster for an AI workflow protocol explainer. Bright editorial background, one central transformation from a rough packet card into a route trace, scorecard chips, prompt assembly sheet, and a delivery-ready neutral project asset frame. Clear top-third title-safe area with no rendered text. Premium product-design poster, restrained slate blue and warm neutral palette, no logos, no fake brand text, no sci-fi clutter, no consumer product semantics.
```

## Outputs Observed

- baseline_summary: 构图干净，但主体仍是“泛化图像变换流程”，最终 asset board 也直接漂成山景样张，更像漂亮的 image pipeline 概念图。
- candidate_summary: 已经出现 `packet -> route -> scorecard -> prompt assembly -> delivery frame` 的协议型链路，首轮就具备可诊断性，但最终 destination asset 仍偏 scenic sample。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_00c2e76377d7b9100169e8cf130e6c81918ba142866ad96f1c`
- candidate_generation_id: `ig_00c2e76377d7b9100169e8ceb5075c8191a71493bfddd38f2f`
- baseline_image_output_ref: `<generated-images-root>/019db552-7ffb-7b91-96db-97d3c520b5fa/ig_00c2e76377d7b9100169e8cf130e6c81918ba142866ad96f1c.png`
- candidate_image_output_ref: `<generated-images-root>/019db552-7ffb-7b91-96db-97d3c520b5fa/ig_00c2e76377d7b9100169e8ceb5075c8191a71493bfddd38f2f.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: 用新 `schema v2` 写入后，已能按 `matched_profile=none` 和 `support_tier=exploratory` 直接查询到 baseline / candidate 两条记录。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 2.5 | 3.5 | 20 | 10.0 | 14.0 | candidate 更像 protocol explainer，而不只是 image pipeline 变换图 |
| product_native_fit | 2.0 | 3.5 | 15 | 6.0 | 10.5 | candidate 开始长出 packet / route / scorecard 语义 |
| structure_and_composition | 3.5 | 4.0 | 15 | 10.5 | 12.0 | 两版都保持安全留白，candidate 的中轴更清楚 |
| asset_credibility | 2.0 | 3.5 | 15 | 6.0 | 10.5 | baseline 偏概念物料，candidate 已像可继续 refine 的解释型设计稿 |
| text_and_layout_fidelity | 4.0 | 4.5 | 10 | 8.0 | 9.0 | 两版都没有文字污染，candidate 的 title-safe 区更稳 |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 工艺都较干净 |
| anti_ai_artifact | 3.5 | 3.0 | 10 | 7.0 | 6.0 | candidate 虽更对题，但 scenic sample drift 仍明显 |
| iteration_clarity | 0.5 | 3.0 | 5 | 0.5 | 3.0 | candidate 已给出明确下一轮约束点，baseline 只有模糊“再具体一点” |

### Totals

- baseline_total: `56.0`
- candidate_total: `73.0`
- baseline_result: `fail`
- candidate_result: `conditional_pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Result

- what_improved: protocol-native 对象一旦写实，模型会明显减少“抽象变换流程”的漂移，并且首轮就能暴露出真正的下一轮问题。
- what_did_not_improve: `delivery-ready neutral project asset frame` 仍不足以阻止模型补成风景/样片类最终资产。
- new_regression_or_risk: candidate 的中间链路更具体后，模型会更愿意补全可读 label，这说明后续要继续守住“安全区无最终文案”和“最终 asset 类型中性化”。

## Decision

- pass / conditional_pass / fail: `conditional_pass`
- lane_verdict: `exploratory lane validated`
- tier_expectation_met: `yes`
- scenario_followup_needed: `yes`

## Next Action

- keep: `packet -> route -> scorecard -> prompt assembly` 这条 protocol-native 中间链路应保留为 exploratory scene 的优先诊断骨架。
- change_next: 下一轮只收紧一个变量，把 destination asset frame 从泛化 scenic sample 收紧成 neutral project collateral，例如 hero plate、onboarding visual 或 benchmark board。
