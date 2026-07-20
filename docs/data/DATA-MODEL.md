# EpochArc 数据模型规范

**版本**：v2.3
**更新日期**：2026-07-20
**适用范围**：AI 历史时间轴内容的结构、类型定义、来源标准、评分规则和数据校验。

关联文档：
- 工作流与发现机制：[WORKFLOW.md](../workflow/WORKFLOW.md)
- Possible Directions 公开规则：[FORECASTS-SPEC.md](../product/FORECASTS-SPEC.md)
- 产品路线图：[PRODUCT-PLAN.md](../product/PRODUCT-PLAN.md)
- 文案风格：[STYLE-GUIDE.md](../product/STYLE-GUIDE.md)
- 上线清单：[LAUNCH-CHECKLIST.md](../product/LAUNCH-CHECKLIST.md)

---

## 1. 核心原则

### 1.1 分层表达

每条内容区分四层：

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| Fact | 可验证事实 | OpenAI 于 2022-11-30 发布 ChatGPT |
| Claim | 来源中的主张 | "ChatGPT helped popularize generative AI" |
| Assessment | 本站评估 | 该事件是 L3 转折点，影响维度包括普惠化和范式转变 |
| Forecast | 未来判断 | 2027-2029 年可能出现可被公开验证的通用智能系统 |

数据层必须能追踪每个判断来自事实、来源主张还是本站评估。

### 1.2 判断可追溯

- 可解释：评分有依据。
- 可追溯：重要判断能回溯到来源、证据或反方观点。
- 可修正：更新时保留变更记录。

### 1.3 宁缺毋滥

- 只有社交媒体热度、无原始来源的内容，不发布为正式节点。
- 单一公司营销说法，只能作为候选。
- 对未来的判断必须写成预测，不作为事实。

---

## 2. 正式数据模型

### 2.1 事件:`AIEvent`

```ts
export interface AIEvent {
  id: string;
  slug: string;

  title: LocalizedText;
  summary: LocalizedText;
  narrative?: LocalizedText;

  date: string;                       // YYYY-MM-DD / YYYY-MM / YYYY
  datePrecision: DatePrecision;
  displayDate?: LocalizedText;

  categories: EventCategory[];        // 1-2 个分类，第一个为主分类
  status: ContentStatus;

  significance: SignificanceLevel;    // L1-L3
  impactIndex: number;                // 0-10
  consensusLevel: ConsensusLevel;
  controversy: boolean;

  impacts: ImpactAssessment[];
  claims: EventClaim[];
  sources: SourceRef[];
  relatedEvents: string[];
  relatedForecasts?: string[];

  editorial: EditorialMetadata;
}

export interface LocalizedText {
  en: string;
  zhHans: string;
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
  | 'broad'
  | 'debated'
  | 'emerging';

export type EventCategory =
  | 'capability'   // 能力突破
  | 'product'      // 产品工具
  | 'commerce'     // 商业产业
  | 'governance'   // 治理监管
  | 'safety'       // 安全伦理
  | 'society';     // 社会文化
```

#### 状态转换与发布门槛

事件状态只允许按以下路径变化：

```text
candidate → draft → reviewed → published → archived
                ↘───────────────↗
```

- `candidate`、`draft`、`reviewed` 不得进入公开构建输出。
- `reviewed` 必须填写 `editorial.reviewedAt`、`editorial.reviewer` 和 `editorial.reviewProvenance`。
- `published` 必须填写 `editorial.reviewedAt`、`editorial.reviewer`、`editorial.reviewProvenance` 和 `editorial.publishedAt`。
- `archived` 保留源文件和变更记录，但默认不进入时间轴；引用它的方向或 Arc 必须先解除引用或明确迁移目标。
- 任何逆向状态变化都必须增加 `changeLog`，并使用 `correction` 或 `archived` 说明原因。
- 当前为单人策展时，`curator` 与 `reviewer` 可以是同一人，但两个责任字段仍必须显式填写。

`slug` 是公开 URL 的唯一标识，必须全局唯一且符合 `^[a-z0-9]+(?:[.-][a-z0-9]+)*$`。构建器不得静默用 `id` 替代缺失的 `slug`。

#### 语言要求

`LocalizedText` 中 `en` 和 `zhHans` 均为必填。其他语言可选。

#### 关联事件

`relatedEvents` 表示无方向的事件关联。编辑源文件可以只在一侧登记；`scripts/build_events.py` 会在生成 `data/events.json` 时自动补齐反向关系。目标 ID 必须已存在，且不允许自引用或重复 ID。

#### 文件组织

```
content/events/*.json      ← 编辑源文件
  ↓ python3 scripts/build_events.py
data/events.json           ← 构建输出
data/sources.json          ← 来源独立表
```

---

### 2.2 事件分类：`categories`

`categories` 是长度为 1-2 的数组。第一个是主分类，第二个（可选）是次分类。

#### 六分类定义

| Category | 中文 | 判定标准 |
| --- | --- | --- |
| `capability` | 能力突破 | AI 做到了以前做不到的事。前沿模型发布、首次达到人类/超人类水平、新范式改变了技术路线 |
| `product` | 产品工具 | AI 变成了普通人能用的东西。产品上线、重大迭代、退出市场。包含被当作产品使用的开源项目 |
| `commerce` | 商业产业 | AI 公司、资本、市场的关键变化。公司治理重组、估值里程碑、关键人事变动、重大交易/合作、以 AI 为由的大规模裁员 |
| `governance` | 治理监管 | 政府开始管 AI 了。法律、监管、法院判例、行政命令、国际协议 |
| `safety` | 安全伦理 | AI 闯祸了，或引发伦理危机。安全事故、吹哨人事件、深度伪造事件、版权诉讼（当核心争议是 AI 失控时） |
| `society` | 社会文化 | AI 改变了社会，不用 AI 的人也能感受到。文化现象、就业危机、公众认知时刻、开源运动改变权力结构 |

#### 多分类规则

最多 2 个分类。加第二分类的条件：删除这个分类维度会丢失 ≥ 30% 的事件故事信息。

**判定启发：**

| 主分类 | 常见第二分类 | 触发条件 |
| --- | --- | --- |
| `capability` | `commerce` | 模型发布引发巨大市场波动 |
| `capability` | `society` | 技术突破被全社会认可为文化时刻 |
| `commerce` | `society` | 公司决策引发大规模就业危机 |
| `governance` | `safety` | 诉讼或监管直接源于安全事故 |
| `product` | `commerce` | 产品变动揭示商业压力 |
| `product` | `society` | 产品成为文化现象 |
| `safety` | `society` | 安全事件引发公众广泛关注 |

#### 日期选择规则

时间轴上的日期是**"大量普通人可感知到这件事的时刻"**：

| 事件形态 | 日期取什么 |
| --- | --- |
| 单日事件 | 发生日 |
| 渐变 + 引爆 | 引爆点（新闻量/GitHub stars/社交讨论爆发的时刻） |
| 无明确引爆点 | 最早的大规模公开报道日 |
| 仍在进行中 | 有代表性的里程碑日 |

---

### 2.3 事件主张:`EventClaim`

```ts
export interface EventClaim {
  id: string;
  text: LocalizedText;
  claimType: 'fact' | 'impact' | 'limitation' | 'interpretation';
  evidenceGrade: EvidenceGrade;
  sourceIds: string[];
  notes?: string;
}

export type EvidenceGrade = 'A' | 'B' | 'C' | 'D';
```

使用原则：

- 每个 L2/L3 事件至少 2 条 claim：一条事实 + 一条影响。
- `controversy = true` 且 L2 以上，必须有一条 `claimType = limitation`。
- 每条 claim 必须有唯一非空 `id`、完整中英文 `text`、合法的 `claimType` 和 `evidenceGrade`，并通过非空 `sourceIds` 直接绑定证据。
- 不接受旧别名 `statement`、`type`、`confidence`、`sources`；`assessment` 也不是合法的 `claimType`。
- D 级证据只用于候选池，不作为正式事件核心依据。

---

### 2.4 影响评估:`ImpactAssessment`

```ts
export interface ImpactAssessment {
  dimension: ImpactDimension;
  severity: ImpactSeverity;
  direction: 'positive' | 'negative' | 'neutral';
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

export type ImpactTimeframe = 'immediate' | 'short' | 'medium' | 'long';
```

如果同一事件既带来正面又带来负面影响，拆成两个 impact，不要写成一个模糊的 0 分。

`severity` 是带符号值，`direction` 只用于前端显示，二者必须一致：

- `positive` → `severity` 必须为 `+1..+3`
- `negative` → `severity` 必须为 `-1..-3`
- `neutral` → `severity` 必须为 `0`

不再允许 `mixed`。正负影响必须拆开记录，避免同一条记录同时承担相反语义。

---

### 2.5 来源

来源使用独立表 `data/sources.json`。事件中只引用 `sourceIds`。

```ts
export interface Source {
  id: string;
  type: SourceType;
  tier: SourceTier;
  title: string;
  url: string;
  archiveUrl?: string;
  publisher?: string;
  authors?: string[];
  publishedAt?: string;
  accessedAt?: string;
  language?: string;
  doi?: string;
  arxivId?: string;
  repositoryUrl?: string;
  independence: SourceIndependence;
  notes?: string;
}

export type SourceType =
  | 'primary' | 'paper' | 'official' | 'model_card'
  | 'benchmark' | 'report' | 'news' | 'analysis'
  | 'community' | 'encyclopedia';

export type SourceTier = 1 | 2 | 3 | 4;

export type SourceIndependence =
  | 'primary_actor' | 'independent' | 'community_signal' | 'unknown';

export interface SourceRef {
  sourceId: string;
  supports?: string[];                 // 可选的编辑提示；证据绑定以 claim/impact 的 sourceIds 为准
  quote?: string;
}
```

`publishedAt` 表示来源自身的发布日期，`accessedAt` 表示编辑最后一次实际打开并核对该链接的日期，两者不得混用。新建或更新来源时 `accessedAt` 必填；历史来源缺失时校验器报 warning，完成真实链接检查后才能补写，禁止用迁移日期伪装成访问日期。

`independence` 的判定对象是“相对于事件中的核心主张是否独立”，而不是网站类型：

- 当事公司、作者、监管发布主体：`primary_actor`
- 与核心主张无直接利益关系的媒体、研究机构或复核方：`independent`
- 社区帖子与热度聚合：`community_signal`
- 暂时无法判断：`unknown`，不得计入独立来源门槛

“2 个独立来源”按出版机构/控制主体去重，而不是按 URL 数量计数；同一媒体、同一公司集团或同一份稿件的转载只能算 1 个来源。校验器优先使用 `publisher`，缺失时以 URL 域名作为保守去重键。

---

### 2.6 未来信号：`AIForecast`

完整公开规则见 [FORECASTS-SPEC.md](../product/FORECASTS-SPEC.md)。

```ts
export interface AIForecast {
  id: string;
  slug: string;
  title: LocalizedText;
  thesis: LocalizedText;
  description: LocalizedText;
  forecastType: ForecastType;
  status: ForecastStatus;
  createdAt: string;
  updatedAt: string;
  lastReviewedAt: string;
  reviewCadence: 'monthly' | 'quarterly' | 'semiannual';
  expectedWindow: ForecastWindow;
  confidence: ForecastConfidence;
  rationale: ForecastRationale;
  signals: ForecastSignal[];
  consensusBasis: ForecastConsensusBasis;
  resolution?: ForecastResolution;
  sources: SourceRef[];
  relatedEvents: string[];
  selection?: ForecastSelectionSummary; // 1.0 可只存在前端 localStorage
  editorial: EditorialMetadata;
}

export type ForecastType =
  | 'capability' | 'product' | 'economic' | 'safety'
  | 'policy' | 'science' | 'infrastructure' | 'social';

export type ForecastStatus =
  | 'active' | 'resolved_true' | 'resolved_false'
  | 'partially_resolved' | 'superseded' | 'retracted';

export interface ForecastWindow {
  start: string;                       // YYYY
  end: string;                         // YYYY，且不得早于 start
  precision: 'year';
}

export interface ForecastConfidence {
  level: 'low' | 'medium' | 'high';
  evidenceGrade: EvidenceGrade;
}

export interface ForecastRationale {
  currentBaseline: LocalizedText;      // 当前已经发生什么，避免把现状写成预测
  whyThisDirection: LocalizedText;     // 为什么这些事件和信号值得组成一个观察方向
  counterSignal: LocalizedText;        // 当前最重要的限制或反向证据
  openQuestions: LocalizedText[];      // 仍待观察的问题
}

export interface ForecastSignal {
  id: string;
  kind:
    | 'product'
    | 'deployment'
    | 'workflow'
    | 'benchmark'
    | 'research'
    | 'infrastructure'
    | 'regulation'
    | 'incident'
    | 'market';
  status: 'observed';
  label: LocalizedText;
  summary: LocalizedText;
  eventIds: string[];                  // 必须回指到正式时间轴事件
  sourceIds: string[];                 // 支撑该 signal 的来源
}

export interface ForecastConsensusBasis {
  resolutionMode: 'monitor_only' | 'consensus_gated';
  basisType:
    | 'none'
    | 'regulatory_standard'
    | 'benchmark_norm'
    | 'market_consensus';
  summary: LocalizedText;              // 说明为什么当前只能观察，或采用哪种外部共识
  sourceIds: string[];
}

export interface ForecastSelectionSummary {
  selectedForecastId?: string;
  storedAt: 'localStorage' | 'd1' | 'account';
  updatedAt: string;
}

export interface ForecastResolution {
  resolvedAt: string;
  outcome: 'true' | 'false' | 'partial';
  criterion: LocalizedText;            // 采用的外部公开口径
  summary: LocalizedText;
  sourceIds: string[];
  reviewer: string;
}
```

方向生命周期约束：

- `monitor_only` 只能使用 `active`、`superseded` 或 `retracted`，不得使用任何 `resolved_*` 状态。
- `consensus_gated` 必须使用非 `none` 的 `basisType`，并给出可追溯的外部来源。
- 任何 `resolved_*` 状态都必须包含 `resolution`；`resolution.outcome` 必须与状态一致。
- `superseded` 必须在编辑记录中说明替代方向 ID；`retracted` 必须说明撤回原因。

1.0 公开 JSON 不发布全站投票聚合；如果未来引入 Reader Pulse 后端统计，建议放在独立接口或 D1 表，而不是写回静态方向数据。

#### 未来方向门槛

Possible Direction 必须描述“由已发生事件支撑、但尚未成为常态的中期变化方向”。

公开前必须确认：

- 普通读者不会合理地认为“这已经是普遍事实”。
- `currentBaseline` 与方向本身清晰区分。
- 每条 `signals` 都绑定至少 1 条已发布事件和 1 个来源。
- 页面展示的是 `observed signals`，不是内部设定的完成度。
- 如果不存在公开的外部共识基础，则 `consensusBasis.resolutionMode` 必须为 `monitor_only`。

---

### 2.7 编辑元数据

```ts
export interface EditorialMetadata {
  createdAt: string;
  updatedAt: string;
  reviewedAt?: string;
  publishedAt?: string;
  lastSourceCheckAt?: string;
  curator?: string;
  reviewer?: string;
  reviewProvenance?: 'legacy_pre_v23' | 'v2.3';
  curatorNote?: LocalizedText;
  changeLog?: ChangeLogEntry[];
}

export interface ChangeLogEntry {
  date: string;
  changeType:
    | 'created' | 'source_added' | 'score_changed'
    | 'translation_changed' | 'forecast_resolved'
    | 'correction' | 'archived';
  summary: string;
}
```

`createdAt` 与 `updatedAt` 是每个正式事件的必填字段。`lastReviewed` 是旧字段，必须迁移为 `reviewedAt`。`reviewProvenance = legacy_pre_v23` 表示该条目只完成了旧数据迁移，不能冒充按当前规范完成的事实复核；经过当前规范复核后才可改为 `v2.3`，并同步更新 `updatedAt`、`reviewedAt` 与 `changeLog`。`curatorNote` 用于保留双语策展说明，不替代时间和责任人字段。

---

## 3. 来源标准

### 3.1 来源分级

| Tier | 定义 | 可用作 |
| --- | --- | --- |
| 1 | 原始来源：论文、官方公告、模型卡、代码仓库、法规原文、法院文件、技术报告 | 事实确认、事件日期、核心能力描述 |
| 2 | 高质量独立来源：主流科技/财经媒体、学术综述、机构报告、监管机构解读 | 影响确认、外部采用、争议背景 |
| 3 | 专家分析与社区整理：研究者博客、专业通讯、会议演讲 | 背景解释、趋势线索、候选发现 |
| 4 | 社区热度信号：社交媒体、HN、Reddit、论坛 | 仅用于发现，不可独立支撑结论 |

类型与层级必须相容：论文、官方公告、模型卡、代码/法规/司法原文和直接技术报告才有资格标为 Tier 1；新闻报道最高为 Tier 2；普通分析和百科默认 Tier 3。经过学术编辑的参考工具可在 `notes` 中说明理由后标 Tier 2；Wikipedia 不得作为 Tier 2 的默认替代品。社区内容只能标 Tier 4。

### 3.2 最低来源要求

| 内容类型 | 发布最低要求 |
| --- | --- |
| L1 事件 | 1 个 Tier 1，或 2 个相互独立的 Tier 2 |
| L2 事件 | 1 个 Tier 1 + 1 个独立 Tier 2/3；若不存在可获得的一手材料，可用 2 个相互独立的 Tier 2，并在编辑记录中说明 |
| L3 事件 | 1 个 Tier 1 + 2 个独立 Tier 2；若有争议须收录反方来源 |
| 影响评估 | 每个核心影响至少 1 个可追溯来源 |
| Possible Direction | 至少 2 条 observed signals + 1 条明确 counterSignal |

---

## 4. 评价标准

significance（L1-L3）和 impactIndex（0-10）是两套独立的评价体系：

- **significance (L1-L3)** — 编辑判断的历史重要度。不使用公式。
- **impactIndex (0-10)** — 数据驱动的可观测影响评分。基于维度、严重度、证据、持续性、受众广度。

两者互不包含。不一致本身有信息量。

### 4.1 重要度：L1-L3

| 等级 | 名称 | 判定标准 |
| --- | --- | --- |
| L1 | Important | 对长期脉络有记录价值；影响范围有限；通常不单独改变行业方向 |
| L2 | Key | 推动研究范式、产品采用、商业模式、政策讨论或公众认知中的至少一项 |
| L3 | Turning Point | 改变主流技术路线、公众认知、资本配置、监管议程或社会行为；跨领域且可持续 |

- L3 不应过多。
- 古早理论事件可以是 L3，但需证明长期引用和范式影响。
- 新事件默认不给 L3，确认外溢后再升级。

### 4.2 影响维度

| 维度 | 关注问题 |
| --- | --- |
| capability_leap | AI 是否获得了此前不可行的新能力？ |
| economic_disruption | 是否改变就业、成本结构、商业模式或资本配置？ |
| access_democratization | 是否让更多人获得能力，或加强少数主体的控制？ |
| risk_creation | 是否制造新的安全、偏见、版权、失控或伦理风险？ |
| paradigm_shift | 是否改变社会对智能、创造力或知识劳动的理解？ |

### 4.3 严重度：-3 到 +3

| 分值 | 含义 |
| --- | --- |
| +3 | 极强正向：跨领域、长期、可重复观察 |
| +2 | 明确正向：对一个或多个群体产生实质改变 |
| +1 | 有限正向：方向清楚但范围有限 |
| 0 | 中性或正负高度混合无法拆分 |
| -1 | 有限负向：风险存在但范围有限 |
| -2 | 明确负向：已造成可观察损害或高概率结构性风险 |
| -3 | 极强负向：跨领域、长期、难以逆转 |

### 4.4 影响分：`impactIndex`

正式计算规则：

```
impactIndex =
  dimensionScore      ← 每个影响维度只取最大的 |severity|，再求和 / 3，上限 4
  + evidenceBonus     ← 取所有 impact 中最弱的 evidenceGrade：A=+1.5, B=+1, C=+0.5；D 不得发布
  + durabilityBonus   ← 取最高 timeframe：long=+1.5, medium=+1, short=+0.5, immediate=0
  + scopeBonus        ← 去空格、转小写、去重后的受影响群体数：≥4类+2, 3类+1.5, 2类+1, 1类+0.5
  + controversyAdj    ← controversy=true 且任一核心 claim 为 C 级时 -0.5，否则 0
```

先将原始分截断到 0-10，再按 `floor(score + 0.5)` 四舍五入为整数。重复添加同一维度或同义 affected group 不得提高分数。

#### EvidenceGrade 判定

| 等级 | 可发布含义 |
| --- | --- |
| A | 有直接一手证据，并有独立复核；或有多份相互独立的高质量直接证据 |
| B | 有可靠的一手证据但独立复核有限；或有至少 2 个相互独立的 Tier 2 |
| C | 只有单一可靠二手来源，结论仍需补强；不得支撑 L3 核心判断 |
| D | 未核实线索、社区传闻或营销主张；仅限候选池，不得出现在 `published` 内容中 |

EvidenceGrade 评价的是具体 claim/impact 的证据链，不等于单个来源的 Tier。

### 4.5 共识度

| 值 | 定义 |
| --- | --- |
| broad | 事实和主要影响解释已被广泛接受 |
| debated | 事实成立，但影响规模、归因或长期后果有明显分歧 |
| emerging | 早期趋势判断，证据正在积累 |

### 4.6 争议标记

`controversy = true` 的条件：

- 有权威反方来源。
- 存在法律、伦理、安全或版权争议。
- 社会影响、风险或归因争议很大。

---

## 5. 数据质量校验

所有公开数据先通过 `python3 scripts/validate_all.py` 统一校验；`npm run build` 必须先执行该门禁。`build_events.py` 和 `build_arcs.py` 只负责生成，不是完整发布门禁。校验至少检查：

- JSON 可解析。
- ID 唯一。
- 日期格式合法。
- L2/L3 来源数量满足最低要求。
- 所有来源有 URL。
- `impactIndex` 在 0-10。
- `severity` 在 -3 到 +3。
- 枚举字段只允许规定值。
- 每条 claim 的 `id`、`text`、`claimType`、`evidenceGrade`、`sourceIds` 完整且合法。
- Claim 引用的 `sourceIds` 必须存在于 `data/sources.json`，且数组不能为空。
- 每个事件都有 `editorial.createdAt` 和 `editorial.updatedAt`；可选的 `changeLog` 条目结构合法。
- 每条方向至少有 2 条 `signals`。
- 每条 `signals` 至少有 1 个 `eventIds` 和 1 个 `sourceIds`。
- `signals[].eventIds` 必须存在于 `events.json`。
- `consensusBasis.resolutionMode = monitor_only` 时不得填写私设公开裁定标准。
- `relatedEvents` 的目标存在性、自引用和重复检查；构建输出自动双向规范化。

覆盖 `events.json`、`forecasts.json` 和 `sources.json` 三类数据。

---

## 6. 附录：v2 事件完整示例（ChatGPT）

```json
{
  "id": "chatgpt-2022",
  "slug": "chatgpt-launch",
  "title": {
    "en": "OpenAI launches ChatGPT",
    "zhHans": "OpenAI 发布 ChatGPT"
  },
  "summary": {
    "en": "OpenAI released ChatGPT, a conversational AI product based on GPT-3.5, free to the public. It reached 1 million users in 5 days and 100 million in 2 months.",
    "zhHans": "OpenAI 发布基于 GPT-3.5 的对话式 AI 产品 ChatGPT，首次对公众免费开放。5 天注册用户破百万，两个月达到 1 亿用户。"
  },
  "narrative": {
    "en": "ChatGPT was not the first large language model, but it was the first to package the technology into a zero-friction consumer product...",
    "zhHans": "ChatGPT 不是第一个大语言模型，但它是第一个将这项技术包装成零门槛消费品的产品..."
  },
  "date": "2022-11-30",
  "datePrecision": "day",
  "displayDate": { "en": "November 30, 2022", "zhHans": "2022年11月30日" },
  "categories": ["product", "society"],
  "status": "published",
  "significance": 3,
  "impactIndex": 9,
  "consensusLevel": "broad",
  "controversy": false,
  "impacts": [
    {
      "dimension": "capability_leap",
      "severity": 3,
      "direction": "positive",
      "description": { "en": "...", "zhHans": "..." },
      "affectedGroups": ["general public", "educators", "content creators"],
      "timeframe": "immediate",
      "evidenceGrade": "A",
      "sourceIds": ["openai-chatgpt-blog-2022", "reuters-chatgpt-users-2023"]
    }
  ],
  "claims": [
    {
      "id": "chatgpt-launch-fact",
      "text": { "en": "OpenAI released ChatGPT on November 30, 2022.", "zhHans": "..." },
      "claimType": "fact",
      "evidenceGrade": "A",
      "sourceIds": ["openai-chatgpt-blog-2022"]
    }
  ],
  "sources": [
    { "sourceId": "openai-chatgpt-blog-2022", "supports": ["chatgpt-launch-fact"], "quote": "..." }
  ],
  "relatedEvents": ["gpt3-2020", "gpt4-2023"],
  "editorial": {
    "createdAt": "2026-06-20",
    "updatedAt": "2026-06-24",
    "reviewedAt": "2026-06-24",
    "publishedAt": "2026-06-24",
    "curator": "gang",
    "changeLog": [
      { "date": "2026-06-24", "changeType": "score_changed", "summary": "Adjusted impactIndex from 8 to 9 after evidence review." }
    ]
  }
}
```
