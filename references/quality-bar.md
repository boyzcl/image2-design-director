# Quality Bar

## Core Question

不是“这张图漂不漂亮”，而是：

> 这张图是不是正确的资产、承载了可信的信息、用了匹配的表达机制，而且现在真的还能被继续使用或直接验收？

## General Pass Bar

- 用途感明确
- 资产类型正确
- 信息表达可信
- 表达机制匹配任务
- 成品度与任务合同一致
- 交付完整性没有被 overlay 或补充信息破坏

## Must-Have Evaluation Angles

### 1. Asset Type Fidelity

问：

- 它是不是用户真正要的那类资产

### 2. Information Reliability

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

### 3. Representation Fit

问：

- 这类信息是否被交给了正确的表达机制

高分信号：

- 纯视觉任务用模型直出
- 精确图表和指标走 deterministic 或 hybrid
- 需要后置的固定元素没有强塞进模型文字

### 4. Delivery Integrity

问：

- 最终结果有没有因为 overlay 或交付操作而破坏主视觉和信息层级

高分信号：

- protected regions 保持完整
- 文本和 fixed elements 进入后仍然稳定

低分信号：

- overlay 虽然“放上去了”，但图已经失去可用性

### 5. Completion Readiness

问：

- 这张图现在是不是用户可验收的完成状态

### 6. Language Alignment

问：

- 文案语言和文字策略是否跟随当前任务

### 7. Misleading Risk

问：

- 这张图会不会让读者相信一个没有被可靠支撑的结论

## Quick Red Flags

出现以下任一项时，优先进入 `repair`、`contract_realign` 或直接 `regenerate`：

- 资产类型错
- 成品度错
- 事实性表达未经验证
- representation mode 明显错位
- overlay 侵入 protected regions
- “好看但不可信”
- “准确但不可用”

## Hard Fail Conditions

出现以下任一项时，不应称为“已经达到目标”：

- 资产类型错误
- 成品任务被做成底图
- 高事实敏感任务缺少可靠性 gate 结果
- 精确数字、价格、日期仍留在不可信模型文字里
- delivery viability 明显失败
- `misleading_risk = high`
