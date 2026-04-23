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

## Runtime 应承接什么

runtime 现在至少应承接两层判断：

### 1. Scene Profile

- `domain_direction`
- `matched_profile`
- `support_tier`

### 2. Asset Contract

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

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
  - 本地晋升经验
- `promoted/local-skill/active/`
  - 默认会被读取链路优先读取的本地参考层
- `promoted/local-skill/disabled/`
  - 被人工禁用的本地参考
- `promoted/local-skill/archive/`
  - 因容量治理退出 active working set 的本地参考
- `promoted/local-skill/history/`
  - 本地参考层的回滚快照
- `promoted/repo-candidates/`
  - 值得考虑回流仓库规则层的候选
- `promoted/archive/`
  - 低价值或一次性样本
- `state/`
  - policy、ledger、manifest

## Capture 最小字段

建议至少包含：

- `schema_version`
- `session_id`
- `scene`
- `domain_direction`
- `matched_profile`
- `support_tier`
- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`
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

- `contract_alignment_result`
- `completion_readiness_result`
- `repair_class`
- `score`

## review / field note 也要承接合同字段

runtime 不只要求 capture 带上 asset contract 字段，review queue 和 field note 也应保留：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`

否则合同判断只停在 capture，无法进入 review 和晋升阶段。

## Runtime 现在应能回答什么

1. 用户最初想要什么资产
2. 当时系统理解的交付物合同是什么
3. 最终给模型的 prompt 是什么
4. 生成结果有没有满足那份合同
5. 如果失败，错在 prompt 还是错在合同判断

## 建议命令

```bash
python scripts/log_image_generation.py \
  --host generic \
  --scene "image2-design-director brand promo poster" \
  --domain-direction "brand promo poster for an AI design-director skill" \
  --matched-profile social-creative \
  --support-tier accelerated \
  --route direct \
  --initial-brief "给这个 skill 做一张完整可用的品牌宣传图" \
  --final-prompt "Deliverable: brand promo poster ..." \
  --image-prompt "Brand promo poster ..." \
  --image-generation-id "example-id" \
  --image-generation-dir "<generated-images-root>/example-id" \
  --image-output-path "<generated-images-root>/example-id/example.png" \
  --result-status review \
  --evaluation-summary "方向基本正确，但仍偏底图，不够像完整成品海报"
```

运行时记录里，还应补充：

- `deliverable_type = brand promo poster`
- `asset_completion_mode = complete_asset`
- `content_language = zh-CN`
- `allowed_text_scope = only project name + one Chinese slogan + one Chinese subtitle`
- `layout_owner = model`
- `acceptance_bar = directly usable poster`
- `contract_alignment_result = partially_aligned`
- `completion_readiness_result = workable_draft`
- `repair_class = contract_realign`

## 默认读取链路

`read_runtime_context.py` 当前默认按下面顺序读取：

1. `local_skill_reference`
2. `field_note`
3. `capture`

如果想临时跳过 local skill 层，可用：

```bash
python scripts/read_runtime_context.py --host generic --raw-only
```
