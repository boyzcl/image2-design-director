# Repair Playbook

## 目标

repair 模式下，不靠“再来一版”碰运气，而是按失败类型做最小纠偏。

## 总规则

1. 先给失败归类
2. 一轮只改 1 到 2 个关键变量
3. 明确 `Change only` 和 `Keep unchanged`
4. 不要同时大改构图、风格、场景、文案和主体

## 失败类型到修复动作

### 1. 产品图不够商品化

优先改：

- `Asset type`
- `Objective`
- `Style/medium`
- `Composition/framing`

推荐动作：

- 把用途钉死为 `landing page hero`、`ecommerce hero` 或 `catalog image`
- 把风格钉死为 `commercial product photography`
- 增加 `usable negative space`

### 2. 社媒图不像传播素材

优先改：

- `Asset type`
- `Audience/context`
- `Composition/framing`

推荐动作：

- 指定平台语境，例如 `LinkedIn feed creative`
- 明确保留文字区或安全留白
- 限制“像海报”的装饰性

### 3. UI mockup 不可信

优先改：

- 页面类型
- fidelity
- 信息层级

推荐动作：

- 指定为 `dashboard`、`settings page`、`mobile onboarding screen` 之一
- 减少组件数量
- 强化单一任务导向

### 4. App 素材图太像独立海报

优先改：

- `Objective`
- `Visual priorities`
- `Constraints`

推荐动作：

- 强调 “support the product interface”
- 压低装饰复杂度
- 加入 “system-friendly” 或 “product-compatible”

### 5. AI 味太重

优先改：

- 夸张风格词
- 不必要装饰物
- 过度戏剧化灯光

推荐动作：

- 去掉空泛高级词
- 换成更具体的资产用途和材质/版式约束
- 强调可信、克制、真实使用场景

### 6. 社媒图出现额外文案

优先改：

- `Text (verbatim)`
- `Constraints`
- `Change only`

推荐动作：

- 明确 `only show the exact headline text`
- 删除 badge、副标题和自动生成标签
- 保留平台语境，但不靠额外 copy 制造“营销感”

### 7. UI mockup 伪造品牌身份

优先改：

- `Constraints`
- `Change only`
- `Keep unchanged`

推荐动作：

- 补 `no brand name, no logo mark, no fake company identity`
- 把 header 改成 generic
- 保留布局和组件结构，不要因为一个 logo 问题整页重做

## 输出模板

repair 时可优先按这个格式组织：

```text
Failure class: <哪一类失败>
Why it failed: <一句话根因>
Change only: <本轮只改什么>
Keep unchanged: <必须保持什么>
Prompt delta: <本轮新增或替换的关键约束>
```
