# image2-design-director

给具备图像生成能力的 Agent 加上一层 design-director judgment，让结果更接近真实产品、设计、增长团队会采用的视觉资产，而不只是“能出图”。

[SKILL](./SKILL.md) · [Docs Guide](./docs/README.md) · [Architecture](./docs/target-skill-architecture.md) · [Runtime Memory](./references/runtime-memory.md) · [Release Review](./docs/release-readiness-review-2026-04-23.md)

AI Agent 原本常见的问题不是不会写 prompt，而是缺少一层更稳定的设计判断：什么时候该直接生成，什么时候该先补 brief，什么时候该围绕失败类型做最小 repair；什么结果只是漂亮概念图，什么结果才更像可以继续交付的项目资产。`image2-design-director` 补上的就是这层协议、评估和经验复利机制。

兼容思路上，这个仓库面向所有支持 `SKILL.md` 工作流、且具备图像生成能力的 Agent 运行环境。它不绑定单一宿主，repo 规则层和本地 runtime 经验层也被明确分开。

## 支持的能力

| 能力 | 现在支持什么 |
|---|---|
| 路由判断 | 在 `direct`、`brief-first`、`repair`、`contract_realign` 之间选择合适路径 |
| 结构化 prompt 组装 | 把模糊需求收成 intake、task packet、prompt schema、assembly rules 和 sample prompts |
| 参考图适配 | 接收 `reference_assets`，按参考图对齐形式、风格、构图、信息密度、材质和视觉语气 |
| 比例与尺寸约束 | 接收固定比例、像素尺寸、导出尺寸和多尺寸交付约束 |
| 多张输出与抽卡 | 支持 `single-output` 和 `multi-candidate`，可用于多风格测试、方向比较和抽卡选择 |
| 成品与底图分流 | 区分 `complete_asset`、`base_visual`、`delivery_refinement`，不再默认把任务降成底图 |
| 文案与语言控制 | 明确默认语言、允许文字范围、是否 verbatim、是否直出 |
| 设计质量判断 | 用 `quality-bar` 与 `scorecard` 判断结果是否真的过线 |
| runtime memory | 记录 brief、prompt、输出、评估和纠偏，形成可回看经验 |
| local compounding | 把高价值本地经验晋升为 local references，但不自动写回 repo 规则层 |
| delivery-aware handoff | 明确区分 `raw_visual`、`text_safe_visual`、`delivery_ready_visual`，方便后续交付处理 |

## 用户可以直接提的常见请求

- “我给你一张参考图，按这个构图和气质做一版，但主题换成我们的产品。”
- “保持这个风格，给我做成 `4:5`，同时再出一个 `1:1` 版本。”
- “给我 3 张不同方向，我想抽卡选一张最像品牌主视觉的。”
- “先给我一张可以直接发的完整海报，不要底图。”
- “我后面自己排字，你先给我一个干净的 text-safe visual。”
- “这版方向对了，但不像成品，帮我做一次最小 repair。”
- “这不是我要的资产类型，重新按 README hero 来理解，不要再做成海报。”
- “中文对话就用中文文案，项目名保留英文，其余不要乱出英文小字。”
- “这张图里只能出现项目名、主标题和副标题，不允许额外小字。”
- “这个主视觉后面还要扩 `16:9`、`4:5`、`1:1`，请按可扩展交付来做。”

## 典型输入信息

用户不需要一次把所有字段都说全，但下面这些信息会显著提高命中率：

- 参考图或旧版本
- 最终资产类型，例如 `brand promo poster`、`README hero`、`feed creative`
- 是否要完整成品，还是只要底图
- 比例、尺寸或导出要求
- 需要几张候选图
- 固定文案、logo、二维码、badge
- 当前会话语言之外，是否要指定别的文案语言
- 什么结果才算“现在就能用”

## 适合什么任务

- 产品或项目公开发布图
- 社交媒体创意图
- UI / UX mockup 方向图
- App、workflow、protocol 系统相关视觉资产
- 已有结果跑偏后的定向修正

如果任务重点是普通插画、头像、梗图、纯艺术概念图或一般摄影风格探索，这个 skill 往往不是最佳入口。

## 它和普通“提示词增强器”的区别

- 它关注的是“设计可用性”，不是单次 prompt 润色
- 它默认会判断 route、candidate mode、post-process involvement，而不是一把梭地扩写
- 它把失败样本和纠偏规则当成一等公民，而不是只收集成功模板
- 它把 repo 规则层、本地 runtime 和记忆晋升边界写清楚了

## 快速开始

### 1. 安装到你的 skill 目录

目前这个仓库主要提供手动接入方式。最简单的是把整个仓库 clone 到你的 agent skills 目录：

```bash
git clone https://github.com/boyzcl/image2-design-director.git "$AGENT_SKILLS_HOME/image2-design-director"
```

如果你的运行环境没有统一的 `AGENT_SKILLS_HOME`，也可以直接把仓库放到该宿主实际读取 skill 的目录里，或把 `SKILL.md`、`references/`、`patterns/`、`scripts/` vendoring 到现有系统。

### 2. 先读核心入口

第一次使用，建议按这个顺序：

1. [SKILL.md](./SKILL.md)
2. [docs/README.md](./docs/README.md)
3. `references/` 下的核心协议文档

### 2.5 调用方式

显式调用时，直接使用：

```text
$image2-design-director
```

也支持自然语言直接触发，只要你的 Agent 宿主会读取 `SKILL.md` 并按技能描述进行路由。

### 3. 可选启用 runtime memory

如果你只想使用规则层，直接读 skill 即可。

如果你想启用本地经验沉淀，再配置 runtime root，并使用脚本：

```bash
python scripts/init_runtime_memory.py --host generic
python scripts/read_runtime_context.py --host generic --raw-only
```

运行时也可以通过 `IMAGE2_DESIGN_DIRECTOR_RUNTIME_ROOT` 显式指定本地 runtime 根目录。详情见 [references/runtime-memory.md](./references/runtime-memory.md)。

## 仓库结构

- [SKILL.md](./SKILL.md): skill 主入口与默认工作流
- [references/](./references): 对外可复用的协议、策略、质量标准和运行规则
- [patterns/](./patterns): 可迁移的 pattern 模板
- [scripts/](./scripts): runtime、delivery 和治理脚本
- [docs/README.md](./docs/README.md): 文档导航，区分 public-facing 与 maintainer / historical 内容
- [agents/openai.yaml](./agents/openai.yaml): 最小 interface 示例

## 核心文档

- [Prompt Schema](./references/prompt-schema.md)
- [Prompt Assembly](./references/prompt-assembly.md)
- [Task Packet](./references/task-packet.md)
- [Quality Bar](./references/quality-bar.md)
- [Scorecard](./references/scorecard.md)
- [Runtime Memory](./references/runtime-memory.md)
- [Delivery Ops](./references/delivery-ops.md)

## 验证与证据

这个仓库保留了 benchmark 和 experiment 文档，作为历史验证材料，而不是公开仓库首页的主叙事。

可以从这些入口继续看：

- [docs/benchmarks/](./docs/benchmarks)
- [docs/experiments/](./docs/experiments)
- [Status Summary](./docs/status-summary-2026-04-22.md)
- [Stage Progress Review](./docs/stage-progress-review-2026-04-22.md)
- [Release Readiness Review](./docs/release-readiness-review-2026-04-23.md)

## 当前边界

- local auto-promotion 只作用于本地 runtime / local skill reference 层
- repo 规则更新和 GitHub promotion 仍然是人工 review 边界
- runtime、state、generated images、test outputs 默认不进入公开仓库
- 这个仓库提供的是 design-director 协议层与辅助脚本，不替代具体图像模型本身

## 适合先看什么

- 第一次了解项目：看本页和 [docs/README.md](./docs/README.md)
- 直接使用 skill：看 [SKILL.md](./SKILL.md)
- 想理解协议层：从 `references/` 开始
- 想看历史验证：再进入 `docs/benchmarks/` 与 `docs/experiments/`
- 想继续维护和扩展：看 maintainer / historical docs
