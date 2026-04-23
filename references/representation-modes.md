# Representation Modes

## Purpose

这份文档定义 `image2-design-director` 的表达机制层。

一句话版本：

> representation strategy 回答的不是“要不要后置”，而是“这类信息最适合由哪种系统承载”。

## Supported Modes

### `model_direct_visual`

适用于：

- 纯视觉品牌图
- 社媒氛围图
- 低事实负载的成品海报

默认特征：

- `primary_expression_system = image_model`
- `text_generation_tolerance = headline_only` 或更低
- `deterministic_render_needed = false`

### `model_visual_with_limited_text`

适用于：

- 模型可承担短标题、短 slogan、有限 supporting copy
- 但不承担精确数字或重信息图层

### `visual_base_plus_post`

适用于：

- 主视觉靠模型
- 标题、QR、logo、导出适配靠后置
- 需要复用底图

### `hybrid_visual_plus_deterministic_overlay`

适用于：

- 图像气氛、主体和构图靠模型
- 精确数字、图表、价格、时间标签靠确定性叠加

这是当前最小 deterministic asset path 的首选模式。

### `deterministic_render`

适用于：

- 图表本身就是主要交付物
- 精确值和结构是第一优先级

## Decision Heuristics

### Prefer `model_direct_visual` When

- `factual_sensitivity = low`
- 结果主要靠视觉说服力
- 文字范围有限且已锁定

### Prefer `visual_base_plus_post` When

- 需要 QR、logo、badge、跨尺寸复用
- 文字经常要变
- 用户明确要底图或交付细化

### Prefer `hybrid` Or `deterministic` When

- `factual_sensitivity = high`
- 任务核心是精确数据、时间、价格、对比
- 模型文本失真会直接破坏可用性

## Hard Rules

- 高事实敏感图表默认不应只靠模型写数字
- 需要 exact overlay 的任务，不应被伪装成“低风险直出”
- 当 dense info layout 已经超出底图容量，优先换 mode，不要只继续压排版
