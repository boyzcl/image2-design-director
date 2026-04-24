# Direct-First Full Regression 2026-04-24

## Purpose

This benchmark checks the routing change made on 2026-04-24:

> Image2 owns the image. Post-processing only owns fixed, exact, or scannable elements.

The test covers two layers:

1. Direct-first asset classes:
   - cover
   - base visual
   - workflow
   - advance / explainer
   - evidence
   - data figure
   - price figure
   - ranking figure
2. Surgical post-processing:
   - QR replacement
   - exact text patch

## Generated Inputs

| Scenario | File | Route |
|---|---|---|
| Direct-first matrix | `generated/direct-matrix.png` | Image2 direct |
| QR replacement base | `generated/qr-base.png` | Image2 direct, model-generated placeholder QR |
| Text patch base | `generated/text-base.png` | Image2 direct, editable title and metric zones |
| Provided QR fixture | `fixtures/provided-qr.png` | user-provided fixture substitute for regression |

## Post-Processing Outputs

| Scenario | File | Result |
|---|---|---|
| QR replacement | `postprocess/qr-replaced.png` | pass |
| Exact text patch | `postprocess/text-edited.png` | pass |

Detailed machine-readable results:

- `review/postprocess-regression-results.json`

## Visual Review

### Direct-First Matrix

Result: `pass`

The matrix correctly exercises all direct-first classes in one Image2 direct generation. The data, price, and ranking panels remain visually designed publication assets instead of collapsing into plain deterministic tables. This supports the new route rule.

Notes:

- This is a regression contact sheet, not a final article asset.
- Some tiny labels are decorative and should not be treated as verified copy.
- For a real data / price / ranking asset, the reliability gate must still lock the source values before generation.

### QR Replacement

Result: `pass`

The base poster was generated as a complete asset with a model-made placeholder QR in a lower-right quiet zone. Post-processing replaced only that QR card with the provided QR fixture.

Verification:

- Provided QR hash recorded in `review/postprocess-regression-results.json`.
- Replacement target region diff ratio: `0.9933`.
- The poster layout, title, subtitle, and main illustration were not rebuilt.

### Exact Text Patch

Result: `pass`

The base image was generated as a complete asset with replaceable title and score zones. Post-processing patched:

- `Alpha Delivery` -> `Stable Gate`
- `Quality Score 72` -> `Quality Score 94`
- added `Release Gate: PASS`

First run issue:

- The title initially wrapped as `Stable Del / ivery`.
- The enlarged replacement zone also exposed why a conservative cover box is necessary: a small old-letter residue remained after the first pass.

Fix:

- Reduced title font pressure.
- Enlarged the replacement title panel to cover the full original title region.
- Re-ran the post-processing script.

Final verification:

- Title patch is single-line and readable.
- Old title residue is covered.
- Title region diff ratio: `0.9987`.
- Metric region diff ratio: `0.9979`.

## Conclusion

The direct-first routing update is behaving as intended.

Default route:

- cover / base / workflow / advance / evidence / data / price / ranking -> Image2 direct first

Post-processing route:

- QR / Logo / Exact copy / locked values / export adaptation -> surgical patch only

Important remaining rule:

If the whole image is weak, regenerate with Image2. Do not use post-processing to rebuild the image into a weaker design.
