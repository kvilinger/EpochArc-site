# EpochArc 数据模型与内容治理规范

**版本**：v2.0  
**更新日期**：2026-06-24  
**适用范围**：AI 历史时间轴、前瞻预测、来源证据、投票与后续更新流程  
**目标**：让 EpochArc 成为一个可持续维护、可公开解释、可被质疑和修正的 AI 发展记录网站。

---

## 0. 对现有 v1.1 的评估

现有文档的方向是合理的：已经把事件拆成分类、影响维度、重要度、可信度和来源，也意识到不能只靠单一搜索引擎收集内容。这是一个好的第一版骨架。

但如果要长期上线，需要补强以下问题：

1. **事实、影响判断和预测没有完全拆开**  
   历史事件是“已发生事实”，影响评估是“基于证据的解释”，预测是“尚未发生的可检验判断”。三者必须分层，否则可信度会混在一起。

2. **数据字段与真实 JSON 不一致**  
   v1 数据曾同时存在字符串 `title/summary`、旧语言块 `zh/en` 和未规范化的 `impactIndex`。v2 已直接迁移为 `LocalizedText`、来源引用和正式评分字段。

3. **来源字段太薄**  
   当前只存 `title/url/type/date/author`，不足以支撑未来的公开质疑、断链修复、归档、来源分级和中立性审计。

4. **评分口径偏主观**  
   `significance`、`severity`、`consensusLevel`、`impactIndex` 需要可执行的判定标准，否则不同时间补内容时会越来越漂。

5. **预测缺少达成标准**  
   v1 预测只有标题、描述和预计年份。v2 使用 `forecasts.json`，预测必须定义：什么算发生、什么不算发生、看哪些证据、何时裁定。

6. **缺少内容状态和修订记录**  
   公开站点需要知道一条内容是候选、草稿、已审核、已发布还是已废弃；同时要保留关键修订原因。

结论：v1.1 可以作为原型；v2.0 应当成为正式上线前的数据治理基线。

---

## 1. 核心原则

### 1.1 分层表达

每条内容都要区分四层：

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| Fact | 可验证事实 | OpenAI 于 2022-11-30 发布 ChatGPT |
| Claim | 来源中的主张 | “ChatGPT helped popularize generative AI” |
| Assessment | 本站评估 | 该事件是 L3 转折点，影响维度包括普惠化和范式转变 |
| Forecast | 未来判断 | 2027-2029 年可能出现可被公开验证的通用智能系统 |

页面文案可以写得自然，但数据层必须能追踪每个判断来自事实、来源主张还是本站评估。

### 1.2 中立不是没有判断

EpochArc 不是新闻数据库，也不是论文检索器。它允许做判断，但判断必须满足：

- 可解释：为什么是 L2 或 L3，要有评分依据。
- 可追溯：重要判断能回到来源、证据或反方观点。
- 可修正：当新证据出现时，保留更新记录。
- 不装作绝对客观：公开说明这是结构化策展，不是终局裁判。

### 1.3 宁缺毋滥

一个事件宁可暂时留在候选池，也不要因为短期热度直接发布。尤其是：

- 只有社交媒体热度、没有原始来源的内容，不发布为正式节点。
- 单一公司营销说法，只能作为候选，不足以支撑影响评估。
- 对未来的判断必须写成预测，不要伪装成事实。

---

## 2. 正式数据模型

### 2.1 事件：`AIEvent`

```ts
export interface AIEvent {
  id: string;                         // 稳定 ID，如 "chatgpt-2022"
  slug: string;                       // URL 友好 slug，可与 id 相同

  title: LocalizedText;               // 多语言标题
  summary: LocalizedText;             // 2-5 句，说明发生了什么
  narrative?: LocalizedText;          // 展开详情，说明背景、影响和争议

  date: string;                       // YYYY-MM-DD / YYYY-MM / YYYY
  datePrecision: DatePrecision;
  displayDate?: LocalizedText;        // 如 "November 30, 2022"

  category: EventCategory;
  status: ContentStatus;              // candidate / draft / reviewed / published / archived

  significance: SignificanceLevel;    // L1-L3
  impactIndex: number;                // 0-10，按 5.4 规则给出
  consensusLevel: ConsensusLevel;
  controversy: boolean;

  impacts: ImpactAssessment[];
  claims: EventClaim[];
  sources: SourceRef[];
  relatedEvents: string[];
  relatedForecasts?: string[];
  tags: string[];

  editorial: EditorialMetadata;
}

export interface LocalizedText {
  en: string;
  zhHans?: string;
  zhHant?: string;
  ja?: string;
  es?: string;
  fr?: string;
}

export type DatePrecision = 'day' | 'month' | 'year';

export type ContentStatus =
  | 'candidate'
  | 'draft'
  | 'reviewed'
  | 'published'
  | 'archived';

export type SignificanceLevel = 1 | 2 | 3;

export type ConsensusLevel =
  | 'broad'       // 广泛共识
  | 'debated'     // 事实成立，但意义、规模或后果仍有争议
  | 'emerging';   // 新兴判断，证据还在积累
```

#### 直接迁移原则

网站尚未正式上线，因此不保留旧结构兼容层。正式数据直接按 v2 结构维护：

- `title`、`summary`、`narrative` 使用 `LocalizedText`。
- 不再保留顶层字符串 `title/summary`。
- 不再保留旧语言块 `zh/en`。
- `impactIndex` 是正式字段，必须按评分规则解释。
- 事件中的 `sources` 只保存 `SourceRef`；完整来源记录放在 `data/sources.json`。
- 预测统一使用 `data/forecasts.json`，不再使用 `data/predictions.json`。

---

### 2.2 事件主张：`EventClaim`

`claims` 用来把“来源说了什么”和“本站怎么判断”拆开。

```ts
export interface EventClaim {
  id: string;
  text: LocalizedText;
  claimType:
    | 'fact'             // 可验证事实
    | 'impact'           // 影响主张
    | 'limitation'        // 局限或反方观点
    | 'interpretation';   // 解释性判断

  evidenceGrade: EvidenceGrade;
  sourceIds: string[];
  notes?: string;
}

export type EvidenceGrade =
  | 'A'   // 原始来源 + 独立强来源交叉验证
  | 'B'   // 一个原始来源，或两个可靠二级来源
  | 'C'   // 来源可信但证据较薄，适合保守表达
  | 'D';  // 发现信号或单方观点，不应单独支撑正式结论
```

使用原则：

- 每个 L2/L3 事件至少要有 2 条 `claim`：一条事实主张，一条影响主张。
- 如果 `controversy = true`，必须至少有一条 `claimType = limitation` 或反方来源。
- `EvidenceGrade = D` 的内容可以进入候选池，但不应作为正式事件的核心依据。

---

### 2.3 影响评估：`ImpactAssessment`

```ts
export interface ImpactAssessment {
  dimension: ImpactDimension;
  severity: ImpactSeverity;
  direction: 'positive' | 'negative' | 'mixed' | 'neutral';
  description: LocalizedText;
  affectedGroups: string[];
  timeframe: ImpactTimeframe;
  evidenceGrade: EvidenceGrade;
  sourceIds: string[];
}

export type ImpactDimension =
  | 'capability_leap'
  | 'economic_disruption'
  | 'access_democratization'
  | 'risk_creation'
  | 'paradigm_shift';

export type ImpactSeverity = -3 | -2 | -1 | 0 | 1 | 2 | 3;

export type ImpactTimeframe =
  | 'immediate'   // 0-3 个月
  | 'short'       // 3-12 个月
  | 'medium'      // 1-3 年
  | 'long';       // 3 年以上
```

注意：

- `severity` 描述影响方向和强度，不描述确定性。
- 确定性由 `evidenceGrade` 和 `consensusLevel` 表达。
- 如果同一事件既带来普惠化又带来风险，不要写成一个模糊的 0 分；应拆成两个 impact。

---

### 2.4 来源：`Source`

来源使用独立表：`data/sources.json`。事件中只引用 `sourceIds`，不再内嵌完整来源对象。

```ts
export interface Source {
  id: string;                         // 如 "openai-chatgpt-blog-2022"
  type: SourceType;
  tier: SourceTier;

  title: string;
  url: string;
  archiveUrl?: string;
  publisher?: string;
  authors?: string[];
  publishedAt?: string;               // YYYY-MM-DD
  accessedAt: string;                 // YYYY-MM-DD
  language?: string;                  // BCP 47，如 "en", "zh-CN"

  doi?: string;
  arxivId?: string;
  repositoryUrl?: string;
  license?: string;

  independence: SourceIndependence;
  notes?: string;
}

export type SourceType =
  | 'primary'       // 原始论文、官方公告、法规原文、模型卡、代码仓库
  | 'paper'
  | 'official'
  | 'model_card'
  | 'benchmark'
  | 'report'
  | 'news'
  | 'analysis'
  | 'community'
  | 'encyclopedia';

export type SourceTier = 1 | 2 | 3 | 4;

export type SourceIndependence =
  | 'primary_actor'       // 事件参与方或发布方
  | 'independent'         // 独立第三方
  | 'community_signal'    // 社区讨论信号
  | 'unknown';

export interface SourceRef {
  sourceId: string;
  supports: string[];                 // claim id 或 impact id
  quote?: string;                     // 短引用，避免大段摘录
}
```

---

### 2.5 预测：`AIForecast`

预测必须独立建模，不应只靠 `expected + description`。

```ts
export interface AIForecast {
  id: string;
  slug: string;
  title: LocalizedText;
  thesis: LocalizedText;              // 一句话预测命题
  description: LocalizedText;         // 背景说明

  forecastType: ForecastType;
  status: ForecastStatus;
  createdAt: string;
  updatedAt: string;

  expectedWindow: ForecastWindow;
  confidence: ForecastConfidence;

  rationale: ForecastRationale;
  resolution: ForecastResolutionCriteria;

  sources: SourceRef[];
  relatedEvents: string[];
  tags: string[];
  votes?: ForecastVoteSummary;
  editorial: EditorialMetadata;
}

export type ForecastType =
  | 'capability'
  | 'product'
  | 'economic'
  | 'safety'
  | 'policy'
  | 'science'
  | 'infrastructure'
  | 'social';

export type ForecastStatus =
  | 'active'
  | 'resolved_true'
  | 'resolved_false'
  | 'partially_resolved'
  | 'superseded'
  | 'retracted';

export interface ForecastWindow {
  start: string;                      // YYYY / YYYY-MM / YYYY-MM-DD
  end: string;
  precision: DatePrecision;
}

export interface ForecastConfidence {
  level: 'low' | 'medium' | 'high';
  probability?: number;               // 0-100，可选；没有严格校准前不要强行写
  evidenceGrade: EvidenceGrade;
}

export interface ForecastRationale {
  signalsFor: ForecastSignal[];
  signalsAgainst: ForecastSignal[];
  assumptions: string[];
}

export interface ForecastSignal {
  text: LocalizedText;
  sourceIds: string[];
  strength: 1 | 2 | 3;
}

export interface ForecastResolutionCriteria {
  achievedWhen: LocalizedText;         // 达成标准
  notAchievedWhen: LocalizedText;      // 未达成标准
  measurementSources: string[];        // 裁定时优先看的来源类型或具体来源
  minimumDuration?: string;            // 如 "must persist for 90 days"
  adjudicationNotes?: LocalizedText;
}

export interface ForecastVoteSummary {
  totalVotes: number;
  yes: number;
  no: number;
  unsure?: number;
  updatedAt: string;
}
```

预测卡展示时建议显示：

- 预测窗口：例如 `2027-2029`，不要只写单一年份。
- 置信度：低 / 中 / 高，不要早期就伪装成精确概率。
- 达成标准：用可观察指标写清楚。
- 反方信号：至少保留 1 条，避免把预测写成宣传语。

---

### 2.6 编辑元数据

```ts
export interface EditorialMetadata {
  createdAt: string;
  updatedAt: string;
  reviewedAt?: string;
  publishedAt?: string;
  lastSourceCheckAt?: string;
  curator?: string;
  reviewer?: string;
  changeLog?: ChangeLogEntry[];
}

export interface ChangeLogEntry {
  date: string;
  changeType:
    | 'created'
    | 'source_added'
    | 'score_changed'
    | 'translation_changed'
    | 'forecast_resolved'
    | 'correction'
    | 'archived';
  summary: string;
}
```

---

## 3. 来源标准

### 3.1 来源分级

| Tier | 定义 | 可用作 |
| --- | --- | --- |
| 1 | 原始来源：论文、官方公告、模型卡、代码仓库、法规原文、法院文件、公司技术报告 | 事实确认、事件日期、核心能力描述 |
| 2 | 高质量独立来源：主流科技/财经媒体、学术综述、机构报告、监管机构解读 | 影响确认、外部采用、争议背景 |
| 3 | 专家分析与高质量社区整理：研究者博客、专业通讯、会议演讲、行业评论 | 背景解释、趋势线索、候选发现 |
| 4 | 社区热度信号：社交媒体、HN、Reddit、论坛、未核实流言 | 只能用于发现，不可单独支撑正式结论 |

### 3.2 最低来源要求

| 内容类型 | 发布最低要求 |
| --- | --- |
| L1 事件 | 至少 1 个 Tier 1 来源，或 2 个相互独立的 Tier 2 来源 |
| L2 事件 | 至少 1 个 Tier 1 来源 + 1 个独立 Tier 2/3 来源 |
| L3 事件 | 至少 1 个 Tier 1 来源 + 2 个独立 Tier 2 来源；若有争议，必须收录反方来源 |
| 影响评估 | 每个核心影响至少 1 个可追溯来源；L2/L3 影响建议 2 个来源 |
| 预测 | 至少 2 个支持信号 + 1 个反方或限制信号 |
| 投票结果 | 只能显示用户意见，不得作为事实证据 |

### 3.3 来源记录规范

每个正式来源尽量补齐：

- 原始 URL。
- `accessedAt`。
- 发布日期。
- 发布机构或作者。
- 归档链接：优先使用 Internet Archive、perma.cc 或 Cloudflare R2 自建快照索引。
- DOI、arXiv ID、GitHub repository 等机器可识别标识。

注意版权：可以保存短引用、摘要、元数据和自己的评估；不要公开复制整篇付费文章或大段受版权保护文本。

---

## 4. 收集与过滤方案

### 4.1 候选收集漏斗

```
发现信号 -> 候选池 -> 事实确认 -> 影响评估 -> 人工审核 -> 发布 -> 定期复核
```

#### A. 发现信号

建议按类型覆盖，而不是只按平台覆盖：

| 信号类型 | 推荐来源 |
| --- | --- |
| 研究论文 | arXiv, OpenReview, ACL Anthology, NeurIPS/ICML/ICLR proceedings, Hugging Face Daily Papers |
| 模型与产品 | 公司博客、模型卡、API 文档、发布会、GitHub release |
| 开源生态 | GitHub trending/releases, Hugging Face models/datasets, Papers with Code |
| 政策法规 | EU、US、China、UK 等监管机构原文，法院文件，官方新闻稿 |
| 社会经济 | OECD、ILO、IMF、World Bank、Stanford AI Index、McKinsey、Goldman Sachs 等报告 |
| 社区注意力 | Hacker News, Reddit, X/Bluesky, 专业 Newsletter |
| 安全伦理 | METR, ARC Evals, Anthropic/OpenAI safety reports, academic safety papers |

社区来源用于发现，不用于独立确认。

#### B. 候选初筛

候选事件进入人工审核前，先按 0-2 分快速打分：

| 维度 | 0 分 | 1 分 | 2 分 |
| --- | --- | --- | --- |
| 可验证性 | 无原始来源 | 有二级来源 | 有原始来源 |
| 新颖性 | 重复旧事 | 小幅增量 | 明确新节点 |
| 外溢影响 | 只在小圈层讨论 | 影响单一群体 | 跨研究、产业、政策或公众 |
| 持续性 | 短期热度 | 可能持续 | 已有后续采用或制度影响 |
| 来源质量 | 社区流言 | 可靠二级来源 | 原始来源 + 独立确认 |

建议阈值：

- 0-4：不收录，保留观察。
- 5-7：候选池。
- 8-10：进入草稿。

#### C. 人工审核

人工审核至少检查：

- 日期是否准确。
- 标题是否克制，没有夸张词。
- 来源是否足以支撑事实和影响。
- `significance` 是否与同类事件一致。
- 是否存在明显反方观点。
- 英文主文案是否适合公开传播。

---

## 5. 评价标准

### 5.1 重要度：L1-L3

| 等级 | 名称 | 判定标准 |
| --- | --- | --- |
| L1 | Important | 对长期脉络有记录价值；影响明确但范围有限；通常不单独改变行业方向 |
| L2 | Key | 推动研究范式、产品采用、商业模式、政策讨论或公众认知中的至少一项；有独立来源确认 |
| L3 | Turning Point | 改变主流技术路线、公众认知、资本配置、监管议程或社会行为；影响跨领域且可持续 |

辅助判断：

- L3 不应过多。一个时代节点如果没有“前后叙事明显改变”，通常不是 L3。
- 古早理论事件可以是 L3，但需要证明其长期引用和范式影响。
- 新事件默认不要急着给 L3，除非影响已经外溢到多个群体。

### 5.2 影响维度

| 维度 | 关注问题 |
| --- | --- |
| capability_leap | AI 是否获得了此前不可行或显著不可用的新能力？ |
| economic_disruption | 是否改变就业、成本结构、商业模式、产业链或资本配置？ |
| access_democratization | 是否让更多人获得能力，或反过来加强少数主体的控制？ |
| risk_creation | 是否制造新的安全、偏见、版权、失控、滥用或伦理风险？ |
| paradigm_shift | 是否改变社会对智能、创造力、知识劳动或人的理解？ |

### 5.3 严重度：-3 到 +3

| 分值 | 含义 |
| --- | --- |
| +3 | 极强正向影响：跨领域、长期、可重复观察 |
| +2 | 明确正向影响：对一个或多个群体产生实质改变 |
| +1 | 有限正向影响：方向清楚但范围或持续性有限 |
| 0 | 中性、影响未明，或正负高度混合且无法拆分 |
| -1 | 有限负向影响：风险存在但范围有限 |
| -2 | 明确负向影响：已造成可观察损害或高概率结构性风险 |
| -3 | 极强负向影响：跨领域、长期、难以逆转或可能造成重大安全后果 |

不要把“影响很大但有好有坏”直接写成 0。应拆成多个维度分别评分。

### 5.4 影响分：`impactIndex`

`impactIndex` 用于前端快速展示，建议 0-10 分。它不是精密科学，但必须有一致口径。

推荐公式：

```
impactIndex =
  significanceBase
  + dimensionBonus
  + evidenceBonus
  + durabilityBonus
  + controversyAdjustment
```

| 项 | 规则 |
| --- | --- |
| significanceBase | L1=3，L2=5，L3=7 |
| dimensionBonus | 每覆盖一个核心影响维度 +0.5，最高 +1.5 |
| evidenceBonus | A=+1，B=+0.5，C=0，D=-1 |
| durabilityBonus | 长期影响 +1，中期 +0.5，短期/即时 +0 |
| controversyAdjustment | 高争议但证据不足 -0.5；争议本身构成重大公共影响时不扣分 |

最后四舍五入并限制在 0-10。前端显示时建议写成 **Impact Score**，并在 tooltip 解释“综合重要度、影响范围、证据等级和持续性”。

### 5.5 共识度

| 值 | 定义 |
| --- | --- |
| broad | 事实和主要影响解释已经被原始来源、独立报道或学界/产业广泛接受 |
| debated | 事实成立，但影响规模、意义、归因或长期后果有明显分歧 |
| emerging | 早期趋势判断，证据正在积累；适合保守措辞 |

### 5.6 争议标记

`controversy = true` 的条件：

- 有权威反方来源。
- 存在法律、伦理、安全或版权争议。
- 事件事实无争议，但社会影响、风险或归因争议很大。
- 预测明显依赖不稳定假设。

---

## 6. 预测内容规范

### 6.1 预测从哪里来

预测不应来自单一专家观点，也不应来自社交媒体热度。建议使用“信号篮子”：

| 信号篮子 | 可观察内容 |
| --- | --- |
| 技术能力 | benchmark、模型报告、第三方评测、可复现实验 |
| 产品采用 | 用户规模、企业部署、API 使用、开发者生态、价格变化 |
| 基础设施 | GPU/ASIC 供给、推理成本、数据中心建设、开源工具成熟度 |
| 资本与产业 | 投融资、并购、收入披露、供应链变化 |
| 政策与安全 | 法规、标准、诉讼、监管处罚、安全评测 |
| 社会行为 | 劳动力市场、教育、创作、媒体、公众使用习惯 |
| 反向信号 | 技术瓶颈、成本瓶颈、监管阻力、采用失败案例 |

一条预测发布前至少要有：

- 2 条支持信号。
- 1 条反向信号或限制条件。
- 明确的时间窗口。
- 明确的达成标准。

### 6.2 达成标准怎么写

预测描述必须能被未来裁定。推荐写法：

```md
Achieved when:
An AI system can complete at least X% of benchmark/task set Y under public or independently audited evaluation, and the capability is available outside a single closed demo for at least 90 days.

Not achieved when:
The result depends only on a private demo, cherry-picked examples, or a benchmark that is later shown to be contaminated or not representative.

Primary measurement sources:
Independent benchmark reports, model cards, peer-reviewed or public technical reports, regulator/auditor documents.
```

### 6.3 示例：AGI 预测的更好写法

不推荐：

> AGI will arrive in 2027.

推荐：

> By 2027-2029, at least one AI system may demonstrate broad autonomous performance across knowledge work, software, scientific reasoning, and multi-step planning under independent evaluation.

达成标准：

- 系统在多个独立评测中达到或超过专业人类基线。
- 能在真实或近真实工作流中连续完成多步骤任务。
- 能力不是单一封闭演示，至少持续公开可用或可被第三方审计 90 天。

未达成标准：

- 只在单一 benchmark 上高分。
- 只展示剪辑 demo。
- 需要大量隐藏人工接管。
- 没有独立评测或可复核材料。

---

## 7. 方法与来源是否公开

建议公开，但公开的是“用户能理解和监督的方法”，不是全部内部操作细节。

### 应公开

- 收录标准。
- 来源分级。
- L1-L3 的定义。
- Impact Score 的基本含义。
- 共识度和争议标记的定义。
- 预测达成与裁定原则。
- 更新频率、修订和纠错方式。
- 局限性：本站是结构化策展，不是学术数据库或投资建议。

### 不必完全公开

- 具体抓取脚本、API key、自动化提示词。
- 未审核候选池的完整列表。
- 个人内部备注。
- 可能引发版权问题的全文缓存。

公开方法页的价值：

- 增强可信度。
- 降低“你凭什么这么排”的质疑成本。
- 有利于 SEO 和被引用。
- 为未来广告、赞助或合作建立更专业的基础。

建议页面命名：`Methodology` 或 `Methodology & Sources`。英文站点里，`Methodology` 更干净。

---

## 8. 技术与更新架构

### 8.1 第一版推荐架构

第一版推荐：

- **Cloudflare Pages**：托管静态前端、JSON 数据、预览部署、自定义域名。
- **Pages Functions**：处理轻量动态接口，例如投票、反馈、提交候选。
- **Cloudflare D1**：保存投票、反馈、候选提交、更新日志等结构化数据。
- **Cloudflare R2**：可选，用于保存来源快照索引、截图或未来生成的归档附件。
- **Scheduled Worker**：可选，用于定时抓取候选信号，不直接自动发布。

不建议第一版直接把所有内容放数据库里动态渲染。原因：

- 当前核心价值是策展质量，不是实时更新。
- 文件化内容更容易人工 review、版本追踪和回滚。
- 静态站更稳定、便宜，也更适合 Cloudflare Pages。

### 8.2 Pages 还是 Workers

| 方案 | 适合场景 | 推荐度 |
| --- | --- | --- |
| Cloudflare Pages | 静态站、JSON 数据、预览部署、Git 发布、少量 API | 第一版首选 |
| Workers + Static Assets | 动态 API 更重、边缘逻辑多、需要统一 Worker 入口 | 第二阶段可考虑 |
| Pages + 独立 Worker | 静态站独立，自动抓取/任务队列独立 | 推荐的渐进式方案 |

结论：**先用 Pages，上线更快；投票用 Pages Functions + D1；自动收集用独立 Scheduled Worker。**

### 8.3 建议目录结构

```txt
data/
  events.json              # 公开事件数据
  forecasts.json           # 公开预测数据
  sources.json             # 来源索引
  schema/
    event.schema.json
    forecast.schema.json
    source.schema.json

content/
  events/
    chatgpt-2022.json
    transformer-2017.json
  forecasts/
    agi-2027-2029.json
  candidates/
    2026-06-24-hf-daily-papers.json

scripts/
  validate-data.mjs
  build-data.mjs
  collect-candidates.mjs

functions/
  api/
    vote.ts
    feedback.ts
```

### 8.4 更新流程

1. 自动或手动收集候选信号。
2. 写入 `content/candidates/` 或 D1 `candidate_signals` 表。
3. 人工筛选后生成 `content/events/*.json` 或 `content/forecasts/*.json`。
4. 运行数据校验：
   - 必填字段。
   - 来源 URL 不为空。
   - L2/L3 来源数量达标。
   - 预测必须有达成标准。
   - 多语言字段完整性。
5. 构建生成 `data/events.json`、`data/forecasts.json`。
6. Cloudflare Pages 自动部署。
7. 每月检查断链和更新来源访问日期。

### 8.5 投票功能

可以实现。建议第一版只做预测卡投票：

- 用户选择：`will happen` / `will not happen` / `unsure`。
- 前端展示总票数和比例。
- 后端用 D1 保存聚合和匿名事件。
- 防刷：IP hash + user agent hash + forecast id + 日期窗口；不要存明文 IP。
- 明确声明：投票代表读者观点，不影响事实评分。

建议 D1 表：

```sql
CREATE TABLE forecast_votes (
  id TEXT PRIMARY KEY,
  forecast_id TEXT NOT NULL,
  vote TEXT NOT NULL CHECK (vote IN ('yes', 'no', 'unsure')),
  voter_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_forecast_votes_forecast_id
ON forecast_votes (forecast_id);
```

### 8.6 数据质量守门脚本

上线前建议加入 `npm run validate:data`，至少检查：

- JSON 可解析。
- ID 唯一。
- 日期格式合法。
- L2/L3 来源数量满足要求。
- 所有来源有 URL 或明确 `missingUrlReason`。
- `impactIndex` 在 0-10。
- `severity` 在 -3 到 +3。
- `consensusLevel` 只允许规定值。
- 预测有 `achievedWhen` 和 `notAchievedWhen`。

---

## 9. 近期迁移计划

### Phase 1：上线前数据补强

- 直接维护 v2 结构的 `data/events.json`、`data/forecasts.json` 和 `data/sources.json`。
- 补齐所有空 URL 来源。
- 将 `Impact Score` 的说明加入前端 tooltip 或方法页。
- 将预测卡补上更完整的支持信号、反向信号和来源。
- 方法页公开 v2 的简版规则。

### Phase 2：结构化内容生产

- 新增 `content/events/` 和 `content/forecasts/`。
- 新增 schema 和校验脚本。
- 构建时合并生成公开 JSON。
- 通过构建脚本从 `content/` 生成公开 `data/` 文件。

### Phase 3：动态能力

- Pages Functions + D1 投票。
- Feedback / submit candidate 表单。
- Scheduled Worker 生成候选池。
- 每月自动断链检查。

---

## 10. 文案口径

### 标题

标题尽量克制，避免：

- “震撼”
- “颠覆一切”
- “史诗级”
- “终局”
- “彻底改变人类”

推荐格式：

- `OpenAI launches ChatGPT`
- `Transformer architecture reshapes sequence modeling`
- `EU AI Act establishes a risk-based regulatory framework`

### 预测

预测文案避免：

- `will definitely`
- `inevitable`
- `the end of`
- `solved`

推荐：

- `may`
- `could`
- `is likely to`
- `under current assumptions`
- `would count as achieved if`

### 争议

争议不是削弱内容，而是提升可信度。对于安全、版权、就业、AGI、监管等内容，应主动呈现反方或限制条件。

---

## 11. 最小上线标准

正式公开前，建议至少完成：

1. 所有 L2/L3 事件补齐可点击来源 URL。
2. 每个 L3 事件至少有 2 个独立来源。
3. 每个预测有达成标准和未达成标准。
4. 方法页公开来源分级、评分规则和预测裁定规则。
5. 数据校验脚本能在部署前阻断明显错误。
6. 投票如上线，必须有隐私说明和反刷策略。

---

## 12. 一句话定位

EpochArc 的数据方法不是“宣布 AI 真相”，而是把 AI 发展的事实、证据、影响和不确定性放在同一个可审阅的结构里。
