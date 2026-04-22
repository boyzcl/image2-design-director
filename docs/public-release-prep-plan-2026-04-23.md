# Public Release Prep Plan 2026-04-23

## Purpose

这份文档定义 `image2-design-director` 在推送到 GitHub 公开仓库之前，需要完成的最小公开化整备方案。

目标不是继续扩功能，而是把当前“内部研发仓库”收口成“可公开理解、可公开浏览、可公开复用”的 skill 仓库。

一句话版本：

> 先做 publish hardening，再公开，不把本地路径、测试产物、内部执行叙事直接暴露到公开仓库。

## Release Decision

当前判断：

- `private GitHub backup`
  - 随时可做
- `public GitHub skill release`
  - 需要先完成本方案中的公开化整备

## Target State

完成后，仓库应满足：

1. 第一次打开仓库的外部用户，能在根目录立刻理解：
   - 这是什么 skill
   - 解决什么问题
   - 如何使用
   - 仓库里哪些内容是核心，哪些是研究/历史
2. 仓库中不再泄露：
   - 本地绝对路径
   - 本机宿主路径
   - 本地 generated image 路径
   - 不该进入公开仓库的测试产物
3. 仓库结构能区分：
   - 面向外部用户的公开说明
   - 面向维护者的内部执行记录
4. 仓库可被正常 clone、浏览、引用，而不会因为脏文件或本地痕迹显得像半成品

## Main Gaps To Fix

当前最主要的公开化缺口有 6 类：

1. Root publishing surface 缺失
   - 根目录没有 `README`
   - 根目录没有 `LICENSE`
   - 根目录没有 `.gitignore`
2. 本地执行痕迹过重
   - `.DS_Store`
   - `test-output/`
   - 可能还有 runtime-like replay fixtures
3. 文档里存在大量本地绝对路径
   - 个人机器绝对路径
   - 宿主私有路径
   - 本地 generated image 路径
4. 公开文档和内部执行文档没有清晰分层
   - status / execution / sync / replay 仍偏内部研发语境
5. benchmark / experiment 文档目前更像研发记录
   - 对公开访客噪音高
   - 同时还带本地路径引用
6. 对外叙事还没收口
   - 现在的仓库更像“做了很多事”
   - 还不像“一个别人能理解并使用的 skill 产品”

## Workstreams

### Workstream 1. Build The Public Root Surface

目标：

- 让根目录具备最小公开仓库形态

必须完成：

1. 新增根目录 `README.md`
2. 新增根目录 `.gitignore`
3. 新增根目录 `LICENSE`

`README.md` 最少应包含：

- skill 是什么
- 适用场景
- 核心能力
- 仓库结构
- 最小使用方式
- runtime memory / local learning 是什么
- 当前边界
  - local auto-promotion 是本地层
  - repo / GitHub promotion 仍是人工

`.gitignore` 最少应排除：

- `.DS_Store`
- `test-output/`
- 任何 runtime/state/replay 产物
- 常见 Python cache

### Workstream 2. Clean Repository Hygiene

目标：

- 移除不应进入公开仓库的本地产物

必须完成：

1. 删除根目录 `.DS_Store`
2. 明确 `test-output/` 不进入公开仓库
3. 检查是否有其它应排除的临时产物

注意：

- 不要误删仓库中真正要保留的 references/docs
- 优先通过 `.gitignore` 和必要的删除操作收口

### Workstream 3. Sanitize Local Paths And Host-Specific References

目标：

- 去掉公开仓库中的个人本地路径和宿主私有路径

必须检查并处理：

1. 文档中的个人机器绝对路径
2. 文档中的宿主私有路径
3. benchmark / experiment 文档中的 generated image 绝对路径
4. references 中引用其它本地仓库路径的例子

处理原则：

- 能泛化就泛化成相对或占位路径
- 能删掉就删掉
- 真正只对维护者有意义的内部执行细节，应移出公开主面

不要保留：

- 个人用户名
- 本机目录结构
- 本机 generated_images 链接

### Workstream 4. Separate Public Docs From Internal Maintenance Docs

目标：

- 仓库首页和核心 docs 面向外部用户
- 内部执行追踪文档降噪或归档

建议分层：

1. Public-facing
   - `README.md`
   - `SKILL.md`
   - 核心 `references/`
   - 少量必要 architecture / policy docs
2. Maintainer-facing
   - execution plan
   - status summary
   - stage progress review
   - sync automation scope
   - benchmark run logs
   - experiment run logs

建议动作：

- 不一定删除内部文档
- 但需要在 `README` 里重新组织“先看什么，后看什么”
- 必要时为内部文档增加 `maintainer-only` 说明

### Workstream 5. Reduce Public Noise In Benchmark / Experiment Docs

目标：

- 保留证明力，降低研发噪音

执行策略二选一，优先选更轻的一种：

1. 保留 benchmark / experiment docs，但统一去本地路径并加“historical validation”定位
2. 或把最噪音的执行日志移到单独 archive/maintainer 区域

最低要求：

- benchmark docs 不再直接暴露本地图片绝对路径
- experiment docs 不再像私人工作台记录

### Workstream 6. Reframe The External Narrative

目标：

- 把仓库叙事从“内部研发过程”改成“公开 skill 产品”

对外表述应重点强调：

- 这是一个 design-director layer
- 它适用于高设计可用性要求的 Image2 任务
- 它有 runtime learning
- 它支持 local compounding
- 它已经有 delivery chain / benchmark / governance 基础

但应弱化：

- 过多的内部 milestone 叙事
- 过细的个人执行时间线
- 和具体本机安装路径强绑定的说法

## Suggested File Actions

高优先级新增：

- `README.md`
- `.gitignore`
- `LICENSE`

高优先级更新：

- `SKILL.md`
- `docs/status-summary-2026-04-22.md`
- `docs/stage-progress-review-2026-04-22.md`
- `docs/upgrade-roadmap-from-current-state.md`
- `references/runtime-memory.md`
- `references/task-packet.md`
- `references/intake-schema.md`
- `docs/repo-installed-runtime-sync-contract.md`
- `docs/benchmarks/*.md`
- `docs/experiments/*.md`

高优先级移除或排除：

- `.DS_Store`
- `test-output/`

## Execution Order

建议按这个顺序执行：

1. 建 `README.md` / `.gitignore` / `LICENSE`
2. 删除 `.DS_Store` 并处理 `test-output/`
3. 全仓扫描并清理本地绝对路径
4. 收口 docs 分层与 public narrative
5. 清理 benchmark / experiment 文档中的本地图片路径
6. 最后做一轮 release-readiness review

## Release Readiness Checklist

公开发布前必须满足：

- 根目录存在 `README.md`
- 根目录存在 `.gitignore`
- 根目录存在 `LICENSE`
- 根目录不再有 `.DS_Store`
- `test-output/` 不进入公开仓库
- 全仓不再出现个人机器绝对路径
- 全仓不再出现公开无意义的宿主私有路径
- benchmark / experiment 文档不再依赖本机图片链接
- README 已能独立解释 skill 的价值、用法和边界
- local auto-promotion 与 repo manual boundary 已在公开文档中被正确表达

## Out Of Scope

这轮不要做：

- 新功能扩展
- delivery 新工具开发
- benchmark 新一轮运行
- sync automation 实现
- repo candidate 自动化升级

只做公开化整备。

## Definition Of Done

完成后应达到：

1. 仓库可以直接公开到 GitHub
2. 外部用户进入仓库不会看到个人路径和本机产物
3. 外部用户能在 2 到 3 分钟内理解这个 skill 是什么、怎么用、边界在哪里
4. 仓库保留必要技术深度，但不再像内部工作台快照
