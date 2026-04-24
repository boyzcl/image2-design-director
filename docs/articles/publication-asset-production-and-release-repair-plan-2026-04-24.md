# Publication Asset Production And Release Repair Plan

## Background

这份方案修复 `image2-design-director` 在文章配图、公众号头图、正文机制图和 workflow evidence 图上的一个核心缺口：

> 之前的链路主要修了“结果如何验证”，但没有足够修“制作过程如何正确执行”。

当前三张文章图已经证明，`publication_review = pass` 可以保证资产身份、场景、残留元素和 metadata 大体正确，但不能保证图面本身已经达到发布级。更严重的是，如果生产前没有明确 figure role、representation route、文字预算和 drift boundary，Agent 仍然会用错误路线生成图片，然后只靠后置 review 拦截。

所以这次修复必须同时覆盖两段：

1. `production protocol`
   - 让 Agent 在制作前知道这张图该怎么做。
2. `release protocol`
   - 让流程上看似通过但图面不过线的资产不能进入用户可见输出。

## Target Chain

新的文章配图链路必须是：

```text
asset contract
-> production packet
-> production preflight
-> representation strategy
-> generation / deterministic render / hybrid overlay
-> delivery bundle
-> delivery viability
-> publication identity review
-> visual quality review
-> final release gate
-> user-facing output / article insertion
-> runtime capture
```

`publication_review` 不再等于最终可发布。它只证明资产身份正确。

最终可发布必须同时满足：

- `production_preflight_result = pass`
- `publication_review_result = pass`
- `visual_quality_review_result = pass`
- `final_release_result = pass`
- 有完整 runtime capture 或明确豁免原因

## Production Layer Repair

### 1. Production Packet

每张文章图生成前必须形成一个 production packet。

最小字段：

```yaml
figure_role: editorial_cover | mechanism_figure | workflow_evidence
asset_goal: 这张图支撑文章里的哪一个论点
representation_mode: image_model | visual_base_plus_post | hybrid_visual_plus_deterministic_overlay | deterministic_render
layout_owner: model | deterministic_renderer | hybrid
text_owner: model | deterministic_overlay | deterministic_renderer
text_budget:
  headline: 1
  subtitle: 0-1
  node_labels: number
  paragraphs: 0
visual_structure: 该图应该采用的结构
forbidden_drift:
  - benchmark artifact
  - generic README hero
  - event poster
candidate_policy: single | multi_candidate
repair_policy: micro_repair | regenerate | contract_realign
```

### 2. Figure Role Defaults

#### Figure A. Editorial Cover

- default route: `hybrid_visual_plus_deterministic_overlay`
- visual base owner: image model
- text owner: deterministic overlay
- candidate policy: `multi_candidate`
- must avoid:
  - model-rendered long Chinese headline
  - pure schematic deterministic cover unless explicitly chosen
  - report-page dullness

Production intent:

> 先获得有封面张力的 publication visual base，再用确定性排版叠中文标题。

#### Figure B. Mechanism Figure

- default route: `deterministic_render` or `hybrid_visual_plus_deterministic_overlay`
- layout owner: deterministic renderer
- text owner: deterministic renderer
- candidate policy: `single` allowed only after wireframe
- must avoid:
  - paragraph-heavy cards
  - broken English labels
  - dense explanatory copy inside cards
  - decorative workflow board

Production intent:

> 图内只放机制节点和极短标签，解释性文字放文章正文或图注。

#### Figure C. Workflow Evidence

- default route: `hybrid_visual_plus_deterministic_overlay`
- visual base owner: image model
- text owner: deterministic overlay
- candidate policy: `multi_candidate`
- must include concrete evidence objects:
  - capture record
  - scorecard
  - delivery bundle
  - route trace
  - accepted output state
- must avoid:
  - abstract radar decoration
  - generic device mockup cluster
  - README hero drift

Production intent:

> 让读者看到“这套 skill 已进入真实工作流”，而不是看到一张抽象流程装饰图。

### 3. Production Preflight

进入生成前必须跑 `production_preflight`。它检查：

- `figure_role` 是否明确
- `asset_goal` 是否绑定文章论点
- route 是否匹配 figure role
- text owner 是否合理
- text budget 是否过载
- 是否有 forbidden drift
- candidate policy 是否满足该角色

硬拦截例子：

- cover 用 `deterministic_render` 且没有明确豁免：`cover_visual_energy_risk`
- mechanism figure 出现 paragraph cards：`mechanism_text_density_too_high`
- workflow evidence 没有 evidence objects：`workflow_evidence_objects_missing`
- 文章图把长中文交给模型直出：`model_text_ownership_risk`

## Release Layer Repair

### 1. Publication Identity Review

现有 `publication_review` 保留，但职责收窄为：

- 是否文章场景
- 是否正确 asset role
- 是否 `complete_asset`
- 是否无 CTA / QR / event residue
- 是否不是 benchmark / overlay demo / internal artifact
- 是否具备 required protected regions

它不能单独决定最终可发布。

### 2. Visual Quality Review

新增 `visual_quality_review`。它回答：

> 这张具体图的视觉、文字和语义表达是否已经达到 publication-ready。

维度：

| Dimension | Meaning |
|---|---|
| `text_readability` | 文字是否清楚、无异常断行 |
| `typographic_craft` | 字体、行距、字号、层级是否成熟 |
| `layout_hierarchy` | 标题、主体、辅助信息是否稳定 |
| `semantic_clarity` | 读者能否理解图在表达什么 |
| `publication_argument_support_visual` | 图像本身是否支撑文章论点 |
| `series_consistency` | 同组图是否一致但不模板化 |
| `asset_distinctiveness` | 是否具备该图角色的独特性 |
| `polish_and_finish` | 是否像真实可发布资产 |

默认结果：

- `pass`: 分数 >= 85 且无 blocker
- `conditional_pass`: 分数 70-84 或存在可修复 blocker
- `fail`: 分数 < 70 或存在 hard blocker

硬 blocker：

- broken word
- broken Chinese line
- paragraph overload
- template sameness
- weak article support
- internal draft look

### 3. Final Release Gate

新增 `final_release_gate`。它只回答一个问题：

> 这张图能否进入用户可见输出、正文、README 或成功样张。

规则：

```text
final_release_result = pass
only if:
production_preflight_result == pass
and publication_review_result == pass
and visual_quality_review_result == pass
and delivery_viability_result != overlay_not_allowed_regenerate
and runtime_capture_present == true
```

否则最多是 `conditional_pass`，不能用户可见。

## Current Asset Reclassification

当前三张图应降级为最多 `conditional_pass`，如果单张图命中硬视觉 blocker，则应进一步降为 `fail`：

- `publication_review_result = pass`
- `visual_quality_review_result = conditional_pass | fail`
- `final_release_result = conditional_pass | fail`

原因：

- 它们证明了 publication metadata 和 bundle 机制可工作。
- 但图面存在文字断行、模板化、封面张力不足、workflow evidence 证据感不足等问题。
- 它们不能继续作为最终高质量样张。

## Verification Plan

至少验证 5 件事：

1. 正确的 mechanism production packet 能通过 preflight。
2. paragraph-heavy mechanism packet 会被 preflight 拦下。
3. metadata pass 但 visual quality 差的资产会被 final release gate 拦下。
4. 当前三张历史图被标记为 `final_release_result = conditional_pass`。
5. 没有 runtime capture 的 final asset 不能被标成 `final_release_result = pass`。

## Completion Definition

本轮修复完成的标准：

- 方案文档已落库。
- production protocol 已落到 reference。
- production preflight 有可执行脚本。
- visual quality review 有可执行脚本。
- final release gate 已进入代码。
- 当前三张图的 bundle metadata 已重写为 conditional release。
- 有 benchmark / smoke 记录证明上述规则生效。
