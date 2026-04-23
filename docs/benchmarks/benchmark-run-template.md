# Benchmark Run Template

## Purpose

用于记录这个 skill 在真实图像任务里的表现，避免只靠感觉判断“变好了”。

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
- prompt_family_under_test:
- representation_mode_under_test:

## Input

- original_request:
- route:
- initial_brief:
- factual_sensitivity:
- claim_type:
- metric_definition:
- as_of_date:

## Gate Decisions

- reliability_gate_result:
- representation_mode:
- viability_check_required:
- expected_viability_result:

## Comparison Setup

- strategy_under_test:

### baseline

- workflow:
- representation_mode:
- notable_limit:

### candidate

- workflow:
- representation_mode:
- notable_limit:

## Outputs Observed

- baseline_summary:
- candidate_summary:
- baseline_generation_id:
- candidate_generation_id:
- baseline_output_ref:
- candidate_output_ref:
- baseline_viability_result:
- candidate_viability_result:

## Runtime Memory Provenance

- runtime_capture_written:
- runtime_capture_ref:
- runtime_reuse_observed:

## Scores

按 [references/scorecard.md](../../references/scorecard.md) 的维度打分。

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match |  |  | 10 |  |  |  |
| asset_type_fidelity |  |  | 12 |  |  |  |
| contract_alignment |  |  | 8 |  |  |  |
| information_reliability |  |  | 15 |  |  |  |
| representation_fit |  |  | 10 |  |  |  |
| delivery_integrity |  |  | 12 |  |  |  |
| completion_readiness |  |  | 8 |  |  |  |
| language_alignment |  |  | 8 |  |  |  |
| structure_and_composition |  |  | 9 |  |  |  |
| asset_credibility_and_craft |  |  | 8 |  |  |  |

### Totals

- baseline_total:
- candidate_total:
- baseline_result: `pass | conditional_pass | fail`
- candidate_result: `pass | conditional_pass | fail`
- misleading_risk_baseline:
- misleading_risk_candidate:
- hard_fail_reason_baseline:
- hard_fail_reason_candidate:

## Result

- what_improved:
- what_did_not_improve:
- new_regression_or_risk:

## Decision

- lane_verdict:
- tier_expectation_met:
- scenario_followup_needed:

## Next Action

- keep:
- change_next:
```
