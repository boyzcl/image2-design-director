# Market Map For `image2-design-director`

## Purpose

这份文档把当前市场上与 `image2-design-director` 相邻的产品能力做一次可执行收束。

目标不是做“竞品列表”，而是回答 5 个问题：

1. 市场上同类型能力主要分成哪些类
2. 它们各自解决什么问题
3. `image2-design-director` 和它们相比，真正独特的地方是什么
4. 哪些能力值得借鉴，哪些不该学
5. 接下来应该补哪些协议、路由和验证面

一句话版本：

> 市场上多数工具在卖单点能力；`image2-design-director` 更像把“资产判断 -> 生成 -> 验收 -> 交付”接成闭环的协议层。

## Executive Summary

当前市场上与本项目最接近的，不是某一个单独产品，而是一组分散能力的组合：

- `prompt rewrite`
- `style / character / composition reference`
- `brand / template / layout consistency`
- `variation / batch extension`
- `editable delivery`

这意味着：

- 我们不应该退化成“另一个 prompt enhancer”
- 也不应该只补“风格参考”一个 feature
- 更合理的方向，是继续把这些能力吸收到 `asset contract -> route -> acceptance -> delivery` 这条主线里

## Market Categories

### 1. Prompt Rewrite Layer

代表：

- Leonardo `Improve a Prompt`
- OpenAI image generation 的 `revised_prompt`
- Adobe Firefly `Prompt Guidance`

核心逻辑：

- 把用户原始输入改写成更适合模型的提示词
- 重点是提升 prompt 清晰度和模型可执行性

强项：

- 速度快
- 适合作为默认辅助动作
- 对新手友好

弱项：

- 不判断最终资产类型是否正确
- 不判断是否应该走“补 brief / 微修 / 重建理解”
- 对交付和系列一致性帮助有限

对我们的启发：

- 可以把 prompt rewrite 当作 skill 内部子动作
- 但不能把 skill 主身份写成 prompt rewrite

### 2. Style / Character / Composition Reference Layer

代表：

- Midjourney `Style Reference`
- Midjourney `Style Creator`
- Ideogram `Style Reference`
- Ideogram `Character Reference`
- Adobe Firefly `Style Reference`
- Adobe Firefly `Composition Reference`
- Adobe Firefly `Generative Match`
- Krea `Style transfer` / `Image prompt`

核心逻辑：

- 用参考图锁定某一类继承关系：
  - 风格
  - 角色
  - 构图
  - 结构

强项：

- 一致性控制强
- 对“复刻 / 换主体重做 / 同系列延展”非常有效
- 用户理解成本低

弱项：

- 大多只锁某一层，不处理完整交付物合同
- 经常默认“只要像参考图就算成功”
- 很少显式区分“保风格”和“保结构”

对我们的启发：

- 需要把“参考图约束”拆成多个一等字段，而不是只写“有参考图”
- 需要把“保什么”与“锁多强”协议化

### 3. Brand / Template / Layout Consistency Layer

代表：

- Adobe Firefly `Style IDs`
- Canva `Brand Kit`
- Canva `Magic Layers`
- Recraft 自定义 style / brand color / styles

核心逻辑：

- 让输出遵循既有品牌资产、版式系统、模板规则和设计标准
- 重点不是“做一张好图”，而是“做对一类可持续生产的图”

强项：

- 与真实组织工作流接近
- 对品牌一致性、模板复用、多尺寸适配帮助大
- 对设计生产可落地

弱项：

- 常常更像平台 feature，而不是跨模型协议
- 在“任务理解错了怎么办”这件事上通常不强
- 多数仍默认用户已经知道自己要什么

对我们的启发：

- 模板约束型任务应该成为一等场景，不只是一个例子
- 交付物合同里要明确“版式锁定”“品牌锁定”“结构锁定”

### 4. Variation / Batch Extension Layer

代表：

- Adobe Firefly Boards `Vary`
- Recraft `Image sets`
- Krea / OpenAI / Recraft 多图生成能力

核心逻辑：

- 在同一视觉系统下快速探索多个变体
- 保持一致性，同时提高方向探索效率

强项：

- 适合系列资产和方向探索
- 适合同风格多对象、多尺寸、多用途输出

弱项：

- 不一定知道什么时候应该先停下来重建合同
- 容易把批量变体误当成策略正确

对我们的启发：

- `series extension` 不该只是 trigger 文案，要进入 route 和输出协议
- 需要显式说明“整组哪些维度必须保持、哪些允许变化”

### 5. Editable Delivery Layer

代表：

- Canva `Magic Layers`
- Canva `Resize / Magic Switch`
- Adobe Firefly Boards 的继续编辑能力

核心逻辑：

- 让 AI 输出不是终点，而是进入继续编辑、改尺寸、替换元素、加文案的起点

强项：

- 更贴近真实交付
- 对社媒图、品牌图、README 视觉、活动海报很有价值

弱项：

- 大多数产品把它做成编辑器能力，不会自然回流到 prompt / route 判断

对我们的启发：

- 我们不一定要自己做编辑器
- 但要在协议层提前判断“是否需要为后续交付保留空间和结构”

## Where `image2-design-director` Is Different

当前版本和市场单点能力相比，最核心的不同有 4 点：

### 1. 它不是单点 feature，而是判断层

市场上大多在卖：

- 风格锁定
- 角色一致
- prompt 提升
- 品牌模板

而我们卖的是：

- 什么时候该直接生成
- 什么时候该先补 brief
- 什么时候该 repair
- 什么时候该 contract_realign

### 2. 它把“资产类型正确”放在“画面好看”前面

很多工具默认：

- 生成得像就够了

而我们当前协议强调：

- 资产类型不能错
- 成品度不能错
- 语言策略不能错
- 输出必须可验收

### 3. 它天然适合高误判成本任务

比如：

- 参考图换主体重做
- 同系列资产延展
- 教育海报 / 信息图 / 机制图
- 多约束成品交付
- 结果跑偏后的救火

这些任务一旦理解错，重试成本很高。

### 4. 它已经有“经验复利”这一层

市场上很多工具只优化单轮生成。

而本项目已经明确：

- capture
- review
- promote
- pattern

这让它更像长期协议层，而不是临时生成技巧。

## What We Should Borrow

### Borrow 1. 把“参考图角色”拆细

建议新增字段：

- `reference_role`
  - `style`
  - `composition`
  - `layout`
  - `character`
  - `brand`
  - `mixed`

原因：

- 市场已经证明“参考图”不是一个维度
- 同一张参考图可能承担完全不同的约束角色

### Borrow 2. 把“锁定强度”协议化

建议新增字段：

- `lock_strength`
  - `low`
  - `medium`
  - `high`
- `inheritance_mode`
  - `vibe_only`
  - `style_locked`
  - `composition_locked`
  - `near_remake`

原因：

- Midjourney、Firefly、Krea 都在做 influence / strength 这类控制
- 这说明现实任务不是“参考 / 不参考”二值问题

### Borrow 3. 把“系列资产”从 trigger 升级成路由概念

建议新增字段：

- `series_mode`
  - `single_asset`
  - `series_extension`
  - `batch_system`
- `series_invariants`
  - style
  - layout
  - density
  - palette
  - framing
  - text policy

原因：

- 系列任务不是多出几张图，而是多张图在同一系统里运动

### Borrow 4. 把“模板约束说明图”做成正式 lane

建议新增：

- `template-bound explainer asset` 对应的更明确 route / family

例如新增 prompt family：

- `structured annotated board`
  - 适用于教育海报、知识板、博物图鉴、复杂机制说明图

原因：

- 这类任务和品牌海报、UI mockup、单图叙事资产不是一回事
- 市场上已有 composition/template thinking，但协议层普遍不够强

### Borrow 5. 强化“交付后可编辑”的前置判断

建议新增字段：

- `post_delivery_editability`
  - `not_needed`
  - `copy_safe_required`
  - `overlay_expected`
  - `multi_size_expected`
  - `fixed_element_expected`

原因：

- Canva / Adobe 的编辑能力说明：很多真实任务成功与否，不在生成瞬间，而在后续适配

## What We Should Not Borrow

### Do Not Borrow 1. 不要退化成 prompt enhancer

原因：

- 市场上已经很多
- 一旦退化，`asset contract` 和 `route` 的差异化会直接消失

### Do Not Borrow 2. 不要把 style ref 当成总解

原因：

- 风格像，不代表资产对
- 参考图并不总是在锁“风格”

### Do Not Borrow 3. 不要把 skill 写成“凡生图必触发”

原因：

- 会破坏 trigger 清晰度
- 轻量壁纸、趣味头像、单步换背景不该走这套厚协议

### Do Not Borrow 4. 不要过早绑定某一家模型参数

比如：

- `--sref`
- 平台私有 slider
- 某家 style code

这些可以作为 adapter 层知识存在，但不该污染主协议。

## Proposed Contract Additions

建议分两批补。

### P0. 应尽快补到协议里的字段

- `reference_role`
- `lock_strength`
- `inheritance_mode`
- `series_mode`
- `series_invariants`
- `post_delivery_editability`

这批字段不要求先做脚本，也不要求先做 UI。

最低目标：

- 先让 skill 在任务判断和输出合同里显式使用这些概念

### P1. 适合补到 route / family / validation 的字段

- `template_class`
  - `campaign_poster`
  - `hero`
  - `ui_mockup`
  - `annotated_board`
  - `knowledge_poster`
  - `delivery_sheet`
- `reference_dependency`
  - `none`
  - `optional`
  - `critical`
- `series_change_policy`
  - `keep_layout_change_subject`
  - `keep_style_change_content`
  - `keep_system_change_scene`

## Proposed Route Expansions

当前 4 路由已经够清楚，但可以补两个“决策镜头”而不是新增大路由：

### 1. `reference-locked direct`

适用：

- 合同清楚
- 有明确参考锁定
- 目标是近似复刻或换主体重做

它仍属于 `direct`，但应该带一个更强的参考合同。

### 2. `series-extension direct`

适用：

- 已有视觉系统存在
- 新任务只是同系统扩展
- 关键不是重新定义资产，而是守住 invariant

它也仍可归在 `direct`，但输出合同应显式说明保持项和变化项。

结论：

- 不一定需要增加新 route 名称
- 更重要的是给现有 route 增加 mode

## Proposed Prompt Family Expansions

当前建议重点不是新增很多 family，而是精准补 1 到 2 个。

### 1. `structured annotated board`

适用：

- 教育海报
- 博物图鉴
- 机制图
- 多编号说明图
- 高信息密度视觉板

为什么值得补：

- 它和普通海报、hero、UI、自然语言单图叙事差异很大
- 最近“蝴蝶换青蛙”这类请求正好暴露了这个 gap

### 2. `series continuation asset`

适用：

- README 视觉系列
- 同一 campaign 套图
- 同一视觉系统下的补页和续页

为什么值得补：

- 当前 skill 已经有 `series extension` trigger，但 prompt family 还没有明确承接

## Proposed Trigger Refinements

当前 trigger 已经明显变强，但还可以继续精炼为：

### 强触发的真正本质

不是：

- “用户要做一张图”

而是：

- “资产类型、系列关系、版式结构、交付成品度中至少有一个维度不能错”

建议今后所有 trigger 判断都围绕这句话校验。

## Validation Plan

### P0. Trigger Surface

已经新增：

- `docs/benchmarks/trigger-regression-suite.md`

接下来建议每次改 trigger 都过这组样例。

### P1. 新场景 benchmark

建议新增 2 个 benchmark 场景：

1. `bm_reference_locked_subject_swap`
   - 参考图锁定 + 换主体重做
2. `bm_template_bound_annotated_board`
   - 复杂知识板 / 说明图 / 博物图鉴式任务

### P2. 输出合同 spot check

建议做一轮小型 spot check：

- 5 个真实请求
- 检查是否都能自然产出：
  - `Asset Contract Summary`
  - `Chosen Route`
  - `Acceptance Check`
  - `Next Action`

## Priority Recommendation

### P0. 立即做

- 把上面的合同字段补进 `SKILL.md` 语言层
- 新增 `bm_reference_locked_subject_swap`
- 新增 `bm_template_bound_annotated_board`

### P1. 下一轮做

- 明确 `structured annotated board`
- 明确 `series continuation asset`
- 在 runtime capture 里保留 `reference_role / lock_strength / series_mode`

### P2. 再下一轮做

- 评估是否需要更细的 adapter 层
- 针对不同模型写“参考锁定策略差异”
- 只在必要时补脚本，不急着工具化

## Decision

基于本轮调研，我对 `image2-design-director` 的判断是：

- 方向是对的
- 差异化是真实存在的
- 现在最该做的不是“补更多 feature”
- 而是把市场上已证明重要的那几层控制显式化：
  - 参考角色
  - 锁定强度
  - 系列 invariant
  - 模板约束
  - 交付后可编辑性

一句话收束：

> 我们不该变成另一个“会生图的平台 feature 集”，而该继续成为“把复杂图像任务收成可判断、可交付、可复利协议”的上层 Skill。

## Sources

官方来源，按能力类别列出：

- Midjourney Style Reference
  - https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
- Midjourney Style Creator
  - https://docs.midjourney.com/hc/en-us/articles/41308374558221-Style-Creator
- Ideogram Style Reference
  - https://docs.ideogram.ai/using-ideogram/features-and-tools/reference-features/style-reference
- Ideogram Character Reference
  - https://docs.ideogram.ai/using-ideogram/features-and-tools/reference-features/character-reference
- Krea Image
  - https://docs.krea.ai/user-guide/features/krea-image
- Leonardo Improve a Prompt
  - https://docs.leonardo.ai/reference/promptimprove
- Recraft Styles Overview
  - https://www.recraft.ai/docs/using-recraft/styles/styles-overview
- Recraft Getting Started
  - https://www.recraft.ai/docs/api-reference/getting-started
- Recraft Generating Multiple Images
  - https://www.recraft.ai/docs/recraft-studio/image-generation/generating-multiple-images
- Adobe Firefly Style Reference / Generative Match
  - https://helpx.adobe.com/in/firefly/how-to/generate-image-using-reference-image.html
  - https://www.adobe.com/products/firefly/features/generative-match.html
- Adobe Firefly Composition Reference
  - https://helpx.adobe.com/firefly/mobile/generate-images-with-text-to-image/customize-generated-images/match-image-composition-to-reference-image.html
- Adobe Firefly Boards Vary
  - https://helpx.adobe.com/firefly/web/create-mood-boards/firefly-boards/generate-image-variations.html
- Adobe Firefly Style IDs
  - https://helpx.adobe.com/firefly/web/firefly-design-intelligence/firefly-design-intelligence-for-illustator/generate-designs-with-style-ids.html
- Canva Brand Kit
  - https://www.canva.com/pro/brand-kit/
- Canva Magic Layers
  - https://www.canva.com/newsroom/news/magic-layers/
- OpenAI Image Generation Guide
  - https://developers.openai.com/api/docs/guides/image-generation
