# EpochArc 数据模型与内容治理规范

**版本**:v2.1
**更新日期**:2026-06-24
**适用范围**：AI 历史时间轴、未来信号、来源证据、评分标准与内容治理
**目标**:让 EpochArc 成为一个可持续维护、可公开解释、可被质疑和修正的 AI 发展记录网站。

产品定位、技术路线、投票实现和视觉规范见 [PRODUCT-PLAN.md](/Users/gang/Documents/Project/WhereIsAIGoing/PRODUCT-PLAN.md)。

---

## 0. 对现有 v1.1 的评估

现有文档的方向是合理的:已经把事件拆成分类、影响维度、重要度、可信度和来源,也意识到不能只靠单一搜索引擎收集内容。这是一个好的第一版骨架。

但如果要长期上线,需要补强以下问题:

1. **事实、影响判断和预测没有完全拆开**
   历史事件是"已发生事实",影响评估是"基于证据的解释",预测是"尚未发生的可检验判断"。三者必须分层,否则可信度会混在一起。

2. **数据字段与真实 JSON 不一致**
   v1 数据曾同时存在字符串 `title/summary`、旧语言块 `zh/en` 和未规范化的 `impactIndex`。v2 已直接迁移为 `LocalizedText`、来源引用和正式评分字段。

3. **来源字段太薄**
   当前只存 `title/url/type/date/author`,不足以支撑未来的公开质疑、断链修复、归档、来源分级和中立性审计。

4. **评分口径偏主观**
   `significance`、`severity`、`consensusLevel`、`impactIndex` 需要可执行的判定标准,否则不同时间补内容时会越来越漂。

5. **预测缺少达成标准**
   v1 预测只有标题、描述和预计年份。v2 使用 `forecasts.json`,预测必须定义:什么算发生、什么不算发生、看哪些证据、何时裁定。

6. **缺少内容状态和修订记录**
   公开站点需要知道一条内容是候选、草稿、已审核、已发布还是已废弃;同时要保留关键修订原因。

结论:v1.1 可以作为原型;v2.0 应当成为正式上线前的数据治理基线。

---

## 1. 核心原则

### 1.1 分层表达

每条内容都要区分四层:

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| Fact | 可验证事实 | OpenAI 于 2022-11-30 发布 ChatGPT |
| Claim | 来源中的主张 | "ChatGPT helped popularize generative AI" |
| Assessment | 本站评估 | 该事件是 L3 转折点,影响维度包括普惠化和范式转变 |
| Forecast | 未来判断 | 2027-2029 年可能出现可被公开验证的通用智能系统 |

页面文案可以写得自然,但数据层必须能追踪每个判断来自事实、来源主张还是本站评估。

### 1.2 中立不是没有判断

EpochArc 不是新闻数据库,也不是论文检索器。它允许做判断,但判断必须满足:

- 可解释:为什么是 L2 或 L3,要有评分依据。
- 可追溯:重要判断能回到来源、证据或反方观点。
- 可修正:当新证据出现时,保留更新记录。
- 不装作绝对客观:公开说明这是结构化策展,不是终局裁判。

### 1.3 宁缺毋滥

一个事件宁可暂时留在候选池,也不要因为短期热度直接发布。尤其是:

- 只有社交媒体热度、没有原始来源的内容,不发布为正式节点。
- 单一公司营销说法,只能作为候选,不足以支撑影响评估。
- 对未来的判断必须写成预测,不要伪装成事实。

---

## 2. 正式数据模型

### 2.1 事件:`AIEvent`

```ts
export interface AIEvent {
  id: string;                         // 稳定 ID,如 "chatgpt-2022"
  slug: string;                       // URL 友好 slug,可与 id 相同

  title: LocalizedText;               // 多语言标题
  summary: LocalizedText;             // 2-5 句,说明发生了什么
  narrative?: LocalizedText;          // 展开详情,说明背景、影响和争议

  date: string;                       // YYYY-MM-DD / YYYY-MM / YYYY
  datePrecision: DatePrecision;
  displayDate?: LocalizedText;        // 如 "November 30, 2022"

  categories: EventCategory[];         // 1-2个分类，第一个为主分类
  status: ContentStatus;              // candidate / draft / reviewed / published / archived

  significance: SignificanceLevel;    // L1-L3
  impactIndex: number;                // 0-10,按 5.4 规则给出
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
  | 'broad'       // 广泛共识
  | 'debated'     // 事实成立,但意义、规模或后果仍有争议
  | 'emerging';   // 新兴判断,证据还在积累

export type EventCategory =
  | 'capability'   // 能力突破
  | 'product'      // 产品工具
  | 'commerce'     // 商业产业
  | 'governance'   // 治理监管
  | 'safety'       // 安全伦理
  | 'society';     // 社会文化
```

#### 直接迁移原则

网站尚未正式上线,因此不保留旧结构兼容层。正式数据直接按 v2 结构维护:

- `title`、`summary`、`narrative` 使用 `LocalizedText`。
- 不再保留顶层字符串 `title/summary`。
- 不再保留旧语言块 `zh/en`。
- `impactIndex` 是正式字段，必须按评分规则解释。
- 事件中的 `sources` 只保存 `SourceRef`；完整来源记录放在 `data/sources.json`。
- 预测统一使用 `data/forecasts.json`，不再使用 `data/predictions.json`。

#### 语言要求

`LocalizedText` 中 `en` 和 `zhHans` 均为必填字段。其他语言可选。

内容生产流程中，AI 负责中英互译，人工只需审核即可发布，不存在翻译瓶颈。

#### 文件组织

```
content/events/*.json      ← 编辑源文件（agent + 人工修改这里）
content/forecasts/*.json   ← 编辑源文件
  ↓ npm run build:data
data/events.json           ← 构建合并输出，前端消费
data/forecasts.json        ← 同上
data/sources.json          ← 从事件/预测中自动提取生成
```

编辑流程清晰：修改 `content/events/*.json` → 运行构建脚本 → 生成 `data/*.json` → 前端自动读取。

---

### 2.2 事件分类：`categories`

`categories` 是一个长度为 1-2 的数组。第一个是**主分类**（前端徽章着色和筛选以此为准），第二个是可选的**次分类**（当事件的重要叙事需要两个维度才能完整表达时使用）。

分类描述的是事件的**主属性**，不是影响结果；影响结果放在 `impacts.dimension`。

#### 六分类定义

| Category | 中文 | 一句话 | 判定标准 |
| --- | --- | --- | --- |
| `capability` | 能力突破 | AI 做到了以前做不到的事 | 前沿模型发布、首次达到人类/超人类水平、新范式（论文/架构/训练方法）改变了技术路线。不包含每次 benchmark 提升——必须是"能讲给不用 AI 的普通人听，对方会觉得'哇，真的吗'"的突破 |
| `product` | 产品工具 | AI 变成了普通人能用的东西 | AI 能力进入用户可使用的产品、工具、工作流或平台。包括开源项目被当作产品使用（如 OpenClaw）。包含产品上线、重大迭代、退出市场（如 Sora 关停） |
| `commerce` | 商业产业 | AI 公司、资本、市场的关键变化 | 公司治理重组、估值/市值里程碑、行业格局改变（如一家公司影响整个市场）、关键人事变动、重大交易/合作/收购、以 AI 为由的大规模裁员（作为商业决策面） |
| `governance` | 治理监管 | 政府开始管 AI 了 | 法律、监管、法院判例、行政命令、国际协议、监管机构行动。面向行业监管而非个别公司 |
| `safety` | 安全伦理 | AI 闯祸了，或引发伦理危机 | 安全事故、伦理争议、吹哨人事件、安全评测揭示新风险、深度伪造事件、版权诉讼（当核心争议是 AI 失控而非商业利益时） |
| `society` | 社会文化 | AI 改变了社会，不用 AI 的人也能感受到 | 文化现象（如 vibecoding 流行、"养龙虾"梗）、就业危机（作为社会影响面）、公众认知时刻（如诺贝尔奖认可 AI）、开源运动改变行业权力结构 |

#### 多分类规则

一个事件最多 2 个分类。加第二分类的条件：

> 对候选的第二分类，问：**"如果删掉这个分类维度，讲这个事件时会丢失多少信息？"**
> 丢失 ≥ 30% → 加为第二分类；丢失 < 30% → 不加。

**判定启发：**

| 主分类 | 常见第二分类 | 典型触发条件 |
| --- | --- | --- |
| `capability` | `commerce` | 模型发布引发巨大市场波动（如 DeepSeek R1 → $593B 美股蒸发） |
| `capability` | `society` | 技术突破被全社会认可为文化时刻（如 AlphaFold 获诺贝尔奖） |
| `commerce` | `society` | 公司决策引发大规模就业危机（如 Meta 裁 8000 人） |
| `governance` | `safety` | 诉讼或监管直接源于安全事故（如佛罗里达诉 OpenAI） |
| `product` | `commerce` | 产品变动揭示商业压力（如 Sora 关停 → 成本压力） |
| `product` | `society` | 产品成为文化现象（如 OpenClaw 引发中国"养龙虾"热潮） |
| `safety` | `society` | 安全事件引发公众广泛关注（如 Grok 深度伪造多国封禁） |

**反例（不加第二分类）：**
- GPT-4 发布：`capability` 为主，产品面可通过 `claims` 表达，信息丢失 < 30% → 不加 `product`
- 欧盟 AI 法案通过：`governance` 足够，社会影响是长期后果 → 不加 `society`

#### 日期选择规则

时间轴上的日期是 **"大量普通人可感知到这件事的时刻"**，而不是最早的酝酿或代码提交时间：

| 事件形态 | 日期取什么 | 例子 |
| --- | --- | --- |
| 单日事件 | 发生日 | GPT-4 发布日、佛罗里达诉讼提起日 |
| 渐变 + 引爆 | 引爆点（新闻量/GitHub stars/社交讨论爆发的那天或那周） | OpenClaw 取 2026-01-25（HN 发布引爆），而非 2025-11-24（Warelay 首次提交） |
| 无明确引爆点 | 最早的大规模公开报道日 | vibecoding 概念流行取 Karpathy 造词那天（2025-02），而非后续数月的扩散 |
| 仍在进行中 | 取有代表性的里程碑日 | AI 裁员潮取 Meta 宣布裁 8000 人那天（2026-05-19），这本身代表了一个可测量拐点 |

酝酿期和后续扩散放在 `narrative` 中叙述，不改变时间轴日期。

---

### 2.3 事件主张:`EventClaim`

`claims` 用来把"来源说了什么"和"本站怎么判断"拆开。

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
  | 'B'   // 一个原始来源,或两个可靠二级来源
  | 'C'   // 来源可信但证据较薄,适合保守表达
  | 'D';  // 发现信号或单方观点,不应单独支撑正式结论
```

使用原则:

- 每个 L2/L3 事件至少要有 2 条 `claim`:一条事实主张,一条影响主张。
- 如果 `controversy = true`,必须至少有一条 `claimType = limitation` 或反方来源。
- `EvidenceGrade = D` 的内容可以进入候选池,但不应作为正式事件的核心依据。

---

### 2.4 影响评估:`ImpactAssessment`

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

注意:

- `severity` 描述影响方向和强度,不描述确定性。
- 确定性由 `evidenceGrade` 和 `consensusLevel` 表达。
- 如果同一事件既带来普惠化又带来风险,不要写成一个模糊的 0 分;应拆成两个 impact。

---

### 2.5 来源:`Source`

来源使用独立表:`data/sources.json`。事件中只引用 `sourceIds`,不再内嵌完整来源对象。

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
  language?: string;                  // BCP 47,如 "en", "zh-CN"

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
  quote?: string;                     // 短引用,避免大段摘录
}
```

---

### 2.6 未来信号：`AIForecast`

对外产品命名使用 **Future Signals / 未来信号**，避免让用户误以为本站在做确定性预测。内部数据仍使用 `AIForecast` / `forecasts.json`，含义是“可裁定的未来方向记录”。

完整采纳标准、投票逻辑和运营规则见 [FORECASTS-SPEC.md](/Users/gang/Documents/Project/WhereIsAIGoing/FORECASTS-SPEC.md)。

未来信号必须独立建模，不应只靠 `expected + description`。

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
  probability?: number;               // 0-100,可选;没有严格校准前不要强行写
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

未来信号卡展示时建议显示：

- 预测窗口:例如 `2027-2029`,不要只写单一年份。
- 置信度:低 / 中 / 高,不要早期就伪装成精确概率。
- 达成标准:用可观察指标写清楚。
- 反方信号:至少保留 1 条,避免把预测写成宣传语。

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
| 1 | 原始来源:论文、官方公告、模型卡、代码仓库、法规原文、法院文件、公司技术报告 | 事实确认、事件日期、核心能力描述 |
| 2 | 高质量独立来源:主流科技/财经媒体、学术综述、机构报告、监管机构解读 | 影响确认、外部采用、争议背景 |
| 3 | 专家分析与高质量社区整理:研究者博客、专业通讯、会议演讲、行业评论 | 背景解释、趋势线索、候选发现 |
| 4 | 社区热度信号:社交媒体、HN、Reddit、论坛、未核实流言 | 只能用于发现,不可单独支撑正式结论 |

### 3.2 最低来源要求

| 内容类型 | 发布最低要求 |
| --- | --- |
| L1 事件 | 至少 1 个 Tier 1 来源,或 2 个相互独立的 Tier 2 来源 |
| L2 事件 | 至少 1 个 Tier 1 来源 + 1 个独立 Tier 2/3 来源 |
| L3 事件 | 至少 1 个 Tier 1 来源 + 2 个独立 Tier 2 来源;若有争议,必须收录反方来源 |
| 影响评估 | 每个核心影响至少 1 个可追溯来源;L2/L3 影响建议 2 个来源 |
| 预测 | 至少 2 个支持信号 + 1 个反方或限制信号 |
| 投票结果 | 只能显示用户意见,不得作为事实证据 |

### 3.3 来源记录规范

每个正式来源尽量补齐:

- 原始 URL。
- `accessedAt`。
- 发布日期。
- 发布机构或作者。
- 归档链接:优先使用 Internet Archive、perma.cc 或 Cloudflare R2 自建快照索引。
- DOI、arXiv ID、GitHub repository 等机器可识别标识。

注意版权:可以保存短引用、摘要、元数据和自己的评估;不要公开复制整篇付费文章或大段受版权保护文本。

---

## 4. 收集与过滤方案

### 4.1 候选收集漏斗

```
发现信号 -> 候选池 -> 事实确认 -> 影响评估 -> 人工审核 -> 发布 -> 定期复核
```

#### A. 发现信号

建议按类型覆盖,而不是只按平台覆盖:

| 信号类型 | 推荐来源 |
| --- | --- |
| 研究论文 | arXiv, OpenReview, ACL Anthology, NeurIPS/ICML/ICLR proceedings, Hugging Face Daily Papers |
| 模型与产品 | 公司博客、模型卡、API 文档、发布会、GitHub release |
| 开源生态 | GitHub trending/releases, Hugging Face models/datasets, Papers with Code |
| 政策法规 | EU、US、China、UK 等监管机构原文,法院文件,官方新闻稿 |
| 社会经济 | OECD、ILO、IMF、World Bank、Stanford AI Index、McKinsey、Goldman Sachs 等报告 |
| 社区注意力 | Hacker News, Reddit, X/Bluesky, 专业 Newsletter |
| 安全伦理 | METR, ARC Evals, Anthropic/OpenAI safety reports, academic safety papers |

社区来源用于发现,不用于独立确认。

#### B. 候选初筛

候选事件进入人工审核前,先按 0-2 分快速打分:

| 维度 | 0 分 | 1 分 | 2 分 |
| --- | --- | --- | --- |
| 可验证性 | 无原始来源 | 有二级来源 | 有原始来源 |
| 新颖性 | 重复旧事 | 小幅增量 | 明确新节点 |
| 外溢影响 | 只在小圈层讨论 | 影响单一群体 | 跨研究、产业、政策或公众 |
| 持续性 | 短期热度 | 可能持续 | 已有后续采用或制度影响 |
| 来源质量 | 社区流言 | 可靠二级来源 | 原始来源 + 独立确认 |

建议阈值:

- 0-4:不收录,保留观察。
- 5-7:候选池。
- 8-10:进入草稿。

#### C. 人工审核

人工审核至少检查:

- 日期是否准确。
- 标题是否克制,没有夸张词。
- 来源是否足以支撑事实和影响。
- `significance` 是否与同类事件一致。
- 是否存在明显反方观点。
- 英文主文案是否适合公开传播。

---

## 5. 评价标准

significance（L1-L3）和 impactIndex（0-10）是两套独立的评价体系：

- **significance (L1-L3)** — 编辑判断的历史重要度，回答"如果没有它，AI 的故事还一样吗？"。由人根据定性标准判断，不使用公式。
- **impactIndex (0-10)** — 数据驱动的可观测影响评分，回答"它实际影响了多少人、多广、多久？"。基于影响维度、严重度、证据等级、持续性、受众广度计算。

两者互不包含。有时一致（L3 + 高 impactIndex），有时不一致（L3 但影响需要时间发酵，或 L2 但引爆了巨大社会反响）。不一致本身有信息量，前端可以同时展示两个值。

### 5.1 重要度：L1-L3

| 等级 | 名称 | 判定标准 |
| --- | --- | --- |
| L1 | Important | 对长期脉络有记录价值;影响明确但范围有限;通常不单独改变行业方向 |
| L2 | Key | 推动研究范式、产品采用、商业模式、政策讨论或公众认知中的至少一项;有独立来源确认 |
| L3 | Turning Point | 改变主流技术路线、公众认知、资本配置、监管议程或社会行为;影响跨领域且可持续 |

辅助判断:

- L3 不应过多。一个时代节点如果没有"前后叙事明显改变",通常不是 L3。
- 古早理论事件可以是 L3,但需要证明其长期引用和范式影响。
- 新事件默认不要急着给 L3,除非影响已经外溢到多个群体。

### 5.2 影响维度

| 维度 | 关注问题 |
| --- | --- |
| capability_leap | AI 是否获得了此前不可行或显著不可用的新能力? |
| economic_disruption | 是否改变就业、成本结构、商业模式、产业链或资本配置? |
| access_democratization | 是否让更多人获得能力,或反过来加强少数主体的控制? |
| risk_creation | 是否制造新的安全、偏见、版权、失控、滥用或伦理风险? |
| paradigm_shift | 是否改变社会对智能、创造力、知识劳动或人的理解? |

### 5.3 严重度:-3 到 +3

| 分值 | 含义 |
| --- | --- |
| +3 | 极强正向影响:跨领域、长期、可重复观察 |
| +2 | 明确正向影响:对一个或多个群体产生实质改变 |
| +1 | 有限正向影响:方向清楚但范围或持续性有限 |
| 0 | 中性、影响未明,或正负高度混合且无法拆分 |
| -1 | 有限负向影响:风险存在但范围有限 |
| -2 | 明确负向影响:已造成可观察损害或高概率结构性风险 |
| -3 | 极强负向影响:跨领域、长期、难以逆转或可能造成重大安全后果 |

不要把"影响很大但有好有坏"直接写成 0。应拆成多个维度分别评分。

### 5.4 影响分：`impactIndex`

`impactIndex` 用于前端快速展示，建议 0-10 分。它与 `significance`（L1-L3）独立计算，不包含重要度信息。

推荐公式：

```
impactIndex =
  dimensionScore      ← 影响维度的广度与强度
  + evidenceBonus     ← 证据等级加分
  + durabilityBonus   ← 影响持续性加分
  + scopeBonus        ← 受众广度加分
  + controversyAdj    ← 争议调整
```

| 项 | 规则 |
| --- | --- |
| dimensionScore | 对所有影响维度取 severity 绝对值求和，除以 3，上限 4 分。
例如：capability_leap +3 + paradigm_shift +2 + risk_creation -1 → (3+2+1)/3 = 2.0 |
| evidenceBonus | A=+1.5，B=+1，C=+0.5，D=-1（取该事件所有影响评估中最低的 evidenceGrade） |
| durabilityBonus | 取所有影响中最高 timeframe：long=+1.5，medium=+1，short=+0.5，immediate=0 |
| scopeBonus | 受影响群体的总类别数：≥4 类 +2，3 类 +1.5，2 类 +1，1 类 +0.5 |
| controversyAdj | 高争议但证据不足 -0.5；争议本身构成重大公共影响时不扣分 |

最后四舍五入并限制在 0-10。前端显示时建议并列展示两项：**Significance L1-L3** + **Impact Score 0/10**，并在 tooltip 分别解释含义。

### 5.5 共识度

| 值 | 定义 |
| --- | --- |
| broad | 事实和主要影响解释已经被原始来源、独立报道或学界/产业广泛接受 |
| debated | 事实成立,但影响规模、意义、归因或长期后果有明显分歧 |
| emerging | 早期趋势判断,证据正在积累;适合保守措辞 |

### 5.6 争议标记

`controversy = true` 的条件:

- 有权威反方来源。
- 存在法律、伦理、安全或版权争议。
- 事件事实无争议,但社会影响、风险或归因争议很大。
- 预测明显依赖不稳定假设。

---

## 6. 未来信号内容规范

### 6.1 未来信号从哪里来

预测不应来自单一专家观点,也不应来自社交媒体热度。建议使用"信号篮子":

| 信号篮子 | 可观察内容 |
| --- | --- |
| 技术能力 | benchmark、模型报告、第三方评测、可复现实验 |
| 产品采用 | 用户规模、企业部署、API 使用、开发者生态、价格变化 |
| 基础设施 | GPU/ASIC 供给、推理成本、数据中心建设、开源工具成熟度 |
| 资本与产业 | 投融资、并购、收入披露、供应链变化 |
| 政策与安全 | 法规、标准、诉讼、监管处罚、安全评测 |
| 社会行为 | 劳动力市场、教育、创作、媒体、公众使用习惯 |
| 反向信号 | 技术瓶颈、成本瓶颈、监管阻力、采用失败案例 |

一条预测发布前至少要有:

- 2 条支持信号。
- 1 条反向信号或限制条件。
- 明确的时间窗口。
- 明确的达成标准。

### 6.2 达成标准怎么写

预测描述必须能被未来裁定。推荐写法:

```md
Achieved when:
An AI system can complete at least X% of benchmark/task set Y under public or independently audited evaluation, and the capability is available outside a single closed demo for at least 90 days.

Not achieved when:
The result depends only on a private demo, cherry-picked examples, or a benchmark that is later shown to be contaminated or not representative.

Primary measurement sources:
Independent benchmark reports, model cards, peer-reviewed or public technical reports, regulator/auditor documents.
```

### 6.3 示例:AGI 预测的更好写法

不推荐:

> AGI will arrive in 2027.

推荐:

> By 2027-2029, at least one AI system may demonstrate broad autonomous performance across knowledge work, software, scientific reasoning, and multi-step planning under independent evaluation.

达成标准:

- 系统在多个独立评测中达到或超过专业人类基线。
- 能在真实或近真实工作流中连续完成多步骤任务。
- 能力不是单一封闭演示,至少持续公开可用或可被第三方审计 90 天。

未达成标准:

- 只在单一 benchmark 上高分。
- 只展示剪辑 demo。
- 需要大量隐藏人工接管。
- 没有独立评测或可复核材料。

---

## 7. 数据质量守门脚本

上线前建议加入 `npm run validate:data`,至少检查:

- JSON 可解析。
- ID 唯一。
- 日期格式合法。
- L2/L3 来源数量满足要求。
- 所有来源有 URL 或明确 `missingUrlReason`。
- `impactIndex` 在 0-10。
- `severity` 在 -3 到 +3。
- `consensusLevel` 只允许规定值。
- 预测有 `achievedWhen` 和 `notAchievedWhen`。
- `relatedEvents` 双向一致性：若 A 引用 B，B 也必须引用 A；单向引用报 warning。

---

## 8. 文案口径

### 标题

标题尽量克制,避免:

- "震撼"
- "颠覆一切"
- "史诗级"
- "终局"
- "彻底改变人类"

推荐格式:

- `OpenAI launches ChatGPT`
- `Transformer architecture reshapes sequence modeling`
- `EU AI Act establishes a risk-based regulatory framework`

### 预测

预测文案避免:

- `will definitely`
- `inevitable`
- `the end of`
- `solved`

推荐:

- `may`
- `could`
- `is likely to`
- `under current assumptions`
- `would count as achieved if`

### 争议

争议不是削弱内容,而是提升可信度。对于安全、版权、就业、AGI、监管等内容,应主动呈现反方或限制条件。

---

## 9. 数据最小上线标准

正式公开前,建议至少完成:

1. 所有 L2/L3 事件补齐可点击来源 URL。
2. 每个 L3 事件至少有 2 个独立来源。
3. 每个预测有达成标准和未达成标准。
4. 方法页公开来源分级、评分规则和预测裁定规则。
5. 数据校验脚本能在部署前阻断明显错误。
6. 数据校验脚本覆盖 `events`、`forecasts` 和 `sources` 三类公开数据。

---

## 10. 一句话定位

EpochArc 的数据方法不是"宣布 AI 真相",而是把 AI 发展的事实、证据、影响和不确定性放在同一个可审阅的结构里。

---

## 11. 附录：v2 事件完整示例（ChatGPT）

以下是按 v2 所有字段填充的 ChatGPT 事件示例，供新事件录入时参考。

```json
{
  "id": "chatgpt-2022",
  "slug": "chatgpt-launch",
  "title": {
    "en": "OpenAI launches ChatGPT",
    "zhHans": "OpenAI 发布 ChatGPT"
  },
  "summary": {
    "en": "OpenAI released ChatGPT, a conversational AI product based on GPT-3.5, free to the public. It reached 1 million users in 5 days and 100 million in 2 months, becoming the fastest-growing application in history and igniting the global AI democratization wave.",
    "zhHans": "OpenAI 发布基于 GPT-3.5 的对话式 AI 产品 ChatGPT，首次对公众免费开放。5 天注册用户破百万，两个月达到 1 亿用户，成为史上增长最快的应用，引爆全球 AI 大众化浪潮。"
  },
  "narrative": {
    "en": "ChatGPT was not the first large language model, but it was the first to package the technology into a zero-friction consumer product. By combining an intuitive chat interface, free access, and GPT-3.5's conversational fluency, OpenAI created a cultural moment. Within weeks, educators worried about cheating, writers feared obsolescence, and every major tech company scrambled to respond. Microsoft deepened its OpenAI partnership with a $10 billion investment; Google declared a 'code red.' The launch marked the moment AI became a mainstream topic — not just for researchers and tech enthusiasts, but for policymakers, teachers, artists, and the general public.",
    "zhHans": "ChatGPT 不是第一个大语言模型，但它是第一个将这项技术包装成零门槛消费品的产品。凭借直观的对话界面、免费访问和 GPT-3.5 的流畅对话能力，OpenAI 创造了一个文化时刻。数周之内，教育工作者担心作弊，写作者担心被取代，每家大型科技公司都在紧急应对。微软加深了与 OpenAI 的合作，投资 100 亿美元；Google 发布了\"红色代码\"。这个发布标志着 AI 成为主流话题——不再只是研究人员和科技爱好者的讨论，而是进入了政策制定者、教师、艺术家和普通公众的视野。"
  },
  "date": "2022-11-30",
  "datePrecision": "day",
  "displayDate": {
    "en": "November 30, 2022",
    "zhHans": "2022年11月30日"
  },
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
      "description": {
        "en": "For the first time, non-technical users could directly experience LLM capabilities through natural conversation. The dialogue quality far surpassed all previous consumer AI products.",
        "zhHans": "首次让非技术用户通过自然对话直接体验大语言模型的能力，对话质量远超此前所有消费级 AI 产品。"
      },
      "affectedGroups": ["general public", "educators", "content creators"],
      "timeframe": "immediate",
      "evidenceGrade": "A",
      "sourceIds": ["openai-chatgpt-blog-2022", "reuters-chatgpt-users-2023"]
    },
    {
      "dimension": "economic_disruption",
      "severity": -2,
      "direction": "negative",
      "description": {
        "en": "Triggered an AI arms race among tech giants. Microsoft invested $10B in OpenAI and integrated ChatGPT into Bing and Office. Google declared a 'code red.'",
        "zhHans": "引发科技巨头 AI 军备竞赛。微软向 OpenAI 追加投资 100 亿美元并将 ChatGPT 整合进 Bing 和 Office。Google 发布\"红色代码\"紧急追赶。"
      },
      "affectedGroups": ["tech industry", "investors", "startups"],
      "timeframe": "short",
      "evidenceGrade": "A",
      "sourceIds": ["reuters-chatgpt-users-2023", "nyt-google-code-red-2022"]
    },
    {
      "dimension": "access_democratization",
      "severity": 3,
      "direction": "positive",
      "description": {
        "en": "Zero-barrier free registration brought AI to hundreds of millions globally, breaking the perception that AI was only for researchers and large corporations.",
        "zhHans": "零门槛免费注册使全球数亿人首次直接使用 AI，打破了 AI 仅限研究机构和科技公司的壁垒。"
      },
      "affectedGroups": ["general public", "students", "small businesses"],
      "timeframe": "immediate",
      "evidenceGrade": "A",
      "sourceIds": ["reuters-chatgpt-users-2023"]
    },
    {
      "dimension": "risk_creation",
      "severity": -2,
      "direction": "negative",
      "description": {
        "en": "Exposed AI hallucinations, bias, copyright issues, and privacy concerns to public view at an unprecedented scale, accelerating regulatory discussions worldwide.",
        "zhHans": "将 AI 幻觉、偏见、版权侵权、隐私等问题大规模暴露在公众视野，各国监管机构加速 AI 立法进程。"
      },
      "affectedGroups": ["policymakers", "researchers", "legal professionals"],
      "timeframe": "short",
      "evidenceGrade": "B",
      "sourceIds": ["mit-tech-review-chatgpt-one-year-2023"]
    },
    {
      "dimension": "paradigm_shift",
      "severity": 3,
      "direction": "positive",
      "description": {
        "en": "'AI as the next computing platform' shifted from industry consensus to global social consensus. Every sector began reassessing AI's strategic position.",
        "zhHans": "\"AI 是下一个计算平台\"从行业共识变为全球社会共识，各行各业开始重新评估 AI 的战略位置。"
      },
      "affectedGroups": ["general public", "business leaders", "policymakers", "educators"],
      "timeframe": "medium",
      "evidenceGrade": "B",
      "sourceIds": ["mit-tech-review-chatgpt-one-year-2023"]
    }
  ],
  "claims": [
    {
      "id": "chatgpt-launch-fact",
      "text": {
        "en": "OpenAI released ChatGPT on November 30, 2022.",
        "zhHans": "OpenAI 于 2022年11月30日 发布 ChatGPT。"
      },
      "claimType": "fact",
      "evidenceGrade": "A",
      "sourceIds": ["openai-chatgpt-blog-2022"]
    },
    {
      "id": "chatgpt-growth-impact",
      "text": {
        "en": "ChatGPT reached 100 million users within two months, making it the fastest-growing consumer application in history.",
        "zhHans": "ChatGPT 两个月达到 1 亿用户，成为史上增长最快的消费级应用。"
      },
      "claimType": "impact",
      "evidenceGrade": "A",
      "sourceIds": ["reuters-chatgpt-users-2023"]
    }
  ],
  "sources": [
    { "sourceId": "openai-chatgpt-blog-2022", "supports": ["chatgpt-launch-fact"], "quote": "We've trained a model called ChatGPT which interacts in a conversational way." },
    { "sourceId": "reuters-chatgpt-users-2023", "supports": ["chatgpt-growth-impact"], "quote": "ChatGPT is estimated to have reached 100 million monthly active users in January." },
    { "sourceId": "mit-tech-review-chatgpt-one-year-2023", "supports": [], "quote": null },
    { "sourceId": "nyt-google-code-red-2022", "supports": [], "quote": null }
  ],
  "relatedEvents": ["gpt3-2020", "gpt4-2023"],
  "relatedForecasts": ["agi-2027-2029"],
  "editorial": {
    "createdAt": "2026-06-20",
    "updatedAt": "2026-06-24",
    "reviewedAt": "2026-06-24",
    "publishedAt": "2026-06-24",
    "curator": "gang",
    "changeLog": [
      {
        "date": "2026-06-20",
        "changeType": "created",
        "summary": "Initial v2 entry for ChatGPT launch."
      },
      {
        "date": "2026-06-24",
        "changeType": "score_changed",
        "summary": "Adjusted impactIndex from 8 to 9 after evidence review."
      }
    ]
  }
}
```
