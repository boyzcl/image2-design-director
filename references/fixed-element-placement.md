# Fixed Element Placement

## Purpose

这份文档定义二维码、logo、badge、认证标识、价格角标等固定元素在交付阶段的放置规则。

它回答的是：

- 哪些元素默认不应由模型直接生成
- 放置时应优先保护什么
- 多个固定元素同时出现时如何分层
- 什么样的落位会破坏资产可信度

## Core Principle

### 1. Fixed Elements Are Precision Objects

二维码、logo、badge 不是装饰噪音，而是高精度交付对象。

它们默认应：

- 后处理加入
- 保持清晰
- 保持可识别
- 与主视觉保持稳定关系

### 2. Placement Should Feel Designed, Not Patched On

落位目标不是“能塞进去”，而是：

- 像原本就属于这套资产

### 3. Element Priority Must Be Explicit

当多个固定元素同时存在时，必须先排优先级。

不要临时拼贴。

## Element Classes

### Class A. Functional Elements

包括：

- QR code
- 下载入口码
- 可扫描券码

优先目标：

- 可用
- 清晰
- 易扫

### Class B. Identity Elements

包括：

- 主品牌 logo
- 合作方 logo
- lockup
- 认证标识

优先目标：

- 身份准确
- 比例正确
- clear space 足够

### Class C. Support Elements

包括：

- badge
- 价格角标
- 限时标签
- small claim chip

优先目标：

- 不抢主标题
- 不压主体焦点
- 小尺寸下仍可读

## Placement Rules

### 1. QR Codes Need Dedicated Quiet Space

二维码默认需要：

- 独立落位区
- 足够对比度
- 不被复杂背景干扰

不要把二维码放在：

- 纹理过强区域
- 主体上
- 画面最拥挤的角落

### 2. Logos Need Clear Space

logo 默认应放在：

- 明确的品牌位
- 边缘安全区
- 视觉层级稳定的位置

避免：

- 紧贴边界
- 与标题抢一级注意力
- 与二维码、badge 粘连

### 3. Badges Should Support, Not Dominate

badge、限时标签、认证标识默认不应变成主视觉焦点。

它们更适合：

- 辅助角位
- 标题附近但不贴死
- 主内容之外的支撑区

### 4. Protect The Main Axis

无论放什么固定元素，都应优先保护：

- 主体焦点
- 标题区
- 视线主轴

### 5. Respect Crop Behavior

如果要导出多个尺寸，固定元素应放在：

- 主要目标尺寸都能保留的位置

不要把关键元素压在容易被裁掉的边缘。

## Multi-Element Priority

当多个元素同时出现时，默认优先级建议为：

1. 主标题与一级信息
2. QR code 或主要行动入口
3. 主品牌 logo
4. 支撑 badge / 价格角标 / 次级标识
5. 合作方 logo 或补充认证元素

如果某任务要求不同优先级，必须在 task packet 里显式说明。

## Recommended Zones

下面不是硬模板，但可作为默认起点。

### QR Code

优先考虑：

- 右下
- 左下
- 独立信息区

### Logo

优先考虑：

- 左上
- 右上
- 底部品牌条

### Badge

优先考虑：

- 标题附近的辅助角
- 顶角小型标签位

## Red Flags

出现以下任一项时，当前 fixed-element placement 应视为不过线：

- 二维码一看就难扫
- logo 比主标题还抢
- badge 像临时贴纸
- 多个元素彼此挤压
- 元素一换尺寸就跑位
- 固定元素遮挡主体关键部分

## Hard Boundary

下面这些情况不能算交付完成：

- 使用模型伪造的二维码充当正式二维码
- 使用模型伪造的 logo 充当正式品牌元素
- 关键固定元素没有经过可用性或可识别性检查

## Delivery Contract

当任务涉及固定元素时，建议在交付计划里补齐：

```yaml
fixed_element_plan:
  qr_code_needed: true
  logo_needed: true
  badge_needed: false
  placement_priority:
    - "qr_code"
    - "primary_logo"
  reserved_zones:
    - ""
  crop_sensitive_elements:
    - ""
```

当前第一版执行入口：

```bash
python scripts/apply_delivery_overlay.py --bundle <bundle> --title "..." --qr-image <path> --logo-image <path>
```

它当前默认做的是：

- 从最新 `text_safe_visual` 读取
- 在 `top_title / top_left_logo / bottom_right_qr / bottom_cta_band` 这组保守 zone 上落版
- 先写 `overlay/applied/`
- 再登记新的 `delivery_ready_visual`

## Example Judgments

### Example 1. Recruitment Poster With QR Code And Logo

做法：

- 标题区与二维码区分离
- logo 放在上方或底部品牌位
- 二维码单独留 quiet zone

### Example 2. Hero Banner With Small Badge

做法：

- badge 只做辅助强调
- 不与主标题争一级层级

### Example 3. Social Card For Multiple Crops

做法：

- 把关键 logo 和二维码都放在多比例更安全的内边距区域

## Completion Checklist

- 当前固定元素是否都由后处理承担
- 每个元素是否有明确优先级
- 落位是否保护了主体和标题区
- 主要目标尺寸下元素是否都能保留
- 二维码、logo、badge 是否各自满足可用性与可识别性
