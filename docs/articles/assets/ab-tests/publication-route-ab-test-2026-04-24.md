# Publication Route A/B Test

## Purpose

这次 A/B 不是测 prompt 的小差异，而是测两条生产路线：

- Route A: one-shot image generation
- Route B: production protocol + deterministic / hybrid post-processing

目标是回答：

> 同一主题、同一文章语义下，直接一次直出与协议化交付路线各自哪里强、哪里弱，哪条更适合作为 publication asset 主路径。

## Current Execution Status

Route A and Route B have both been executed.

Important correction:

Route A was generated with Codex built-in Image2, not a shell API path. The first version of this note incorrectly treated missing `OPENAI_API_KEY` as blocking image generation. That was wrong for Codex built-in image generation.

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

Actual outputs:

- [cover-one-shot.png](route-a-direct/cover-one-shot.png)
- [mechanism-one-shot.png](route-a-direct/mechanism-one-shot.png)
- [workflow-one-shot.png](route-a-direct/workflow-one-shot.png)

Runtime capture session ids:

- `route-a-direct-cover-ab-20260424`
- `route-a-direct-mechanism-ab-20260424`
- `route-a-direct-workflow-ab-20260424`

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
| title fidelity | surprisingly good, but not guaranteed | strong |
| Chinese readability | good on main text, risky on microcopy | strong |
| visual richness | strong | medium |
| publication cover energy | strong | medium-high |
| mechanism clarity | strong | strong |
| evidence object specificity | strong on workflow | strong |
| family consistency | medium | strong |
| unexpected design quality | strong | medium |
| repeatability | medium-low | strong |
| final release readiness | review candidate | pass |

## Actual Route Judgment

### Cover

Route A is more compelling as a cover. It has richer editorial polish, stronger depth, and a more persuasive protocol-stack motif.

Route A problems:

- adds extra explanatory copy beyond the intended text budget
- introduces many small labels that would need review
- less repeatable than Route B

Route B problems:

- cleaner and more controllable, but flatter
- feels more like a generated report cover than a top-tier editorial cover

Preference:

- production path: Route A direct
- post-processing: only if exact title replacement is required after review

### Mechanism

Route A is visually stronger than expected and the loop structure works well.

Route A problems:

- adds extra top and bottom explanatory text beyond the strict node-label-only contract
- may still invent small supporting labels

Route B problems:

- very clean and controllable
- less visually impressive and less publication-polished

Preference:

- production path: Route A direct
- post-processing: only exact node-label replacement if the direct candidate is otherwise strong
- Route B deterministic schematic is a fallback, not the default

### Workflow Evidence

Route A is clearly stronger visually. It shows concrete workflow objects and feels like a real publication asset.

Route A problems:

- dense generated microcopy
- invented small text details
- hard to guarantee exact audit semantics

Route B problems:

- accurate and controlled
- too schematic compared with Route A

Preference:

- production path: Route A direct
- post-processing: only exact labels or locked evidence text if required
- if the evidence composition is weak, regenerate with Image2 rather than rebuilding in post

## Updated Recommendation

The route preference should be corrected.

Route A direct generation is the better default production path for this publication asset family. Route B-style deterministic / hybrid work should be demoted from "main production route" to "surgical post-processing route".

Default direct-first classes:

- cover
- base visual
- workflow
- advance / explainer
- evidence
- data figure
- price figure
- ranking figure

Default post-processing classes:

- QR code
- Logo / brand lockup
- Exact copy
- locked price / date / ranking / metric replacement
- export crop / padding / resize adaptation

In short:

> Image2 should own the image. Post-processing should only own fixed, exact, or scannable elements.

The verification gates still matter, but their job changes:

- `information_reliability_gate` locks the facts before direct generation.
- `visual_quality_review` decides whether the direct image is actually publishable.
- `delivery_viability_gate` is only entered when a surgical post-process patch is needed.
- `final_release_gate` checks the finished asset after any exact patch.

Route B remains useful as a repair lane, not as the default lane. If a direct Image2 candidate is visually strong but has a wrong QR, Logo, title character, price, date, ranking, or exact value, patch that element. If the whole image is weak, regenerate with Image2 instead of trying to engineer a weaker design in post.
