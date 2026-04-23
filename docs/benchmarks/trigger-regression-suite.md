# Trigger Regression Suite

## Purpose

这份文档定义 `image2-design-director` 的最小触发回归面。

它不验证出图质量，而是专门检查下面这件事：

> 哪些请求应该稳定触发这个 skill，哪些不应该，哪些属于需要继续观察的边界场景。

一句话版本：

> 每次修改 `SKILL.md` 的 `description`、`强触发信号` 或 README 里的触发说明后，都应该拿这组样例复核一次。

## How To Use

当下面任一项发生时，优先回看这份 suite：

- 修改 frontmatter `description`
- 修改 `强触发信号`
- 修改 README 里的“什么时候优先调用”
- 发现真实使用中出现明显漏触发或误触发

最小检查方式：

1. 逐条看下面的请求
2. 判断当前版本是否会触发
3. 与 `expected_trigger` 对照
4. 如果结果不一致，先改触发边界，再决定是否改工作流

## Pass Rule

最低通过标准：

- `should trigger` 组没有明显漏触发
- `should not trigger` 组没有明显误触发
- `watch boundary` 组至少能给出稳定、一致的判断理由

如果新增触发规则只让“该触发”变多，但也同时把“不该触发”的样例吸进来，这不算通过。

## Suite

### Group A. Should Trigger

这些请求应该稳定触发 `image2-design-director`。

#### trg_01_reference_locked_subject_swap

- expected_trigger: `yes`
- request:
  - “照这个版本和风格复刻一张，但把蝴蝶换成青蛙，信息图结构和版式不要变。”
- why:
  - 这是典型的 `reference-locked remake`，不能只当普通生图。

#### trg_02_series_extension_same_system

- expected_trigger: `yes`
- request:
  - “沿用这一套 README 视觉系统，再补两张同系列机制图，风格、信息密度和构图语言保持一致。”
- why:
  - 这是 `series extension`，重点是系列感和系统一致性。

#### trg_03_template_bound_explainer_board

- expected_trigger: `yes`
- request:
  - “帮我做一张中文教育信息图海报，分成 8 个编号模块，讲清楚青蛙的生命周期、结构和栖息地。”
- why:
  - 这是 `template-bound explainer asset`，带明显版式和信息密度约束。

#### trg_04_delivery_heavy_finished_asset

- expected_trigger: `yes`
- request:
  - “做一张活动海报，必须是完整可用成品，要有中文主标题、副标题、二维码位置、logo 安全区，并同时给我 `4:5` 和 `1:1` 两个版本。”
- why:
  - 这是 `delivery-heavy finished asset`，约束多且目标是成品交付。

#### trg_05_repair_existing_off_target_asset

- expected_trigger: `yes`
- request:
  - “这版图方向基本对了，但不像成品，文字也乱了，帮我判断是该小修还是重新理解后再做。”
- why:
  - 这是典型的 `repair / contract_realign` 入口。

#### trg_06_high_design_bar_social_asset

- expected_trigger: `yes`
- request:
  - “给我做一张品牌发布图，不要太 AI 味，要像设计团队真的会发出去的东西。”
- why:
  - 虽然没有参考图，但明确要求高设计可用性和真实商业成品感。

### Group B. Should Not Trigger

这些请求默认不该触发 `image2-design-director`。

#### trg_07_simple_fun_image

- expected_trigger: `no`
- request:
  - “帮我画一只可爱的卡通青蛙头像，随便一点，发群里玩。”
- why:
  - 轻量、低风险、一次性趣味出图，不需要设计导演层。

#### trg_08_plain_wallpaper_generation

- expected_trigger: `no`
- request:
  - “生成一张蓝色极简手机壁纸，不要字。”
- why:
  - 没有明显资产合同复杂度，也没有成品交付压力。

#### trg_09_single_fact_edit

- expected_trigger: `no`
- request:
  - “把这张图的背景换成白色。”
- why:
  - 这是窄编辑，不需要完整的合同和路由判断。

#### trg_10_basic_style_variation

- expected_trigger: `no`
- request:
  - “画一只青蛙，水彩风就行。”
- why:
  - 只有对象和风格，没有复杂约束或交付要求。

### Group C. Watch Boundary

这些请求是边界观察项，重点不是绝对 yes/no，而是要有稳定理由。

#### trg_11_ui_mockup_lightweight

- expected_trigger: `lean_yes`
- request:
  - “做一个简洁的 app 登录页 mockup。”
- why:
  - 如果只是随手草图，可能不必触发；如果用户隐含要可信 UI 成品，应该触发。当前版本更适合偏 `yes`，但要看上下文是否真的要求“可信、可用、像产品团队会交付”。

#### trg_12_reference_only_style_mood

- expected_trigger: `lean_yes`
- request:
  - “按这张参考图的感觉做一版差不多的。”
- why:
  - 如果参考图只提供模糊气质，可能还是普通生图；但只要参考图在承担版式、系列感或资产类型锚点，应该触发。当前版本建议偏 `yes`，避免漏掉高风险参考任务。

#### trg_13_clean_base_visual_request

- expected_trigger: `lean_no`
- request:
  - “给我做一个干净的科技感底图，后面我自己加字。”
- why:
  - 这是 `base_visual` 请求，但如果没有更多品牌、版式或交付约束，可能不需要强触发。当前版本建议偏 `no`，除非用户再补充尺寸、系列感或真实交付压力。

## What This Suite Is Trying To Protect

这组回归样例主要保护 3 件事：

1. 不漏掉高误判成本任务
   - 参考锁定重做、系列延展、模板约束说明图、多约束成品交付、结果救火
2. 不把 skill 扩成“所有生图都该触发”
   - 轻量趣味图、普通壁纸、单步小编辑、仅对象加风格的简单请求仍应留在普通生图路径
3. 让边界判断可解释
   - 即使对某些样例仍有讨论空间，也要能稳定说明为什么偏 `yes` 或偏 `no`
