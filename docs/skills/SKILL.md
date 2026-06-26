# EpochArc 数据管护工作流 Skill

**状态**：跟随项目源文件，非独立文档。源文件变更时本 skill 应同步更新。

**源文件**（规范来源，以这些为准）：
- [WORKFLOW.md](../workflow/WORKFLOW.md) — 发现→初筛→确认→发布全流程
- [DATA-MODEL.md](../data/DATA-MODEL.md) — 数据结构、评分系统、验证规则
- `data/labels.json` — 所有枚举字段的展示标签（中英）

---

## 核心流程（四阶段）

### 一、发现层 → 候选池

扫描可用信源：

| 通道 | 状态 | 采集方式 |
|:--|:--:|:--|
| Hugging Face Daily Papers | ✅ 可用 | `curl https://huggingface.co/api/daily_papers?limit=20` |
| Hacker News | ✅ 可用 | Firebase API（公开） |
| Brave Search → Reddit（代理） | ✅ 可用 | `node search.js -n 10 "reddit.com AI trending"` |
| Brave Search → X/Twitter（代理） | ✅ 可用 | `node search.js -n 10 "x.com AI breakthrough"` |
| Gmail — Import AI | ✅ 已连接，无内容 | `gws gmail users messages list`（需 gws CLI） |
| Gmail — The Batch | ✅ 已连接，未订阅 | 同上 |

详见 [WORKFLOW.md](../workflow/WORKFLOW.md) 信源矩阵。

在年度/批次 sweep 中补充以下**社区热点信号**（解决产品工具/社会文化类遗漏）：

| 信号类型 | 搜索方法 | 发现目标 |
|:--|:--|:--|
| GitHub 增速最快仓库 | `"fastest growing open source AI project {year}"` | 开源工具爆火 |
| 社区爆火 AI 工具 | `"viral AI tool agent {year} GitHub trending"` / `"Hacker News top AI posts {year}"` | 草根产品爆发 |
| AI 概念流行 | `"AI buzzword new term coined {year}"` / `"AI concept went viral mainstream {year}"` | 概念/文化时刻 |
| 商业/资本信号 | `"AI company valuation IPO restructuring {year}"` / `"AI market cap milestone trillion {year}"` | 产业格局变动 |

每一个信号用 5 维 × 0-2 分快速初筛：

| 维度 | 0 分 | 1 分 | 2 分 |
|------|------|------|------|
| 可验证性 | 无原始来源 | 有二级来源 | 原始来源（论文/公告/代码） |
| 新颖性 | 重复旧事 | 小幅增量 | 明确新节点 |
| 外溢影响 | 只在圈内 | 影响单一群体 | 跨研究/产业/政策/公众 |
| 持续性 | 短期热度 | 可能持续 | 已有后续采用或制度化 |
| 来源质量 | 社区流言 | 可靠二级报道 | 原始来源 + 独立确认 |

阈值：0-4 不收录 | 5-7 候选池 | 8-10 直接草稿。

**记录方式**：事件候选可写入本地候选日志（例如 `data/event_screening_log.json`，不要求公开）；首页方向的公开运行记录维护在 `data/possible_directions_screening_log.json`。通过审核后回填 `eventId` 与正式事件关联，形成可追溯链条。

### 发现后检查：6 分类维度覆盖

候选列表出来后，按 6 个分类染色，确保无空白：

- `capability` 能力突破 / `product` 产品工具 / `commerce` 商业产业
- `governance` 治理监管 / `safety` 安全伦理 / `society` 社会文化

如某分类完全空白，在确认层执行定向 Brave 搜索补漏。

### 二、确认层 → Brave Search 四层漏斗 + 分类定向深挖

每个候选执行 4 轮搜索，每轮产出映射到数据模型的不同字段：

| 层 | 搜什么 | 产出字段 |
|----|--------|---------|
| 1️⃣ 事实确认 | 准确时间、主体、参数、原始公告 | `date`, `summary`, `sources` (Tier 1) |
| 2️⃣ 影响分析 | 可观测后果、就业/产业变化 | `ImpactAssessment[]`, `severity`, `affectedGroups` |
| 3️⃣ 行业报告 | 独立第三方权威分析 | `evidenceGrade` 升级 (C→B→A) |
| 4️⃣ 争议批评 | 反方观点、安全伦理风险 | `controversy`, `consensusLevel`, `claims[limitation]` |

**第 5 层 — 按分类定向深挖 + 社区热点信号**：批次收集中若发现某分类空白，执行分类级 Brave 搜索。同时补充社区热点搜索如下：

```bash
# 产品工具类 — 社区爆火信号
"fastest growing open source AI project {year}"
"viral AI tool agent {year} GitHub trending"
"Hacker News top AI posts {year} breakthrough"

# 社会文化类 — 概念流行信号
"AI buzzword new term coined {year}"
"AI concept went viral mainstream {year}"
"AI cultural phenomenon meme trend {year}"

# 商业产业类 — 公司/资本信号
"AI company valuation IPO restructuring acquisition {year}"
"AI market cap milestone trillion valuation {year}"
```

### 三、AI 草稿生成

确认层搜索结果 → agent 生成完整 v2 JSON（`content/events/*.json`）：

- 提取事实信息 → `title`, `summary`, `date`, `datePrecision`
- 识别影响 → `ImpactAssessment[]`, `severity`, `direction`
- 分类来源 → `sources[*].sourceId` 引用 `data/sources.json`
- 识别争议 → `controversy`, `claims[claimType = limitation]`
- 中英双语 → `LocalizedText` 的 `en` 和 `zhHans`
- 计算 `impactIndex`（见 [DATA-MODEL.md](../data/DATA-MODEL.md) 公式）

**AI 不做**（留给人工）：
- `significance` (L1/L2/L3) — 最重要的编辑判断
- 微调 `severity` — AI 评分可能有偏差
- 最终发布决定

### 四、人工审核 → 提交

审核清单在 [WORKFLOW.md](../workflow/WORKFLOW.md)「五、人工审核清单」。通过后：

1. `content/events/` 下提交 JSON
2. 更新 `data/sources.json`（如有新来源）
3. 运行 `scripts/build_events.py` 生成 `data/events.json`
4. 刷新页面验证渲染

---

## 数据模型要点

| 概念 | 说明 |
|------|------|
| `categories` | 字符串数组，1-2 个，第一个为主分类。多分类用 30% 信息丢失测试决定 |
| **日期规则** | 时间轴上的日期 = "大量普通人可感知到这件事的时刻"。渐变事件取引爆点（OpenClaw 取 HN 发布日而非代码首次提交日），概念流行取造词日，持续进行的事件取代表性里程碑日 |
| **6 分类** | `capability` 能力突破 / `product` 产品工具 / `commerce` 商业产业 / `governance` 治理监管 / `safety` 安全伦理 / `society` 社会文化。次分类通过 30% 信息丢失测试准入 |
| `significance` | L1-L3，独立于 impactIndex |
| `impactIndex` | 0-10，公式见 [DATA-MODEL.md](../data/DATA-MODEL.md) |
| `consensusLevel` | broad / debated / emerging |
| `controversy` | boolean，有则必须配 claims[limitation] |
| `sources` | 只存 sourceId，不存完整 URL（查 data/sources.json） |
| `relatedEvents` | 双向引用，脚本会校验 |
| `LocalizedText` | 必须同时有 `en` 和 `zhHans` |

完整类型定义见 [DATA-MODEL.md](../data/DATA-MODEL.md) `## 2. 核心类型定义`。

---

## 标签系统

展示标签统一从 `data/labels.json` 加载，前端 HTML 不硬编码任何映射。分类 `category` 枚举值的语义轴见 labels.json，目前有 6 个分类。

具体定义和判定标准见 [DATA-MODEL.md](../data/DATA-MODEL.md) `## 2.2`。

---

## 历史事件回溯（非发现层流程）

对于 1950 → 至今的已发生事件，不是走 7 信源扫描，而是：

1. **划定范围** — 公认的学科里程碑
2. **里程碑密度** — 年代越近事件越密
3. **概念骨架** — 最少节点讲出一条连续故事线

选择标准：这个事件是否第一次引入了后代沿用至今的概念/范式/方法。

---

## 文件结构

```
project-root/
├── workflow/WORKFLOW.md ← 完整流程（本 skill 的上游）
├── data/DATA-MODEL.md   ← 数据模型和评分体系
├── SKILL.md             ← 当前文件（流程摘要）
├── content/events/      ← 源事件 JSON（每文件一个事件）
├── data/
│   ├── events.json      ← 合并后的公开数据（build 产物）
│   ├── sources.json     ← 来源库
│   ├── forecasts.json   ← Possible Directions 数据
│   ├── possible_directions_screening_log.json ← 方向筛选运行记录
│   └── labels.json      ← 枚举标签映射
├── scripts/
│   └── build_events.py  ← 合并 content/events/*.json
└── index.html           ← 前端（从 data/*.json 加载）
```

---

**本 skill 不替代 [WORKFLOW.md](../workflow/WORKFLOW.md) 和 [DATA-MODEL.md](../data/DATA-MODEL.md)。当流程或模型变更时，先更新那两个文件，再同步本 skill。**
