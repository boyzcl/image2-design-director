# Post-Processing Policy

## Purpose

这份文档定义 `image2-design-director` 的 post-processing 决策规则。

一句话版本：

> 后处理不是默认制作路线，而是对 Image2 成品图的外科式确定性补丁；先让 Image2 负责完整视觉资产，再决定哪些固定元素必须后期处理。

## Core Principles

### 1. Image2 Owns The Asset

默认不要先想“哪些东西要后置”，而先判断：

- Image2 能否直接完成这张图的主体构图、层级、风格和可发布感
- 哪些元素确实必须逐字、逐数、可扫描或品牌一致
- 后期是否只是局部补丁，而不是整张图的主设计

### 2. Finished Asset Is Still A Valid Default

不要把：

- `text_safe base`
- `hero base`
- `visual plate`

当成默认出口。

如果合同要求完整成品，`direct_output` 是默认值。即便是数据图、价格图、排行图，也应先过 reliability gate，再优先让 Image2 直出成品；后期只修必须精确的局部元素。

### 3. Deterministic Precision Is A Surgical Layer

以下信息默认进入 post 或 hybrid，但范围必须收窄：

- QR
- Logo / brand lockup
- Exact copy
- 已确认必须替换的精确数值
- 已确认必须替换的价格、日期、排行
- 多尺寸导出适配

以下资产类型不因为含有信息就自动进入后期主制作：

- 数据图
- 价格图
- 排行图
- workflow 图
- evidence 图
- advance / explainer 图

### 4. Overlay Must Pass Viability

哪怕只是外科式后期，也不代表当前这版图仍然适合继续叠信息。

继续交付前必须判断：

- `delivery_viability`
- `protected_regions`
- `collision_risk`
- `continue_overlay_or_regenerate`

### 5. Post-Processing Must Not Weaken The Image

如果后期让图变得更像模板、更扁、更弱，默认动作不是继续工程化，而是回到 Image2 直出候选或重生成。

## Direct-First Asset Classes

这些任务默认先走 `direct_output` 或多候选直出：

- 封面
- 基础图
- workflow
- advance / explainer
- evidence
- 数据图
- 价格图
- 排行图

这些元素默认才进入后期：

- QR code
- Logo / brand lockup
- Exact copy
- locked value replacement
- export adaptation

## Output Modes

只承认下面 4 种输出模式：

- `direct_output`
- `visual_base_plus_post`
- `hybrid_render`
- `deterministic_render`

## Decision Rule Stack

### Rule 1. Start From Representation Mode

默认映射：

- `model_direct_visual` -> `direct_output`
- `model_visual_with_limited_text` -> `direct_output` 或 `hybrid_render`
- `visual_base_plus_post` -> `visual_base_plus_post`
- `hybrid_visual_plus_deterministic_overlay` -> `hybrid_render`
- `deterministic_render` -> `deterministic_render`

### Rule 2. Route Exact Information To The Right Owner

| Element Type | Default Owner | Why |
|---|---|---|
| 主视觉氛围、构图、场景 | model | 视觉说服力主由模型承担 |
| 封面、基础图、workflow、advance、evidence | model | 需要完整图面质量和设计判断 |
| 数据图、价格图、排行图 | model first, post only for locked values | 先保留 Image2 的整体视觉质量 |
| 已锁定且很短的 headline / slogan | model first, exact repair if needed | 可由模型承担有限文字 |
| 长中文正文、法务 copy、精确指标 | post | 需要逐字正确 |
| QR code | post | 必须可扫描 |
| logo / badge / 合作标识 | post | 需要品牌正确性 |
| 程序化图表、严格表格、合规披露 | deterministic only by explicit route | 这类任务不是普通 publication visual |

### Rule 3. Check Delivery Reuse Requirements

满足以下任一项时，才优先 `visual_base_plus_post` 或 `hybrid_render`：

- 必须放入可扫描 QR
- 必须使用真实 Logo 或品牌 lockup
- Exact copy 不能有任何字形、字符或断句偏差
- 已确认价格、日期、排行或指标必须替换为锁定值
- 同一主视觉要扩多尺寸，且平台裁切会影响可读性

### Rule 4. Completion-Sensitive Tasks Must Not Drift By Habit

下列任务默认不应因为“怕翻车”就自动降级成底图：

- `brand promo poster`
- `launch poster`
- `project intro poster`
- `social launch creative`
- `editorial cover`
- `workflow evidence figure`
- `data / price / ranking publication visual`

如果用户要完整成品，就应先尝试让 representation 真正服务成品，而不是直接退成中间稿。

### Rule 5. Overlay Requires A Go / No-Go Gate

进入 overlay 之前必须判断：

- 是否有硬保护区
- 是否会挤占主体焦点
- overlay 之后是否仍满足 `acceptance_bar`

如果结果是：

- `overlay_allowed`
  - 可以继续
- `overlay_allowed_with_limits`
  - 继续，但必须缩减 overlay 类别或密度
- `overlay_not_allowed_regenerate`
  - 回到生成或 representation 选择

## Hard Rules

### 1. QR Codes Must Not Be Left To Model Text

二维码默认必须后置。

### 2. Exact Numeric Claims Must Not Rely On Decorative AI Text

如果数字是结论核心，先走 reliability gate；如果必须逐数一致，再对局部数值走 exact overlay 或 replacement。不要因此默认把整张图改成 deterministic render。

### 3. High-Fact-Sensitivity Tasks Need Matching Representation

高事实敏感任务若跳过 reliability gate，默认视为 representation mismatch。通过 gate 后可以直出，但锁定值必须被复核，必要时只替换局部。

## Prompt And Render Implications

### When `direct_output`

prompt 应明确：

- 这是完整可用成品
- 可读文字范围
- 语言
- 不允许额外噪音文字

### When `visual_base_plus_post`

prompt 应明确：

- 这轮交底图
- 哪些元素不在本轮生成
- 哪些区是保留给 overlay 的
- 哪些区是 protected regions

### When `hybrid_render`

需要同时准备：

- 图像 prompt
- 确定性 overlay / chart spec
- overlay viability 检查输入
