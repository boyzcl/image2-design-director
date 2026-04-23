# README Homepage Image Suite V1

## Purpose

这份文档把 `image2-design-director` 的 README 首页图片叙事方案，压成一份可直接执行的任务包和首轮出图 prompt 包。

它服务两个目标：

- 为本轮 README 首页首期图片生成提供稳定输入
- 为后续 `micro_repair`、重跑、替换模型或补做二期机制图保留一致合同

## Asset Contract

### Deliverable Type

- `README homepage image suite`

这不是单张海报，而是一组用于仓库首页连续叙事的横向图片模块。

### Asset Completion Mode

- `complete_asset`

每张图都应是可直接放入 README 的完成版视觉模块，不是等后续再找设计师补结构的底图。

### Content Language

- `zh-CN`

当前会话语言为中文，因此 README 的解释文字默认以中文为主。

### Allowed Text Scope

- generated image 中默认不依赖长可读文字
- 允许极少量可忽略的抽象标签感文字，但不要求必须可读
- 核心说明文字由 README markdown 承担

### Layout Owner

- `hybrid`

图片负责主叙事和视觉机制，README 文本负责标题、解释、导航和调用说明。

### Acceptance Bar

符合下面条件时可视为过线：

- 单张图即使脱离长文，也能表达清楚所属 section 的主题
- 整组图在 GitHub 白底环境下有统一系统感
- 视觉语言明显像“设计导演系统”而不是泛 AI 宣传图
- 低 AI 味，结构清楚，适合作为 README 首页视觉资产
- 用户看完整组后，能理解这个 skill 的核心价值是“先做对资产，再把资产做成可交付”

## Task Packet

### Request Block

- `user_raw_request`
  - 用图片讲整个 skill 的故事，做一组可用于 README 首页的图片；先完成文本方案，再继续做图

### Requirement Block

- `user_goal`
  - 产出一组 README 首页视觉资产，让用户快速理解 `image2-design-director` 的定位、机制、价值和差异点
- `asset_type`
  - `README homepage storytelling visuals`
- `deliverable_type`
  - `README homepage image suite`
- `usage_context`
  - GitHub README 首页，图片主叙事，文本辅助解释
- `requirement_summary`
  - 使用统一视觉系统，为 README 首页制作首期 6 张横向图片，分别承担 hero、问题定义、asset contract、任务分流、验收标准、delivery ops 六个叙事功能
- `success_criteria`
  - 首次进入仓库的用户能被画面吸引，并快速理解这不是普通 prompt enhancer，而是一层会判断交付物合同、分流任务并推动交付的设计导演系统

### Asset Contract Block

- `asset_completion_mode`
  - `complete_asset`
- `content_language`
  - `zh-CN`
- `allowed_text_scope`
  - `no required readable text inside the images; surrounding README copy carries the explanation`
- `layout_owner`
  - `hybrid`
- `acceptance_bar`
  - `README-ready section visuals with a unified editorial-system look`

### Context Block

- `context_summary`
  - 这是一个 public skill repo 的首页改造任务，重点不是展示某一张成图，而是用一组视觉模块建立产品理解和机制理解
- `background_context`
  - `image2-design-director` 不是提示词扩写器，而是图像生成 agent 的设计导演层，核心差异是先对齐 asset contract，再决定 route、prompt、验收和交付推进
- `must_avoid`
  - 泛紫色 AI 霓虹风
  - 过度抽象、看不出机制的科技壁纸
  - 太像广告海报、不像系统首页视觉
  - 依赖大量准确小字才能成立的版面

### Constraint Block

- `fixed_text`
  - none inside the images
- `fixed_elements`
  - none
- `size_and_delivery_constraints`
  - horizontal README-friendly visuals, preferably 16:9, with clear margins on white GitHub backgrounds
- `direct_output_vs_post_process`
  - direct output for the first pass, with Markdown text added outside the image

### Strategy Block

- `domain_direction`
  - `README homepage visual system for an AI design-director skill`
- `matched_profile`
  - `none`
- `support_tier`
  - `exploratory`
- `task_mode`
  - `fresh_generation`
- `route`
  - `direct`
- `candidate_mode`
  - `single-output`
- `output_mode`
  - `direct_output`
- `delivery_involvement`
  - `image-only`
- `strategy_reasoning`
  - 合同已经比较清楚，且当前目标是先建立统一视觉系统的一期首轮资产，优先直接出图；如果首轮出现资产类型或机制表达偏移，再进入 `micro_repair`

### Readiness Block

- `packet_lineage`
  - `derived from readme-image-story-homepage-plan-2026-04-23.md`
- `open_questions`
  - whether future README should stay Chinese-first or become bilingual
  - whether a later version should allow more embedded labels inside diagrams
- `missing_critical_fields`
  - none for first-pass generation
- `intake_confidence`
  - `high`
- `packet_readiness`
  - `ready`

## Unified Art Direction

### Visual Positioning

- editorial system poster
- product operating board
- design review wall

### Palette

- warm paper white
- soft stone gray
- charcoal black
- signal red accents
- restrained electric blue accents

### Material And Finish

- premium print-poster clarity
- crisp interface-like geometry
- subtle paper grain or board texture
- clean edges, intentional whitespace, low noise

### Composition Rules

- horizontal composition
- clear central focal structure
- side modules or surrounding panels to express mechanism
- enough clean margin to sit well on a white GitHub page
- use blocks, arrows, rails, diagram energy, but avoid literal flowchart blandness

### Text Discipline

- do not rely on exact readable text
- do not render random English filler copy
- if any micro-labels appear, they should function as abstract design marks, not required content

## README Copy Placement Recommendation

这些内容更适合写在 README markdown，而不是压到图片里：

- section title
- 一句话解释
- 调用方式 `$image2-design-director`
- 安装命令
- docs 导航

这些内容更适合让图片承担：

- “这不是 prompt enhancer”的感受
- 任务为什么会跑偏
- asset contract 六要素的结构感
- route 分流机制
- 设计评审与验收氛围
- 从主视觉到交付资产的推进感

## Prompt Family

这组图统一采用：

- `Hybrid Structured Hero`

原因：

- 每张图都不是纯机制流程图
- 也不是纯情绪主视觉
- 需要同时保留“产品首页 hero 感”和“系统机制表达”

## Prompts

下面 prompt 直接面向图像生成模型书写。

### 01. Hero

```text
Create a finished horizontal README homepage hero visual for an AI design-director skill. This is not a generic AI poster and not a pure abstract wallpaper. The image should communicate that a design-director layer sits between a vague image request and a usable final asset.

Objective: make the viewer instantly feel that this system aligns the asset before it optimizes the generation.
Audience/context: GitHub README homepage, white background environment, image-first storytelling with explanatory text outside the image.
Content language: no required readable text inside the image.
Allowed text scope: do not depend on readable copy, do not invent slogan text blocks.
Acceptance bar: looks like a premium product-system hero that could sit on a public repo homepage.

Main visual system: on the left, fragmented brief materials, scraps, thumbnails, messy request fragments, rough visual cues; in the center, a bright decisive design-director control layer or judgment core, like a sophisticated operating board; on the right, polished shippable visual asset previews emerging from the system.
Structure/layout: wide editorial composition, strong central control module, clean left-to-right transformation, large negative space, high hierarchy clarity, looks like a design operating system rather than a marketing poster.
Style layer: editorial product visual, warm paper white and light stone background, charcoal structures, precise signal red highlights, restrained electric blue details, premium print clarity, clean geometric rails, subtle texture, low noise, serious and intelligent.
Constraints: no purple neon, no fantasy sci-fi glow overload, no clutter, no UI gibberish, no dependency on exact text rendering.
Avoid: generic AI art, random dashboard screenshots, startup cliché gradients, decorative filler typography.
```

### 02. Problem

```text
Create a finished horizontal README section visual that explains what goes wrong without a design-director layer in image generation. This is a problem-definition image for a public skill repo homepage.

Objective: show that image agents often fail not because they cannot generate, but because they optimize too early and make the wrong asset.
Audience/context: GitHub README section image, paired with short Chinese explanatory copy outside the image.
Content language: no required readable text.
Allowed text scope: abstract micro-label feeling only, no meaningful long text.
Acceptance bar: instantly readable as a visual diagnosis board.

Main visual system: four misaligned output zones or cards pinned on a review wall, each clearly showing a different failure mode through composition alone: wrong asset type, half-finished output, language drift, patching instead of realignment. The center or overlay should feel like a red-flag diagnostic review.
Structure/layout: horizontal design review wall, four-panel misfit story, clear contrast between polished framing and wrong outcomes, some review marks, signal highlights, rejection energy, but still elegant and product-like.
Style layer: editorial review board, warm white board, charcoal lines, red flags and red circles, subtle blue system accents, premium product-design critique aesthetic.
Constraints: no readable paragraphs, no meme energy, no comic style, no chaotic collage mess.
Avoid: cheesy warning icons, childish layouts, exaggerated glitch effects.
```

### 03. Asset Contract

```text
Create a finished horizontal README section visual about asset contract alignment for an AI design-director skill.

Objective: visually communicate that the system asks six critical questions before generation and that deliverable definition is the center of the whole process.
Audience/context: public repo README section, explanatory markdown sits below the image.
Content language: no required readable text.
Allowed text scope: if any labels exist they are abstract and secondary, not relied upon.
Acceptance bar: the viewer can feel a six-part contract board orbiting a central deliverable decision.

Main visual system: a sophisticated intake console or contract board with six modular nodes surrounding a dominant central core. The central element feels like the chosen deliverable; the six surrounding modules feel like completion mode, language, text scope, layout owner, acceptance standard, and task definition. The image should feel like an intelligent design intake system, not a literal spreadsheet.
Structure/layout: balanced radial or semi-radial layout, clean board geometry, one dominant center, six clearly distinct supporting modules, elegant connectors, lots of clarity.
Style layer: premium editorial systems diagram, paper-white and light gray surfaces, charcoal framework, signal red selections, a few electric blue guide marks, tactile print-board finish.
Constraints: avoid literal unreadable UI text blocks, avoid turning into a software dashboard screenshot.
Avoid: overtechnical schematics, neon cyberpunk, generic infographic templates.
```

### 04. Route

```text
Create a finished horizontal README section visual showing four execution routes for an AI image design-director skill.

Objective: make it clear that once the contract is understood, the task can branch into four different routes rather than forcing every request through the same process.
Audience/context: GitHub README section image with short text outside the image.
Content language: no required readable text.
Allowed text scope: minimal abstract labels only.
Acceptance bar: strong branching logic, still visually premium and product-oriented.

Main visual system: a central confirmed-contract node branching into four distinct pathways, each with its own visual rhythm and destination mood. One branch feels immediate and direct, one feels like a short clarification loop, one feels like precise repair, one feels like deep realignment and reframing. The viewer should understand the logic through composition and directional cues rather than reading labels.
Structure/layout: strong center-to-four-way split, generous spacing, each branch visually differentiated but still within one system, horizontal layout suited for README.
Style layer: design operations map, editorial systems poster, refined geometry, warm white board, charcoal rails, red emphasis points, subtle blue guidance marks.
Constraints: not a bland corporate flowchart, not too abstract to understand.
Avoid: presentation-slide template style, childish arrows, tangled routing spaghetti.
```

### 05. Acceptance

```text
Create a finished horizontal README section visual about design acceptance and asset evaluation for an AI design-director skill.

Objective: communicate that the system judges whether the output is the right asset and actually usable, not just visually attractive.
Audience/context: GitHub README page, paired with short Chinese explanation text outside the image.
Content language: no required readable text.
Allowed text scope: no important readable copy inside the image.
Acceptance bar: clearly feels like a high-level design review board around a candidate asset.

Main visual system: a strong candidate visual in the center, surrounded by evaluation rails, scorecard-like modules, approval and rejection cues, composition guides, asset fidelity checks, completion readiness signals, and contract alignment markers. The atmosphere should feel like a design crit or launch readiness review, not a decorative infographic.
Structure/layout: central candidate asset, surrounding evaluation frame, multiple assessment modules, elegant directional emphasis, clear hierarchy.
Style layer: premium design review aesthetic, crisp lines, paper-white and gray board, charcoal framework, signal red review marks, restrained blue calibration details, quiet authority.
Constraints: no literal star ratings, no childish checklists, no too-small text dependence.
Avoid: startup KPI dashboard vibe, gamified scoring UI, visual noise.
```

### 06. Delivery Ops

```text
Create a finished horizontal README section visual about turning one visual into shippable delivery assets for an AI design-director skill.

Objective: show that the system can push an approved visual into real delivery states such as multi-size versions, text refinement, QR/logo placement, and release-ready asset packaging.
Audience/context: GitHub README section image on a public repo homepage.
Content language: no required readable text.
Allowed text scope: minimal incidental marks only.
Acceptance bar: the image should feel like a believable assetization board expanding one master visual into deployable outputs.

Main visual system: one strong master visual in the center expanding into several polished derivative asset frames around it, with clear differences in aspect ratio and deployment context. Supporting modules suggest text refinement, QR placement, logo or badge positioning, delivery packaging, and final shippable readiness. This should feel operational and elegant, not cluttered.
Structure/layout: central master asset, surrounding derivative formats, balanced spacing, obvious progression from one source to multiple ready outputs, clean rails and anchors.
Style layer: product delivery board, editorial systems visual, warm white and light gray surfaces, charcoal structure, signal red emphasis, subtle electric blue calibration details, premium finish.
Constraints: no literal fake QR codes that dominate the image, no readable tiny copy, no poster-shop clutter.
Avoid: chaotic contact sheet, noisy marketing collage, generic presentation mockup.
```

## Suggested README Pairing Copy

每张图下面可配一条很短的中文说明：

- Hero
  - 不是让 agent 更会出图，而是先让它做对图。
- Problem
  - 大多数失败不是生成失败，而是交付物判断失败。
- Asset Contract
  - 先收清 asset contract，再决定怎么生成。
- Route
  - 同一个 skill，会根据任务状态走不同路径。
- Acceptance
  - 判断标准不是“好不好看”，而是“是不是对的资产，能不能直接用”。
- Delivery Ops
  - 一张过线图，才值得被推进成真正可交付资产。

## First-Pass Evaluation Checklist

首轮图片出来后，按下面标准快速评估：

- 是否仍然像 README 首页视觉，而不是品牌广告海报
- 是否明显体现“设计导演系统”而不是泛 AI 工具
- 是否统一属于同一视觉系统
- 是否在没有长文说明时也能看出每张图的主题
- 是否过度依赖模型内嵌文字
- 是否出现明显 AI 杂质、伪 UI、无意义英文

如果某张图失败，优先按 `micro_repair` 处理：

- 只修资产类型漂移
- 只修机制表达不清
- 只修结构过满或过空
- 不重写整套视觉系统
