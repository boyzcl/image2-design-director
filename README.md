# image2-design-director

`image2-design-director` 是一个面向高设计可用性图像任务的 skill 仓库。它不是泛用提示词扩写器，而是一个放在任意具备图像生成能力的 Agent 之上的 design-director layer，用来把“能出图”推进到“更像真实产品、设计、增长团队会采用的资产”。

## 适用场景

- 产品或项目公开发布图
- 社交媒体创意图
- UI / UX mockup 方向图
- App 或 workflow 系统的视觉资产
- 已有结果跑偏后的定向 repair

如果任务重点不是“设计可用性”，而是普通艺术创作、摄影、头像、梗图或纯概念视觉，这个 skill 通常不是最佳入口。

## 核心能力

- 三路由执行：`direct`、`brief-first`、`repair`
- 结构化 prompt 组装与设计约束收口
- 设计质量门槛与 scorecard 评估
- runtime memory：记录 brief、prompt、输出与评估
- local compounding：把有复用价值的本地经验晋升为 local references

## 仓库结构

- [SKILL.md](./SKILL.md): skill 主入口与运行规则
- [references/](./references): 对外可复用的核心协议、策略与质量标准
- [patterns/](./patterns): 可迁移的 pattern 模板
- [scripts/](./scripts): runtime、delivery 与治理脚本
- [docs/README.md](./docs/README.md): 文档导航，区分 public-facing 与 maintainer/historical 内容
- [agents/openai.yaml](./agents/openai.yaml): 一个最小 interface 示例

## 最小使用方式

1. 先读 [SKILL.md](./SKILL.md)。
2. 按需读取 `references/` 里的核心协议文档。
3. 把整个目录作为一个 skill 仓库接入你的 Agent 运行环境，或把 `SKILL.md` 与 `references/` 作为可读规则层 vendoring 到现有系统里。
4. 如果要启用本地经验沉淀，再配置 runtime root，并使用 `scripts/` 下的命令写 capture、读取经验、做 review 与本地晋升。

## Runtime Memory 与 Local Learning

这个仓库区分三层：

- `repo`: 规则、模板、脚本、文档
- `host-installed copy`: 某个 Agent 宿主实际加载的 skill 副本
- `runtime`: 本地经验、review queue、field notes、local skill references

`runtime memory` 是本地层，不是 Git 仓库层。它用于沉淀真实运行经验，但不会自动把本地经验直接提升为 repo 规则。

## 当前边界

- local auto-promotion 只作用于本地 runtime / local skill reference 层
- repo 规则更新、GitHub promotion 与公开发布仍然是人工 review 边界
- benchmark / experiment 文档保留为 historical validation，不捆绑本地生成产物
- 仓库默认不包含 runtime、state、test output 或 generated images

## 阅读顺序

- 第一次了解项目：先看 [README.md](./README.md) 和 [docs/README.md](./docs/README.md)
- 直接使用 skill：看 [SKILL.md](./SKILL.md)
- 理解协议层：从 `references/` 开始
- 想看验证证据：再进入 `docs/benchmarks/` 与 `docs/experiments/`
- 做维护或继续研发：最后看 maintainer/historical docs
