# Publication Route A/B Test

## Purpose

这次 A/B 不是测 prompt 的小差异，而是测两条生产路线：

- Route A: one-shot image generation
- Route B: production protocol + deterministic / hybrid post-processing

目标是回答：

> 同一主题、同一文章语义下，直接一次直出与协议化交付路线各自哪里强、哪里弱，哪条更适合作为 publication asset 主路径。

## Current Execution Status

Route B has been executed end to end.

Route A is prepared but not executed because this local shell has no `OPENAI_API_KEY`. The route A prompts are ready and should be run through a real image generation backend before final visual comparison.

## Shared Theme

Article:

《我为什么还是做了 image2-design-director，当 gpt-image-2 已经这么强之后》

Figure set:

1. Editorial cover
2. Mechanism figure
3. Workflow evidence visual

## Route A. One-Shot Direct Generation

### Contract

- single image generation call per figure
- model owns the whole layout and visible text
- no deterministic overlay
- no post-process repair before first evaluation

### Expected Advantages

- higher visual richness and unexpected composition
- more organic image-model aesthetics
- stronger chance of cover-level energy

### Expected Risks

- Chinese title fidelity
- broken English labels
- paragraph overgeneration
- fake UI text or invented labels
- weak control over evidence objects
- inconsistent figure family

### Output Status

Prepared prompts:

- [route-a-direct-cover-prompt.txt](route-a-direct-cover-prompt.txt)
- [route-a-direct-mechanism-prompt.txt](route-a-direct-mechanism-prompt.txt)
- [route-a-direct-workflow-prompt.txt](route-a-direct-workflow-prompt.txt)

Actual output status:

- `blocked_missing_image_api_key`

## Route B. Production Protocol + Deterministic / Hybrid

### Contract

- production packet before generation
- preflight before generation
- deterministic ownership for exact text
- visual quality review and final release gate after generation

### Executed Outputs

- [editorial-cover-report-v2.png](../editorial-cover-report-v2.png)
- [protocol-visual-mechanism-v2.png](../protocol-visual-mechanism-v2.png)
- [workflow-evidence-v2.png](../workflow-evidence-v2.png)

### Result

All Route B outputs passed:

- `production_preflight = pass`
- `publication_review = pass`
- `visual_quality_review = pass`
- `final_release = pass`

Benchmark record:

- [benchmark-run-2026-04-24-publication-regeneration-v2.md](../../../benchmarks/benchmark-run-2026-04-24-publication-regeneration-v2.md)

## Comparison Rubric

When Route A outputs are available, compare both routes on:

| Dimension | Route A One-Shot | Route B Protocol |
|---|---|---|
| title fidelity | TBD | strong |
| Chinese readability | TBD | strong |
| visual richness | TBD | medium |
| publication cover energy | TBD | medium-high |
| mechanism clarity | TBD | strong |
| evidence object specificity | TBD | strong |
| family consistency | TBD | strong |
| unexpected design quality | TBD | medium |
| repeatability | TBD | strong |
| final release readiness | TBD | pass |

## Provisional Judgment

Until Route A is actually generated, Route B remains the only validated publication-ready path.

My expected preference:

- For cover: Route A may produce a more visually exciting base, but Route B is safer for final text.
- For mechanism: Route B is likely better because the task is structure-first and text-sensitive.
- For workflow evidence: Route A may create richer scenes, but Route B is more reliable at showing required evidence objects.

Likely best future path:

> Use Route A to explore visual bases for cover and workflow evidence, then promote the winning base into Route B for deterministic text, review, bundle, and release.

Mechanism figures should usually stay Route B-first.
