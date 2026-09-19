# EpochArc 数据模型规范

**版本**：v2.4（已接受）
**更新日期**：2026-09-18

编辑规则权威：[EDITORIAL-STANDARD](../workflow/EDITORIAL-STANDARD.md)；参数唯一来源：[policy.json](../../governance/policy.json)。本文件定义公开字段，不重复维护评级准入规则。新增审计字段见 [REVIEW-CONTRACT](REVIEW-CONTRACT.md)。
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
- 单一公司营销说法不能证明客观性能；公告可以直接证明“公司宣布了什么”，是否发布仍按核心事实与阶段规则评估。
- 对未来的判断必须写成预测，不作为事实。

---

## 2. 正式数据模型

### 2.1 事件:`AIEvent`

```ts
export interface AIEvent {
  id: string;
  slug: string;

  title: LocalizedText;
  searchSummary: LocalizedText;
  summary: LocalizedText;
  narrative: LocalizedText;

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
- `curator/reviewer` 记录实际操作者，不自动表示人类。v2.4 L2/L3 需要独立会话或真实人工复核；发布另需精确版本的人工批准。新草稿不要求编造复核记录。

`slug` 是公开 URL 的唯一标识，必须全局唯一且符合 `^[a-z0-9]+(?:[.-][a-z0-9]+)*$`。构建器不得静默用 `id` 替代缺失的 `slug`。

#### 语言要求

`LocalizedText` 中 `en` 和 `zhHans` 均为必填。其他语言可选。

#### 内容字段职责与公开呈现

`title`、`searchSummary`、`summary` 和 `narrative` 承担不同的信息职责，不得互相替代：

| 字段 | 职责 | 写作要求 |
| --- | --- | --- |
| `title` | 事件名称 | 准确标识主体与动作，不在标题中加入未经来源支持的评价 |
| `searchSummary` | 核心导语 | 用 1-2 句概括事件最重要的事实或意义；供标题下副标题、搜索结果描述和社交分享描述使用 |
| `summary` | 完整事件摘要 | 交代时间、主体、动作、直接结果和必要的事实边界；不能因已有 `searchSummary` 而省略 |
| `narrative` | 背景与脉络 | 说明前因后果、机制、历史位置和限制；不得把推测写成已经发生的事实 |

公开页面遵循“语义一致、逐层增量、详情页最完整”的原则：

| 呈现场景 | `searchSummary` | `summary` | `narrative` | `claims` / `impacts` / `sources` |
| --- | --- | --- | --- | --- |
| 时间轴收起态 | 标题下导语 | 不展示 | 不展示 | 仅显示指标 |
| 时间轴展开态 | 保留在卡片头部 | 完整展示 | 完整展示 | 展示影响与来源概览 |
| 独立详情页 | 标题下导语 | 完整展示 | 完整展示 | 完整展示并保留证据绑定 |

`searchSummary` 不能代替详情页的“事件摘要”。SEO 元数据可以使用 `searchSummary`，但正文中的“事件摘要”必须始终来自 `summary`。所有已发布事件必须提供完整中英文 `searchSummary`；兼容旧数据的渲染回退顺序为 `searchSummary[lang] ?? summary[lang]`，回退只用于防止页面空白，不替代数据补齐。

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

最多 2 个分类。按 EDITORIAL-STANDARD 的 CLASS-01/02：主分类按核心动作，次分类须绑定一个独立成句、有来源且确实增加实际变化信息的 claim；不再使用不可测的 30% 标准。

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

按 IDENT-02：取节点所述动作发生日；只知披露日就明确写为披露节点；保留来源支持的 day/month/year 精度。公告、预览、实际可用、部署、立法通过和生效不可混写。不以热度峰值替代动作日期。

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
- v2.4 所有等级的 `controversy = true` 都必须有一条 `claimType = limitation` 及对应证据。
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
  affectedGroups: string[];            // v2.4 只允许 policy.audiences 中的角色 ID
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

v2.4 每条影响在 review.impactBasis 中记录观察期、证据和基线/结果；不计算尚未发生的预期。无可核实影响的 L1 可以 impacts=[]、impactIndex=0，不要捏造影响来满足数组要求。

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
  publisherId?: string;              // v2.4 新建/修改必填：控制主体 ID
  originId?: string;                 // v2.4 新建/修改必填：主要信息起源
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
  supports: string[];                  // 非空：事件 ID 或 claim ID；具体证据仍以 claim/impact.sourceIds 为准
  quote?: string;
}
```

`publishedAt` 表示来源自身的发布日期，`accessedAt` 表示编辑最后一次实际打开并核对该链接的日期，两者不得混用。新建或更新来源时 `accessedAt` 必填；历史来源缺失时校验器报 warning，完成真实链接检查后才能补写，禁止用迁移日期伪装成访问日期。

`independence` 的判定对象是“相对于事件中的核心主张是否独立”，而不是网站类型：

- 当事公司、作者、监管发布主体：`primary_actor`
- 与核心主张无直接利益关系的媒体、研究机构或复核方：`independent`
- 社区帖子与热度聚合：`community_signal`
- 暂时无法判断：`unknown`，不得计入独立来源门槛

v2.4 同时按 publisherId 与摘录级 originId 区分控制主体和信息起源；同一稿件转载不能算独立验证。关系与验证范围写在 review.evidence 每条摘录上。旧 publisher/域名去重只适用于冻结历史记录，不是新证据的独立性判据。

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
  reviewProvenance?: 'legacy_pre_v23' | 'v2.3' | 'v2.4';
  reviewRecord?: string;              // v2.4 审核后必填，governance/reviews 下的相对路径
  screeningRunId?: string;            // 方向必填，回指真实批次
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

`createdAt/updatedAt` 是正式事件必填；`lastReviewed` 是旧别名。v2.4 已审核/发布记录必须有 curator/reviewer/changeLog/lastSourceCheckAt/reviewRecord 等，完整约束见 REVIEW-CONTRACT。历史标记只代表旧记录，不能供新建或修改内容选择；只有内容与依赖指纹均未改变才获历史豁免。publishedAt 不随更新重置。curatorNote 不替代责任与时间字段。

---

## 3. 来源标准

### 3.1 来源分级

| Tier | 定义 | 可用作 |
| --- | --- | --- |
| 1 | 原始来源：论文、官方公告、模型卡、代码仓库、法规原文、法院文件、技术报告 | 事实确认、事件日期、核心能力描述 |
| 2 | 高质量独立来源：主流科技/财经媒体、学术综述、机构报告、监管机构解读 | 影响确认、外部采用、争议背景 |
| 3 | 专家分析与社区整理：研究者博客、专业通讯、会议演讲 | 背景解释、趋势线索、候选发现 |
| 4 | 社区热度信号：社交媒体、HN、Reddit、论坛 | 仅用于发现，不可独立支撑结论 |

类型与层级必须相容：论文、官方公告、模型卡、代码/法规/司法原文和直接技术报告才有资格标为 Tier 1；新闻报道最高为 Tier 2；普通分析和百科默认 Tier 3。v2.4 百科不得以独立 Tier 2 代替主张核实；引用其原始文献时另建真实来源记录。社区内容只能标 Tier 4。

### 3.2 最低来源要求

| 内容类型 | 发布最低要求 |
| --- | --- |
| L1 事件 | 1 个 Tier 1，或 2 个相互独立的 Tier 2 |
| L2 事件 | 核心事实 ≥B，并满足至少一个 SIG-02 路径的独立验证；无一手资料时两个独立 Tier 2 加缺失理由，不能豁免路径条件 |
| L3 事件 | 原始材料、SIG-03 的跨类别/持续性/独立起源门槛；有争议须收录反方来源 |
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
| L1 | Important | 核心事实成立、有记录价值，但尚未证明满足更高路径 |
| L2 | Key | 满足 EDITORIAL-STANDARD SIG-02 中至少一个类别变化路径 |
| L3 | Turning Point | 满足 SIG-03 的跨类别、实证持续性与独立来源条件 |

完整条件、未知处理、对照和升级边界只维护于总表与 policy.json。不设等级比例配额，不能仅按事件年龄升级。

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
| ±3 | 满足 ±2，并达到 IMP-02 的受众/实证持续期门槛 |
| ±2 | 有来源支持的基线→结果实质变化 |
| ±1 | 已观察到方向性后果，但未达实质变化门槛 |
| 0 | 实测中性；不是正负相抵，也不是未知 |

符号表示受影响群体的获益/损害，不表示事件好坏；潜在后果不入指数。完整判定见 IMP-01/02。

### 4.4 影响分：`impactIndex`

正式计算规则：

```
impactIndex =
  dimensionScore      ← 每个影响维度只取最大的 |severity|，再求和 / 3，上限 4
  + evidenceBonus     ← 取所有 impact 中最弱的 evidenceGrade：A=+1.5, B=+1, C=+0.5；D 不得发布
  + durabilityBonus   ← 取最高 timeframe：long=+1.5, medium=+1, short=+0.5, immediate=0
  + scopeBonus        ← 受影响群体数：≥4类+2, 3类+1.5, 2类+1, 1类+0.5；v2.4 仅使用 policy 受众 ID
  + controversyAdj    ← controversy=true 且任一核心 claim 为 C 级时 -0.5，否则 0
```

先将原始分截断到 0-10，再按 `floor(score + 0.5)` 四舍五入为整数。重复添加同一维度或同义 affected group 不得提高分数。现公式各项上限总和为 9，不能为了使用满 0–10 手动加分。v2.4 无观察影响的 L1 返回 0；旧评分不自动重算。

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
| broad | 主要影响有至少两组独立支持且无未解决的实质反证，见 CONS-01 |
| debated | 事实成立，但影响规模、归因或长期后果有明显分歧 |
| emerging | 早期趋势判断，证据正在积累 |

### 4.6 争议标记

按 CONS-01：存在具体且有证据的争议，附 limitation claim；主题涉及安全或法律不自动等于 controversy，证据不足也不自动等于存在争议。

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
- 每个事件的 `searchSummary`、`summary` 和 `narrative` 都包含非空的 `en` 与 `zhHans`，且公开渲染不得用 `searchSummary` 替代 `summary`。
- 每条 claim 的 `id`、`text`、`claimType`、`evidenceGrade`、`sourceIds` 完整且合法。
- Claim 引用的 `sourceIds` 必须存在于 `data/sources.json`，且数组不能为空。
- 每个事件都有 createdAt/updatedAt；v2.4 审核后还需完整审核与批准契约，changeLog 非空。
- 每条方向至少有 2 条 `signals`。
- 每条 `signals` 至少有 1 个 `eventIds` 和 1 个 `sourceIds`。
- `signals[].eventIds` 必须存在于 `events.json`。
- `consensusBasis.resolutionMode = monitor_only` 时不得填写私设公开裁定标准。
- `relatedEvents` 的目标存在性、自引用和重复检查；构建输出自动双向规范化。

覆盖 `events.json`、`forecasts.json` 和 `sources.json` 三类数据。

---

## 6. 可执行契约样例

旧版带省略号的 ChatGPT 示意已移除，避免被误复制为合格数据。完整合成事件、来源、run、review、approval 及错误变体见 [`tests/test_editorial_policy.py`](../../tests/test_editorial_policy.py)。样例仅在临时目录运行，不是真实事实或人工批准。生产字段遵循 [REVIEW-CONTRACT](REVIEW-CONTRACT.md)。
