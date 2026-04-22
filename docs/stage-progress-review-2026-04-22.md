# Stage Progress Review 2026-04-22

> Public historical note: 这是一份阶段复盘文档，主要帮助外部读者理解项目当时推进到了哪里，也帮助维护者追踪哪些阶段已闭环。

## Purpose

这份文档把 `image2-design-director` 当前推进状态，按我们已经实际走过的阶段重新收口。

它回答的是：

1. 每个阶段原本预期要达到什么
2. 当前真实做到哪里了
3. 和预期相比还差什么
4. 哪些阶段已经闭环，哪些还没有

一句话版本：

> 这不是路线图，也不是状态摘要，而是一份“阶段视角”的差距看板。

## Stage Map

当前按 8 个阶段看：

1. Intake / Task Packet
2. Strategy / Route Decision
3. Prompt System / Prompt Family Defaults
4. Delivery Layer
5. Compounding / Runtime Governance
6. Scene Generalization / Host Portability
7. Operationalization
8. Follow-up Validation / Narrow Repair

## Stage Review

| Stage | Original Expectation | Current Reality | Main Remaining Gap | Closure Level | Priority |
|---|---|---|---|---|---|
| 1. Intake / Task Packet | 有稳定 intake schema 和 task packet，能把原始需求收成可执行输入 | 已有 `intake-schema.md`、`task-packet.md`、`strategy-decision-tree.md`，输入层结构基本成立 | 缺更大样本量去证明哪些 intake 字段和问题最值钱 | mostly_closed | medium |
| 2. Strategy / Route Decision | route、candidate、post-process、repair 决策应显式化 | 三路由和策略树已落地，多候选 / post-process policy 已成文 | 跨更多 scene 的迁移稳健性还需要更多真实样本 | mostly_closed | medium |
| 3. Prompt System / Prompt Family Defaults | 有稳定默认 prompt family，并能 regression、repair、promotion | prompt-system 融合、family regression、targeted repair、default promotion、spot-check 都已完成 | 剩余问题已降到局部视觉完成度，不再是系统框架问题 | closed_for_now | low |
| 4. Delivery Layer | skill 不只是出图，而是能稳定交付可使用资产 | delivery docs、bundle versioning、fixed-element overlay、size export、QR replacement validation 都已落地 | 还缺更多真实资产上的 hardening 和版式校准，不再缺主执行链 | mostly_closed | medium-high |
| 5. Compounding / Runtime Governance | capture、review、promotion、repo 回流形成可持续经验复利 | runtime schema v2、promotion governance、profile promotion policy、本地 auto-promotion、local skill reference layer、最小治理与真实 backlog replay 已落地 | 缺更厚的 promotion 样本，以及 runtime-only working layers 的进一步分层策略 | mostly_closed | medium-high |
| 6. Scene Generalization / Host Portability | 从四 use case 走向全 scene，并去掉 Codex 绑定 | scene system + host-agnostic runtime 已成立 | 差距不在定义，而在更多 unmatched scene 证明厚度 | mostly_closed | medium |
| 7. Operationalization | generalized benchmark、runtime schema、promotion gate、repo/installed/runtime 边界都应运营化 | `m9` 已补齐 generalized benchmark surface、runtime schema v2、promotion policy、sync contract，并做过真实 follow-up execution | 缺更厚的 validation surface，sync 也还没自动化 | partially_closed | highest |
| 8. Follow-up Validation / Narrow Repair | 新问题出现后应进入窄 repair，而不是回去大改架构 | 已从 exploratory benchmark 继续修到 destination asset identity，再修到 text discipline pass | 当前只剩 `slight-ui-board-literalness` 这类 polish 级问题 | closed_for_now | low |

## Stage-By-Stage Notes

### 1. Intake / Task Packet

当前不是缺 schema，而是缺更大规模的真实任务验证。

这一步和原预期的差距已经从：

- “没有结构”

收敛成：

- “结构已经有了，但还没经历足够多任务去证明最优字段组合”

### 2. Strategy / Route Decision

这一步当前也不是缺规则，而是缺更大场景面的稳健性验证。

尤其还缺：

- 更多 `standard transfer` 样本
- 更多 delivery-heavy 场景来验证 route 是否仍稳

### 3. Prompt System / Prompt Family Defaults

这一步基本已经过线。

当前剩余差距不是 framework，而是：

- 少数场景的 polish 问题

所以它现在不应再是主攻方向。

### 4. Delivery Layer

这一步已经明显比之前更接近预期了。

当前不再缺：

- delivery policy 文档
- 可执行工具链
- 二维码替换验证

当前还缺的是：

- 更多真实资产上的 zone / typography calibration
- 非二维码类 fixed elements 的更多真实交付验证
- 更强的 export heuristics，而不是只有 safe-first 默认策略

### 5. Compounding / Runtime Governance

runtime 和 promotion policy 已经比早期预期走得更远。

但当前还没达到的点是：

- 真实升档案例还不够
- 自动 review / promotion assist 还偏轻
- cross-scene aggregation 还没形成更强的复利面
- benchmark / backlog 样本目前主要停在 field note，是否需要单独 runtime-only working layer 还没定
- repo / GitHub 公开规则层仍是清晰人工边界，但 repo candidate review 还没有更正式的产品化工作流

### 6. Scene Generalization / Host Portability

定义层已经基本闭环。

当前主要差距是：

- `proof thickness`

也就是：

- 方向已经对
- 但“全场景适用”的样本厚度还不够

### 7. Operationalization

这仍然是当前最值得优先继续推进的阶段之一，但缺口判断已经比之前更窄。

原因不是因为 contract 还没写，也不是因为 local auto-promotion 还没落地，而是因为它现在卡在：

- validation thickness
- promotion thickness
- sync automation
- runtime-only layer stratification

换句话说，协议已经长出来了，但系统级运营化还没足够“厚”。

### 8. Follow-up Validation / Narrow Repair

这一阶段已经按预期工作了。

我们已经证明：

- 不需要回去大改架构
- 可以围绕真实 gap 做单变量 repair

当前剩余只有：

- `slight-ui-board-literalness`

它属于 polish，不应抢走更高层级的优先级。

## Highest-Priority Judgment

当前优先级最高的不是再修单场景视觉，也不再是先证明 local auto-promotion 能不能跑，而是：

> Stage 7. Operationalization

更具体地说，是：

1. 扩验证面
2. 厚 promotion 证据
3. 再决定 runtime working-layer 分层与 sync automation 的下一步

## Recommended Path To Reach Expectation

如果目标是最终达到：

- 全场景适用
- 已验证档案加速
- 宿主无关
- 经验可复利
- repo / installed / runtime 不再漂移

建议按下面路径继续。

### Path 1. Expand Validation Surface First

优先新增 3 类真实 run：

1. `exploratory` unmatched scene 再补 `2-3` 条
2. `standard transfer` 场景至少补 `2` 条
3. `delivery-heavy` 场景至少补 `1-2` 条

目标：

- 先把 generalized claim 的证据面做厚

### Path 2. Use Those Runs To Drive Real Promotion Decisions

不是先空谈 promotion，而是用上面新增样本去判断：

- 哪些 scene 仍应停在 `exploratory`
- 哪些 scene 已够 `standard`
- 是否出现新的 `accelerated` 候选

目标：

- 让 `profile-promotion-policy.md` 从 policy 进入真实执行

同时要顺手回答：

- 哪些样本只应停在 field note
- 哪些样本值得进入 active local skill
- benchmark/backlog 样本是否需要单独的 runtime-only reference layer

### Path 3. Productize Delivery Where Repeated Pain Appears

当 exploratory / standard runs 足够多之后，再根据重复痛点决定 delivery 工具化优先级。

当前最可能优先的方向是：

1. text-safe / delivery-ready 版本化
2. fixed-element overlay
3. size adaptation

目标：

- 让 delivery layer 从“规则存在”升级为“执行低摩擦”

### Path 4. Automate Sync And Drift Detection

当 repo / installed sync 已经验证可行后，下一步应补：

- sync manifest
- drift check
- 一键同步脚本

目标：

- 让宿主实际行为不再依赖手工记忆

## Current Recommendation

当前不建议优先继续做 `slight-ui-board-literalness` polish。

更建议进入一个新的执行阶段：

> `m15_validation_thickening_and_runtime_layer_clarification`

这一阶段的目标应是：

1. 做厚 generalized benchmark / exploratory / standard surface
2. 产出第一批真实 profile promotion judgment
3. 明确 benchmark/backlog 样本在 runtime 中应停在哪一层
4. 再根据真实重复痛点决定 sync automation 与后续 delivery hardening 的排序

如果这一阶段做完，项目和“之前的计划预期”之间的主要差距会明显缩小。
