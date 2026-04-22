# Destination Asset Identity Repair 2026-04-22

> Historical validation note: 这份文档记录的是一次已完成的 experiment 或 repair run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录针对 `destination_asset_identity_gap` 做的一轮最小 repair。

目标不是重开泛化架构讨论，而是只验证一件事：

> 把 `delivery-ready asset frame` 改写成更具体的 `neutral project collateral` 语言之后，能否压掉 scenic / architecture sample drift。

## Trigger

上一轮 exploratory benchmark 的关键结论是：

- protocol-native 中间链路已经成立
- 但最终 destination asset frame 仍被模型补成风景 / 建筑样张

对应基线文档：

- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md`

## Repair Strategy

这次只改一个变量：

- `destination asset identity`

保持不变：

- exploratory scene
- `matched_profile: none`
- `support_tier: exploratory`
- `direct` route
- top title-safe area
- `packet -> route -> scorecard -> prompt assembly` 协议链路

## What Was Tightened

这次不是只说“中性项目资产”，而是把 destination state 写成两层：

1. allowed examples
   - `README hero plate`
   - `onboarding visual card`
   - `benchmark board preview`
2. hard exclusions
   - `landscape photograph`
   - `architecture render`
   - `room scene`
   - `framed art print`
   - `travel-style sample`

## Prompt Under Test

```text
A clean square poster for an AI workflow protocol explainer. Bright editorial background, one central transformation from a rough packet card into a route trace, scorecard chips, prompt assembly sheet, and a delivery-ready neutral project collateral panel. The final destination panel must read as neutral project collateral such as a README hero plate, onboarding visual card, or benchmark board preview, built from abstract system surfaces and editorial layout blocks, not a landscape photograph, architecture render, room scene, framed art print, or travel-style sample. Clear top-third title-safe area with no rendered text. Premium product-design poster, restrained slate blue and warm neutral palette, no logos, no fake brand text, no sci-fi clutter, no consumer product semantics.
```

## Output

- generation_id: `ig_00c2e76377d7b9100169e8d259e0ec819194876082f9364c82`
- image_ref: `<generated-images-root>/019db552-7ffb-7b91-96db-97d3c520b5fa/ig_00c2e76377d7b9100169e8d259e0ec819194876082f9364c82.png`

## Assessment

- what_improved:
  - scenic destination drift 被明显压下去
  - 最终 panel 更像 neutral project collateral，而不是风景样片
  - `packet -> route -> scorecard -> prompt assembly` 主链路仍保持可读
- what_still_leaked:
  - destination panel 里仍会出现一些可读小标签 / interface-like text
  - 说明 asset identity 已被修对，但 text discipline 还没完全收紧

## Score

- total: `80.0`
- result: `conditional_pass`

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4.0 | 20 | 16.0 | 已明显更像 protocol explainer poster |
| product_native_fit | 4.0 | 15 | 12.0 | destination state 已更项目化 |
| structure_and_composition | 4.0 | 15 | 12.0 | 结构稳定，安全区仍成立 |
| asset_credibility | 4.0 | 15 | 12.0 | 最终 panel 更像真实 collateral preview |
| text_and_layout_fidelity | 3.5 | 10 | 7.0 | 没有大标题污染，但小标签仍偏多 |
| craft_finish | 4.0 | 10 | 8.0 | 工艺仍干净 |
| anti_ai_artifact | 3.5 | 10 | 7.0 | scenic drift 下降，但 readable label leak 仍在 |
| iteration_clarity | 4.5 | 5 | 4.5 | 下一轮变量已收敛到 text discipline |

## Runtime Memory

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- session_id: `image2-design-director-exploratory-protocol-visual-destination-asset-repair`

## Decision

当前应把这次 repair 的结论收束为：

1. `destination asset identity` 这一条默认规则值得保留
2. 当前最大 open issue 已从 scenic drift 下降到 `minor_text_discipline_leak`

也就是说，这一轮已经证明：

> 问题不在 scene system，而在更细的 destination panel 文本纪律。

## Next Action

- keep: destination asset identity 必须继续写成 `allowed examples + hard exclusions`
- change_next: 在同一 prompt 上继续加一条更强的 no-readable-label / placeholder-only 约束，测试最终 collateral panel 是否还能保持中性且更干净
