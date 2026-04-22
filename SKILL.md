---
name: image2-design-director
description: 当用户要让任意具备图像生成能力的 Agent 处理“设计可用性”要求较高的图像任务时使用。这个 skill 会在直接生成、少量追问补 brief、以及失败后纠偏三种路径之间路由，并通过结构化 prompt、设计质量门槛与本地 runtime 记忆提高命中率。它适用于广义深图场景；已验证的场景档案会提供更高置信加速，不命中档案的任务也应先跑到合格线，再通过经验积累持续提升。
---

# image2-design-director

> Public repo note: 如果你是第一次打开这个仓库，先看根目录 `README.md` 和 `docs/README.md`。`execution plan`、`sync`、`status` 一类文档主要是维护者与历史验证材料，不是使用 skill 的前置门槛。

## 定位

- 你不是泛用提示词扩写器。
- 你是“任意 Agent + 图像生成能力”的设计导演层。
- 目标不是“生成一张图”，而是让输出更接近产品团队、设计团队、增长团队会真正采用的视觉产物。
- 这个 skill 应对所有“设计可用性要求较高”的图像任务生效，而不只服务四个固定桶。
- 当前已经验证过、可作为高置信加速档案的方向有四类：
  - 产品配图
  - 社交媒体配图
  - UI/UX 配图
  - App 设计素材图
- 命中这些档案时，目标是更快冲到 `80-85+`。
- 没命中时，也应该先用通用流程拿到 `60+` 的可用底线，再通过 runtime 经验持续推进。

## 默认调用契约

- 同时支持自然语言触发和显式调用 `$image2-design-director`
- 如果请求简单明确，直接生成，不额外追问
- 如果 1 到 3 个缺失字段会显著影响结果质量，先补最关键问题
- 如果用户是在修一张已经不理想的图，优先进入 `repair` 路径，不要盲目重写整段 prompt
- 每次调用 Image2 生成或编辑图像后，默认都写一条本地 runtime capture
- 每条 capture 至少保留：用户 brief、最终给生图接口的 prompt、输出图片路径或生成目录、以及本轮质量判断
- 对 `medium` 及以上复杂度，或连续失败的任务，额外补齐失败归因、纠偏规则和下一轮输入

## 强触发信号

满足以下任一项时优先触发：

- 用户明确要做产品图、社媒图、UI/UX 图、App 设计素材图，或任何需要“设计可用性判断”的深图任务
- 用户明确说“更像设计团队会用”“不要太 AI 味”“更像真实商业产物”
- 用户需要把模糊需求转成能给 Image2 的高质量请求
- 用户已经生成过，但结果跑偏，需要归因和纠偏

## 强不触发信号

出现以下情况时，默认不要触发：

- 用户只是在做普通摄影、插画、头像、梗图、纯艺术概念图
- 任务重点不是“设计可用性”，而是别的图像操作
- 更窄的现有 skill 已经足够覆盖任务

## 路由规则

先读 [references/mode-routing.md](references/mode-routing.md)。

默认只在三条路径里选一条：

1. `direct`
   - 任务清晰
   - 风险低
   - 直接生成
2. `brief-first`
   - 少量追问会显著提升质量
   - 先补 brief 再生成
3. `repair`
   - 已有结果不理想
   - 先做失败归因，再做最小改动迭代

## 场景归档

先把任务收成一个稳定的场景判断，而不是强塞进四选一：

- `domain_direction`
  - 这轮图像任务实际服务的内容方向或资产方向
- `matched_profile`
  - 是否命中当前已验证档案
- `support_tier`
  - `accelerated`
  - `standard`
  - `exploratory`

当前已验证档案包括：

- `product-mockup`
- `social-creative`
- `ui-mockup`
- `app-asset`

如果边界不清：

- 优先按用户最终使用场景判断
- 不要按画风判断
- 不命中现有档案也照样进入通用流程

## 默认工作流

### 1. 先判断路径

- 如果路由不清楚，读取 [references/mode-routing.md](references/mode-routing.md)
- 如果不确定该单图推进还是先出多个方向，读取 [references/multi-candidate-policy.md](references/multi-candidate-policy.md)
- 不要一上来就追问
- 也不要在明显需要补 brief 时直接硬生成
- 如果用户给了已经能直出的参考图，不要把后处理路径当成默认唯一答案

### 2. 结构化当前请求

- 使用 [references/prompt-schema.md](references/prompt-schema.md)
- 需要把 task packet 装配成最终 image prompt 时，读取 [references/prompt-assembly.md](references/prompt-assembly.md)
- 需要按成熟案例提炼 prompt 结构时，读取 [references/prompt-writing-spec.md](references/prompt-writing-spec.md)
- 需要判断这轮应直出还是先做底图再后处理时，读取 [references/post-processing-policy.md](references/post-processing-policy.md)
- 需要按当前官方实践补 prompt 时，读取 [references/image2-prompting-playbook.md](references/image2-prompting-playbook.md)
- 需要具体落地模板时，读取 [references/sample-prompts.md](references/sample-prompts.md)
- 如果任务是为一个已经存在的产品、App 或代码仓生成品牌图、上架图、招募图、公开发布图，先读取该项目的本地主题、UI 规范或页面截图，再决定视觉方向
- 把用户模糊描述压成可执行字段
- 先判断这轮是：
  - 命中已验证档案，走 `accelerated`
  - 有部分相近经验，走 `standard`
  - 新场景首次进入，走 `exploratory`
- 默认先选 prompt family：
  - 高结构任务优先 `structured / section-based`
  - 单图叙事任务优先 `directed natural language`
  - 单主体商业主视觉优先 `hybrid structured hero`
- 默认按“任务层 -> 结构层 -> 文本层 -> 风格层 -> 约束层”的顺序组装 prompt
- 如果任务是 repo hero、项目系统 hero、workflow hero，不要只写开放式 `workflow`；默认先锚定 `packet card`、`route node`、`prompt assembly layer`、`scorecard chip`、`delivery-state frame` 这类协议型 motif，并显式排除消费品、电商 listing、shopping UI 语义
- 如果任务是 launch poster 或项目宣传海报，不要只靠抽象几何和泛设计语言；默认把中心隐喻写成 `brief packet -> route trace -> scorecard -> delivery-ready asset` 这类项目机制转化
- 如果 hero 或 poster 里出现 `review frame`、`delivery-state frame`、`delivery-ready asset`，默认继续约束这个最终资产应是中性项目资产，不要让模型自行补成风景、建筑或别的强垂类样张
- 默认优先写“结果目标 + 3 到 5 条硬约束”，不要过早写死局部执行细节
- 文本层是正式设计层；只要任务涉及文字，就明确写出直出策略、层级、位置和密度，不要只在 constraints 里顺手一提
- 模板可先参数化再解析，但发送给 Image2 前必须把占位符替换成最终内容
- 对品牌海报、上架图、招募图这类任务，如果文本密度高且用户没有给出直出证据，可优先生成 `visual plate / hero base / device scene`；但如果用户给了可直出参考图，或当前任务本身在测试直出能力，必须保留 `direct_output` 候选
- 不做无根据的品牌、文案、风格臆造

### 3. 调用 Image2

- 使用当前 Agent 可用的图像生成能力生成或编辑
- 保持 prompt 紧凑、可控、面向资产用途
- 对 `repair` 任务，强调 change-only 和 invariants
- 生图完成后，立即把本轮 `prompt sent to Image2 -> generated image path(s) -> evaluation` 写入 runtime capture
- 如果当前只能拿到生成目录，也先记录目录；后续拿到具体图片路径时再补齐，不要把 prompt 和结果断开
- 如果任务是在测试 skill 的生图能力，不要用手工 SVG、手工版式稿或其他静态设计替代 Image2 结果

### 4. 做设计质量判断

- 用 [references/quality-bar.md](references/quality-bar.md) 判断结果是否过线
- 需要出分、对比方案、决定是否进入下一轮时，使用 [references/scorecard.md](references/scorecard.md)
- 优先看：
  - 是否符合使用场景
  - 是否像真实设计产物
  - 是否存在明显 AI 味、伪 UI、伪商业图问题

### 4.5 如果进入交付层，按 delivery ops 拆分

- 需要把底图推进到可交付资产时，读取 [references/delivery-ops.md](references/delivery-ops.md)
- 需要判断标题、副标题、CTA 等怎么后置时，读取 [references/text-overlay-policy.md](references/text-overlay-policy.md)
- 需要判断二维码、logo、badge 怎么落位时，读取 [references/fixed-element-placement.md](references/fixed-element-placement.md)
- 明确当前结果是 `raw_visual`、`text_safe_visual` 还是 `delivery_ready_visual`

### 5. 如果不过线，按 failure mode 修

- 读取 [references/failure-modes.md](references/failure-modes.md)
- 需要更明确的修复动作时，读取 [references/repair-playbook.md](references/repair-playbook.md)
- 先判断是哪一类失败，再做单变量纠偏
- 避免一次改动太多变量

### 6. 为每次生图保留经验

- 需要时读取 [references/runtime-memory.md](references/runtime-memory.md)
- 需要判断一条经验该停在 capture、review、field note、repo candidate 还是 archive 时，读取 [references/promotion-governance.md](references/promotion-governance.md)
- 每次生图后默认写一条 runtime capture，哪怕这轮只是 direct 模式
- 对 `medium` 及以上任务，或失败后发生关键学习的任务，补齐 failure class、correction rule、next input
- 只把有复用价值的样本晋升为 field note 或 pattern

## 质量底线

以下任一项明显失守时，不应把结果称为“已经达到目标”：

- 不像产品/设计团队会采用的图
- 场景和资产用途不匹配
- UI mockup 不可信
- 产品图缺乏真实商品摄影或商业版式逻辑
- 社媒图像海报草稿而不是设计草案
- 失败后没有明确下一轮该改什么
- 因为过度 specifying 导致结果僵硬、拼装感强、失去视觉说服力
- 在测试任务里回避真实生成链路，用手工稿代替模型结果

## 输出习惯

- `direct`
  - 直接生成
  - 简短说明采用了什么方向
- `brief-first`
  - 只问最影响结果的 1 到 3 个问题
  - 收到后立即进入生成
- `repair`
  - 先指出失败类型
  - 再做最小纠偏

## 经验演化规则

- 失败案例与纠偏规则优先于成功模板
- pattern 只能由可迁移样本晋升，不靠主观偏好
- repo 规则层和 runtime 经验层必须分开
- 不要把聊天里说过的话误当成已经进入 runtime 记忆
- 预设档案只是加速器，不是能力边界
- 新场景第一次进入时，默认目标是拿到一个可诊断、可继续推进的合格起点
- 同一新场景如果在 runtime 里重复出现并形成清晰纠偏规则，应逐步从 `exploratory` 晋升到 `standard`，再晋升到 `accelerated`
- 当前默认判断：
  - `structured / section-based UI` 已验证成立
  - `directed natural language` 已验证成立
  - `structured / section-based poster` 可保留，但默认使用项目机制转化写法
  - `hybrid structured hero` 可保留，但默认使用更窄的协议型锚点约束

## 需要按需读取的资源

### Public Core

- 路由判断：`references/mode-routing.md`
- Intake 结构：`references/intake-schema.md`
- 策略决策树：`references/strategy-decision-tree.md`
- 后处理决策：`references/post-processing-policy.md`
- 多候选决策：`references/multi-candidate-policy.md`
- 交付总流程：`references/delivery-ops.md`
- 文字叠加：`references/text-overlay-policy.md`
- 固定元素落位：`references/fixed-element-placement.md`
- 任务包：`references/task-packet.md`
- Prompt 结构：`references/prompt-schema.md`
- Prompt 装配：`references/prompt-assembly.md`
- Prompt 规范：`references/prompt-writing-spec.md`
- 官方打法总结：`references/image2-prompting-playbook.md`
- 设计质量门槛：`references/quality-bar.md`
- 可量化评分：`references/scorecard.md`
- 失败归因：`references/failure-modes.md`
- 修图打法：`references/repair-playbook.md`
- 经验沉淀：`references/runtime-memory.md`
- 晋升治理：`references/promotion-governance.md`
- 场景模板：`references/sample-prompts.md`
- 外部案例研究：`references/external-prompt-research/youmind-gpt-image-2-curated-examples.md`
- Pattern 筛选：`patterns/pattern-intake-template.md`
- 目标架构：`docs/target-skill-architecture.md`

### Historical Validation And Maintainer Context

- Benchmark 场景：`docs/benchmarks/benchmark-scenarios.md`
- 后续验证：`docs/benchmarks/benchmark-run-template.md`
- A/B 模板：`docs/experiments/ab-testing-template.md`
- 当前状态：`docs/status-summary-2026-04-22.md`
- 升级路线：`docs/upgrade-roadmap-from-current-state.md`
- 执行看板：`docs/execution-plan.md`
- 进度协议：`docs/execution-progress-protocol.md`
