# Prompt Family Regression Run 2026-04-22

> Historical validation note: 这份文档记录的是一次已完成的 benchmark run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录 `image2-design-director` 在 prompt-system 融合后的第一轮真实 benchmark regression。

目标不是证明“所有新写法都更好”，而是判断：

- 哪些 prompt family 已经形成真实改善
- 哪些 family 只是方向对，但还没稳定
- 哪些 family 当前反而发生了回归

## Overall Setup

- benchmark_ref: `docs/benchmarks/prompt-family-regression-pack.md`
- date: `2026-04-22`
- evaluator: `Codex`
- comparison mode: `baseline vs candidate`
- baseline definition: 融合前的轻量字段写法
- candidate definition: 融合后的 `prompt family + text layer + prompt assembly` 写法
- image generation host: `Codex Image2`
- output directory: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/`

## Outcome Summary

| Scenario | Prompt Family | Baseline | Candidate | Judgment |
|---|---|---:|---:|---|
| `bm_project_hero_repo` | `hybrid structured hero` | `70.5 fail` | `62.5 fail` | candidate 回归，当前 family 未验证 |
| `bm_ui_mockup_credibility` | `structured / section-based UI` | `66.0 fail` | `85.5 pass` | candidate 明显成立 |
| `bm_social_creative_launch` | `structured / section-based poster` | `60.0 fail` | `75.0 conditional_pass` | candidate 有明显改善，但仍需一轮收紧 |
| `bm_app_asset_onboarding_scene` | `directed natural language` | `50.0 fail` | `82.5 conditional_pass` | candidate 明显成立，已接近稳定默认写法 |

## Family-Level Decision

- `structured / section-based UI`: `keep`
- `directed natural language`: `keep`
- `structured / section-based poster`: `keep with targeted repair`
- `hybrid structured hero`: `adjust before default claim`

---

## Scenario 1: `bm_project_hero_repo`

### Scenario

- scenario_id: `bm_project_hero_repo`
- use_case: `social-creative / project hero`
- prompt_family_under_test: `hybrid structured hero`
- text_layer_mode_under_test: `safe-area-only`

### Comparison Setup

#### baseline

- prompt_or_workflow: 轻量字段写法
- prompt_family: implicit lightweight hero prompt
- text_layer_mode: no rendered text, implied copy-safe area
- assembly_ref: pre-fusion lightweight field style
- notable_limit: 项目特异性不足，容易滑向泛科技系统图

```text
Wide README hero visual for the project "image2-design-director". Make it feel like an AI-native image workflow system. Abstract orchestration cluster with layered cards, soft interface panels, and a cinematic tech atmosphere. Wide composition with generous clean space for a repo headline. Polished product-marketing visual, premium but restrained. No logo, no rendered text, no clutter, no generic neon sci-fi wallpaper look.
```

#### candidate

- prompt_or_workflow: `hybrid structured hero`
- prompt_family: `hybrid structured hero`
- text_layer_mode: `safe-area-only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `post-fusion candidate`

```text
Create a wide README hero for the project image2-design-director. Goal: make it feel like a real design-ops system for turning rough image requests into usable product assets. Audience/context: open-source repo hero with clean copy-safe space. Main subject: a composed visual workflow showing intake packet, routing decision, prompt assembly, scorecard review, and delivery states as one coherent system. Scene/backdrop: bright editorial workspace atmosphere, not dark sci-fi. Composition/framing: wide hero, strong left-side copy-safe area, main visual system anchored to the right, stable hierarchy, generous breathing room. Text layer: no rendered headline; preserve a clean hero-safe zone with no fake labels. Style/medium: premium product-marketing visual, crisp layered cards and device-light surfaces, restrained warm-neutral and steel-blue palette, believable design-system polish. Visual priorities: 1. project-specific workflow cues, 2. usable README hero composition, 3. product-native clarity. Constraints: show packet-like cards, routing nodes, evaluation panel logic, and delivery-ready states without clutter; no logos, no random dashboards, no generic cyberpunk effects. Avoid: abstract tech wallpaper, busy neon grids, fake brand text, generic floating UI nonsense.
```

### Outputs Observed

- baseline_summary: 画面干净、hero 留白好、资产感较强，但更像通用视觉系统 hero，而不是 `image2-design-director` 自己的 repo hero
- candidate_summary: 结构化流程感更强，但模型把“design-ops system”误译成了电商背包工作流，出现明显领域偏移
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_01a43042b9bb54990169e8a6478a048191b68e026c3b77a3e0`
- candidate_generation_id: `ig_01a43042b9bb54990169e8a67a2bac81919f63bc025af53d1d`
- baseline_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a6478a048191b68e026c3b77a3e0.png`
- candidate_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a67a2bac81919f63bc025af53d1d.png`

### Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3.5 | 2.5 | 20 | 14.0 | 10.0 | candidate 的流程感更强，但场景语义完全偏到背包产品流程 |
| product_native_fit | 2.5 | 1.5 | 15 | 7.5 | 4.5 | baseline 泛化，candidate 错域 |
| structure_and_composition | 4.0 | 4.0 | 15 | 12.0 | 12.0 | 两版都保留了可用 hero 留白与构图稳定性 |
| asset_credibility | 3.5 | 3.0 | 15 | 10.5 | 9.0 | candidate 像真实物料，但不像这个项目自己的物料 |
| text_and_layout_fidelity | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 两版都没被错误文字污染 |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 工艺都比较干净 |
| anti_ai_artifact | 3.5 | 3.5 | 10 | 7.0 | 7.0 | 都没有强烈 AI 脏感，但 candidate 有概念误解 |
| iteration_clarity | 3.5 | 4.0 | 5 | 3.5 | 4.0 | candidate 更清楚暴露了下一轮需要收紧“项目特异性锚点” |

### Totals

- baseline_total: `70.5`
- candidate_total: `62.5`
- baseline_result: `fail`
- candidate_result: `fail`

### Result

- what_improved: candidate 更明确尝试了“workflow hero”而不是纯抽象主视觉
- what_did_not_improve: 项目特异性没有真正变强，反而发生了领域误读
- new_regression_or_risk: `hybrid structured hero` 目前对“项目机制词”约束不够，容易被模型映射到别的垂类

### Decision

- result: `candidate regressed`
- scenario_followup_needed: `yes`

### Next Action

- keep: hero 仍应保持大留白、单主体系统感、copy-safe 区
- change_next: 下一轮必须把“packet / route / scorecard / delivery states”锚定为图形协议元素，而不是开放式“workflow”

---

## Scenario 2: `bm_ui_mockup_credibility`

### Scenario

- scenario_id: `bm_ui_mockup_credibility`
- use_case: `ui-mockup`
- prompt_family_under_test: `structured / section-based UI`
- text_layer_mode_under_test: `suggestive only`

### Comparison Setup

#### baseline

- prompt_or_workflow: 轻量字段写法
- prompt_family: implicit lightweight UI prompt
- text_layer_mode: suggestive only
- assembly_ref: pre-fusion lightweight field style
- notable_limit: 容易滑向泛 BI dashboard

```text
Create a realistic analytics SaaS dashboard concept for an AI image workflow product. Light theme, professional tone, desktop web app, charts and KPI cards with a left navigation. Front-facing screen on a neutral presentation background. Make it feel like a believable product screen rather than a decorative UI illustration. Avoid random widgets, excessive glassmorphism, fake brand names, and clutter.
```

#### candidate

- prompt_or_workflow: `structured / section-based UI`
- prompt_family: `structured / section-based UI`
- text_layer_mode: `suggestive only`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `post-fusion candidate`

```text
Task: create a product operations dashboard mockup. Goal: make it feel like a believable internal dashboard for an AI image workflow system rather than a generic analytics board. Platform/device: desktop web app. Audience/context: product and design ops review for a visual-generation pipeline. Main subject/system: a light-theme dashboard for image task intake, route decisions, generation batches, review outcomes, and delivery states. Global constraints: brand-neutral, professional, readable but not text-heavy, one primary workflow focus, no fake company identity.

Structure:
- page type: operations overview dashboard
- main regions: left navigation, top run summary, central pipeline board, right-side review queue
- information density: medium; enough to feel real, not crowded
- screen framing: front-facing screen with clean margins and limited perspective distortion

Section 1:
- role: navigation and orientation
- content: compact left navigation and top bar for runs, benchmarks, prompt packets, and delivery review
- visual treatment: quiet, product-like, visually subordinate

Section 2:
- role: primary workflow area
- content: one clear pipeline from intake to route selection to generation to scoring, with KPI cards and one main trend chart
- visual treatment: strong hierarchy, aligned cards, consistent components, believable ops software logic

Section 3:
- role: supporting review area
- content: a small review queue and score summary for recent image tasks
- visual treatment: restrained and useful, not decorative

Text layer:
- mode: suggestive only
- hierarchy: short interface labels and statuses only, no slogans, no fake marketing copy
- placement: native UI positions only

Style layer:
- medium: modern product UI mockup
- palette: neutral light interface with restrained slate-blue accents
- fidelity: high enough to feel like a real product screenshot concept

Avoid:
- random widgets, fake-complex clutter, decorative charts for their own sake
- generic BI dashboard feel, glassmorphism excess, made-up startup branding
```

### Outputs Observed

- baseline_summary: 一眼像成熟 SaaS analytics 页面，但更接近通用 BI 仪表盘，品牌和数据都偏泛化
- candidate_summary: 成功出现 intake、route、generation、scoring、delivery 的可信流程板块，已明显更像真实 image workflow ops 产品
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_01a43042b9bb54990169e8a6afc9e08191972188ad449f3a52`
- candidate_generation_id: `ig_01a43042b9bb54990169e8a6eadbf0819197edd4d6dad5d28b`
- baseline_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a6afc9e08191972188ad449f3a52.png`
- candidate_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a6eadbf0819197edd4d6dad5d28b.png`

### Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 3.0 | 4.5 | 20 | 12.0 | 18.0 | candidate 明显更对题 |
| product_native_fit | 2.0 | 4.0 | 15 | 6.0 | 12.0 | baseline 是通用 analytics，candidate 开始长出本项目机制 |
| structure_and_composition | 4.0 | 4.5 | 15 | 12.0 | 13.5 | candidate 的主次和区块逻辑更稳定 |
| asset_credibility | 3.5 | 4.5 | 15 | 10.5 | 13.5 | candidate 更像真实 ops 产品 |
| text_and_layout_fidelity | 3.5 | 4.0 | 10 | 7.0 | 8.0 | 两版都可读，candidate 更克制 |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 工艺都较干净 |
| anti_ai_artifact | 3.5 | 4.0 | 10 | 7.0 | 8.0 | candidate 的伪 BI 感显著下降 |
| iteration_clarity | 3.5 | 4.5 | 5 | 3.5 | 4.5 | candidate 不是只“更好看”，而是更易进入下一轮产品化 |

### Totals

- baseline_total: `66.0`
- candidate_total: `85.5`
- baseline_result: `fail`
- candidate_result: `pass`

### Result

- what_improved: UI family 已经真正吃到 section-based 写法带来的收益，主区域、流程逻辑、review queue 都更可信
- what_did_not_improve: 仍然带少量泛产品视觉气质，但已不影响通过判断
- new_regression_or_risk: 无明显新红旗

### Decision

- result: `validated`
- scenario_followup_needed: `optional polish only`

### Next Action

- keep: section-based UI family 作为默认写法保留
- change_next: 后续只需补更细的中性文本与 review-area 密度控制

---

## Scenario 3: `bm_social_creative_launch`

### Scenario

- scenario_id: `bm_social_creative_launch`
- use_case: `social-creative`
- prompt_family_under_test: `structured / section-based poster`
- text_layer_mode_under_test: `verbatim`

### Comparison Setup

#### baseline

- prompt_or_workflow: 轻量字段写法
- prompt_family: implicit lightweight poster prompt
- text_layer_mode: verbatim headline only
- assembly_ref: pre-fusion lightweight field style
- notable_limit: 容易出现错误副标题、伪品牌或错误主体

```text
Create a square launch poster for image2-design-director. Make it feel like a real design-tool launch visual for social media, not an infographic board. One bold central visual about turning rough prompts into usable assets. Clean title area. Exact headline text: "Prompts That Ship". Polished brand marketing visual, premium contrast, feed-friendly composition. Avoid noisy gradients, over-glossy 3D effects, meme styling, fake dashboards, and extra copy.
```

#### candidate

- prompt_or_workflow: `structured / section-based poster`
- prompt_family: `structured / section-based poster`
- text_layer_mode: `verbatim`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `post-fusion candidate`

```text
Task: create a square launch poster. Goal: make it feel like a real social launch creative for image2-design-director, not a generic AI poster and not a product demo board. Audience/context: design and product people seeing a feed launch visual. Main subject: one clean transformation metaphor from rough image brief to shippable design asset, with a single strong focal pathway. Global constraints: only one exact headline, no brand lockup, no fake logos, no extra captions, no dashboard UI.

Structure:
- overall layout: square poster with a clear center axis and one dominant transformation scene
- focal hierarchy: headline first, transformation metaphor second, supporting atmosphere third
- safe space / title zone: top third reserved for one large headline with clear breathing room

Section 1:
- role: headline zone
- content: exact headline text "Prompts That Ship"
- visual treatment: bold, readable, integrated cleanly into the poster with no secondary text

Section 2:
- role: hero visual
- content: a refined metaphor of rough creative intent becoming a production-ready visual asset, using packet-to-asset cues rather than product advertising
- visual treatment: crisp, singular, campaign-like, visually strong without turning into an interface board

Section 3:
- role: supporting atmosphere
- content: restrained design-system cues, alignment marks, and light motion traces that reinforce craft and shipping readiness
- visual treatment: quiet and premium, no decorative clutter

Text layer:
- mode: verbatim
- hierarchy: one main headline only
- placement: top third, large and intentional

Style layer:
- medium: premium editorial campaign poster
- palette: graphite, warm white, restrained electric blue accents
- lighting/material: sharp contrast, polished but not glossy, bold campaign energy

Avoid:
- fake logos, extra taglines, or made-up UI
- furniture-ad look, generic tech wallpaper, infographic board, noisy gradients
```

### Outputs Observed

- baseline_summary: headline 很强，但主体变成了错误的椅子产品转化，且自动出现了品牌锁定和额外视觉噪音
- candidate_summary: 成功收敛成更抽象但更正确的“sketch to shipped asset”海报，headline 更干净，额外副文案被压下去了
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_01a43042b9bb54990169e8a732054c8191aff0d5fd103499a7`
- candidate_generation_id: `ig_01a43042b9bb54990169e8a76ca728819184f47b59bd71e8b2`
- baseline_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a732054c8191aff0d5fd103499a7.png`
- candidate_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a76ca728819184f47b59bd71e8b2.png`

### Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 2.5 | 3.5 | 20 | 10.0 | 14.0 | candidate 回到正确主题 |
| product_native_fit | 1.5 | 3.0 | 15 | 4.5 | 9.0 | baseline 错成家具广告，candidate 至少回到设计资产语境 |
| structure_and_composition | 4.0 | 4.0 | 15 | 12.0 | 12.0 | 两版都有海报感；candidate 更克制 |
| asset_credibility | 3.0 | 4.0 | 15 | 9.0 | 12.0 | candidate 更像真实 launch creative |
| text_and_layout_fidelity | 3.0 | 4.0 | 10 | 6.0 | 8.0 | candidate 减少了多余文字和 lockup |
| craft_finish | 4.0 | 4.0 | 10 | 8.0 | 8.0 | 工艺均较稳 |
| anti_ai_artifact | 3.5 | 4.0 | 10 | 7.0 | 8.0 | candidate 的“AI 海报感”下降 |
| iteration_clarity | 3.5 | 4.0 | 5 | 3.5 | 4.0 | candidate 清楚暴露下一轮要补“项目特异性” |

### Totals

- baseline_total: `60.0`
- candidate_total: `75.0`
- baseline_result: `fail`
- candidate_result: `conditional_pass`

### Result

- what_improved: text layer 更受控，错误副文案减少，主视觉从错题回到正确的“rough-to-shippable”语义
- what_did_not_improve: 仍然更像泛设计系统海报，而不是 `image2-design-director` 自己的标志性 poster
- new_regression_or_risk: 无严重回归，但仍缺项目特异性锚点

### Decision

- result: `directionally validated`
- scenario_followup_needed: `yes`

### Next Action

- keep: section-based poster family 保留，headline zone 与 text-layer 控制有效
- change_next: 下一轮补 `task packet / route / scorecard / delivery-state` 的独有视觉 motif，减少泛设计 poster 气质

---

## Scenario 4: `bm_app_asset_onboarding_scene`

### Scenario

- scenario_id: `bm_app_asset_onboarding_scene`
- use_case: `app-asset`
- prompt_family_under_test: `directed natural language`
- text_layer_mode_under_test: `none`

### Comparison Setup

#### baseline

- prompt_or_workflow: 轻量字段写法
- prompt_family: implicit lightweight app-asset prompt
- text_layer_mode: implicit no-text
- assembly_ref: pre-fusion lightweight field style
- notable_limit: 容易被模型误解成通用团队插图或说明卡片

```text
Create an onboarding illustration for a mobile app that helps teams turn rough image requests into usable design assets. Friendly visual metaphor, clean product illustration, portrait-friendly composition, calm and trustworthy. Minimal abstract backdrop that can sit behind onboarding copy. Keep it lightweight and system-friendly. Avoid childish style, heavy visual noise, hyper-detailed 3D scenes, and unrelated fantasy props.
```

#### candidate

- prompt_or_workflow: `directed natural language`
- prompt_family: `directed natural language`
- text_layer_mode: `none`
- assembly_ref: `references/prompt-schema.md` + `references/prompt-assembly.md`
- version: `post-fusion candidate`

```text
Create an onboarding illustration for a mobile app that helps teams turn rough image requests into usable design assets. The main subject is a rough creative request becoming a calm, production-ready asset kit. It should show a sense of guided transformation and clarity rather than a busy workflow dashboard. The environment is a minimal product-illustration space that can sit beside onboarding copy inside a modern mobile app. The composition should feel portrait-friendly, centered, easy to crop, and built around one clear visual center of gravity with generous surrounding breathing room. The text layer strategy is no rendered text; leave clean space for product copy and avoid labels, logos, or fake UI captions. The visual language should feel like a soft flat-meets-light-volume product illustration with warm neutral surfaces and restrained slate-blue accents, trustworthy and system-friendly rather than playful or childish. Key constraints: make it feel native to a real app onboarding flow, with a clear before-to-after metaphor and lightweight forms that do not overpower the interface. Avoid: information-board layouts, heavy 3D scenes, handwritten notes, extra copy, unrelated characters, or noisy decorative details.
```

### Outputs Observed

- baseline_summary: 模型把任务误解成“团队高五 + 说明卡片”，出现了大量无关文字和说明 UI
- candidate_summary: 成功变成干净的“rough request -> asset kit”单图叙事，留白、产品兼容性、文本控制都显著更好
- baseline_final_prompt: same as baseline prompt above
- candidate_final_prompt: same as candidate prompt above
- baseline_image_prompt: same as baseline final prompt
- candidate_image_prompt: same as candidate final prompt
- baseline_generation_id: `ig_01a43042b9bb54990169e8a7b4e8148191baccbc72ad74b018`
- candidate_generation_id: `ig_01a43042b9bb54990169e8a7eeea488191b6cb4cccd8813660`
- baseline_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a7b4e8148191baccbc72ad74b018.png`
- candidate_image_output_ref: `<generated-images-root>/019db4b8-fdb7-7902-9d07-74604989958d/ig_01a43042b9bb54990169e8a7eeea488191b6cb4cccd8813660.png`

### Scores

| Dimension | baseline_0_5 | candidate_0_5 | weight | baseline_weighted | candidate_weighted | notes |
|---|---:|---:|---:|---:|---:|---|
| intent_match | 2.0 | 4.0 | 20 | 8.0 | 16.0 | candidate 回到“rough request -> usable asset”主线 |
| product_native_fit | 2.0 | 4.0 | 15 | 6.0 | 12.0 | candidate 更像 app onboarding 资产 |
| structure_and_composition | 3.0 | 4.5 | 15 | 9.0 | 13.5 | candidate 的 portrait 构图和中心更稳 |
| asset_credibility | 2.5 | 4.0 | 15 | 7.5 | 12.0 | baseline 更像说明页，candidate 更像真实产品插图 |
| text_and_layout_fidelity | 1.5 | 4.5 | 10 | 3.0 | 9.0 | candidate 成功压掉无关文案 |
| craft_finish | 3.5 | 4.0 | 10 | 7.0 | 8.0 | candidate 更轻、更干净 |
| anti_ai_artifact | 3.0 | 4.0 | 10 | 6.0 | 8.0 | candidate 的伪 UI / 伪说明块明显减少 |
| iteration_clarity | 3.5 | 4.0 | 5 | 3.5 | 4.0 | candidate 已接近稳定默认写法 |

### Totals

- baseline_total: `50.0`
- candidate_total: `82.5`
- baseline_result: `fail`
- candidate_result: `conditional_pass`

### Result

- what_improved: directed natural language family 对单图叙事 app asset 的帮助非常明显
- what_did_not_improve: 仍可再提高 metaphor 的独特性和品牌原生感
- new_regression_or_risk: 无明显新红旗

### Decision

- result: `validated`
- scenario_followup_needed: `minor polish`

### Next Action

- keep: directed natural language family 保留为单图叙事 app asset 默认写法
- change_next: 后续只需加强更具体的产品语义锚点，不需要回退到字段堆叠

---

## Cross-Scenario Judgment

### What The Regression Actually Proved

这轮真实跑图后，可以收束成 4 条判断：

1. `structured / section-based UI` 已经被真实验证，应该保留为默认写法
2. `directed natural language` 对单图叙事类 app asset 已经被真实验证，应该保留为默认写法
3. `structured / section-based poster` 已方向成立，但仍需要补项目特异性锚点
4. `hybrid structured hero` 当前还不能直接作为默认能力宣称，需要先修复 domain drift

### Highest-Leverage Next Move

不是继续扩所有 prompt family，而是聚焦两条 targeted repair：

1. 修 `hybrid structured hero`
   - 收紧项目语义锚点
   - 避免“workflow”被错解成电商 / 其他垂类流程
2. 修 `structured / section-based poster`
   - 增加 `image2-design-director` 独有视觉 motif
   - 减少泛设计 poster 感

## Runtime Memory Provenance

- runtime_capture_written: `yes`
- runtime_capture_ref: `<runtime-root>/captures/2026-04-22.jsonl`
- runtime_reuse_observed: `no`
