# Prompt Assembly

## Purpose

这份文档定义 `task packet -> final image prompt` 的默认装配方法。

它解决的问题不是“字段有哪些”，而是：

- 什么时候该用 structured / section-based
- 什么时候该用自然语言连续写法
- 怎么把任务、结构、文本层、风格层按稳定顺序拼起来

一句话版本：

> packet 是执行输入，schema 是骨架选择，assembly 才是把它变成可发给 Image2 的最终 prompt。

## Inputs

默认输入来自：

- [references/task-packet.md](references/task-packet.md)
- [references/prompt-schema.md](references/prompt-schema.md)
- [references/prompt-writing-spec.md](references/prompt-writing-spec.md)
- [references/sample-prompts.md](references/sample-prompts.md)

如果 task packet 还不是 `ready`，不要进入 assembly。

## Default Assembly Sequence

### 1. Lock The Task Statement

先写一句明确的任务定义：

- 这是什么资产
- 它服务什么目标
- 使用场景是什么

如果这一步还模糊，后面的结构和风格都会漂。

### 2. Choose Prompt Family

按版式复杂度选默认写法：

- 多模块、多区块、多文案层：`Structured / Section-Based`
- 单主体但要保留商业版式和 copy-safe 区：`Hybrid Structured Hero`
- 单图叙事、动作、中心隐喻：`Directed Natural Language`
- 已有图像迭代：在原写法上加 `Repair Overlay`

不要为了“统一格式”把所有任务都写成字段表。

## 3. Build The Prompt In Layers

### Layer A. Task Layer

先落：

- `asset type`
- `goal`
- `audience/context`

这是默认第一屏信息。

### Layer B. Subject Layer

明确：

- 主体是谁或是什么
- 主体处在什么场景
- 当前这张图的中心隐喻或中心对象是什么

### Layer C. Structure Layer

高结构任务必须明确：

- 区块
- 区域角色
- 主次层级
- 数量
- 留白或安全区

单图叙事任务则把这些信息转成：

- 视角
- 构图
- 前中后景
- 视觉焦点

### Layer D. Text Layer

文本层默认要单独写，不要埋在 constraints 里。

至少说明：

- `mode`: `verbatim` / `partial` / `emphasis-only` / `safe-area-only` / `none`
- `hierarchy`: 有几层信息
- `placement`: 放在哪
- `density`: 文本密度高还是低

长中文文本处理规则：

- 它是高风险信号，不是自动排除 `direct_output` 的理由
- 如果有可直出的参考图，或任务明确在测试直出，必须保留直出候选
- 如果走后处理路径，也要明确让模型产出 `text-safe visual`，而不是模糊地希望它顺带把所有小字排对

### Layer E. Style Layer

风格层最后补。

推荐只写真正影响结果的几类信息：

- 媒介感
- 材质感
- 灯光
- 色板
- 商业气质

不要让风格词压过任务层和结构层。

### Layer F. Constraints And Avoid

最后才补：

- 非谈判约束
- 明确不要什么

尤其要避免模型自行发明：

- logo
- badge wall
- 假文案
- 伪 UI
- 装饰性噪音

## 4. Resolve The Parameterized Draft

如果先写了模板，发送前要做两步：

1. 把 `{{placeholder}}` 替换成具体值
2. 删掉重复表达和无效修饰词

目标是让最终 prompt 保持：

- 信息完整
- 结构清楚
- 语言紧凑

而不是长成一份冗余说明书。

## 5. Apply Repair Overlay If Needed

如果是 repair，最后再叠加：

```text
Change only: <只改什么>
Keep unchanged: <必须保持什么>
```

默认只改最关键变量，不要重启整张图。

## Family-Specific Guidance

### Structured / Section-Based

适合：

- 海报
- UI mockup
- 落地页
- 设计系统页
- 信息图

默认要求：

- section 名称可读
- 区块职责明确
- 数量和位置尽量具体
- 文本层单独存在

### Hybrid Structured Hero

适合：

- 产品 hero
- 设备主视觉
- 社媒视觉底图
- 有单一主体的 campaign creative

默认要求：

- 先写结果目标
- 再写主体与场景
- 再写构图与留白
- 再写文本策略
- 风格层尽量短
- 如果是 repo hero、项目系统 hero、workflow hero，先把开放式系统语义翻成协议型视觉锚点，再写风格
- 默认写入 3 到 5 个可画出来的 motif，例如 `packet card`、`route node`、`scorecard chip`、`delivery-state frame`
- 如果 prompt 里出现 `delivery-state frame` 或 `review frame`，默认补一句 destination asset identity，明确它应保持中性项目资产，而不是模型自行发明的风景或建筑样张
- 这句 destination asset identity 默认不要停在抽象名词
- 应同时写：
  - `allowed examples`
    - 例如 `README hero plate`、`onboarding visual card`、`benchmark board preview`
  - `hard exclusions`
    - 例如 `landscape photograph`、`architecture render`、`room scene`、`framed scenic sample`
- 同时加一组语义排除，避免模型把系统 hero 误解成消费品、电商或 shopping workflow

### Directed Natural Language

适合：

- 单图叙事
- 动作场景
- 中心隐喻视觉
- onboarding 插图

默认要求：

- 句子顺序稳定
- 主体与动作尽量靠前
- 构图和光影明确
- 不要为了“结构化”把语言写碎

### Structured Poster For Launch Creative

如果当前任务是发布海报或品牌宣传海报，默认在 `Structure layer` 与 `Text layer` 之间补一句 transformation statement：

- 从什么转成什么
- 这个转化由哪些项目机制构成

推荐写成：

- `rough brief packet -> route trace -> scorecard -> delivery-ready asset`
- 并额外说明 destination asset 应该是什么类型的中性项目资产
- 最好直接写成：
  - `destination state: neutral project collateral such as a README hero plate, onboarding visual card, or benchmark board preview`
- 再补一句：
  - `not a scenic photograph, architecture sample, framed poster print, or travel-style image card`

不要只写：

- abstract transformation
- bold geometric energy
- futuristic campaign feel

否则很容易得到泛设计海报，而不是项目自己的 launch asset。

## Assembly Do / Don't

### Do

- 先任务，后结构，再风格
- 把文本层写成正式设计层
- 对复杂任务明确 section、数量和层级
- 对单图叙事保持连续语言张力
- 对可复用模板做参数化

### Don't

- 只堆 mood words
- 用风格词代替结构描述
- 在高结构任务里省略文本层
- 在单图叙事任务里硬塞太多 section
- 因为长中文文本就自动否决 `direct_output`

## Preflight Checklist

发送给 Image2 前，至少过一遍：

- 开头是否已经定义了资产类型和目标
- 画面组织方式是否明确
- 文本层是否单独处理
- 风格层是否服务任务，而不是喧宾夺主
- 如果是 repo hero，是否已经把 workflow 语义翻成协议型 motif，并排除了错误垂类语义
- 如果是 launch poster，是否已经把 transformation metaphor 写成项目机制，而不只是抽象几何语言
- 有没有清楚的 `Avoid`
- 如果这是测试任务，是否保留了可复盘的最终 prompt
