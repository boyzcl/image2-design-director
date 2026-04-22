# YouMind GPT Image 2 Curated Examples

## Source

- source page: `https://youmind.com/zh-CN/gpt-image-2-prompts`
- capture date: `2026-04-22`
- public release note: 公开仓库保留的是提炼后的例子与方法总结，不再附带第三方页面整页快照。

## Why This File Exists

这份文件不是简单搬运整站内容，而是从页面中挑出几类有代表性的提示词范式，方便后续作为写法参考。

重点关注的不是题材本身，而是：

- 它们怎么组织信息
- 怎么把视觉目标说清
- 怎么把复杂版式拆成可执行结构

## Example 1. 产品爆炸视图海报

title:

- `VR 头显爆炸视图海报`

pattern:

- 用 JSON 结构化描述复杂商业海报
- 把任务拆成 `type / subject / style / background / header / layout`
- 在 `layout` 里进一步细分 `centerpiece / callout_labels / footer`

why it matters:

- 适合高结构、高信息量的产品海报
- 同时照顾主视觉、标注、标题和底部文案

signals:

- 不只是说“做一张炫酷爆炸图”
- 而是把“组件数量、左右标注、底部文案块”全部写死

## Example 2. 手绘地图信息图

title:

- `手绘城市美食地图`

pattern:

- 用 `title_section / border / layout / sections / centerpiece / extras` 组织复杂插画地图
- 把每个信息区的数量和标签都列出来

why it matters:

- 适合需要大量对象、标签、地标和图例的插画信息图
- 强调“区域拆分 + 列表枚举”

signals:

- 不依赖抽象氛围词
- 主要靠“区域、数量、元素、标签”驱动结果

## Example 3. 电商直播 UI 样机

title:

- `电商直播 UI 样机`

pattern:

- 先给真人主体与背景
- 再把 UI overlay 分成 `top_header / mid_left_gifts / bottom_left_chat / product_card / bottom_bar`
- 每个区块都写入精确文案与数字

why it matters:

- 说明这类复杂 UI prompt 的核心不是“像直播界面”
- 而是把界面拆成可数的 overlay 区块

signals:

- 对信息密度高的界面，必须明确区域和元素职责

## Example 4. 演化时间轴信息图

title:

- `3D 石阶演化信息图`

pattern:

- 明确 `instruction`：基于 `REFERENCE_0` 做风格与结构变换
- 保留原始结构关系，再做材质和表现层升级
- 在 `layout` 里写主标题、侧边栏、底部中心、中心主体与 notable elements

why it matters:

- 这是“基于参考图重构”的强范式
- 不是完全从零描述，而是“参考结构 + 局部升级”

signals:

- `REFERENCE_0`
- `transform`
- `replace`
- `upgrade`

## Example 5. 品牌形象与周边设计项目

title:

- `动漫角色品牌形象与周边项目`

pattern:

- 从 `theme / character / branding / layout` 出发
- 在 `layout.sections` 中逐区定义：
  - 页眉横幅
  - 产品包装
  - 宣传海报
  - 网页横幅
  - 社媒资料样机
  - 周边商品系列

why it matters:

- 适合“一个角色，多种品牌触点”的项目化输出
- 本质上是“品牌系统 prompt”，不是单图 prompt

signals:

- 同一世界观同时驱动多个落点
- 主题、角色、标识与版式共同约束

## Example 6. UI 设计系统演示项目

title:

- `浅色模式 UI 设计系统项目`

pattern:

- 把设计系统展示页拆成：
  - 色彩
  - 渐变
  - 排版
  - 图标
  - 按钮
  - 导航
  - 组件
  - 网页
  - 移动应用

why it matters:

- 这类 prompt 的关键不是美学词，而是“设计系统模块清单”
- 很适合转成 `section-based` 写法

signals:

- 对复杂 UI 展示页，模块化列举比形容词更重要

## Example 7. 2x2 广告横幅网格

title:

- `4 格日式数字广告横幅网格`

pattern:

- 用统一母版结构，分成 4 个象限
- 每个象限有独立 `theme / subject / elements / text_labels / badges / icons`

why it matters:

- 适合一图多变体、同模板多广告位的任务
- 强调“网格结构 + 象限差异化”

signals:

- 同一视觉系统下的多主题广告组合
- 每格内容单独定义，但共享总布局

## Example 8. 落地页案例研究

title:

- `深色模式病毒式营销案例研究落地页`

pattern:

- 用 `sections` 来组织落地页
- 每段再定义 `layout + content`
- 数据、图表、社证、CTA 都被视为不同内容模块

why it matters:

- 对 landing page 或 case study 页面，最有效的写法是“按 section 建模”
- 不是笼统地让模型自己想页面结构

signals:

- `hero`
- `strategy`
- `performance`
- `keys_to_success`
- `social_proof`
- `cta`

## Example 9. 动漫动作场景

title:

- `动漫武术对决`

pattern:

- 不用 JSON
- 直接用高密度自然语言描述角色、动作、服装、能量轨迹、环境、镜头和光影

why it matters:

- 说明不是所有 prompt 都适合结构化 JSON
- 对单张动作插画，连续叙述式 prompt 反而更自然

signals:

- 前景主体
- 另一角色的位置与动作
- 服装细节
- 动作特效
- 场景环境
- 低角度光影

## Cross-Example Takeaways

这些样本里最稳定的共性是：

1. 高结构任务偏向 JSON 或 section-based 写法
2. 单图叙事插画更适合自然语言连续描述
3. 好 prompt 很少只写风格，通常会同时写：
   - 任务类型
   - 主体
   - 结构
   - 区域
   - 文案
   - 元素数量
4. 很多 prompt 采用参数化写法：
   - `{argument name="..." default="..."}`
5. 优秀 prompt 往往先定义信息架构，再定义美学表现
