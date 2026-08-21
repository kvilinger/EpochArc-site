# EpochArc 语言规范

**版本**：v1.0  
**更新日期**：2026-07-21  
**适用范围**：事件详情页、方向页面、专题页面及所有公开文案的中英文书写。

> 本文档是 [STYLE-GUIDE.md](STYLE-GUIDE.md) 的可操作扩展。STYLE-GUIDE.md 定义原则，本文档定义具体句法模式、可检测的"AI 味"清单和模块级差异。

---

## 目录

1. [核心原则](#1-核心原则)
2. [英文句法规则](#2-英文句法规则)
3. [中文句法规则](#3-中文句法规则)
4. [AI 味检测清单](#4-ai-味检测清单)
5. [模块差异](#5-模块差异)
6. [时间锚点规则](#6-时间锚点规则)
7. [常用词汇对照表](#7-常用词汇对照表)
8. [校对检查项](#8-校对检查项)

---

## 1. 核心原则

### 1.1 同一段文字只表达一个核心信息

- 好：`OpenAI released ChatGPT, a conversational AI product based on GPT-3.5, free to the public. It reached 1 million users in 5 days.`
- 不好：`ChatGPT represented a paradigm shift in conversational AI and was released by OpenAI in 2022, changing how millions of people interacted with AI.`

### 1.2 用具体信息代替抽象评价

| 抽象评价 | 具体信息 |
|---------|---------|
| 改变了行业格局 | 达到 1 亿用户、引发监管议程变化、被 X 家公司采用 |
| 具有重要意义 | 获得诺贝尔奖、触发 5930 亿美元市值蒸发、被 Nature 收录 |
| 快速普及 | 5 天达到 100 万用户、2 个月达到 1 亿用户 |

### 1.3 优先使用事件页语言，而非方向页或营销语言

- 事件页：陈述已发生的事实及其可观测影响
- 方向页：基于已发生信号的观察，不描述未来
- 禁止使用营销、投资或媒体评论中的语言（"震撼世界"、"颠覆一切"）

### 1.4 英文为原文，中文为翻译

所有公开内容先以英文写作（英文最接近来源事实），再翻译为中文。中文不是独立的创作版本，但也不应逐字直译。

---

## 2. 英文句法规则

### 2.1 基本句型模板

事件详情页的摘要和叙述遵循以下句型结构：

```
[主体] [动词过去式] [直接宾语] [时间/方式状语].
```

- 正确：`OpenAI released ChatGPT on November 30, 2022.`
- 正确：`Meta laid off 8,000 employees in May 2026.`
- 正确：`The EU Parliament passed the AI Act on March 13, 2024.`

方向页 thesis 使用现在进行时或现在时：

```
[主体] [动词进行式/一般时] [方向性短语].
```

- 正确：`Software development is evolving from one-off AI assistance toward coordinated processes.`
- 正确：`Agentic systems are being deployed across real business tools.`

### 2.2 首句必须是事实句

段落首句应该直接陈述一个可验证事实，而非做出评价后再补充事实。

- 正确：`OpenAI retired GPT-4o on February 13, 2026.`
- 更差：`In a controversial move that angered many users, OpenAI retired GPT-4o on February 13, 2026.`

评价性内容应放在后续句子或 `narrative` 段落中。

### 2.3 避免以"What matters now"开头

方向页中常见但错误的句式：

```
What matters now is whether these capabilities stay as demos...
What matters now is whether embodied AI is leaving the demo circuit...
```

改为：

```
The open question is whether these capabilities remain at the demo stage...
The relevant question is whether embodied AI is entering real operating environments...
```

### 2.4 "is moving from...toward..." 的使用限制

这类句式在方向页 thesis 中只能使用一次。避免嵌套：

- 正确：`Robots are moving from staged demonstrations into commercial environments.`
- 更差：`The shift is about robots moving from demos toward commercial environments where the shift toward operational deployment is accelerating.`

### 2.5 避免"already"填充

- 正确：`AI coding tools operate in production environments. Code generation is commercially deployed.`
- 更差：`AI coding tools are already embedded in real development environments. Code generation is no longer just an experiment.`

只有需要明确强调"不是未来的事"时才使用 `already`。

### 2.6 动词选择

| 推荐 | 避免 |
|-----|------|
| released, launched, published, announced | unveiled, dropped, debuted |
| laid off, cut, eliminated | axed, slashed, got rid of |
| reached, achieved, crossed | hit, smashed, crushed |
| proposed, introduced, released | revolutionized, transformed |
| demonstrated, showed, indicated | proved (除非有严格证明) |
| affected, changed, shifted | disrupted, upended |
| contributed to, played a role in | fundamentally altered |

---

## 3. 中文句法规则

### 3.1 避免"把"结构

- 正确：`SpaceX 于 2026 年 2 月 2 日宣布已收购 xAI。`
- 更差：`SpaceX 于 2026 年 2 月 2 日把 xAI 收购了。`

只有必须强调"对某个对象的处置"时才使用"把"，通常可以用直接宾语+动词替代。

### 3.2 避免无主语"让"结构

- 正确：`智能体在邮件、ERP 和工单系统之间执行固定工作流。`
- 更差：`让智能体在邮件、ERP 和工单系统之间自动跑固定流程。`

中文疑问："谁让"？如果不需要回答这个问题，就不要用"让"开头。

### 3.3 避免"不只是...还在...(和/并)"的长串谓语

- 正确：`AI 编程工具已参与拆解任务、生成代码、运行测试和持续维护。`
- 更差：`AI 编程工具已经不只是补全代码，还在参与拆任务、写代码、跑测试和做维护。`

多个动词并列时：
- 使用名词化：`参与拆解任务、生成代码和运行测试`
- 不使用：`不只是...还在...并...以及还要...`

### 3.4 避免"什么..."型反问或模糊问句

方向页 openQuestions 中使用：

- 正确：`什么公开证据能表明企业对智能体的信任已经超越试点？`
- 更差：`什么样的证据才能说明企业真的信任...？`

去掉"才能"、"真的"、"才"等情绪化修饰。

### 3.5 主语使用明确实体而非抽象概念

- 正确：`AlphaFold 及其后续的诺贝尔奖认可表明...`
- 更差：`AI 成为科学工作底座这件事已经越来越成为共识...`

### 3.6 事件页中文模板

```
[主体] [于时间] [动词] [直接宾语]。
```

- `OpenAI 于 2022 年 11 月 30 日发布了 ChatGPT。`
- `Meta 于 2026 年 5 月裁员 8,000 名员工。`

方向页中文模板：

```
[主体] [正在/已] [动词] [宾语]，[补充说明]。
```

- `具身 AI 正从舞台演示进入商业环境。`
- `智能体系统正部署于真实业务工具。`

### 3.7 避免"着"、"了"、"过"滥用

- 不带"了"：`AI 编程工具已参与拆解任务。`
- 错误使用"着"：`代表着...开始着...持续着...`

中文的事件描述使用"已"或"于...发布"等明确时间标记，比"了"、"着"、"过"更清晰。

### 3.8 "很"、"非常"、"十分"、"极其"

不用。需要强调程度时用具体数据：

- 正确：`验证成本仍然较高。`
- 更差：`验证成本非常高。` --> `目前一次全栈验证约需 $X 和 Y 天。`

---

## 4. AI 味检测清单

以下是中英文文案中最常见的 AI 翻译痕迹。如果以下特征超过 2 个出现在一段文案中，必须重写。

| # | 特征 | 英文原文 | AI 翻译 | 人工改写 |
|---|------|---------|--------|---------|
| 1 | 无主语"把"结构 | — | `把机器人从演示和试点带到仓库` | `机器人正在仓库、工厂和服务现场接受测试` |
| 2 | 无主语"让"结构 | — | `让智能体在系统之间跑流程` | `智能体在系统之间执行固定工作流` |
| 3 | "不只是...还在..." | `not only...but also` | `AI 不再只是科学工具，还在进入发现流程` | `AI 正在成为发现工作流的一部分` |
| 4 | "已经...不再只是..." | `no longer just` | `AI 已经不再只是辅助工具` | `AI 已从辅助工具演进为核心基础设施` |
| 5 | "在...那里，才是关键" | `where...matter` | `在那里部署和工作流集成才是关键` | `部署可靠性、运行时长和工作流集成是真正的衡量标准` |
| 6 | 套嵌"是否"结构 | `whether...or...` | `真正的变化不是 AI 会不会写代码，而是软件工作是否会...` | `问题不在于 AI 能否生成代码，而在于...` |
| 7 | "什么样的...才能说明" | `What evidence would show...` | `什么样的证据才能说明团队信任 AI` | `什么证据能说明团队信任 AI` |
| 8 | 长串并列动词 | `help plan, write, run, and handle` | `不只是补全代码，还在参与拆任务、写代码、跑测试和做维护` | `已参与拆解任务、生成代码、运行测试和持续维护` |
| 9 | "真正值得看的是" | `What matters now is` | — | `待观察的是` / `关键在于` |
| 10 | "走"系动词 | — | `走向闭环`、`走出试点`、`走进环境` | `转向`、`离开`、`进入` |

### 快速检测方法

写完后用以下问题自查：

1. 这段中文可以直接逐句对应回英文吗？→ 如果是，很可能有 AI 味。
2. 去掉"已经"、"正在"、"开始"后，句子是否仍然成立？→ 如果成立，去掉。
3. 这段话去掉第一句是否影响读者理解？→ 如果第一句只有铺垫作用，删除或合并。
4. 这段话用一个具体事件/数据替换抽象表述后，是否更清晰？→ 如果是，替换。

---

## 5. 模块差异

不同模块对语言的要求有系统性差异。

### 5.1 事件详情页

- 严格事实驱动
- 中文使用"于...发布"、"就...达成"等明确时间标记
- `searchSummary` 是标题下的核心导语：用 1-2 句概括事件，不承担完整摘要职责
- `summary` 是完整事件摘要：交代时间、主体、动作、直接结果和必要的事实边界
- `narrative` 是背景与脉络：可包含有证据支持的判断性语言，但必须与事实句分开
- 详情页按 `searchSummary` → `summary` → `narrative` → `claims` / `impacts` / `sources` 逐层展开，不得用短导语替代完整摘要
- 影响评估使用结构化 `ImpactAssessment[]`，不在自由文本中重复

### 5.2 方向页面

- thesis：1 句声明式现在时，说明方向性变化
- currentBaseline：**只能写"已经发生且可验证"的内容**
- whyThisDirection：以`关键问题在于`/`待观察的是`/`相关问题是`开头
- counterSignal：不能写成"不是...而是"的对称论证，应直接列出具体障碍
- openQuestions：以"什么"开头的不完整句，不能包含夹带预设（"到什么程度才能说明..."）

### 5.3 方向页面卡片列表

- thesis 控制在 20 个英文词以内
- 方向描述只写谓语动词（使用动宾结构而非完整句）
- 卡片元数据（时间窗、信号数、证据等级）不嵌入文案判断

### 5.4 专题页面

- 专题标题使用名词性短语：`Transformers Empire` 而非 `How Transformers Changed Everything`
- 专题描述应包含明确的日期边界（covered period）

---

## 6. 时间锚点规则

### 6.1 事件页

事件页中的每一个事实句，原则上应包含：

1. 主体
2. 动词（过去时）
3. 时间标记

```text
SpaceX agreed to acquire Cursor for $60 billion on June 16, 2026.
```

如果上下文已经建立了时间框架，后续句子可以不重复时间：

```text
OpenAI released ChatGPT on November 30, 2022. It reached 1 million users in 5 days.
```

但时间跨度过大时必须重新锚定：

```text
...By January 2023, it had reached 100 million users.
```

### 6.2 方向页

方向页 thesis 使用现在时，不绑定具体日期。但：

- `currentBaseline` 中的每个事实句必须可追溯到事件或来源日期
- 每个 signal 的 `summary` 须包含具体事件及其日期
- 不能出现"目前"、"最近"、"今年"等相对时间词——必须写出具体日期或术语

| 错误写法 | 正确写法 |
|---------|---------|
| 最近发表在 Nature 上 | Nature 于 2026 年 3 月发表 |
| 今年早些时候 | 2026 年 4 月 |

---

## 7. 常用词汇对照表

### 7.1 公司/组织主体

| 英文 | 中文 |
|-----|------|
| OpenAI | OpenAI（不译） |
| Anthropic | Anthropic（不译） |
| Google DeepMind | Google DeepMind |
| Meta | Meta（不译） |
| Microsoft | 微软 |
| European Union | 欧盟 |
| xAI | xAI（不译） |

### 7.2 时间副词

| 英文 | 中文 |
|-----|------|
| subsequently | 随后 |
| over the following months | 在随后的数月间 |
| within days | 数日内 |
| as of July 2026 | 截至 2026 年 7 月 |
| prior to | 在...之前（少用） |

### 7.3 因果动词

| 英文 | 中文 |
|-----|------|
| triggered | 引发、触发 |
| led to | 导致、促使 |
| resulted in | 造成 |
| contributed to | 助力、促成 |
| sparked | 引发（热议、讨论） |
| reinforced | 强化、加强、巩固了...判断 |

---

## 8. 校对检查项

### 8.1 中文校对

- [ ] 有没有直接对应英文句法结构的中文？（AI 味标志）
- [ ] 有没有"把"、"让"开头的无主语句？
- [ ] 有没有"不只是...还在..."、"已经...不再只是..."、"什么样的...才能"结构？
- [ ] "了"在句尾出现超过一次？
- [ ] 有"走"系动词（走向、走出、走进）？
- [ ] 有没有"目前"、"最近"、"今年"等无日期锚点的相对时间词？

### 8.2 英文校对

- [ ] 首句是否直接陈述可验证事实？
- [ ] 有没有"What matters now"、"The important shift"等促销式开头？
- [ ] "already"出现超过一次？
- [ ] 评价性语言是否混入事实句？
- [ ] 方向页 thesis 是否是声明式现在时？
- [ ] event page narrative 中的判断是否有数据或来源支撑？

### 8.3 跨模块校对

- [ ] 方向页没有写成营销语言或投资研报
- [ ] 方向页的信号 summary 包含具体事件引用
- [ ] 事件页的 `narrative` 没有推测未来
