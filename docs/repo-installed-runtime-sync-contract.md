# Repo Installed Runtime Sync Contract

> Maintainer note: 这份文档描述的是 repo、宿主安装副本和本地 runtime 的维护边界。公开保留是为了可追溯，但普通使用者通常不需要先读它。

## Purpose

这份文档定义 `image2-design-director` 当前三层边界：

- `repo`
- `installed copy`
- `runtime`

以及它们之间如何同步、什么不应互相覆盖。

一句话版本：

> repo 是规则主副本，installed copy 是宿主执行快照，runtime 是本地经验宿主；三者必须协作，但不能混写成一层。

## Current Risk

当前环境里同时存在：

- repo：`<repo-root>`
- installed copy：`<agent-home>/skills/image2-design-director`

而且两者已经发生明显漂移：

- installed copy 仍保留旧的四 use case / Codex 绑定口径
- repo 已进入 scene generalization + host-agnostic 阶段
- runtime 目录只存在于 installed copy

这意味着：

- 改 repo 不等于宿主已在用新版本
- 改 installed copy 也不等于 repo 已被正确回写

## Layer Ownership

### 1. Repo

repo 负责：

- `SKILL.md`
- `references/`
- `scripts/`
- 核心 benchmark / architecture / status docs
- execution planning docs

repo 是规则和实现的主副本。

### 2. Installed Copy

installed copy 负责：

- 被当前宿主真正加载的技能快照
- 供宿主使用的 `SKILL.md`、`references/`、`scripts/`
- 宿主侧 `runtime/`

installed copy 不是规则源头，而是可执行镜像。

### 3. Runtime

runtime 负责：

- captures
- review queue
- field notes
- repo candidates
- state ledger

runtime 只承接经验，不承接 repo 规则编辑。

## Sync Rules

### Rule 1. Repo -> Installed Is Explicit

repo 规则更新后，只有在显式同步到 installed copy 后，宿主实际行为才算升级。

### Rule 2. Installed -> Repo Is Not Automatic

installed copy 中的临时修补、补脚本、手工热修，必须明确回写 repo，不能默认被视为已进入主副本。

### Rule 3. Runtime Never Gets Replaced By Repo Sync

同步 repo 到 installed copy 时，不应覆盖：

- `runtime/`
- 宿主本地 capture
- review ledger

## Recommended Sync Scope

### Must Sync

- `SKILL.md`
- `references/`
- `scripts/`
- `docs/status-summary-2026-04-22.md`
- `docs/target-skill-architecture.md`
- `docs/benchmarks/`

### Repo-Only By Default

- `state/`
- `docs/execution-plan.md`
- `docs/execution-progress-protocol.md`
- `docs/experiments/`
- `test-output/`

这些内容用于 repo 内开发推进，不要求每次进 installed copy。

### Installed-Only By Default

- `runtime/`
- 宿主生成的缓存或本地状态

## Verification Checklist

每次准备声称“skill 已升级”时，至少检查：

1. repo 侧改动是否完成
2. installed copy 是否已同步核心 skill 文件
3. installed copy 是否没有继续引用旧口径
4. runtime 是否被保留，没有被 repo 覆盖

## Recommended Commands

先看差异：

```bash
diff -rq <repo-root> <agent-home>/skills/image2-design-director
```

再做受控同步：

```bash
rsync -a --delete \
  --exclude 'runtime/' \
  --exclude 'state/' \
  --exclude 'test-output/' \
  --exclude '.DS_Store' \
  <repo-root>/ \
  <agent-home>/skills/image2-design-director/
```

同步后再次做 `diff -rq` 检查，确认剩余差异只来自：

- `runtime/`
- repo-only execution docs
- 系统噪音文件

## Current Contract Decision

当前阶段先把 contract 写清楚，再决定是否把同步脚本自动化。

也就是说：

- 这轮先解决“边界不清”
- 下一轮再优先解决“同步动作自动化或实际执行”

## Relationship To Other Docs

- runtime 字段契约：`docs/runtime-schema-v2.md`
- runtime 总说明：`references/runtime-memory.md`
- 当前状态：`docs/status-summary-2026-04-22.md`
