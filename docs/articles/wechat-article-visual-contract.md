# WeChat Article Visual Contract

## Purpose

这份文档定义《我为什么还是做了 image2-design-director，当 gpt-image-2 已经这么强之后》这篇公众号文章的正式配图合同。

目标不是“给文章找几张好看的图”，而是保证每一张图都服务文章论点，并且不会把 benchmark 工件、overlay 验证产物或别的场景资产误当成发布配图。

一句话版本：

> 文章配图是 `editorial collateral`，不是 benchmark artifact，也不是 delivery overlay demo。

同时，这个场景默认遵循：

> `complete_asset by default`

也就是说，文章中的图默认应交付成品图，而不是只留 masthead-safe、title-safe 的中间稿。

## Scene Position

- `deliverable_type`: `wechat_article_editorial_visual_set`
- `usage_context`: `公众号长文配图`
- `asset_completion_mode`: `complete_asset`
- `content_language`: `zh-CN article context`
- `allowed_text_scope`: `rendered_headline_plus_short_supporting_text`
- `layout_owner`: `model` or `hybrid`, but no benchmark overlay copy
- `acceptance_bar`: `looks like publication-grade editorial collateral that directly supports the article's argument`

## Core Rules

### 1. Publication Asset, Not Benchmark Artifact

以下产物默认不得直接作为文章配图：

- benchmark run candidate image
- overlay viability demo artifact
- delivery-ready event poster
- any bundle asset whose original contract is not article/editorial collateral

只有当它同时满足下面 3 条时，才允许例外复用：

1. 原始合同与文章配图语义一致
2. 图中没有别的任务残留文案或 fixed elements
3. 文章内的图注能准确解释它，而不会造成场景错位

### 2. Argument Fit Before Visual Polish

文章配图首先要回答：

- 这张图是否在支持当前段落的论点
- 它是否真的属于“这篇文章要交付的视觉资产”

如果只是“画面好看”“模型能力强”，但不服务该段论点，视为不过线。

### 3. Editorial Identity Before Demo Identity

文章配图应优先呈现：

- editorial cover
- editorial systems figure
- workflow evidence visual

不要优先呈现：

- literal event signup poster
- benchmark checker output
- generic AI wallpaper
- off-topic campaign visual

### 4. No Contract Drift In Text

文章配图不得出现以下内容：

- `深图`
- 与文章无关的活动报名文案
- 二维码、CTA、日期、badge，除非该图本身就是在讲 fixed-element delivery，并且合同已显式要求
- 任何与当前文章主题无关的标题或标签

允许且推荐出现的文本类型：

- 1 条主标题
- 1 到 2 条 supporting text

不推荐：

- 长段落
- dense info overlay
- 与文章无关的 campaign 文案

### 5. Style Direction Must Match The Article

本篇文章适合的风格方向：

- bright editorial / report collateral
- premium systems visual
- calm product-design / knowledge collateral
- restrained warm-neutral, slate-blue, muted sand palette

避免：

- dark sci-fi void
- generic cinematic tech wallpaper
- event-campaign poster language
- loud social-promo treatment

## Required Figure Set

这篇文章最多保留 3 张图，分别承担不同角色。

### Figure A. Editorial Cover

- role: 开篇头图
- purpose: 传达“这不是 prompt 小技巧，而是一套更完整的系统”
- preferred asset type: `editorial report cover` or `knowledge collateral cover`
- required signals:
  - finished editorial cover with rendered headline
  - protocol-native system cues
  - no off-topic text
  - publication-grade calmness

### Figure B. Mechanism Figure

- role: 中段机制图
- purpose: 支持 `asset contract -> route -> acceptance -> delivery -> accumulation`
- preferred asset type: `systems figure` or `protocol visual`
- required signals:
  - visible transformation or system structure
  - rendered headline that names the mechanism
  - no scenic drift
  - no literal benchmark demo residue

### Figure C. Workflow Evidence Visual

- role: 后段证据图
- purpose: 说明这套 skill 不是理念，而是进入了实际工作流组织
- preferred asset type: `workflow collateral` or `editorial system hero`
- required signals:
  - from rough request to usable asset system
  - rendered headline that states the workflow claim
  - organized modules rather than decorative abstraction
  - no unrelated CTA / QR / event-poster semantics

## Acceptance Checklist

每张图入选文章前，至少回答下面问题：

1. 这张图的原始合同是不是文章配图，或者至少与文章配图同类
2. 这张图是否直接支持所在段落的论点
3. 图中是否存在别的任务残留文案、二维码、CTA、日期、badge
4. 图像资产类型是否属于 editorial collateral，而不是 benchmark demo
5. 风格是否与本文的理性分析 + 系统感定位一致

## Hard Fail Conditions

出现以下任一项时，默认不得进入正文：

- 与文章主题不一致的 rendered text
- 来自 event-poster / signup / campaign overlay 场景的工件
- 需要图注强行解释才能勉强成立
- benchmark 能过线，但 publication asset 明显不过线
- asset identity 明显错位

## Current Selected Assets

当前这一轮先只允许以下 3 张进入候选池：

1. `editorial-cover-report-final`
   - source:
     `/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/editorial-cover-report-final.png`
   - role:
     `Figure A`
2. `protocol-visual-mechanism-final`
   - source:
     `/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/protocol-visual-mechanism-final.png`
   - role:
     `Figure B`
3. `workflow-evidence-final`
   - source:
     `/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/workflow-evidence-final.png`
   - role:
     `Figure C`

## Next Move

1. 把上面 3 张候选资产推进到 `delivery_ready_visual`
2. 给每张图补上最终标题与短 supporting text
3. 用文章内图注解释它们各自承担的论点
4. 不再复用任何 event poster overlay bundle 产物
