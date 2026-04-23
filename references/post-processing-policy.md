# Post-Processing Policy

## Purpose

这份文档定义 `image2-design-director` 在 strategy 与 delivery 之间的后处理决策规则。

它回答的不是工具怎么操作，而是：

- 什么情况下应该一次直出完整成品
- 什么情况下应该走 `visual_base_plus_post`
- 哪些任务不能因为安全起见就默认降成底图

一句话版本：

> 后处理是交付策略，不是默认保守出口；先服从交付物合同，再决定模型和后处理怎么分工。

## Core Principles

### 1. Contract Beats Habit

是否后处理，不先看“我们平时更喜欢哪种工作流”，而先看：

- 用户要的是成品还是底图
- 谁负责最后排版
- 这轮怎样才算可验收

### 2. Finished Asset Is A Valid Default

不要把：

- `text-safe base`
- `hero base`
- `visual plate`

当成默认出口。

只有当用户明确要求，或交付合同明确如此时，才把任务定义为底图任务。

### 3. Precision Still Matters

如果一个元素需要：

- 文案逐字正确
- 二维码可扫描
- logo 比例稳定
- 多尺寸复用

那它通常更适合后处理。

### 4. Post-Processing Is Not A Repair Penalty

后处理不是“模型不够好所以兜底”，而是正式交付策略的一部分。

## Output Modes

只承认三种判断值：

- `direct_output`
- `visual_base_plus_post`
- `undecided`

## Decision Rule Stack

### Rule 1. Check The Asset Contract First

如果下面大部分成立，优先保留 `direct_output`：

- `asset_completion_mode = complete_asset`
- `layout_owner = model`
- `acceptance_bar` 明确要求直接可用
- 允许文字范围有限且清晰
- 没有必须后置的高精度固定元素

### Rule 2. Check Precision Requirements

满足以下任一项时，优先转向 `visual_base_plus_post`：

- 有必须可扫码的二维码
- 有品牌 logo lockup 或合作方 logo
- 有价格条、平台 badge、认证标识
- 有必须跨多个尺寸稳定复用的精确信息

### Rule 3. Check Reuse Requirements

满足以下任一项时，优先转向 `visual_base_plus_post`：

- 同一主视觉要扩多个尺寸
- 未来还要换标题、换 CTA、换日期
- 需要同时交付无字版、上字版和不同导出版

### Rule 4. Check Completion-Sensitive Tasks

下列任务默认不应自动滑向底图：

- `brand promo poster`
- `brand poster`
- `launch poster`
- `project intro poster`
- `recruitment poster`

这些任务如果用户没有明确说“我后续自己排字”，则默认优先 `direct_output`。

### Rule 5. Check User Intent

如果用户明确说：

- “给我一张完整可用的海报”
- “我要直接能发的图”
- “不要半成品”

那就不要再把任务默认为底图工作流。

## Precision Matrix

| Element Type | Default Owner | Why |
|---|---|---|
| 主视觉氛围、构图、材质、场景 | model | 模型更适合承担视觉说服力 |
| 有限且已锁定的标题 / slogan / 副标题 | model or hybrid | 若合同要求成品直出，模型可承担 |
| 中文长正文、价格、日期、活动信息 | post-processing | 需要逐字准确与稳定排版 |
| QR code | post-processing | 必须可扫描 |
| logo / badge / 合作标识 | post-processing | 需要品牌正确性和比例稳定 |
| 多尺寸导出版 | post-processing | 属于交付操作，不是模型强项 |

## Hard Rules

### 1. QR Codes Must Be Post-Processed

二维码默认必须后置。

### 2. Brand / Promo / Launch Assets Are Not Base Visuals By Default

这类任务只有在用户明确要求底图时，才可定义成：

- `visual_base_plus_post`

### 3. Direct-Output Text Is Allowed When The Contract Is Clear

不要把“任务带文字”视为自动排除 `direct_output` 的理由。

当下面条件同时成立时，允许并且应优先考虑直出文本：

- 用户要完整成品
- 文案范围已锁定
- 语言已锁定
- 没有二维码 / logo / 多尺寸强依赖

## Prompt Implications

### When `direct_output`

prompt 应明确：

- 这是完整可用成品
- 允许出现的文字只有哪些
- 默认文案语言是什么
- 不允许额外小字、伪 UI 文案和品牌墙

### When `visual_base_plus_post`

prompt 应明确：

- 这是底图
- 最终标题 / 二维码 / logo 不在本轮生成
- 需要保留哪些安全区和留白区
