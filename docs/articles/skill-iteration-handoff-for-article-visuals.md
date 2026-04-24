# 新会话执行指令：先迭代 `image2-design-director`，再处理公众号文章配图

## 任务背景

当前正在为 `image2-design-director` 撰写一篇可直接发布的公众号文章《我为什么还是做了 `image2-design-director`，当 `gpt-image-2` 已经这么强之后》。

在文章成稿过程中，我们尝试用当前的 `image2-design-director` 为文章生成配图，并经历了多轮失败与返工。

这些失败不应该再被当作单次操作失误看待。它们已经暴露出当前 skill 在“文章配图 / editorial collateral / publication asset”这一类场景上的协议缺口、流程缺口和验收缺口。

因此，当前优先级不是继续给文章硬做图，而是：

> 先系统性迭代 `image2-design-director`，把这次暴露出来的问题修到机制层，再回头处理文章配图与最终交付。

## 这次实际遇到的问题

### 1. 任务对象与文案合同多次漂移

- 最早一批图里出现了 `深图`，而文章已经明确纠正对象是 `gpt-image-2`
- 一些图里出现了与文章无关的活动报名语义、二维码、CTA、日期、badge
- 这些内容并不是文章需要的资产元素，而是别的合同残留

这说明当前系统没有足够强地锁住“当前交付物到底是什么”。

### 2. benchmark 工件被错误复用成 publication asset

- 这次有多张图并不是为文章新生成的
- 它们来自 benchmark candidate、overlay viability bundle、delivery-ready event poster 等已有产物
- 这些图在原场景里可能是有效工件，但不等于适合作为公众号文章配图

这说明当前 skill 缺少一条非常重要的规则：

> benchmark artifact 不得默认充当 publication asset

### 3. 成品图规则没有被真正执行到底

- 文章场景其实已经明确要求默认交付 `complete_asset`
- 但实际过程中却多次落成了 `masthead-safe`、`title-safe`、`text-safe` 的中间稿
- 即便后来补了 overlay，也没有先经过正式的最终评分审核，就被拿去给用户看

这说明 `complete_asset by default` 虽然在理念上存在，但在执行链里没有被强制落实。

### 4. `delivery viability gate` 走了，但没有形成真正的 publication 审核

- overlay 过程里确实跑了 `delivery viability`
- 但很多图的 `protected_regions` 其实是空的
- 也就是说，做了基础覆盖率和 box-level overlay 检查，却没有真正做有效的主体碰撞检测
- 更关键的是，图在展示给用户之前，没有再经过完整的 `scorecard` 审核

这说明当前系统把“能 overlay”误当成了“能发布”。

### 5. 文章配图场景没有正式建模

目前 skill 对以下场景已经有一定协议化能力：

- 品牌图
- README hero
- limited-text feature visual
- high-fact-sensitivity hybrid visual
- overlay delivery viability

但对“公众号文章配图 / editorial collateral / argument-supporting publication image”这一类场景，还没有正式定义：

- deliverable_type
- acceptance bar
- representation strategy
- publication vs benchmark reuse boundary
- final review gate

这导致系统不断在“机制图”“头图”“workflow evidence 图”“benchmark 说明图”之间来回滑动。

## 这些问题的根本原因

### 根因 1. 缺少正式的文章配图场景协议

当前 skill 还没有把 `wechat_article_editorial_visual_set` 或等价场景真正产品化。

结果就是：

- 文章图会被误当成 README hero
- README hero 会被误当成 workflow evidence
- benchmark collateral 会被误当成 publication illustration

也就是说，场景画像不完整，导致资产身份反复漂移。

### 根因 2. 执行链没有把“用户看到的图”绑定到最终审核

目前链路更像这样：

`contract -> route -> generation -> overlay viability -> 给用户看`

但真正应该是：

`contract -> route -> generation -> delivery viability -> publication scorecard review -> only then user-facing output`

少掉的那一层，就是正式的用户前审核。

### 根因 3. “中间工件”和“最终资产”边界不清

当前 skill 已经能很好地产生很多中间工件：

- text-safe visual
- delivery-ready bundle
- benchmark candidate
- exploratory editorial cover
- mechanism visual skeleton

但系统没有明确防止：

- 中间工件被直接当最终图交付
- 原场景工件被跨场景复用

这不是单点 prompt 问题，而是资产治理问题。

### 根因 4. overlay gate 还停留在局部工程工具级

当前 `delivery viability gate` 能做的更多是：

- box-level overlay coverage
- hard/soft collision 判断
- go / with_limits / no_go

但 publication 级的文章配图还需要额外回答：

- 这张图语义上是否对题
- 它是不是正确的 publication asset
- 这个 overlay 之后，图是否仍然像一张真正的文章配图，而不是一个被技术上允许叠字的工作图

也就是说，当前 viability 更偏“能不能继续叠”，还不够偏“是不是可以发布”。

## 需要解决的完整方向

### 方向 A. 为文章配图新增正式场景协议

新增一个正式的场景类型，名称可以是：

- `wechat_article_editorial_visual_set`
- 或 `editorial_publication_visual`

至少补齐：

- `deliverable_type`
- `usage_context`
- `asset_completion_mode`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

并明确：

- 默认是 `complete_asset`
- 默认交付的是成品图，不是中间稿

### 方向 B. 新增 publication asset 审核层

在现有 `delivery viability gate` 之后，再新增一层：

- `publication_readiness_review`

至少判断：

- 这张图是否属于正确资产类型
- 图像语义是否支持文章论点
- 图中是否存在跨场景残留文案或 fixed elements
- 风格是否符合 publication 场景
- 是否达到 `pass / conditional_pass / fail`

并强制执行：

> 未通过 publication review 的图，不能给用户看，也不能挂进正文

### 方向 C. 禁止 benchmark artifact 默认直出给用户

新增规则：

- benchmark candidate
- delivery bundle artifact
- overlay demo
- exploratory repair output

默认只能算：

- internal evidence
- review candidate
- reusable source

不能默认算：

- final publication asset

需要显式 override 才能跨用途进入正文。

### 方向 D. 把 `protected_regions` 变成文章图的必填项

当前文章图 overlay 的问题之一是：

- viability 跑了
- 但 `protected_regions` 为空

需要改成：

- 文章图一旦进入 overlay，就必须声明 protected regions
- 至少包含标题区不可撞、核心主体不可压、关键信息焦点区不可破坏

没有 protected regions，就不允许 claim 已做过完整碰撞检测。

### 方向 E. 把“中间工件”和“最终资产”分层治理

明确几类状态：

- `raw_visual`
- `text_safe_visual`
- `editorial_ready_visual`
- `publication_ready_visual`

如果不想新增太多状态，最少也要在 metadata 里加：

- `artifact_role: internal_candidate | review_candidate | publication_asset`

并让系统在展示给用户前检查：

- 当前图是不是 `publication_asset`

### 方向 F. 为文章配图补 benchmark surface

新增至少 3 个 benchmark：

1. `bm_editorial_cover_publication_asset`
2. `bm_mechanism_figure_publication_asset`
3. `bm_workflow_evidence_publication_asset`

目标不是只看图好不好看，而是验证：

- 资产身份稳不稳
- complete asset 是否真的被落实
- publication review 是否能拦住中间稿和错场景图

## 新会话的执行目标

在新会话里，不要继续直接给文章出图。

先完成下面 4 件事：

1. 把文章配图场景正式写进 skill 协议
2. 把 publication review 层补进当前工作流
3. 把 benchmark artifact 与 publication asset 的边界规则补齐
4. 设计并跑通最小 benchmark，确认这些规则已经生效

只有这些做完以后，才回到文章配图任务。

## 新会话里建议直接执行的步骤

### Step 1. 收清当前相关协议文件

重点检查并更新：

- `SKILL.md`
- `references/intake-schema.md`
- `references/strategy-decision-tree.md`
- `references/quality-bar.md`
- `references/scorecard.md`
- `references/delivery-viability-gate.md`
- `references/runtime-memory.md`

同时决定文章配图场景应该落在哪一层。

### Step 2. 新增文章配图协议文档

新增一份正式 reference，内容至少包括：

- scene definition
- required figure classes
- complete-asset default rule
- publication vs benchmark boundary
- required protected regions
- publication review checklist

### Step 3. 把 publication review 接进主链路

要求系统在用户看到图之前，必须输出：

- `pass / conditional_pass / fail`
- `misleading_risk`
- `hard_fail_reason`

并明确：

- `overlay_allowed` 不等于 `publication_pass`

### Step 4. 设计最小 benchmark pack

至少验证：

- 头图不会再滑成中间稿
- 机制图不会再只做出 benchmark skeleton
- workflow evidence 图不会再滑向 README hero 或 scenic product hero
- 错场景工件会被 publication review 拦下

### Step 5. 完成后，再回到文章

只有在上述协议补完并验证通过后，再重做文章配图。

## 可直接复制到新会话的执行指令

下面这段可以直接在新会话里作为启动指令使用：

```md
当前不要继续直接给公众号文章生成配图，先迭代 `image2-design-director` 本身。

背景是这样的：

我们在为《我为什么还是做了 image2-design-director，当 gpt-image-2 已经这么强之后》这篇文章制作配图时，暴露出了一系列系统性问题。这些问题已经不再是单次操作失误，而是 skill 在“文章配图 / editorial collateral / publication asset”场景上的协议缺口。

已确认的问题包括：

1. 多次发生任务对象与文案合同漂移，例如图里出现 `深图`、活动报名文案、二维码、CTA、日期、badge 等与文章无关的内容。
2. benchmark candidate、overlay bundle、delivery-ready event poster 等内部工件被错误复用成 publication asset。
3. 虽然文章场景要求默认 `complete_asset`，但实际多次交付了 masthead-safe、title-safe、text-safe 中间稿。
4. `delivery viability gate` 走了，但没有在用户前再做完整的 `pass / conditional_pass / fail` 审核。
5. overlay 过程里很多图虽然做了 coverage 检查，但 `protected_regions` 为空，导致不能算真正完成了有效碰撞检测。
6. 当前 skill 尚未正式建模“公众号文章配图 / editorial publication visual”这一场景，导致资产身份在头图、机制图、workflow evidence 图、README hero、benchmark collateral 之间反复漂移。

请你在这个新会话里，把主任务切换为：

> 先补齐 `image2-design-director` 在文章配图 / publication asset 场景上的协议、审核和 benchmark，再回头处理文章本身。

请按下面顺序执行：

1. 盘点并更新现有主链路协议文件，包括：
   - `SKILL.md`
   - `references/intake-schema.md`
   - `references/strategy-decision-tree.md`
   - `references/quality-bar.md`
   - `references/scorecard.md`
   - `references/delivery-viability-gate.md`
   - `references/runtime-memory.md`

2. 新增正式的文章配图场景协议，至少定义：
   - `deliverable_type`
   - `usage_context`
   - `asset_completion_mode`
   - `allowed_text_scope`
   - `layout_owner`
   - `acceptance_bar`
   - `publication asset` vs `benchmark artifact` 边界

3. 把新的 `publication review` 层接进主链路，要求任何展示给用户的图必须先输出：
   - `pass / conditional_pass / fail`
   - `misleading_risk`
   - `hard_fail_reason`

4. 强化 overlay 检测规则，要求文章配图进入 overlay 时必须提供有效的 `protected_regions`，否则不能宣称已经完成碰撞检测。

5. 新增最小 benchmark pack，至少覆盖：
   - editorial cover publication asset
   - mechanism figure publication asset
   - workflow evidence publication asset
   - benchmark artifact 被 publication review 拦截

6. 在上述协议补完并完成最小验证前，不要继续直接为文章生成最终配图。

最终输出要求：

- 明确写出当前问题、本质原因、协议修正方案、benchmark 方案
- 完成必要的文档与代码更新
- 明确哪些问题已经被修到机制层，哪些还只是临时 workaround
```

## 当前任务完成定义

当前这个 handoff 文档的完成标准是：

- 已经清楚总结本次文章配图过程中的主要问题
- 已经抽象出这些问题的根本原因
- 已经给出先修 skill、再回到文章的完整方向
- 已经提供一份可以直接在新会话里执行的指令

这份文档本身不负责修完问题。

它负责让下一次对话从正确的问题定义开始。
