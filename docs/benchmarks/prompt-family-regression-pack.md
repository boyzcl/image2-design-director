# Prompt Family Regression Pack

## Purpose

这份文档把当前这次 prompt 体系融合后的下一轮工作，收成一份可直接执行的验证包。

它不是再解释一遍 prompt 规范，而是回答：

- 现在项目真正卡在哪一环
- 下一轮最该做什么
- 应该如何验证这次 prompt 写法升级是否真的成立

## Diagnosis Card

- `loop_stage`: `re-input`
- `intervention_level`: `medium`
- `primary_block`: prompt family、text layer 和 assembly 规则已经写进 skill，但 benchmark surface 还没有完整覆盖这些变化
- `risk_note`: 如果继续补文档而不先验证，项目会把“写法升级”误当成“默认能力已稳定”

## Task Packet

- `objective`: 把 prompt-system 融合结果变成一组可执行的 benchmark regression packet，而不是停留在文档对齐层
- `current_state`: `SKILL.md`、`prompt-schema.md`、`prompt-assembly.md`、`sample-prompts.md` 已经完成对齐；但原 benchmark 集没有专门覆盖 `directed natural language`，run template 也没有显式记录 `prompt_family` 和 `text_layer_mode`
- `artifacts`:
  - `SKILL.md`
  - `references/prompt-schema.md`
  - `references/prompt-assembly.md`
  - `references/sample-prompts.md`
  - `docs/benchmarks/benchmark-scenarios.md`
  - `docs/benchmarks/benchmark-run-template.md`
- `constraints`:
  - 不声称真实 benchmark 已经跑完
  - 不伪造图像结果或分数
  - 保持现有 benchmark 文档结构可持续扩展
- `success_signal`:
  - benchmark surface 覆盖 4 种默认 prompt family
  - run template 能显式记录 `prompt_family`、`text_layer_mode` 和 `final_prompt`
  - 下一轮可以直接开始真实 baseline vs candidate benchmark
- `next_checkpoint`: 基于本 pack 跑第一轮真实 prompt-family regression run，并留下实际图像输出与评分

## Feedback Attribution Card

- `signal`: prompt 规范已经融合，但“下一轮该怎么验证”仍然不够明确，导致执行闭环在文档层停住
- `failure_class`: `decision failure`
- `root_cause`: 原执行路线在 `m4_benchmark_loop` 完成后收束得太早，没有为后续 prompt-system 级改动预留专门的 validation loop
- `keep`: 已经完成的 prompt family 定义、text layer 规则、参数化模板和失败复盘结论
- `change`: 给 benchmark 增加 prompt-family coverage、补齐 onboarding narrative 场景、让 run template 能记录 prompt-family 证据链

## Re-input Packet

- `preserve`:
  - 新的 prompt family 划分
  - “先任务、后结构、再风格”
  - “文本层是正式设计层”
  - 长中文文本是高风险信号，不是 `direct_output` 硬挡板
- `discard`:
  - 默认认为现有 5 个 benchmark 场景已足以验证 prompt-system 改动
  - 只看 `image_prompt`，不显式记录 `final_prompt` 与 text-layer strategy
- `add_context`:
  - prompt family coverage matrix
  - `bm_app_asset_onboarding_scene`
  - `prompt_family_under_test`
  - `text_layer_mode_under_test`
- `change_request`: 下一轮按 4-scenario prompt-system regression pack 跑真实 baseline vs candidate，对每个 family 至少保留一条可回溯记录
- `next_checkpoint`: 完成第一份真实 benchmark run 文档，并判断新 prompt system 是 `keep`、`adjust` 还是 `partial rollback`

## Change Under Test

这次要验证的不是某一条 sample prompt，而是默认 prompt 写法的整体切换：

- 从轻量字段表，升级到按 prompt family 选写法
- 从“字段写全”升级到“task -> structure -> text -> style -> constraints”的装配顺序
- 从“文字只是附带限制”升级到“text layer 是正式设计层”
- 从“模板示例”升级到“参数化模板 + resolved example”

## Baseline vs Candidate

### Baseline

- 使用融合前的轻量字段写法
- 默认不显式记录 `prompt_family`
- text layer 往往只体现在 `Constraints` 或零散字段里
- 对单图叙事任务缺少明确的自然语言写法判断

### Candidate

- 使用新的 prompt-family 选择逻辑
- 显式写出 `prompt_family`
- 显式写出 `text_layer_mode`
- 使用 `prompt-schema.md` + `prompt-assembly.md` + `sample-prompts.md` 的组合骨架

## Regression Surface

默认先跑下面 4 个场景：

| Scenario | Prompt Family | Why It Is Required |
|---|---|---|
| `bm_social_creative_launch` | `structured / section-based poster` | 验证海报结构、标题区、text layer 直出策略 |
| `bm_project_hero_repo` | `hybrid structured hero` | 验证单主体商业主视觉和 text-safe hero 留白 |
| `bm_ui_mockup_credibility` | `structured / section-based UI` | 验证 UI 模块拆分、品牌中性和信息密度控制 |
| `bm_app_asset_onboarding_scene` | `directed natural language` | 验证单图叙事类 app asset 是否真正切换写法 |

如果这轮还要验证 repair，则在下面两个场景里至少选一个追加第二轮：

- `bm_social_creative_launch`
- `bm_ui_mockup_credibility`

## Run Order

建议顺序：

1. `bm_project_hero_repo`
2. `bm_ui_mockup_credibility`
3. `bm_social_creative_launch`
4. `bm_app_asset_onboarding_scene`
5. 按需要追加 repair pass

这样安排的原因：

- 先跑最稳定、最容易看出 prompt family 是否真的切换成功的场景
- 再跑 text layer 更敏感、风险更高的海报场景
- 最后再验证自然语言叙事场景

## Evidence Contract

每个场景至少保留：

- `prompt_family_under_test`
- `text_layer_mode_under_test`
- `baseline_final_prompt`
- `candidate_final_prompt`
- `baseline_image_prompt`
- `candidate_image_prompt`
- `baseline_generation_id`
- `candidate_generation_id`
- `baseline_image_output_ref`
- `candidate_image_output_ref`
- scorecard 评分
- 一句保留 / 放弃 / 下一轮改什么

## Pass Rule

这次 regression pack 成立，不等于全部场景都必须直接 `pass`。

最低通过标准是：

1. 4 个 prompt family 都有实际验证面
2. 至少 2 个场景出现清楚改善
3. 没有新增严重回归
4. 至少能明确指出哪个 family 仍需调整

## Execution Decision

当前最高杠杆动作不是继续扩 prompt 文档，而是：

1. 先把 benchmark surface 对齐到 prompt family
2. 再跑第一轮真实 regression
3. 最后再决定哪些 prompt family 规则值得进一步固化

## Immediate Outcome Of This Packet

本次已直接执行的内容：

- 扩 benchmark scenarios，使其覆盖 `directed natural language`
- 升级 benchmark run template，使其显式记录 `prompt_family`、`text_layer_mode` 和 `final_prompt`
- 打开一个专门服务 prompt-system 的 regression pack

尚未执行但已明确打开的下一步：

- 跑第一轮真实 prompt-family benchmark run
