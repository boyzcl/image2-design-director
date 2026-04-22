# Delivery Bundle Contract v1

## Purpose

这份文档把 `raw_visual / text_safe_visual / delivery_ready_visual` 收成第一版可执行版本链。

它回答的是：

- bundle 目录该怎么长
- 三种状态各自最少要保留什么
- 命名和 lineage 怎么保持稳定
- 后续 overlay / size adaptation 应挂到哪里

一句话版本：

> delivery bundle 的职责，是把“已经成立的图”收成一个可回退、可追加、可继续交付的资产链，而不是一堆散落文件。

## Scope

这份 contract 当前只先解决第一层问题：

1. 三种状态的版本化
2. bundle manifest 与目录边界
3. 最小 CLI 入口
4. 给 fixed-element overlay / size adaptation 预留稳定挂点

当前已经有第一版执行层：

- `scripts/apply_delivery_overlay.py`
- `scripts/export_bundle_sizes.py`

但它们当前仍是：

- safe-first 的最小实现
- 主要服务 bundle 主链闭环
- 还没有做更重的智能 zone 推断或复杂版式系统

## Canonical Structure

一个 bundle 默认长成下面这样：

```text
delivery-bundles/<bundle_id>/
  bundle.json
  assets/
    raw_visual/
    text_safe_visual/
    delivery_ready_visual/
  overlay/
    pending/
    applied/
  size-adaptation/
    pending/
    exports/
  notes/
```

说明：

- `bundle.json`
  - bundle 主清单
  - 记录上下文、latest pointers、所有版本摘要
- `assets/<state>/`
  - 每个状态自己的版本文件与同名 `.json` metadata
- `overlay/`
  - 未来 overlay pass 的工作区
- `size-adaptation/`
  - 未来 size fan-out 的工作区与导出区
- `notes/`
  - 交付说明或人工判断补充

## State Contract

### 1. `raw_visual`

最少保留：

- 实际图像文件
- 原来源路径
- transition label
- 可选 scene / domain context

它代表：

- 模型刚生成或刚选中的可评估底图

### 2. `text_safe_visual`

除了 `raw_visual` 的基础字段，还应至少开始补齐：

- `reserved_zones`
- `overlay_mode`
- 需要承载的 `fixed_elements`
- 主要 `target_sizes`

它代表：

- 文本区、留白区、落位区已经稳定到可以承接后续交付动作

### 3. `delivery_ready_visual`

除了前两态字段，还应至少补齐：

- 当前 transition 是哪类交付动作形成的
- 最终要服务的 fixed elements / sizes 是否已明确
- 可选额外 metadata 用来记录 overlay / export 结果

它代表：

- 当前任务下已经形成可直接交付的版本

## Naming Rules

每个 state 独立递增编号：

- `raw_visual-v001`
- `raw_visual-v002`
- `text_safe_visual-v001`
- `delivery_ready_visual-v001`

文件名默认使用：

- `<version_id><original_suffix>`

例如：

- `raw_visual-v001.png`
- `text_safe_visual-v001.png`
- `delivery_ready_visual-v001.png`

这样可以保证：

- state 一眼可见
- 同 state 可稳定迭代
- 后续 overlay / size adaptation 不会覆盖母版

## Manifest Shape

`bundle.json` 的核心字段如下：

```json
{
  "schema_version": 1,
  "bundle_id": "event-signup-poster",
  "asset_name": "AI Prompt Clinic Event Signup Poster",
  "context": {
    "scene": "event signup poster base for an AI image prompt clinic",
    "domain_direction": "delivery-heavy event signup poster",
    "matched_profile": "none",
    "support_tier": "standard"
  },
  "latest_versions": {
    "raw_visual": "raw_visual-v001",
    "text_safe_visual": "text_safe_visual-v001",
    "delivery_ready_visual": null
  },
  "versions": [
    {
      "version_id": "text_safe_visual-v001",
      "state": "text_safe_visual",
      "parent_version_id": "raw_visual-v001",
      "transition": "promote_text_safe",
      "delivery_plan": {
        "overlay_mode": "text_safe_only",
        "reserved_zones": ["top_title", "bottom_right_qr"],
        "fixed_elements": ["qr_code", "primary_logo"],
        "target_sizes": ["1080x1080", "1920x1080"]
      }
    }
  ]
}
```

## Version Lineage Rules

默认 lineage 规则如下：

1. `raw_visual` 可以没有 parent
2. 第一个 `text_safe_visual` 默认继承最新 `raw_visual`
3. 第一个 `delivery_ready_visual` 默认继承最新 `text_safe_visual`
4. 同一 state 的后续修订，默认继承该 state 当前 latest version

这样做的目的不是强行限制流程，而是让默认路径收束为：

- `raw -> text_safe -> delivery_ready`

同时允许：

- `text_safe` 内部多次微调
- `delivery_ready` 内部多次落版修订

## CLI Entry

当前最小入口：

- `python scripts/manage_delivery_bundle.py init`
- `python scripts/manage_delivery_bundle.py add-version`
- `python scripts/manage_delivery_bundle.py show`
- `python scripts/apply_delivery_overlay.py`
- `python scripts/export_bundle_sizes.py`

### Example 1. Seed A Bundle

```bash
python scripts/manage_delivery_bundle.py init \
  --bundle-root tmp/example-output/delivery-bundles/event-signup-poster \
  --bundle-id event-signup-poster \
  --asset-name "AI Prompt Clinic Event Signup Poster" \
  --scene "event signup poster base for an AI image prompt clinic" \
  --domain-direction "delivery-heavy event signup poster" \
  --state raw_visual \
  --source-image tmp/example-output/agent-top-permille-poster.svg.png \
  --transition init_bundle \
  --target-size 1080x1080
```

### Example 2. Promote To `text_safe_visual`

```bash
python scripts/manage_delivery_bundle.py add-version \
  --bundle tmp/example-output/delivery-bundles/event-signup-poster \
  --state text_safe_visual \
  --source-image tmp/example-output/agent-top-permille-poster.svg.png \
  --transition promote_text_safe \
  --overlay-mode text_safe_only \
  --reserved-zone top_title \
  --reserved-zone bottom_right_qr \
  --reserved-zone bottom_cta_band \
  --fixed-element qr_code \
  --fixed-element primary_logo \
  --target-size 1080x1080
```

### Example 3. Inspect Latest Chain

```bash
python scripts/manage_delivery_bundle.py show \
  --bundle tmp/example-output/delivery-bundles/event-signup-poster
```

### Example 4. Apply Fixed-Element Overlay

```bash
python scripts/apply_delivery_overlay.py \
  --bundle tmp/example-output/delivery-bundles/event-signup-poster \
  --title "AI 提示词门诊开放报名" \
  --supporting-line "从模糊 brief 到可交付资产的实战工作坊" \
  --date-text "2026.05.08 Fri 19:30" \
  --cta-text "立即报名" \
  --logo-image tmp/example-output/assets/test-logo.png \
  --qr-image tmp/example-output/assets/test-qr.png
```

### Example 5. Export Size Variants

```bash
python scripts/export_bundle_sizes.py \
  --bundle tmp/example-output/delivery-bundles/event-signup-poster \
  --target-size 1080x1350 \
  --target-size 1920x1080 \
  --mode safe_pad
```

## How Overlay Should Attach Next

当前 fixed-element overlay 脚本已经按下面这条原则实现：

- 不直接覆盖 `text_safe_visual` 母版
- 先在 `overlay/applied/` 产出 working file
- 再登记新的 `delivery_ready_visual`

也就是说，当前脚本已经把这条规则从文档变成了执行路径。

推荐做法：

1. 从 bundle 的 latest `text_safe_visual` 读取输入
2. 在 `overlay/pending/` 或 `overlay/applied/` 记录工作文件
3. 生成结果后，回写为新的 `delivery_ready_visual` version
4. 在 version metadata 或 extra metadata 中记录：
   - overlay inputs
   - fixed element paths
   - placement notes

也就是说：

- overlay 是 transition
- `delivery_ready_visual` 是资产状态

不要把两者混成同一个概念。

## How Size Adaptation Should Attach Next

当前 size adaptation 脚本已经按这个方向实现：

- 默认从最新 `delivery_ready_visual` 读取
- 默认使用 `safe_pad`
- 导出写到 `size-adaptation/exports/<source_version>/`
- 并把 export run 记回 `bundle.json`

size adaptation 默认应从 `delivery_ready_visual` 往外扇出，而不是直接回头污染 `raw_visual`。

推荐做法：

1. 读取 latest `delivery_ready_visual`
2. 在 `size-adaptation/pending/` 记录 crop / padding / export plan
3. 把最终导出放到：
   - `size-adaptation/exports/<delivery_ready_version_id>/`
4. 如 fan-out 结果本身成为新的主交付版，再登记新的 `delivery_ready_visual`

这样可以保持：

- 母版稳定
- 导出版可追溯
- 后续回改 overlay 或尺寸时不需要回忆“到底哪张是对的”

## Current Boundary

这份 v1 contract 还不承诺：

- 自动识别 safe zones
- 自动理解任意复杂版式结构
- 自动做内容感知 crop 决策

它当前承诺的是：

- 三态版本链能被明确创建
- 命名、目录和 latest pointers 稳定
- overlay / size adaptation 有统一落点
- overlay / size adaptation 已有最小可执行脚本

这已经足够作为第一版 delivery bundle / versioning 基座。
