# Profile Promotion Policy

## Purpose

这份文档定义 scene profile 如何从：

- `exploratory`
- `standard`
- `accelerated`

逐步晋升。

它处理的是“一个场景方向的支持等级”，不是单条 capture 的层级晋升。

一句话版本：

> capture / field note 解决样本沉淀，profile promotion 解决“这类任务现在应被系统承诺到什么程度”。

## Why This Exists

如果没有这层规则，就会出现两种常见漂移：

1. 一次漂亮命中就被误说成“这个方向已经成熟”
2. 新场景明明已经反复出现，却始终停在口头经验，无法进入正式默认

## Promotion Unit

晋升单位不是某张图，也不是某条 prompt，而是：

- 一个相对稳定的 `domain_direction`
- 或一个已经形成边界的 `matched_profile`

判断时看的是：

- 重复样本
- benchmark 结果
- failure / repair 稳定性
- 是否能复用到下一次

## Tier Definitions

### `exploratory`

含义：

- 新场景第一次进入
- 还没有稳定默认打法
- 当前目标是先拿到 `60+` 的可诊断起点

默认承诺：

- 会留下清楚的 failure class
- 会留下 correction rule
- 会留下 next input

不承诺：

- 高分默认
- 单次直达成熟资产

### `standard`

含义：

- 这类任务已经不再是纯陌生场景
- 已经形成可继承的 prompt family、route 或 delivery 经验
- 当前目标是稳定拿到 `70+` 的工作稿

默认承诺：

- 能较稳定进入可交付或可修复状态
- 同类任务不必每次从零试错

### `accelerated`

含义：

- 已形成高置信加速档案
- 默认可以把同类任务更快带到成熟质量线

默认承诺：

- 已有真实 benchmark / runtime 证据
- 有明确 failure-before / intervention / transfer-rule
- 目标通常是 `80+`

## Promotion Gates

### Gate A. `exploratory -> standard`

必须同时满足：

1. 至少 `2` 条相关真实样本
2. 至少 `1` 条样本达到 `60+` 且 failure / correction / next input 明确
3. 已形成可复述的 route 或 prompt-family 借用方式
4. 不再完全依赖临场 improvisation

推荐再满足其一：

- 有一条 benchmark run 支撑
- 有一次 repair 后明显提升

### Gate B. `standard -> accelerated`

必须同时满足：

1. 至少 `3` 条相关样本，其中至少 `2` 条达到 `80+` 或稳定 `conditional_pass / pass`
2. 有跨样本稳定的 failure-before / intervention / transfer-rule
3. 已能解释适用边界和不适用边界
4. 已在 benchmark surface 中至少出现一次正式验证
5. repo 层已有明确默认规则或 profile 文档，不再只停在本地 runtime

## Hold And Demotion Rules

### Stay In `exploratory` when:

- 只有一次样本
- 方向还说不清
- 结果不到 `60`
- 没形成 correction rule

### Stay In `standard` when:

- 虽然已可复用，但还没有高分稳定性
- 明显依赖单一项目上下文
- benchmark 只在单一例子中成立

### Reconsider `accelerated` when:

- 新 benchmark 连续掉到 `70s`
- profile 边界被证明过宽
- 规则只在旧一类素材下成立

必要时可以：

- 从 `accelerated` 回落到 `standard`
- 保留档案，但缩小适用边界

## Evidence Stack

profile 晋升建议按下面的证据堆栈判断：

1. raw captures
2. reviewed captures / field notes
3. benchmark run
4. repo rule update
5. installed copy sync

如果只完成前 1 到 2 层，就不应过早宣称 `accelerated`。

## Relationship To Sample Promotion

样本晋升与 profile 晋升是两条相邻但不同的链路：

- 样本晋升：`capture -> review -> field_note -> repo_candidate`
- profile 晋升：`exploratory -> standard -> accelerated`

两者关系是：

- 没有样本晋升，profile 晋升缺证据
- 只有样本晋升，没有 profile 晋升，经验很难变成系统默认

## Operational Rule

当某类方向达到 `standard` 或 `accelerated` 时，至少要同步三处：

1. benchmark surface
2. runtime schema / field note 口径
3. repo 规则或 skill 文档

否则它仍只是局部记忆，不是系统承诺。
