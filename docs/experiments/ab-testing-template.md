# A/B Testing Template

## Purpose

这份模板用于记录 `image2-design-director` 的 A/B 测试，避免策略对比停留在“感觉这个更好”。

它适用于两类场景：

- skill 内部策略校准
- 高价值任务里的明确策略比较

如果当前只是给用户看两个视觉方向，不一定需要走完整 A/B 模板；那更适合使用多候选对比记录。

## Template

```md
# A/B Test: <test-name>

## Test Metadata

- date:
- evaluator:
- test_type: `internal_strategy_calibration | task_level_strategy_compare`
- benchmark_ref:
- related_candidate_set_id:

## Goal

- business_or_skill_goal:
- decision_to_make:
- success_signal:
- stop_rule:

## Hypothesis

- hypothesis_a:
- hypothesis_b:
- why_this_is_worth_testing:

## Shared Context

- original_request:
- use_case:
- asset_type:
- usage_context:
- shared_constraints:
- must_avoid:
- post_processing_assumption:

## Variant Definition

### Variant A

- variant_id:
- strategy_summary:
- what_changed:
- what_stayed_fixed:
- prompt_or_workflow_summary:

### Variant B

- variant_id:
- strategy_summary:
- what_changed:
- what_stayed_fixed:
- prompt_or_workflow_summary:

## Execution Record

### Variant A Output

- image_prompt:
- revised_prompt_if_any:
- generation_id:
- image_output_ref:

### Variant B Output

- image_prompt:
- revised_prompt_if_any:
- generation_id:
- image_output_ref:

## Scoring

先按 [references/scorecard.md](../../references/scorecard.md) 的维度评分。

| Dimension | A_0_5 | B_0_5 | weight | A_weighted | B_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match |  |  | 20 |  |  |  |
| product_native_fit |  |  | 15 |  |  |  |
| structure_and_composition |  |  | 15 |  |  |  |
| asset_credibility |  |  | 15 |  |  |  |
| text_and_layout_fidelity |  |  | 10 |  |  |  |
| craft_finish |  |  | 10 |  |  |  |
| anti_ai_artifact |  |  | 10 |  |  |  |
| iteration_clarity |  |  | 5 |  |  |  |

## Totals

- total_a:
- total_b:
- result_a: `pass | conditional_pass | fail`
- result_b: `pass | conditional_pass | fail`
- score_gap:

## One-Vote Veto Check

- variant_a_red_flags:
- variant_b_red_flags:
- veto_applied: `yes | no`
- veto_reason:

## Result Summary

- winner: `A | B | no_clear_winner`
- why_winner_won:
- why_loser_lost:
- what_was_learned:
- is_the_learning_transferable: `yes | maybe | no`
- confidence_level: `low | medium | high`

## Action

- next_action: `promote_strategy | repair_winner | run_followup_test | keep_as_reference_only`
- runtime_capture_updated:
- benchmark_record_written:
- field_note_candidate:
```

## Minimum Rules

### 1. Test A Single Decision

一次 A/B 只比较一个核心策略问题。

### 2. Hold Shared Constraints Stable

如果 use case、资产类型、硬约束全变了，这就不再是有效 A/B。

### 3. Record Why The Winner Won

不能只记录：

- “B 更好”

要记录：

- 它具体改善了什么
- 这个改善是否可迁移

### 4. Accept `no_clear_winner`

如果结果不清楚，可以明确写：

- `no_clear_winner`

这比强行得出错误结论更有价值。
