# Default Family Spot Check 2026-04-22

> Historical validation note: 这份文档记录的是一次已完成的 experiment 或 repair run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录在默认规则晋升之后，对两条最敏感 family 做的一轮小规模真实 spot-check：

- `hybrid structured hero`
- `structured / section-based poster`

目标不是再开一轮大 benchmark，而是验证：

- 把 repair 规则写回默认规范后，是否不依赖显式 `repair` framing 也能维持方向
- 还剩下哪些默认层面的漏洞

## Setup

- date: `2026-04-22`
- mode: `tightened default prompt check`
- generation host: `Codex Image2`
- image directory: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/`
- source defaults:
  - `references/prompt-schema.md`
  - `references/prompt-assembly.md`
  - `references/sample-prompts.md`
  - `SKILL.md`

## Spot Check 1: Tightened Repo Hero Default

### Prompt

```text
Create a repo README hero for the project image2-design-director. Make it feel like a real AI-native design system for turning rough image requests into shippable assets. Audience and context: open-source repo hero with a large clean copy-safe area on the left. Main subject: one protocol-native focal cluster built from intake packet cards, route decision nodes, prompt assembly layers, scorecard chips, and delivery-ready asset frames. Scene and backdrop: bright editorial workspace atmosphere with calm depth, not a dark sci-fi void. Composition: wide hero, focal cluster on the right, stable hierarchy, generous breathing room, highly usable for README copy. Text layer: no rendered headline, no fake labels, preserve a clean left-side copy-safe area. Style: premium product-marketing visual with crisp system surfaces, restrained warm-neutral and slate-blue palette, believable design polish. Constraints: keep the image system-like rather than dashboard-like; if a review frame appears, keep it neutral and non-domain-specific. Avoid consumer product semantics, backpacks, furniture, ecommerce listings, shopping UI, generic tech wallpaper, random floating widgets, fake startup branding, and neon cyberpunk effects.
```

### Output

- generation_id: `ig_06879615dd6fdf130169e8b47e43ac81918ece9d78e7ca379e`
- image_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_06879615dd6fdf130169e8b47e43ac81918ece9d78e7ca379e.png`

### Assessment

- what_worked:
  - left-side copy-safe area 非常稳定
  - `packet / route / scorecard / delivery-state` 的协议型视觉语言已经成立
  - 消费品、电商、shopping 语义没有再回流
- what_still_leaked:
  - 最终 asset frame 仍被模型补成了偏风景/建筑样张
  - 项目系统感已经对了，但 destination asset identity 还要再写得更死一点

### Score

- total: `82.5`
- result: `conditional_pass`

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4.0 | 20 | 16.0 | repo hero 方向稳定成立 |
| product_native_fit | 3.5 | 15 | 10.5 | 系统语言对了，但 asset frame 仍不够项目中性 |
| structure_and_composition | 4.5 | 15 | 13.5 | 留白和主次很好 |
| asset_credibility | 4.5 | 15 | 13.5 | 已经像能用于 README 的高质量底图 |
| text_and_layout_fidelity | 4.5 | 10 | 9.0 | 无误文字污染，safe area 成立 |
| craft_finish | 4.5 | 10 | 9.0 | 工艺干净 |
| anti_ai_artifact | 3.5 | 10 | 7.0 | 仍有一点“模型自己补样张”的习惯 |
| iteration_clarity | 4.0 | 5 | 4.0 | 下一轮变量很明确 |

## Spot Check 2: Tightened Launch Poster Default

### Prompt

```text
Create a square launch poster for image2-design-director. Goal: make it feel like a real project launch asset rather than a generic design poster. Audience and context: social feed creative for builders and design-minded AI users. Main subject: one bold transformation from rough prompt intent into a delivery-ready visual system. Render the exact headline text "Prompts That Ship" as the only headline, large in the top third. Structure: square poster with one dominant center-axis transformation and a clean top-third title zone. Transformation core: rough brief packet becoming route trace, scorecard marks, prompt assembly sheet, and a delivery-ready asset frame. Supporting atmosphere: restrained supporting lines and accents that reinforce the packet-to-asset transition without decoration spam. Text layer: one main headline only, no subtitle, no badge wall, no secondary captions, no fake logos. Style: bold campaign poster, dark graphite background, restrained electric blue accents, crisp contrast, controlled glow, clean breathing room. Avoid furniture ad cues, generic logo poster language, dashboard board layouts, fake brand lockup, made-up UI, and abstract geometry that has no project mechanism.
```

### Output

- generation_id: `ig_06879615dd6fdf130169e8b4bfebd08191b9b9bca8d3fa7baa`
- image_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_06879615dd6fdf130169e8b4bfebd08191b9b9bca8d3fa7baa.png`

### Assessment

- what_worked:
  - 标题控制继续成立，主标题是唯一显著文字层
  - `brief -> route -> scorecard -> asset` 的项目机制已经成为海报主干
  - 泛 logo poster / 家具广告 / 纯几何海报感被明显压下去
- what_still_leaked:
  - 最终 asset 仍偏风景样张
  - brief 和 spec sheet 里还带了一点不必要的小字噪音

### Score

- total: `82.0`
- result: `conditional_pass`

| Dimension | score_0_5 | weight | weighted | notes |
|---|---:|---:|---:|---|
| intent_match | 4.5 | 20 | 18.0 | 发布海报方向明确成立 |
| product_native_fit | 3.5 | 15 | 10.5 | 项目机制已对，但最终 asset 还不够中性项目化 |
| structure_and_composition | 4.5 | 15 | 13.5 | 标题区和主轴都很稳 |
| asset_credibility | 4.0 | 15 | 12.0 | 已像对外 campaign draft |
| text_and_layout_fidelity | 4.0 | 10 | 8.0 | 主标题稳定，但次级小字仍可更克制 |
| craft_finish | 4.5 | 10 | 9.0 | 工艺和对比干净 |
| anti_ai_artifact | 3.5 | 10 | 7.0 | 仍有模型自动补细碎说明字的倾向 |
| iteration_clarity | 4.0 | 5 | 4.0 | 默认层面的下一步很清楚 |

## Combined Judgment

这轮 spot-check 说明两件事：

1. 把 repair 规则晋升为默认规范是对的
2. tightened default 已经能在不显式声明 `repair` 的情况下维持方向

但也暴露了一个新的共性缺口：

- 只写 `delivery-ready asset frame` 还不够，默认还要补 `destination asset identity`

换句话说，当前默认写法已经从“hero / poster 方向不稳”前进到“方向已稳，但最终 asset 类型还要更中性、更项目化”。

## Default Update Triggered By This Spot Check

spot-check 后，默认规范又额外补了一条：

- 如果 prompt 里出现 `review frame`、`delivery-state frame`、`delivery-ready asset`
- 默认继续约束这个最终资产应是中性项目资产
- 不要让模型自行补成风景、建筑或别的强垂类样张
