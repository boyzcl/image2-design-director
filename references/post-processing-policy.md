# Post-Processing Policy

## Purpose

这份文档定义 `image2-design-director` 的 post-processing 决策规则。

一句话版本：

> 后处理不是默认保守出口，而是 representation strategy 的一部分；先决定什么系统承载信息，再决定哪些内容进入后置，最后用 viability gate 判断这版图还能不能继续交付。

## Core Principles

### 1. Representation Beats Habit

不要先想“我们平时喜欢后置还是直出”，而先判断：

- 这轮关键信息该由什么表达机制承载
- 哪些元素必须确定性表达
- 当前结果还剩多少 overlay capacity

### 2. Finished Asset Is Still A Valid Default

不要把：

- `text_safe base`
- `hero base`
- `visual plate`

当成默认出口。

如果合同要求完整成品，且任务低事实风险，`direct_output` 仍然是有效默认值。

### 3. Deterministic Precision Is A First-Class Option

以下信息默认优先考虑 post 或 hybrid，而不是强行交给模型直出：

- 精确数值
- 价格、日期、排行
- QR
- logo lockup
- 多尺寸必须稳定复用的文案块
- 程序化图表

### 4. Overlay Must Pass Viability

哪怕 representation mode 允许 post，也不代表当前这版图仍然适合继续叠信息。

继续交付前必须判断：

- `delivery_viability`
- `protected_regions`
- `collision_risk`
- `continue_overlay_or_regenerate`

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
| 已锁定且很短的 headline / slogan | model or hybrid | 可由模型承担有限文字 |
| 长中文正文、价格、日期、精确指标 | deterministic or post | 需要逐字正确 |
| QR code | post | 必须可扫描 |
| logo / badge / 合作标识 | post | 需要品牌正确性 |
| 图表、对比表、数值卡 | deterministic or hybrid | 需要口径稳定 |

### Rule 3. Check Delivery Reuse Requirements

满足以下任一项时，优先 `visual_base_plus_post` 或 `hybrid_render`：

- 同一主视觉要扩多尺寸
- 后续还要换标题、换 CTA、换日期
- 需要同时交付无字版、上字版和平台适配版

### Rule 4. Completion-Sensitive Tasks Must Not Drift By Habit

下列任务默认不应因为“怕翻车”就自动降级成底图：

- `brand promo poster`
- `launch poster`
- `project intro poster`
- `social launch creative`

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

如果数字是结论核心，就应走 deterministic 或 exact overlay 路径。

### 3. High-Fact-Sensitivity Tasks Need Matching Representation

高事实敏感任务若仍走纯模型直出，并让模型承担精确数值或图表，默认视为 representation mismatch。

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
