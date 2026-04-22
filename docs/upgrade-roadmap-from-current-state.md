# Upgrade Roadmap From Current State

> Public historical note: 这份路线图混合了历史缺口与当时的升级判断。公开发布后，它更适合作为维护者参考，而不是外部用户的主入口。

## Purpose

这份文档说明：

- 当前 `image2-design-director` 已经做到哪里
- 与目标 skill 架构相比还缺什么
- 应按什么顺序升级

它不是纯愿景文档，而是从“当前真实状态”出发的升级方案。

## Current State Snapshot

结合当前 `SKILL.md`、runtime 结构与 `2026-04-22` 状态总结，可以把现状收束为下面几条事实。

## Latest Delta After M10

这份路线图最初写于更早阶段，下面这些“最近进展”需要被当成当前优先事实，否则会误以为项目还停在更前面的缺口判断上。

截至 `2026-04-22` 当前最新状态已经额外完成：

1. `Milestone 1-4` 的核心文档层已落地
   - intake schema
   - strategy decision tree
   - task packet
   - post-processing policy
   - multi-candidate policy
   - delivery ops docs
   - promotion governance
   - benchmark loop
2. prompt family 已完成：
   - regression
   - targeted repair
   - default rule promotion
   - default spot-check
3. scene generalization + host portability 已完成
   - 四个方向被重定义为 validated profiles
   - runtime root 已 host-agnostic
4. `m9_generalization_operationalization` 已完成
   - generalized benchmark surface
   - runtime schema v2
   - profile promotion policy
   - repo / installed / runtime sync contract
5. follow-up execution 已完成到真实验证层
   - 已有一条真实 exploratory benchmark 跑通到 `73.0 conditional_pass`
   - repo -> installed copy 已做过一轮受控同步
6. 后续最小 repair 也已完成两轮
   - `destination asset identity gap` 已被压下去
   - `minor text discipline leak` 也已压下去
   - 当前只剩 `slight_ui_board_literalness` 这种 polish 级问题

因此，这份路线图里下面那些“还没有 intake / strategy / delivery / governance”的表述，应理解为历史缺口，而不是当前主阻塞。

### What Already Exists

1. 已有稳定的三路由：
   - `direct`
   - `brief-first`
   - `repair`
2. 已有结果导向 prompt 框架：
   - `asset goal`
   - `desired outcome`
   - `non-negotiables`
   - `context anchors`
3. 已有质量判断层：
   - `quality-bar`
   - `scorecard`
4. 已有 runtime 经验层：
   - capture
   - review queue
   - field note / repo candidate promotion
5. 已开始记录真实图像运行链路：
   - `brief`
   - `image_prompt`
   - `image output path`
   - `evaluation`

### What Is Still Missing

相对于当前目标形态，项目现在的主要缺口已经不再是“有没有 schema / policy / benchmark contract”，而是下面这些更靠后、更偏运营化或产品化的差距：

1. exploratory 覆盖面还偏窄
   - 目前只有一条真实 unmatched-scene benchmark 被跑通
   - 还不足以支撑更强的“全场景适用”承诺
2. profile promotion 规则已经有了，但 promotion 证据还不够厚
   - `exploratory -> standard -> accelerated` 已有 policy
   - 但新场景还没有真实升档样本
3. delivery layer 仍以文档规则为主
   - `delivery-ops / text-overlay / fixed-element-placement` 已有
   - 但还没有真正产品化成稳定执行工具链
4. installed sync 已有 contract 和一次受控执行
   - 但还没有自动化 sync / manifest / drift detection
5. runtime compounding 仍偏轻量
   - capture、review、field note、local skill auto-promotion 都能工作
   - 但 benchmark/backlog 这类 runtime-only 样本还缺更明确的分层与聚合策略
6. 当前单场景的 open issue 已降到 polish 级
   - `slight_ui_board_literalness`
   - 这是视觉完成度问题，不再是架构阻塞

## Gap Map

从目标架构的 5 个模块来看，当前状态可以这样判断。

| Module | Current Maturity | Notes |
|---|---|---|
| 输入层 | strong | intake schema、task packet、strategy tree 已落地 |
| 生成层 | strong | prompt family、default rules、repair loop 已形成稳定主线 |
| 评估层 | strong | scorecard、benchmark loop、exploratory validation 已跑通 |
| 交付层 | medium | delivery docs 已建，但执行层仍偏文档化 |
| 复利层 | medium-strong | runtime schema v2、promotion policy、sync contract 已有，但自动化与跨场景复利还不够厚 |

## Remaining Gaps Vs Prior Plan Expectation

如果把“之前的计划预期”理解为：

- 让 skill 从四档案工具升级成真正的全场景协议层
- 让经验复利从概念变成规则
- 让 repo、installed copy、runtime 三层不再漂移

那么当前已经达到的部分是：

1. 协议层已经基本到位
2. 至少一条 unmatched scene 已证明可以先拿到 `60+`
3. repo / installed / runtime 的边界已经清楚且做过一次真实同步

真正还没达到预期的部分主要剩 4 类：

1. 验证面厚度
   - 预期是“全场景适用”
   - 当前现实是“已有一条真实 exploratory 样本证明入口成立，但样本厚度还不够”
2. 晋升面厚度
   - 预期是新场景能持续从 exploratory 升到 standard / accelerated
   - 当前现实是 policy 有了，但升档案例还没积出来
3. 交付执行力
   - 预期是 delivery layer 不只是文档
   - 当前现实是 delivery 规则已建，但缺更完整的执行工具化
4. 自动化运维
   - 预期是 repo / installed / runtime 的协同更低摩擦
   - 当前现实是已能手工受控同步，但还没自动化

同时，复利层现在的差距也比之前更窄了：

- 不是“有没有 local auto-promotion”
- 而是 local runtime 中哪些样本应停在 field note，哪些应进入 active local skill，是否还需要一层 benchmark-reference 或别的 runtime-only working layer

## Upgrade Principles

从当前版本升级时，应遵循 4 个原则。

### 1. 先补系统缺口，不先补更多 prompt 花样

当前更需要补的是：

- intake
- strategy
- delivery
- compounding governance

而不是再堆更多 sample prompt。

### 2. 先让闭环更完整，再让单点更强

如果输入、评估、交付和经验晋升不成系统，即使 prompt 再强，也只会停在“偶尔命中”。

### 3. 默认路径优先于理想路径

升级时优先考虑：

- 用户第一次来时，默认会经历什么
- 一张图不过线时，默认怎么进入下一轮
- 一次成功 / 失败后，默认留下什么经验

### 4. 经验升级必须受控

不是让更多记录进入长期知识层，而是让更少但更可靠的规律进入长期知识层。

## Roadmap Overview

建议分 4 个里程碑推进。

### Milestone 1. Build The Intake Layer

目标：

- 把“需求确认”从口头理解，升级成稳定结构

需要新增的能力：

1. intake schema
   - `user_goal`
   - `asset_type`
   - `usage_context`
   - `background_context`
   - `brand_or_product_sources`
   - `fixed_text`
   - `fixed_elements`
   - `size_and_delivery_constraints`
   - `direct_output_vs_post_process`
2. intake questions policy
   - 哪些情况直接做
   - 哪些情况必须补 1 到 3 个问题
3. task packet 结构
   - 把用户原话和我们理解后的摘要分开

推荐产物：

- `references/intake-schema.md`
- `references/strategy-decision-tree.md`
- `references/delivery-constraints.md`

为什么先做它：

- 因为 prompt 质量的上限，先被 intake 质量决定

### Milestone 2. Build The Strategy Layer

目标：

- 把“怎么做这次任务”从隐式经验升级成显式决策

需要补的决策维度：

1. `single-output` vs `multi-candidate`
2. `direct-output` vs `visual-base-plus-post`
3. `generate-first` vs `repair-first`
4. `image-only` vs `image-plus-delivery-ops`

这里需要形成明确规则：

- 什么情况下适合直出
- 什么情况下应该留白再后置叠字
- 什么情况下二维码必须后置
- 什么情况下应该先做 hero base 再扩尺寸
- 什么情况下应该同时出 A/B 两组候选

推荐产物：

- `references/strategy-decision-tree.md`
- `references/post-processing-policy.md`
- `references/multi-candidate-policy.md`

### Milestone 3. Build The Delivery Layer

目标：

- 让 skill 能交付“可使用资产”，而不只是“模型产图”

至少需要落地 4 类交付能力：

1. 尺寸策略
   - 何时大图缩小
   - 何时小图放大
   - 不同交付位的尺寸适配
2. 文本后处理
   - 固定文案是否后置
   - 何时只保留留白区
3. 固定元素后处理
   - 二维码
   - logo
   - badge
4. 资产版本化
   - raw visual
   - text-safe visual
   - delivery-ready visual

推荐产物：

- `references/delivery-ops.md`
- `references/text-overlay-policy.md`
- `references/fixed-element-placement.md`

这个里程碑也可能需要新脚本或配套 skill，但文档策略应先明确。

### Milestone 4. Strengthen The Compounding Layer

目标：

- 把“会记”升级成“会判断什么值得长期记”

当前 runtime 已有基础设施，接下来重点不是再加 capture，而是治理升级。

需要补的内容：

1. capture quality gate
   - 哪些记录只保留 raw
   - 哪些记录值得 review
2. promotion governance
   - 什么情况下升 field note
   - 什么情况下升 pattern
   - 什么情况下归档
3. benchmark loop
   - 不同策略对比
   - A/B 样本进入 benchmark
4. knowledge pollution control
   - 避免一次性命中污染长期规则

推荐产物：

- `references/promotion-governance.md`
- `docs/benchmarks/benchmark-scenarios.md`
- `docs/experiments/ab-testing-template.md`

## Recommended Execution Order

建议按下面顺序推进，而不是并行全开。

### Phase 1

- 建 intake schema
- 建 strategy decision tree
- 让“需求确认 -> 任务包”先稳定

### Phase 2

- 扩策略层
- 明确多候选、后处理、直出之间的边界

### Phase 3

- 建交付层文档和最小可用流程
- 先定义，再决定是否上脚本

### Phase 4

- 收紧经验晋升治理
- 把 benchmark 和 A/B testing 接进正式验证体系

## Execution Tracking

为了让这份路线图在执行阶段不是静态说明，而是持续推进的工作面板，项目当前补了一套最小进度回写机制：

- machine source of truth: `state/execution-progress.json`
- auto-written execution board: `docs/execution-plan.md`
- update script: `scripts/update_execution_progress.py`
- usage notes: `docs/execution-progress-protocol.md`

这意味着后续执行时，应该优先更新状态源，再由脚本回写执行文档，而不是手工同时维护多份进度说明。

## Concrete Upgrade Plan

如果要把路线图改写成更直接的执行清单，可以拆成下面 8 个任务。

1. 新增 intake 文档
   - 明确“用户原始需求”和“我们理解后的任务包”必须分开保存
2. 新增 strategy 决策树文档
   - 明确 direct / brief-first / repair 之外的执行策略分叉
3. 新增 delivery policy 文档
   - 把二维码、文案、logo、尺寸适配纳入正式流程
4. 扩展 runtime capture schema
   - 增加 `user_requirement_summary`
   - 增加 `context_summary`
   - 增加 `delivery_strategy`
5. 引入 candidate-set 概念
   - 支持单次任务里多候选图统一评审
6. 引入 A/B benchmark 模板
   - 让策略对比变成结构化试验，而不是临时感受
7. 定义 promotion governance
   - 让经验晋升规则变成显式文档
8. 用 3 到 5 个真实场景跑升级后回归
   - 社媒图
   - 项目宣传图
   - UI mockup
   - icon
   - 带固定文本 / 二维码的图

## Risks And Controls

升级过程中最容易出的问题有 5 类。

### 1. 文档越来越多，但默认路径没变清楚

控制方式：

- 每次新增文档都要回答“默认流程中哪一步会真正使用它”

### 2. 经验记录越来越多，但知识越来越脏

控制方式：

- 强化 promotion governance
- 默认保守晋升

### 3. 后处理能力越补越散

控制方式：

- 先定义 delivery 层边界，再考虑脚本或外部工具

### 4. A/B 测试变成额外负担

控制方式：

- 只在高价值任务或 skill 校准阶段启用

### 5. 用户体验被流程压重

控制方式：

- 用户面前保持轻量
- 重结构主要放在 skill 内部运行层和 runtime 里

## Definition Of Success

可以用下面这些信号判断升级是否成功。

### Short-Term Success

- intake 更稳定，少量问题就能把需求收清楚
- 修图时能更快定位 failure mode
- runtime 记录比现在更完整但不更混乱

### Mid-Term Success

- 同类任务命中率提升
- `conditional_pass` 更容易推进到 `pass`
- 多候选和后处理策略开始稳定产出高质量资产

### Long-Term Success

- 经验升级机制稳定
- pattern 库增长缓慢但质量更高
- skill 在新任务上也能复用判断，而不是只复用旧 prompt

## Current Recommendation

如果从今天开始继续推进，最优先建议不是马上补交付脚本，而是先做下面两件事：

1. 把 intake 层正式文档化
2. 把 strategy 层正式文档化

原因很简单：

- 没有 intake，prompt 上限不稳
- 没有 strategy，交付和经验层都会漂

所以，从当前 skill 升级到目标 skill，第一步应当是：

> 把“需求确认”和“执行策略判断”从已有经验，升级成明确的系统层文档与运行合同。
