# Delivery Viability Checker MVP

## Purpose

这份文档描述当前最小可用的版式碰撞检查器方案。

目标不是做完整视觉理解，而是先把最常见、最致命的 overlay 失败前移成可执行 gate。

## Current Scope

当前 checker 已集成到：

- `scripts/apply_delivery_overlay.py`

它会在真正叠加前先检查：

1. 计划 overlay 的 box 集合
2. `protected_regions`
3. overlay footprint 是否超过默认容量预算

## Inputs

### Overlay Candidates

当前内置候选区：

- `title_panel`
- `footer_band`
- `qr_zone`
- `logo_zone`
- `badge_zone`

### Protected Regions

支持三种来源：

1. 版本元数据里的 `extra_metadata.protected_regions`
2. `--protected-region-file`
3. 重复传入的 `--protected-region name:x:y:width:height[:hard|soft]`

坐标支持：

- 绝对像素
- `0-1` 比例值

## Output

checker 会输出：

- `delivery_viability`
- `collision_risk`
- `continue_overlay_or_regenerate`
- `overlay_coverage_ratio`
- `hard_region_hits`
- `soft_region_hits`

默认判定：

- 命中硬保护区：`overlay_not_allowed_regenerate`
- overlay footprint 超预算：`overlay_not_allowed_regenerate`
- 仅命中软保护区：`overlay_allowed_with_limits`
- 无明显碰撞：`overlay_allowed`

## CLI Example

```bash
python scripts/apply_delivery_overlay.py \
  --bundle <bundle-root> \
  --title "主标题" \
  --supporting-line "补充说明" \
  --protected-region subject_core:0.22:0.18:0.42:0.48:hard \
  --protected-region ui_detail_band:0.10:0.62:0.28:0.16:soft
```

## Current Limits

- 还不做真实图像语义分割
- 还不自动识别人物、产品边缘或高噪点区
- 还不直接判断字号是否过小

所以它现在是：

- 一个稳定的 preflight gate
- 不是完整 layout intelligence

## Next Upgrade Targets

下一步优先补：

1. 文本密度与字号下限检查
2. 多尺寸 crop 下的 protected-region 复核
3. 更细的 overlay class 预算
