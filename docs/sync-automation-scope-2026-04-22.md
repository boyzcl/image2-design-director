# Sync Automation Scope 2026-04-22

> Maintainer note: 这份文档讨论的是 repo 与宿主安装副本之间的同步自动化边界，主要供维护者阅读。

## Purpose

这份文档把 repo / installed copy / runtime 的手工 sync 经验收成最小自动化边界。

它回答的是：

- manifest 是否需要
- drift detection 应该查到哪一层
- one-command sync 最小应覆盖哪些路径
- 哪些内容必须继续排除

## Current Inputs

判断主要基于：

- `docs/repo-installed-runtime-sync-contract.md`
- `docs/status-summary-2026-04-22.md`
- 当前 repo / installed / runtime 分层事实

## Decision 1. Sync Manifest Is Needed

判断：`yes`

原因：

1. 当前 sync 不是“把整个 repo 镜像过去”
   - 它本来就有 must-sync、repo-only、installed-only 三种边界
2. 如果没有 manifest，自动化脚本只会把隐性约定重新埋回命令里
3. manifest 是 drift check 和 one-command sync 的共同真相源

## Recommended Manifest Surface

manifest 最小建议只表达三类信息：

1. `must_sync`
   - `SKILL.md`
   - `references/`
   - `scripts/`
   - `docs/benchmarks/`
   - `docs/status-summary-2026-04-22.md`
   - `docs/target-skill-architecture.md`
2. `repo_only`
   - `state/`
   - `docs/execution-plan.md`
   - `docs/experiments/`
   - `test-output/`
3. `installed_only`
   - `runtime/`
   - host-local caches or generated local state

manifest 默认不需要表达更细粒度的业务语义，只要先把路径边界写死即可。

## Decision 2. Drift Detection Should Stay Minimal

判断：只做 `repo-owned sync surface` 的 drift check

最小范围应覆盖：

1. `SKILL.md`
2. `references/`
3. `scripts/`
4. `docs/benchmarks/`
5. `docs/status-summary-2026-04-22.md`
6. `docs/target-skill-architecture.md`

不要默认把 drift check 扩到：

- `runtime/`
- `state/`
- `test-output/`
- repo-only execution notes

原因：

- 这些路径天然允许差异
- 把它们混进 drift check 只会制造大量假阳性

## Decision 3. One-Command Sync Should Be Narrow And Safe

判断：需要 `one-command sync`，但边界必须很窄

最小应做的事：

1. 读取 manifest
2. 把 repo 的 `must_sync` 同步到 installed copy
3. 自动排除：
   - `runtime/`
   - `state/`
   - `test-output/`
   - repo-only docs / experiments
4. 同步后跑一次 drift check
5. 输出剩余差异清单

最小不应做的事：

- 不要覆盖 runtime
- 不要把 installed hotfix 自动回写 repo
- 不要碰 repo-only execution artifacts

## Decision 4. Explicit Exclusion List Must Stay

下面这些路径应继续被视为硬排除：

- `runtime/`
- `state/`
- `test-output/`
- `docs/execution-plan.md`
- `docs/experiments/`
- 其他明确属于 repo 内执行过程的临时记录

原因不是因为它们“不重要”，而是因为：

- 它们不属于 installed executable snapshot 的规则主副本
- 自动化覆盖这些内容会破坏分层

## Recommended Automation Shape

最小自动化建议分成两个命令，而不是一把梭：

1. `check-sync-drift`
   - 只读
   - 输出 manifest 范围内的差异
2. `sync-installed-copy`
   - 按 manifest 执行受控同步
   - 然后自动跑一次 drift check

这样更符合当前阶段：

- 先保证边界正确
- 再提升动作效率

## Why This Scope Is Enough For Now

当前最重要的是：

- 让 repo 更新真正能稳定到达 installed copy
- 同时保证 runtime 不被误覆盖

现在还不需要上来就做更复杂的：

- 双向 sync
- 自动回写 repo
- runtime migration
- experiments auto-sync

这些都应该继续排除，直到真正有重复痛点证明值得做。

## Final Decision

本轮 sync automation scope 正式收口为：

1. 需要 manifest
2. drift detection 只查 repo-owned sync surface
3. one-command sync 只覆盖 `must_sync` 路径
4. `runtime/`、`state/`、`test-output/`、repo-only docs / experiments 必须继续排除

一句话版本：

> 先把“规则主副本如何安全同步到 installed executable snapshot”自动化，不要把 runtime 和记忆层一起卷进去。
