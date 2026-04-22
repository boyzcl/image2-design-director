# Target Skill Architecture

## Purpose

这份文档把 `image2-design-director` 的目标形态收束成一份稳定架构说明。

它回答三件事：

1. 这个 skill 的完整闭环到底是什么
2. 每个阶段各自负责什么，不负责什么
3. 为什么它不应只是一个“会扩写提示词的生图助手”

## Core Positioning

`image2-design-director` 的目标形态不是单次生图工具，而是一个围绕图像生成建立的双层闭环系统：

- 第一层：单次任务执行闭环
  - 把一轮图片任务做对
- 第二层：经验复利与知识升级闭环
  - 让每轮尝试都能反哺未来判断

一句话版本：

> 它不是只负责“生成图片”，而是负责把需求、上下文、生成、评估、交付和经验沉淀接成一个可持续优化的系统。

## Two-Layer Loop

### Layer 1: Single-Run Delivery Loop

单次任务应该按下面 6 个阶段运行。

#### Stage 1. Requirement Intake

目标：

- 把用户“想要什么”和“为什么要这个东西”收成可执行任务包

至少应确认：

- 用户想要的资产类型是什么
- 这张图最终用在哪里
- 背景上下文是什么
- 是否有品牌、产品、页面、仓库、截图、已有素材
- 是否有固定文本、二维码、logo、尺寸或交付限制
- 用户是想要直出成品，还是允许后处理

本质：

- 不是只收需求
- 而是判断这次任务的上下文边界与约束条件

#### Stage 2. Strategy Selection

目标：

- 决定“怎么做”这轮任务，而不是直接写 prompt

这里至少要判断：

- 当前任务的 `domain_direction` 是什么
- 是否命中已验证档案 `matched_profile`
- 当前支持级别 `support_tier` 属于：
  - `accelerated`
  - `standard`
  - `exploratory`
- 走哪条主路径
  - `direct`
  - `brief-first`
  - `repair`
- 是单图策略还是多候选策略
- 是直出策略，还是“底图 + 后处理”策略

本质：

- prompt 不是第二阶段的输入，而是第二阶段的输出
- 预设档案只是加速器，不是场景边界

#### Stage 3. Prompt Assembly And Image Generation

目标：

- 基于任务包和策略，组装可靠、可控、有效的模型输入

这一阶段应明确区分四类东西：

- 用户原始需求
- 我们理解后的需求摘要
- 结构化上下文
- 最终给 Image2 的 `image_prompt`

本质：

- 从“理解用户”转向“指导模型”

#### Stage 4. Evaluation And Scoring

目标：

- 拿到图片后先评估，再决定是否交付

评估应同时覆盖两类标准：

- 用户预期是否被满足
- skill 的质量标准是否被满足

这里至少要判断：

- 用途是否匹配
- 是否像真实设计 / 产品资产
- 是否存在 AI artifact
- 是否具备后续使用价值
- 是否已经过线，还是只是中间稿

本质：

- 不是问“好不好看”
- 而是问“能不能用、像不像对的资产”

#### Stage 5. Branching: Deliver Or Repair

评估后进入分叉：

- 通过：进入交付阶段
- 不通过：进入修复重生成阶段

当进入修复时，必须明确：

- failure mode 是什么
- 下一轮只改哪些变量
- 哪些部分必须保持不变

本质：

- 让迭代是可诊断、可控的，不靠碰运气

#### Stage 6. Delivery And Assetization

目标：

- 交付“可使用结果”，而不只是交一张图

交付可能包含：

- 最终展示图
- 保留留白的版本
- 便于后续叠字 / 叠二维码的版本
- 不同尺寸版本
- 后处理说明

本质：

- skill 应服务最终资产交付，而不只是服务一次模型输出

### Layer 2: Compounding Loop

这是 skill 的第二层系统，用来保证它会越来越强，而不是每次都从零开始。

#### Stage A. Capture Every Run

每次图片生成都应留痕，包括：

- 用户原始需求
- 我们理解后的需求摘要
- 上下文摘要
- 最终 `final_prompt`
- 最终 `image_prompt`
- 输出图片路径或生成目录
- 当前轮评估结果
- 成功点 / 失败点
- 下一轮修正建议

#### Stage B. Preserve As Local Experience

所有经验先进入本地 runtime。

原因：

- 很多经验只在局部任务里有效
- 不是所有经验都值得立即进入长期知识层

#### Stage C. Promote Experience To Knowledge

经验与知识必须分层：

- `capture`
- `review`
- `field note`
- `pattern / rule`
- 长期 skill 知识

经验是单次样本。
知识是可复用、可迁移、可长期进入 skill 的规则。

#### Stage E. Expand Scene Coverage

skill 不应只在少数预设方向里越来越强。

它还应具备一条通用场景扩展路径：

1. 新场景第一次出现，先以 `exploratory` 跑到可诊断、可继续推进的及格线
2. 如果同类场景重复出现并形成稳定纠偏，升到 `standard`
3. 如果已经形成稳定高分打法，再升到 `accelerated`

这样 skill 的能力边界会不断扩张，而不是永远停在一开始的四个高频档案。

#### Stage D. Controlled Knowledge Upgrade

升级策略必须克制。

只有满足下面条件时，经验才值得晋升：

- 规律明确
- 可迁移
- 不是偶然命中
- 对未来判断有帮助

## Operationalization Layer

当 skill 从“四个已知方向”升级到“全场景 + 已验证档案加速”后，还必须补一层运营化协议。

这层至少包含 4 个面：

1. benchmark surface
   - 不能只验证旧四档案
   - 还要验证新场景首轮是否能先到 `60+`
2. runtime schema
   - capture / review / field note 都要承接 `domain_direction + matched_profile + support_tier`
3. profile promotion policy
   - 明确 `exploratory -> standard -> accelerated` 的晋升门槛
4. repo / installed / runtime sync
   - 明确规则主副本、宿主快照和本地经验宿主的边界

如果少了这层，scene generalization 只会停在 repo 口号，无法变成真实工作系统。

## Enhancement Modules

除了主闭环，这个 skill 还应显式支持下面几类增强模块。

### 1. Post-Processing Module

适用于这些场景：

- 固定二维码
- 确定文案
- 需要人为控制的排版
- 尺寸适配
- icon 放大 / 缩小 / 导出

原则：

- 不是所有内容都适合直接交给模型一次生成
- skill 应能判断哪些内容更适合后置处理

### 2. Multi-Candidate Module

适用于：

- 同需求多方向探索
- 不确定构图
- 希望用户在候选中做判断

形式可以包括：

- 同一 prompt 多候选
- 不同 prompt 版本对比
- 不同构图策略并行

### 3. A/B Testing Module

这里有两种 A/B。

一种是 skill 开发阶段：

- 用不同策略测试效果
- 由评分结果倒推更优流程

另一种是用户任务阶段：

- 对同一需求生成多张候选
- 由用户或评分机制做选择

## Minimal Mental Model

最终应该把这个 skill 理解为 5 个系统模块：

1. 输入层
   - 需求确认
   - 上下文收集
   - 任务分型
   - 策略判断
2. 生成层
   - prompt 组装
   - 模型调用
   - 多候选生成
3. 评估层
   - 质量评分
   - 预期判断
   - 通过 / repair 分叉
4. 交付层
   - 展示
   - 尺寸适配
   - 二维码 / 文本后处理
   - 最终资产输出
5. 复利层
   - runtime capture
   - 经验总结
   - 知识晋升
   - 长期规则更新

## What This Means For The Skill

这套架构意味着：

- 这个 skill 不应只输出 prompt
- 这个 skill 不应只负责第一次生图
- 这个 skill 不应只靠聊天记忆积累经验
- 这个 skill 最终应该同时具备：
  - 任务执行能力
  - 质量判断能力
  - 交付支持能力
  - 经验复利能力
