# Status Summary 2026-04-22

> Public historical note: 这份文档保留的是 `2026-04-22` 的阶段性事实快照。它适合作为公开仓库中的历史背景材料，不是第一次使用 skill 时的必读入口。

## Purpose

这份文档记录 `image2-design-director` 在 `2026-04-22` 的当前事实状态，避免仓库内出现“默认规则是什么、最近验证到了哪一步、当前样本说明了什么”这些问题的多版本口径。

## Current Operating Truth

截至 `2026-04-22`，这个 skill 的运行真相可以收束为八点：

1. 已经形成稳定的三路由框架：
   - `direct`
   - `brief-first`
   - `repair`
2. 默认 prompt 框架已从“执行细节导向”收紧为“结果导向”：
   - `asset goal`
   - `desired outcome`
   - `3-5 non-negotiables`
   - `minimal context anchors`
3. 每次调用 Image2 生成或编辑图像后，默认都要写 runtime capture。
4. runtime capture 现在不只记录 brief 和总结，还应能回溯：
   - `brief -> final_prompt -> image_prompt -> generated image path(s) -> evaluation`
5. “长中文文本默认必须后处理”不能再被当成硬结论：
   - 它现在应被视为高风险信号，而不是自动否决 `direct_output` 的挡板
6. 如果用户已经提供了模型可直出的参考图，或当前任务本身就是在测试直出能力：
   - strategy 必须至少保留一个 `direct_output` 候选
   - 不能直接把任务压进单一路径的 `visual_base_plus_post`
7. 四个高频方向不再应被当成 skill 的能力边界：
   - 它们现在应被视为已验证档案，用来提供 `accelerated` 加速
   - 不命中档案的新场景也应进入通用流程，先拿到 `60+` 的可诊断起点
8. runtime 和宿主解析不应绑定 Codex：
   - runtime root 现在应优先支持显式 `--root`、通用环境变量，以及多 Agent 宿主
   - `<agent-home>/...` 只能算已知宿主之一，不应再被写成唯一默认真相

## Runtime Memory Status

当前 runtime 机制已经具备以下事实能力：

- runtime root 已改成 host-agnostic 解析：
  - `--root`
  - `IMAGE2_DESIGN_DIRECTOR_RUNTIME_ROOT`
  - `AGENT_SKILLS_HOME`
  - 已知 Agent home 环境变量
  - `AI_AGENT_HOME` / `AGENT_HOME`
  - 通用兜底 `~/.ai-agents/skills/image2-design-director/runtime/`
- 已支持原始 capture 追加写入
- 已支持按 `scene`、`failure_mode`、`generation_id` 建索引
- 已支持 review queue
- 已支持从 capture 晋升到 field note / repo candidate

## Generalization And Portability Decision

当前项目已经做出两条新的架构判断：

1. `image2-design-director` 应该面向所有“设计可用性要求较高”的深图场景生效
   - 四个既有方向保留，但被重新定义为已验证档案
   - 命中时提供 `accelerated`，不命中时走 `standard` 或 `exploratory`
2. 这个 skill 不应绑定 Codex
   - 它本质上是文本规则、策略和经验系统
   - 只要 Agent 具备图像生成能力，就应该能够复用这套协议与 runtime 机制

因此，repo 当前新的协议重心是：

- 用 `domain_direction + matched_profile + support_tier` 代替固定四选一 `use_case`
- 用 host-agnostic runtime root 代替单一宿主私有路径假设
- 让新场景可以通过 repeated capture 从 `exploratory -> standard -> accelerated`

## M9 Operationalization Judgment

进入 `m9_generalization_operationalization` 之后，当前真正的阻塞已经不是 prompt 规则，而是 4 条链路没有被同一套协议接起来：

1. generalized benchmark surface
   - 旧 benchmark 主要还在回归旧高频方向
   - 还不足以验证新场景首轮能否先拿到 `60+` 的可诊断起点
2. runtime schema v2
   - repo 已经说 `domain_direction / matched_profile / support_tier`
   - 但 runtime 还没有把 capture / review / field note 的正式字段契约单独收清楚
3. profile promotion policy
   - 已有样本晋升治理
   - 但还没有明确 scene profile 如何从 `exploratory -> standard -> accelerated`
4. repo vs installed copy sync
   - 本机同时存在 repo 与 `<agent-home>/skills/image2-design-director`
   - 两者已经发生明显漂移
   - 如果没有 contract，就会持续出现“repo 改了，宿主没跟上”的问题

这轮已补齐的口径是：

- `docs/benchmarks/generalized-benchmark-surface.md`
- `docs/runtime-schema-v2.md`
- `docs/profile-promotion-policy.md`
- `docs/repo-installed-runtime-sync-contract.md`

同时，benchmark template、runtime docs、promotion docs、architecture docs 和执行看板也已同步到这套新口径。

## M9 Follow-Up Validation Snapshot

在上面的协议层补齐之后，本轮又完成了两项真正的 follow-up execution：

1. 跑了一条真实 exploratory benchmark
2. 执行了一次受控 repo -> installed copy sync

### Exploratory Benchmark Result

对应文档：

- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md`

这次验证选择的是一个不命中既有四档案的场景：

- `domain_direction: protocol explainer poster for an AI workflow system`
- `matched_profile: none`
- `support_tier: exploratory`

最重要的结果不是“已经成熟”，而是：

> 新场景首轮已经能从 `56.0 fail` 提升到 `73.0 conditional_pass`，并且 candidate 明确越过了 exploratory lane 的 `60+` 可诊断起点。

这次实跑进一步确认了两点：

1. generalized benchmark surface 不是空口承诺
   - unmatched scene 现在已经有一条真实验证样本
2. 当前 exploratory lane 的真正剩余问题已经收敛
   - 不再是“整个 scene system 不成立”
   - 而是更具体的 `destination asset identity gap`

### Runtime V2 Real-Run Confirmation

这次 exploratory benchmark 没有只停在 benchmark 文档里。

对应 runtime 事实：

- 两条真实 run 已写入：
  - `<runtime-root>/captures/2026-04-22.jsonl`
- 并且已经能按新字段直接查询：
  - `matched_profile=none`
  - `support_tier=exploratory`

这说明 runtime schema v2 已经不只是文档定义，而是能承接真实 run。

### Repo vs Installed Sync Confirmation

这轮还执行了一次受控同步：

- source repo: `<repo-root>`
- installed copy: `<agent-home>/skills/image2-design-director`

同步方式按 contract 保留了：

- `runtime/`
- `state/`
- `test-output/`
- repo-only execution docs / experiments

同步后又做了两层验证：

1. 关键文件逐个 `cmp`
2. 排除 contract 允许差异后的文件清单对比

当前结论应收束为：

> installed copy 的核心 skill / docs / scripts 已和 repo 对齐，剩余差异已被收敛到 contract 允许的范围内。

## Current Highest-Leverage Open Gap

在 exploratory benchmark 和 sync 都落地之后，当前最高杠杆问题已经进一步收束：

> 不是 scene system 还没泛化，而是 `destination asset identity` 这一条默认约束仍然写得不够死。

具体表现是：

- protocol-native 中间链路已经成立
- 但 `delivery-ready asset frame` 仍容易被模型补成 scenic / architecture / framed sample

因此，下一轮默认不应再回到大范围架构改写，而应优先做：

1. 收紧 prompt schema / assembly / sample prompt 里的 destination asset language
2. 用同一 exploratory benchmark 复跑
3. 看 scenic drift 是否真的下降

## Destination Asset Identity Repair Snapshot

对应文档：

- `docs/experiments/destination-asset-identity-repair-2026-04-22.md`

这轮 repair 已经按最小变量原则完成一次真实复跑。

当前最重要的判断是：

> `destination asset identity` 这一条规则本身已经被验证有效，scenic drift 已明显下降。

这次 repair 的变化不在于整体 scene system 又变了，而在于默认 prompt 语言终于从：

- `neutral project asset`

收紧成了：

- allowed examples
  - `README hero plate`
  - `onboarding visual card`
  - `benchmark board preview`
- hard exclusions
  - `landscape photograph`
  - `architecture render`
  - `room scene`
  - `framed art print`

修复后结果可收束为：

- 总分：`80.0`
- 结果：`conditional_pass`

当前剩余问题也更窄了：

- 不再是 scenic sample drift
- 而是 `minor_text_discipline_leak`

也就是说，最高杠杆 open issue 已从“asset 类型不对”继续缩小到“destination panel 里的小字纪律还不够稳”。

## Text Discipline Repair Snapshot

对应文档：

- `docs/experiments/text-discipline-repair-2026-04-22.md`

在 `destination asset identity` 修正后，本轮又追加了一次更小的 repair：

- 保持 neutral project collateral examples 不变
- 只增加 `placeholder-only / no readable labels / no microtext`

这次结果可收束为：

- 总分：`84.0`
- 结果：`pass`

最重要的判断是：

> 这条 exploratory protocol visual 已经不再处于“救火状态”，而是进入了可选 polish 状态。

当前残余风险已继续缩小为：

- `slight-ui-board-literalness`

也就是：

- scenic drift 已压下去
- readable label leak 也已压下去
- 剩下的是最终 collateral panel 还有一点偏 literal board preview，而不够 editorial

## Remaining Gaps Vs Earlier Plan Expectation

如果回到更早那版计划预期，当前还剩的差距已经不再是“缺 intake / 缺 strategy / 缺 generalized benchmark contract”。

这些更早的系统缺口现在基本都已经补齐。

当前还剩的差距主要是 4 类：

1. 验证厚度还不够
   - 已证明有一条 unmatched scene 能达到 exploratory `60+`
   - 但还没有足够多的 exploratory / standard transfer 样本来支撑更强的全场景承诺
2. promotion 规则已成文，但 promotion 样本还不够
   - `exploratory -> standard -> accelerated` 已有明确门槛
   - 但新场景还没有真实升档案例
3. delivery layer 还是“规则强于工具”
   - delivery docs 已经齐
   - 但后处理 / 尺寸适配 / fixed-element 还没有更产品化的执行链路
4. sync 已经受控，但还没自动化
   - repo -> installed copy 已真实跑过一次
   - 但还没有 manifest、自动 drift 检测或一键同步机制

换句话说，当前项目和之前计划预期之间的差距，已经从“体系没长出来”收敛成了：

- 样本厚度
- 晋升厚度
- 交付工具化
- 同步自动化

而不是更早阶段那些基础协议缺口。

## M14 Local Auto-Promotion Snapshot

对应本轮新增事实：

- `runtime -> local skill reference layer` 第一版已落地
- `runtime -> repo / GitHub public rule layer` 仍保持人工边界

当前已经完成：

1. local skill reference layer 已有稳定落点
   - `promoted/local-skill/active`
   - `promoted/local-skill/disabled`
   - `promoted/local-skill/archive`
   - `promoted/local-skill/history`
2. review worker 已能把合格 capture：
   - 先升为 `field note`
   - 再按 gate 自动晋升到 active local skill refs
3. skill 读取链路已默认改为：
   - `local_skill_reference -> field_note -> capture`
4. 最小治理已经工程化：
   - working-set ceiling
   - `disable`
   - `archive`
   - `rollback`
5. repo 边界已被守住：
   - `repo-candidates/` 目录仍保留
   - 但自动链路不会写 repo candidate，也不会自动改 repo 公开资产

本轮又额外完成了两项更关键的收口：

1. merge 质量已从“纯 token overlap”升级到：
   - `scene family`
   - `scene role`
   - `domain_direction / matched_profile / support_tier`
   - 文本相似度
2. 真实 backlog replay 已证明：
   - `alpha / beta / retry` 这类变体仍会收敛
   - `baseline / candidate / preflight / repair` 这类真实对照位不会被误并

同时，旧 runtime 的兼容层也已补上：

- 旧 `promotion-policy.json` 会自动收敛到当前安全默认值
- 旧 capture 的列表字段现在也能正确参与打分

因此，`local auto-promotion 仍未落地` 这条旧判断现在应视为失效。

## Stage Review Entry

如果需要按“阶段 / 预期 / 当前状态 / 剩余差距 / 是否闭环”来讨论项目，而不是只看 milestone 和实验记录，当前统一入口是：

- `docs/stage-progress-review-2026-04-22.md`

这份文档把当前项目拆成 8 个阶段，并额外收束了：

- 当前最高优先级阶段
- 哪些阶段已经基本闭环
- 哪些差距已经从系统性问题下降到 polish 级问题

## M11 Entry

基于阶段看板，项目当前已正式打开下一执行阶段：

- `docs/m11-validation-thickening-and-promotion-activation.md`

这份文档把当前“还差什么”进一步收束成可执行任务，而不是继续停在阶段判断层。

当前对 M11 的总判断是：

> 现在最需要的不是继续优化单个 prompt，而是把 generalized validation 做厚，让第一批真实 profile promotion judgment 发生，再用这些样本反推 delivery toolization 和 sync automation 的真实优先级。

## Scene Generalization And Portability Snapshot

在 prompt-family 验证和默认规则收紧之后，项目又完成了一轮更偏架构层的调整。

这轮调整的核心不是继续抠单个 prompt family，而是修正 skill 的边界定义：

1. skill 不再被定义成只服务四类固定 use case
   - 四个方向保留
   - 但被重新定义为已验证档案，而不是能力边界
2. skill 不再被定义成 Codex 专属
   - repo 规则层现在按“任意具备图像生成能力的 Agent”来写
   - runtime root 解析也已改成 host-agnostic

对应完成的工作包括：

- `SKILL.md`
- `docs/target-skill-architecture.md`
- `references/task-packet.md`
- `references/strategy-decision-tree.md`
- `references/prompt-schema.md`
- `references/image2-prompting-playbook.md`
- `references/runtime-memory.md`
- `scripts/runtime_memory_lib.py`

这轮同步后的当前认知应收束为：

- 命中已验证档案的任务，目标是更快冲到 `80-85+`
- 不命中档案的新场景，仍应进入统一流程，先拿到 `60+` 的可诊断起点
- 新场景应通过 repeated capture 和纠偏规则，从 `exploratory -> standard -> accelerated`

### Portability Smoke Test

本轮还做了一次显式 `--root` 的 runtime smoke test。

验证内容：

- `init_runtime_memory.py`
- `write_runtime_capture.py`
- `read_runtime_context.py`
- `review_runtime_candidates.py`

验证结果：

- 脚本语法检查通过
- 显式 `--root` 的 runtime 初始化、capture 写入、上下文读取、review queue 流程全部跑通
- 当前判断：repo 层的 runtime 协议已经不再依赖 Codex 特定路径才能工作

当前新增脚本：

- `scripts/log_image_generation.py`

它的目的不是替代 `write_runtime_capture.py`，而是把一次真实生图结果更稳定地写进 runtime，尤其是：

- 给生图接口的文本输入是什么
- 生成目录或具体图片路径是什么
- 当前轮结果是 `review / fail / conditional_pass / pass` 中的哪一种
- 下一轮应改哪个变量

## Latest Validation Snapshot

本次新增了一组围绕 `ai-native-loop` 宣传图的真实样本，可作为当前阶段的参考验证。

### Scenario

- asset type: 项目 / skill 宣传 hero 图
- use case: `social-creative`
- route sequence:
  - first pass: `direct`
  - second pass: `repair`

### Version 1

结论：

- 方向基本正确
- 已抓到 `loop / collaboration / runtime memory` 的语义
- 但更像抽象概念主视觉，还不够像真实项目介绍物料

主要 failure class：

- `product-marketing specificity gap`

### Version 2

结论：

- 总分：`78 / 100`
- 结果：`conditional_pass`

改善点：

- 留白更干净
- 可读英文几乎被移除
- 更利于后续中文标题排版
- 主视觉、辅卡片、留白关系更稳定

仍存在的问题：

- 主体仍偏抽象系统板
- 项目特异性还不够强
- 更像高质量视觉底图，而不是已经长成独特品牌资产

因此，当前最明确的下一轮方向是：

> 在不破坏现在这版干净 hero 构图的前提下，进一步加入 `ai-native-loop` 独有的协议卡、runtime capture、回收链路等结构特征，让图像从“泛系统设计图”进一步收敛到“这个 skill 自己的视觉资产”。

## Latest Repair Snapshot

本次还新增了一次围绕“Agent 海报长中文直出能力”的故障修复与重跑验证。

对应文档：

- `docs/experiments/2026-04-22-agent-poster-recovery.md`

### Failure Before Repair

上一次错误不在于“图不够好看”而已，而是链路本身失真：

- 过早把任务判成 `visual_base_plus_post`
- 把长中文文本误当成直出硬障碍
- 没有完整保留 prompt chain
- 用手工 SVG 冒充真实生图测试结果

### What Was Corrected

本次已完成 4 类修正：

1. 策略修正
   - 高观点 `social-creative` 海报在文本可行性存疑时，必须至少保留一个 `direct_output` 候选
2. policy 修正
   - 长中文文本从“硬挡板”降级为“高风险信号”
3. evaluation 修正
   - 测试任务若没有真实模型产物，不能判为通过
4. workflow 修正
   - 禁止再用手工 SVG、静态版式稿代替生图链路测试结果

### Retest Outcome

修复后，已按 `direct_output` 路径真实重跑一次 Image2 海报测试。

当前最重要的结论是：

> 模型可以直接承担这类长中文观点海报，`direct_output` 不是应被默认排除的路线。

当前对这次重跑结果的判断应收束为：

- 结果：`conditional_pass`

原因：

- 已经证明直出路线成立
- 已经明显优于上一次错误链路产物
- 但离“成熟传播海报”还有继续压缩文本密度、强化 campaign 感的空间

## Documentation Alignment Notes

截至本次同步，以下文档已经与当前运行真相对齐：

- `SKILL.md`
- `references/prompt-schema.md`
- `references/prompt-assembly.md`
- `references/sample-prompts.md`
- `references/runtime-memory.md`
- `references/scorecard.md`
- `references/post-processing-policy.md`
- `references/strategy-decision-tree.md`
- `docs/benchmarks/benchmark-run-template.md`
- `docs/benchmarks/generalized-benchmark-surface.md`
- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-protocol-visual.md`
- `docs/runtime-schema-v2.md`
- `docs/profile-promotion-policy.md`
- `docs/repo-installed-runtime-sync-contract.md`
- `docs/experiments/2026-04-22-agent-poster-recovery.md`
- `patterns/README.md`
- `runtime/README.md`

对齐后的共同口径是：

- capture 默认每次都写
- scorecard 用来判过线、repair 与晋升，而不是决定要不要写 capture
- benchmark 记录需要带上 `image_prompt / generation_id / image_output_ref`
- benchmark 记录现在还应带上 `domain_direction / matched_profile / support_tier`
- exploratory lane 现在已有一条真实 `60+` 通过样本，而不只是协议定义
- pattern 提升前，必须能回溯 `prompt -> output -> evaluation`
- 长中文文本默认是风险，不是硬挡板
- 用户给出可直出参考图时，必须保留 `direct_output` 候选
- 测试任务里，手工稿不能代替真实模型产物
- repo、installed copy、runtime 是三层边界，不应再被默认混写
- repo 到 installed copy 的核心同步已经做过一轮受控执行，当前剩余差异已符合 contract

## Post-Fusion Prompt System Judgment

截至当前回合，项目已经不再停留在“知道外部 prompt 范式有价值”的阶段，而是已经把它们写回默认 prompt 体系：

- prompt family 已被正式拆成：
  - `structured / section-based`
  - `hybrid structured hero`
  - `directed natural language`
  - `repair overlay`
- prompt assembly 已从字段堆叠升级成层级装配：
  - `task -> structure -> text -> style -> constraints`
- text layer 已被正式定义为设计层，而不是附带限制
- sample prompt 已转成参数化模板 + resolved example

这意味着当前最大的未闭环点已经改变：

> 现在缺的不是更多 prompt 规则，而是 prompt-system 级改动的真实 benchmark 验证面。

截至这次判断，最关键的新缺口有两项：

1. 原 benchmark surface 还没有专门覆盖 `directed natural language`
2. benchmark run 记录还没有显式写入 `prompt_family`、`text_layer_mode` 和 `final_prompt`

因此，当前最合理的下一轮不是继续扩 prompt 文档，而是先把 benchmark surface 对齐到新的 prompt family，并打开一轮正式 regression。

## Open Follow-Up

当前还没有完成的，不是“prompt 规则有没有写出来”，而是下面三步：

1. 跑第一轮 prompt-family regression，验证新的默认 prompt 写法是否在 4 个 family 上都成立
2. 如何把 `conditional_pass` 海报继续推进到更稳定的 `85+ pass`
3. 如何把“直出成立”变成更可靠的默认策略判断，而不是一次偶然命中

就当前样本看，下一步最值得持续强化的方向是：

- 让 benchmark surface 覆盖 `structured / section-based`、`hybrid structured hero`、`directed natural language` 和 `repair overlay`
- 让 benchmark run 强制记录 `prompt_family`、`text_layer_mode`、`final_prompt` 与真实输出 ref
- 在保留直出分支的同时，引入 `direct_output` vs `visual_base_plus_post` 的正式 A/B
- 强化观点海报的中心隐喻、层级压缩和真实 campaign 感
- 让测试任务的 prompt chain、evaluation 和 result ref 成为强制留痕项

## Prompt Family Validation Snapshot

在本次同步之后，项目又完成了第一轮真实 prompt-family regression。

对应记录：

- `docs/benchmarks/prompt-family-regression-run-2026-04-22.md`

当前最重要的验证结论是：

1. `structured / section-based UI`
   - 已被真实验证
   - candidate 从 `66.0 fail` 提升到 `85.5 pass`
2. `directed natural language`
   - 已被真实验证
   - candidate 从 `50.0 fail` 提升到 `82.5 conditional_pass`
3. `structured / section-based poster`
   - 方向成立，但仍未完全稳定
   - candidate 从 `60.0 fail` 提升到 `75.0 conditional_pass`
4. `hybrid structured hero`
   - 当前未通过验证
   - candidate 从 `70.5 fail` 回退到 `62.5 fail`

这说明当前默认 prompt-system 的真实状态不是“全面升级已验证”，而是更准确地收束为：

- 两个 family 已成立
- 一个 family 方向成立但还要补 repair
- 一个 family 需要先修 domain drift，不能直接上升为更强默认能力承诺

因此，当前最合理的下一步也发生了变化：

> 不再是继续扩 prompt family，而是围绕最弱的两条 family 做 targeted repair。

## Prompt Family Retuning Snapshot

在第一轮 regression 之后，项目又对两条最弱 family 各跑了一轮 targeted repair。

对应记录：

- `docs/experiments/prompt-family-retuning-2026-04-22.md`

repair 后的当前判断应更新为：

1. `hybrid structured hero`
   - 从 `62.5 fail` 提升到 `81.0 conditional_pass`
   - 主要修复：清掉消费品 / 电商漂移，重新拉回 protocol-native hero
   - 仍保留的问题：review frame 里的 asset 题材还不够中性，微文案略多
2. `structured / section-based poster`
   - 从 `75.0 conditional_pass` 提升到 `83.0 conditional_pass`
   - 主要修复：从泛设计海报转成 `brief -> score -> asset` 的项目化海报
   - 仍保留的问题：最终 asset 仍稍偏通用样张，离稳定 `85+ pass` 还差一轮 polish

这意味着当前 prompt family 的真实状态已经进一步收束为：

- `structured / section-based UI`: 已验证，保留
- `directed natural language`: 已验证，保留
- `structured / section-based poster`: repair 后可保留，但仍需一轮 polish 才适合更强默认承诺
- `hybrid structured hero`: repair 后可保留，但必须维持更窄的协议型锚点约束

## Default Rule Promotion Decision

基于 regression 和 retuning 的合并结论，当前项目不需要回退 prompt family 体系，但要把两条 repair 规则正式提升为 repo 默认规范。

具体判断：

1. `structured / section-based UI`
   - 已验证成立
   - 可以继续按当前默认骨架使用
2. `directed natural language`
   - 已验证成立
   - 可以继续按当前默认骨架使用
3. `structured / section-based poster`
   - 不应继续停留在“方向成立但只存在实验文档里”
   - 要正式把 `brief packet -> route trace -> scorecard -> delivery-ready asset` 的项目机制转化写法写回默认规范
4. `hybrid structured hero`
   - 不应继续使用开放式 `workflow hero` 叙述
   - 要正式把 `packet card / route node / prompt assembly layer / scorecard chip / delivery-state frame` 这组协议型锚点和对应的错误语义排除写回默认规范

因此，下一步不再是大范围扩 prompt family，而是：

1. 回写默认规则
2. 用 tightened default 做小规模 spot-check
3. 再决定是否把这轮 repair 规则进一步晋升为更强 pattern

## Default Spot-Check Snapshot

在把 hero / poster 的 repair 规则回写进默认规范后，项目又做了一轮小规模真实 spot-check。

对应记录：

- `docs/experiments/default-family-spot-check-2026-04-22.md`

当前结果：

1. tightened `hybrid structured hero`
   - 得分：`82.5 conditional_pass`
   - 已验证：协议型视觉锚点默认化后，repo hero 不再回流到消费品 / 电商语义
   - 新暴露缺口：`delivery-ready asset frame` 还会被模型补成风景 / 建筑样张
2. tightened `structured / section-based poster`
   - 得分：`82.0 conditional_pass`
   - 已验证：项目机制转化写法默认化后，poster 不再退回泛 logo / 抽象几何海报
   - 新暴露缺口：最终 asset 仍偏风景样张，次级小字还可继续压缩

这说明当前默认 prompt-system 的真实状态又进一步收束为：

- `structured / section-based UI`: 已验证，保留
- `directed natural language`: 已验证，保留
- `structured / section-based poster`: 默认方向已稳，但需要补 `destination asset identity`
- `hybrid structured hero`: 默认方向已稳，但需要补 `destination asset identity`

也就是说，当前最值得继续写进默认规范的，不再是更大范围的新 family，而是：

- 对 `review frame / delivery-state frame / delivery-ready asset` 增加最终资产身份约束

## M11 Exploratory Validation Snapshot

进入 `m11_validation_thickening_and_promotion_activation` 后，本轮已继续完成两条新的 `exploratory unmatched-scene` benchmark。

对应记录：

- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-editorial-report-cover.md`
- `docs/benchmarks/benchmark-run-2026-04-22-exploratory-educational-visual-board.md`

这轮最重要的结果不是“又多两张图”，而是：

> exploratory lane 现在已经不只在一条 protocol poster 上成立，而是在 `editorial report cover` 和 `educational visual board` 这两类不同资产身份上也跑通了 `60+ -> 可诊断 -> 可继续修` 的闭环。

### New Exploratory Run 1. Editorial Report Cover

这条 run 选择的是：

- `domain_direction: editorial report cover for an AI design-operations system`
- `matched_profile: none`
- `support_tier: exploratory`

结果可收束为：

- baseline：`67.5 fail`
- candidate：`83.5 conditional_pass`

最重要的判断是：

> unmatched scene 不只可以长成 poster 或 protocol explainer，也已经能长成可信的 editorial collateral。

当前剩余问题也很窄：

- `minor-abstract-art-residue`

也就是：

- 正式 report-cover identity 已经成立
- masthead-safe band 已经很稳
- 剩下只是 subordinate cards 还有一点偏抽象封面 study，而不够 report-native

### New Exploratory Run 2. Educational Visual Board

这条 run 选择的是：

- `domain_direction: educational visual board for AI image-prompt debugging heuristics`
- `matched_profile: none`
- `support_tier: exploratory`

结果可收束为：

- baseline：`73.5 fail`
- candidate：`79.5 conditional_pass`

最重要的判断是：

> educational visual board 这类 unmatched scene 也已经具备稳定 diagnostic starting point，而且当前主问题确实不是“scene system 不成立”，而是 board framing 还不够 editorial。

当前剩余问题可明确命名为：

- `slight-board-literalness`

这说明：

- skill 已经能避免 classroom / physical whiteboard / dashboard drift
- 也已经能把 learning flow 收成 `failure -> correction -> next input -> improved output`
- 剩下的是更后段的 publishability polish

## Updated Operational Judgment

在这两条新增 exploratory run 之后，当前系统级判断应更新为：

1. generalized exploratory claim 现在更厚了
   - 不再只靠一条 `protocol explainer poster`
   - 已至少覆盖：
     - `protocol explainer poster`
     - `editorial report cover`
     - `educational visual board`
2. 当前 exploratory lane 的主要 open gap 已继续收窄
   - 不再是“新场景首轮拿不到 diagnostic start”
   - 而是不同资产类型各自还残留少量 asset-identity 或 editorial-finish 问题
3. `slight_ui_board_literalness` 的优先级判断仍成立
   - 它在新 educational board 里再次出现
   - 但已经表现为 `conditional_pass` 之后的尾部 polish，而不是高层协议阻塞

## Preliminary Promotion Signal

虽然本轮还没有正式产出独立的 promotion decision note，但已经出现了第一批真实 promotion 信号。

当前最接近 `exploratory -> standard` 门槛的方向，不是 `educational board`，而是：

- `editorial protocol/report collateral`

原因是：

1. 它已经显示出明确可复述的借用方式
   - `masthead-safe editorial cover skeleton`
   - `brief packet / route trace / score chips / report-cover plate`
2. candidate 已经达到：
   - `83.5 conditional_pass`
3. 当前剩余问题很窄
   - 不是 scene identity 错位
   - 而是 subordinate fragment 的 report-native 程度还可继续收紧

但当前仍不应直接 promotion，原因也很明确：

- 证据还主要集中在单一 cover run
- 还缺同方向的第二条 transfer 或 repair 支撑
- 还没有单独做 grouped review

因此，最准确的当前判断是：

> `editorial protocol/report collateral` 已经成为新的 `exploratory -> standard` 近门槛候选，但现在仍应先保持 `exploratory`。

## M11 Standard Transfer Snapshot

在 exploratory unmatched-scene evidence 做厚之后，本轮又完成了两条 `standard transfer`。

对应记录：

- `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-knowledge-product-poster.md`
- `docs/benchmarks/benchmark-run-2026-04-22-standard-transfer-onboarding-learning-asset.md`

当前最重要的结果是：

> standard lane 现在不只是“理论上应该能借用已有规则”，而是已经在 `knowledge-product poster` 和 `onboarding-adjacent learning asset` 这两类相邻场景上被真实跑通。

### Standard Transfer 1. Knowledge-Product Poster

这条 run 选择的是：

- `domain_direction: knowledge-product poster for an AI design-operations field guide`
- `matched_profile: custom`
- `support_tier: standard`

结果可收束为：

- baseline：`78.0 conditional_pass`
- candidate：`89.5 pass`

最重要的判断是：

> `protocol-native editorial collateral` 规则已经不再只停在 exploratory collateral，而是能稳定迁移到 knowledge-product launch poster。

### Standard Transfer 2. Onboarding Learning Asset

这条 run 选择的是：

- `domain_direction: onboarding-adjacent learning asset for a mobile AI image app`
- `matched_profile: custom`
- `support_tier: standard`

结果可收束为：

- baseline：`81.0 conditional_pass`
- candidate：`89.5 pass`

最重要的判断是：

> `app-asset` 邻近场景的 transfer 也已经成立，而且 protocol-native teaching flow 没有把资产拉成 dashboard mockup。

## M11 Delivery-Heavy Snapshot

本轮还补了一条真正需要 delivery judgement 的验证。

对应记录：

- `docs/benchmarks/benchmark-run-2026-04-22-delivery-heavy-event-signup-poster.md`

场景为：

- `event signup poster base for an AI image prompt clinic`

当前最重要的判断是：

> 当前 skill 已经能稳定长出可信 `text_safe_visual`，但从 `text_safe_visual -> delivery_ready_visual` 仍缺低摩擦执行链路。

结果可收束为：

- baseline：`71.0 fail`
- candidate：`85.5 pass`

但这里的 `pass` 不是说“直接交付完成”，而是说：

- delivery-heavy validation 成功
- `text_safe_visual` 已成立
- 阻塞点已被明确定位到：
  - title/date/CTA overlay
  - QR / logo precision overlay
  - size adaptation

## M11 Promotion And Toolization Judgment

在上述新增样本之后，本轮已经形成三份正式判断文档：

- `docs/profile-promotion-judgment-2026-04-22-m11.md`
- `docs/delivery-toolization-priority-2026-04-22.md`
- `docs/sync-automation-scope-2026-04-22.md`

其中最关键的系统判断有三条：

1. `protocol-native editorial / knowledge collateral`
   - 正式从 `exploratory` 晋升到 `standard`
2. `educational visual board`
   - 继续 `hold in exploratory`
   - 当前主要剩余问题仍是 `slight-board-literalness`
3. delivery layer 的工具化优先级已经明确
   - `text-safe -> delivery-ready` 版本化
   - fixed-element overlay
   - size adaptation

## Current End-Of-M11 Judgment

截至当前，M11 最关键的新增事实应收束为：

1. generalized validation surface 已明显变厚
   - exploratory unmatched scenes 已不再只有一条
   - standard transfer 也已有两条真实通过
2. profile promotion policy 已从文档进入真实判断
   - 至少已有一条方向被正式晋升到 `standard`
3. delivery toolization priority 已不再模糊
   - 当前首要矛盾不是继续 polish 单张图
   - 而是把 `text_safe_visual` 稳定推进成 `delivery_ready_visual`
4. sync automation scope 已有最小边界
   - manifest
   - narrow drift check
   - one-command sync
   - hard exclusions

因此，当前项目最准确的状态不是：

- “还在补 prompt 小修”

而是：

> generalized system 已经跨过“协议成立”阶段，进入了“validation / promotion / delivery / sync 开始真实运营化”的阶段。

## Delivery Bundle Versioning v1 Snapshot

在上述判断之后，delivery layer 已经补上第一版可执行 versioning 基座。

对应实现：

- `references/delivery-bundle-contract.md`
- `scripts/delivery_bundle_lib.py`
- `scripts/manage_delivery_bundle.py`

当前最重要的新事实是：

> `raw_visual -> text_safe_visual -> delivery_ready_visual` 已经不再只存在于 delivery docs 里，而是能以 bundle manifest + state version 的形式被真正登记、追踪和回放。

这次实现解决的不是 overlay 本身，而是 overlay 之前最缺的那条资产管理链：

- 每个 state 单独版本号
- latest pointer 明确
- parent lineage 明确
- overlay / size adaptation 有固定挂点

因此，delivery layer 现在更准确的状态应是：

- 不再是“纯规则层”
- 而是“versioning 已落地，overlay 与 size adaptation 仍待接入”

当前新的默认实现顺序应收束为：

1. 用 bundle contract 管理 `raw_visual / text_safe_visual / delivery_ready_visual`
2. 在 bundle 上接 fixed-element overlay
3. 再把 size adaptation 接到 `delivery_ready_visual` fan-out

## Delivery Execution Snapshot

在 versioning 基座之后，delivery layer 的后两层也已经补上第一版执行链。

对应实现：

- `scripts/apply_delivery_overlay.py`
- `scripts/export_bundle_sizes.py`
- `scripts/delivery_image_ops_lib.py`

当前最重要的新事实是：

> 现在已经可以从最新 `text_safe_visual` 直接落标题、日期、CTA、logo、QR，登记新的 `delivery_ready_visual`，并继续从这个版本做多尺寸导出。

这意味着：

1. `text_safe_visual -> delivery_ready_visual`
   - 已经不再只靠人工回忆或临时覆盖文件
   - 而是有 bundle 内 working file、registered version 和 metadata
2. size adaptation
   - 已经能从最新 `delivery_ready_visual` 做 `safe_pad` fan-out
   - 导出结果和 export run 都会回写到 bundle
3. delivery layer 的当前真实状态
   - 不再是“只有 versioning”
   - 而是“versioning + overlay + size export 都已有可执行第一版”

这轮 smoke validation 还暴露并修掉了一个真实 bug：

- 粗体中文字体回退错误导致标题与 CTA 出现方块字

修复后结果说明：

- 当前实现不是纸面闭环
- 而是真正经过一轮交付 smoke 验证的最小 delivery chain

## QR Replacement Validation Conclusion

在上面的 smoke delivery chain 之后，本轮又补了一次更强的真实替换验证。

验证输入：

- 一张用户提供的微信样式群二维码
- 一张用户提供的标准外部二维码

最重要的结论应收束为：

> 二维码替换链路本身已经成立；微信样式群二维码更像是码制与解码器兼容性的特例，而不是 delivery chain 失效。

这次验证进一步说明了三点：

1. bundle 内替换二维码是稳定成立的
   - 可从 `text_safe_visual` 读底图
   - 替换真实二维码
   - 生成新的 `delivery_ready_visual`
   - 不污染源母版
2. 对标准二维码，当前验证已经达到强结论
   - 输入码可解码
   - 主交付图可解码
   - `1080x1350`
   - `1920x1080`
   - `1200x628`
   - 这三种 safe-pad 导出版也都可解码
3. 当前系统级判断应更新为
   - “二维码能不能替换”这件事已经不是 open issue
   - 这条链路现在可以视为已验证能力

因此，delivery layer 当前不应再把“QR replacement feasibility”视为主缺口。

更准确的当前缺口应是：

- 更复杂真实资产上的 typography / zone calibration
- 非二维码类 fixed element 在更多真实素材上的稳定性
- 更大样本面的 real-asset hardening，而不是二维码替换本身

## Current Gap Reassessment Vs Expected Goal

如果把这次 delivery validation 也算进来，当前项目与“之前预期目标”之间的差距应进一步收窄。

现在已经达到的部分是：

1. delivery layer 已不再只是文档
   - versioning
   - fixed-element overlay
   - size export
   - QR replacement verification
   都已经有真实执行链
2. 二维码替换链路已被真实验证
   - 主图成立
   - 标准二维码在多尺寸导出里也成立
3. “怎么把已经成立的图推进成可交付资产”这条主路径
   - 已经不是抽象设计题
   - 而是可执行系统

## Runtime Compounding Mechanism Snapshot

如果把 runtime / promotion 这一层也按最新事实收口，当前结论应是：

> 本地经验积累机制已经真实运行，但当前仍属于“半自动运行”，还没有自动晋升到可直接影响本地 skill 判断的层。

当前已经成立的事实包括：

1. runtime 不是空壳
   - 已有真实 capture
   - 已有 review queue
   - 已有 field notes
   - 已有 promotion runs
2. 积累不是停在原始日志
   - 已经有可复用 field note
   - 已经能通过 `read_runtime_context` 读取本地经验
3. 但当前默认行为仍然是：
   - 写 capture 有能力，也有真实运行
   - review / promotion 仍依赖显式脚本调用
   - field note 不会自动回写成“本地 skill 默认参考层”

因此，当前最准确的机制判断不是：

- “经验机制还没成立”

而是：

- “经验机制已成立，但自动化深度还不够”

## Local Auto-Promotion Direction

基于当前阶段判断，runtime 这一层接下来最值得补的，不是再证明 capture / review 能不能跑，而是把晋升边界收清楚：

1. `local runtime -> local skill reference layer`
   - 应该允许自动晋升
   - 目标是让本地已验证经验自动影响后续 skill 使用
2. `local runtime -> repo / GitHub public rule layer`
   - 不应自动晋升
   - 应继续由人工审核和人工判断决定

一句话边界：

> 本地经验层应该自动影响本地 skill；公开到 GitHub 的 repo 规则层仍应继续人工审核。

当前离预期目标真正还差的，主要收束为 4 类：

1. real-asset hardening 还不够厚
   - 当前有真实 run
   - 但还缺更多真实 logo / copy / multi-element 资产去校准 zone 与排版策略
2. generalized validation thickness 还不够
   - delivery 这条链已经有了
   - 但 scene generalization 和 promotion 还需要更多真实样本继续做厚
3. promotion thickness 还不够
   - policy 和第一批 judgment 已有
   - 但跨更多方向的真实升档案例仍偏少
4. sync automation 仍未落地
   - 边界和范围已明确
   - 但 drift check / manifest / one-command sync 还没做成真实工具

一句话更新版判断：

> 当前项目与预期目标之间的主要差距，已经不再是 local auto-promotion 本身，而是 real-asset hardening、validation thickness、promotion thickness，以及 sync automation。
