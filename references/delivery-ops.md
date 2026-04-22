# Delivery Ops

## Purpose

这份文档定义 `image2-design-director` 如何把生成结果推进成真正可交付资产。

它回答的不是：

- 具体用哪个设计工具执行后处理

它回答的是：

- 一张图从底图到交付版要经历哪些状态
- 什么时候只需要 `image-only`
- 什么时候必须进入 `image-plus-delivery-ops`
- 尺寸适配、文字叠加、固定元素放置分别在什么阶段发生

一句话版本：

> delivery ops 的职责，是把“看起来不错的图”收束成“真的能用的资产”。

## Position In The Loop

这份文档主要服务：

- `Stage 5. Branching: Deliver Or Repair`
  - 决定当前结果是进入 repair，还是进入交付层
- `Stage 6. Delivery And Assetization`
  - 定义交付状态、转场条件和导出目标

它与下面两份子文档配合：

- `references/text-overlay-policy.md`
- `references/fixed-element-placement.md`
- `references/delivery-bundle-contract.md`

## Core Principle

### 1. Delivery Is A Separate Stage

图像生成通过，不等于交付完成。

只要任务包含下面任一项，就应把 delivery 视为独立阶段：

- 文本后处理
- 二维码或 logo
- 多尺寸版本
- 多渠道导出
- 需要无字版 / 上字版 / 终版并存

### 2. Preserve Reusable States

交付层不要只保留最终成品。

至少要保留：

- 可回退的底图
- 可复用的 text-safe 版本
- 已落版的 delivery-ready 版本

### 3. Adaptation Should Protect The Composition

尺寸适配不是随便拉伸或硬裁切。

目标是：

- 保留主视觉焦点
- 保留文本安全区
- 保留固定元素可落位空间

## Delivery Involvement Modes

### `image-only`

适用于：

- 当前只是验证视觉方向
- 本轮结果还是探索稿或中间稿
- 文本、固定元素、尺寸不在本轮范围

输出重点：

- `raw_visual`
- 可选附带评估结论

### `image-plus-delivery-ops`

适用于：

- 本轮目标接近可发版资产
- 已明确有文本、二维码、logo、badge、尺寸或导出约束
- 当前任务属于 `delivery_refinement`

输出重点：

- `raw_visual`
- `text_safe_visual`
- `delivery_ready_visual`
- 交付说明

## Canonical Delivery States

这份文档承认三个交付状态。

### 1. `raw_visual`

定义：

- 模型刚生成的可评估底图

必须满足：

- 主视觉方向已形成
- 基础构图可判断
- 可进入评分或 repair

还不要求：

- 文本准确
- 固定元素已落位
- 尺寸版本齐全

### 2. `text_safe_visual`

定义：

- 已确认文本区、留白区、元素承载区足够安全的底图版本

必须满足：

- 主要文本区足够干净
- 焦点不会与未来标题或 CTA 冲突
- 关键角落或边缘有可用落位空间
- 画面裁切后仍能保住信息承载结构

### 3. `delivery_ready_visual`

定义：

- 已满足当前任务的文本、固定元素、尺寸与导出要求的交付版

必须满足：

- 文本已准确
- 二维码 / logo / badge 已正确落位
- 所需尺寸已导出或导出策略已确认
- 没有明显破坏主视觉的后处理痕迹

## State Transition Rules

### `raw_visual -> text_safe_visual`

只有同时满足下面条件，才能升级：

- 构图已经稳定
- 留白区足够干净
- 后续叠字不会压坏主体
- 如果要放固定元素，已经存在合理落位区

否则应：

- 进入 repair
- 或重新生成更适合承载交付的底图

### `text_safe_visual -> delivery_ready_visual`

只有同时满足下面条件，才能升级：

- 文本叠加符合 [text-overlay-policy](text-overlay-policy.md)
- 固定元素放置符合 [fixed-element-placement](fixed-element-placement.md)
- 尺寸适配没有破坏层级与焦点
- 输出版本覆盖当前交付目标

### Direct Promotion To `delivery_ready_visual`

只有在低风险直出场景，才允许从 `raw_visual` 直接视为 `delivery_ready_visual`。

例如：

- 纯视觉配图
- 无文本无固定元素
- 无额外尺寸要求

如果存在任何精确交付约束，不建议跳过 `text_safe_visual` 这个中间状态。

## Delivery Package Contract

一个完整交付包建议包含下面对象中的一部分或全部：

| Asset | Required When | Meaning |
|---|---|---|
| `raw_visual` | 默认建议保留 | 原始底图 |
| `text_safe_visual` | 需要后续叠字或多版本时 | 留白已确认的底图 |
| `delivery_ready_visual` | 任务要求可直接使用时 | 最终交付版 |
| `alternate_sizes` | 多尺寸时 | 尺寸适配版本 |
| `delivery_notes` | 有后处理或裁切决策时 | 说明哪些元素如何落位 |

如果要把这些对象真正收成稳定资产链，默认应使用：

- `references/delivery-bundle-contract.md`
- `scripts/manage_delivery_bundle.py`
- `scripts/apply_delivery_overlay.py`
- `scripts/export_bundle_sizes.py`

### Minimum Delivery-Ready Bundle

当任务被判为 `delivery_ready_visual` 时，默认至少应交付：

- 最终可用版本
- 如有后续复用价值，则保留对应 `text_safe_visual`
- 如有尺寸要求，则保留主要目标尺寸版本
- 简短 `delivery_notes`

## Size Adaptation Policy

### 1. Prefer Designing A Strong Base Before Fan-Out

如果一个主视觉需要扩多个尺寸，默认先做：

- 一个最能承载主视觉关系的 base

再向外适配，而不是每个尺寸都从零乱做。

### 2. Preserve Three Things During Resize

尺寸适配时优先保护：

- 主体焦点
- 文本安全区
- 固定元素预留区

### 3. Large-To-Small Is Usually Safer Than Small-To-Large

默认更推荐：

- 先做结构稳定的大底图
- 再向更小尺寸收敛

因为小图放大更容易暴露：

- 细节不足
- 边缘发糊
- icon 与 badge 可读性下降

### 4. Re-Crop Before Re-Generate

如果尺寸不匹配，默认先判断：

- 是否可通过裁切解决
- 是否可通过扩边或留白解决

只有当核心构图已不适配目标比例时，才优先考虑重生成。

## Delivery Decision Ladder

每次都按下面顺序判断：

1. 当前结果有没有过线
2. 如果过线，它是 `raw_visual` 还是已具备 `text_safe_visual`
3. 这轮是否需要文字叠加
4. 这轮是否需要二维码、logo、badge 等固定元素
5. 这轮是否需要多尺寸或多渠道版本
6. 当前能不能形成 `delivery_ready_visual`

## Strategy And Packet Alignment

当 delivery ops 被显式启用时，strategy / task packet 至少要补齐：

```yaml
delivery_involvement: "image-plus-delivery-ops"
delivery_plan:
  current_state: "raw_visual"
  target_states:
    - "text_safe_visual"
    - "delivery_ready_visual"
  required_outputs:
    - ""
  delivery_targets:
    - ""
  text_overlay_needed: true
  fixed_element_needed: true
  size_adaptation_needed: true
```

建议最少字段映射如下：

| Layer | Field | Expected Value |
|---|---|---|
| strategy | `delivery_involvement` | `image-plus-delivery-ops` |
| strategy | `task_mode` | 常见为 `delivery_refinement` |
| task packet | `strategy.delivery_involvement` | 继承 strategy |
| task packet | `constraint.size_and_delivery_constraints` | 对应尺寸与导出目标 |
| task packet | `strategy.output_mode` | 通常为 `visual_base_plus_post` |

## Example Workflows

### Example 1. README Hero + Social Crop

流程：

1. 生成主 hero 底图
2. 修到留白和结构足够稳定
3. 标为 `text_safe_visual`
4. 叠中文标题与副标题
5. 裁出社媒首发图
6. 输出 `delivery_ready_visual`

### Example 2. Recruitment Poster With QR Code

流程：

1. 先生成主海报底图
2. 确认标题区和二维码区安全
3. 标为 `text_safe_visual`
4. 后置标题、报名时间、二维码、logo
5. 导出主尺寸与备份尺寸

对应第一版执行链可收成：

1. `init` bundle 并登记 `raw_visual`
2. `add-version` 登记 `text_safe_visual`
3. overlay 完成后再登记 `delivery_ready_visual`
4. 最后把多尺寸导出挂到同一个 bundle 下

### Example 3. Exploratory Visual Only

流程：

1. 生成并评估
2. 结果作为 `raw_visual` 保留
3. 不进入 delivery ops

## Common Failure Patterns

如果 delivery ops 缺失或执行顺序错位，最常见的问题会是：

- 图像本身不错，但叠字后变挤
- 文本安全区原本不存在，只能硬压主体
- 二维码或 logo 放上去像补丁
- 多尺寸版本各自像不同资产
- 最终只保留终版，后续无法复用底图

## Completion Checklist

- 当前任务是否需要从 `image-only` 升到 `image-plus-delivery-ops`
- `raw_visual` 是否足够稳定，值得进入交付层
- 是否已经形成可靠的 `text_safe_visual`
- 文本和固定元素是否已经分别按专门 policy 判断
- 多尺寸适配是否保护了焦点、留白和元素区
- 最终是否保留了可复用中间状态
