# Strategy Decision Tree

## Purpose

这份文档定义 `image2-design-director` 的主决策树。

一句话版本：

> strategy 现在不只回答“怎么生成”，而要先回答“信息是否可信、该由什么表达机制承载、结果还能不能安全交付、当前产物是不是对的资产身份，以及它是否真的达到 publication-ready”。

## Core Decision Layers

策略判断分成 12 层，必须按顺序做。

### Layer 0. Scene Profiling

先确认：

- `domain_direction`
- `matched_profile`
- `support_tier`
- 是否命中 `wechat_article_editorial_visual_set` 或 `editorial_publication_visual`

### Layer 1. Asset Contract Lock

再确认：

- `deliverable_type`
- `usage_context`
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

### Layer 4. Publication Production Packet

如果命中文章图、公众号配图、editorial publication visual，必须先形成 `production_packet`：

- `figure_role`
- `asset_goal`
- `representation_mode`
- `layout_owner`
- `text_owner`
- `text_budget`
- `visual_structure`
- `forbidden_drift`
- `candidate_policy`
- `repair_policy`

这一层解决“这张图应该怎么做”，不是解决“做出来以后能不能过”。

### Layer 5. Production Preflight

如果是 publication asset，必须在生成前跑 `production_preflight`。

结果只允许：

- `pass`
- `conditional_pass`
- `fail`

`conditional_pass` 和 `fail` 都不能进入最终生成。必须先修 production packet。

### Layer 6. Task Mode Decision

判断：

- `fresh_generation`
- `repair_iteration`
- `delivery_refinement`
- `benchmark_or_ab`

### Layer 7. Route Decision

在前面 4 层都明确后，再判断：

- `direct`
- `brief-first`
- `repair`
- `contract_realign`

### Layer 8. Execution Mode Decision

继续判断：

- `single-output`
- `multi-candidate`
- `direct_output`
- `visual_base_plus_post`
- `hybrid_render`
- `deterministic_render`

### Layer 9. First Output Evaluation

按 `quality-bar` 和 `scorecard` 先判断：

- 资产类型是否正确
- 信息是否可信
- 表达机制是否匹配
- 当前结果属于什么资产身份
- 结果是否仍可用

### Layer 10. Delivery Viability Gate

如果要继续 overlay、放 fixed elements、加图表或导出版式，再判断：

- `overlay_allowed`
- `overlay_allowed_with_limits`
- `overlay_not_allowed_regenerate`

### Layer 11. Publication Identity Review

如果目标是文章配图、editorial figure、report cover、publication collateral，必须进一步判断：

- `pass`
- `conditional_pass`
- `fail`

这一层只判断资产身份和场景边界，不判断图面工艺。

### Layer 12. Visual Quality And Final Release

目标是用户可见或文章正文资产时，必须继续判断：

- `visual_quality_review_result`
- `final_release_result`

只有 `final_release_result = pass` 时，才能给用户或进入正文。

### Layer 13. Deliver / Repair / Regenerate

最后才决定：

- 直接交付
- `micro_repair`
- `contract_realign`
- 直接重生成

## Decision Order

每次都按这个顺序判断：

1. 当前场景画像是什么
2. 最终交付物是什么
3. 最终会出现在哪里
4. 这是成品还是底图
5. 哪些信息会被当成事实
6. 主线 metric 和日期截点是什么
7. 哪种表达机制最适合承载
8. 这轮是 fresh / repair / delivery / benchmark 哪一类
9. route 是什么
10. 是单图、多候选、混合渲染还是确定性渲染
11. 第一版结果是否通过 accountability 基线
12. 如果还要继续交付，当前版式还有没有 overlay capacity
13. 如果目标是发表资产，它是否真的通过 publication identity review
14. 图面质量是否通过 visual quality review
15. 最终是否通过 final release gate

## Layer 0. Scene Profiling

### Editorial Publication Profiles

如果满足下面任一项，优先命中文章发表型场景：

- 用户说的是公众号文章配图、文章头图、正文机制图、证据图
- 当前结果将进入 article body、editorial cover、publication figure
- 用户需要的是 `editorial collateral` 而不是活动海报或 benchmark board

命中后默认合同：

- `deliverable_type = wechat_article_editorial_visual_set` 或 `editorial_publication_visual`
- `asset_completion_mode = complete_asset`
- `target_artifact_role = publication_asset`
- `publication_review_required = yes`
- `production_preflight_required = yes`
- `visual_quality_review_required = yes`
- `final_release_required = yes`

### Hard Scene Separation Rule

以下类型默认不得自动升格为文章发表资产：

- `benchmark candidate`
- `delivery bundle artifact`
- `overlay demo`
- `exploratory repair output`

它们默认只能是：

- `internal_candidate`
- 或最多 `review_candidate`

除非显式通过 `publication_readiness_review`，否则不能给用户，也不能进入正文。

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
- 文章发表图默认以 `complete_asset` 为目标；中间底图只可作为内部工件

### Editorial Production Defaults

| Figure Role | Default Representation | Layout Owner | Text Owner | Candidate Policy |
|---|---|---|---|---|
| `editorial_cover` | `hybrid_visual_plus_deterministic_overlay` | `hybrid` | `deterministic_overlay` | `multi_candidate` |
| `mechanism_figure` | `deterministic_render` or `hybrid_visual_plus_deterministic_overlay` | `deterministic_renderer` | `deterministic_renderer` | `single` after wireframe |
| `workflow_evidence` | `hybrid_visual_plus_deterministic_overlay` | `hybrid` | `deterministic_overlay` | `multi_candidate` |

文章图不能默认从 Image2 候选直接退化为纯 deterministic poster，除非 production packet 明确说明这是一个 schematic draft 或 deterministic fallback。

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
- 发表资产身份

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
- 使用场景理解错
- 成品度理解错
- 语言理解错
- 信息口径理解错
- 本应 hybrid / deterministic 的任务被误交给模型直出
- 内部工件被误当 publication asset

这类 route 的第一步不是补 prompt，而是重建：

- `deliverable_type`
- `usage_context`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `metric_definition`
- `representation_mode`
- `acceptance_bar`
- `target_artifact_role`

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

### Output Identity Rule

输出模式不等于资产身份。

例如：

- `benchmark_or_ab + multi-candidate`
  - 默认仍是内部工件
- `delivery bundle artifact`
  - 默认仍是内部工件
- `overlay demo`
  - 默认仍是内部工件

只有在 Layer 9 判为 `pass` 后，当前结果才可标记为 `publication_asset`。

## Layer 8. Delivery Viability Gate

只在准备继续 overlay、放 fixed elements 或导出多尺寸时进入。

### Gate Questions

1. 当前结果是否还有结构能力承载新增信息
2. `protected_regions` 是否会被侵入
3. `collision_risk` 是否可接受
4. 这次 overlay 会不会破坏信息层级或误导读者
5. 如果这是文章图，是否已声明完整 editorial `protected_regions`

### Editorial Overlay Rule

文章图一旦进入 overlay，必须声明 `protected_regions`，至少包含：

- `title_region`
- `core_subject_region`
- `focus_information_region`

没有这些区域时：

- 不能 claim 已完成完整碰撞检测
- 不能 claim 已达到 publication-ready

### Output Values

- `overlay_allowed`
- `overlay_allowed_with_limits`
- `overlay_not_allowed_regenerate`

### Hard Rule

如果 gate 给出 `overlay_not_allowed_regenerate`，默认动作是回到生成或 representation 选择，而不是继续往图上塞字。

## Layer 9. Publication Readiness Review

目标是文章发表资产时必须进入这一层。

### Review Questions

1. 当前资产身份是否正确
2. 这张图是否真正支持文章论点，而不是只提供好看氛围
3. 是否仍残留跨场景文案或 fixed elements
4. 是否误复用了 benchmark、event poster、overlay demo、repair artifact
5. 当前 metadata 是否允许把它认定为 `publication_asset`

### Output Values

- `pass`
  - 可作为用户可见资产，可进入正文
- `conditional_pass`
  - 仅可继续内部修订，不可给用户，不可进入正文
- `fail`
  - 必须回到 repair / realign / regenerate

### Hard Rules

- `conditional_pass` 不算通过，不得当作用户可见 publication asset
- 未跑 `publication_readiness_review` 的文章图，默认不能给用户
- 若存在跨场景残留 CTA、二维码、日期、badge、报名语义或错误资产身份，默认至少 `fail`

## Layer 10. Deliver / Repair / Regenerate

### Deliver

只有同时满足下面条件时才可直接交付：

- scorecard 过线
- 没有 hard fail
- 若为发表资产，`publication_readiness_review = pass`
- 当前 `artifact_role = publication_asset`

### Repair / Regenerate

若不满足上面条件：

- 结构没错但细节不过线：`micro_repair`
- 合同或资产身份错：`contract_realign`
- 图本身结构已不适合承载：`regenerate`
