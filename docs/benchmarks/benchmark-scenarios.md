# Benchmark Scenarios

## Purpose

这份文档定义 `image2-design-director` 的核心 benchmark 场景集。

目标不是覆盖所有任务，而是用少量高代表性场景去验证：

- intake 是否更稳
- strategy 是否更准
- post-processing 与 delivery ops 是否真的提升可用性
- 多候选与 A/B 是否带来更清楚的决策
- 经验晋升规则是否在真实任务里有判断价值
- 泛化后的 scene system 是否既能守住已验证档案，也能让新场景先拿到 `60+` 的可诊断起点

一句话版本：

> benchmark 场景不是示例库，而是升级后的最小回归面。

## How To Use

### 1. Run Benchmarks For Change Validation

当下面任一项发生时，优先跑 benchmark：

- 修改 prompt 框架
- 修改 route 判断
- 修改 post-processing 或 delivery 规则
- 修改多候选策略
- 修改 promotion governance

### 2. Prefer Representative Scenarios Over Many Easy Ones

不要只挑容易命中的任务。

优先挑那些最容易暴露边界问题的场景。

### 3. Compare With Structure

每次 benchmark 应至少配合：

- `docs/benchmarks/benchmark-run-template.md`

如果是在比较两种策略，额外配合：

- `docs/experiments/ab-testing-template.md`
- `docs/benchmarks/generalized-benchmark-surface.md`

## Scenario Set

当前最小 benchmark 集包含 6 个核心场景。

| Scenario ID | Use Case | What It Stresses |
|---|---|---|
| `bm_social_creative_launch` | `social-creative` | 传播感、标题区、campaign 逻辑 |
| `bm_project_hero_repo` | `social-creative` / `project hero` | 项目特异性、hero 构图、text-safe 底图 |
| `bm_ui_mockup_credibility` | `ui-mockup` | 页面可信度、伪 UI 风险、品牌中性控制 |
| `bm_app_asset_onboarding_scene` | `app-asset` | 单图叙事、产品兼容性、自然语言写法稳定性 |
| `bm_icon_small_size` | `app-asset` / `icon` | 轮廓、缩小后可读性、工艺干净度 |
| `bm_fixed_element_delivery` | `social-creative` / `delivery_refinement` | 二维码、logo、标题、安全区、多尺寸交付 |

## Generalized Surface Reminder

无论当前 benchmark 场景是否来自旧四个高频方向，实际 run 记录都应显式带上：

- `domain_direction`
- `matched_profile`
- `support_tier`

如果当前是旧记录兼容或历史复盘，可补：

- `legacy_use_case`

但新的 benchmark 判断不应再只靠 `use_case` 一列收口。

## Prompt Family Coverage

如果改动的是默认 prompt 写法，不应只按 use case 覆盖 benchmark，还应检查新的 prompt family 是否都有代表性验证面。

| Prompt Family | Primary Scenario | Why It Matters |
|---|---|---|
| `structured / section-based poster` | `bm_social_creative_launch` | 验证标题区、模块层级、campaign poster 结构 |
| `hybrid structured hero` | `bm_project_hero_repo` | 验证单主体商业主视觉、hero 构图、text-safe 留白 |
| `structured / section-based UI` | `bm_ui_mockup_credibility` | 验证 UI 分区、信息密度、品牌中性控制 |
| `directed natural language` | `bm_app_asset_onboarding_scene` | 验证单图叙事任务不被误写成字段堆叠 |
| `repair overlay` | `bm_social_creative_launch` 或 `bm_ui_mockup_credibility` 的第二轮 | 验证 change-only / keep-unchanged 的最小纠偏 |

## Scenario 1. `bm_social_creative_launch`

### Goal

验证 skill 能否把“传播图”做成真实 campaign creative，而不是漂亮壁纸。

### Typical Request Shape

- 为发布、招募、活动或首发做社媒图
- 需要明显传播感
- 往往后续还会叠标题或 CTA

### What To Hold Constant

- use case: `social-creative`
- asset type: `feed creative` 或 `launch poster`
- usage context: 社媒首发

### What This Scenario Should Stress

- 是否正确预留文字区
- 是否像传播物料，而不是抽象海报
- 是否存在未要求额外文案

### High-Value Dimensions

- `intent_match`
- `structure_and_composition`
- `asset_credibility`
- `text_and_layout_fidelity`

### Common Failure Watchlist

- 像壁纸，不像 campaign asset
- 文字区混乱
- 传播意图不清
- AI 海报感过强

## Scenario 2. `bm_project_hero_repo`

### Goal

验证 skill 能否为真实项目或仓库做出“可继续使用”的 hero 底图，而不是泛科技概念图。

### Typical Request Shape

- README hero
- 项目主页 hero
- 产品介绍头图

### What To Hold Constant

- 项目本体信息
- usage context: README 或 landing hero
- 后续通常需要叠标题

### What This Scenario Should Stress

- 项目特异性
- hero 结构是否稳定
- text-safe visual 是否成立
- 多尺寸裁切后是否仍保真

### High-Value Dimensions

- `product_native_fit`
- `structure_and_composition`
- `asset_credibility`
- `iteration_clarity`

### Common Failure Watchlist

- 只借了科技配色，没有项目结构特征
- 更像抽象系统图
- 看起来高级，但没法做 hero
- 一叠标题就破画面

## Scenario 3. `bm_ui_mockup_credibility`

### Goal

验证 skill 是否能生成可信 UI mockup，而不是 UI 风格插画。

### Typical Request Shape

- dashboard
- mobile app screen
- onboarding UI visual

### What To Hold Constant

- 页面类型
- fidelity 预期
- 平台或设备上下文

### What This Scenario Should Stress

- 信息层级是否可信
- 组件关系是否像真实产品
- 是否出现伪品牌名、伪 logo、伪账号身份

### High-Value Dimensions

- `intent_match`
- `product_native_fit`
- `asset_credibility`
- `anti_ai_artifact`

### Common Failure Watchlist

- UI 风格插画化
- 组件逻辑失真
- 自动出现未要求品牌信息
- 文本块像生成噪音

## Scenario 4. `bm_app_asset_onboarding_scene`

### Goal

验证 skill 是否能为 onboarding 这类单图叙事 app asset 正确切到 `directed natural language` 写法，而不是继续沿用高结构字段骨架。

### Typical Request Shape

- onboarding 插图
- 功能说明插图
- app 内单张叙事视觉

### What To Hold Constant

- use case: `app-asset`
- 结果要服务真实产品界面，而不是脱离产品语境的独立概念画
- 默认不要求复杂 UI 模块板

### What This Scenario Should Stress

- 单主体叙事是否自然
- 是否能和真实 onboarding copy / layout 共存
- 文本层策略是否明确，即使结果不直接渲染文字
- 自然语言 prompt 是否比字段式堆叠更稳定

### High-Value Dimensions

- `intent_match`
- `product_native_fit`
- `structure_and_composition`
- `anti_ai_artifact`

### Common Failure Watchlist

- 被写成结构化信息板
- 画面虽然好看，但无法贴合真实 onboarding 场景
- 自动出现无关文案、logo 或 UI 噪音
- 叙事和产品用途脱节

## Scenario 5. `bm_icon_small_size`

### Goal

验证 icon 或小尺寸 app asset 在缩小后是否仍清晰、稳定、可读。

### Typical Request Shape

- app icon
- feature icon
- small badge-like asset

### What To Hold Constant

- 核心 metaphor
- 使用场景
- 小尺寸可读性要求

### What This Scenario Should Stress

- silhouette 是否清楚
- 缩小后是否仍可辨认
- 细节是否过多
- 工艺是否干净

### High-Value Dimensions

- `asset_credibility`
- `craft_finish`
- `anti_ai_artifact`

### Common Failure Watchlist

- 小尺寸发糊
- 细节堆太多
- 边缘脏
- 轮廓不稳

## Scenario 6. `bm_fixed_element_delivery`

### Goal

验证 skill 能否把底图推进成带标题、二维码、logo 或 badge 的真实交付资产。

### Typical Request Shape

- 招募海报
- 活动传播图
- 带 CTA 的 hero banner

### What To Hold Constant

- 主视觉 brief
- 固定元素清单
- 目标尺寸与导出要求

### What This Scenario Should Stress

- `visual_base_plus_post` 判断是否正确
- `text_safe_visual` 是否真实可用
- 二维码和 logo 落位是否像设计而不是补丁
- 多尺寸版本是否仍稳定

### High-Value Dimensions

- `text_and_layout_fidelity`
- `structure_and_composition`
- `asset_credibility`
- `iteration_clarity`

### Common Failure Watchlist

- 文字压坏主体
- 二维码难扫
- logo 抢主标题
- 一换尺寸就跑版

## Benchmark Cadence Guidance

### Minimal Regression Pack

如果只是一次中等规模改动，默认至少跑：

1. `bm_project_hero_repo`
2. `bm_ui_mockup_credibility`
3. `bm_fixed_element_delivery`

如果这次改动影响 scene profiling、support tier、runtime schema 或 promotion gate，再补：

4. `1` 个 `exploratory` lane 场景

### Full Validation Pack

如果修改了 strategy、delivery、runtime schema 或 promotion 的核心规则，建议跑全套 6 个场景，并额外补 `1` 个 exploratory lane 场景。

### Prompt-System Regression Pack

如果改动的是 prompt family 选择、text layer 规则、prompt assembly 顺序或 sample prompt 默认骨架，默认至少跑：

1. `bm_social_creative_launch`
2. `bm_project_hero_repo`
3. `bm_ui_mockup_credibility`
4. `bm_app_asset_onboarding_scene`

如果这次改动还影响 `repair`，再补一轮：

5. 在 `bm_social_creative_launch` 或 `bm_ui_mockup_credibility` 上追加一次 repair pass

## Pass Criteria

benchmark 不要求每个场景都直接 `pass`，但至少应满足：

- 没有明显新增红旗
- candidate 相比 baseline 有清楚改善
- 如果总分没显著提高，也要减少某类关键风险

按 support tier 看，建议再加一层最低判断：

- `accelerated`: 目标 `80+`
- `standard`: 目标 `70+`
- `exploratory`: 目标 `60+`，且 failure / correction / next input 清楚

以下情况可判本次 benchmark 有效：

- baseline `fail`，candidate 到 `conditional_pass`
- baseline `conditional_pass`，candidate 到 `pass`
- baseline 和 candidate 分数接近，但 candidate 去掉了一票否决红旗

## Benchmark Output Contract

每次场景验证建议至少产出：

- 一份 benchmark run 记录
- 如涉及策略对比，再加一份 A/B 记录
- 一句结论：保留什么、放弃什么、下一轮改什么

## Promotion Link

下面这些 benchmark 结果尤其值得进入 promotion review：

- 某条 correction rule 跨场景复现
- 某个 delivery 规则显著降低返工
- 某种 route 选择在多个场景里更稳
- 某个 pattern 在至少两个场景中都有帮助
