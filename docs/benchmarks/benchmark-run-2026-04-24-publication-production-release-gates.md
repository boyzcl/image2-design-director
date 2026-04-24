# Benchmark Run: Publication Production And Release Gates

## Scenario

- date: `2026-04-24`
- evaluator: `Codex`
- scope: production preflight, visual quality review, final release gate
- related repair plan: [publication-asset-production-and-release-repair-plan-2026-04-24.md](../articles/publication-asset-production-and-release-repair-plan-2026-04-24.md)

## Verification Intent

这次验证不重新生成图片。它验证三件事：

1. 制作前，direct-first production route 不会被旧 hybrid / deterministic 逻辑误拦。
2. 制作后，`publication_review = pass` 但图面质量不够的资产不会再被当作最终发布资产。
3. 后期整图重建、缺 evidence objects、paragraph-heavy 这类错误 route 仍会被拦下。

## Fixtures

- cover direct pass fixture: [publication-production-packet-cover-direct-pass.json](fixtures/publication-production-packet-cover-direct-pass.json)
- mechanism direct pass fixture: [publication-production-packet-mechanism-pass.json](fixtures/publication-production-packet-mechanism-pass.json)
- workflow direct pass fixture: [publication-production-packet-workflow-direct-pass.json](fixtures/publication-production-packet-workflow-direct-pass.json)
- data direct pass fixture: [publication-production-packet-data-direct-pass.json](fixtures/publication-production-packet-data-direct-pass.json)
- mechanism fail fixture: [publication-production-packet-mechanism-fail.json](fixtures/publication-production-packet-mechanism-fail.json)
- workflow fail fixture: [publication-production-packet-workflow-fail.json](fixtures/publication-production-packet-workflow-fail.json)
- postprocess rebuild fail fixture: [publication-production-packet-postprocess-rebuild-fail.json](fixtures/publication-production-packet-postprocess-rebuild-fail.json)

## Production Preflight Results

| Case | Expected | Actual | Key Blockers |
|---|---|---|---|
| cover direct packet | `pass` | `pass` | none |
| mechanism direct packet | `pass` | `pass` | none |
| workflow direct packet | `pass` | `pass` | none |
| data direct packet with verified facts | `pass` | `pass` | none |
| mechanism paragraph-heavy packet | `fail` | `fail` | `mechanism_text_density_too_high` |
| workflow missing evidence objects | `fail` | `fail` | missing `runtime_capture`, `scorecard`, `route_trace`, `accepted_asset_state`; `workflow_evidence_requires_multi_candidate` |
| postprocess full-layout rebuild | `fail` | `fail` | `unsupported_postprocess_scope:full_layout_rebuild`, `postprocess_scope_full_layout_rebuild`, `direct_first_route_not_established` |

## Final Release Gate Function Results

| Case | Actual Result | Blockers |
|---|---|---|
| all gates pass | `pass` | none |
| metadata pass but visual quality fail | `fail` | `visual_quality_review_not_pass` |
| runtime capture missing | `conditional_pass` | `runtime_capture_missing` |
| production preflight not pass | `conditional_pass` | `production_preflight_not_pass` |

## Historical Article Asset Reclassification

| Asset | Publication Review | Visual Quality Review | Final Release | Blockers |
|---|---|---|---|---|
| `editorial-cover-report-final.png` | `pass` | `conditional_pass` | `conditional_pass` | `production_preflight_not_pass`, `visual_quality_review_not_pass`, `runtime_capture_missing` |
| `protocol-visual-mechanism-final.png` | `pass` | `fail` | `fail` | `production_preflight_not_pass`, `visual_quality_review_not_pass`, `runtime_capture_missing` |
| `workflow-evidence-final.png` | `pass` | `conditional_pass` | `conditional_pass` | `production_preflight_not_pass`, `visual_quality_review_not_pass`, `runtime_capture_missing` |

## Result

- direct-first production routes now pass preflight instead of being incorrectly blocked by the old hybrid / deterministic preference.
- production route failures are still caught before generation.
- visual quality failures are now separated from publication identity pass.
- final release cannot pass without production preflight, visual quality pass, and runtime capture.
- the current three article images no longer count as final release assets.

## Remaining Risk

`visual_quality_review` is currently a structured review gate, not an automated image-semantic critic. It must be filled by the Agent or human reviewer after inspecting the raster. This is intentional for this iteration: the immediate goal is to prevent metadata pass from masquerading as publication-ready image quality.
