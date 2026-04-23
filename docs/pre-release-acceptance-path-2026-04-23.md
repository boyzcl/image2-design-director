# Pre-Release Acceptance Path 2026-04-23

## Purpose

这份文档定义本轮升级上线前的最短验收路径。

## Step 1. Document Consistency Check

确认下面内容已经一致：

- `SKILL.md`
- `references/intake-schema.md`
- `references/task-packet.md`
- `references/strategy-decision-tree.md`
- `references/information-reliability-gate.md`
- `references/representation-modes.md`
- `references/delivery-viability-gate.md`
- `references/quality-bar.md`
- `references/scorecard.md`

通过标准：

- 四层能力在入口、主流程、评分和 repair 里表述一致

## Step 2. Tooling Sanity Check

检查：

- `scripts/apply_delivery_overlay.py --help`
- `scripts/log_image_generation.py --help`

通过标准：

- overlay checker 参数可见
- runtime logging 支持 reliability / representation / viability / accountability 字段

## Step 3. Run Minimum Benchmark Pack

执行：

- `bm_pure_visual_brand_asset`
- `bm_low_density_text_info_visual`
- `bm_high_fact_sensitivity_data_visual`
- `bm_overlay_delivery_viability`

通过标准：

- 每组都有清晰 gate output
- 至少一组高事实敏感任务正确转向 hybrid / deterministic
- 至少一组 overlay 冲突被 checker 拦住

## Step 4. Scorecard Review

每条 benchmark run 必须补齐：

- `information_reliability`
- `representation_fit`
- `delivery_integrity`
- `misleading_risk`
- `hard_fail_reason`

通过标准：

- 不再只看“像不像设计图”

## Step 5. Installed Copy Sync Check

确认 repo 与 installed copy 的下列内容已同步：

- `SKILL.md`
- `references/`
- `scripts/`

通过标准：

- 宿主实际使用的 skill 已经加载新架构

## Release Decision

只有当下面条件同时成立时，才应视为 release-ready：

1. 四层能力已进入主链路文档
2. overlay checker 已可执行
3. benchmark pack 已跑完
4. scorecard 已包含 reliability / viability / accountability
5. installed copy 已同步
