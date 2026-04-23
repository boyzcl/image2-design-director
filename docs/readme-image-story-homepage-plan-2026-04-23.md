# README Image Story Homepage Plan 2026-04-23

## 目标

这份方案把现有 `README.md` 从“说明型首页”重组为“图片叙事型首页”。

目标不是减少信息，而是改变信息的进入方式：

- 先让用户被画面吸引
- 再让用户一眼理解这个 skill 到底解决什么问题
- 再让用户通过少量文字抓住机制
- 最后把详细协议、安装、结构说明下沉到文档层

一句话版本：

> 首页不再主要靠长段文字解释 `image2-design-director`，而是通过一组连续图片，把“先做对资产，再把资产做成可交付”的故事讲出来。

## 推荐方向

推荐做成：

- `image-first README homepage`
- 不是“纯海报墙”
- 而是“图片主叙事 + 极少量高密度文字锚点”

不建议首页做成完全无文字的纯图片页。原因很简单：

- GitHub README 仍然需要让用户快速扫描定位
- 安装、入口、能力边界这类信息仍然更适合文本
- 如果首页全是图，用户知道“很强”，但不一定知道“怎么用”

所以最优解不是：

- `all-image`

而是：

- `70% image`
- `30% text`

也就是：

- 图片负责吸引、演示、定调、讲机制
- 文本负责命名、解释、导航、降低理解成本

## 首页叙事主线

整套首页建议围绕一条主线展开：

1. 普通生图 agent 常常“会出图，但没先做对图”
2. `image2-design-director` 先收交付物合同，而不是先堆 prompt
3. 它会在不同任务状态里做判断和分流
4. 它不只产出图片，还把图片推进成可交付资产
5. 它会把每轮经验沉淀成下一轮的判断优势

如果把这条主线翻译成首页情绪，应该是：

- 第一眼：这不是又一个 prompt enhancer
- 第二眼：它像一个会判断的设计系统
- 第三眼：我知道它如何介入我的任务了

## 首页视觉语言建议

这套图片不建议走：

- 通用 AI 紫色霓虹
- 泛科技抽象流体
- 传统 SaaS 扁平插画

更适合的方向是：

- `editorial system poster`
- `product operating board`
- `design review wall`

建议统一视觉特征：

- 背景以暖白、浅灰、纸感米白为主
- 文字和骨架以炭黑、深灰为主
- 强调色使用信号红、琥珀橙或电蓝中的一种到两种
- 局部加入高对比裁切、标尺、标签、箭头、分镜编号
- 图片风格介于“产品海报”和“系统说明图”之间

这个方向的好处是：

- 能体现“设计导演”而不是“模型炫技”
- 既适合讲故事，也适合讲机制
- 放在 GitHub README 上更像一个成熟产品，而不是一组随意示例图

## 哪些信息应该保留为文字

下面这些内容不应该硬塞进图里，文字更高效：

- 仓库一句话定位
- 顶部导航链接
- 显式调用方式 `$image2-design-director`
- 安装方式
- 仓库结构
- 核心文档入口
- 当前边界和非目标

下面这些内容最适合“图 + 一句说明”：

- 为什么普通生图流程会失败
- `asset contract` 六要素
- `direct / brief-first / repair / contract_realign`
- 成品图、底图、交付细化的差异
- 质量验收维度
- 运行时经验复利

下面这些内容最适合“纯视觉主导”：

- 首页 hero
- Skill 的人格与气质
- 从模糊需求到可交付资产的推进感
- “会生成”与“会判断”的差异
- 多场景覆盖能力的广度

## 建议的 README 首页结构

建议首页分成 9 个区块，其中 6 到 8 个区块是图片主导。

### Section 1. Hero

用途：

- 让用户在 3 秒内知道这不是普通生图 skill

形式：

- 一张强主视觉
- 配 1 句标题 + 1 句副标题 + 顶部链接

### Section 2. Problem

用途：

- 展示没有这个 skill 时，生图 agent 为什么经常跑偏

形式：

- 一张“错误资产墙”式图片
- 配极短文字

### Section 3. Core Turn

用途：

- 讲清它的核心转折不是“更会写 prompt”
- 而是“先对齐交付物合同”

形式：

- 一张系统转盘或控制面板式图片

### Section 4. Routing

用途：

- 展示它不是一条直线，而是会判断任务状态

形式：

- 一张四分流视觉图

### Section 5. Assembly

用途：

- 展示它如何把模糊需求变成结构化生成输入

形式：

- 一张分层装配图

### Section 6. Acceptance

用途：

- 展示它判断的是“能不能用”，不只是“漂不漂亮”

形式：

- 一张设计评审板式图片

### Section 7. Delivery

用途：

- 展示它能把主视觉推进成真正的交付资产

形式：

- 一张多尺寸、多版本、多元素落位的资产展开图

### Section 8. Compounding

用途：

- 展示运行时记忆和经验复利

形式：

- 一张“单轮执行 -> 本地 capture -> pattern 升级”的闭环图

### Section 9. CTA

用途：

- 把用户带回 README 的可执行入口

形式：

- 文本为主，配一张轻量收尾图或缩略横幅

## 首页图片分镜方案

下面这套分镜是建议的一期版本。建议先做 8 张。

| 编号 | 区块 | 这一张图负责讲什么 | 更适合图还是字 | 建议保留的文字 |
|---|---|---|---|---|
| 01 | Hero | 这是一个设计导演层，不是提示词扩写器 | 图主导 | 标题 + 副标题 |
| 02 | Problem | 普通生图常见失败：资产类型错、成品度错、语言错、方向错 | 图主导 | 4 个短标签 |
| 03 | Asset Contract | 先收清交付物合同的 6 个关键问题 | 图主导 | 6 个字段名 |
| 04 | Route | 任务会被分流到 4 条路径 | 图主导 | `direct` 等短标签 |
| 05 | Prompt Assembly | 需求不是被扩写，而是被装配 | 图主导 | 4 到 6 个层名 |
| 06 | Acceptance | 验收标准是“像对的资产且能直接用” | 图主导 | 4 个评分维度 |
| 07 | Delivery Ops | 一张图如何扩成真正可交付资产 | 图主导 | 尺寸 / 文案 / 二维码等短标签 |
| 08 | Runtime Memory | 每次任务都为下一次任务提供判断优势 | 图主导 | `capture -> review -> pattern` |

## 每张图的详细定义

### 01. Hero: The Design Director Layer

目标：

- 把 skill 的身份一次讲透

推荐画面：

- 主体不是单张图片成品
- 而是一块被拆解中的“视觉任务控制台”
- 左边是模糊需求碎片
- 中间是一个被点亮的判断层
- 右边是成品级资产预览

画面关键词：

- 设计导演台
- 资产控制台
- 大号标题区
- 像产品首页 hero，不像海报宣传画

建议标题：

- `Direct Images Like a Design Director`

建议副标题：

- `image2-design-director aligns the asset before it optimizes the generation.`

为什么用图：

- 这是身份建立，不是机制解释
- 必须先建立高级感和产品感

### 02. Problem: What Goes Wrong Without It

目标：

- 让用户看到这个 skill 解决的是“错做资产”的问题

推荐画面：

- 四格错误案例墙
- 同一个需求被错误地做成不同方向
- 每格贴一个失败标签

四个失败标签建议：

- `Wrong Asset Type`
- `Half-Finished`
- `Language Drift`
- `Patch Instead Of Realign`

为什么用图：

- README 里这些问题目前是文字说明
- 但“跑偏”这件事最适合视觉对比

### 03. Asset Contract: The Six Questions

目标：

- 讲清“先收合同”是全 Skill 的核心机制

推荐画面：

- 像一块设计任务接单面板
- 六个卡槽逐个点亮
- 中间突出 `deliverable_type`
- 其他字段围绕展开

六个字段建议直接上画面：

- `deliverable_type`
- `asset_completion_mode`
- `content_language`
- `allowed_text_scope`
- `layout_owner`
- `acceptance_bar`

为什么用图：

- 这不是安装说明，而是价值主张
- 应该被记住，而不是被略读

### 04. Route: Four Ways To Run A Task

目标：

- 把它的智能分流机制讲清楚

推荐画面：

- 中心节点是 `asset contract confirmed`
- 向四个方向分流
- 每条路径对应一种视觉节奏

四条路径建议：

- `direct`
- `brief-first`
- `repair`
- `contract_realign`

为什么用图：

- 分流是这个 skill 与普通 prompt 流程的关键差异
- 用图能一眼懂，用段落要读很久

### 05. Prompt Assembly: From Brief To Structured Prompt

目标：

- 展示这个 skill 并不是把一句话扩写长

推荐画面：

- 一张分层爆炸图
- 从 brief、context、layout、text、style、constraints 逐层装配
- 最后落到 `image prompt`

建议层级标签：

- `task goal`
- `subject and scene`
- `layout structure`
- `text layer`
- `style system`
- `hard constraints`

为什么用图：

- “装配”是比“扩写”更强的视觉隐喻

### 06. Acceptance: Not Just Pretty, But Usable

目标：

- 强化“可验收资产”这个差异点

推荐画面：

- 一块设计评审看板
- 中间是一张看起来不错的图
- 四周是验收标尺、打分卡、通过与退回标记

建议打在图上的 4 个验收维度：

- `asset type fidelity`
- `completion readiness`
- `language alignment`
- `contract alignment`

为什么用图：

- 这是“设计评审感”，不是文字教程感

### 07. Delivery Ops: From One Visual To Shippable Assets

目标：

- 讲清它不只负责生成图，还负责走向交付

推荐画面：

- 中间一个主视觉
- 周围展开成 `16:9`、`4:5`、`1:1`
- 旁边还有标题、二维码、logo、CTA 的落位示意

建议图上短标签：

- `multi-size`
- `text refinement`
- `QR placement`
- `logo and badge`

为什么用图：

- 这是最容易被用户理解为“真能用”的一张

### 08. Runtime Memory: Every Run Makes The Next Run Better

目标：

- 展示这个 skill 的第二层闭环

推荐画面：

- 一个从单次任务卡片出发的循环系统
- `capture`
- `review`
- `field note`
- `pattern`
- `future run`

为什么用图：

- 经验复利如果只靠文字讲，会显得抽象
- 用系统图更有“这是个长期可进化产品”的感觉

## 哪些 README 原内容应下沉

以下内容建议从首页主叙事里挪到折叠后或 docs：

- “它适合什么”的长列表
- “我们支持什么”的完整能力表
- 大段逐步说明
- 长串常见请求示例
- 全量核心文档列表

这些内容不是不重要，而是：

- 对第一次进入首页的人来说太像说明书
- 会削弱图片叙事的节奏

建议保留为：

- 首页中段的一小段摘要
- 以及跳转到 `docs/README.md` 的入口

## README 首页建议保留的文字骨架

首页即使改成图片主导，也建议至少保留下面这些文字块。

### 顶部一句话

建议：

`A design-director layer for image-generating agents. It aligns the asset contract before generation, and pushes outputs toward shippable visual assets.`

### 顶部导航

- `Skill`
- `Docs`
- `Architecture`
- `Runtime Memory`
- `Release Readiness`

### 中段两句解释

建议保留一段短说明：

`Most image agents do not fail because they cannot generate images. They fail because they optimize too early, before confirming what asset should be made. image2-design-director adds that missing judgment layer.`

### 底部 CTA

建议保留：

- 如何调用
- 如何安装
- 去哪里看完整协议

## 两个 README 版本建议

### Version A. 纯图片首页

结构：

- 顶部 hero 图
- 连续 6 到 8 张图
- 最后只留极少链接和安装入口

优点：

- 冲击力最强

缺点：

- GitHub 可扫描性较弱
- 对首次理解成本更高

适用：

- 对外展示页
- 作品集式 landing page

### Version B. 图片 + 文本首页

结构：

- Hero 图 + 两句定位
- 每张图下配 1 句解释
- 安装、入口、文档导航保留为文本

优点：

- 传播力和可用性平衡最好

缺点：

- 需要更克制的排版

适用：

- GitHub README 首页
- 当前仓库的首选方案

结论：

- `Version B` 适合作为第一版正式落地
- `Version A` 可以作为后续站外宣传页或 README 的实验版本

## 一期出图优先级

建议不要一口气做所有图片，先做最关键的 6 张：

1. `Hero`
2. `Problem`
3. `Asset Contract`
4. `Route`
5. `Acceptance`
6. `Delivery Ops`

这样已经足够支撑 README 首页的主故事。

第二期再补：

1. `Prompt Assembly`
2. `Runtime Memory`

## 图片制作规格建议

为了适配 GitHub README，建议：

- 横图为主
- 主比例优先 `16:9`
- 少数机制图可用 `4:3`
- 所有图片保持同一视觉系统
- 每张图都允许在 README 中单独上下排布

建议出图时统一考虑：

- 顶部标题安全区
- GitHub 白底环境下的边界清晰度
- 缩略阅读时仍能看出结构
- 图内文字尽量少，避免过度依赖模型文字生成

## 后续执行顺序

下一步建议按这个顺序推进：

1. 先确认首页采用 `Version B`
2. 先为 6 张一期图片写统一 art direction
3. 再逐张生成首轮图
4. 选出可用图后，重写 README 首页结构
5. 最后补齐第二期机制图

## 最终建议

这次 README 首页升级，不应理解成“给 README 配几张插图”。

应该理解成：

- 把 `image2-design-director` 变成一个可以被看见、被感受到、被快速理解的产品故事

最核心的设计判断是：

- 首页负责建立信念和理解
- 文档负责承接细节和协议
- 图片负责讲“这个 skill 为什么不一样”
- 文字负责讲“用户下一步该怎么做”
