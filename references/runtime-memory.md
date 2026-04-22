# Runtime Memory

## 目标

让这个 Skill 的经验不是停在聊天里，而是能本地沉淀、复查、晋升。

## 分层原则

- `repo`
  - 规则、模板、脚本、固定 failure mode、初始 pattern
- `host-installed copy`
  - 任意 Agent 宿主中的 Skill 副本
- `runtime`
  - 本地经验宿主

不要把仓库里的文档误当成已经进入 runtime 的经验。

scene generalization 之后，runtime 默认按 `schema v2` 承接 scene-profile 主字段：

- `domain_direction`
- `matched_profile`
- `support_tier`

兼容旧记录时可保留：

- `legacy_use_case`

具体字段契约见：

- `docs/runtime-schema-v2.md`
- `docs/repo-installed-runtime-sync-contract.md`

## 默认 runtime root 解析

runtime 不应绑定某个单一 Agent。

默认按下面顺序解析：

1. `--root`
2. `IMAGE2_DESIGN_DIRECTOR_RUNTIME_ROOT`
3. `AGENT_SKILLS_HOME`
4. 已知 Agent home 环境变量
5. `AI_AGENT_HOME` 或 `AGENT_HOME`
6. 通用兜底 `~/.ai-agents/skills/image2-design-director/runtime/`

## 运行时目录

- `captures/`
  - 原始经验记录
- `index/`
  - 轻量索引
- `inbox/`
  - 待 review 条目
- `promoted/field-notes/`
  - 本地晋升的经验
- `promoted/local-skill/active/`
  - 默认会被 skill 读取链路优先读取的本地参考层
- `promoted/local-skill/disabled/`
  - 被人工禁用、暂时不进入默认读取链路的本地参考
- `promoted/local-skill/archive/`
  - 因容量治理或人工治理退出 active working set 的本地参考
- `promoted/local-skill/history/`
  - local skill reference 被更新前保留的回滚快照
- `promoted/repo-candidates/`
  - 值得考虑回流仓库规则层的候选
- `promoted/archive/`
  - 低价值或一次性样本
- `state/`
  - policy、ledger、manifest

其中：

- `state/local-skill-manifest.json`
  - 记录每条 local skill reference 的 `status`、`path`、`version`、来源 field note 和治理状态
- `state/promotion-policy.json`
  - 包含 local skill 自动晋升门槛、读取预算和 active working-set 上限

## 何时写 capture

默认规则：

- 每次调用 Image2 生成或编辑图像后，都写一条 capture

额外必须补全评估与纠偏字段的场景：

- 任务复杂度 `medium+`
- 用户对结果预期高，且过程中做了关键判断
- 生成失败后找到了明确 failure mode
- 修图后得到了可迁移的纠偏规则

## capture 最小字段

建议至少包含：

- `schema_version`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `route`
- `initial_brief`
- `final_prompt`
- `image_prompt`
- `image_generation_id`
- `image_output_paths`
- `image_generation_dir`
- `result_status`
- `evaluation_summary`
- `failure_class`
- `what_worked`
- `what_failed`
- `correction_rule`
- `next_input`
- `promotion_hint`

推荐补充字段：

- `image_outputs`
  - 用对象数组记录每张图片的 `path`、`role`、`notes`
- `score`
  - 当前轮主观或量化评分
- `prompt_version`
  - 当你在持续迭代同一任务时，方便回看哪一轮 prompt 生效
- `legacy_use_case`
  - 只用于兼容旧 capture；新记录不再依赖它作为主分类

核心追踪关系要始终能回答：

1. 用户最初想要什么
2. 最终给生图接口的文本输入是什么
3. 具体生成了哪张图或哪批图
4. 这批图为什么算过线、不过线，或者只算中间稿
5. 下一轮该改 prompt 的哪一部分

## review / field note 也要承接 scene-profile

runtime v2 不只要求 capture 带上新字段，review queue 和 field note 也应保留：

- `schema_version`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `legacy_use_case`

否则 scene generalization 会只停在 capture，无法进入 review 和晋升阶段。

## Local Skill Reference Layer

`field note` 不是默认读取终点。

当前第一版已经把 `runtime -> local skill` 自动晋升落实为一个单独参考层：

1. review worker 先判断 capture 是否能升为 `field note`
2. 满足 local skill gate 的样本，再自动写入 `promoted/local-skill/active/`
3. 后续 `read_runtime_context.py` 默认优先返回 active local skill references
4. active 层超出容量上限时，旧条目会被自动转入 `promoted/local-skill/archive/`

这样区分开：

- `field note`
  - 是完整本地经验
- `local skill reference`
  - 是默认可读、压缩后的工作集

不要再把“field note 已存在”误认为“skill 默认能读到它”。只有进入 active local skill reference layer 的样本，才会自动影响默认读取链路。

## 自动晋升门槛

当前默认 gate 是：

- 先满足 `review -> field note`
- 再满足以下四项：
  - `score_ready`
  - `trigger_ready`
  - `intervention_ready`
  - `result_ready`

也就是：

- 有可描述的触发情境
- 有可描述的干预动作
- 有可描述的结果或下一步
- promotion score 达到 local skill 最低分

第一版默认分数来源仍复用现有 runtime policy：

- `repeat_signal`
- `transfer_signal`
- `specificity_signal`
- `future_judgment_signal`

## 默认读取链路

`read_runtime_context.py` 当前默认按下面顺序读取：

1. `local_skill_reference`
2. `field_note`
3. `capture`

并带预算保护：

- local skill refs 默认最多 `3`
- field notes 默认最多 `3`
- raw captures 默认最多 `5`

如果想临时跳过 local skill 层，可用：

```bash
python scripts/read_runtime_context.py --host generic --raw-only
```

## 容量治理与最小治理动作

第一版已经把最小治理工程化：

- `local_skill_working_set_ceiling`
  - 限制 active local skill refs 数量，避免无限累积
- `disable`
  - 把条目移出默认读取链路，但保留文件与 manifest
- `archive`
  - 把条目移出 active working set，用于容量治理或人工收缩
- `rollback`
  - 从 `promoted/local-skill/history/` 恢复上一个版本

注意：

- local skill 治理操作应串行执行
- `repo-candidates/` 目录继续保留，但这轮不会自动写入

## 建议命令

初始化 runtime：

```bash
python scripts/init_runtime_memory.py --host generic
```

写入一条 capture：

```bash
python scripts/write_runtime_capture.py --host generic --record-file /path/to/record.json
```

直接记录一次生图结果：

```bash
python scripts/log_image_generation.py \
  --host generic \
  --scene "ai-native-loop skill promo visual" \
  --domain-direction "project hero for an AI workflow skill" \
  --matched-profile social-creative \
  --support-tier accelerated \
  --legacy-use-case social-creative \
  --route direct \
  --initial-brief "为 ai-native-loop skill 生成宣传图" \
  --final-prompt "Asset goal: promotional hero visual ..." \
  --image-prompt "Promotional hero visual for the ai-native-loop skill ..." \
  --image-generation-id "019db439-cae9-7e73-ba86-39e56e279089" \
  --image-generation-dir "<generated-images-root>/019db439-cae9-7e73-ba86-39e56e279089" \
  --image-output-path "<generated-images-root>/019db439-cae9-7e73-ba86-39e56e279089/example.png" \
  --result-status review \
  --evaluation-summary "方向基本正确，但更像概念图，还不够像真实项目宣传物料"
```

读取相关经验：

```bash
python scripts/read_runtime_context.py \
  --host generic \
  --matched-profile ui-mockup \
  --support-tier accelerated \
  --limit 5
```

只看 raw capture 与 field note，跳过 local skill reference：

```bash
python scripts/read_runtime_context.py --host generic --raw-only
```

审阅待晋升样本：

```bash
python scripts/review_runtime_candidates.py --host generic
```

查看或治理 local skill references：

```bash
python scripts/manage_local_skill_references.py --host generic status
python scripts/manage_local_skill_references.py --host generic disable --slug some-note
python scripts/manage_local_skill_references.py --host generic archive --slug some-note
python scripts/manage_local_skill_references.py --host generic rollback --slug some-note
```

## 晋升原则

默认顺序：

1. raw capture
2. review queue
3. local field note
4. repo candidate

只有满足下面几项时，才值得晋升：

- 失败类型明确
- 纠偏动作明确
- 可迁移规律明确
- 不只是一次性的漂亮案例

如果要决定整个 scene profile 是否该从 `exploratory` 升到 `standard` 或 `accelerated`，不要只看这份文档，还要读取：

- `docs/profile-promotion-policy.md`

## Local Vs Repo Promotion Boundary

当前推荐的下一步边界如下：

1. `runtime -> local skill reference layer`
   - 可以自动晋升
   - 目标是让本地已验证 field note 自动进入后续 skill 执行时可读取的参考层
2. `runtime -> repo candidate -> GitHub public rule layer`
   - 不自动晋升
   - 当前也不自动写 `runtime/promoted/repo-candidates/`
   - 仍保留人工审核和后续手动判断

也就是说：

- 本地经验复利应自动化
- 公开规则升级应继续人工把关

这条边界成立之前，不要把“本地 field note 已存在”误认为“已经自动影响 skill 默认行为”。

## 建议工作流

每次生图都尽量按这个顺序走：

1. 结构化用户 brief
2. 产出最终 `image_prompt`
3. 调用生图接口
4. 记录生成目录和图片路径
5. 写一句本轮评估
6. 如果不过线，再补 failure class、correction rule、next input

这样 runtime 里沉淀下来的就不是“做过一张图”，而是“某个文本输入为什么会得到某种视觉反馈”。
