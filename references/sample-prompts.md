# Sample Prompts

## How To Use This File

- 这些不是固定咒语，而是默认骨架和参数化模板
- 先锁 `asset contract`，再写视觉层
- 先选 prompt family，再替换参数，再发送给 Image2
- 如果用户已经给得很具体，就少改，不要为“看起来完整”而过度扩写
- 未解析的 `{{placeholder}}` 不应该直接发给模型

## Prompt Family 1. Hybrid Structured Hero

适用于：

- 产品 hero
- 单主体 campaign visual
- 社媒主视觉
- 需要明确 copy-safe 区的视觉底图

### Parameterized Template

```text
Asset contract:
- deliverable type: {{deliverable_type}}
- completion mode: {{asset_completion_mode}}
- content language: {{content_language}}
- allowed text scope: {{allowed_text_scope}}
- layout owner: {{layout_owner}}
- acceptance bar: {{acceptance_bar}}

Use case: {{use_case}}
Asset type: {{asset_type}}
Primary request: create a {{asset_type}} for {{primary_request}}
Objective: {{objective}}
Audience/context: {{audience_context}}
Subject: {{subject}}
Scene/backdrop: {{scene_backdrop}}
Composition/framing: {{composition_framing}}
Text layer: {{text_layer_strategy}}
Motif anchors: {{motif_anchors}}
Style/medium: {{style_medium}}
Visual priorities:
1. {{priority_1}}
2. {{priority_2}}
3. {{priority_3}}
Constraints: {{constraints}}
Semantic exclusions: {{semantic_exclusions}}
Avoid: {{avoid}}
```

### Resolved Example

```text
Use case: product-mockup
Asset type: landing page hero
Primary request: create a landing page hero for a matte white countertop coffee grinder
Objective: make it feel like a premium ecommerce hero asset that could ship on a real product page
Audience/context: design-conscious home coffee enthusiasts comparing premium countertop gear
Subject: matte white coffee grinder with subtle brushed metal accents and believable product-scale details
Scene/backdrop: clean studio backdrop with a soft warm-gray gradient and a faint countertop grounding plane
Composition/framing: wide composition, product anchored slightly off-center, generous clean negative space on the right for headline and CTA, clear hero focal point
Text layer: no rendered headline; preserve a clean right-side copy-safe area with no fake labels or badges
Style/medium: commercial product photography with premium material realism and restrained studio lighting
Visual priorities:
1. product credibility
2. premium material feel
3. usable layout space
Constraints: no logo, no watermark, no extra props that distract from the grinder
Semantic exclusions: ecommerce UI, packaging mockup, lifestyle kitchen scene, retail badge cluster
Avoid: poster-like composition, cluttered background, surreal lighting, generic concept-render feel
```

### Resolved Example: Repo / System Hero Variant

```text
Asset contract:
- deliverable type: README hero
- completion mode: base_visual
- content language: zh-CN
- allowed text scope: no readable text
- layout owner: post_process
- acceptance bar: must remain a clean README hero base with a stable copy-safe area

Use case: social-creative
Asset type: repo README hero
Primary request: create a repo README hero for image2-design-director
Objective: make it feel like a real AI-native design system for turning rough image requests into shippable assets
Audience/context: open-source repo hero with large left-side copy-safe space
Subject: one protocol-native focal cluster built from intake packet cards, route decision nodes, prompt assembly layers, scorecard chips, and delivery-ready asset frames
Scene/backdrop: bright editorial workspace atmosphere with calm depth, not a dark sci-fi void
Composition/framing: wide hero, large clean copy-safe area on the left, focal cluster on the right, stable hierarchy, generous breathing room
Text layer: no rendered headline; preserve a clean left-side copy-safe area with no fake labels
Motif anchors: intake packet card, route decision node, prompt assembly layer, scorecard chip, delivery-state frame
Style/medium: premium product-marketing visual with crisp system surfaces and restrained warm-neutral plus slate-blue color
Visual priorities:
1. protocol-native specificity
2. usable repo hero composition
3. calm premium finish
Constraints: keep the image system-like rather than dashboard-like; if a review frame appears, keep it neutral and non-domain-specific
Semantic exclusions: consumer product, backpack, furniture, ecommerce listing, shopping UI
Avoid: generic tech wallpaper, random floating widgets, fake startup branding, neon cyberpunk effects
```

### Working Note

对 repo / system hero，如果 prompt 里出现 `review frame` 或 `delivery-state frame`，最好再显式补一句：

```text
Keep the reviewed asset neutral and project-safe, not a scenic photograph, architecture render, or another strong vertical-specific sample.
```

更稳的写法是直接补允许范围：

```text
Keep the reviewed asset in the form of neutral project collateral such as a README hero plate, onboarding visual card, or benchmark board preview, not a scenic photograph, architecture render, room scene, or framed art sample.
```

## Prompt Family 2. Structured / Section-Based Poster

适用于：

- 高结构海报
- 信息量偏高的社媒图
- 有标题区、中心主体、底部辅助区的 campaign poster

### Parameterized Template

```text
Asset contract:
- deliverable type: {{deliverable_type}}
- completion mode: {{asset_completion_mode}}
- content language: {{content_language}}
- allowed text scope: {{allowed_text_scope}}
- layout owner: {{layout_owner}}
- acceptance bar: {{acceptance_bar}}

Task: create a {{asset_type}}
Goal: {{goal}}
Audience/context: {{audience_context}}
Main subject: {{main_subject}}
Global constraints: {{global_constraints}}

Structure:
- overall layout: {{overall_layout}}
- focal hierarchy: {{focal_hierarchy}}
- safe space / title zone: {{title_zone}}

Section 1:
- role: {{section_1_role}}
- content: {{section_1_content}}
- visual treatment: {{section_1_treatment}}

Section 2:
- role: {{section_2_role}}
- content: {{section_2_content}}
- visual treatment: {{section_2_treatment}}

Section 3:
- role: {{section_3_role}}
- content: {{section_3_content}}
- visual treatment: {{section_3_treatment}}

Text layer:
- mode: {{text_mode}}
- hierarchy: {{text_hierarchy}}
- placement: {{text_placement}}
- density: {{text_density}}

Transformation metaphor:
- source state: {{source_state}}
- transition cues: {{transition_cues}}
- destination state: {{destination_state}}

Style layer:
- medium: {{medium}}
- palette: {{palette}}
- lighting/material: {{lighting_material}}

Avoid:
- {{avoid_1}}
- {{avoid_2}}
```

### Resolved Example

```text
Task: create a LinkedIn feature-launch poster
Goal: make it feel like a real B2B product marketing asset for a new analytics dashboard feature, not a generic AI poster
Audience/context: product managers and operations leaders seeing a square feed creative
Main subject: a dashboard-inspired visual system with one central screen motif and a restrained analytics atmosphere
Global constraints: keep the composition campaign-ready, leave the headline readable, and avoid fake product microcopy

Structure:
- overall layout: square poster with a clear center axis, one dominant hero panel, and supporting detail zones that do not compete with the headline
- focal hierarchy: headline first, hero visual second, supporting analytics cues third
- safe space / title zone: top third reserved for headline integration with clean contrast and no noisy overlays

Section 1:
- role: headline zone
- content: exact launch headline with one optional emphasis phrase
- visual treatment: bold, readable title integration with clean breathing room

Section 2:
- role: hero visual
- content: a believable dashboard-inspired centerpiece with charts, KPI cues, and product-marketing polish
- visual treatment: crisp focal object, restrained depth, no fake UI overload

Section 3:
- role: supporting atmosphere
- content: subtle analytics grid cues and campaign-supportive secondary shapes
- visual treatment: quiet background energy that reinforces the product story without becoming decoration spam

Text layer:
- mode: verbatim
- hierarchy: one main headline, no subtitle paragraph, no badge wall
- placement: headline in the top third, centered and intentionally integrated into the poster
- density: low; one dominant title only

Transformation metaphor:
- source state: rough analytics workflow becoming a campaign-ready feature story
- transition cues: dashboard-inspired signal lines, KPI cues, and controlled depth
- destination state: polished feature-launch visual anchored by one believable product centerpiece

Style layer:
- medium: polished brand marketing visual
- palette: deep navy, cool neutrals, and restrained cyan accents
- lighting/material: clean digital glow with premium contrast, not glossy 3D excess

Avoid:
- over-glossy 3D gimmicks
- noisy gradients, generic AI poster look, fake infographic boards
```

### Resolved Example: Project-Native Launch Poster Variant

```text
Asset contract:
- deliverable type: project launch poster
- completion mode: complete_asset
- content language: zh-CN
- allowed text scope: only project name + one Chinese slogan + one Chinese subtitle
- layout owner: model
- acceptance bar: must be directly usable as a project launch poster without another copy pass

Task: create a square launch poster
Goal: make it feel like a real project launch asset for image2-design-director rather than a generic design poster
Audience/context: social feed launch creative for builders and design-minded AI users
Main subject: one bold transformation from rough prompt intent into a delivery-ready visual system
Global constraints: render only these readable lines: "image2-design-director", "能交付的提示词", and "把粗糙图像需求收敛成可交付设计资产"; keep the poster campaign-ready and avoid any extra captions or fake microcopy

Structure:
- overall layout: square poster with one dominant center-axis transformation and a clean top-third title zone
- focal hierarchy: headline first, transformation metaphor second, supporting protocol detail third
- safe space / title zone: top third reserved for the exact headline with clear contrast and no competing noise

Section 1:
- role: headline zone
- content: the exact readable text "image2-design-director" and "能交付的提示词"
- visual treatment: large, bold, readable, integrated cleanly into the top third

Section 2:
- role: transformation core
- content: rough brief packet becoming route trace, scorecard marks, prompt assembly sheet, and a delivery-ready asset frame
- visual treatment: one strong central flow with project-native cues, not an abstract logo shape

Section 3:
- role: supporting atmosphere
- content: restrained supporting lines and accents that reinforce the packet-to-asset transition
- visual treatment: quiet energy, clean breathing room, no decorative noise swarm

Text layer:
- mode: verbatim
- hierarchy: project name first, Chinese slogan second, one Chinese subtitle third
- placement: top third and upper-middle area with clear reading order
- density: low; no badge wall, no secondary captions, no fake UI text

Transformation metaphor:
- source state: rough brief packet
- transition cues: route trace, scorecard marks, prompt assembly sheet
- destination state: delivery-ready asset frame showing a neutral project-safe visual output, not a scenic photo storyboard

Working note:
- 如果这类 poster 仍把 destination state 补成风景样片，就把 destination state 再收紧成：
  - `README hero plate`
  - `onboarding visual card`
  - `benchmark board preview`
- 并显式排除：
  - `landscape photo`
  - `architecture render`
  - `room scene`
  - `framed scenic print`

Style layer:
- medium: bold campaign poster
- palette: dark graphite with restrained electric blue accents
- lighting/material: crisp contrast and controlled glow, not glossy 3D excess

Avoid:
- furniture ad, architecture board, generic logo poster, dashboard board, fake brand lockup, English secondary captions
- made-up UI, decoration spam, abstract geometry with no project mechanism
```

## Prompt Family 3. Structured / Section-Based UI Mockup

适用于：

- SaaS dashboard
- app showcase board
- design system page
- UI-heavy visual

### Parameterized Template

```text
Task: create a {{asset_type}}
Goal: {{goal}}
Platform/device: {{platform_device}}
Audience/context: {{audience_context}}
Main subject/system: {{main_subject}}
Global constraints: {{global_constraints}}

Structure:
- page type: {{page_type}}
- main regions: {{main_regions}}
- information density: {{information_density}}
- screen framing: {{screen_framing}}

Section 1:
- role: {{section_1_role}}
- content: {{section_1_content}}
- visual treatment: {{section_1_treatment}}

Section 2:
- role: {{section_2_role}}
- content: {{section_2_content}}
- visual treatment: {{section_2_treatment}}

Section 3:
- role: {{section_3_role}}
- content: {{section_3_content}}
- visual treatment: {{section_3_treatment}}

Text layer:
- mode: {{text_mode}}
- hierarchy: {{text_hierarchy}}
- placement: {{text_placement}}

Style layer:
- medium: {{medium}}
- palette: {{palette}}
- fidelity: {{fidelity}}

Avoid:
- {{avoid_1}}
- {{avoid_2}}
```

### Resolved Example

```text
Task: create a product dashboard mockup
Goal: make it feel like a believable analytics SaaS screen rather than a decorative UI-style illustration
Platform/device: desktop web app
Audience/context: B2B software product presentation
Main subject/system: analytics dashboard with charts, KPI cards, and a left navigation
Global constraints: light theme, professional tone, readable but not text-heavy, one primary task focus, no fake company identity

Structure:
- page type: analytics overview dashboard
- main regions: left navigation, top summary row, central chart area, right-side detail support
- information density: medium; enough to feel real, not crowded
- screen framing: front-facing screen with clean margins and limited perspective distortion

Section 1:
- role: navigation and orientation
- content: compact left navigation and top bar that establish product structure
- visual treatment: quiet and system-consistent, never louder than the content area

Section 2:
- role: primary analysis area
- content: a focused mix of KPI cards and one main chart cluster
- visual treatment: strong hierarchy, aligned cards, consistent component spacing

Section 3:
- role: supporting detail area
- content: one or two secondary modules that support the main task without fragmenting the screen
- visual treatment: restrained, useful, visually subordinate

Text layer:
- mode: suggestive only
- hierarchy: readable interface labels, but no brand slogan, no oversized fake marketing text
- placement: native UI positions only

Style layer:
- medium: modern product UI mockup
- palette: neutral light interface with restrained accent color
- fidelity: high enough to feel like a product screenshot concept, not a dribbble fantasy panel

Avoid:
- random widgets and decorative complexity
- excessive glassmorphism, fake-complex clutter, impossible UI patterns
```

## Prompt Family 4. Directed Natural Language Scene

适用于：

- onboarding 插图
- 单图叙事视觉
- 中心隐喻主视觉
- 动作或氛围导向任务

### Parameterized Template

```text
Create a {{scene_type}} for {{asset_goal}}.
The main subject is {{main_subject}}.
They are {{action_or_state}}.
The environment is {{environment}}.
The composition should feel {{composition}}.
The text layer strategy is {{text_layer_strategy}}.
The visual language should feel {{visual_language}}.
Key constraints: {{constraints}}.
Avoid: {{avoid}}.
```

### Resolved Example

```text
Create an onboarding illustration for a personal budgeting app.
The main subject is a simple financial planning metaphor built from friendly, trustworthy shapes.
It should show a calm sense of progress and control rather than a flashy money fantasy.
The environment is a minimal abstract backdrop that can sit behind or alongside onboarding copy in a mobile flow.
The composition should feel portrait-friendly, centered, and easy to crop, with one clear visual center of gravity.
The text layer strategy is no rendered text, but leave clean surrounding space so product copy can sit next to or above the illustration.
The visual language should feel like a clean flat-meets-soft-gradient product illustration with lightweight forms and calm fintech trust.
Key constraints: keep it lightweight, system-friendly, and compatible with real app UI; avoid loud decorative detail.
Avoid: childish illustration style, hyper-detailed 3D scenes, heavy visual noise, unrelated fantasy props.
```

## Prompt Family 5. Repair Overlay

适用于已有图像的最小纠偏。

### Parameterized Template

```text
Use case: {{use_case}}
Asset type: {{asset_type}}
Primary request: refine the previous image
Objective: {{objective}}
Change only: {{change_only}}
Keep unchanged: {{keep_unchanged}}
Visual priorities:
1. {{priority_1}}
2. {{priority_2}}
Avoid: {{avoid}}
```

### Resolved Example

```text
Use case: ui-mockup
Asset type: product dashboard mockup
Primary request: refine the previous image
Objective: make the screen feel like a real software product instead of a concept collage
Change only: simplify the information hierarchy, reduce random widget variety, and make the layout feel like one focused dashboard
Keep unchanged: overall light theme, analytics context, modern professional tone, front-facing product presentation
Visual priorities:
1. believable interface structure
2. clearer hierarchy
3. component consistency
Avoid: decorative complexity, random panels, concept-art styling, extra fake brands
```

## Notes On Parameterization

- 优先参数化：任务类型、主体、文案、区块、色彩、关键约束
- 不要参数化一大串空泛风格词
- 高结构任务先出模板，再填值；单图叙事任务先定句子顺序，再替换变量
- 如果任务是直出海报测试，把 `text layer` 的直出策略写清楚，不要只在脑中默认
