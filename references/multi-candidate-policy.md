# Multi-Candidate Policy

## Purpose

这份文档定义 `image2-design-director` 什么时候应从 `single-output` 升级为 `multi-candidate`，以及多候选生成后该如何比较、收敛和留痕。

它回答的不是：

- 每次都要多出几张图

它回答的是：

- 什么情况下值得付出多候选成本
- 候选集应该怎么组织
- 哪些变量可以同时变化，哪些不该一起变化
- 用户任务里的“多候选选择”和 skill 校准里的 “A/B 测试”有什么区别

一句话版本：

> 多候选不是默认豪华模式，而是用有限额外成本换更高方向确定性和更强决策质量的策略工具。

## Position In The Loop

这份 policy 主要服务：

- `Stage 2. Strategy Selection`
  - 决定 `candidate_mode` 是 `single-output` 还是 `multi-candidate`
- `Stage 4. Evaluation And Scoring`
  - 决定多候选如何统一比较
- `Stage 5. Branching: Deliver Or Repair`
  - 决定是选优进入交付，还是抽取 failure mode 进入下一轮
- `Stage A-D. Compounding Loop`
  - 决定哪些对比样本值得进入 benchmark 或经验晋升

## Core Principle

### 1. Use Multiple Candidates Only To Resolve Real Uncertainty

如果当前方向已经很清楚，多候选往往只会：

- 增加生成成本
- 增加评审负担
- 稀释下一轮修正信号

所以多候选必须服务于真实不确定性，而不是服务于“多来几张总没错”。

### 2. Candidate Sets Must Be Comparable

多候选不是素材堆。

一次合格的候选集必须能回答：

- 我们到底在比较什么
- 变量改了哪些
- 哪些条件保持不变
- 最终要按什么标准选

### 3. One Candidate Set Should Test One Decision

同一组候选里，不要同时乱动太多层变量。

优先只比较其中一类：

- 构图方向
- 场景设定
- 信息密度
- 视觉语气
- prompt 框架
- 后处理策略

### 4. Selection Must Lead To Action

多候选之后必须进入明确动作，而不是停在“这几张都还行”。

动作只能是下面几类：

- 选一张进入交付
- 选一张作为 repair 基底
- 合并结论后再出下一组
- 进入 benchmark 记录

## Candidate Modes

这份 policy 只承认两种候选模式：

- `single-output`
- `multi-candidate`

结构化字段里统一使用上面的连字符值。

如果别的文档里出现：

- `single_output`
- `multi_candidate`

应视为同一概念的非规范写法，后续回写时统一收敛到：

- `single-output`
- `multi-candidate`

### `single-output`

适用于：

- 路径已经清楚
- 当前重点是快速推进
- 当前任务处于 repair 微调
- 评估成本应控制

### `multi-candidate`

适用于：

- 当前存在高价值不确定性
- 需要并排比较两个以上可行方向
- 用户明确希望从几个方向里选
- 当前任务属于 benchmark / A-B 校准场景

## Packet Field Alignment

当这份 policy 被写回 strategy 和 task packet 时，建议最少对齐下面这些字段：

| Layer | Field | Expected Value |
|---|---|---|
| strategy | `candidate_mode` | `single-output` / `multi-candidate` |
| strategy | `task_mode` | `fresh_generation` / `benchmark_or_ab` / other compatible mode |
| strategy | `delivery_involvement` | `image-only` / `image-plus-delivery-ops` |
| task packet | `strategy.candidate_mode` | strategy 最终裁决 |
| task packet | `strategy.strategy_reasoning` | 说明为什么值得多候选 |

## When To Escalate To `multi-candidate`

满足以下任一项时，可考虑启用：

### 1. Directional Uncertainty Is High

表现为：

- 构图还不确定
- 主视觉焦点还不确定
- 是做“产品近景”还是“系统感 hero”仍不清楚
- 同一 brief 至少有两条都合理的视觉路径

### 2. Asset Value Is High

高价值资产更值得用多候选换方向把握。

典型场景：

- 项目首页 hero
- 产品首发图
- 招募主视觉
- App Store 首屏卖点卡
- 品牌关键传播图

### 3. User Choice Is Legitimately Part Of The Task

满足以下任一项时，启用多候选通常是合理的：

- 用户明确说“给我两个方向选”
- 用户自己也不确定风格方向
- 用户希望先选方向再深修

### 4. The Skill Is Calibrating A Strategy

当当前目标不只是交付，而是验证下面这些问题时，应考虑 `multi-candidate`：

- 新 prompt 结构是否更稳
- 新 policy 是否降低 AI artifact
- 后处理路径是否比直出更可用
- 某个 pattern 是否可迁移

## When To Stay On `single-output`

满足以下大部分时，不要升级为多候选：

- 当前是 repair 任务，只改 1 到 2 个变量
- 用户要求尽快推进，不需要方向探索
- 只是中低价值常规素材
- 我们已经知道最可能正确的方向
- 多出几张图并不会带来更清楚的决策

## Candidate Set Design

一个合格的 candidate set 至少要包含下面 6 个对象。

### 1. Set Objective

回答：

- 这组候选是为了比较什么

示例：

- 比较“抽象系统 hero”与“项目结构特征 hero”
- 比较“单主体构图”与“多层卡片构图”
- 比较 `direct_output` 与 `visual_base_plus_post`

### 2. Shared Constraints

这组候选共同继承的硬约束。

例如：

- 相同 use case
- 相同 asset type
- 相同 usage context
- 相同 must_avoid
- 相同 post-processing 假设

### 3. Variant Axes

定义每个候选允许变化的主变量。

推荐只选 1 到 2 个主变量：

- `composition_axis`
- `scene_axis`
- `tone_axis`
- `prompt_framework_axis`
- `delivery_strategy_axis`

### 4. Candidate Records

每个候选必须有可回溯记录：

- `candidate_id`
- `candidate_hypothesis`
- `what_changed`
- `what_stayed_fixed`
- `image_prompt`
- `generation_id`
- `image_output_ref`

### 5. Comparison Criteria

至少要提前写清：

- 用哪些 scorecard 维度判优
- 是否有额外任务特定标准
- 是否存在一票否决项

### 6. Decision Rule

比较结束后，必须提前定义：

- 选单一 winner
- 选 baseline + best challenger
- 或宣布当前 candidate set 不足以下结论

## Recommended Candidate Counts

默认不要无限扩张。

### Default

- 常规多候选：`2`
- 高价值方向探索：`2-3`
- benchmark / A-B：`2`

### Avoid By Default

- 一次出 `4+` 个候选

除非：

- 用户明确要求
- 当前是独立 benchmark 任务
- 有清楚的批量比较模板和评审预算

## User-Facing Presentation Rules

即使内部生成了多个候选，面对用户时也要控制认知负担。

### Default Presentation

默认优先展示：

- `2` 个方向清晰的候选

如果内部测了 `3` 个候选，通常也应先筛掉最弱的一张，再把更清楚的两张拿出来沟通。

### Each Presented Candidate Should Have A Label

不要只说：

- “方案 1”
- “方案 2”

更推荐：

- “协议卡 hero 方向”
- “系统面板 hero 方向”

### Each Presented Candidate Should Carry One-Sentence Reasoning

至少说明：

- 这张在试什么
- 为什么它和另一张不一样

## Allowed Variation Patterns

### Pattern 1. Same Brief, Different Composition

适用于：

- 想比较构图或信息层级

保持不变：

- use case
- scene intent
- tone
- delivery strategy

### Pattern 2. Same Composition, Different Tone

适用于：

- 想比较品牌气质、冷暖、克制程度

保持不变：

- 构图主轴
- 使用场景
- 信息密度

### Pattern 3. Same Task, Different Strategy

适用于：

- 比较 `direct_output` 与 `visual_base_plus_post`
- 比较不同 prompt 框架
- 比较 route 或 delivery involvement

这类比较优先进入 benchmark 记录，而不是只做业务交付内的随手对比。

## Disallowed Comparison Patterns

下面这些做法默认不推荐：

### 1. Too Many Axes At Once

不要同时改：

- use case
- 构图
- 场景
- 文案策略
- 后处理策略

否则最后无法知道到底什么起了作用。

### 2. Fake Diversity

如果几张候选本质上只是同一方向的小抖动，就不要称为有效多候选。

### 3. Winner By Taste Only

不能只说：

- “我更喜欢这张”

至少要说明：

- 为什么它更匹配任务
- 为什么另一个方向不值得继续

## Comparison Workflow

### Step 1. Register The Candidate Set

先写清：

- `candidate_set_id`
- `set_objective`
- `shared_constraints`
- `variant_axes`

### Step 2. Generate And Log Each Candidate

每个候选至少记录：

- `candidate_id`
- `candidate_hypothesis`
- `image_prompt`
- `generation_id`
- `image_output_ref`

### Step 3. Score Side By Side

默认按 [scorecard](scorecard.md) 做并排评分。

至少比较：

- `intent_match`
- `product_native_fit`
- `structure_and_composition`
- `asset_credibility`
- `anti_ai_artifact`

如果任务有文本或交付约束，再加看：

- `text_and_layout_fidelity`

### Step 4. Record Winner And Loser Reasons

至少要回答：

- winner 为什么赢
- loser 输在哪
- 是否需要合并两者结论进入下一轮

### Step 5. Convert The Result Into Action

只能进入以下动作之一：

- `deliver_winner`
- `repair_winner`
- `run_next_candidate_set`
- `record_benchmark`
- `fallback_to_single_output`

## Selection Rules

### Pick A Winner Immediately When:

- 有一个候选明显更接近任务目标
- 总分差距清楚
- 虽然都未 `pass`，但已有一个更适合作为 repair 基底

### Run Another Round When:

- 两个方向都只解决了部分问题
- 当前 candidate set 证明了“该测什么”，但还没给出可交付 winner
- winner 仍落在 `fail`

### Fallback To `single-output` When:

- 候选之间没有真正差异
- 当前继续多候选不会带来额外信息
- 已经找到明确更优方向，后续只需精修

## User-Facing Multi-Candidate Vs Internal A/B

### User-Facing Multi-Candidate

目标：

- 帮用户在多个方向里做选择

特点：

- 候选可以是视觉方向差异
- 更重用户偏好与使用场景反馈
- 不要求形成严格 benchmark 结论

### Internal A/B

目标：

- 比较策略优劣，校准 skill 自身方法

特点：

- 必须固定 shared constraints
- 必须写明 tested hypothesis
- 必须进入模板化记录
- 更重可迁移结论，而不只是“这次哪张更好看”

## Runtime And Benchmark Capture

如果一次多候选满足以下任一条件，建议进入 benchmark 或至少补齐 runtime 对比记录：

- 比较的是两种策略，而不是两种单纯风格
- 结果显著改变了后续默认判断
- 某个候选从 `<75` 提升到 `>=75`
- 某个新 pattern 显示出可迁移价值

推荐最少记录：

- `candidate_set_id`
- `set_objective`
- `variant_axes`
- `winner_candidate_id`
- `loser_reasons`
- `score_summary`
- `next_action`

## Strategy Handoff Contract

如果选择 `multi-candidate`，strategy 层建议至少输出：

```yaml
candidate_mode: "multi-candidate"
candidate_set:
  candidate_set_id: ""
  set_objective: ""
  candidate_count: 2
  variant_axes:
    - ""
  shared_constraints:
    - ""
  tested_hypothesis:
    - ""
  comparison_method: "scorecard_side_by_side"
  decision_rule: "pick_winner_or_repair"
```

## Example Judgments

### Example 1. Project Hero With Two Plausible Directions

情况：

- README hero 图
- 可以走“项目结构协议卡”方向
- 也可以走“抽象协作系统板”方向

判断：

- `multi-candidate`

原因：

- 方向不确定且资产价值高

### Example 2. Repair Round On A Nearly Working Hero

情况：

- 已有一版 `conditional_pass`
- 当前只想补项目特异性

判断：

- `single-output`

原因：

- 已经知道该改什么，不需要再开方向探索

### Example 3. Compare Direct Output Vs Post-Processing Strategy

情况：

- 想知道 App Store feature card 是直出更稳，还是底图加后处理更稳

判断：

- `multi-candidate`
- 且建议进入 internal A/B

原因：

- 当前比较的是策略，而不是单纯视觉偏好

## Completion Checklist

- 这次多候选是否在解决真实不确定性
- 这组候选是否只测试了 1 到 2 个主变量
- 每个候选是否有可回溯记录
- 比较标准是否在生成前就已明确
- 结果是否已转成明确动作
- 这次对比是否值得进入 benchmark 或经验晋升
