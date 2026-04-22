# Delivery Toolization Priority 2026-04-22

## Purpose

这份文档把 `m11` 新增样本里暴露出的 delivery friction 收成真实优先级，而不是凭直觉排序。

## Evidence Used

主要依据：

- `docs/benchmarks/benchmark-run-2026-04-22-delivery-heavy-event-signup-poster.md`
- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-editorial-report-cover.md`
- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-educational-visual-board.md`
- `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-knowledge-product-poster.md`
- `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-onboarding-learning-asset.md`
- `references/delivery-ops.md`
- `references/text-overlay-policy.md`
- `references/fixed-element-placement.md`

## Repeated Frictions Observed

本轮新增样本里，真正重复出现的不是“图生成不出来”，而是下面三类 friction：

1. `text-safe_visual` 已经成立，但缺低摩擦方法推进到 `delivery_ready_visual`
2. QR / logo / CTA / date 这类 precision overlay 仍必须后置，而且目前没有顺手的版本化链路
3. 多尺寸适配是明确存在的需求，但在本轮里仍属于第二层问题，因为它依赖前两层先成立

## Priority Ranking

### 1. `text-safe -> delivery-ready` 版本化

判断：`highest priority`

原因：

1. 这是本轮 delivery-heavy run 的主阻塞
   - candidate 已是可信 `text_safe_visual`
   - 但没有低摩擦链路推进到 `delivery_ready_visual`
2. 它比单点 overlay 更基础
   - 没有状态版本化，就很容易在加字、加二维码、裁尺寸时把底图弄坏
3. 它和多数真实交付任务都相关
   - poster
   - hero
   - learning asset
   - social creative

最值得优先工具化的不是某一个按钮，而是一条明确的资产版本链：

- `raw_visual`
- `text_safe_visual`
- `delivery_ready_visual`

### 2. fixed-element overlay

判断：`second priority`

原因：

1. QR / logo / badge / CTA 都是 precision objects
   - 当前依然不能靠模型直出替代
2. delivery-heavy run 已证明 reserved zones 可以由生成阶段解决
   - 但真正可交付仍卡在 overlay 动作本身
3. 这一层的价值非常直接
   - 一旦有稳定 overlay 链路，许多 text-safe 底图就能真正交付

但它排在第二位，而不是第一位，因为：

- 如果没有版本化状态管理，单独做 overlay 容易反复覆盖和污染源底图

### 3. size adaptation

判断：`third priority`

原因：

1. 它是真需求，但本轮还没表现成最频繁的第一阻塞
2. 它依赖上面两层
   - 先要有可复用的 text-safe / delivery-ready 版本
   - 再谈 crop-aware fan-out
3. 目前我们更缺的是“先把一张图交付对”，而不是“同时交很多尺寸”

## Why This Order Is Better Than The Alternatives

### Why Not Put Fixed-Element Overlay First

如果先只做 QR / logo overlay，很可能得到的是：

- 可以放元素
- 但没有明确源版本管理
- 每次修改都要人工回忆哪个底图才是正确母版

这会把交付链路做成局部补丁，而不是稳定系统。

### Why Not Put Size Adaptation First

如果先做尺寸适配，当前最可能发生的是：

- 把还没真正 ready 的底图扩散成更多尺寸
- 把 overlay 问题和版本问题一起放大

所以 size adaptation 更适合在前两层成立后再做。

## Recommended Toolization Scope

最小可执行优先项应是：

1. 建一个 delivery bundle contract
   - 明确源底图、text-safe 版、delivery-ready 版的命名和关系
2. 在这个 bundle 上叠一个 fixed-element overlay pass
   - 标题
   - 日期 / CTA
   - QR
   - logo
3. 再在 delivery-ready 版上做 size fan-out
   - 只保护焦点、safe area、fixed-element zones

## Final Decision

本轮 delivery toolization priority 正式收口为：

1. `text-safe -> delivery-ready` 版本化
2. fixed-element overlay
3. size adaptation

一句话版本：

> 当前最该先工具化的不是“怎么再多生成一张”，而是“怎么把已经成立的底图稳定推进成真正可交付资产”。 
