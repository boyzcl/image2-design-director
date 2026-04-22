# Intake Schema

## Purpose

这份文档定义 `image2-design-director` 在执行闭环第一阶段的稳定 intake 结构。

目标不是立刻写 prompt，而是先把下面几件事收清楚：

- 用户到底想要什么
- 这张图最终在哪里使用
- 这次任务的上下文边界是什么
- 有没有固定文本、二维码、logo、尺寸或交付约束
- 用户认为什么才算“这轮已经过线”
- 这轮任务更像直出任务，还是应为后处理留接口

一句话版本：

> intake 的职责是把“用户原话”和“可执行上下文”收成稳定任务入口，而不是直接替代 strategy 和 prompt。

## Position In The Loop

这个 schema 属于：

- `Stage 1. Requirement Intake`

它输出的内容应交给下一阶段：

- `Stage 2. Strategy Selection`

所以 intake 的产物应该足够清楚，但不应该提前做太多策略判断。

## Core Principles

### 1. Raw Request And Structured Understanding Must Stay Separate

必须同时保留：

- 用户原始请求
- 我们理解后的需求摘要

不要把用户原话直接覆盖成“整理后的版本”，否则后面难以回看误解是怎么发生的。

### 2. Context Is Part Of The Requirement

背景不是附件，而是需求的一部分。

对于很多图像任务，下面这些信息会直接改变输出结果：

- 产品或品牌语境
- 使用场景
- 受众
- 交付渠道
- 是否允许后处理

### 3. Ask Only High-Leverage Questions

如果需要补问，只问那些会显著改变结果的问题。

不要在 intake 阶段问大量偏风格偏好小题目，除非这些偏好真的是本轮成败关键。

### 4. Intake Should Produce Reusable Structure

intake 产物不只是服务当前轮 prompt，也要服务：

- strategy 选择
- runtime capture
- repair 诊断
- 后续经验晋升

## Intake Outputs

一次合格的 intake 至少应产出下面四个对象。

### 1. Raw Request

保留用户原话或原始素材入口。

### 2. Requirement Summary

把“这次要交付什么”收成简洁、可执行的摘要。

### 3. Context Summary

把背景、产品语境、素材来源、风险边界收成上下文摘要。

### 4. Delivery Constraints Snapshot

把固定文本、二维码、尺寸、直出 / 后处理等交付限制单独列出。

## Minimum Intake Contract

下面这些字段构成最小 intake 合同。

### Required Core Fields

这些字段在绝大多数任务里都应该有。

| Field | Required | Meaning |
|---|---|---|
| `user_raw_request` | yes | 用户原始请求，不做改写 |
| `user_goal` | yes | 用户最终想要达成什么 |
| `asset_type` | yes | 资产类型，如 hero、feed post、icon、onboarding visual |
| `usage_context` | yes | 最终使用位置或渠道 |
| `requirement_summary` | yes | 我们对交付目标的结构化摘要 |
| `context_summary` | yes | 与本轮输出直接相关的背景摘要 |
| `direct_output_vs_post_process` | yes | 预判更适合直出还是后处理辅助 |

### Conditional Fields

这些字段不是每次都必须有，但一旦任务涉及，就应明确记录。

| Field | Required When | Meaning |
|---|---|---|
| `background_context` | 任务绑定具体项目、产品、品牌、活动时 | 任务的业务或产品背景 |
| `brand_or_product_sources` | 用户给了仓库、截图、页面、品牌资料时 | 上下文来源列表 |
| `target_audience` | 受众会改变表达方式时 | 目标受众 |
| `fixed_text` | 有必须准确出现的文案时 | 必须保留的文字 |
| `fixed_elements` | 有二维码、logo、badge、价格条等时 | 必须出现的固定元素 |
| `size_and_delivery_constraints` | 有尺寸、比例、导出格式要求时 | 交付约束 |
| `success_criteria` | 用户明确表达“什么样算过线”时，或我们需要主动收束验收标准时 | 用户预期中的通过标准 |
| `reference_assets` | 有参考图、旧版本、已有素材时 | 已有可参考资产 |
| `source_materials` | 用户给了 PDF、截图、页面、附件、现有图片、设计稿时 | 任务直接依赖的输入素材 |
| `existing_generation_context` | 用户已有上一版、已有失败图、或当前任务本质是修图时 | 对已有结果的说明 |
| `must_avoid` | 有明确禁区时 | 必须避免的方向 |

### Execution-Handoff Fields

这些字段不是最终 prompt 本身，但会直接影响下一阶段判断。

| Field | Required | Meaning |
|---|---|---|
| `open_questions` | yes | 当前仍未确定、但可能影响结果的问题 |
| `missing_critical_fields` | yes | 当前缺失的关键字段 |
| `intake_confidence` | yes | 当前 intake 完整度的主观判断：`low / medium / high` |
| `recommended_route_hint` | yes | 只给出建议方向：`direct / brief-first / repair` |

## Field Guidance

### `user_goal`

不要写成“生成一张图”。

要写成用户真正想完成的事情，例如：

- 为项目主页准备一张介绍 hero 图
- 为测试招募做一张传播图
- 为 app onboarding 准备一张系统兼容的配图

### `asset_type`

尽量具体，不要只写“宣传图”。

更推荐：

- `project hero`
- `feed creative`
- `launch poster`
- `App Store listing image`
- `icon`
- `text-safe background visual`

### `usage_context`

这里回答的是“它最终放哪里”，不是“它长什么样”。

例如：

- 项目 README 顶部
- 社媒首发配图
- 招募页面 header
- App Store 截图底图

### `context_summary`

只保留会影响结果的重要上下文，不做散漫背景介绍。

上下文摘要应优先包含：

- 产品 / 项目本体是什么
- 这轮图像服务于哪种目标
- 当前已有的视觉线索来自哪里
- 当前最不能偏离的边界是什么

### `success_criteria`

这里回答的是：

- 用户认为什么样算完成
- 我们后面评估时最该对齐的通过条件是什么

推荐写法：

- “需要像真实项目 hero，而不是抽象概念图”
- “必须能安全叠加中文标题”
- “图中不能自带错误英文或失真文案”
- “至少要达到可对外展示的高质量草稿”

不要只写：

- “好看”
- “高级”
- “有感觉”

### `existing_generation_context`

如果任务已经不是第一次生成，而是对上一版做修复，这个字段应明确写：

- 上一版的问题是什么
- 用户显式不满意什么
- 本轮是“重做”还是“最小纠偏”

这能避免下一阶段把 repair 任务误判成全新 direct 任务。

### `direct_output_vs_post_process`

只允许写三种值：

- `direct_output`
- `visual_base_plus_post`
- `undecided`

这里先做 intake 层判断，不展开具体后处理方案。

## Intake Question Policy

### When To Ask Follow-Up Questions

当下面任一项缺失且会显著改变结果时，应该补问：

- 最终使用位置不清楚
- 资产类型不清楚
- 固定文本或固定元素不清楚
- 是否允许后处理不清楚
- 任务绑定具体产品，但上下文来源不清楚
- 用户的通过标准不清楚
- 用户已经有上一版结果，但上一版的问题没有说清楚

### Question Budget

默认最多问 `1-3` 个问题。

优先级顺序：

1. 使用位置
2. 资产类型
3. 最不能跑偏的约束

### When Not To Ask

如果下面这些已经足够明确，优先直接进入下一阶段：

- 用途明确
- 资产类型明确
- 上下文边界明确
- 没有高风险固定文本或固定元素要求

## Output Template

推荐把一次 intake 先收成下面这个结构。

```yaml
user_raw_request: ""
user_goal: ""
asset_type: ""
usage_context: ""
requirement_summary: ""
context_summary: ""
background_context: ""
brand_or_product_sources: []
target_audience: ""
fixed_text: []
fixed_elements: []
size_and_delivery_constraints: []
success_criteria: []
reference_assets: []
source_materials: []
existing_generation_context: ""
must_avoid: []
direct_output_vs_post_process: "undecided"
open_questions: []
missing_critical_fields: []
intake_confidence: "medium"
recommended_route_hint: "brief-first"
```

## Example

```yaml
user_raw_request: "帮我给 ai-native-loop 做一张介绍 skill 的宣传图。"
user_goal: "为项目介绍页和社媒发布准备一张可继续排版的主视觉。"
asset_type: "project hero"
usage_context: "docs / landing page / social announcement"
requirement_summary: "需要一张更像真实项目物料的 hero 图，能体现 ai-native-loop 的协议闭环和 runtime memory 特征。"
context_summary: "ai-native-loop 是协议型 workflow skill，核心语义是 input-execution-feedback-reinput loop、multi-agent collaboration、runtime capture 和经验复利。"
background_context: "服务于已有项目 ai-native-loop，而不是纯概念视觉。"
brand_or_product_sources:
  - "<related-project>/README.md"
  - "<related-project>/SKILL.md"
target_audience: "会第一次接触这个 skill 的开发者和 AI-native workflow 用户"
fixed_text: []
fixed_elements: []
size_and_delivery_constraints:
  - "16:9 hero"
  - "需要预留后续中文标题区域"
success_criteria:
  - "更像真实项目物料，而不是抽象概念图"
  - "需要能安全叠加后续中文标题"
  - "至少达到可对外展示的高质量草稿"
reference_assets: []
source_materials: []
existing_generation_context: ""
must_avoid:
  - "generic AI poster"
  - "excessive glow"
  - "dense baked-in English text"
direct_output_vs_post_process: "visual_base_plus_post"
open_questions: []
missing_critical_fields: []
intake_confidence: "high"
recommended_route_hint: "direct"
```

## Runtime Alignment

当前阶段虽然 task packet 和 strategy tree 还未正式文档化，但 intake 至少应能稳定喂给 runtime 这些信息：

- `user_raw_request`
- `requirement_summary`
- `context_summary`
- `direct_output_vs_post_process`
- `fixed_text`
- `fixed_elements`
- `size_and_delivery_constraints`

后续 runtime capture schema 应逐步补齐这些字段，而不是只记录 prompt 和结果。

## Intake Completion Checklist

在把 intake 交给下一阶段前，建议用下面这份 checklist 过一遍。

### Must Be Clear

- 用户真正想达成的目标是什么
- 最终交付资产是什么
- 最终使用位置是什么
- 与这轮结果强相关的上下文是什么
- 是否有固定文本、固定元素、尺寸或导出要求
- 用户认为什么算通过
- 当前更适合直出还是后处理辅助

### Must Be Explicit If Present

- 是否已有上一版结果
- 是否已有参考图或源素材
- 是否绑定具体产品、品牌、页面或仓库
- 是否已有明确禁区

### Should Trigger Follow-Up If Missing

- 使用位置缺失
- 资产类型缺失
- 成功标准缺失
- 固定元素要求模糊
- 上一版问题描述模糊

## Minimum Pass Standard

如果下面任一项还不清楚，就不应把 intake 视为“已经收住”：

- 交付资产是什么
- 最终用在哪里
- 任务上下文边界是什么
- 是否有固定文本 / 固定元素 / 尺寸限制
- 用户认为什么算通过
- 当前更适合直出还是后处理辅助

## What This Schema Does Not Do

这份 schema 不负责：

- 最终 prompt 组装
- 失败模式判断
- repair 策略
- 后处理具体操作
- benchmark 和 A/B 试验设计

这些能力应交给后续阶段和对应文档。
