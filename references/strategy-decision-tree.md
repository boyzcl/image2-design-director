# Strategy Decision Tree

## Purpose

这份文档定义 `image2-design-director` 在 `Stage 2. Strategy Selection` 的显式决策树。

它回答的问题不是：

- prompt 具体怎么写

而是：

- 这次任务到底该怎么跑
- 先走哪条主路径
- 是单图还是多候选
- 是直出还是后处理协同
- 是第一次生成还是 repair 迭代

一句话版本：

> intake 决定“我们知道了什么”，strategy 决定“这轮该怎么做”。

## Position In The Loop

这个决策树接收：

- `references/intake-schema.md` 的结构化输出

它向后输出：

- scene profiling
- route decision
- execution mode
- candidate strategy
- delivery strategy hint
- prompt assembly brief

## Core Decision Layers

策略判断分成 5 层，必须按顺序做。

### Layer 0. Confirm Scene Profiling

先确认这轮任务的场景画像，而不是强塞进四选一：

- `domain_direction`
- `matched_profile`
- `support_tier`

asset type 可以更细，但场景画像必须先明确。

### Layer 1. Identify Task Mode

先判断这轮任务属于哪一类模式：

1. `fresh_generation`
   - 第一次做这轮图
2. `repair_iteration`
   - 已有上一版结果，这轮主要是修正
3. `delivery_refinement`
   - 主视觉基本已过线，本轮重点是交付适配、文本、二维码、尺寸等
4. `benchmark_or_ab`
   - 当前重点是比较不同策略，而不是尽快交付单一结果

### Layer 2. Choose Route

在 `fresh_generation` 或 `repair_iteration` 下，再判断 route：

- `direct`
- `brief-first`
- `repair`

### Layer 3. Choose Execution Mode

route 决定的是“交流和推进方式”，不是完整执行策略。

还要继续判断：

- `single-output`
- `multi-candidate`
- `direct-output`
- `visual-base-plus-post`

### Layer 4. Choose Delivery Involvement

最后判断这一轮是否只做到图像生成，还是同时考虑交付层：

- `image-only`
- `image-plus-delivery-ops`

## Decision Order

每次都按这个顺序判断。

1. 当前场景画像是什么
2. 这轮是首次生成、repair，还是交付细化
3. 是否需要补问才能继续
4. route 是什么
5. 是单图还是多候选
6. 是直出还是底图 + 后处理
7. 是否要把 delivery ops 一起纳入本轮

不要跳过前面的判断，直接根据直觉决定候选数或后处理方式。

## Layer 0: Scene Profiling

这一层要同时产出三件事：

- `domain_direction`
  - 当前任务实际服务的内容方向、资产方向或交付方向
- `matched_profile`
  - 是否命中已验证档案
- `support_tier`
  - `accelerated`
  - `standard`
  - `exploratory`

### Current Accelerated Profiles

当前已验证档案有：

- `product-mockup`
- `social-creative`
- `ui-mockup`
- `app-asset`

它们是高置信加速档案，不是能力边界。

### Match `product-mockup` when:

- 主体是商品或产品本体
- 重点是商业摄影感、材质、镜头和商品可信度

### Match `social-creative` when:

- 重点是传播、首发、招募、项目介绍或活动发布
- 重点不是 UI 可信度，而是 campaign / hero 资产感

### Match `ui-mockup` when:

- 重点是界面可信度
- 重点是信息架构、组件和页面结构

### Match `app-asset` when:

- 重点是服务已有 app 或产品系统
- 图像要嵌入 onboarding、说明图、产品配图或系统资产体系

### Choose `support_tier`

#### `accelerated`

当下面大部分成立时：

- 明确命中已验证档案
- 已有可复用 prompt family、failure rule 或 delivery 经验
- 这类任务在 repo 或 runtime 里已有真实验证样本

#### `standard`

当下面大部分成立时：

- 没有完全命中强档案
- 但能继承相近任务的 prompt family、text layer 或 delivery 规则
- 当前目标是稳定拿到 `70-80` 之间的可用工作稿

#### `exploratory`

当下面大部分成立时：

- 新场景第一次进入
- 只知道资产用途和部分约束，还没有成熟档案
- 当前目标不是直接拿到高承诺默认，而是先拿到 `60+` 的可诊断起点

### Escalate If Profiling Is Ambiguous

当 `matched_profile` 或 `support_tier` 仍然摇摆时，优先：

- 转 `brief-first`
- 或补一个“最终用在哪里 / 它更像哪类资产”的问题

## Layer 1: Task Mode Decision

### A. `repair_iteration`

满足以下任一项时，优先判为 `repair_iteration`：

- 用户明确说“上一版不对”
- 用户给出已有生成结果并要求调整
- intake 中 `existing_generation_context` 非空
- 任务目标不是探索方向，而是修正具体问题

输出要求：

- route 默认优先 `repair`
- 必须保留 `change_only` 思路
- 必须明确本轮不改什么

### B. `delivery_refinement`

满足以下大部分时，可判为 `delivery_refinement`：

- 主视觉方向已经基本过线
- 当前需求主要是叠字、二维码、logo、尺寸适配、版本导出
- 用户更关心“怎么用”，而不是“图像核心方向是否正确”

输出要求：

- route 可不再是主判断中心
- 重点转向 `direct-output` vs `visual-base-plus-post`
- delivery ops 需显式开启

### C. `benchmark_or_ab`

满足以下任一项时，可判为 `benchmark_or_ab`：

- 当前目标是比较两种以上策略
- 用户明确想看多个候选再选
- 当前是 skill 校准阶段而不是业务交付阶段

输出要求：

- 默认启用 `multi-candidate`
- 结果必须进入可比较评估

### D. `fresh_generation`

如果不属于上面三类，默认视为 `fresh_generation`。

## Layer 2: Route Decision

### Route 1. `direct`

当下面大部分都成立时，选择 `direct`：

- `usage_context` 明确
- `asset_type` 明确
- `requirement_summary` 清楚
- `context_summary` 已足够支撑判断
- 没有高风险固定文本或固定元素要求
- `missing_critical_fields` 为空或接近为空
- `intake_confidence` 为 `high`

典型场景：

- 项目 hero 图，目标清楚，允许后续叠标题
- 电商产品图，主体、风格和渠道都明确

### Route 2. `brief-first`

当缺少少量关键字段，且这些字段会显著改变结果时，选择 `brief-first`。

高频触发条件：

- 用途不清楚
- 资产类型不清楚
- 成功标准不清楚
- 固定文本 / 固定元素要求不清楚
- 是否允许后处理不清楚
- 任务绑定具体产品，但上下文来源不清楚

问题预算：

- 默认 `1-3` 个问题

### Route 3. `repair`

在 `repair_iteration` 场景下，默认优先 `repair`。

只有当已有结果几乎不可复用，且用户明确要求重新探索方向时，才退回 `direct` 或 `brief-first`。

repair 的最低要求：

- 明确上一版 failure mode
- 明确本轮只改 1 到 2 个变量
- 明确 keep unchanged 部分

## Route Override Rules

`intake` 中的 `recommended_route_hint` 只是输入信号，不是最终裁决。

当它和当前策略判断冲突时，按下面优先级覆盖：

1. 如果 `existing_generation_context` 明确，优先 `repair`
2. 如果 `missing_critical_fields` 明确存在，优先 `brief-first`
3. 如果上下文已清楚且低风险，优先 `direct`

也就是说：

- 不要因为 intake hint 写了 `direct`，就忽略明显的 repair 场景
- 也不要因为用户催得急，就跳过应有的 `brief-first`

## Layer 3: Execution Mode Decision

### A. `single-output` vs `multi-candidate`

具体判定细则见：

- `references/multi-candidate-policy.md`

#### Prefer `single-output` when:

- 用户要尽快推进
- 当前方向已比较清楚
- 本轮重点是精修或验证单一路径
- 生成成本和评估成本应控制

#### Prefer `multi-candidate` when:

- 当前构图或视觉方向不确定
- 用户明确希望从多个候选里选
- 当前任务本身是高价值首图 / 项目主视觉 / 品牌关键物料
- 当前处于 benchmark / A-B 校准阶段
- 用户提供了可行参考图，且当前争议点正是“应不应该允许直出”

默认建议：

- 普通业务任务默认 `single-output`
- 高价值关键视觉或策略对比任务可升为 `multi-candidate`

### B. `direct-output` vs `visual-base-plus-post`

具体判定细则见：

- `references/post-processing-policy.md`

#### Prefer `direct-output` when:

- 不存在高精度文本需求
- 不存在固定二维码 / logo / badge 必须正确落位
- 用户要的是偏纯视觉资产
- 当前任务本身适合完整画面一次生成

#### Prefer `visual-base-plus-post` when:

- 有固定文本需要准确出现
- 有二维码、logo、badge 等固定元素
- 需要中文标题安全区
- 需要多尺寸扩展
- 需要让图像先承担主视觉，再后续完成交付版式

默认建议：

- icon、海报、招募图、上架图、项目 hero 图，通常更适合先生成 `visual_base_plus_post`
- 纯插图、纯配图、无固定元素的素材，更容易走 `direct-output`

## Layer 4: Delivery Involvement Decision

### `image-only`

适合：

- 当前只需验证视觉方向
- 文本、二维码、尺寸不在本轮范围
- 本轮只是中间稿或探索稿

### `image-plus-delivery-ops`

适合：

- 用户要求接近最终可用资产
- 本轮必须考虑尺寸、文案、二维码、logo 或导出版本
- 已进入 `delivery_refinement`

## Decision Table

| Situation | Mode | Route | Candidate Mode | Output Mode | Delivery Involvement |
|---|---|---|---|---|---|
| 明确且低风险的首次生成 | `fresh_generation` | `direct` | `single-output` | 按任务判断 | `image-only` |
| 缺少少量关键字段 | `fresh_generation` | `brief-first` | `single-output` | 待补问后判断 | `image-only` |
| 已有结果但跑偏 | `repair_iteration` | `repair` | `single-output` | 沿原路径微调 | `image-only` |
| 高价值主视觉方向不确定 | `fresh_generation` | `direct` 或 `brief-first` | `multi-candidate` | 常偏 `visual-base-plus-post` | `image-only` |
| 主视觉已稳，开始交付适配 | `delivery_refinement` | 不以 route 为中心 | `single-output` | `visual-base-plus-post` | `image-plus-delivery-ops` |
| 需要比较策略优劣 | `benchmark_or_ab` | 按具体样本判断 | `multi-candidate` | 视实验目标而定 | `image-only` 或 `image-plus-delivery-ops` |

## Default Strategy Contracts

### Contract 1. Fresh And Clear

如果 intake 完整、风险低、没有高精度固定元素要求：

- route: `direct`
- candidate mode: `single-output`
- output mode: `direct-output`
- delivery involvement: `image-only`

### Contract 2. Fresh But Needs Clarification

如果只差少量高杠杆信息：

- route: `brief-first`
- candidate mode: `single-output`
- output mode: 暂不定
- delivery involvement: `image-only`

### Contract 3. Existing Result Needs Correction

如果已有上一版，且本轮目标是修正：

- mode: `repair_iteration`
- route: `repair`
- candidate mode: `single-output`
- output mode: 延续上一版主路径
- delivery involvement: `image-only`

### Contract 4. Hero Or Launch Asset With Real Delivery Needs

如果是高价值主视觉、且后续有文案 / 二维码 / 版式落位要求：

- route: `direct` 或 `brief-first`
- candidate mode: `single-output` 或 `multi-candidate`
- output mode: `visual-base-plus-post`
- delivery involvement: `image-plus-delivery-ops`

### Contract 5. High-Opinion Social Poster With Text Feasibility In Question

如果是高观点、高传播性的海报任务，且争议点正是“模型能否直接承担文本与整体海报感”：

- mode: `benchmark_or_ab` 或 `fresh_generation`
- route: `direct`
- candidate mode: `multi-candidate`
- output mode: 先比较 `direct-output` 与 `visual-base-plus-post`
- delivery involvement: 首轮可先 `image-only`

目的不是立刻保守交付，而是先验证哪条路径更对。

## Hand-Off Output

策略层结束时，建议输出下面这些字段，交给 prompt assembly 或后续阶段：

```yaml
domain_direction: "project hero for an AI workflow skill"
matched_profile: "social-creative"
support_tier: "accelerated"
task_mode: "fresh_generation"
route: "direct"
candidate_mode: "single-output"
output_mode: "visual-base-plus-post"
delivery_involvement: "image-only"
strategy_reasoning:
  - ""
question_budget: 0
repair_scope: ""
keep_unchanged: []
route_override_reason: ""
strategy_conflicts: []
```

## Example

```yaml
domain_direction: "project hero for an AI workflow skill"
matched_profile: "social-creative"
support_tier: "accelerated"
task_mode: "fresh_generation"
route: "direct"
candidate_mode: "single-output"
output_mode: "visual-base-plus-post"
delivery_involvement: "image-only"
strategy_reasoning:
  - "用途、资产类型和上下文都已经足够明确。"
  - "这是项目 hero 图，后续需要叠加中文标题，因此更适合先做视觉底图。"
question_budget: 0
repair_scope: ""
keep_unchanged: []
route_override_reason: ""
strategy_conflicts: []
```

## Strategy Completion Checklist

在把策略结果交给下一阶段前，至少确认下面这些点已经收住。

### Must Be Clear

- `domain_direction` 是什么
- 是否命中 `matched_profile`
- 当前 `support_tier` 是什么
- 当前是 fresh、repair、delivery refinement 还是 benchmark
- route 是什么
- 当前是单图还是多候选
- 当前是直出还是底图 + 后处理
- 是否需要把 delivery ops 纳入本轮

### Must Be Explicit If Present

- 是否覆盖了 intake 的 route hint
- 是否存在策略冲突
- 是否处于 benchmark / A-B 场景
- repair scope 和 keep unchanged 是否明确

### Not Ready If

- 场景画像还没定
- route 只是“感觉像 direct”
- output mode 没定，但已经开始写 prompt
- 明明有固定元素交付要求，却没判断是否后处理

## Escalation Rules

遇到下面情况时，不应硬做单一路径决策，而应升级判断：

- intake 关键字段缺失过多
- 用户要求互相冲突
- 用户要求既要一次直出，又要高精度文字和固定元素
- 用户已有上一版，但不满意点描述过于模糊
- 任务风险高，但用户给的上下文又明显不足

这时应优先：

- 转 `brief-first`
- 或拆成“主视觉生成 + 后处理交付”两步

## What This Document Does Not Do

这份文档不负责：

- 定义 intake 字段本身
- 写最终 prompt
- 写 repair playbook 的 failure rules
- 做评分
- 直接执行后处理

这些内容分别属于：

- `references/intake-schema.md`
- `references/prompt-schema.md`
- `references/repair-playbook.md`
- `references/scorecard.md`
- 后续 delivery 文档
