# Execution Plan

> Maintainer note: 这是自动回写的内部执行看板。公开保留仅用于维护轨迹追溯，外部用户应先看 `README.md`、`SKILL.md` 与 `docs/README.md`。

## Purpose

这份文档由 `scripts/update_execution_progress.py` 自动回写。
它的作用是让执行阶段始终围绕升级路线推进，并把当前进度回写成可读状态。

## Current Status

- updated_at: `2026-04-23T01:43:27+08:00`
- current_focus: `m13_delivery_real_asset_hardening`
- pending: `0`
- in_progress: `1`
- completed: `32`
- blocked: `0`

## Source Docs

- `docs/target-skill-architecture.md`
- `docs/upgrade-roadmap-from-current-state.md`
- `docs/status-summary-2026-04-22.md`

## Task Board

| id | milestone | title | status | outputs | next_step |
|---|---|---|---|---|---|
| `m1_intake_schema` | Milestone 1 | Build intake schema | `completed` | references/intake-schema.md | Draft the intake schema fields and define which fields are required versus optional. |
| `m1_strategy_tree` | Milestone 1 | Build strategy decision tree | `completed` | references/strategy-decision-tree.md | Map decision branches for direct, brief-first, repair, direct-output, post-process, and multi-candidate. |
| `m1_task_packet` | Milestone 1 | Define task packet format | `completed` | references/task-packet.md | Design a task packet format that preserves raw request, requirement summary, context summary, and delivery strategy. |
| `m2_post_process_policy` | Milestone 2 | Define post-processing policy | `completed` | references/post-processing-policy.md | Write the decision rules for direct output versus visual-base-plus-post-processing. |
| `m2_multi_candidate_policy` | Milestone 2 | Define multi-candidate and A/B policy | `completed` | references/multi-candidate-policy.md<br>docs/experiments/ab-testing-template.md | Define candidate set structure, comparison rules, and when A/B testing is worth the added cost. |
| `m3_delivery_ops` | Milestone 3 | Build delivery operations docs | `completed` | references/delivery-ops.md<br>references/text-overlay-policy.md<br>references/fixed-element-placement.md | Define raw visual, text-safe visual, and delivery-ready visual as explicit delivery states. |
| `m4_promotion_governance` | Milestone 4 | Strengthen promotion governance | `completed` | references/promotion-governance.md | Define promotion gates for raw capture, review, field note, pattern, and archive. |
| `m4_benchmark_loop` | Milestone 4 | Build benchmark and validation loop | `completed` | docs/benchmarks/benchmark-scenarios.md<br>docs/experiments/ab-testing-template.md | Define benchmark scenarios that cover social creative, project hero, UI mockup, icon, and fixed-element delivery. |
| `m5_prompt_family_regression_surface` | Milestone 5 | Align benchmark surface to prompt families | `completed` | docs/benchmarks/benchmark-scenarios.md<br>docs/benchmarks/benchmark-run-template.md<br>docs/benchmarks/prompt-family-regression-pack.md<br>docs/status-summary-2026-04-22.md | Use the regression pack to run real baseline-vs-candidate comparisons across the four default prompt families and record actual outputs plus scorecards. |
| `m5_prompt_family_validation_runs` | Milestone 5 | Run prompt-family validation loop | `completed` | docs/benchmarks/prompt-family-regression-run-2026-04-22.md | Run bm_social_creative_launch, bm_project_hero_repo, bm_ui_mockup_credibility, and bm_app_asset_onboarding_scene with baseline vs candidate prompts, then score and decide keep/adjust/revert by family. |
| `m6_targeted_prompt_family_repairs` | Milestone 6 | Retune weak prompt families after regression | `completed` | docs/experiments/prompt-family-retuning-2026-04-22.md | Run one repair pass for bm_project_hero_repo and one repair pass for bm_social_creative_launch, then compare against the current candidate outputs and decide whether those families can be promoted or still need narrower constraints. |
| `m7_default_rule_promotion` | Milestone 7 | Promote repaired prompt rules into defaults | `completed` | references/prompt-schema.md<br>references/prompt-assembly.md<br>references/sample-prompts.md<br>references/prompt-writing-spec.md<br>SKILL.md<br>docs/status-summary-2026-04-22.md | Promote the protocol-anchor hero rule and the packet-to-asset poster rule into the default prompt docs and skill guidance. |
| `m7_default_family_spot_checks` | Milestone 7 | Spot-check tightened prompt defaults | `completed` | docs/experiments/default-family-spot-check-2026-04-22.md | Generate one tightened-default hero and one tightened-default poster, then score whether the promoted defaults hold without extra repair framing. |
| `m8_scene_generalization_and_portability` | Milestone 8 | Generalize scene coverage and remove host binding | `completed` | SKILL.md<br>docs/target-skill-architecture.md<br>references/task-packet.md<br>references/strategy-decision-tree.md<br>references/prompt-schema.md<br>references/image2-prompting-playbook.md<br>references/runtime-memory.md<br>scripts/runtime_memory_lib.py | Validate the generalized runtime path resolution and ensure new scene-profile fields remain compatible with existing captures. |
| `m9_generalized_benchmark_surface` | Milestone 9 | Operationalize generalized benchmark surface | `completed` | docs/benchmarks/generalized-benchmark-surface.md<br>docs/benchmarks/benchmark-scenarios.md<br>docs/benchmarks/benchmark-run-template.md<br>docs/status-summary-2026-04-22.md | Run at least one real exploratory benchmark and verify the first-pass result clears the 60+ diagnostic threshold. |
| `m9_runtime_schema_v2` | Milestone 9 | Formalize runtime schema v2 | `completed` | docs/runtime-schema-v2.md<br>references/runtime-memory.md<br>scripts/runtime_memory_lib.py<br>scripts/read_runtime_context.py<br>scripts/log_image_generation.py | Use the repo-side logging flow on one real generalized benchmark run and verify the emitted capture and field note stay v2-compliant. |
| `m9_profile_promotion_policy` | Milestone 9 | Define profile promotion policy | `completed` | docs/profile-promotion-policy.md<br>references/promotion-governance.md<br>docs/target-skill-architecture.md<br>docs/status-summary-2026-04-22.md | Apply the new ladder to one real non-profiled scene and decide whether it stays exploratory or has enough evidence to enter standard. |
| `m9_repo_installed_sync_contract` | Milestone 9 | Define repo vs installed copy sync contract | `completed` | docs/repo-installed-runtime-sync-contract.md<br>docs/status-summary-2026-04-22.md | Execute one controlled repo -> installed sync and confirm the remaining diff is only runtime or repo-only execution artifacts. |
| `m9_followup_validation` | Milestone 9 | Run exploratory validation and sync execution | `completed` | docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md<br>docs/status-summary-2026-04-22.md<br>docs/execution-plan.md | Open the next repair loop around destination asset identity so exploratory protocol visuals stop drifting into scenic sample frames. |
| `m10_destination_asset_identity_repair` | Milestone 10 | Repair destination asset identity drift | `completed` | references/prompt-schema.md<br>references/prompt-assembly.md<br>references/sample-prompts.md<br>docs/experiments/destination-asset-identity-repair-2026-04-22.md<br>docs/status-summary-2026-04-22.md | Open one final text-discipline repair pass so the destination collateral panel keeps placeholder blocks instead of readable labels. |
| `m10_text_discipline_repair` | Milestone 10 | Repair destination panel text discipline | `completed` | docs/experiments/text-discipline-repair-2026-04-22.md<br>docs/status-summary-2026-04-22.md | Only if polishing further, soften the destination panel from literal board preview toward a more editorial collateral crop. |
| `m11_validation_thickening_plan` | Milestone 11 | Define validation thickening and promotion activation plan | `completed` | docs/m11-validation-thickening-and-promotion-activation.md<br>docs/stage-progress-review-2026-04-22.md<br>docs/status-summary-2026-04-22.md | Start M11 by running two new exploratory unmatched-scene benchmarks and recording them with runtime schema v2. |
| `m11_exploratory_validation_runs` | Milestone 11 | Run exploratory unmatched-scene validations | `completed` | docs/benchmarks/ | Select two unmatched scenes from the exploratory archetypes and run benchmark plus runtime capture for each. |
| `m11_standard_transfer_runs` | Milestone 11 | Run standard transfer validations | `completed` | docs/benchmarks/ | Choose two transfer scenes and record whether they truly hold at the standard tier. |
| `m11_delivery_heavy_validation` | Milestone 11 | Run delivery-heavy validation | `completed` | docs/benchmarks/<br>docs/experiments/ | Pick one task where delivery-state judgment is unavoidable and document the repeated friction points. |
| `m11_profile_promotion_judgment` | Milestone 11 | Produce first profile promotion judgment | `completed` | docs/ | Group the new validation runs by scene direction and apply the profile promotion policy evidence stack. |
| `m11_delivery_toolization_priority` | Milestone 11 | Set delivery toolization priority | `completed` | docs/ | Compare repeated delivery frictions and choose whether versioning, fixed-element overlay, or size adaptation comes first. |
| `m11_sync_automation_scope` | Milestone 11 | Define sync automation scope | `completed` | docs/ | Define the minimum manifest, drift-check, and one-command sync surface without touching runtime state. |
| `m12_delivery_bundle_versioning_v1` | Milestone 12 | Implement delivery bundle versioning v1 | `completed` | references/delivery-bundle-contract.md<br>scripts/delivery_bundle_lib.py<br>scripts/manage_delivery_bundle.py<br>references/delivery-ops.md<br>docs/status-summary-2026-04-22.md | Use the new bundle chain as the substrate for fixed-element overlay so text-safe bases can be promoted to delivery-ready without overwriting the source asset. |
| `m12_fixed_element_overlay` | Milestone 12 | Attach fixed-element overlay to the bundle | `completed` | scripts/apply_delivery_overlay.py<br>scripts/delivery_image_ops_lib.py<br>references/fixed-element-placement.md | Calibrate zone presets and typography heuristics on real delivery assets instead of synthetic smoke fixtures. |
| `m12_size_adaptation_fanout` | Milestone 12 | Attach size adaptation fan-out to the bundle | `completed` | scripts/export_bundle_sizes.py<br>scripts/delivery_image_ops_lib.py<br>references/delivery-ops.md | Compare safe_pad against future crop-aware modes on real channel targets once more production overlays exist. |
| `m13_delivery_real_asset_hardening` | Milestone 13 | Harden delivery chain on real assets | `in_progress` | scripts/<br>docs/<br>references/ | Run at least one real delivery-heavy asset through the new chain with actual logo, QR, and final copy instead of test fixtures. |
| `m14_local_auto_promotion_to_skill` | Milestone 14 | Auto-promote local runtime experience into local skill references | `completed` | scripts/<br>references/runtime-memory.md<br>references/promotion-governance.md<br>state/ | Decide whether benchmark-style field notes that currently stop at score 3 should remain runtime-only or gain a separate benchmark-reference layer, since they now replay cleanly but still stay below the local-skill score gate. |

## Task Details

### m1_intake_schema - Build intake schema

- milestone: `Milestone 1`
- status: `completed`
- depends_on: `none`
- summary: Define a stable intake structure for user goal, context, fixed elements, and delivery constraints.
- outputs: `references/intake-schema.md`
- next_step: Draft the intake schema fields and define which fields are required versus optional.
- notes:
  - 2026-04-22T17:09:02+08:00 - Started drafting the intake schema for requirement and context capture.
  - 2026-04-22T17:10:33+08:00 - Completed intake-schema.md with required core fields, conditional fields, intake question policy, output template, and runtime alignment notes.
  - 2026-04-22T17:13:03+08:00 - Refined intake-schema.md after self-review: added success_criteria, existing_generation_context, source_materials, and an intake completion checklist to raise stage quality bar.

### m1_strategy_tree - Build strategy decision tree

- milestone: `Milestone 1`
- status: `completed`
- depends_on: `m1_intake_schema`
- summary: Turn route and execution choices into an explicit decision tree instead of implicit judgment.
- outputs: `references/strategy-decision-tree.md`
- next_step: Map decision branches for direct, brief-first, repair, direct-output, post-process, and multi-candidate.
- notes:
  - 2026-04-22T17:13:52+08:00 - Started drafting the strategy decision tree for route and execution-mode selection.
  - 2026-04-22T17:16:47+08:00 - Completed strategy-decision-tree.md with explicit use-case classification, route selection, execution-mode selection, route override rules, and strategy completion checklist.

### m1_task_packet - Define task packet format

- milestone: `Milestone 1`
- status: `completed`
- depends_on: `m1_intake_schema`
- summary: Separate user raw request from our structured understanding and execution packet.
- outputs: `references/task-packet.md`
- next_step: Design a task packet format that preserves raw request, requirement summary, context summary, and delivery strategy.
- notes:
  - 2026-04-22T17:19:08+08:00 - Started drafting the task packet format that bridges intake and strategy outputs.
  - 2026-04-22T17:22:09+08:00 - Completed task-packet.md with packet structure, readiness rules, assembly rules, fresh and repair examples, and packet lineage tracking.

### m2_post_process_policy - Define post-processing policy

- milestone: `Milestone 2`
- status: `completed`
- depends_on: `m1_strategy_tree`
- summary: Clarify when text, QR codes, logos, and fixed assets should be added after generation.
- outputs: `references/post-processing-policy.md`
- next_step: Write the decision rules for direct output versus visual-base-plus-post-processing.
- notes:
  - 2026-04-22T17:27:03+08:00 - Started drafting post-processing policy for direct output versus visual-base-plus-post-processing decisions.
  - 2026-04-22T17:29:57+08:00 - Completed post-processing-policy.md and aligned SKILL.md and strategy-decision-tree.md. Self-review: 9.7/10. Minor remaining gap is that delivery-state mechanics will be further expanded in Milestone 3 delivery docs.

### m2_multi_candidate_policy - Define multi-candidate and A/B policy

- milestone: `Milestone 2`
- status: `completed`
- depends_on: `m1_strategy_tree`
- summary: Formalize when the skill should generate multiple candidates for comparison or user choice.
- outputs: `references/multi-candidate-policy.md`, `docs/experiments/ab-testing-template.md`
- next_step: Define candidate set structure, comparison rules, and when A/B testing is worth the added cost.
- notes:
  - 2026-04-22T17:30:06+08:00 - Started drafting multi-candidate policy and A/B testing template for candidate set structure, comparison rules, and strategy validation.
  - 2026-04-22T17:33:32+08:00 - Completed multi-candidate-policy.md and docs/experiments/ab-testing-template.md, and aligned SKILL.md plus strategy-decision-tree.md. Self-review: 9.6/10. Minor remaining gap is that benchmark scenario inventory will be expanded in the dedicated benchmark milestone.

### m3_delivery_ops - Build delivery operations docs

- milestone: `Milestone 3`
- status: `completed`
- depends_on: `m2_post_process_policy`
- summary: Document how generated visuals become usable assets through size adaptation and fixed-element placement.
- outputs: `references/delivery-ops.md`, `references/text-overlay-policy.md`, `references/fixed-element-placement.md`
- next_step: Define raw visual, text-safe visual, and delivery-ready visual as explicit delivery states.
- notes:
  - 2026-04-22T17:33:41+08:00 - Started drafting delivery operations docs for delivery states, text overlay policy, and fixed-element placement rules.
  - 2026-04-22T17:36:14+08:00 - Completed delivery-ops.md, text-overlay-policy.md, and fixed-element-placement.md, and aligned SKILL.md with delivery-state workflow. Self-review: 9.6/10. Minor remaining gap is that any future export scripting should add explicit file naming and packaging conventions.

### m4_promotion_governance - Strengthen promotion governance

- milestone: `Milestone 4`
- status: `completed`
- depends_on: `m1_task_packet`
- summary: Make experience promotion rules explicit so useful captures can upgrade without polluting long-term knowledge.
- outputs: `references/promotion-governance.md`
- next_step: Define promotion gates for raw capture, review, field note, pattern, and archive.
- notes:
  - 2026-04-22T17:36:26+08:00 - Started drafting promotion governance for capture, review, field note, pattern, and archive decisions.
  - 2026-04-22T17:37:41+08:00 - Completed promotion-governance.md and aligned SKILL.md with promotion decisions for capture, review, field note, repo candidate, pattern, and archive. Self-review: 9.6/10. Minor remaining gap is that future automation could add explicit governance ledger fields, but the decision rules are now clear and stable.

### m4_benchmark_loop - Build benchmark and validation loop

- milestone: `Milestone 4`
- status: `completed`
- depends_on: `m2_multi_candidate_policy`, `m4_promotion_governance`
- summary: Create repeatable benchmark scenarios and validation templates for strategy comparison.
- outputs: `docs/benchmarks/benchmark-scenarios.md`, `docs/experiments/ab-testing-template.md`
- next_step: Define benchmark scenarios that cover social creative, project hero, UI mockup, icon, and fixed-element delivery.
- notes:
  - 2026-04-22T17:37:51+08:00 - Started drafting benchmark scenarios that exercise social creative, project hero, UI mockup, icon, and fixed-element delivery workflows.
  - 2026-04-22T17:39:03+08:00 - Completed benchmark-scenarios.md and aligned benchmark-run-template.md plus SKILL.md so scenario-based regression, A/B comparison, and promotion review can run as a single validation loop. Self-review: 9.6/10. Minor remaining gap is that future benchmark automation may add more recording fields, but the benchmark surface and templates are now complete.
  - 2026-04-22T18:03:48+08:00 - Fed the 2026-04-22 agent-poster failure analysis, policy fixes, and direct-output retest result back into docs. Current judgment: long Chinese social posters are a high-risk case but not a hard blocker for direct_output; benchmark work should preserve a direct-output branch when user evidence shows it is plausible.

### m5_prompt_family_regression_surface - Align benchmark surface to prompt families

- milestone: `Milestone 5`
- status: `completed`
- depends_on: `m4_benchmark_loop`
- summary: Extend benchmark docs so prompt-system changes can be validated as a real regression surface rather than only being documented in references.
- outputs: `docs/benchmarks/benchmark-scenarios.md`, `docs/benchmarks/benchmark-run-template.md`, `docs/benchmarks/prompt-family-regression-pack.md`, `docs/status-summary-2026-04-22.md`
- next_step: Use the regression pack to run real baseline-vs-candidate comparisons across the four default prompt families and record actual outputs plus scorecards.
- notes:
  - 2026-04-22T18:36:12+08:00 - Created a prompt-family coverage matrix, added a directed-natural-language benchmark scenario, upgraded benchmark-run-template with prompt_family/text_layer_mode/final_prompt fields, and wrote a dedicated regression pack after prompt-system fusion.

### m5_prompt_family_validation_runs - Run prompt-family validation loop

- milestone: `Milestone 5`
- status: `completed`
- depends_on: `m5_prompt_family_regression_surface`
- summary: Run the first real benchmark cycle for the new prompt-family prompt system and decide whether the default writing shift is validated, partial, or needs correction.
- outputs: `docs/benchmarks/prompt-family-regression-run-2026-04-22.md`
- next_step: Run bm_social_creative_launch, bm_project_hero_repo, bm_ui_mockup_credibility, and bm_app_asset_onboarding_scene with baseline vs candidate prompts, then score and decide keep/adjust/revert by family.
- notes:
  - 2026-04-22T18:36:12+08:00 - Opened the next loop as validation-first work: benchmark the four prompt families with real Image2 outputs before making stronger default-capability claims.
  - 2026-04-22T18:40:20+08:00 - Completed the first real prompt-family regression run. Result: structured UI and directed natural language validated, structured poster directionally validated, hybrid structured hero regressed and needs retuning before stronger default claims.

### m6_targeted_prompt_family_repairs - Retune weak prompt families after regression

- milestone: `Milestone 6`
- status: `completed`
- depends_on: `m5_prompt_family_validation_runs`
- summary: Use the regression evidence to repair the two weakest prompt families instead of expanding the whole prompt system again.
- outputs: `docs/experiments/prompt-family-retuning-2026-04-22.md`
- next_step: Run one repair pass for bm_project_hero_repo and one repair pass for bm_social_creative_launch, then compare against the current candidate outputs and decide whether those families can be promoted or still need narrower constraints.
- notes:
  - 2026-04-22T18:40:20+08:00 - Opened the next loop around targeted repair rather than broad expansion. Priority 1: hybrid structured hero domain drift. Priority 2: structured poster project-specificity gap.
  - 2026-04-22T18:58:53+08:00 - Completed one repair pass for hero and poster. Hero improved from 62.5 fail to 81.0 conditional_pass; poster improved from 75.0 conditional_pass to 83.0 conditional_pass. The family system now holds, but both families still need narrower constraints before stronger default claims.

### m7_default_rule_promotion - Promote repaired prompt rules into defaults

- milestone: `Milestone 7`
- status: `completed`
- depends_on: `m6_targeted_prompt_family_repairs`
- summary: Sync the validated prompt-family judgment back into repo defaults so hero and poster improvements stop living only in experiment notes.
- outputs: `references/prompt-schema.md`, `references/prompt-assembly.md`, `references/sample-prompts.md`, `references/prompt-writing-spec.md`, `SKILL.md`, `docs/status-summary-2026-04-22.md`
- next_step: Promote the protocol-anchor hero rule and the packet-to-asset poster rule into the default prompt docs and skill guidance.
- notes:
  - 2026-04-22T19:16:00+08:00 - Opened the post-repair promotion step so the hero/poster fixes can become default repo guidance rather than staying only in regression notes.
  - 2026-04-22T19:25:00+08:00 - Promoted the protocol-anchor hero rule, packet-to-asset poster rule, and related guidance into prompt-schema, prompt-assembly, sample-prompts, prompt-writing-spec, SKILL, and status-summary.

### m7_default_family_spot_checks - Spot-check tightened prompt defaults

- milestone: `Milestone 7`
- status: `completed`
- depends_on: `m7_default_rule_promotion`
- summary: Run a small real-generation check on the tightened hero and poster defaults before claiming the prompt system is fully re-closed.
- outputs: `docs/experiments/default-family-spot-check-2026-04-22.md`
- next_step: Generate one tightened-default hero and one tightened-default poster, then score whether the promoted defaults hold without extra repair framing.
- notes:
  - 2026-04-22T19:33:00+08:00 - Ran one tightened-default hero and one tightened-default poster with real Image2 outputs. Both reached conditional_pass and confirmed the promoted rules hold without explicit repair framing.
  - 2026-04-22T19:34:00+08:00 - Spot-check exposed a remaining shared gap: review/delivery frames still need explicit destination asset identity to avoid scenic or architecture sample drift.

### m8_scene_generalization_and_portability - Generalize scene coverage and remove host binding

- milestone: `Milestone 8`
- status: `completed`
- depends_on: `m7_default_family_spot_checks`
- summary: Refactor the skill from four fixed use-case buckets into a general-purpose scene system with accelerated profiles, and make runtime guidance portable across agents instead of Codex-bound.
- outputs: `SKILL.md`, `docs/target-skill-architecture.md`, `references/task-packet.md`, `references/strategy-decision-tree.md`, `references/prompt-schema.md`, `references/image2-prompting-playbook.md`, `references/runtime-memory.md`, `scripts/runtime_memory_lib.py`
- next_step: Validate the generalized runtime path resolution and ensure new scene-profile fields remain compatible with existing captures.
- notes:
  - 2026-04-22T20:10:00+08:00 - Reframed the skill from four fixed buckets to general scene coverage with accelerated, standard, and exploratory support tiers.
  - 2026-04-22T20:11:00+08:00 - Removed Codex-only runtime assumptions from repo docs and runtime resolution logic; explicit root and generic agent homes are now first-class.
  - 2026-04-22T20:39:37+08:00 - Passed portability smoke test with explicit --root: runtime init, capture write, context read, and review flow all worked under a generic host.

### m9_generalized_benchmark_surface - Operationalize generalized benchmark surface

- milestone: `Milestone 9`
- status: `completed`
- depends_on: `m8_scene_generalization_and_portability`
- summary: Extend the benchmark surface so generalized scene coverage is validated at accelerated, standard, and exploratory lanes instead of only old fixed profiles.
- outputs: `docs/benchmarks/generalized-benchmark-surface.md`, `docs/benchmarks/benchmark-scenarios.md`, `docs/benchmarks/benchmark-run-template.md`, `docs/status-summary-2026-04-22.md`
- next_step: Run at least one real exploratory benchmark and verify the first-pass result clears the 60+ diagnostic threshold.
- notes:
  - 2026-04-22T21:19:00+08:00 - Diagnosed that benchmark coverage was still mostly protecting the old validated archives and could not prove a new unmatched scene can reach a 60+ diagnostic starting point.
  - 2026-04-22T21:20:00+08:00 - Added a generalized benchmark surface doc, upgraded the benchmark run template with domain_direction / matched_profile / support_tier, and updated benchmark-scenarios with exploratory-lane guidance.

### m9_runtime_schema_v2 - Formalize runtime schema v2

- milestone: `Milestone 9`
- status: `completed`
- depends_on: `m8_scene_generalization_and_portability`
- summary: Define and minimally implement a runtime schema that keeps scene-profile fields intact across capture, review, and field-note stages while preserving legacy use-case compatibility.
- outputs: `docs/runtime-schema-v2.md`, `references/runtime-memory.md`, `scripts/runtime_memory_lib.py`, `scripts/read_runtime_context.py`, `scripts/log_image_generation.py`
- next_step: Use the repo-side logging flow on one real generalized benchmark run and verify the emitted capture and field note stay v2-compliant.
- notes:
  - 2026-04-22T21:20:30+08:00 - Identified that runtime docs mentioned the new scene-profile fields, but there was no explicit schema contract for capture, review, and field notes.
  - 2026-04-22T21:21:30+08:00 - Landed runtime schema v2 docs plus minimal script support: schema_version defaulting, legacy_use_case normalization, scene-profile review metadata, runtime filters, and a repo-side log_image_generation script.

### m9_profile_promotion_policy - Define profile promotion policy

- milestone: `Milestone 9`
- status: `completed`
- depends_on: `m8_scene_generalization_and_portability`
- summary: Turn the compounding idea into explicit rules for when a scene direction stays exploratory, graduates to standard, or qualifies as accelerated.
- outputs: `docs/profile-promotion-policy.md`, `references/promotion-governance.md`, `docs/target-skill-architecture.md`, `docs/status-summary-2026-04-22.md`
- next_step: Apply the new ladder to one real non-profiled scene and decide whether it stays exploratory or has enough evidence to enter standard.
- notes:
  - 2026-04-22T21:21:45+08:00 - Separated sample promotion from profile promotion so capture/field-note governance no longer has to implicitly carry the exploratory -> standard -> accelerated ladder.
  - 2026-04-22T21:22:15+08:00 - Added explicit promotion gates, hold/demotion rules, and evidence-stack requirements for scene-profile promotion.

### m9_repo_installed_sync_contract - Define repo vs installed copy sync contract

- milestone: `Milestone 9`
- status: `completed`
- depends_on: `m8_scene_generalization_and_portability`
- summary: Document the boundary and synchronization rules between the repo worktree, the host-installed skill copy, and runtime memory so rule updates stop drifting away from actual host behavior.
- outputs: `docs/repo-installed-runtime-sync-contract.md`, `docs/status-summary-2026-04-22.md`
- next_step: Execute one controlled repo -> installed sync and confirm the remaining diff is only runtime or repo-only execution artifacts.
- notes:
  - 2026-04-22T21:22:30+08:00 - Confirmed that the local Codex installed copy exists and is materially behind the repo, including pre-generalization skill language and missing repo-side docs/scripts.
  - 2026-04-22T21:23:00+08:00 - Defined a three-layer contract for repo, installed copy, and runtime, including explicit sync scope and an rsync pattern that preserves runtime state.

### m9_followup_validation - Run exploratory validation and sync execution

- milestone: `Milestone 9`
- status: `completed`
- depends_on: `m9_generalized_benchmark_surface`, `m9_runtime_schema_v2`, `m9_profile_promotion_policy`, `m9_repo_installed_sync_contract`
- summary: Execute the first real exploratory benchmark under the new benchmark/runtime contracts, then perform one controlled repo-to-installed sync and verify the remaining drift is within contract.
- outputs: `docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md`, `docs/status-summary-2026-04-22.md`, `docs/execution-plan.md`
- next_step: Open the next repair loop around destination asset identity so exploratory protocol visuals stop drifting into scenic sample frames.
- notes:
  - 2026-04-22T21:27:00+08:00 - Opened the next operationalization loop: first run one real exploratory benchmark with the new template and runtime schema v2, then execute one controlled repo-to-installed sync.
  - 2026-04-22T21:42:50+08:00 - Completed one real exploratory benchmark run at 73.0 conditional_pass under the new generalized benchmark surface, wrote both baseline and candidate into runtime schema v2, and verified query by matched_profile=none plus support_tier=exploratory.
  - 2026-04-22T21:43:00+08:00 - Executed a controlled repo-to-installed sync and verified the remaining differences are now limited to contract-allowed areas such as runtime, state, test-output, execution docs, and experiments; core skill/docs/scripts cmp clean.
  - 2026-04-22T21:43:43+08:00 - Next highest-leverage open issue is now explicit: destination asset identity still drifts scenic in exploratory protocol visuals, so the next loop should target that variable instead of reopening generalized architecture work.

### m10_destination_asset_identity_repair - Repair destination asset identity drift

- milestone: `Milestone 10`
- status: `completed`
- depends_on: `m9_followup_validation`
- summary: Tighten destination asset identity from an abstract neutral-asset phrase into concrete allowed collateral examples plus hard exclusions, then rerun the same exploratory scene to verify scenic drift drops.
- outputs: `references/prompt-schema.md`, `references/prompt-assembly.md`, `references/sample-prompts.md`, `docs/experiments/destination-asset-identity-repair-2026-04-22.md`, `docs/status-summary-2026-04-22.md`
- next_step: Open one final text-discipline repair pass so the destination collateral panel keeps placeholder blocks instead of readable labels.
- notes:
  - 2026-04-22T21:47:00+08:00 - Opened a narrow repair loop around destination asset identity instead of reopening generalized architecture work.
  - 2026-04-22T21:54:00+08:00 - Tightened destination asset language into allowed examples plus hard exclusions, reran the exploratory protocol visual, and reduced scenic drift. The main remaining leak is now small readable labels inside the destination panel.

### m10_text_discipline_repair - Repair destination panel text discipline

- milestone: `Milestone 10`
- status: `completed`
- depends_on: `m10_destination_asset_identity_repair`
- summary: Keep the repaired destination asset identity and add a placeholder-only text discipline constraint so the destination collateral panel stops generating readable labels or microcopy.
- outputs: `docs/experiments/text-discipline-repair-2026-04-22.md`, `docs/status-summary-2026-04-22.md`
- next_step: Only if polishing further, soften the destination panel from literal board preview toward a more editorial collateral crop.
- notes:
  - 2026-04-22T21:57:00+08:00 - Opened one more narrow repair pass after destination asset identity succeeded: keep the collateral panel but suppress readable labels into placeholder blocks.
  - 2026-04-22T22:01:00+08:00 - The text-discipline repair reached 84.0 pass. Scenic drift and readable label leak are both down; the remaining issue is only slight UI-board literalness.

### m11_validation_thickening_plan - Define validation thickening and promotion activation plan

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m10_text_discipline_repair`
- summary: Turn the current stage diagnosis into a concrete M11 execution plan so the next phase can run on explicit validation, promotion, delivery-priority, and sync-automation tasks instead of high-level intent.
- outputs: `docs/m11-validation-thickening-and-promotion-activation.md`, `docs/stage-progress-review-2026-04-22.md`, `docs/status-summary-2026-04-22.md`
- next_step: Start M11 by running two new exploratory unmatched-scene benchmarks and recording them with runtime schema v2.
- notes:
  - 2026-04-22T22:18:00+08:00 - Converted the stage-gap diagnosis into an explicit M11 plan with workstreams, task breakdown, success criteria, non-goals, and execution order.

### m11_exploratory_validation_runs - Run exploratory unmatched-scene validations

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_validation_thickening_plan`
- summary: Add at least two new unmatched-scene benchmark runs so the generalized exploratory claim is supported by more than one real scene.
- outputs: `docs/benchmarks/`
- next_step: Select two unmatched scenes from the exploratory archetypes and run benchmark plus runtime capture for each.
- notes:
  - 2026-04-22T22:49:03+08:00 - Completed two new exploratory unmatched-scene validations: editorial report cover and educational visual board. Added benchmark docs, wrote four runtime schema v2 captures, and confirmed a preliminary near-threshold promotion signal for editorial protocol/report collateral.

### m11_standard_transfer_runs - Run standard transfer validations

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_validation_thickening_plan`
- summary: Run at least two transfer-style validations that partially inherit existing prompt families or delivery rules but do not cleanly match current accelerated profiles.
- outputs: `docs/benchmarks/`
- next_step: Choose two transfer scenes and record whether they truly hold at the standard tier.
- notes:
  - 2026-04-22T23:36:41+08:00 - Completed two standard transfer validations: knowledge-product poster and onboarding-adjacent learning asset. Both cleared 70+, and both candidates reached pass-level results.

### m11_delivery_heavy_validation - Run delivery-heavy validation

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_validation_thickening_plan`
- summary: Run at least one delivery-heavy task that forces text-safe, delivery-ready, or fixed-element judgment so delivery toolization priorities come from real pain.
- outputs: `docs/benchmarks/`, `docs/experiments/`
- next_step: Pick one task where delivery-state judgment is unavoidable and document the repeated friction points.
- notes:
  - 2026-04-22T23:36:42+08:00 - Completed one delivery-heavy validation on an event signup poster base. Confirmed a repeatable text-safe visual state and isolated the main delivery blockers to overlay plus size adaptation.

### m11_profile_promotion_judgment - Produce first profile promotion judgment

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_exploratory_validation_runs`, `m11_standard_transfer_runs`
- summary: Use the new validation evidence to make at least one real keep, hold, or promote decision at the profile level instead of leaving promotion policy purely theoretical.
- outputs: `docs/`
- next_step: Group the new validation runs by scene direction and apply the profile promotion policy evidence stack.
- notes:
  - 2026-04-22T23:36:42+08:00 - Produced the first formal profile promotion judgment. Promoted protocol-native editorial / knowledge collateral from exploratory to standard, held educational visual board in exploratory, and kept existing accelerated profiles.

### m11_delivery_toolization_priority - Set delivery toolization priority

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_delivery_heavy_validation`
- summary: Rank the next delivery implementation targets using repeated pain points from M11 validations instead of intuition.
- outputs: `docs/`
- next_step: Compare repeated delivery frictions and choose whether versioning, fixed-element overlay, or size adaptation comes first.
- notes:
  - 2026-04-22T23:36:42+08:00 - Set delivery toolization priority based on real M11 evidence: text-safe to delivery-ready versioning first, fixed-element overlay second, and size adaptation third.

### m11_sync_automation_scope - Define sync automation scope

- milestone: `Milestone 11`
- status: `completed`
- depends_on: `m11_validation_thickening_plan`
- summary: Turn the already-validated manual repo-to-installed sync into a scoped automation design with explicit include and exclude boundaries.
- outputs: `docs/`
- next_step: Define the minimum manifest, drift-check, and one-command sync surface without touching runtime state.
- notes:
  - 2026-04-22T23:36:42+08:00 - Defined sync automation scope with a minimal manifest, narrow drift check, one-command repo-to-installed sync, and hard exclusions for runtime/state/test-output/repo-only execution artifacts.

### m12_delivery_bundle_versioning_v1 - Implement delivery bundle versioning v1

- milestone: `Milestone 12`
- status: `completed`
- depends_on: `m11_delivery_toolization_priority`
- summary: Turn raw_visual, text_safe_visual, and delivery_ready_visual into an executable bundle contract with stable naming, lineage, and command entrypoints.
- outputs: `references/delivery-bundle-contract.md`, `scripts/delivery_bundle_lib.py`, `scripts/manage_delivery_bundle.py`, `references/delivery-ops.md`, `docs/status-summary-2026-04-22.md`
- next_step: Use the new bundle chain as the substrate for fixed-element overlay so text-safe bases can be promoted to delivery-ready without overwriting the source asset.
- notes:
  - 2026-04-23T00:00:00+08:00 - Implemented delivery bundle versioning v1 with a bundle manifest, per-state version ids, latest pointers, parent lineage, and reserved overlay/size-adaptation directories.

### m12_fixed_element_overlay - Attach fixed-element overlay to the bundle

- milestone: `Milestone 12`
- status: `completed`
- depends_on: `m12_delivery_bundle_versioning_v1`
- summary: Add a low-friction overlay pass that reads the latest text_safe_visual, applies QR/logo/title/date placement, and registers a new delivery_ready_visual version.
- outputs: `scripts/apply_delivery_overlay.py`, `scripts/delivery_image_ops_lib.py`, `references/fixed-element-placement.md`
- next_step: Calibrate zone presets and typography heuristics on real delivery assets instead of synthetic smoke fixtures.
- notes:
  - 2026-04-23T00:25:00+08:00 - Implemented a first overlay pass that reads the latest text_safe_visual, applies title/date/CTA plus QR/logo/badge assets, writes working files under overlay/applied, and registers a new delivery_ready_visual version.
  - 2026-04-23T00:26:00+08:00 - Fixed a real CJK bold-font fallback bug exposed by smoke validation so Chinese title and CTA text no longer render as tofu boxes.

### m12_size_adaptation_fanout - Attach size adaptation fan-out to the bundle

- milestone: `Milestone 12`
- status: `completed`
- depends_on: `m12_delivery_bundle_versioning_v1`
- summary: Add a crop-aware export layer that fans out from delivery_ready_visual while preserving focus, text-safe zones, and fixed-element safety.
- outputs: `scripts/export_bundle_sizes.py`, `scripts/delivery_image_ops_lib.py`, `references/delivery-ops.md`
- next_step: Compare safe_pad against future crop-aware modes on real channel targets once more production overlays exist.
- notes:
  - 2026-04-23T00:27:00+08:00 - Implemented safe-first size fan-out from delivery_ready_visual, writing exports under size-adaptation/exports/<source_version>/ and recording each export run back into the bundle manifest.

### m13_delivery_real_asset_hardening - Harden delivery chain on real assets

- milestone: `Milestone 13`
- status: `in_progress`
- depends_on: `m12_fixed_element_overlay`, `m12_size_adaptation_fanout`
- summary: Replace synthetic smoke fixtures with real QR/logo/copy packages and use them to calibrate overlay zones, typography, and size-export heuristics.
- outputs: `scripts/`, `docs/`, `references/`
- next_step: Run at least one real delivery-heavy asset through the new chain with actual logo, QR, and final copy instead of test fixtures.
- notes:
  - 2026-04-23T00:29:08+08:00 - Ran one real delivery asset with the user-provided WeChat group QR and cropped real group avatar. The square delivery_ready master passed OpenCV QR decode, while the current non-square safe_pad exports lost QR detection, confirming that real-asset size adaptation still needs hardening.
  - 2026-04-23T00:35:05+08:00 - Validated QR replacement end-to-end with a standard externally provided QR. The input QR, the new delivery_ready master, and all three safe_pad exports (1080x1350, 1920x1080, 1200x628) were detected and decoded to the same URL by OpenCV.
  - 2026-04-23T00:40:00+08:00 - Functional-side judgment updated: delivery toolization is no longer the main project gap; remaining work is now real-asset hardening rather than basic delivery feasibility.

### m14_local_auto_promotion_to_skill - Auto-promote local runtime experience into local skill references

- milestone: `Milestone 14`
- status: `completed`
- depends_on: `m13_delivery_real_asset_hardening`
- summary: Turn field-note-level local runtime experience into an automatically readable local skill reference layer, while keeping repo and GitHub-facing rule upgrades under manual review.
- outputs: `scripts/`, `references/runtime-memory.md`, `references/promotion-governance.md`, `state/`
- next_step: Decide whether benchmark-style field notes that currently stop at score 3 should remain runtime-only or gain a separate benchmark-reference layer, since they now replay cleanly but still stay below the local-skill score gate.
- notes:
  - 2026-04-23T00:40:00+08:00 - New direction confirmed: local experience should auto-promote into the local skill layer, but repo / GitHub public rule promotion should remain manual.
  - 2026-04-23T01:06:00+08:00 - Implemented local auto-promotion v1 on top of runtime_memory_lib.py and the existing review flow. Added promoted/local-skill/{active,disabled,archive,history}, local-skill-manifest.json, active-layer read priority, active working-set ceiling, and minimal disable/archive/rollback governance.
  - 2026-04-23T01:06:00+08:00 - Smoke-validated that eligible captures promote into field notes and active local skill refs, the read path prefers local skill refs, active overflow is archived by ceiling policy, rollback can restore from history, and repo-candidates remain untouched by the automatic path.
  - 2026-04-23T01:14:00+08:00 - Hardened merge quality so repeated scene variants converge more reliably into an existing field note / local skill reference. Added scene-family normalization, metadata-weighted matching, stronger merge evidence logging, and a focused smoke test proving alpha/beta variants now merge into one note instead of creating sibling refs.
  - 2026-04-23T01:39:30+08:00 - Replayed the tightened merge logic against a copied real Codex runtime backlog. Added scene-role guards so baseline/candidate/preflight/repair-style comparison slots do not auto-merge even when scene-family overlap is high, while alpha/beta retries still converge. Also added legacy promotion-policy normalization so stale archive keywords such as sample no longer distort real backlog triage.

## Update Command

```bash
python scripts/update_execution_progress.py --task <task-id> --status <pending|in_progress|completed|blocked> --note "progress note"
```
