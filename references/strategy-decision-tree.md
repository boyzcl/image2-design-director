# Strategy Decision Tree

## Purpose

这份文档定义 `image2-design-director` 的主决策树。

一句话版本：

> strategy 现在不只回答“怎么生成”，而要先回答“信息是否可信、该由什么表达机制承载、结果还能不能安全交付，以及最后失败该由谁负责”。

## Core Decision Layers

策略判断分成 9 层，必须按顺序做。

### Layer 0. Scene Profiling

先确认：

- `domain_direction`
- `matched_profile`
- `support_tier`

### Layer 1. Asset Contract Lock

再确认：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

### Layer 2. Information Reliability Gate

判断：

- 这轮是不是事实敏感任务
- 哪些 claim 需要证据
- 主线 metric 的定义和日期截点是什么
- 证据不够时该怎样降级表达

### Layer 3. Representation Strategy Selection

判断：

- 应该走模型直出、模型有限文字、底图加后置、混合渲染，还是确定性渲染

### Layer 4. Task Mode Decision

判断：

- `fresh_generation`
- `repair_iteration`
- `delivery_refinement`
- `benchmark_or_ab`

### Layer 5. Route Decision

在前面 4 层都明确后，再判断：

- `direct`
- `brief-first`
- `repair`
- `contract_realign`

### Layer 6. Execution Mode Decision

继续判断：

- `single-output`
- `multi-candidate`
- `direct_output`
- `visual_base_plus_post`
- `hybrid_render`
- `deterministic_render`

### Layer 7. First Output Evaluation

按 `quality-bar` 和 `scorecard` 先判断：

- 资产类型是否正确
- 信息是否可信
- 表达机制是否匹配
- 结果是否仍可用

### Layer 8. Delivery Viability Gate

如果要继续 overlay、放 fixed elements、加图表或导出版式，再判断：

- `overlay_allowed`
- `overlay_allowed_with_limits`
- `overlay_not_allowed_regenerate`

### Layer 9. Deliver / Repair / Regenerate

最后才决定：

- 直接交付
- `micro_repair`
- `contract_realign`
- 直接重生成

## Decision Order

每次都按这个顺序判断：

1. 当前场景画像是什么
2. 最终交付物是什么
3. 这是成品还是底图
4. 哪些信息会被当成事实
5. 主线 metric 和日期截点是什么
6. 哪种表达机制最适合承载
7. 这轮是 fresh / repair / delivery / benchmark 哪一类
8. route 是什么
9. 是单图、多候选、混合渲染还是确定性渲染
10. 第一版结果是否通过 accountability 基线
11. 如果还要继续交付，当前版式还有没有 overlay capacity

## Layer 2. Information Reliability Gate

满足下面任一项时，进入这一 gate：

- 图中会出现价格、日期、排行、对比结论、性能结论
- 用户使用“最新”“最强”“增长”“领先”“对比”这类会被当成 factual claim 的描述
- 图像将被用作信息图、数据图、带结论的宣传图

### Gate Questions

必须回答：

1. `factual_sensitivity` 是多少
2. `claim_type` 是什么
3. `metric_definition` 是否明确
4. `as_of_date` 是否需要锁定
5. `evidence_requirement` 是否已满足
6. 证据不足时执行哪种 `uncertainty_policy`

### Gate Outputs

只使用下面 4 个结果：

- `verified_fact`
- `fact_with_disclaimer`
- `visual_analogy_only`
- `blocked_needs_brief`

### Hard Rules

- 不要用关键词代替逻辑判断
- 高事实敏感任务在 evidence 不足时，不能直接进入常规 prompt assembly
- 如果结果只能做视觉隐喻，就必须从 prompt 和文案中移除精确 claim

## Layer 3. Representation Strategy Selection

这一层回答的不是“要不要后置”，而是“什么系统最适合承载信息”。

### Preferred Modes

| Mode | Use When |
|---|---|
| `model_direct_visual` | 纯视觉、品牌型、低事实负载、结果要像完整设计资产 |
| `model_visual_with_limited_text` | 可由模型承担有限标题或短文案，但不承担精确数据 |
| `visual_base_plus_post` | 主视觉靠模型，关键文本 / logo / QR / 导出靠后置 |
| `hybrid_visual_plus_deterministic_overlay` | 视觉氛围靠模型，精确数据或图表靠确定性叠加 |
| `deterministic_render` | 图表、价格板、对比板本身是主资产 |

### Default Heuristics

- 精确数字、图表、时间口径重的任务，优先 `hybrid` 或 `deterministic`
- 完整品牌海报、社媒宣传图且事实负载低时，优先 `model_direct_visual`
- 需要 QR、logo、多尺寸复用时，优先把这些元素放入 post 或 hybrid 路径

## Layer 4. Task Mode Decision

### `repair_iteration`

满足以下任一项时优先判为：

- 用户明确说上一版不对
- 已有生成结果待纠偏
- `existing_generation_context` 非空

### `delivery_refinement`

满足以下大部分时可判为：

- 主视觉方向已过线
- 当前主要工作是叠字、放 fixed elements、出多个尺寸

### `benchmark_or_ab`

满足以下任一项时可判为：

- 当前目标是比较两种以上策略
- 用户明确要看方向选择

### `fresh_generation`

不属于上面三类时默认是它。

## Layer 5. Route Decision

### `direct`

当下面大部分都成立时选择：

- 资产合同清楚
- reliability gate 已给出可执行结果
- representation mode 已明确
- 使用场景和成功标准明确

### `brief-first`

当缺少 1 到 3 个高杠杆字段，且这些字段会显著改变：

- 资产合同
- 信息可靠性判断
- 表达机制
- 交付 viability

### `repair`

当合同和主线判断大体没错，只需纠正：

- 工艺
- 层级
- 轻量文字纪律
- 局部 overlay 策略

默认归为：

- `micro_repair`

### `contract_realign`

当下面任一项成立时优先选择：

- 资产类型理解错
- 成品度理解错
- 语言理解错
- 信息口径理解错
- 本应 hybrid / deterministic 的任务被误交给模型直出

这类 route 的第一步不是补 prompt，而是重建：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `metric_definition`
- `representation_mode`
- `acceptance_bar`

## Layer 6. Execution Mode Decision

### Candidate Mode

- `single-output`
  - 默认用于已锁合同的交付任务
- `multi-candidate`
  - 默认用于 benchmark、A/B 或方向性探索

### Output Mode

- `direct_output`
  - 结果就是主要交付物
- `visual_base_plus_post`
  - 需要显式预留交付区
- `hybrid_render`
  - 图像与确定性层一起构成成品
- `deterministic_render`
  - 程序化结果本身是主要交付物

## Layer 8. Delivery Viability Gate

只在准备继续 overlay、放 fixed elements 或导出多尺寸时进入。

### Gate Questions

1. 当前结果是否还有结构能力承载新增信息
2. `protected_regions` 是否会被侵入
3. `collision_risk` 是否可接受
4. 这次 overlay 会不会破坏信息层级或误导读者

### Output Values

- `overlay_allowed`
- `overlay_allowed_with_limits`
- `overlay_not_allowed_regenerate`

### Hard Rule

如果 gate 给出 `overlay_not_allowed_regenerate`，默认动作是回到生成或 representation 选择，而不是继续往图上塞字。
