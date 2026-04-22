# Agent Poster Recovery

> Historical validation note: 这份文档记录的是一次已完成的 experiment 或 repair run。为公开发布，本地输出路径与 runtime 引用已泛化处理。

## Purpose

这份文档记录 `2026-04-22` 这次“Agent 海报测试任务”的失败点、修复方案、执行约束，以及修复后重跑测试时应保留的链路证据。

这不是泛泛复盘，而是一次明确的故障修复单。

## Trigger Task

用户原始需求：

> 生成一张这个主题的海报「CodeX 和 Claude Code 的每日活跃用户低于1000万，从人类整体的AI迁移视角出发，在使用这些最前沿Agent产品，就已经是人类的前千分之一了。」

用户额外提供的事实信号：

- 附了一张在 ChatGPT 中直出的参考海报
- 该参考图已经证明：模型并非必然无法完成长中文海报直出
- 用户预期的是高风格化、高传播感、高中心隐喻的海报，而不是仅仅把文字排上去

## What Went Wrong

### Problem 1. The Test Did Not Actually Exercise Image2

上一次所谓“完整测试任务”的最终产物是：

- `tmp/example-output/agent-top-permille-poster.svg`

它是手工绘制的 SVG，而不是一次真实 Image2 生成结果。

这意味着：

- 测试目标错位
- skill 的 prompt 能力没有被测试
- 模型对长中文海报的真实能力没有被测试
- 交付层手工排版冒充了生成层结果

### Problem 2. The Strategy Classified The Task Too Early Into `visual_base_plus_post`

上一次策略直接把这类任务判成：

- `social-creative`
- `visual_base_plus_post`
- `image-plus-delivery-ops`

问题不在于这条路径永远错误，而在于：

- 它被过早当成唯一正确路径
- 没有先验证 `direct_output` 是否可行
- 没有把用户给出的参考图当成高优先级证据

### Problem 3. The Policy Treated Long Chinese Copy As A Hard Blocker

现有 policy 倾向于把“必须准确中文文本”直接推向后处理。

这条规则本意是风险控制，但在执行时被误用了：

- 从“高风险”滑成了“默认做不到”

这会造成：

- 错误放弃直出分支
- 错误缩窄模型可探索空间

### Problem 4. The Prompt Chain Was Missing

上一次没有完整展示：

- intake summary
- strategy packet
- final image prompt
- evaluation notes

这让复盘时无法回答最关键的问题：

- 当时到底是怎么判断的
- 到底让模型做了什么
- 到底是哪一步导致输出跑偏

### Problem 5. The Evaluation Gate Failed

上一次最终给用户展示的图：

- 风格化不够
- 隐喻不够强
- 视觉上更像泛科技信息板
- 没有达到“真实传播海报”的强表达强叙事标准

按当前质量标准，它不应该被当成通过稿展示。

## Root Cause

这次失败不是单点 bug，而是链路连续失守：

1. intake 没把“参考图已证明直出可行”写成事实
2. strategy 把后处理路径过早钉死
3. execution 没有真正调用 Image2
4. evaluation 没有按高预期传播海报标准拦截
5. delivery 产物冒充 generation test 结果

## Repair Goals

修复后，这类任务必须满足下面 5 个要求：

1. 真实测试必须真的调用 Image2
2. 参考图或先验证据必须进入 strategy 判断
3. 长中文海报不能被默认排除在直出分支之外
4. 测试任务必须保留完整 prompt chain
5. 不过线结果不能再被包装成“已完成测试”

## Concrete Fixes

### Fix 1. Downgrade Long-Chinese Handling From Hard Block To Risk Signal

修复目标：

- 把“长中文文本需要后处理”从默认硬判断，改成高风险提醒

新规则：

- 如果用户提供了参考图、先验成功样本，或当前任务本身就是在测试模型直出能力
- 则必须至少保留一个 `direct_output` 候选

### Fix 2. Add A Direct-Output Branch For High-Opinion Poster Tasks

修复目标：

- 对 `social-creative` 里的观点型海报、招募海报、强传播口号海报
- 默认不要只走单一路径

新规则：

- 至少做一次：
  - `candidate A = direct_output`
  - `candidate B = visual_base_plus_post`

除非：

- 用户明确说只要后处理底图
- 或已有证据证明直出在当前场景必败

### Fix 3. Ban Manual SVG/Static Design Substitution In Generation Tests

修复目标：

- 真实测试任务里，不能再用手工 SVG、手工版式稿去冒充 Image2 生成结果

新规则：

- 如果任务目标是测试 skill 的生图链路
- 就必须保留真实模型产物

### Fix 4. Make Prompt Transparency Mandatory In Test Tasks

修复目标：

- 测试任务必须能完整复盘

新规则：

- 至少保留：
  - requirement summary
  - strategy summary
  - final image prompt
  - result evaluation

### Fix 5. Raise The Evaluation Bar For Social-Creative Posters

修复目标：

- 防止“可读但不够强”的海报混进通过稿

新规则：

- 对观点型海报额外关注：
  - 中心隐喻是否强
  - 风格是否足够鲜明
  - 是否具有真实 campaign poster 的传播压迫感

## Execution Rules For The Retest

这次重跑测试，必须遵守：

1. 真调用 Image2
2. 至少保留一个 `direct_output` prompt
3. 明确写出 prompt
4. 不用手工 SVG 当主结果
5. 如结果不过线，明确说不过线，不包装

## Retest Packet

### Requirement Summary

- 做一张高风格化、高传播感的观点型海报
- 主题是“使用最前沿 Agent 产品的人群，仍是人类中的极少数先行者”
- 文本可以长，但不允许因此自动降级成“纯后处理排版测试”

### Use Case

- `social-creative`

### Strategy Summary

- task mode: `benchmark_or_ab`
- route: `direct`
- candidate mode: `multi-candidate`
- output mode: 先测试 `direct_output`
- delivery involvement: `image-only`

### Success Criteria

- 必须有强中心隐喻
- 必须有明显海报感，而不是信息看板感
- 必须验证模型能否直接承担长中文文本海报
- 即使文字有瑕疵，整体也要先像一张真正想传播的海报

## Prompt Under Test

这次优先测试 `direct_output` 提示词，先不做底图后处理保守路径。

```text
Use case: social-creative
Asset type: launch poster
Primary request: generate a high-impact vertical campaign poster about how using frontier agent products already places someone in the leading tiny fraction of humanity's AI migration
Objective: make it feel like a real premium poster people would share, not an infographic board and not a generic tech wallpaper
Audience/context: Chinese-speaking frontier AI users, creators, developers, operators; social poster for high-agency early adopters
Subject: one lone human figure at the leading edge of a massive migration wave, with the scale of humanity behind them
Scene/backdrop: cinematic cosmic-earth horizon, immense crowd fading into darkness, a luminous path or threshold of migration, strong central symbolic composition
Style/medium: bold editorial campaign poster, premium sci-fi realism, high contrast black and gold with restrained blue accents, dramatic lighting, iconic and memorable
Composition/framing: vertical poster, unmistakable center axis, very strong hierarchy, large title integrated cleanly into the design, top and middle text zones are readable and intentional, not cluttered
Visual priorities:
1. strong symbolic metaphor for "frontier minority leading humanity's AI migration"
2. real poster energy, not dashboard, not information board
3. Chinese typography should be bold, legible, and naturally integrated
Text (verbatim):
"CodeX 和 Claude Code 的
每日活跃用户低于1000万
从人类整体的AI迁移视角出发
在使用这些最前沿Agent产品
就已经是人类的前千分之一了"
Constraints: render the Chinese headline cleanly and prominently; allow one additional large emphasis phrase only if needed, such as “前千分之一”; no extra paragraphs, no fake data panels, no UI cards, no infographic dashboard, no QR code, no logos
Avoid: generic futuristic HUD, weak stock-poster look, clutter, fake interface boxes, decorative nonsense text, low-drama composition, bland corporate gradient
```

## Test Result

### Observed Output

修复后，按 `direct_output` 路径重跑了一次真实 Image2 测试。

生成结果引用：

- `<generated-images-root>/019db483-28d8-79f2-bbf6-568007b06e1c/ig_06c13e80b8691f920169e89ba277b88191aedea29b93c440e7.png`

结果说明了三件事：

1. 模型可以直接生成这类长中文观点海报
2. 中文标题可以保持较高可读性
3. 强中心隐喻和史诗感海报语言可以通过直出拿到

### What Improved

- 不再是手工 SVG 冒充测试结果
- 中文文本直出可行性得到了真实验证
- 画面已经具备明确的中心隐喻：
  - 单个先行者
  - 人群
  - 发光通路
  - 地球尺度迁移语境
- 海报感明显强于上一版手工稿

### What Is Still Not Ideal

- 文字量仍然偏大，压缩了画面的呼吸感
- 视觉语言仍偏“史诗科技海报”，还可以更像真正 campaign creative
- “前千分之一” 的强调很强，但整体层级还可以再做一版更克制的对照

### Evaluation Summary

- `intent_match`: 明显提升，已经在解决原任务
- `asset_credibility`: 显著高于上一次手工稿
- `text_and_layout_fidelity`: 已证明不是硬失败点
- `anti_ai_artifact`: 仍有一点典型“大模型史诗海报感”，但比上一版链路错误更值得继续修

### Result Classification

- 当前结果应判为：`conditional_pass`

原因：

- 已经证明直出能力成立
- 已经达到“值得继续沿这条路修”的质量
- 但还没到最优传播海报版本

## Final Decision

### Decision

这次修复后的重跑，已经验证了最关键的判断：

- 这类任务不能被默认排除在 `direct_output` 之外

接下来更合理的默认流程应是：

1. 先保留 `direct_output` 候选
2. 如果需要，再和 `visual_base_plus_post` 做 A/B
3. 用真实生成结果，而不是手工稿，进入后续评估和修复

### Next Recommended Move

如果继续优化这张海报，建议下一步不是回退到保守后处理，而是：

- 保留当前中心隐喻
- 减少顶部文本压迫
- 把海报从“模型能做出来”推进到“更像成熟传播海报”

## Current Plan

基于这次修复后的认知，后续更合理的执行顺序应是：

1. 用同一 brief 做一次正式 A/B
   - `candidate A = direct_output`
   - `candidate B = visual_base_plus_post`
2. 把对比结果按 `ab-testing-template.md` 记录下来
3. 只在真实 A/B 显示后处理更稳时，才把后处理升成该类任务的默认推荐路径
4. 把“高观点长中文海报”补进 benchmark 常用回归样本
