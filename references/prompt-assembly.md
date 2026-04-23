# Prompt Assembly

## Purpose

这份文档定义 `task packet -> final image prompt` 的默认装配方法。

一句话版本：

> packet 是执行输入，schema 是骨架选择，assembly 才是把它变成真正可执行的图像 prompt 或图像段指令；如果任务是 hybrid 或 deterministic，assembly 还要明确哪些内容不交给模型承担。

## Inputs

默认输入来自：

- [references/task-packet.md](references/task-packet.md)
- [references/prompt-schema.md](references/prompt-schema.md)
- [references/information-reliability-gate.md](references/information-reliability-gate.md)
- [references/representation-modes.md](references/representation-modes.md)
- [references/prompt-writing-spec.md](references/prompt-writing-spec.md)

如果 task packet 还不是 `ready`，不要进入 assembly。

## Default Assembly Sequence

### 1. Lock The Asset Contract

先锁定：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

### 2. Lock The Information Contract

再锁定：

- `factual_sensitivity`
- `claim_type`
- `metric_definition`
- `as_of_date`
- `uncertainty_policy`
- `reliability_gate_result`

如果结果是 `blocked_needs_brief`，不要继续 assembly。

### 3. Lock The Representation Strategy

明确：

- `representation_mode`
- `primary_expression_system`
- `deterministic_render_needed`
- `text_generation_tolerance`
- `numeric_render_strategy`

如果当前路径是 `hybrid` 或 `deterministic`，本阶段应同时产出：

- 图像 prompt
- overlay / render spec 占位说明

### 4. Lock The Task Statement

再写一句明确的任务定义：

- 这是什么资产
- 它服务什么目标
- 使用场景是什么

### 5. Choose Prompt Family

按版式复杂度选默认写法：

- 多模块、多区块、多文案层：`Structured / Section-Based`
- 单主体但要保留商业版式和 copy-safe 区：`Hybrid Structured Hero`
- 单图叙事、动作、中心隐喻：`Directed Natural Language`
- 已有图像迭代：在原写法上加 `Repair Overlay`

## Build The Prompt In Layers

### Layer A. Asset Contract Layer

在第一屏就明确：

- final deliverable 是什么
- 这次交的是成品还是底图
- 谁负责最终排版
- 文案语言是什么
- 允许出现哪些文字

### Layer B. Information Contract Layer

如果任务有事实敏感信息，prompt 或 render spec 必须明确：

- 只允许表达哪些 claim
- 哪些 claim 被降级成视觉隐喻
- 哪些数字或日期不会由模型直接生成

### Layer C. Representation Layer

明确当前是：

- 纯模型直出
- 有限文字直出
- text-safe base
- hybrid visual plus deterministic overlay
- deterministic render

### Layer D. Task Layer

先落：

- `asset type`
- `goal`
- `audience/context`

### Layer E. Subject Layer

明确：

- 主体是谁或是什么
- 主体处在什么场景
- 这张图的中心对象或视觉比喻是什么

### Layer F. Structure Layer

高结构任务必须明确：

- 区块
- 区域角色
- 主次层级
- 留白或安全区

### Layer G. Text Layer

文本层默认要单独写，不要埋在 constraints 里。

至少说明：

- `mode`
- `hierarchy`
- `placement`
- `density`

### Layer H. Style Layer

风格层最后补。

### Layer I. Constraints And Avoid

最后才补：

- 非谈判约束
- 明确不要什么

## Resolve The Draft

发送前做两步：

1. 把模板位替换成具体值
2. 删除和当前 representation mode 冲突的内容

## Apply Repair Overlay If Needed

如果是 `micro_repair`，最后再叠加：

```text
Change only: <只改什么>
Keep unchanged: <必须保持什么>
```

如果是 `contract_realign`，先重写：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `metric_definition`
- `representation_mode`
- `acceptance_bar`
