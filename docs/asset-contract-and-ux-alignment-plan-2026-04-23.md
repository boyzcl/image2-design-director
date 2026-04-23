# Asset Contract And UX Alignment Plan 2026-04-23

## Purpose

这份方案把本轮交互中暴露出来的更底层问题，收敛成一份可落库的优化计划。

目标不是只补几条 prompt 技巧，而是把 `image2-design-director` 从：

- “会增强图像生成”

推进到：

- “先对齐交付物合同，再做图像生成”

一句话版本：

> 更好的用户体验，不是让 skill 更会出图，而是让它更稳定地先做对的资产，再把资产做漂亮。

## Why This Plan Exists

本轮交互暴露出的错误，不只是一次 prompt 失误，而是 4 类系统级问题：

1. 用户要的是“完整可用品牌宣传图”，系统却默认滑向了 `text-safe base`
2. 用户在中文会话中提出需求，系统却默认生成英文文案
3. repair 没有先回到“原始交付物合同”，而是先做局部修补
4. 系统更早关注的是视觉生成策略，而不是“最终资产类型是否判对”

这些问题如果不改，用户会持续感受到：

- “你很会生图，但没先听懂我要什么”
- “你交的是中间稿，不是成品”
- “你在补 prompt，不是在重新对齐任务”

## Core Diagnosis

当前系统更像一个：

- `image generation optimization system`

但用户真正需要的是一个：

- `asset contract alignment system`

这意味着下一阶段的核心优化方向应该是：

1. 让系统先稳定识别交付物合同
2. 再选择 route、output mode、delivery involvement
3. 再进入 prompt assembly、generation、evaluation

## Target UX

优化后，用户体验应更接近下面这种感受：

1. 系统先理解“我要的到底是什么资产”
2. 系统默认把“完整可用成品”当作正常需求，而不是例外
3. 系统自动跟随当前会话语言，而不是自由切换文案语言
4. 用户否定结果时，系统会先判断“是方向错了还是细节没打磨”，再决定 repair 方式
5. 系统给出的“完成”是用户可验收的完成，而不是模型可辩护的完成

## Design Principles

### 1. Asset Contract Before Prompt

先定义：

- 最终交付物是什么
- 谁来完成最后排版
- 是否必须成品直出
- 语言是什么
- 允许出现哪些可读文字

再进入 prompt 层。

### 2. Finished Asset By Default

用户未明确要求“底图 / 待补字 / 中间稿”时，默认按：

- `complete direct-output asset`

处理，而不是：

- `visual base`
- `hero base`
- `text-safe placeholder`

### 3. Conversation Language Is The Default Content Language

当前会话语言应成为海报、宣传图、品牌图中的默认文案语言。

项目名可保留原文，但：

- slogan
- subtitle
- CTA
- supporting copy

默认跟随当前会话语言。

### 4. Asset Type Beats Style

先判断：

- 这是品牌宣传图、README hero、社媒海报，还是 onboarding illustration

再判断：

- 配色
- 质感
- 镜头
- 风格词

### 5. Misalignment Requires Realignment, Not Patching

如果用户指出“这不是我要的资产类型”或“这不是成品”，下一步应该先重建合同，而不是只补几个 prompt 约束。

### 6. User-Acceptance Completion Beats Model-Acceptance Completion

过线标准必须包含：

- 能不能直接用
- 资产类型是否正确
- 语言是否符合当前任务
- 文案是否完整
- 是否仍然需要额外解释“后续再补”

## Proposed System Changes

### Workstream 1. Add An Explicit Asset Contract Layer

这是本方案最核心的变化。

建议在 intake 与 strategy 之间，新增一层明确的 `asset contract` 判断。它可以先作为 task packet / strategy 的新字段组合存在，不一定要独立成新文档层，但语义上必须显式化。

最小应回答：

1. `deliverable_type`
   - 最终交付物是什么
2. `asset_completion_mode`
   - `complete_asset`
   - `base_visual`
   - `delivery_refinement`
3. `layout_owner`
   - `model`
   - `post_process`
   - `hybrid`
4. `content_language`
   - 当前默认文案语言
5. `allowed_text_scope`
   - 允许出现哪些可读文字
6. `acceptance_bar`
   - 这轮怎样才算用户可验收

### Workstream 2. Reorder Strategy Priority

当前 strategy 应该调整判断顺序。

建议顺序改为：

1. 先确认 `deliverable_type`
2. 先确认 `asset_completion_mode`
3. 先确认 `content_language`
4. 再判断 `task_mode`
5. 再判断 `route`
6. 再判断 `candidate_mode`
7. 最后才判断 `direct_output` / `visual_base_plus_post`

这样可以避免系统还没搞清楚“用户要成品还是底图”，就过早滑到保守的 post-process 路径。

### Workstream 3. Promote Language Following To A System Rule

建议把“语言遵循”从 prompt 层提升为协议层规则。

默认规则：

- 当前会话语言 = 默认文案语言
- 项目名、产品名、repo 名可保留原文
- 用户未要求双语时，不应自动插入英文 slogan 或副标题
- 对中文任务，必须显式抑制额外英文小字、伪 UI 英文和品牌墙英文

### Workstream 4. Split Repair Into Two Classes

当前 repair 机制需要拆成两种：

1. `micro_repair`
   - 细节没过线，但资产类型没错
2. `contract_realign`
   - 资产类型、语言、成品度、品牌语义判错了

如果是第二类，repair 的第一步必须是重建：

- 交付物合同
- 成功标准
- 允许文本
- 语言
- 禁止漂移域

而不是直接进 `Change only`。

### Workstream 5. Add Completion And Acceptance Dimensions To Evaluation

`quality-bar` 和 `scorecard` 需要新增用户视角的验收维度。

建议至少增加：

- `asset_type_fidelity`
- `completion_readiness`
- `language_alignment`
- `contract_alignment`

其中：

- `completion_readiness`
  - 判断这张图是否已经是用户可直接使用的成品
- `contract_alignment`
  - 判断输出是否还在最初定义的交付物合同之内

### Workstream 6. Treat Brand / Promo / Launch Assets As Completion-Sensitive

对于以下任务，应把“完整可用成品”作为默认假设：

- 品牌宣传图
- 品牌海报
- 项目发布海报
- launch poster
- 招募海报
- 项目介绍海报

只有当用户明确说：

- “我后续自己排字”
- “先给我底图”
- “预留文字区”

才切换为底图思路。

## Proposed Doc-Level Changes

### 1. `references/intake-schema.md`

新增或强化字段：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `final_layout_owner`
- `acceptance_bar`

新增判断：

- 用户是否明确要求完整成品
- 是否明确由模型承担最终排版
- 会话语言是否应作为默认文案语言

### 2. `references/task-packet.md`

新增一个正式区块：

- `Asset Contract Block`

建议字段：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`
- `contract_risks`

并把它放在：

- `Requirement Block`
- `Constraint Block`

之间，作为后续 strategy 和 evaluation 的共同继承层。

### 3. `references/strategy-decision-tree.md`

改动重点：

- 把“资产类型 / 成品度 / 语言”前置到 route 判断之前
- 新增 `contract_realign` 触发条件
- 新增 completion-sensitive asset 类型的默认策略

### 4. `references/post-processing-policy.md`

需要补的不是“什么时候后处理”，而是：

- 什么时候**不应该**默认后处理

建议新增强规则：

- 品牌宣传图、项目发布图、招募海报默认不是底图任务
- 成品导向任务不能因为精度风险，就自动滑向“只做 base visual”

### 5. `references/prompt-schema.md`

新增字段组：

- `content_language`
- `allowed_text_scope`
- `completion_mode`
- `asset_contract`

并明确：

- 文字策略不是约束角落项，而是成品任务的主结构项

### 6. `references/quality-bar.md`

新增用户验收维度：

- 资产类型对不对
- 这是不是成品
- 语言跟不跟随任务
- 有没有“好看但没法直接用”

### 7. `references/repair-playbook.md`

新增 repair 分流：

- `micro_repair`
- `contract_realign`

并规定：

- 用户指出“这不是我要的东西”时，优先走 `contract_realign`

### 8. `SKILL.md`

需要把上面这些原则回写成默认行为：

- 对 completion-sensitive 任务默认交付成品
- 默认跟随当前会话语言
- 当用户否定的是“任务理解”，先重建合同再修图

## Proposed Runtime Changes

runtime 不应只记录 prompt 和结果，也应记录这轮的合同判断。

建议 capture schema 增补：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `contract_alignment_result`
- `completion_readiness_result`
- `repair_class`

这样后续才能追踪：

- 哪些失败是 prompt 失败
- 哪些失败其实是合同判断失败

## Proposed Milestone Sequence

### Milestone 1. Contract Vocabulary

先把字段、枚举值和定义写清楚。

目标：

- 所有核心文档使用同一套词

### Milestone 2. Strategy Reorder

把 strategy 决策顺序改掉。

目标：

- 不再过早滑向保守输出

### Milestone 3. Quality And Repair Upgrade

把“用户验收”和“合同重对齐”纳入默认评估与 repair。

目标：

- 用户指出方向错时，系统会真正重新对齐

### Milestone 4. Runtime Tracking

把合同判断写进 runtime。

目标：

- 后续能从真实失败案例里看出系统究竟错在 prompt，还是错在任务理解

## Success Criteria

如果这份方案落实到位，后续应明显看到这些变化：

1. 用户要成品时，系统不再默认输出底图或半成品
2. 中文任务中，文案默认跟随中文，不再无故切英文
3. 用户否定结果时，系统更常先做方向重对齐，而不是局部修补
4. “好看但没法用”的结果被更早判定为不过线
5. 品牌宣传图、项目发布图、招募海报这类任务的首轮命中率提高

## Immediate Next Step

如果要继续执行，这份方案之后最合理的落地顺序是：

1. 先改 `intake-schema`、`task-packet`、`strategy-decision-tree`
2. 再改 `post-processing-policy`、`prompt-schema`
3. 然后改 `quality-bar`、`repair-playbook`
4. 最后回写 `SKILL.md` 和 runtime schema

## Decision

本方案的核心判断是：

> 下一阶段最值得投入的，不是更多 prompt 花样，而是把 `image2-design-director` 升级成一个更稳定的“交付物合同对齐系统”。
