# Text Overlay Policy

## Purpose

这份文档定义 `image2-design-director` 在交付阶段如何处理标题、副标题、CTA、价格、日期等文本叠加问题。

它回答的是：

- 哪些文字必须后置
- 底图需要预留什么样的文本安全区
- 什么情况下只交付无字版，什么情况下需要直接做上字版
- 文字叠加后，什么样才算没有破坏主视觉

## Core Principle

### 1. Text Accuracy Comes Before Visual Convenience

只要文字承担真实信息传达，就默认优先后置。

### 2. Overlay Should Respect The Image, Not Fight It

叠字不是把空白塞满，而是让文字与主视觉形成稳定层级。

### 3. Text-Safe Is A Real Delivery State

能承载文字的底图不是“差半步”，而是正式交付中间态。

## Text Classes

### Class A. Must Overlay

默认必须后置的文本：

- 中文标题
- 中文副标题
- CTA
- 价格
- 日期
- 报名信息
- 活动名
- 精确卖点文案

### Class B. Usually Overlay

通常更适合后置的文本：

- 英文品牌文案
- section heading
- feature label
- onboarding headline

### Class C. May Stay Decorative

可以允许留在图里的文字：

- 不承担真实含义的短装饰英文
- 作为纹理的微型字样
- 不需要校验正确性的背景符号

前提是：

- 不会被误读为真实主文案
- 不会降低资产可信度

## Overlay Modes

### 1. `text_safe_only`

适用于：

- 本轮先交底图
- 文案还没确定
- 需要后续由别的流程接手排版

输出：

- 干净底图
- 明确文本承载区说明

### 2. `title_plus_supporting_text`

适用于：

- 有明确主标题和少量辅助信息
- 海报、hero、feature card 等常见资产

### 3. `dense_info_layout`

适用于：

- 同时有标题、副标题、CTA、价格、日期等多层信息

默认提醒：

- 如果信息密度过高，先检查这张底图是否还适合承载
- 不要因为硬塞信息破坏主视觉

## Safe Area Rules

### 1. Safe Area Must Be Planned, Not Hoped For

如果任务预期要叠字，底图阶段就必须明确：

- 左侧标题区
- 顶部标题条
- 右上 badge 区
- 底部说明区

至少要有其中一种明确结构，而不是等交付时才发现“哪里都能放一点”。

### 2. Text Should Not Sit On Visually Noisy Surfaces

默认避免把主文案压在：

- 高细节纹理
- 强高光区域
- 人脸或产品主体上
- 复杂 UI 区块上

### 3. Safe Area Must Survive Target Crops

如果后面要裁不同尺寸，文本安全区在主要目标比例下都必须可用。

## Overlay Hierarchy Rules

### 1. Start With One Primary Message

每张图先确定：

- 哪一句是一级信息

其他文字都只能服务它。

### 2. Do Not Let Text Weight Exceed Image Capacity

如果叠字后：

- 主体被压弱
- 焦点被打散
- 留白被吃光

那不是文字还不够精细，而是底图不适合当前信息量。

### 3. Shorter Beats Denser

在交付层，宁可：

- 短标题
- 少量辅助文案

也不要把一张主视觉逼成文字海报。

## By Asset Type

### `project hero`

默认优先：

- 大标题
- 一行支持说明
- 可选轻 CTA

### `social-creative`

默认优先：

- 强主标题
- 一条活动或传播信息
- 如有二维码或 CTA，注意与标题分区

### `ui-mockup`

默认优先：

- 让图片承担界面解释
- 文字只补外部说明

不要让主标题和 UI 内文本互相抢。

### `app-asset`

默认优先：

- 短标题
- 短卖点
- 保持渠道截图或卡片感

## Red Flags

出现以下任一项时，当前文字叠加应视为不过线：

- 中文断句像机器拼接
- 文字区过满
- 文案压到主体焦点
- 不同信息层级权重混乱
- 明明需要无字版，却只保留了上字版
- 文字一换尺寸就失衡

## Hard Boundary

下面这些情况不能算交付完成：

- 标题虽然“看起来对”，但逐字未校验
- 关键日期、价格、CTA 仍留在模型生成文本里
- 本该保留无字版复用，但只留下单一上字版

## Delivery Contract

当任务涉及文字叠加时，建议在交付计划里补齐：

```yaml
text_overlay_plan:
  overlay_mode: "title_plus_supporting_text"
  primary_message: ""
  supporting_text:
    - ""
  safe_area_definition:
    - ""
  no_text_version_required: true
  target_sizes:
    - ""
```

## Example Judgments

### Example 1. Hero With Pending Copy

判断：

- 只交 `text_safe_only`

原因：

- 文案还未定，先保底图复用价值

### Example 2. Recruitment Poster

判断：

- `title_plus_supporting_text`

原因：

- 需要清晰标题和少量报名信息，但不应把二维码区挤占掉

### Example 3. Feature Card With Too Much Copy

判断：

- 当前底图不适合直接交付

动作：

- 减文案
- 或回到 repair / 重新生成更适合承载文字的底图

## Completion Checklist

- 这轮文字是否都属于应后置的文本类别
- 底图是否存在稳定可用的 safe area
- 叠字后是否仍保住主体焦点
- 是否需要同时保留无字版
- 主要目标尺寸下文字层级是否仍成立
