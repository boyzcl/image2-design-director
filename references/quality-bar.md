# Quality Bar

## Core Question

不是“这张图漂不漂亮”，而是：

> 这张图是不是正确的资产、承载了可信的信息、用了匹配的表达机制、现在真的还能被继续使用或直接验收，而且在 publication 场景下它是不是已经是正确身份的成品图。

## General Pass Bar

- 用途感明确
- 资产类型正确
- 资产身份正确
- 信息表达可信
- 表达机制匹配任务
- 成品度与任务合同一致
- 交付完整性没有被 overlay 或补充信息破坏
- 如果是文章发表图，结果已通过 publication review

## Must-Have Evaluation Angles

### 1. Asset Type Fidelity

问：

- 它是不是用户真正要的那类资产

### 2. Asset Identity Fidelity

问：

- 这是不是当前任务需要的资产身份
- 它是 `publication_asset`，还是只是 `internal_candidate / review_candidate`

高分信号：

- benchmark、overlay demo、repair artifact 没有被误当成最终交付
- 文章图已经明确是 `publication_asset`

低分信号：

- 内部工件被误用为正文配图
- `text-safe`、`masthead-safe`、bundle 中间态被误称成成品

### 3. Information Reliability

问：

- 图中关键信息是否可信
- 是否锁定了正确的 metric、日期和口径
- 如果未验证，是否明确降级成视觉隐喻或带免责声明的表达

高分信号：

- 事实敏感内容有明确信息边界
- 精确内容没有交给失真的 AI 文本承担

低分信号：

- “最新”“最强”“涨幅”之类结论没有 evidence support
- 数字、日期、排行被模型随意生成

### 4. Representation Fit

问：

- 这类信息是否被交给了正确的表达机制

高分信号：

- 封面、基础图、workflow、advance、evidence、数据、价格、排行优先用 Image2 直出完整资产
- 数据 / 价格 / 排行图先完成 reliability gate
- QR、Logo、Exact copy 和锁定数值只做局部后期，不重建整张图

### 5. Delivery Integrity

问：

- 最终结果有没有因为 overlay 或交付操作而破坏主视觉和信息层级

高分信号：

- `protected_regions` 保持完整
- 文本和 fixed elements 进入后仍然稳定

低分信号：

- overlay 虽然“放上去了”，但图已经失去可用性
- 文章图进入 overlay 却没有声明 `title_region / core_subject_region / focus_information_region`

### 6. Publication Support

问：

- 这张图是否真正支持文章论点
- 它是在解释、证明、承接文章，而不是把读者带到别的场景

高分信号：

- 视觉隐喻、机制表达或证据组织都直接服务文章主线
- 读者不会把它误读为活动海报、报名图或产品广告

低分信号：

- 图像只是在“看起来像个设计成品”，却没有帮助文章成立
- 内容更像 event poster、benchmark board 或宣传板

### 7. Completion Readiness

问：

- 这张图现在是不是用户可验收的完成状态

文章场景默认要求：

- `complete_asset`
- 默认交付成品图，不是中间稿

### 8. Language Alignment

问：

- 文案语言和文字策略是否跟随当前任务

### 9. Cross-Scene Cleanliness

问：

- 是否还残留跨场景文案、CTA、二维码、badge、日期、报名语义或不该出现的 fixed elements

## Quick Red Flags

出现以下任一项时，优先进入 `repair`、`contract_realign` 或直接 `regenerate`：

- 资产类型错
- 资产身份错
- 成品度错
- 事实性表达未经验证
- representation mode 明显错位
- overlay 侵入 protected regions
- `protected_regions` 缺失却声称完成 overlay collision check
- benchmark / overlay demo / exploratory repair output 被误当正文图
- “好看但不可信”
- “准确但不可用”
- “能继续改，但还不是最终可见资产”

## Hard Fail Conditions

出现以下任一项时，不应称为“已经达到目标”：

- 资产类型错误
- 资产身份错误
- 成品任务被做成底图
- 文章场景结果仍停留在 `title-safe`、`text-safe`、`masthead-safe` 中间态
- 高事实敏感任务缺少可靠性 gate 结果
- 精确数字、价格、日期仍留在不可信模型文字里
- delivery viability 明显失败
- `misleading_risk = high`
- 未通过 `publication_readiness_review`
- 未通过 `visual_quality_review`
- 未通过 `final_release_gate`
- 仍残留活动报名语义、二维码、CTA、日期、badge 等跨场景元素

## Production Quality Gate

文章配图、editorial collateral、publication figure 不能只在结果阶段验收。进入生成前必须先通过 `production_preflight`。

`production_preflight` 最少确认：

- `figure_role` 已明确
- `asset_goal` 已绑定文章论点
- representation route 符合 figure role
- text owner 合理
- text budget 没有过载
- forbidden drift 已声明
- candidate policy 符合 figure role

如果 production preflight 没有通过，不能声称这轮生成是正确执行的 production path。

## Visual Quality Review

`publication_readiness_review = pass` 只说明资产身份和场景边界正确，不说明图面质量达到发布级。

文章图最终还必须通过 `visual_quality_review`。它评估：

- `text_readability`
- `typographic_craft`
- `layout_hierarchy`
- `semantic_clarity`
- `publication_argument_support_visual`
- `series_consistency`
- `asset_distinctiveness`
- `polish_and_finish`

以下情况默认不能判为发布级：

- 中文断行破坏阅读
- 英文术语被异常拆开
- 机制图用段落卡片解释机制
- workflow evidence 图只有抽象装饰，没有证据对象
- 封面缺少开篇张力，只像内部报告页
- 同一组图过度模板化

## Final Release Gate

用户可见输出、正文插图、README 成功样张必须通过 `final_release_gate`。

`final_release_result = pass` 只在下面全部成立时允许：

- `production_preflight_result = pass`
- `publication_review_result = pass`
- `visual_quality_review_result = pass`
- `delivery_viability_result` 不是 no-go
- `runtime_capture_present = true`

`publication_review = pass` 不再等同于 `final_release = pass`。
