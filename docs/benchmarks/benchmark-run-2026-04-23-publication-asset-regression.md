# Benchmark Run: Publication Asset Regression

## Scenario

- scenario_id: `bm_editorial_cover_publication_asset` + `bm_mechanism_figure_publication_asset` + `bm_workflow_evidence_publication_asset`
- benchmark_ref: `docs/benchmarks/benchmark-scenarios.md`
- date: `2026-04-23`
- evaluator: `Codex`
- domain_direction: `wechat article editorial publication assets`
- matched_profile: `custom`
- support_tier: `standard`
- prompt_family_under_test: `metadata / delivery / publication gating regression`
- representation_mode_under_test: `visual_base_plus_post`
- deliverable_type: `editorial_publication_visual`
- usage_context: `wechat article editorial publication`
- asset_completion_mode: `complete_asset`
- target_artifact_role: `publication_asset`

## Scope

这次 regression 不是重新生成图片，而是验证 publication 机制层是否真正成立：

- 历史 article bundle metadata 是否已迁移到新 schema
- `publication_argument_support` 是否不再只能手填
- publication review 是否能区分 `publication_asset` 与 `review_candidate`
- `protected_regions` 是否已补齐到历史资产

执行入口：

- migration script: [migrate_article_bundle_metadata.py](/Users/boyzcl/Documents/image2/image2-design-director/scripts/migrate_article_bundle_metadata.py:1)
- automatic support inference: [publication_review_lib.py](/Users/boyzcl/Documents/image2/image2-design-director/scripts/publication_review_lib.py:105)
- overlay gating path: [apply_delivery_overlay.py](/Users/boyzcl/Documents/image2/image2-design-director/scripts/apply_delivery_overlay.py:229)
- export gating path: [export_bundle_sizes.py](/Users/boyzcl/Documents/image2/image2-design-director/scripts/export_bundle_sizes.py:15)

## Comparison Setup

- strategy_under_test: `legacy article bundle metadata` vs `migrated publication schema + automatic argument-support inference`

### baseline

- workflow: use the historical raster outputs exactly as they existed, with legacy bundle metadata semantics
- representation_mode: `visual_base_plus_post`
- notable_limit: no `usage_context`, no `deliverable_type`, no `artifact_role`, no publication review, empty `protected_regions`

### candidate

- workflow: migrate historical bundle metadata, backfill editorial protected regions, run publication review, preserve older non-final versions as `review_candidate`
- representation_mode: `visual_base_plus_post`
- notable_limit: argument support is now automatic heuristic inference, not image-semantic understanding

## Summary

| Scenario ID | baseline_total | candidate_total | baseline_result | candidate_result | latest_version | publication_review |
|---|---:|---:|---|---|---|---|
| `bm_editorial_cover_publication_asset` | 54.0 | 94.0 | `fail` | `pass` | `delivery_ready_visual-v001` | `pass` |
| `bm_mechanism_figure_publication_asset` | 56.0 | 93.0 | `fail` | `pass` | `delivery_ready_visual-v002` | `pass` |
| `bm_workflow_evidence_publication_asset` | 57.0 | 94.0 | `fail` | `pass` | `delivery_ready_visual-v001` | `pass` |

## Scenario 1. `bm_editorial_cover_publication_asset`

- baseline_output_ref: [delivery_ready_visual-v001.png](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-a-cover/assets/delivery_ready_visual/delivery_ready_visual-v001.png)
- candidate_output_ref: same raster; upgraded metadata at [delivery_ready_visual-v001.json](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-a-cover/assets/delivery_ready_visual/delivery_ready_visual-v001.json:1)
- baseline_viability_result: `overlay_allowed`, but with empty `protected_regions`
- candidate_viability_result: `overlay_allowed`
- baseline_publication_review_result: `not_run`
- candidate_publication_review_result: `pass`
- baseline_artifact_role: `unset`
- candidate_artifact_role: `publication_asset`

Notes:

- migration backfilled `usage_context`, `deliverable_type`, `asset_completion_mode`, `artifact_role`, `publication_review_result`
- editorial `protected_regions` are now present in both text-safe and delivery-ready metadata
- cover asset now clears `asset_identity_result = pass` and `argument_support_result = pass`

## Scenario 2. `bm_mechanism_figure_publication_asset`

- baseline_output_ref: [delivery_ready_visual-v002.png](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-b-mechanism/assets/delivery_ready_visual/delivery_ready_visual-v002.png)
- candidate_output_ref: same raster; upgraded metadata at [delivery_ready_visual-v002.json](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-b-mechanism/assets/delivery_ready_visual/delivery_ready_visual-v002.json:1)
- baseline_viability_result: `overlay_allowed`, but with empty `protected_regions`
- candidate_viability_result: `overlay_allowed`
- baseline_publication_review_result: `not_run`
- candidate_publication_review_result: `pass`
- baseline_artifact_role: `unset`
- candidate_artifact_role: `publication_asset`

Notes:

- latest mechanism figure `v002` is now the only promoted publication asset
- earlier mechanism figure [delivery_ready_visual-v001.json](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-b-mechanism/assets/delivery_ready_visual/delivery_ready_visual-v001.json:1) is intentionally preserved as `review_candidate`
- this confirms the new asset-identity layer can keep historical alternates inside the bundle without leaking them into publication state

## Scenario 3. `bm_workflow_evidence_publication_asset`

- baseline_output_ref: [delivery_ready_visual-v001.png](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-c-workflow/assets/delivery_ready_visual/delivery_ready_visual-v001.png)
- candidate_output_ref: same raster; upgraded metadata at [delivery_ready_visual-v001.json](/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles/figure-c-workflow/assets/delivery_ready_visual/delivery_ready_visual-v001.json:1)
- baseline_viability_result: `overlay_allowed`, but with empty `protected_regions`
- candidate_viability_result: `overlay_allowed`
- baseline_publication_review_result: `not_run`
- candidate_publication_review_result: `pass`
- baseline_artifact_role: `unset`
- candidate_artifact_role: `publication_asset`

Notes:

- workflow evidence asset now records full editorial protection zones
- `publication_argument_support = pass` is inferred automatically from scene + title/supporting lines + no cross-scene residues
- publication review now explicitly records `pass` instead of relying on an implicit “looks okay”

## Automatic Argument Support Validation

除了历史 bundle 迁移，还补了一个直接 smoke：

- direct inference call returned `pass` for editorial cover text
- a temporary bundle copy successfully ran `apply_delivery_overlay.py` without manually passing `--publication-argument-support pass`
- resulting overlay registered as `artifact_role = publication_asset` and `publication_review_result = pass`

结论：

- `publication_argument_support` 现在已经不是纯手填值
- 当前仍是 heuristic inference，不是图像语义理解器
- 但它已经足以把 article-title / supporting-lines / residue-check 这条 publication 主路径 mechanize 下来

## Result

- what_improved: 历史 article bundles 全部补齐 publication schema；latest publication assets now carry stable identity; old alternates stay as review candidates; export gate can rely on real metadata
- what_did_not_improve: 没有新增图像语义识别；argument support 仍主要依赖 article text and scene heuristics
- new_regression_or_risk: 同名 `protected_regions` 叠加会制造假碰撞，这次已顺手修复为后写覆盖

## Decision

- lane_verdict: `pass`
- tier_expectation_met: `yes`
- scenario_followup_needed: `yes`

Follow-up:

- run one future regression with newly generated editorial assets instead of historical migrated assets
- consider adding image-semantic evidence checks if article figures later need stronger automated argument verification

## Next Action

- keep: publication review gate, artifact-role enforcement, historical bundle migration
- change_next: if future article assets mix charts or factual evidence, connect automatic argument-support inference with stronger evidence-structure checks
