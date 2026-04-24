# Benchmark Run: Publication Regeneration V2

## Scenario

- date: `2026-04-24`
- evaluator: `Codex`
- scope: regenerate all three article publication assets through the new production protocol
- source repair plan: [publication-asset-production-and-release-repair-plan-2026-04-24.md](../articles/publication-asset-production-and-release-repair-plan-2026-04-24.md)

## Purpose

The previous validation only proved that old images would no longer pass the new release gate. This run verifies the other half:

> Can the repaired production process generate three new article assets that pass production preflight, publication identity review, visual quality review, runtime capture, and final release gate?

## Generated Assets

| Role | Output | Bundle Version |
|---|---|---|
| Figure A. Editorial cover | [editorial-cover-report-v2.png](../articles/assets/editorial-cover-report-v2.png) | `figure-a-cover / delivery_ready_visual-v003` |
| Figure B. Mechanism figure | [protocol-visual-mechanism-v2.png](../articles/assets/protocol-visual-mechanism-v2.png) | `figure-b-mechanism / delivery_ready_visual-v004` |
| Figure C. Workflow evidence | [workflow-evidence-v2.png](../articles/assets/workflow-evidence-v2.png) | `figure-c-workflow / delivery_ready_visual-v003` |

## Production Packets

| Role | Packet | Preflight |
|---|---|---|
| cover | [figure-a-cover-v2.json](../articles/assets/production-packets/figure-a-cover-v2.json) | `pass` |
| mechanism | [figure-b-mechanism-v2.json](../articles/assets/production-packets/figure-b-mechanism-v2.json) | `pass` |
| workflow | [figure-c-workflow-v2.json](../articles/assets/production-packets/figure-c-workflow-v2.json) | `pass` |

## Verification Results

| Asset | production_preflight | publication_review | visual_quality | score | runtime_capture | final_release |
|---|---|---|---|---:|---|---|
| cover v2 | `pass` | `pass` | `pass` | 95.0 | `true` | `pass` |
| mechanism v2 | `pass` | `pass` | `pass` | 95.0 | `true` | `pass` |
| workflow v2 | `pass` | `pass` | `pass` | 95.0 | `true` | `pass` |

## What Changed Versus The Old Images

### Cover

Old issue:

- deterministic report-page feel
- insufficient publication cover tension
- weak separation between title and visual system

V2 change:

- cover production packet explicitly selected hybrid route and deterministic text ownership
- title area is protected from the protocol stack
- visual system is pushed into a distinct focal region

### Mechanism

Old issue:

- paragraph-heavy cards
- broken English wrapping such as scorecard split
- mechanism explained by dense copy instead of structure

V2 change:

- production preflight enforces node-label-only structure
- mechanism is a compact six-node loop
- explanatory copy is moved out of the card bodies

### Workflow Evidence

Old issue:

- abstract device cluster and weak evidence specificity
- not enough concrete workflow artifacts

V2 change:

- required evidence objects are present: runtime capture, route trace, scorecard, delivery bundle, accepted asset state
- final gate is represented as a workflow condition, not a decorative endpoint

## Runtime Capture

The regeneration run wrote runtime captures to:

`/Users/boyzcl/.codex/skills/image2-design-director/runtime/captures/2026-04-24.jsonl`

Session ids:

- `article-cover-v2-production-regression-20260424`
- `article-mechanism-v2-production-regression-20260424`
- `article-workflow-v2-production-regression-20260424`

## Verdict

This run verifies the repaired process end to end:

- production packets are created before generation
- production preflight passes before generation
- new images are generated
- outputs are registered into delivery bundles
- runtime captures exist
- visual quality review passes
- final release gate passes

Result: `pass`

## Remaining Caveat

These v2 images validate the workflow and are stronger publication assets than the old set, but they were generated through the local deterministic / hybrid-style renderer rather than an external image model call. A future high-fidelity validation should repeat the same production packets with Image2 visual-base generation for the cover and workflow evidence roles, then use deterministic overlay for exact text.
