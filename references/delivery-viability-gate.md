# Delivery Viability Gate

## Purpose

这份文档定义在已有第一版结果后，如何判断它是否仍适合继续 overlay、放 fixed elements 或做多尺寸交付。

一句话版本：

> delivery viability 是一个正式的 go / no-go gate，不是 placement tips。

## When To Trigger

满足以下任一项时进入：

- 继续叠标题、副标题、CTA、价格、日期
- 放入 QR、logo、badge
- 给视觉图补程序化图表或数值卡
- 准备出多尺寸版本

## Required Inputs

- 当前输出图
- `overlay_mode`
- `allowed_overlay_classes`
- `protected_regions`
- 计划进入的 overlay boxes
- 目标尺寸或导出需求

## Core Questions

1. 当前结果还有没有结构能力承载新增信息
2. 是否会侵入硬保护区
3. 与软保护区的碰撞风险有多高
4. overlay footprint 是否超过图像容量
5. 继续 overlay 会不会破坏资产类型或误导风险

## Output Values

### `overlay_allowed`

适用于：

- 无硬碰撞
- overlay footprint 可接受
- 新增信息不会破坏主次结构

### `overlay_allowed_with_limits`

适用于：

- 可以继续，但必须缩减 overlay 类别、密度或区域

常见限制：

- 只保留标题，不放 supporting copy
- QR 与 badge 二选一
- 不做 dense info layout

### `overlay_not_allowed_regenerate`

适用于：

- 硬保护区被侵入
- overlay 已明显压垮版式
- 当前图的 representation 已经不适合承载新增信息

默认动作：

- 回到生成或 representation 选择，而不是继续补字

## Minimal Checker Contract

最小可用 checker 至少输出：

- `delivery_viability`
- `collision_risk`
- `overlay_coverage_ratio`
- `hard_region_hits`
- `soft_region_hits`
- `continue_overlay_or_regenerate`

## Default Threshold Hints

- 硬保护区碰撞：默认 `0` 容忍
- 软保护区碰撞：允许小范围擦边，但要记录风险
- overlay footprint：超过图像可承载范围时应降为 `with_limits` 或 `no_go`

## Hard Rules

- 不要把“能放进去”当成“还能交付”
- dense info overlay 失败时，优先怀疑 representation mode，而不是只怀疑排版技巧
