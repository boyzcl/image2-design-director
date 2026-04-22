# Post-Processing Policy

## Purpose

这份文档定义 `image2-design-director` 在 `Stage 2. Strategy Selection` 与 `Stage 6. Delivery And Assetization` 之间的后处理决策规则。

它回答的不是：

- 后处理工具具体怎么操作

它回答的是：

- 什么情况下可以一次直出
- 什么情况下必须走 `visual_base_plus_post`
- 模型负责什么，后处理负责什么
- 文本、二维码、logo、badge、尺寸适配应如何分层处理

一句话版本：

> 让模型负责视觉说服力，让后处理负责精确控制；任何需要准确、稳定、可复用落位的内容，都不应默认交给模型硬生成。

## Position In The Loop

这份 policy 主要服务三个节点：

- `Stage 1. Requirement Intake`
  - intake 只判断当前更像 `direct_output`、`visual_base_plus_post` 还是 `undecided`
- `Stage 2. Strategy Selection`
  - strategy 负责做最终裁决
- `Stage 6. Delivery And Assetization`
  - delivery 阶段根据这里的规则决定是否进入文本叠加、固定元素落位、尺寸适配和版本化

## Core Principle

### 1. Accuracy Beats Convenience

如果一个元素需要：

- 文案准确
- 位置稳定
- 多尺寸复用
- 品牌一致

那它默认应后处理，而不是交给模型“一次顺手画出来”。

### 2. The Model Should Carry Atmosphere, Not Precision Typesetting

模型最擅长的是：

- 主视觉气质
- 构图关系
- 材质与镜头
- 场景说服力
- 留白和视觉焦点

模型不擅长稳定承担：

- 精确中文排版
- 长文本逐字正确
- QR code 可扫描
- logo lockup 正确比例
- badge、价格条、平台规范位的固定落版

### 3. Post-Processing Is Not A Repair Penalty

后处理不是“模型不够好所以兜底”，而是正式交付策略的一部分。

对于很多真实设计任务：

- 主视觉先生成
- 精确信息后置

本来就是更专业、更稳定的工作流。

### 4. Delivery Risk Should Decide The Policy

是否启用后处理，不要只看用户有没有主动提。

还要看：

- 如果这部分交给模型，会不会显著增加返工风险
- 如果后面要扩多尺寸，会不会难以复用
- 如果要对外发布，错误文本或错误 logo 的代价是不是过高

## Output Modes

本 policy 只承认三种判断值：

- `direct_output`
- `visual_base_plus_post`
- `undecided`

结构化字段里统一使用上面的下划线值。

如果在叙述文本里出现：

- `direct-output`
- `visual-base-plus-post`

应视为同一概念的自然语言写法，而不是另一套枚举值。

### `direct_output`

适用于：

- 结果本质上是纯视觉资产
- 不依赖高精度文本
- 没有必须准确落位的固定元素
- 不需要强依赖后续尺寸扩展

### `visual_base_plus_post`

适用于：

- 主视觉和精确信息应分层完成
- 本轮先生成可用底图、hero base、device scene、background plate 或 safe-layout visual
- 文本、二维码、logo、badge、CTA、渠道尺寸在后续补齐

### `undecided`

只允许出现在 intake 结束时。

一旦进入 strategy 阶段，必须收敛到：

- `direct_output`
- 或 `visual_base_plus_post`

## Packet Field Alignment

当该 policy 被写回 intake、strategy 和 task packet 时，建议最少对齐下面这些字段：

| Layer | Field | Expected Value |
|---|---|---|
| intake | `direct_output_vs_post_process` | `direct_output` / `visual_base_plus_post` / `undecided` |
| strategy | `output_mode` | `direct_output` / `visual_base_plus_post` |
| strategy | `delivery_involvement` | `image-only` / `image-plus-delivery-ops` |
| task packet | `constraint.direct_output_vs_post_process` | 继承 intake 或 strategy 收敛结果 |
| task packet | `strategy.output_mode` | strategy 最终裁决 |

## Decision Rule Stack

每次都按下面顺序判断，不要直接凭直觉决定。

### Rule 1. Check Precision Requirements

满足以下任一项时，优先转向 `visual_base_plus_post`：

- 有必须逐字准确出现的文本
- 有中文标题、副标题、卖点、按钮、价格、日期、活动名
- 有固定二维码且要求可扫码
- 有品牌 logo、合作方 logo、认证标识、平台徽章
- 有截图框、设备框、卡片标签等固定版式元素

### Rule 2. Check Reuse Requirements

满足以下任一项时，优先转向 `visual_base_plus_post`：

- 同一主视觉要扩多个尺寸
- 同一底图要用于多个渠道
- 未来还要改标题、换 CTA、换日期、换价格
- 需要同时交付无字版、留白版、上字版

### Rule 3. Check Delivery Risk

满足以下任一项时，优先转向 `visual_base_plus_post`：

- 图像要直接对外发布
- 错一个字、错一个 logo、错一个二维码都会造成明显损失
- 任务属于品牌首发、招募、上架、活动海报、项目 hero 等高价值物料

### Rule 4. Check Asset Type

下列资产类型默认更偏 `visual_base_plus_post`：

- `project hero`
- `launch poster`
- `feed creative`
- `recruitment visual`
- `App Store listing image`
- `device mockup with headline`
- `banner with CTA`
- `icon sheet`

下列资产类型更容易走 `direct_output`：

- 纯插图
- 无字氛围配图
- 无固定品牌元素的概念视觉
- 只用于探索方向的中间稿

### Rule 5. Check User Intent

如果用户明确说：

- “我要最终能直接发”
- “这版需要把标题、二维码、logo 一起做好”
- “之后还要适配多个尺寸”

那就不要把这轮定义成纯 `image-only` 直出任务。

至少要进入：

- `visual_base_plus_post`
- 且通常应开启 `image-plus-delivery-ops`

## Precision Matrix

| Element Type | Default Owner | Why |
|---|---|---|
| 主视觉氛围、镜头、材质、场景 | model | 模型更适合承担视觉说服力 |
| 安全留白区、文本承载区 | model | 需要在构图层提前预留 |
| 短英文装饰性词片，且不要求精确 | model | 可作为视觉纹理的一部分 |
| 中文标题、副标题、正文、CTA | post-processing | 需要逐字正确、可控排版 |
| 英文品牌文案、活动名、价格、日期 | post-processing | 对准确性和一致性要求高 |
| QR code | post-processing | 必须可扫描，不能靠模型伪造 |
| logo、合作方 logo、认证标识 | post-processing | 需要比例、清晰度和品牌正确性 |
| badge、标签、价格角标 | post-processing | 需要精确对齐和多尺寸稳定 |
| 平台尺寸适配、导出版本 | post-processing | 属于交付操作，不是模型强项 |

## Base Visual Prompt Implications

一旦任务被判为 `visual_base_plus_post`，prompt assembly 阶段应主动把“底图职责”说清楚，而不是模糊地让模型顺带把所有元素都做掉。

### Prompt Should Explicitly Ask For

- 主视觉焦点
- 构图稳定性
- 文本安全区或留白区
- 能承载后续文案的干净背景
- 适合后续叠加 logo、二维码、badge 的落位区域

### Prompt Should Usually Avoid

- 最终中文标题直接嵌入图中
- 真实二维码直接让模型生成
- 真实品牌 logo lockup 直接让模型生成
- 活动日期、价格、报名信息等精确信息直接写死
- 看似真实但无法校验的 pseudo-UI copy

### Preferred Prompt Framing

更推荐把 prompt 写成：

- “生成可交付底图”
- “保留右上角安全留白用于后续标题或 badge”
- “no embedded final copy, no QR code, no logo lockup, clean composition for downstream layout”

而不是：

- “把标题、二维码、logo、按钮、日期全部一起做完”

## Hard Rules

下面这些规则属于强规则，不建议例外。

### 1. QR Codes Must Be Post-Processed

二维码默认必须后置。

原因：

- 模型生成的二维码不可保证可扫描
- 视觉上“像二维码”不等于功能上可用
- 一旦后续尺寸变更，模型生成的伪二维码不可稳定复用

### 2. Verbatim Chinese Text Must Be Post-Processed

凡是逐字正确很重要的中文文本，默认优先后置。

包括：

- 标题
- 副标题
- 海报文案
- CTA
- 价格与日期
- 报名说明

但这条规则不是“模型无法完成中文海报”的硬结论。

如果满足下面任一项，应保留至少一个 `direct_output` 候选做真实测试：

- 用户给出了模型已能直出的参考图
- 当前任务本身就在测试模型直出长中文海报的能力
- 任务价值高，值得比较 `direct_output` 与 `visual_base_plus_post`

### 3. Brand Logos And Lockups Must Be Post-Processed

凡是必须准确代表品牌身份的 logo 或 lockup，默认后置。

不要把品牌识别准确性交给模型碰运气。

如果当前只是要表达“这里将来有品牌位”，可以让模型预留：

- logo area
- brand bar
- badge slot

但不能把模型生成的伪 logo 视为正式交付元素。

### 4. Multi-Size Delivery Defaults To Post

如果明确要：

- 同图适配多个尺寸
- 同底图导出多个版本
- 同主题换不同文案

默认使用 `visual_base_plus_post`。

### 5. Device Screens With Real UI Copy Should Usually Post

如果 device mockup 里的重点是：

- 真实标题
- 真实功能名
- 真实操作按钮
- 真实数值

那屏幕内容通常不应完全靠模型一次写死。

### 6. Fake Precision Should Not Count As Delivery

下面这些内容即使视觉上“像那么回事”，也不能算交付完成：

- 不可扫描的二维码
- 拼写不稳定的标题
- 伪造的品牌名或 logo
- 看起来像真实数据但不可验证的 UI 数值

如果任务需要这些内容真的可用，就必须进入后处理或其他精确交付步骤。

## Soft Rules

下面这些规则允许例外，但默认按此执行。

### 1. Text-Safe Beats Text-Embedded For High-Value Assets

高价值主视觉默认优先争取：

- 构图稳定
- 留白干净
- 文字区清晰

而不是强求一次生成完整标题与排版。

### 2. Decorative Microtext Can Stay In The Image

如果文字只是装饰背景的一部分，且不承担真实信息传达，可以允许模型生成：

- 极短英文标签
- 非核心界面噪音文本
- 抽象纹理化字形

前提是：

- 不会误导为真实可读信息
- 不会损伤资产可信度

### 3. Early Exploration Can Stay Direct

如果本轮只是探索视觉方向，而不是交最终资产，可以先走：

- `direct_output`
- `image-only`

但一旦要进入真正交付，应重新判断是否改为 `visual_base_plus_post`。

## Default By Use Case

### `product-mockup`

默认：

- 商品主体、光影、场景由模型负责
- 价格条、促销角标、logo lockup、渠道标题由后处理负责

当它是纯商品摄影感探索时，可以暂时直出。

### `social-creative`

默认：

- 高价值传播图优先 `visual_base_plus_post`
- 先做 hero base、visual plate 或 text-safe visual
- 最终标题、CTA、二维码、活动信息后置

### `ui-mockup`

默认：

- 如果只是表达产品方向，可直接生成结构感强的 UI visual
- 如果要体现真实产品名、导航名、按钮、数值和品牌 copy，优先后置或把真实内容嵌入后续交付流程

### `app-asset`

默认：

- onboarding visual、功能配图、marketing card 可先做无字或弱字视觉
- App Store、listing、功能卖点图更偏 `visual_base_plus_post`

## Delivery State Contract

当任务走 `visual_base_plus_post` 时，至少要显式区分三个状态：

1. `raw_visual`
   - 模型刚生成的底图
2. `text_safe_visual`
   - 已确认留白和文本安全区可用的底图
3. `delivery_ready_visual`
   - 已完成文本、固定元素、尺寸和导出要求的交付版

这三个状态的细化流程由后续 `delivery ops` 文档展开，但在策略层必须先承认它们是不同状态。

## Strategy Handoff Contract

一旦判为 `visual_base_plus_post`，策略层至少要把下面这些信息交给后续阶段：

```yaml
output_mode: "visual_base_plus_post"
post_process_plan:
  text_policy: "post"
  fixed_element_policy: "post"
  size_adaptation_policy: "post"
  required_safe_areas:
    - ""
  deferred_elements:
    - ""
  delivery_targets:
    - ""
  post_process_reasoning:
    - ""
```

### Minimum Required Fields

| Field | Meaning |
|---|---|
| `required_safe_areas` | 哪些区域必须为空或足够干净 |
| `deferred_elements` | 哪些元素不由模型承担，留到后处理 |
| `delivery_targets` | 后续要落到哪些渠道、尺寸或版本 |
| `post_process_reasoning` | 为什么本轮不能简单直出 |

## Override Rules

### Allow Override To `direct_output` Only When All Hold

只有同时满足下面条件，才允许从默认后处理路径覆盖回 `direct_output`：

- 没有必须准确的文本
- 没有固定二维码、logo、badge
- 没有强烈多尺寸交付要求
- 本轮只是中间稿或探索稿
- 错误信息即使出现，也不会造成对外风险

### Escalate To `visual_base_plus_post` Even If User Did Not Ask

即使用户没主动提后处理，只要出现下面任一项，也应主动升级：

- 要求准确中文标题
- 要求二维码
- 要求品牌 logo
- 要求多个尺寸或最终投放
- 当前任务是高价值正式资产

### Keep A `direct_output` Candidate When Evidence Says It Is Plausible

如果用户已经给出：

- 参考图
- 现成成功样本
- 或明确要求测试直出能力

则不要把 `visual_base_plus_post` 当成唯一合法路径。

更合理的做法是：

- 把它升成 `multi-candidate`
- 并行比较 `direct_output` 与 `visual_base_plus_post`

## Example Judgments

### Example 1. README Hero For An Open Source Project

情况：

- 需要项目 hero 图
- 后续会叠中文标题
- 还要裁成社媒首发图

判断：

- `visual_base_plus_post`

原因：

- 主视觉可先生成
- 标题和多尺寸适配都不应一次写死

### Example 2. Recruitment Poster With QR Code

情况：

- 要做招募海报
- 必须带二维码
- 标题和报名时间必须准确

判断：

- `visual_base_plus_post`

原因：

- 二维码、标题、日期都属于高精度固定信息

### Example 3. Exploratory Product Mood Visual

情况：

- 只想先看产品摄影气质
- 没有固定文案
- 没有渠道尺寸要求

判断：

- `direct_output`

原因：

- 当前重点是方向探索，不是正式交付

### Example 4. App Store Feature Card

情况：

- 需要强调一个功能卖点
- 最终需要平台规范尺寸
- 标题必须与产品文案一致

判断：

- `visual_base_plus_post`

原因：

- 平台资产和卖点文案都要求高一致性和多尺寸稳定性

## Common Failure Patterns

如果没有遵守本 policy，最常见的问题会是：

- 中文标题歪掉或错字
- logo 被模型画错
- 二维码不可扫描
- 一换尺寸就破坏版式
- 主视觉和后续交付目标脱节
- 图像看起来不错，但不能真正发布

## Completion Checklist

当一次任务被判定为 `direct_output` 或 `visual_base_plus_post` 时，应至少自检下面这些问题：

- 这轮是否存在必须逐字正确的文本
- 这轮是否存在必须准确的二维码、logo、badge
- 这轮是否需要安全留白区
- 这轮是否要扩多个尺寸或多个版本
- 这轮是否属于高价值对外资产
- 当前判断是为了交付稳定性，而不是为了省一步操作

如果上面任一项回答为“是”，就必须认真论证为什么还能直出；否则默认进入后处理路径。
