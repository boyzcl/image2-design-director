# Prompt Schema

## Purpose

这份文档定义：

- prompt 应该先选哪一种写法
- 进入最终 image prompt 前，哪些层必须保留
- asset contract、information contract 和 representation mode 如何进入最终 prompt

一句话版本：

> 先资产合同，再信息合同，再表达机制，最后才是视觉语言；文本层不是附属备注，确定性内容也不该被伪装成 prompt 里的装饰说明。

## Core Rules

### 1. Asset Contract And Information Contract Before Prompt Family

先明确：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`
- `factual_sensitivity`
- `claim_type`
- `metric_definition`
- `uncertainty_policy`

再决定 prompt family。

### 2. Representation Mode Before Prompt Family

先决定：

- `representation_mode`
- `primary_expression_system`
- `deterministic_render_needed`
- `text_generation_tolerance`
- `numeric_render_strategy`

如果这轮不是纯模型直出，就不要把最终交付物全部塞进同一种 prompt。

### 3. Task Before Style

先写清：

- 这是什么资产
- 它要解决什么问题
- 用户最终想拿去做什么

### 4. Text Layer Is A Formal Design Layer

只要任务涉及文字，prompt 里就要明确：

- 文案语言
- 允许出现的文字范围
- 文字是否必须 verbatim
- 文字有几层层级
- 文字由模型直出还是只保留安全区

### 5. Completion Mode Must Be Explicit

最终 prompt 必须明确告诉模型：

- 这是完整成品
- 或这是底图

### 6. Final Prompt Should Read Like Production Direction

最终 prompt 应像设计指令，而不是字段 dump。

## Shared Preparation Fields

```text
Domain direction: <...>
Matched profile: <...>
Support tier: <...>
Deliverable type: <brand promo poster / README hero / onboarding visual / ...>
Asset completion mode: <complete_asset / base_visual / delivery_refinement>
Factual sensitivity: <low / medium / high>
Claim type: <visual_analogy / factual / comparative / ...>
Metric definition: <...>
As-of date: <...>
Uncertainty policy: <...>
Representation mode: <...>
Primary expression system: <image_model / deterministic_renderer / hybrid>
Content language: <zh-CN / en / ...>
Allowed text scope: <what readable text is allowed>
Layout owner: <model / post_process / hybrid>
Acceptance bar: <怎样才算可验收>
Subject: <主体>
Scene/backdrop: <环境或背景>
Structure/layout: <区块、镜头、留白、版式>
Text layer: <文案、层级、位置、直出策略>
Style/medium: <...>
Visual priorities: <最不能跑偏的点>
Constraints: <必须保留>
Avoid: <负向约束>
```

## Prompt Family Selection

- 多区块、多模块、多文案层：`Structured / Section-Based`
- 单主体但要可用留白和商业版式：`Hybrid Structured Hero`
- 单图叙事、动作或氛围主视觉：`Directed Natural Language`
- 迭代修正已有图：在原 family 上加 `Repair Overlay`

如果 `representation_mode` 是 `hybrid` 或 `deterministic`，family 只负责图像段，不负责精确数值段。

## Universal Assembly Order

默认按这个顺序装配：

1. `Asset contract layer`
2. `Information contract layer`
3. `Representation layer`
4. `Task layer`
5. `Subject layer`
6. `Structure layer`
7. `Text layer`
8. `Style layer`
9. `Hard constraints`
10. `Avoid`
11. `Repair overlay`

## Text Layer Requirements

### For `complete_asset`

必须明确：

- 可读文字只有哪些
- 哪些文字是唯一允许出现的
- 默认语言是什么
- 不允许额外小字、伪 UI 文案、随机英文

### For `base_visual`

必须明确：

- 这轮不负责最终文字
- 只保留标题区、安全区或可承载文案的干净背景

### For High-Fact-Sensitivity Tasks

必须明确：

- 哪些数字、价格、日期不会由模型直接生成
- 哪些结论已被锁定
- 哪些内容只是视觉隐喻

## Default Skeleton

```text
Deliverable: <what this final asset is>
Completion mode: <complete_asset / base_visual>
Information contract: <what may be stated as fact, what may only be implied>
Representation mode: <model / hybrid / deterministic>
Objective: <what it must help accomplish>
Audience/context: <who and where it will be used>
Content language: <default language>
Allowed text scope: <what readable text is allowed>
Acceptance bar: <what counts as usable>

Main subject/system: <main visual system>
Structure/layout: <hierarchy, safe areas, focal zones>
Text layer: <headline / slogan / subtitle or safe-area-only>
Style layer: <medium, palette, material, lighting>
Constraints: <hard rules>
Avoid: <what to exclude>
```

## Repair Overlay

如果是 `contract_realign`，prompt delta 之前必须先重写：

- deliverable
- completion mode
- content language
- allowed text scope
- metric definition
- representation mode
