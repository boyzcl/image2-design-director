# Promotion Governance

## Purpose

这份文档定义 `image2-design-director` 的经验晋升治理规则。

它回答的是：

- 什么记录只应该停留在 raw capture
- 什么记录应该进入 review
- 什么样的经验值得升为 field note
- 什么情况下才值得成为 repo candidate 或 pattern
- 什么内容应该归档，而不是继续污染判断层

一句话版本：

> 经验默认保守晋升，宁可少升，也不要让一次性命中和偶然好图污染长期规则。

## Position In The Loop

这份文档主要服务 `Layer 2: Compounding Loop`，尤其是：

- `Stage B. Preserve As Local Experience`
- `Stage C. Promote Experience To Knowledge`
- `Stage D. Controlled Knowledge Upgrade`

## Core Principle

### 1. Capture First, Promote Later

每次真实运行都可以记录，但不是每次都值得晋升。

默认活跃顺序：

1. `capture`
2. `review`
3. `field note`
4. `local skill reference`
5. `repo candidate`
6. `pattern`

`archive` 不是线性最后一站，而是可以从任何活跃层进入的归档侧路。

### 2. Promotion Needs Evidence, Not Excitement

一张图“这次很好看”不构成晋升理由。

晋升要看：

- failure mode 是否明确
- intervention 是否明确
- 结果是否稳定改善
- 结论是否可迁移

### 3. Local Learning And Repo Knowledge Must Stay Separate

本地 field note 可以更贴近具体项目、具体品牌、具体上下文。

repo candidate 和 pattern 则必须更克制：

- 更抽象
- 更可迁移
- 更少依赖偶然上下文

### 4. Archive Is A Healthy Outcome

归档不是失败，而是治理动作。

如果一条经验：

- 不可迁移
- 已过时
- 重复度太高
- 只对一次任务有用

那它更适合归档，而不是继续占据注意力。

## Canonical Promotion States

### 1. `capture`

定义：

- 每次生图后留下的原始运行记录

默认规则：

- 每次都写
- 默认不要求已经得出规律

### 2. `review`

定义：

- 值得被再次阅读和判断的 capture

适合进入 review 的信号：

- 发现了明确 failure mode
- 修图带来了显著改善
- 评分跨过关键阈值
- 出现新的可疑规律，值得核验

### 3. `field_note`

定义：

- 本地可复用经验

适合晋升为 field note 的信号：

- 触发场景清楚
- 干预动作清楚
- 对当前 skill 使用者有直接帮助
- 虽然不一定能升 repo，但值得本地复用

### 3.5 `local_skill_reference`

定义：

- 从 field note 压缩出来、默认会进入 skill 读取链路的本地工作集

它不是更高抽象的 repo 资产，而是：

- 更轻
- 更默认
- 更受容量治理约束

适合进入 local skill reference 的信号：

- 已经满足 field note gate
- 能用简短 trigger / carry-forward / avoid / next-move 表达
- 真的值得占用默认上下文预算

### 4. `repo_candidate`

定义：

- 值得考虑回流仓库规则层的候选

适合晋升的信号：

- 不依赖单一项目上下文
- 对多个任务可能有帮助
- 结论已经不只是“这次有效”

### 5. `pattern`

定义：

- 已从多个样本中提炼出的稳定打法

pattern 必须回答：

- 什么时候触发
- 原来常见失败是什么
- 核心 intervention 是什么
- 为什么它可迁移

### 6. `archive`

定义：

- 保留历史，但不再活跃参与判断

适合归档的信号：

- 一次性任务经验
- 上下文已失效
- 与更高质量记录重复
- 证据不足但仍想留底

## State Topology

推荐把晋升路径理解为：

`capture -> review -> field_note -> local_skill_reference -> repo_candidate -> pattern`

同时：

- `capture` 可直接去 `archive`
- `review` 可直接去 `archive`
- `field_note` 可直接去 `archive`
- `local_skill_reference` 可直接去 `archive` 或 `disabled`
- `repo_candidate` 也可回退或归档

也就是说，archive 是治理出口，不是“升到最高级以后才去”的终点。

## Promotion Gates

### Gate 1. From `capture` To `review`

默认不需要太高门槛。

满足以下任一项即可进入 review：

- 结果达到 `conditional_pass` 或 `pass`
- 明确识别出 failure class
- 产生了下一轮非常清楚的 correction rule
- 当前样本在某类场景中具有代表性

### Gate 2. From `review` To `field_note`

必须同时满足：

- 触发条件可描述
- 干预动作可描述
- 结果改善可描述

推荐再满足其中至少一项：

- 与过去样本形成对照
- 评分有明显提升
- 能直接指导下一次同类任务

### Gate 2.5. From `field_note` To `local_skill_reference`

必须同时满足：

- `score_ready`
- `trigger_ready`
- `intervention_ready`
- `result_ready`

翻译成工程约束就是：

- 这条经验足够明确
- 这条经验足够短
- 这条经验值得进入默认读取链路

如果只够保留为 field note，但还不值得占用默认上下文预算，应该停在 field note，而不是硬塞进 local skill layer。

当前第一版 merge / dedup 默认优先看：

- `scene family`
  - 忽略 `alpha / beta / gamma / retry / v2` 这类变体后缀
- `scene role`
  - `baseline / candidate / repair / preflight / spot check / scored result` 这类角色标签默认互斥
- `domain_direction / matched_profile / support_tier`
  - 是否仍是同类运行语境
- 文本相似度
  - trigger / intervention / next move 是否在同一收敛方向上

也就是说：

- 变体 capture 默认应先尝试并回已有 note
- 不是每次 retry 都应该新建 sibling field note
- 但 `baseline` 和 `candidate` 这类真实对照位不应因为文本太像就被自动合并

## Legacy Policy Compatibility

真实 runtime 里可能还存在旧版 `promotion-policy.json`。

第一版兼容策略现在会自动做两件事：

- 用当前默认 policy 补齐旧 policy 缺失字段
- 收紧过宽的旧 archive 关键词
  - 例如不再让泛化过头的 `sample` 误伤 benchmark backlog

也就是说：

- backlog replay 时不会继续被旧治理噪音带偏
- 真实 runtime 下一次跑 worker 时也会自动收敛到更安全的 policy 形态

### Gate 3. From `field_note` To `repo_candidate`

必须同时满足：

- 不依赖单一品牌或单一项目私有上下文
- 结论不是美学偏好，而是判断规则或执行规则
- 能描述适用边界
- 有至少一个对照样本支持

补充边界：

- 这一轮 `runtime -> repo_candidate` 不自动执行
- `repo-candidates/` 目录仍保留，但默认不由 review worker 自动写入
- `runtime -> repo/GitHub` 继续人工审核

### Gate 4. From `repo_candidate` To `pattern`

必须同时满足：

- 触发信号稳定
- failure_before 稳定
- intervention 稳定
- transfer_rule 稳定

默认建议：

- 至少有 `2` 个以上相关样本支持
- 或一个样本加一个强 benchmark 对照支持

### Gate 5. To `archive`

满足以下任一项即可考虑归档：

- 经验已被更高质量记录覆盖
- 任务语境已明显过时
- 只有展示价值，没有判断价值
- 当前无法证明迁移性

## Required Evidence By Level

| Level | Minimum Evidence |
|---|---|
| `capture` | `brief -> image_prompt -> output -> evaluation` 可回溯 |
| `review` | 有至少一个明确问题、改善点或可疑规律 |
| `field_note` | 有明确 trigger、intervention、result |
| `local_skill_reference` | 有明确 trigger、carry-forward、avoid、next-move，且值得占用默认上下文预算 |
| `repo_candidate` | 有适用边界和可迁移理由 |
| `pattern` | 有稳定 trigger、failure_before、intervention、transfer_rule |

## Disqualifiers

出现以下任一项时，不应直接晋升到长期层：

- 只是一次命中
- 只是“更好看”，没有更能用
- 依赖过强的具体品牌语境
- 没有保留 prompt 到 output 的回溯链
- 无法说明为什么有效
- 只能复述案例，无法抽出规则

## Promotion Hint Guidance

如果 capture 里使用 `promotion_hint`，建议只写下面几类：

- `review`
- `field_note_candidate`
- `repo_candidate`
- `archive`
- `none`

`promotion_hint` 是信号，不是最终裁决。

## Capacity Governance

自动晋升不等于无限堆积。

第一版 local skill layer 默认遵守：

- `local_skill_working_set_ceiling`
  - active local skill refs 数量上限
- `max_local_skill_reads`
  - 默认读取预算上限
- `archive`
  - active overflow 的默认出口
- `disable`
  - 临时从默认读取链路移除
- `rollback`
  - 恢复更新前快照

治理偏好顺序：

1. 先限制 active working set
2. 再允许人工 disable / archive
3. 必要时 rollback

一句话：

> local skill layer 是受限工作集，不是无限增长的第二个 field-note 仓库。

## Profile Promotion Link

这份文档处理的是单条样本如何晋升。

如果你要判断的是：

- 某类 `domain_direction` 还只是 exploratory，还是已经能升 standard
- 某个 `matched_profile` 是否已经值得被当成 accelerated 档案

应继续读取：

- `docs/profile-promotion-policy.md`

换句话说：

- `capture -> review -> field_note -> repo_candidate` 是样本层
- `exploratory -> standard -> accelerated` 是 profile 层

前者不能替代后者，后者也不能脱离前者单独成立。

## Decision Ladder

每次 review 时，按下面顺序判断：

1. 这条记录是否值得再次阅读
2. 它有没有清楚的 failure 或 success 机制
3. 它是否只对一次任务有效
4. 它是否能指导下一次相似任务
5. 它是否值得进入 repo 层候选
6. 它是否已经足够抽象成 pattern

## Scoring Signals For Promotion

下面这些信号会提高晋升优先级：

- 总分从 `<75` 提升到 `>=75`
- 从 `conditional_pass` 推进到 `pass`
- 明确识别并修正了某个 failure mode
- 某条 correction rule 在不同任务中复现
- 某种 delivery 或 post-processing 策略被证明更稳

## Local Vs Repo Boundary

### Prefer `field_note` When:

- 结论仍和当前项目强绑定
- 规律看起来有用，但迁移性还没验证
- 更像“工作经验提醒”，而不是稳定规则

### Prefer `repo_candidate` When:

- 规律已从单次任务抽离
- 能清楚讲出适用条件和禁区
- 对多个 use case 有潜在帮助

### Prefer `archive` When:

- 想保留案例但不希望它继续影响默认判断

## Pattern Promotion Contract

进入 pattern 前，至少应能填完整：

- `scene`
- `trigger`
- `failure_before`
- `intervention`
- `transfer_rule`

如果其中任一项说不清，就先停在 `field_note` 或 `repo_candidate`。

## Example Judgments

### Example 1. One Good-Looking Hero With No Clear Why

判断：

- 停在 `capture` 或 `review`

原因：

- 结果虽好，但没有抽出规律

### Example 2. Repair Rule That Repeats Across Two Social Creatives

判断：

- 可升 `field_note`

原因：

- trigger、intervention 和改善结果都已变清楚

### Example 3. Post-Processing Rule Proven Across Hero And Recruitment Poster

判断：

- 可升 `repo_candidate`

原因：

- 不再依赖单一任务，且规则边界可描述

### Example 4. Old Capture From A Dead Visual Direction

判断：

- `archive`

原因：

- 有历史价值，但继续保留在活跃层会造成噪音

## Governance Checklist

- 这条记录是否真的包含可回溯证据
- 这条规律是不是已经超出单一案例
- 当前结论是经验提醒，还是稳定规则
- 升级后会帮助未来判断，还是只会增加噪音
- 这条记录更适合留在本地，还是值得回流 repo
