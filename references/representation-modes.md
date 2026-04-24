# Representation Modes

## Purpose

这份文档定义 `image2-design-director` 的表达机制层。

一句话版本：

> representation strategy 回答的不是“要不要后置”，而是“这类信息最适合由哪种系统承载”。

## Supported Modes

### `model_direct_visual`

适用于：

- 封面
- 基础图
- workflow / advance / evidence 图
- 数据图、价格图、排行图在 reliability gate 通过后的第一轮成品直出
- 社媒、品牌、文章发表类完整视觉资产

默认特征：

- `primary_expression_system = image_model`
- `text_generation_tolerance = headline_only`、`limited_structured_text` 或更低
- `deterministic_render_needed = false`

### `model_visual_with_limited_text`

适用于：

- 模型可承担短标题、短 slogan、有限 supporting copy
- 但不承担精确数字或重信息图层

### `visual_base_plus_post`

适用于：

- 主视觉已由模型完成
- 只需要补 QR、Logo、Exact copy、锁定数值或导出适配
- 用户明确要无字版、底图版或多尺寸交付包

### `hybrid_visual_plus_deterministic_overlay`

适用于：

- Image2 候选已经成立
- 少量精确数字、价格、时间标签或法务文本必须确定性替换

这是外科式确定性修补路径，不是默认图片制作路径。

### `deterministic_render`

适用于：

- 图表本身就是主要交付物
- 精确值和结构是第一优先级
- 用户明确要求程序化图表、表格、规范化披露，或 Image2 直出已经失败

## Decision Heuristics

### Prefer `model_direct_visual` When

- 结果主要靠视觉说服力
- 用户要封面、基础图、workflow、advance、evidence
- 用户要数据图、价格图、排行图，且 reliability gate 已完成
- 文字范围有限，或 exact copy 可在后期局部修

### Prefer `visual_base_plus_post` When

- 需要 QR、Logo、Exact copy 或 locked value replacement
- 用户明确要底图、无字版或交付细化
- 后期范围能保持为局部补丁

### Prefer `hybrid` Or `deterministic` When

- 局部锁定值必须逐字逐数正确，且 Image2 候选整体已经可用
- 用户明确要求程序化图表、严格表格或合规披露
- 模型文本失真会直接破坏可用性，且局部替换不足以修复

## Hard Rules

- 高事实敏感任务默认不应跳过 reliability gate
- 需要 exact overlay 的局部元素，不应被扩大成整张图的后期主制作
- 当 dense info layout 已经超出底图容量，优先换 mode，不要只继续压排版
