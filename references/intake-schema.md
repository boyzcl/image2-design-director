# Intake Schema

## Purpose

这份文档定义 `image2-design-director` 在执行闭环第一阶段的稳定 intake 结构。

目标不是立刻写 prompt，而是先把下面几件事收清楚：

- 用户到底想要什么交付物
- 这次任务要不要直接交成品
- 文案语言和允许出现的文字范围是什么
- 这张图最终在哪里使用
- 这次任务的上下文边界是什么
- 有没有固定文本、二维码、logo、尺寸或交付约束

一句话版本：

> intake 先收“交付物合同”，再收视觉上下文；没有合同，就不应该过早进入生成策略选择。

## Position In The Loop

这个 schema 属于：

- `Stage 1. Requirement Intake`

它输出的内容应交给下一阶段：

- `Stage 2. Strategy Selection`

所以 intake 的职责不是替代 strategy，而是保证 strategy 拿到的是一份已经把“成品还是底图、语言是什么、完成标准是什么”说清楚的任务入口。

## Core Principles

### 1. Raw Request And Structured Understanding Must Stay Separate

必须同时保留：

- 用户原始请求
- 我们结构化理解后的结果

不要直接覆盖用户原话，否则后面无法定位误解源头。

### 2. Asset Contract Before Style

在讨论风格、构图和材质之前，必须先收清：

- 最终交付物是什么
- 是完整成品还是中间底图
- 谁来完成最后排版
- 文案语言是什么
- 什么才算用户可验收

### 3. Finished Asset By Default

如果用户没有明确说：

- “先给底图”
- “我后面自己排字”
- “预留标题区”

那默认应把任务视为：

- `complete_asset`

而不是默认滑向：

- `base_visual`

### 4. Conversation Language Is The Default Content Language

在用户未单独指定时：

- 当前会话语言 = 默认文案语言

项目名、产品名、repo 名可以保留原文，但 slogan、subtitle、CTA、supporting copy 默认跟随当前会话语言。

### 5. Ask Only High-Leverage Questions

如果需要补问，只问那些会显著改变交付物合同的问题。

优先问：

1. 这是成品还是底图
2. 文字要不要直出
3. 文案语言是什么
4. 最终放在哪里
5. 什么样算过线

## Intake Outputs

一次合格的 intake 至少应产出下面五个对象：

### 1. Raw Request

保留用户原话或原始素材入口。

### 2. Requirement Summary

把“这次要交付什么”收成简洁、可执行的摘要。

### 3. Asset Contract Snapshot

把“成品还是底图、语言是什么、允许哪些文字、由谁完成最终排版”单独收出来。

### 4. Context Summary

把背景、产品语境、素材来源、风险边界收成上下文摘要。

### 5. Delivery Constraints Snapshot

把固定文本、二维码、尺寸、直出 / 后处理限制单独列出。

## Minimum Intake Contract

下面这些字段构成最小 intake 合同。

### Required Core Fields

| Field | Required | Meaning |
|---|---|---|
| `user_raw_request` | yes | 用户原始请求，不做改写 |
| `user_goal` | yes | 用户最终想完成什么 |
| `asset_type` | yes | 资产类型，如 brand promo poster、project hero、feed creative |
| `usage_context` | yes | 最终使用位置或渠道 |
| `requirement_summary` | yes | 我们对交付目标的结构化摘要 |
| `context_summary` | yes | 与本轮输出直接相关的背景摘要 |
| `success_criteria` | yes | 用户视角的通过标准 |
| `direct_output_vs_post_process` | yes | intake 层对直出 / 后处理的初步判断 |

### Asset Contract Fields

下面这些字段现在应被视为 intake 的正式主字段。

| Field | Required | Meaning |
|---|---|---|
| `deliverable_type` | yes | 最终交付物类型，如 brand promo poster、README hero、launch poster |
| `asset_completion_mode` | yes | `complete_asset / base_visual / delivery_refinement / undecided` |
| `content_language` | yes | 当前默认文案语言 |
| `allowed_text_scope` | yes | 允许出现的可读文字范围 |
| `final_layout_owner` | yes | `model / post_process / hybrid` |
| `acceptance_bar` | yes | 用户可验收的完成定义 |

### Conditional Fields

| Field | Required When | Meaning |
|---|---|---|
| `background_context` | 任务绑定具体项目、产品、品牌、活动时 | 任务的业务或产品背景 |
| `brand_or_product_sources` | 用户给了仓库、截图、页面、品牌资料时 | 上下文来源列表 |
| `target_audience` | 受众会改变表达方式时 | 目标受众 |
| `fixed_text` | 有必须准确出现的文案时 | 必须保留的文字 |
| `fixed_elements` | 有二维码、logo、badge、价格条等时 | 必须出现的固定元素 |
| `size_and_delivery_constraints` | 有尺寸、比例、导出格式要求时 | 交付约束 |
| `reference_assets` | 有参考图、旧版本、已有素材时 | 已有可参考资产 |
| `source_materials` | 用户给了 PDF、截图、页面、附件、现有图片、设计稿时 | 任务直接依赖的输入素材 |
| `existing_generation_context` | 用户已有上一版、已有失败图、或当前任务本质是修图时 | 对已有结果的说明 |
| `must_avoid` | 有明确禁区时 | 必须避免的方向 |

### Execution-Handoff Fields

| Field | Required | Meaning |
|---|---|---|
| `open_questions` | yes | 当前仍未确定、但可能影响结果的问题 |
| `missing_critical_fields` | yes | 当前缺失的关键字段 |
| `intake_confidence` | yes | `low / medium / high` |
| `recommended_route_hint` | yes | 只给建议方向：`direct / brief-first / repair / contract_realign` |

## Field Guidance

### `deliverable_type`

要写最终资产，不要写视觉气氛。

更推荐：

- `brand promo poster`
- `project launch poster`
- `README hero`
- `feed creative`
- `onboarding visual`

不要只写：

- “宣传图”
- “高级海报”

### `asset_completion_mode`

只允许：

- `complete_asset`
- `base_visual`
- `delivery_refinement`
- `undecided`

默认规则：

- 用户没说要中间稿时，优先 `complete_asset`

### `content_language`

默认写当前会话语言，例如：

- `zh-CN`
- `en`

如果用户明确要双语，再单独说明；不要把“双语可能有帮助”当成默认。

### `allowed_text_scope`

回答的是：

- 图里允许出现哪些可读文字
- 哪些文字是唯一允许的
- 是否允许额外说明字、伪 UI 文案、小字背景纹理

推荐写法：

- `only project name + one Chinese slogan + one Chinese subtitle`
- `project name only`
- `no readable text`

### `final_layout_owner`

只允许：

- `model`
- `post_process`
- `hybrid`

解释：

- `model`: 本轮要求模型直接交成品
- `post_process`: 模型只负责底图，最终版式不在本轮
- `hybrid`: 主视觉由模型完成，精确元素后置

### `acceptance_bar`

这里回答的是：

- 用户眼里什么叫“现在就能用”

推荐写法：

- `must be a directly usable brand promo poster`
- `must preserve Chinese headline hierarchy and require no additional copy pass`
- `may remain a clean text-safe base for later layout`

## Intake Question Policy

### When To Ask Follow-Up Questions

当下面任一项缺失且会显著改变结果时，应该补问：

- 最终交付物类型不清楚
- 这是成品还是底图不清楚
- 文案语言不清楚
- 允许出现哪些文字不清楚
- 谁负责最后排版不清楚
- 使用位置不清楚
- 用户的通过标准不清楚

### Question Budget

默认最多问 `1-3` 个问题。

优先级顺序：

1. 这是完整成品还是底图
2. 文案语言和允许文字范围
3. 最终放在哪里 / 谁来做最后排版

### When Not To Ask

如果下面这些已经明确，优先直接进入下一阶段：

- 交付物类型明确
- 成品度明确
- 文案语言明确
- 使用场景明确
- 成功标准明确

## Output Template

推荐把一次 intake 先收成下面这个结构。

```yaml
user_raw_request: ""
user_goal: ""
asset_type: ""
deliverable_type: ""
usage_context: ""
requirement_summary: ""
context_summary: ""
background_context: ""
brand_or_product_sources: []
target_audience: ""
success_criteria: []

asset_contract:
  asset_completion_mode: "complete_asset"
  content_language: "zh-CN"
  allowed_text_scope: ""
  final_layout_owner: "model"
  acceptance_bar: ""

fixed_text: []
fixed_elements: []
size_and_delivery_constraints: []
reference_assets: []
source_materials: []
existing_generation_context: ""
must_avoid: []
direct_output_vs_post_process: "direct_output"

open_questions: []
missing_critical_fields: []
intake_confidence: "medium"
recommended_route_hint: "direct"
```

## Intake Completion Checklist

在把 intake 交给下一阶段前，至少确认下面这些问题已经被回答：

1. 这轮到底要交付什么资产
2. 这是完整成品还是中间底图
3. 文案语言是否已锁定
4. 允许出现的文字范围是否已锁定
5. 谁负责最终排版是否已明确
6. 用户可验收的完成定义是否已明确
