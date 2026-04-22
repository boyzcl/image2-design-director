# Prompt Family Retuning 2026-04-22

> Historical validation note: 这份文档记录的是一次已完成的 experiment 或 repair run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录 prompt-family regression 之后，针对两条最弱 family 做的 targeted repair：

- `hybrid structured hero`
- `structured / section-based poster`

目标不是重新打开整套 prompt 体系，而是验证：

- 有针对性的 repair 是否足以把弱 family 从明显不过线拉回到可继续保留的状态
- 这些 family 还需要多窄的约束才能继续当默认写法

## Starting Point

来自第一轮 regression 的结论：

- `bm_project_hero_repo`
  - candidate: `62.5 fail`
  - 主要问题：domain drift，误滑到消费品 / 电商流程
- `bm_social_creative_launch`
  - candidate: `75.0 conditional_pass`
  - 主要问题：项目特异性不足，更像泛设计 poster

## Retuning Strategy

### Hero Repair

只改一件事：

- 把开放式 `workflow` 语言收紧成协议型 motif：
  - `intake packet`
  - `route decision`
  - `prompt assembly`
  - `scorecard`
  - `delivery-ready asset states`

同时显式禁止：

- 背包
- 家具
- 电商 listing
- shopping UI

### Poster Repair

只改一件事：

- 把“rough -> shipped”从泛设计隐喻，收紧成 `brief packet -> scorecard -> delivery-ready asset` 的项目化转译

同时显式禁止：

- 家具广告
- generic logo poster
- secondary captions
- brand lockup

## Repair Run 1: `bm_project_hero_repo`

### Prompt Under Repair

```text
Refine the README hero direction for the project image2-design-director. Keep a wide hero composition, a large clean left-side copy-safe area, bright editorial workspace atmosphere, restrained warm-neutral and slate-blue palette, and polished product-marketing craft. Replace any consumer-product or ecommerce cues with protocol-native motifs only: intake packet card, route decision nodes, prompt assembly layers, scorecard chips, image review frame, and delivery-ready asset states. Make the right-side focal cluster feel like an AI-native design system for image tasks, not a dashboard and not a consumer product workflow. No physical goods, no backpacks, no furniture, no ecommerce listing cards, no shopping UI, no fake brand text. Strong hierarchy, calm depth, believable design-system surfaces, wide README hero usability.
```

### Outputs Compared

- previous candidate: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a67a2bac81919f63bc025af53d1d.png`
- repair result: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8aa0d42f481918406a4efa7c45364.png`

### Repair Assessment

- what_improved:
  - 背包 / 电商漂移被清掉
  - 右侧焦点开始真正长出 `intake packet / route / prompt assembly / scorecard / delivery ready` 的协议层
  - hero 留白和 README 可用性仍然成立
- what_still_feels_open:
  - image review 里偏建筑效果图，仍然有一点“别的垂类项目”气味
  - 微文案比理想状态略多

### Score Shift

- previous candidate: `62.5 fail`
- repair result: `81.0 conditional_pass`

### Decision

- judgment: `repair succeeded`
- family_state: `keep with tighter constraints`
- promotion_readiness: `not ready for stronger default claim yet`

### New Working Rule

`hybrid structured hero` 在当前阶段不能只说“workflow”或“design-ops system”。

必须优先锚定为：

- protocol cards
- route nodes
- scorecard chips
- delivery-state frames

并明确排除消费品、listing、shopping 语义。

## Repair Run 2: `bm_social_creative_launch`

### Prompt Under Repair

```text
Refine the square launch poster direction for image2-design-director. Keep the exact headline text "Prompts That Ship" as the only rendered headline, large in the top third, with a dark graphite background and restrained electric blue accents. Replace any generic design-poster symbolism with project-native motifs only: rough brief packet, route decision trace, scorecard marks, prompt assembly sheet, delivery-ready asset frame. Make the transformation feel like rough image intent becoming a shippable visual system, not a furniture ad, not a generic logo poster, and not a dashboard. Strong central transformation metaphor, bold campaign energy, clean breathing room, no extra subtitles, no brand lockup, no fake logos, no made-up UI, no secondary captions.
```

### Outputs Compared

- previous candidate: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a76ca728819184f47b59bd71e8b2.png`
- repair result: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8aa9056088191b256fd2282792579.png`

### Repair Assessment

- what_improved:
  - headline 仍然稳定，只保留一条主标题
  - 海报主视觉不再是泛 logo / 几何 poster，而是开始出现 `brief -> score -> asset` 的项目流程隐喻
  - 项目特异性明显强于前一版
- what_still_feels_open:
  - 最终 asset 仍偏“山景样张”，还不够贴近本项目自己的视觉世界
  - 还可以再压缩小装饰线条和次级噪音

### Score Shift

- previous candidate: `75.0 conditional_pass`
- repair result: `83.0 conditional_pass`

### Decision

- judgment: `repair succeeded`
- family_state: `keep with one more polish pass if aiming for 85+`
- promotion_readiness: `closer, but not yet pass-grade across broader samples`

### New Working Rule

对 launch poster，单有“strong transformation metaphor”还不够。

要优先写：

- brief packet
- route trace
- scorecard / evaluation marks
- delivery-ready frame

这样项目特异性会比抽象几何语言更稳。

## Combined Retuning Judgment

这轮 targeted repair 说明两件事：

1. regression 没有要求我们回退整套 prompt family 体系
2. 弱 family 的问题更像“约束不够窄”，而不是“family 方向错误”

因此，本轮最终判断应收束为：

- `structured / section-based UI`: `validated keep`
- `directed natural language`: `validated keep`
- `structured / section-based poster`: `keep after repair`
- `hybrid structured hero`: `keep after repair, but still narrower than a broad default claim`

## Next Recommended Move

如果继续推进，最高杠杆动作不是重写所有 sample prompt，而是：

1. 把 hero family 的“协议型视觉锚点”写回更强的默认约束
2. 对 poster family 再做一次 `85+` 目标的 polish pass
3. 之后再决定是否把这两条 family 的 repair 规则晋升为 pattern 或 repo rule
