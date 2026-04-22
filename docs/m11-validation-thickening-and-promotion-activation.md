# M11 Validation Thickening And Promotion Activation

## Purpose

这份文档定义 `image2-design-director` 下一执行阶段：

> `m11_validation_thickening_and_promotion_activation`

这一阶段的目标不是再补一轮 prompt 小修，而是把已经成立的 generalized system 从“协议成立”推进到“证据变厚、promotion 开始真实发生”。

## Why M11 Exists

截至当前状态，项目已经完成：

- scene generalization
- host portability
- generalized benchmark surface
- runtime schema v2
- profile promotion policy
- repo / installed / runtime sync contract
- 一条真实 exploratory unmatched-scene benchmark
- 两轮针对真实 gap 的 narrow repair

因此，当前主阻塞已经从：

- “协议没长出来”

转成：

- “validation thickness 不够”
- “promotion thickness 不够”
- “delivery toolization 还缺真实优先级排序”
- “sync 还没自动化”

## Stage Goal

M11 的阶段目标有三条：

1. 做厚 generalized validation surface
2. 产出第一批真实 profile promotion judgment
3. 用新增样本反推 delivery toolization 和 sync automation 的真实优先级

## Success Criteria

M11 结束时，至少应满足：

1. 新增真实 benchmark / validation runs：
   - `2-3` 条 `exploratory unmatched scene`
   - `2` 条 `standard transfer`
   - `1-2` 条 `delivery-heavy`
2. 至少形成 `1` 份正式的 profile promotion judgment
   - 明确某方向继续停在 `exploratory`
   - 或升到 `standard`
   - 或出现新的 `accelerated` 候选
3. 至少形成 `1` 份 delivery toolization priority decision
   - 说明哪个工具化方向最该先做
4. 至少形成 `1` 份 sync automation scope judgment
   - 明确 manifest / drift check / one-command sync 的边界

## Non-Goals

M11 默认不优先做这些事：

- 继续 polish `slight-ui-board-literalness`
- 大规模重写 prompt family
- 再次重定义 runtime schema / promotion policy

除非在新增 validation 中出现新的系统级回归，否则这些都不应抢走主优先级。

## Workstreams

M11 拆成 4 个工作流。

### Workstream A. Validation Thickening

目标：

- 用真实样本把 current claim 做厚

最低任务包：

1. exploratory unmatched scenes
   - 至少 `2` 条新的非既有档案场景
2. standard transfer scenes
   - 至少 `2` 条能部分继承已有规则的场景
3. delivery-heavy scenes
   - 至少 `1` 条需要 text-safe / delivery-ready / fixed-element judgment 的场景

输出：

- benchmark runs
- runtime captures
- lane verdicts

### Workstream B. Promotion Activation

目标：

- 让 profile promotion policy 从文档进入真实判断

最低任务包：

1. 对 exploratory runs 做 grouped review
2. 判断是否已有方向满足：
   - `exploratory -> standard`
3. 对既有 validated profiles 检查是否仍稳定：
   - accelerated regression 是否仍成立

输出：

- promotion decision note
- profile-level keep / hold / promote judgment

### Workstream C. Delivery Toolization Prioritization

目标：

- 不凭感觉，而是根据重复痛点决定 delivery layer 先做什么

候选优先级池：

1. `text-safe -> delivery-ready` 版本化
2. fixed-element overlay
3. size adaptation

判断依据：

- 哪类痛点在 M11 新增样本里重复最多
- 哪类痛点最影响真实交付
- 哪类能力最适合先工具化

输出：

- delivery toolization priority doc 或 decision note

### Workstream D. Sync Automation Scoping

目标：

- 把已验证可行的手工 sync 收成自动化边界

至少要回答：

1. sync manifest 是否需要
2. drift detection 最小范围是什么
3. one-command sync 应覆盖哪些路径
4. 哪些内容必须继续排除：
   - `runtime/`
   - `state/`
   - `test-output/`
   - repo-only docs / experiments

输出：

- sync automation scope note

## Task Breakdown

### Task 1. Run Two New Exploratory Benchmarks

目的：

- 把 unmatched-scene evidence 从 `1` 条提升到 `3+` 条量级

建议方向：

- editorial / report cover
- knowledge-product poster
- educational visual board

验收：

- 每条都有 benchmark run
- 每条都写 runtime capture
- 每条都有 lane verdict

### Task 2. Run Two Standard Transfer Benchmarks

目的：

- 验证相邻场景能否稳定借用已有 family / route / delivery 规则

建议方向：

- 与 `social-creative` 相邻但不完全重合
- 与 `app-asset` 或 `ui-mockup` 相邻但不完全重合

验收：

- 至少 `2` 条 run
- 明确是否达到 `70+`
- 明确 transfer 是否成立

### Task 3. Run One Delivery-Heavy Validation

目的：

- 让 delivery layer 的优先级来自真实痛点，而不是猜测

验收：

- 真实记录 text-safe / delivery-ready / fixed-element 判断
- 留下下一步工具化线索

### Task 4. Produce First Promotion Decision Note

目的：

- 真正应用 `profile-promotion-policy.md`

验收：

- 至少 `1` 份 profile judgement
- 明确：keep / hold / promote
- 有 evidence stack 支撑

### Task 5. Produce Delivery Toolization Priority Note

目的：

- 决定 delivery layer 的下一实现顺序

验收：

- 至少排序 `3` 个候选方向
- 给出为什么先做第 `1` 个

### Task 6. Produce Sync Automation Scope Note

目的：

- 把 repo / installed sync 从手工惯例推进到自动化设计入口

验收：

- 明确 manifest / drift check / one-command sync 的最小边界

## Recommended Execution Order

按下面顺序推进：

1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 6

原因：

- 先拿样本
- 再做 promotion judgement
- 最后才定工具化和自动化优先级

## Main Risks

### Risk 1. Validation Surface Looks Bigger But Is Semantically Repetitive

避免方式：

- exploratory scenes 必须真的不命中既有四档案
- standard transfer 必须是“相邻可借用”，不是换个名字重复旧场景

### Risk 2. Promotion Happens Too Early

避免方式：

- promotion 只在 evidence stack 足够时发生
- 不要因为一两张图更好看就升档

### Risk 3. Delivery Toolization Priority Is Chosen By Taste

避免方式：

- 只根据 M11 中重复出现的真实交付痛点排序

## Completion Definition

只有当下面三件事都完成，才应认为 M11 结束：

1. validation surface 明显变厚
2. promotion judgment 已真实发生至少一次
3. delivery toolization / sync automation 的下一步优先级已被真实证据决定

## Relationship To Other Docs

- 阶段差距总览：`docs/stage-progress-review-2026-04-22.md`
- generalized validation：`docs/benchmarks/generalized-benchmark-surface.md`
- profile promotion：`docs/profile-promotion-policy.md`
- sync contract：`docs/repo-installed-runtime-sync-contract.md`
