# README Homepage Draft V1

> 这是一份图片主叙事的 README 首页草稿。当前使用占位图片路径，等图片正式入库后可直接替换。

```md
# image2-design-director

给具备图像生成能力的 Agent 加上一层“设计导演判断层”，让结果更接近真实用户会采用的图像成品，而不只是“能出图”。

[Skill 入口](./SKILL.md) · [文档导航](./docs/README.md) · [首页图片方案](./docs/readme-image-story-homepage-plan-2026-04-23.md) · [出图 Prompt 包](./docs/readme-image-story-prompts/readme-homepage-image-suite-v1.md) · [目标架构](./docs/target-skill-architecture.md)

![README Hero](./assets/readme-story/01-hero.png)

不是让 agent 更会出图，而是先让它做对图。

大多数图像生成任务失败，不是因为模型不会生成，而是因为系统过早开始优化 prompt，却还没确认自己要交付的到底是什么资产。`image2-design-director` 补上的，是这层缺失的设计导演判断。

![Problem](./assets/readme-story/02-problem.png)

## 普通生图为什么会跑偏

常见问题不是“画得不够漂亮”，而是：

- 资产类型错了
- 成品度错了
- 语言策略错了
- 该重建理解时却只做局部修补

![Asset Contract](./assets/readme-story/03-asset-contract.png)

## 先收 Asset Contract，再决定怎么生成

这个 skill 在真正开始生成前，会先确认交付物合同：

- 最终资产是什么
- 这是成品还是底图
- 默认文案语言是什么
- 图里允许出现哪些文字
- 谁负责最终排版
- 怎样才算用户可验收

![Route](./assets/readme-story/04-route.png)

## 同一个任务，不一定走同一条路

根据合同清晰度和任务状态，系统会在不同路径之间分流：

- `direct`
- `brief-first`
- `repair`
- `contract_realign`

它不是一把梭地反复重试，而是先判断这轮到底该怎么跑。

![Acceptance](./assets/readme-story/05-acceptance.png)

## 判断标准不是“好不好看”

真正的验收问题是：

- 这是不是用户要的那类资产
- 现在是不是可直接使用的完成状态
- 文案语言和文字策略是否一致
- 输出是否仍在原始合同边界之内

![Delivery Ops](./assets/readme-story/06-delivery-ops.png)

## 一张图过线后，才值得进入交付推进

`image2-design-director` 不只负责生成一张图，还会把过线结果继续推进成真正可交付资产，例如：

- 多尺寸版本
- 文案细化
- 二维码与 logo 落位
- 发版级资产整理

## 快速开始

显式调用：

```text
$image2-design-director
```

第一次使用，建议先看：

1. [SKILL.md](./SKILL.md)
2. [docs/README.md](./docs/README.md)
3. [首页图片方案](./docs/readme-image-story-homepage-plan-2026-04-23.md)
4. [出图 Prompt 包](./docs/readme-image-story-prompts/readme-homepage-image-suite-v1.md)

## 当前边界

- 这个仓库提供的是设计导演协议层和辅助脚本，不替代具体图像模型本身
- 本地运行时经验与仓库规则层分离
- benchmark 与 experiment 文档保留为验证材料，而不是首页主叙事
```
