# Execution Progress Protocol

> Maintainer note: 这份协议只面向仓库维护流程，不属于 skill 的公开使用入口。

## Purpose

这份文档说明项目在执行阶段如何进行进度回写。

目标不是让人手工同时维护多份文档，而是建立一个最小可用机制：

- 一份机器可写的状态源
- 一份自动渲染的人类可读执行看板

## Source Of Truth

执行阶段的单一事实源是：

- `state/execution-progress.json`

这里记录：

- 当前 focus
- 各任务状态
- 每个任务的输出目标
- 当前注记
- 下一步动作

## Auto-Written Plan

人类可读的执行文档是：

- `docs/execution-plan.md`

它不是手工编辑源，而是由脚本自动生成。

## Update Command

更新进度时使用：

```bash
python scripts/update_execution_progress.py --task <task-id> --status <pending|in_progress|completed|blocked> --note "progress note"
```

如果只想根据当前 JSON 重新生成 Markdown：

```bash
python scripts/update_execution_progress.py --render-only
```

## Working Rule

执行阶段的推荐规则是：

1. 开始一个任务时，把它标成 `in_progress`
2. 做完后标成 `completed`
3. 遇到阻塞时标成 `blocked`
4. 每次状态变化都尽量补一句 note

## Why This Exists

如果没有这层机制，升级路线文档只是静态规划。

有了这层机制后，我们可以真正做到：

- 按路线图推进
- 每完成一步就回写进度
- 始终知道当前在做什么
- 把阶段性状态收束到单一入口
