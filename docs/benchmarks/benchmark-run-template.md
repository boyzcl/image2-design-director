# Benchmark Run Template

## Purpose

用于记录这个 Skill 在真实图像任务里的表现，避免只靠感觉判断“变好了”。

## Template

```md
# Benchmark Run: <scenario-name>

## Scenario

- scenario_id:
- benchmark_ref:
- date:
- evaluator:
- domain_direction:
- matched_profile:
- support_tier:
- legacy_use_case:
- prompt_family_under_test:
- text_layer_mode_under_test:

## Input

- original_request:
- route:
- initial_brief:

## Comparison Setup

- strategy_under_test:

### baseline

- prompt_or_workflow:
- prompt_family:
- text_layer_mode:
- assembly_ref:
- notable_limit:

### candidate

- prompt_or_workflow:
- prompt_family:
- text_layer_mode:
- assembly_ref:
- version:

## Outputs Observed

- baseline_summary:
- candidate_summary:
- baseline_final_prompt:
- candidate_final_prompt:
- baseline_image_prompt:
- candidate_image_prompt:
- baseline_generation_id:
- candidate_generation_id:
- baseline_image_output_ref:
- candidate_image_output_ref:

## Runtime Memory Provenance

- runtime_capture_written:
- runtime_capture_ref:
- runtime_reuse_observed:

## Scores

先按 [references/scorecard.md](../../references/scorecard.md) 的 8 个维度打分。

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match |  |  | 20 |  |  |  |
| product_native_fit |  |  | 15 |  |  |  |
| structure_and_composition |  |  | 15 |  |  |  |
| asset_credibility |  |  | 15 |  |  |  |
| text_and_layout_fidelity |  |  | 10 |  |  |  |
| craft_finish |  |  | 10 |  |  |  |
| anti_ai_artifact |  |  | 10 |  |  |  |
| iteration_clarity |  |  | 5 |  |  |  |

### Totals

- baseline_total:
- candidate_total:
- baseline_result: `pass | conditional_pass | fail`
- candidate_result: `pass | conditional_pass | fail`
- baseline_score_recorded_in_runtime:
- candidate_score_recorded_in_runtime:

## Result

- what_improved:
- what_did_not_improve:
- new_regression_or_risk:

## Decision

- pass / conditional_pass / fail
- lane_verdict:
- tier_expectation_met:
- scenario_followup_needed:

## Next Action

- keep:
- change_next:
```
