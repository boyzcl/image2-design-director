# Generalized Benchmark Surface

## Purpose

这份文档定义 `m9_generalization_operationalization` 之后的 benchmark 面。

它回答的是：

- 泛化后的 skill 应该怎么验证
- 新场景第一次进入时，合格线是什么
- 已验证档案和非档案场景，应该分别承诺到什么程度

一句话版本：

> benchmark 不再只验证四个旧方向有没有退化，而要验证整个 scene system 是否还能把新场景先稳稳带到可诊断起点。

## Why This Exists

进入 `m8_scene_generalization_and_portability` 之后，repo 已经明确：

- 四个既有方向是已验证档案，不是能力边界
- 不命中档案的新场景也应该进入统一流程
- 新场景首轮目标不是立刻高分，而是先拿到 `60+` 的可诊断起点

如果 benchmark surface 仍只覆盖旧四类，就无法验证这个新承诺是否真实成立。

## Three Validation Lanes

当前 generalized benchmark surface 必须同时覆盖 3 条验证车道。

### Lane 1. Accelerated Regression

用于验证：

- 已验证档案是否仍保持高置信加速
- prompt family、route、delivery 规则修改后，是否伤到成熟方向

默认对应：

- `matched_profile` 命中既有档案
- `support_tier: accelerated`
- 期望结果：`80+`，至少 `conditional_pass`

### Lane 2. Standard Transfer

用于验证：

- 相邻场景能否继承已有规则
- 非档案场景但明显可借用现有 prompt family、text layer 或 delivery 经验时，是否能稳定到工作稿水平

默认对应：

- `matched_profile: custom` 或部分命中
- `support_tier: standard`
- 期望结果：`70+`，至少形成可继续交付或 repair 的稳定工作稿

### Lane 3. Exploratory Entry

用于验证：

- 新场景第一次进入时，统一流程是否真的有底线
- 即使没命中旧档案，系统是否还能留下可诊断、可继续修的首轮样本

默认对应：

- `matched_profile: none` 或非常弱的近似匹配
- `support_tier: exploratory`
- 期望结果：`60+`
- 通过标准不是“已经成熟”，而是：
  - failure class 可描述
  - correction rule 可描述
  - next input 可描述

## Minimum Surface By Change Type

### Prompt / Route / Text Layer Changes

至少跑：

1. `1` 个 `accelerated` 场景
2. `1` 个 `standard` 场景
3. `1` 个 `exploratory` 场景

### Runtime Schema / Promotion Policy Changes

除了上面的 3 个场景，还要额外检查：

1. benchmark run 记录是否带上 scene-profile 字段
2. runtime capture 是否能回写同一组字段
3. review / field note 是否没有把新字段丢掉

### Installed Copy / Sync Contract Changes

至少检查：

1. repo 与 installed copy 的 contract 文档是否同步
2. benchmark 模板和 runtime 命令示例是否以 repo 为准
3. installed copy 中是否仍存在明显旧口径

## Required Scenario Metadata

从这一版开始，benchmark 场景和 benchmark run 至少要显式记录：

- `domain_direction`
- `matched_profile`
- `support_tier`

兼容旧记录时可额外保留：

- `legacy_use_case`

但 `legacy_use_case` 只能作为追溯字段，不能再作为主分类字段。

## Decision Rules By Lane

### For `accelerated`

如果结果掉到 `70s`，即使还能用，也应视为回归警报，而不是简单通过。

### For `standard`

如果结果低于 `70`，但 failure mode 和 next input 非常清楚，可保留为修复入口，不宜直接晋升规则。

### For `exploratory`

如果结果低于 `60`，或没有形成明确 correction rule / next input，应视为“还没建立起点”，不能声称通用流程已覆盖该场景。

## Recommended Exploratory Archetypes

为了避免只用“接近旧四类”的任务冒充泛化验证，建议 exploratory lane 优先选这些类型：

- editorial / report cover
- workflow diagram hero
- knowledge-product poster
- educational visual board
- system protocol explainer visual

这些场景通常：

- 需要设计可用性判断
- 又不天然落进既有四档案
- 最容易暴露 scene profiling、text layer 和 delivery 判断是否真的泛化

## Output Contract

一次合格的 generalized benchmark run，至少要留下：

1. benchmark run 记录
2. scene-profile 判断
3. score 和 lane-level verdict
4. failure class / correction rule / next input
5. runtime capture reference

## Relationship To Other Docs

- 场景集定义：`docs/benchmarks/benchmark-scenarios.md`
- 运行模板：`docs/benchmarks/benchmark-run-template.md`
- runtime 字段契约：`docs/runtime-schema-v2.md`
- profile 晋升规则：`docs/profile-promotion-policy.md`
