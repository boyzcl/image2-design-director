# Profile Promotion Judgment 2026-04-22 M11

## Purpose

这份文档把 `m11_validation_thickening_and_promotion_activation` 期间新增样本收成第一份正式 profile judgement。

它处理的不是单张图过不过线，而是：

- 哪个方向应继续停在 `exploratory`
- 哪个方向已够进入 `standard`
- 哪些已验证档案当前继续 `keep`

## Evidence Stack Used

本轮判断主要基于下面证据：

1. raw captures
   - `<runtime-root>/captures/2026-04-22.jsonl`
2. benchmark runs
   - `docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md`
   - `docs/benchmarks/benchmark-run-2026-04-22-exploratory-editorial-report-cover.md`
   - `docs/benchmarks/benchmark-run-2026-04-22-exploratory-educational-visual-board.md`
   - `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-knowledge-product-poster.md`
   - `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-onboarding-learning-asset.md`
3. narrow repairs
   - `docs/experiments/destination-asset-identity-repair-2026-04-22.md`
   - `docs/experiments/text-discipline-repair-2026-04-22.md`
4. current policy
   - `docs/profile-promotion-policy.md`

## Judgment Summary

| Direction | Previous Tier | Current Decision | Confidence | Why |
|---|---|---|---|---|
| `protocol-native editorial / knowledge collateral` | `exploratory` | `promote_to_standard` | `medium-high` | 已有多条真实样本、可复述借用方式、至少一条标准转移正式通过 |
| `educational visual board for prompt-debug learning` | `exploratory` | `hold_in_exploratory` | `medium` | 已有清楚起点，但仍主要靠单方向样本，且 residual board literalness 还没完全跨过去 |
| `validated accelerated profiles` (`social-creative`, `ui-mockup`, `app-asset`, `product-mockup`) | `accelerated / existing validated set` | `keep` | `medium` | 本轮没有出现 accelerated regression 信号 |

## Decision 1. Promote `protocol-native editorial / knowledge collateral` To `standard`

### Promotion Unit

本轮不是把某一张图升级，而是把下面这组相邻方向收成一个可复述的方向簇：

- protocol explainer poster
- editorial report cover
- knowledge-product field-guide poster

它们共享的不是同一种画风，而是同一组可迁移的资产规则：

- `packet / route / score / prompt assembly` 这条 protocol-native 中间链路
- 明确的 `title-safe / masthead-safe` 结构
- 最终资产身份必须保持 `neutral collateral`
- 避免 scenic sample、consumer product、classroom board、generic sample board 漂移

### Why Gate A Is Now Met

对照 `docs/profile-promotion-policy.md` 的 `exploratory -> standard` gate：

1. 至少 `2` 条相关真实样本
   - 已满足
   - exploratory protocol visual
   - exploratory editorial report cover
   - standard transfer knowledge-product poster
2. 至少 `1` 条样本达到 `60+` 且 failure / correction / next input 明确
   - 已满足
   - protocol visual 从 `73.0 conditional_pass` 到 `84.0 pass`
3. 已形成可复述的 route 或 prompt-family 借用方式
   - 已满足
   - structured / hybrid collateral skeleton + protocol-native cards + neutral collateral identity
4. 不再完全依赖临场 improvisation
   - 已满足
   - report cover 与 knowledge-product poster 都复用了相同骨架

推荐项也已满足：

- 有 benchmark runs 支撑
- 有 repair 后明显提升

### Concrete Evidence

1. `protocol explainer poster`
   - 从 `56.0 fail` 提升到 `84.0 pass`
   - 说明这条方向不是偶然命中，而是可通过明确纠偏规则稳定修正
2. `editorial report cover`
   - candidate `83.5 conditional_pass`
   - 说明同一协议型骨架可迁移到 editorial collateral
3. `knowledge-product poster`
   - candidate `89.5 pass`
   - 说明同一方向已正式通过 `standard transfer`

### New Tier Promise

从现在起，这个方向最准确的系统承诺应变成：

- `support_tier: standard`
- 默认目标：较稳定拿到 `70+` 工作稿，常见情况下可直接逼近 `80+`
- 默认借用方式：
  - structured poster 或 hybrid editorial cover
  - packet / route / score / prompt assembly motifs
  - explicit collateral identity

### Current Boundary

这次 promotion 不是说这个方向已经 `accelerated`。

它当前仍不承诺：

- 默认 `85+`
- 无需 repair 直达成熟交付版
- 对所有 knowledge / editorial collateral 子类都高置信成立

当前边界应明确收在：

- protocol-native project collateral
- editorial report / field-guide / explainer poster

不应自动扩张到：

- dense classroom infographic
- real report layout with heavy body text
- fully delivered poster with exact QR / logo / multi-size packaging

## Decision 2. Hold `educational visual board` In `exploratory`

### Why Not Promote Yet

这条方向当前不是失败，而是还没到 promotion 时点。

原因：

1. 样本仍偏少
   - 当前主要是单一 benchmark 方向
2. 剩余问题虽然变窄，但仍稳定存在
   - `slight-board-literalness`
3. 还没有正式标准转移样本支撑
   - 还缺一次相邻 educational / learning asset transfer

### Current Promise

这条方向当前最准确的承诺仍是：

- `support_tier: exploratory`
- 已有稳定 diagnostic start
- failure / correction / next input 清楚

## Decision 3. Keep Existing Accelerated Profiles

本轮没有新的 accelerated regression 信号。

因此当前对既有 validated profiles 的判断是：

- `keep`

但本轮也没有额外做 accelerated regression run，所以这不是一次加固，只是：

- no-regression-observed

## Operational Follow-Up

这份 judgement 生效后，下一步最该做的是：

1. 在后续 standard / delivery runs 中，继续用 `protocol-native editorial / knowledge collateral` 作为 `standard` 方向来验证
2. 给 `educational visual board` 再补一条相邻 standard transfer
3. 不要因为 `slight-board-literalness` 再回去改大范围 prompt system

## Final Judgment

本轮正式 judgment 收口为：

> `protocol-native editorial / knowledge collateral` 从 `exploratory` 晋升到 `standard`；`educational visual board` 继续 `hold in exploratory`；既有 accelerated profiles 本轮 `keep`。
