# Text Discipline Repair 2026-04-22

> Historical validation note: 这份文档记录的是一次已完成的 experiment 或 repair run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录在 `destination asset identity` 修正之后，对剩余 `minor_text_discipline_leak` 做的一轮最小 repair。

这轮不再处理 scenic drift，而是只验证：

> 当 destination panel 已经回到 neutral project collateral 后，再加 `placeholder-only / no readable labels` 约束，是否能继续压掉可读小字。

## Trigger

上一轮 repair 已经证明：

- scenic drift 被压下去
- 但 destination panel 里仍有 readable labels / interface-like text

对应文档：

- `docs/experiments/destination-asset-identity-repair-2026-04-22.md`

## Repair Strategy

保持不变：

- `domain_direction`
- `matched_profile: none`
- `support_tier: exploratory`
- protocol-native 主链路
- neutral project collateral examples

只新增一组文字纪律约束：

- `placeholder blocks`
- `no readable labels`
- `no interface copy`
- `no microtext`

## Prompt Under Test

```text
A clean square poster for an AI workflow protocol explainer. Bright editorial background, one central transformation from a rough packet card into a route trace, scorecard chips, prompt assembly sheet, and a delivery-ready neutral project collateral panel. The final destination panel must read as neutral project collateral such as a README hero plate, onboarding visual card, or benchmark board preview, built from abstract system surfaces, placeholder blocks, and editorial layout shapes with no readable labels, no interface copy, and no microtext. Do not render scenic photographs, architecture, room scenes, framed art prints, or travel-style samples. Clear top-third title-safe area with no rendered text. Premium product-design poster, restrained slate blue and warm neutral palette, no logos, no fake brand text, no sci-fi clutter, no consumer product semantics.
```

## Output

- generation_id: `ig_00c2e76377d7b9100169e8d3d02c708191871acbc7400a749b`
- image_ref: `<generated-images-root>/019db552-7ffb-7b91-96db-97d3c520b5fa/ig_00c2e76377d7b9100169e8d3d02c708191871acbc7400a749b.png`

## Assessment

- what_improved:
  - readable labels 基本被压成 placeholder blocks
  - destination panel 继续保持 neutral project collateral
  - scenic / architecture drift 没有回流
- what_still_leaked:
  - 最终 panel 现在略偏 literal UI board
  - 更像一个干净的 benchmark board preview，而不是更自由的 editorial collateral crop

## Score

- total: `84.0`
- result: `pass`

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4.0 | 20 | 16.0 | protocol explainer poster 方向继续成立 |
| product_native_fit | 4.5 | 15 | 13.5 | neutral project collateral 保持稳定 |
| structure_and_composition | 4.0 | 15 | 12.0 | 主链路和安全区都稳定 |
| asset_credibility | 4.0 | 15 | 12.0 | 最终 panel 已更像真实 collateral preview |
| text_and_layout_fidelity | 4.5 | 10 | 9.0 | readable labels 明显下降 |
| craft_finish | 4.0 | 10 | 8.0 | 工艺干净 |
| anti_ai_artifact | 4.0 | 10 | 8.0 | scenic drift 与字噪音都被压下去 |
| iteration_clarity | 5.0 | 5 | 5.0 | 如果还要 polish，变量已收束为 board literalness |

## Runtime Memory

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- session_id: `image2-design-director-exploratory-protocol-visual-text-discipline-repair`

## Decision

这轮结果说明：

1. destination asset identity repair 是值得保留的默认规则
2. placeholder-only text discipline 也是有效的 follow-up tightening

当前问题已经继续缩小为：

- `slight-ui-board-literalness`

如果继续做下一轮，它将是 polish，而不是继续救火。

## Next Action

- keep: `allowed examples + hard exclusions + placeholder-only panel text discipline`
- change_next: 只在需要更高审美完成度时，再把 destination panel 从略 literal 的 board preview 进一步收成更 editorial 的 collateral crop
