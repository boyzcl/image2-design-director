# Prompt Writing Spec

## Purpose

这份文档基于对外部优质案例的研究，收束一套适合 `image2-design-director` 的通用 prompt 书写规范。

研究来源之一：

- `references/external-prompt-research/youmind-gpt-image-2-curated-examples.md`

目标不是追求一种唯一格式，而是明确：

- 什么信息必须写
- 不同类型任务该用什么组织方式
- 什么叫“有用的结构”

## Core Position

好 prompt 不是“更多形容词”。

好 prompt 更像：

- 一份视觉任务说明
- 一份画面结构蓝图
- 一份约束清单

一句话版本：

> 先定义任务与结构，再定义风格与气质；先让模型知道要做什么，再让它知道要做得多美。

## Five Core Principles

### 1. Start With Task Type, Not Style Mood

先说清这是什么：

- 海报
- 落地页
- UI 样机
- 信息图
- 品牌系统页
- 单张动作插画

不要一开头就只有：

- cinematic
- beautiful
- stunning
- highly detailed

### 2. Describe The Information Architecture

如果任务有结构，就必须写结构。

常见结构包括：

- `header / hero / footer`
- `left / center / right`
- `quadrants`
- `sections`
- `cards`
- `sidebar`
- `timeline`

### 3. Enumerate Key Elements And Counts

对复杂任务，数量越模糊，结果越容易漂。

更好的写法是：

- 3 个统计卡
- 左侧 8 个标签
- 2x2 网格
- 底部 6 个步骤

### 4. Separate Content From Style

至少把下面几层分开：

- 任务是什么
- 画面里有什么
- 这些内容如何排布
- 整体长什么气质

### 5. Treat Text As A Design Layer

文字不是附属品。

如果任务里文字很重要，要写清：

- 是否必须 verbatim
- 放在哪
- 需要多少层级
- 是主标题、标签还是说明文字

## Recommended Prompt Forms

这套规范建议三种主写法。

### Form A. Structured Object

适用于：

- 信息图
- UI 展示
- 品牌系统页
- 复杂海报
- 多模块落地页

推荐字段：

```yaml
type:
theme:
subject:
style:
layout:
sections:
text:
constraints:
avoid:
```

### Form B. Section-Based Outline

适用于：

- landing page
- poster with sub-blocks
- multi-panel ad
- multi-touchpoint brand board

推荐结构：

```text
Task:
Overall aesthetic:
Main subject:
Global constraints:

Section 1:
Section 2:
Section 3:
...
```

### Form C. Directed Natural Language

适用于：

- 单张角色图
- 动作场景
- 单一叙事插画
- 氛围主视觉

推荐顺序：

```text
Subject
Action
Appearance
Environment
Composition
Lighting
Key constraints
```

## Universal Field Checklist

无论采用哪种形式，至少应尽量覆盖下面 8 类信息。

| Field Group | What It Answers |
|---|---|
| `task_type` | 这是什么资产 |
| `goal` | 这张图要解决什么问题 |
| `subject` | 主体是谁或是什么 |
| `structure` | 内容怎么分区、怎么布局 |
| `text_layer` | 文字是什么、在哪里、几层 |
| `style_layer` | 整体审美与媒介感 |
| `hard_constraints` | 不能跑偏的点 |
| `avoid` | 明确不要出现什么 |

## Writing Rules By Task Class

### A. Poster / Social Creative

必须写清：

- 核心信息
- 主视觉隐喻
- 标题区
- 画面层级
- 海报感而不是信息板感

推荐优先级：

1. 传播目标
2. 中心隐喻
3. 标题结构
4. 风格和灯光

如果这是项目发布海报或产品 launch poster，再额外补一层：

- 转化隐喻必须尽量落到项目机制，而不是只靠抽象几何和情绪词

优先可写成：

- `brief packet`
- `route trace`
- `scorecard`
- `prompt assembly`
- `delivery-ready asset`

### B. UI Mockup

必须写清：

- 页面类型
- 设备或平台
- 模块分区
- 组件数量级
- 是否需要真实文本或仅示意

### C. Infographic / Diagram

必须写清：

- 主体结构
- 信息分组
- 标签数量
- 图例
- 标题和说明区

### D. Brand System / Campaign Board

必须写清：

- 主题色
- motif
- 核心角色或品牌元素
- 落点类型
- 各落点内容

### E. Single Illustration / Action Scene

必须写清：

- 谁在做什么
- 关键服装或外观
- 视角
- 光影
- 动态效果

### F. Repo Hero / System Hero

必须写清：

- 这是不是项目系统 hero，而不是消费品 hero
- 哪些协议型视觉元素是核心锚点
- 留白区或 copy-safe 区在哪里
- 哪些错误语义必须被排除

推荐优先级：

1. hero 的使用场景
2. 协议型 motif
3. 构图和留白
4. 语义排除

## Parameterization Rules

研究案例里一个很值得借鉴的点是参数化写法：

```text
{argument name="theme color" default="soft pink"}
```

这类写法的价值在于：

- 让 prompt 更可复用
- 让模板和实例分开

在本项目里，不一定要照搬这种语法，但建议保留这个思想：

- 把可变化的内容单独标出来
- 把默认值和结构模板分开

## Good Prompt Signals

如果一段 prompt 足够好，通常会出现这些信号：

- 先说任务，不先说美学
- 对复杂内容做了区块拆分
- 对关键元素有数量或位置描述
- 风格词不泛滥
- 有明确 `avoid`
- 文本层被当作正式设计层处理

## Bad Prompt Signals

下面这些信号出现越多，prompt 越可能失控：

- 只有情绪词，没有任务词
- 只有风格词，没有结构词
- 对复杂页面完全不分区
- 希望模型“自动补全所有内容”
- 文案很重要，却不写文字策略
- 没有负向约束

## Minimal Templates

### Template 1. Structured Poster

```yaml
type: ""
goal: ""
subject: ""
centerpiece: ""
layout:
  title_area: ""
  middle_area: ""
  bottom_area: ""
text:
  headline: ""
  supporting_text: []
style:
  medium: ""
  palette: ""
  lighting: ""
constraints:
  - ""
avoid:
  - ""
```

### Template 2. Section-Based UI / Landing

```text
Task: <what this asset is>
Goal: <what this page should communicate>
Overall aesthetic: <theme + tone>
Main subject/device: <if any>
Global constraints: <hard rules>

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

Avoid:
- ...
```

### Template 3. Directed Single-Scene Illustration

```text
Create a <scene type>.
The main subject is <who/what>.
They are <action>.
Appearance details: <key look>.
Environment: <where>.
Composition: <camera/framing>.
Lighting: <light and mood>.
Key constraints: <non-negotiables>.
Avoid: <negative constraints>.
```

## Recommended Next Step

这份规范适合作为：

1. intake 之后的 prompt assembly 参考
2. sample prompt 升级时的统一框架
3. benchmark 中的 prompt quality 检查标准
