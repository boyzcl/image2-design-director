# Text Overlay Policy

## Purpose

这份文档定义交付阶段如何处理标题、副标题、CTA、价格、日期、badge 与说明文本。

一句话版本：

> overlay 不是“看哪里空就放哪里”，而是 delivery viability gate 通过后的受控注入；如果图像结构不再具备承载能力，正确动作是回退或重生成，不是继续硬塞。

## Core Principles

### 1. Text Accuracy Comes Before Visual Convenience

承担真实信息传达的文字，优先用可校验的方式输出。

### 2. Overlay Must Respect Protected Regions

每次 overlay 前，都应明确：

- `protected_regions`
- `allowed_overlay_classes`
- 当前 overlay mode

### 3. Dense Information Is Often A Representation Problem

如果要塞入：

- 标题
- 副标题
- CTA
- 价格
- 日期
- 图表或对比数据

先问“是不是应该换 representation mode”，而不是只继续压字距和字号。

## Overlay Classes

### Class A. Deterministic Or Exact Overlay

默认不交给模型生成文本本体：

- 价格
- 日期
- 排行
- 指标数值
- QR
- 法务 / 免责声明

### Class B. Limited Delivery Overlay

可在 viability gate 通过后进入：

- headline
- subtitle
- CTA
- badge
- 短 supporting copy

### Class C. Decorative Text

只有在不承担真实信息时才允许：

- 背景微型纹理字
- 无结论性的短英文装饰

## Overlay Modes

### `text_safe_only`

适用于：

- 文案未锁定
- 后续还要扩多个尺寸
- 当前只交可承载文本的底图

### `title_plus_supporting_text`

适用于：

- 标题明确
- 支持文本少
- 没有高密度数值信息

### `dense_info_layout`

适用于：

- 已确定这张图真的要承载高密度信息

默认前提：

- representation mode 允许
- viability gate 通过

如果这两个条件不成立，就不是 typography 问题，而是 route 或 representation 问题。

## Viability Rules

### 1. Safe Area Must Be Planned

预计要 overlay 时，底图阶段至少明确：

- 标题承载区
- footer band
- badge / logo / QR 区
- 受保护主体区

### 2. Hard Protected Regions Must Not Be Invaded

典型硬保护区：

- 人脸
- 产品主体
- 关键 UI 主区域
- 核心图表面板

### 3. Soft Protected Regions Need A Risk Budget

典型软保护区：

- 高光区
- 高纹理区
- 次级构图焦点

允许轻微擦边，但必须控制碰撞比例。

### 4. Overlay Footprint Must Match Image Capacity

如果 overlay 后：

- 主体被削弱
- 焦点被打散
- 留白被吃光
- 事实层与视觉层互相抢

则应判定为 `overlay_not_allowed_regenerate` 或至少 `overlay_allowed_with_limits`。

## Delivery Contract

当任务涉及 overlay 时，建议交付计划至少补齐：

```yaml
text_overlay_plan:
  overlay_mode: "title_plus_supporting_text"
  primary_message: ""
  supporting_text:
    - ""
  allowed_overlay_classes:
    - "headline"
    - "subtitle"
  protected_regions:
    - name: "subject_core"
      type: "hard"
      x: 0
      y: 0
      width: 0
      height: 0
  no_text_version_required: true
  target_sizes:
    - ""
```

## Red Flags

出现以下任一项时，当前 overlay 应视为不过线：

- 标题或 support 文案侵入硬保护区
- 关键信息落在高噪音表面上
- QR、logo、badge 与主标题互相争抢
- 文字密度已经超出图像可承载范围
- 改尺寸后布局立刻失衡

## Completion Checklist

- 这轮 overlay 是否通过 delivery viability gate
- 关键文本是否属于允许的 overlay 类别
- 硬保护区是否零侵入
- 是否保留了需要的无字版或底图版
