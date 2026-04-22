# Benchmark Run: exploratory-educational-visual-board

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Scenario

- scenario_id: `bm_exploratory_educational_visual_board`
- benchmark_ref: `docs/benchmarks/generalized-benchmark-surface.md`
- date: `2026-04-22`
- evaluator: `Codex`
- domain_direction: `educational visual board for AI image-prompt debugging heuristics`
- matched_profile: `none`
- support_tier: `exploratory`
- legacy_use_case: `none`
- prompt_family_under_test: `structured educational board`
- text_layer_mode_under_test: `safe-area-only`

## Input

- original_request: 为 AI image-prompt debugging heuristics 生成一张 square educational visual board，顶部预留标题安全区，不渲染最终标题文字。
- route: `direct`
- initial_brief: `Create a square educational visual board for AI image-prompt debugging heuristics with a top safe zone and no rendered title text.`

## Comparison Setup

- strategy_under_test: 验证 unmatched scene 在 `educational visual board` 这一信息设计资产上，能否从 literal worksheet / board 漂移中收回到更 publishable 的 learning board。

### baseline

- prompt_or_workflow: generic educational design board
- prompt_family: exploratory structured board
- text_layer_mode: `safe-area-only`
- assembly_ref: ad hoc baseline
- notable_limit: 容易长成过于完整的 training worksheet，模块多、对称重、publishable 感不足。

```text
Square educational visual board explaining prompt-debugging heuristics for AI image generation. Clean information-design composition with multiple panels, arrows, example cards, and a calm central teaching diagram. Bright neutral background, restrained slate blue and warm beige palette, crisp infographic style, no rendered headline text, no fake readable labels. Make it feel like a polished educational design board, not a classroom scene, not a real whiteboard, not a dashboard screenshot, not a sci-fi poster.
```

### candidate

- prompt_or_workflow: protocol-native reduced-module teaching board
- prompt_family: structured educational board
- text_layer_mode: `safe-area-only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `m11 exploratory educational board candidate`

```text
Square educational visual board for teaching how an AI image request gets diagnosed and corrected. One clear learning flow from failure card to correction rule, next-input card, and improved output preview. Keep 4 to 5 modules only, with generous breathing room and a distinct top header-safe zone with no rendered text. Use protocol-native teaching motifs: failure markers, correction arrows, prompt fragment cards, score chips, and one improved neutral asset preview. Premium information-design aesthetic, bright editorial background, slate blue plus warm sand palette, crisp vector-meets-print finish. No classroom scene, no physical whiteboard, no sticky-note wall, no dashboard UI, no fake readable labels, no tiny microtext, no decorative icon swarm.
```

## Outputs Observed

- baseline_summary: 基线图已经证明场景可达，教育板语义明确，也没有掉进 classroom / whiteboard，但版面太满，左右两侧像完整 worksheet。
- candidate_summary: 候选图把场景收成 5 步学习流，信息密度明显下降，publishable 程度上升，但 numbered modules 仍偏 tutorial sheet。
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_057700bfd1e6d5040169e8dcb43244819191bb6e47fdcb64c2`
- candidate_generation_id: `ig_057700bfd1e6d5040169e8dd2c16748191a6b9463cb0f8b212`
- baseline_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8dcb43244819191bb6e47fdcb64c2.png`
- candidate_image_output_ref: `<generated-images-root>/019db595-01a1-7d12-a3bf-c4eb40470a35/ig_057700bfd1e6d5040169e8dd2c16748191a6b9463cb0f8b212.png`

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: educational board baseline / candidate 两条 capture 已落到同一 runtime capture file，可直接作为 `board literalness` 是否只是 polish 级问题的后续 evidence。

## Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3.5 | 4.0 | 20 | 14.0 | 16.0 | 两版都读得出 educational board，candidate 的教学目标更聚焦 |
| product_native_fit | 3.0 | 3.5 | 15 | 9.0 | 10.5 | candidate 更像 protocol-native learning board，而不只是 generic worksheet |
| structure_and_composition | 4.0 | 4.5 | 15 | 12.0 | 13.5 | candidate 大幅压缩模块数，呼吸感更好 |
| asset_credibility | 3.5 | 3.5 | 15 | 10.5 | 10.5 | baseline 可作内部讲义，candidate 更接近 publishable board，但还没完全脱离 tutorial sheet 语义 |
| text_and_layout_fidelity | 4.5 | 4.5 | 10 | 9.0 | 9.0 | 顶部 safe zone 稳，整体没有可读文字污染 |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 两版工艺都较干净 |
| anti_ai_artifact | 3.5 | 4.0 | 10 | 7.0 | 8.0 | candidate 更克制，减少了 icon swarm 和 dashboard 感 |
| iteration_clarity | 4.0 | 4.0 | 5 | 4.0 | 4.0 | baseline 已暴露“太满太 literal”，candidate 进一步把下一轮变量收束到 worksheet framing |

### Totals

- baseline_total: `73.5`
- candidate_total: `79.5`
- baseline_result: `fail`
- candidate_result: `conditional_pass`
- baseline_score_recorded_in_runtime: `yes`
- candidate_score_recorded_in_runtime: `yes`

## Result

- what_improved: educational visual board 这一 unmatched scene 已确认可进入通用流程，且可以通过减少模块数、保留 protocol-native motifs 获得更 publishable 的 learning board。
- what_did_not_improve: candidate 仍保留明显 numbered tutorial-sheet framing，没有完全转成更 editorial 的 education asset。
- new_regression_or_risk: 这类任务如果只强调“解释清楚”，模型很容易补成训练讲义或模板板，而不是对外可用的 educational visual board。

## Decision

- pass / conditional_pass / fail: `conditional_pass`
- lane_verdict: `exploratory lane validated`
- tier_expectation_met: `yes`
- scenario_followup_needed: `yes`

## Next Action

- keep: `failure card -> correction rule -> next-input card -> improved output preview` 这条 reduced-module learning flow 应保留。
- change_next: 如果继续 refine，只做一件事，把 numbered worksheet framing 压下去，改成更 editorial 的 learning board crop 和模块关系。
