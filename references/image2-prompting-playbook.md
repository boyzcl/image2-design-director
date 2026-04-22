# Image2 Prompting Playbook

## 目的

把当前公开可验证的 `GPT Image / Image 2` 官方实践，翻译成这个 skill 可直接执行的 prompt 规则。

这份文档不是咒语库，而是为了回答两个问题：

1. 现在更容易出好结果的指令结构是什么
2. 这些规则如何落到产品图、社媒图、UI 图和 App 素材图

## 官方资料归纳

基于 2026-04-22 可访问的官方资料，当前更稳定的做法有这些共识：

- prompt 要明确说清主体、背景、风格、构图、光线/色彩、关键细节
- 要把最不能跑偏的约束直接写明，不要指望模型自己补全
- 需要图中文字时，要把文字写成精确文案，并把位置和用途说清
- 修图或二轮迭代时，要明确说“只改什么、保持什么不变”
- UI、logo、品牌图这类高结构任务，比泛艺术图更依赖结构化 prompt，而不是堆形容词
- 如果走 API，可以查看 `revised_prompt`，确认模型实际理解成了什么

参考：

- OpenAI Images guide: https://platform.openai.com/docs/guides/images/image-generation
- OpenAI Cookbook prompting guide: https://cookbook.openai.com/examples/multimodal/image-gen-1.5-prompting_guide/

## 当前推荐结构

### 基础版

适合 `direct` 路径，短而稳。

```text
Domain direction: <open-ended asset or scene direction>
Matched profile: <product-mockup | social-creative | ui-mockup | app-asset | custom | none>
Support tier: <accelerated | standard | exploratory>
Asset type: <具体资产类型>
Primary request: <用户想得到什么>
Objective: <这张图为什么存在>
Audience/context: <给谁看，在哪里用>
Subject: <主体>
Scene/backdrop: <场景与背景>
Style/medium: <商业摄影 / product-native launch creative / realistic UI mockup / ...>
Composition/framing: <镜头、布局、留白、透视>
Visual priorities: <1-3 个最重要约束>
Text (verbatim): "<必须准确出现的文案>"
Constraints: <必须保留、必须满足>
Avoid: <必须避免>
```

### 迭代版

适合 `repair` 路径。

```text
Change only: <这轮只改什么>
Keep unchanged: <这些必须保持>
```

## 一个重要补充

在真实产品资产任务里，很多失败并不是因为“约束太少”，而是因为：

- 给了太多执行细节
- 把模型从生成高质量视觉，带偏成执行版式说明

所以这个 skill 新的默认原则是：

> 对 Image2，优先给目标、边界和上下文；不要过早给很多局部执行步骤。

## 什么叫“目标、边界和上下文”

### 目标

- 这张图最终是什么资产
- 它要帮助完成什么任务
- 用户看到后应该形成什么判断

### 边界

- 最不能跑偏的 3 到 5 条约束
- 必须像什么
- 不能像什么

### 上下文

- 这个品牌或产品的真实气质
- 受众和使用场景
- 必要的产品原生锚点

## 什么不要过度给

- 精确坐标
- 过多版式分块说明
- 很细的 glow、装饰、局部摆放细节
- 像在描述前端页面布局一样描述一张图

这些细节一旦过多，常见结果是：

- 画面僵
- 视觉说服力下降
- 更像拼装稿，而不是生成结果
- 看起来“都对”，但就是不高级

## 已验证加速档案怎么写更稳

下面这四类不是能力边界，而是当前已经验证过的高置信加速档案。

### 1. `product-mockup`

重点不是“好看”，而是可信。

- 先写产品和用途
- 再写商业摄影语言
- 再写布局空间和材质重点
- 最后写不要什么

推荐写法：

- `Style/medium`: commercial product photography
- `Composition/framing`: hero-friendly layout with usable negative space
- `Visual priorities`: product credibility, material feel, layout usability

避免：

- 只写“premium / futuristic / beautiful”
- 没写镜头和留白
- 没写需要像商品图

### 2. `social-creative`

重点不是艺术感，而是传播感。

- 先写渠道语境和传播目标
- 明确是否要保留标题区、安全区域、文案区
- 写清是 feed creative、campaign visual 还是 launch card

推荐写法：

- `Asset type`: feed post / story visual / campaign creative
- `Objective`: feel like a real growth/design team creative
- `Visual priorities`: campaign usability, readable text area, believable brand tone

避免：

- 只做一张漂亮图
- 没有文案安全区
- 像 AI 海报而不是营销素材

### 3. `ui-mockup`

重点是界面可信。

- 明确平台、页面类型、主要任务
- 明确信息层级和真实度
- 约束随机 widget 和过度装饰

推荐写法：

- `Style/medium`: realistic product UI mockup
- `Composition/framing`: front-facing screen, limited perspective distortion
- `Visual priorities`: hierarchy, component consistency, task clarity

避免：

- “现代、炫酷、未来感 dashboard” 这种泛词
- 文字很多但结构不可信
- 像 UI 插画，不像产品界面

### 4. `app-asset`

重点是服务现有产品系统。

- 如果服务已有产品，先读本地主题、UI 规范和现有页面
- prompt 里直接写“derived from the existing product UI language”
- 把产品自己的结构语言写进 `Constraints`

推荐写法：

- `Style/medium`: product-native app asset
- `Visual priorities`: product compatibility, restrained system fit, trust
- `Constraints`: inherit the real product theme, spacing discipline, overlay language, and material restraint

避免：

- 只借颜色 token
- 画得比产品本体更花
- 变成通用 AI 品牌海报

## 文字和版式任务的额外规则

官方资料对“需要精确文字”的场景有帮助，但在高要求品牌物料里，仍要自己加更强约束。

推荐额外写：

```text
Text (verbatim): "测试用户招募"
Typography intent: clean Chinese typography, manually typeset feel, not auto-wrapped
Layout instruction: stable left-column grid, clear hierarchy between eyebrow, title, body, and footer
```

对于中文：

- 不只给文案内容，还要给断句意图
- 指定“人工排版感”，否则容易出现脚本折行感
- 如果任务是高要求品牌物料，优先让模型生成留有清晰文案区的视觉底图，不强迫它一次性烘焙最终中文排版

## Logo / Icon 任务的额外规则

官方 cookbook 明确覆盖了 logo 生成场景，但这个 skill 要更严格：

- 先描述品牌功能语义，不先堆风格词
- 强调 `simple silhouette`, `scalable`, `high contrast`, `minimal detail`
- 要写清 small-size readability
- 如果结果要进入真实交付，优先把 AI 结果当作方向草图，而不是直接当最终 icon 成品

推荐额外写：

```text
Visual priorities: strong silhouette, small-size readability, restrained detail
Constraints: vector-first feel, no tiny decorative marks that collapse at 64px
Avoid: poster-like effects, excessive glow, overly complex line work
```

## 我们这边最值得固定下来的 5 条规则

1. 先写资产用途，再写美学风格
2. 先写结构和约束，再写氛围
3. 文字要精确，改图要有 invariants
4. 服务既有产品时，必须先读产品本体
5. 高结构任务宁可短而硬，也不要长而虚

## 新增的第 6 条规则

6. 让模型负责“视觉说服力”，让后处理负责“精确排版”

## 更适合当前 skill 的三层框架

### Layer 1: outcome brief

只回答：

- 这张图是什么资产
- 为什么做
- 最终希望用户怎么理解它

### Layer 2: hard constraints

只保留 3 到 5 条：

- 产品原生一致性
- 主体与焦点
- 品牌或场景边界
- 一条最重要的反方向约束

### Layer 3: downstream composition

交给后处理：

- 精确中文排版
- 品牌 lockup
- 渠道尺寸
- 最终 CTA 和落版

## 可直接复用的最小模板

```text
Use case: <...>
Asset type: <...>
Primary request: <...>
Objective: <...>
Audience/context: <...>
Subject: <...>
Scene/backdrop: <...>
Style/medium: <...>
Composition/framing: <...>
Visual priorities: <...>
Text (verbatim): "<...>"
Constraints: <...>
Avoid: <...>
```

## 如果走 API，要额外做什么

- 生成后查看 `revised_prompt`
- 如果 `revised_prompt` 漂了，就在下一轮 prompt 里加强约束
- 对重要任务，保留原 prompt、revised prompt 和评分，方便进入 runtime 记忆
