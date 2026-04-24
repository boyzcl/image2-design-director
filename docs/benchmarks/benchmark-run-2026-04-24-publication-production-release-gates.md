# Benchmark Run: Publication Production And Release Gates

## Scenario

- date: `2026-04-24`
- evaluator: `Codex`
- scope: production preflight, visual quality review, final release gate
- related repair plan: [publication-asset-production-and-release-repair-plan-2026-04-24.md](../articles/publication-asset-production-and-release-repair-plan-2026-04-24.md)

## Verification Intent

这次验证不重新生成图片。它验证两件事：

1. 制作前，错误 production route 会被 `production_preflight` 拦下。
2. 制作后，`publication_review = pass` 但图面质量不够的资产不会再被当作最终发布资产。

## Fixtures

- pass fixture: [publication-production-packet-mechanism-pass.json](fixtures/publication-production-packet-mechanism-pass.json)
- mechanism fail fixture: [publication-production-packet-mechanism-fail.json](fixtures/publication-production-packet-mechanism-fail.json)
- workflow fail fixture: [publication-production-packet-workflow-fail.json](fixtures/publication-production-packet-workflow-fail.json)

## Production Preflight Results

| Case | Expected | Actual | Key Blockers |
|---|---|---|---|
| mechanism valid packet | `pass` | `pass` | none |
| mechanism paragraph-heavy/model-text packet | `fail` | `fail` | `mechanism_text_density_too_high`, `mechanism_model_text_risk`, `mechanism_requires_structured_or_hybrid_route` |
| workflow missing evidence objects | `fail` | `fail` | missing `runtime_capture`, `scorecard`, `route_trace`, `accepted_asset_state`; `workflow_evidence_requires_multi_candidate` |

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

- production route failures are now caught before generation.
- visual quality failures are now separated from publication identity pass.
- final release cannot pass without production preflight, visual quality pass, and runtime capture.
- the current three article images no longer count as final release assets.

## Remaining Risk

`visual_quality_review` is currently a structured review gate, not an automated image-semantic critic. It must be filled by the Agent or human reviewer after inspecting the raster. This is intentional for this iteration: the immediate goal is to prevent metadata pass from masquerading as publication-ready image quality.
