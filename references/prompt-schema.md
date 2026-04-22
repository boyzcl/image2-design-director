# Prompt Schema

## Purpose

这份文档不是单纯的字段表。

它定义的是：

- prompt 应该先选哪一种写法
- 不同写法各自的骨架是什么
- 从 task packet 进入最终 image prompt 时，哪些层必须保留

一句话版本：

> 先任务，后结构，再风格；文本层不是附属备注，而是正式设计层。

## What This Schema Solves

目标不是把所有任务都压成同一种格式，而是避免两类常见问题：

1. 复杂任务只剩一串字段，没有真正形成可执行结构
2. 单图叙事任务被硬写成表格，失去自然画面张力

因此，默认先选 prompt family，再落具体字段。

## Core Rules

### 1. Task Before Style

先写清：

- 这是什么资产
- 它要解决什么问题
- 用户最终想拿去做什么

不要一上来堆：

- cinematic
- premium
- stunning
- highly detailed

### 2. Structure Before Detail Spray

如果任务有模块、区块、层级、象限、标题区、安全区、设备区，就先写结构，不要把这些信息埋进形容词里。

### 3. Text Layer Is A Formal Design Layer

只要任务涉及文字，prompt 里就要明确：

- 文字是否必须 verbatim
- 文字有几层层级
- 文字放在哪个区域
- 文字是最终直出，还是只保留标题区 / 安全区

长中文文本是高风险信号，但不是 `direct_output` 的硬挡板。

如果用户给了可直出的参考图，或当前任务本身就在测试直出能力，必须保留 `direct_output` 候选。

### 4. Parameterize Before You Polish

模板阶段先把变量和默认骨架分开，再生成最终 prompt。

推荐用占位符表达可变项，例如：

```text
{{asset_type}}
{{headline}}
{{subject}}
{{layout_note}}
```

真正发送给 Image2 前，要把占位符全部解析成具体内容。

### 5. Final Prompt Should Read Like Production Direction

schema 是组装层，不是最终交付格式本身。

最终 prompt 应该像一份给模型的设计指令，而不是数据库字段 dump。

## Prompt Family Selection

### Family A. Structured / Section-Based

适用于：

- 信息量高的海报
- UI mockup
- landing page
- design system board
- infographic
- 一图多模块 campaign creative

默认特征：

- 有明确区块
- 有数量、位置、层级
- 文字区需要被设计
- 可以使用字段式或 section-based 写法

### Family B. Hybrid Structured Hero

适用于：

- 产品 hero
- 社媒主视觉
- 有单一主物体，但仍需要安全留白或标题区
- 产品图、设备图、品牌视觉底图

默认特征：

- 画面主体相对集中
- 结构比 UI 简单，但仍有版式约束
- 适合短字段块，不必过度分 section
- 如果任务是 repo hero、项目系统 hero、workflow hero，主体不能只写成开放式 `workflow`
- 这类 hero 默认要优先锚定协议型视觉元素，例如 `packet card`、`route node`、`prompt assembly layer`、`scorecard chip`、`delivery-state frame`
- 对项目系统 hero，要显式排除消费品、电商 listing、shopping UI、实体商品语义，避免 domain drift

### Family C. Directed Natural Language

适用于：

- 单图叙事插画
- 动作场景
- 单一中心隐喻画面
- 角色或物体在环境中的主视觉

默认特征：

- 主体和动作连续推进
- 画面更依赖镜头、环境、光影和叙事
- 不需要把内容硬拆成多个 section

### Family D. Repair Overlay

适用于：

- 已有结果不理想
- 需要单变量纠偏
- 必须明确保留什么、不改什么

它不是单独的 family，而是附着在 A、B、C 任一写法上的修正层。

## Family Selection Heuristic

优先按任务复杂度和版式复杂度选，而不是按画风选。

- 多区块、多模块、多文案层：选 `Structured / Section-Based`
- 单主体但要可用留白和商业版式：选 `Hybrid Structured Hero`
- 单图叙事、动作或氛围主视觉：选 `Directed Natural Language`
- 迭代修正已有图：在原 family 上加 `Repair Overlay`

## Universal Assembly Order

无论选哪种 family，默认都按这个顺序装配：

1. `Task layer`
   - 这是什么资产
   - 它服务什么目标
2. `Subject layer`
   - 主体是谁或是什么
   - 核心场景是什么
3. `Structure layer`
   - 区块、布局、视角、留白、安全区、数量
4. `Text layer`
   - 文案内容、层级、位置、直出策略
5. `Style layer`
   - 媒介感、材质感、灯光、审美气质
6. `Hard constraints`
   - 不能跑偏的点
7. `Avoid`
   - 明确不要什么
8. `Repair overlay`
   - `Change only`
   - `Keep unchanged`

## Shared Preparation Fields

下面这些字段适合作为 prompt assembly 的准备层，不一定全部原样出现在最终 prompt 里。

```text
Domain direction: <open-ended asset or scene direction>
Matched profile: <product-mockup | social-creative | ui-mockup | app-asset | custom | none>
Support tier: <accelerated | standard | exploratory>
Asset type: <landing hero / feed post / onboarding screen / app illustration / ...>
Primary request: <用户要什么>
Objective: <这张图要帮助完成什么>
Audience/context: <目标受众或使用场景>
Subject: <主体>
Scene/backdrop: <环境或背景>
Structure/layout: <区块、镜头、留白、版式>
Text layer: <文案、层级、位置、直出策略>
Style/medium: <商业摄影 / editorial / app UI / 3D / illustration ...>
Visual priorities: <最不能跑偏的点>
Constraints: <必须保留>
Avoid: <负向约束>
```

## Default Skeletons

### Skeleton A. Structured / Section-Based

适用于高结构任务。

```text
Task: <what this asset is>
Goal: <what it should achieve>
Audience/context: <who and where it will be used>
Main subject/system: <main visual system>
Global constraints: <hard rules>

Structure:
- overall layout:
- focal hierarchy:
- safe space / title zone:

Section 1:
- role:
- content:
- visual treatment:

Section 2:
- role:
- content:
- visual treatment:

Section 3:
- role:
- content:
- visual treatment:

Text layer:
- mode: <verbatim / partial / none / safe-area-only>
- hierarchy:
- placement:

Style layer:
- medium:
- palette:
- lighting/material:

Avoid:
- ...
```

### Skeleton B. Hybrid Structured Hero

适用于产品图、主视觉、单主体 campaign creative。

```text
Use case: <...>
Asset type: <...>
Primary request: <...>
Objective: <...>
Audience/context: <...>
Subject: <...>
Scene/backdrop: <...>
Composition/framing: <camera + layout + negative space>
Text layer: <headline strategy or safe-area strategy>
Style/medium: <...>
Visual priorities: <1-3 non-negotiables>
Constraints: <...>
Avoid: <...>
```

#### Hybrid Structured Hero Tightening

如果 hero 服务的是 repo、项目、系统能力说明，而不是消费品展示，默认补两层约束：

1. `Motif anchors`
   - 指定 3 到 5 个协议型视觉锚点
   - 例如：`intake packet`、`route decision node`、`prompt assembly layer`、`scorecard chip`、`delivery-ready asset frame`
2. `Semantic exclusions`
   - 明确排除容易漂移到别的垂类的语义
   - 例如：`consumer product`、`furniture`、`backpack`、`shopping UI`、`ecommerce listing`

默认原则：

- 不要只写抽象 `workflow`
- 要把“这是哪个系统”翻译成可被画出来的协议元素
- 如果 hero 里出现 review frame，也要尽量约束为中性资产，而不是另一个强垂类题材
- 如果 hero 里出现 `delivery-ready asset frame`，默认把它约束成中性项目资产、editorial crop 或 product-safe visual，不要让模型自行补成风景、建筑或另一类强题材样张
- 默认不要只写 `neutral project asset`
- 要继续补 1 到 3 个允许的 destination asset example，例如：
  - `README hero plate`
  - `onboarding visual card`
  - `benchmark board preview`
- 同时补一组硬排除：
  - `landscape photo`
  - `architecture render`
  - `room scene`
  - `framed art print`
  - `travel-style sample`

### Skeleton C. Directed Natural Language

适用于单图叙事任务。

```text
Create a <scene type> for <asset goal>.
The main subject is <who/what>.
They are <action or state>.
The environment is <where>.
The composition should feel <framing and hierarchy>.
The text layer strategy is <none / leave clean title area / exact short title>.
The visual language should feel <medium, lighting, mood>.
Key constraints: <non-negotiables>.
Avoid: <negative constraints>.
```

## Scenario-Specific Tightening

### Structured / Section-Based Poster For Product Launch

当任务是 launch poster、社媒发布图、项目宣传海报时，默认不要只依赖抽象几何或泛设计隐喻。

要优先把 transformation metaphor 写成项目机制：

- `brief packet`
- `route trace`
- `scorecard / evaluation marks`
- `prompt assembly sheet`
- `delivery-ready asset frame`

如果标题需要 verbatim 直出，默认同时写清：

- `one main headline`
- 是否允许副标题
- 是否允许品牌 lockup
- 是否允许二级 caption

默认负向约束优先包含：

- generic logo poster
- furniture ad
- dashboard board
- badge wall
- secondary captions
- scenic-photo storyboard used as default destination asset
- framed landscape sample used as destination asset
- architecture render used as delivery frame

## Text Layer Rules

### When Text Is Required

至少写清四件事：

- `mode`: `verbatim`、`partial`、`emphasis-only`、`safe-area-only`
- `hierarchy`: 主标题、强调词、辅助信息分别有几层
- `placement`: 顶部、中部、底部、侧边、卡片内
- `density`: 文本偏少、适中、偏多

### When Text Is Not Required

也不要忽略文本层。

要明确说明：

- `no rendered text`
- 或 `leave clean title-safe area`

否则模型容易自己发明 logo、标签或伪文案。

### When Chinese Copy Is Long

- 先判断这轮是在测试 `direct_output` 还是默认做 `text-safe visual`
- 如果用户给了直出参考图，或任务明确是直出测试，不要自动降级成后处理
- 如果选择后处理路径，也要明确告诉模型保留哪个标题区、不要自造小字和说明块

## Parameterization Rules

模板写法里，默认把这些内容参数化：

- 资产类型
- 使用语境
- 主体
- 中心隐喻
- 标题文案
- section 数量
- 色彩和媒介
- 关键限制

不建议参数化的内容：

- 模糊形容词堆
- 没有复用价值的随机修饰词

## Repair Overlay

如果在修图，额外加上：

```text
Change only: <只改什么>
Keep unchanged: <必须保持什么>
```

默认要求：

- 一次只改最关键的 1 到 2 个变量
- 不要重写整段 prompt，除非问题根源在 prompt family 选错

## Quick Checks

如果 prompt 足够成熟，通常会同时满足：

- 一开头就能看出资产类型和目标
- 能看出画面是怎么组织的
- 文本层被正式处理，而不是顺手提一句
- 风格层服务任务，而不是压过任务
- 有明确的 `Avoid`
