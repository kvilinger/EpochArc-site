# EpochArc 信息收集工作流

**版本**：v2.0  
**更新日期**：2026-06-24  
**适用范围**：从信号发现到事件发布的完整搜集流程，匹配 v2 数据模型（`events.json`、`forecasts.json`、`sources.json`）

---

## 核心原则

### 发现与确认分离

```
发现层 ──────────────→ 候选池 ──────────────→ 确认层 ──────────────→ 发布
多信源自动扫描          初筛 + AI 草稿        Brave Search 深挖       人工审核上线
```

**发现层**回答"有什么值得关注的事发生了"。  
**确认层**回答"这件事的准确事实、可验证影响和可信来源是什么"。

Brave Search 只做确认层的深挖，不做发现层的扫描——否则会漏掉论文、社区信号和未报道的突破。

---

## 一、发现层：7 个信源并行扫描

### 目标

每周自动拉取所有信源，输出一个候选事件列表。每条候选包含：信源地址、简短理由、初步日期。

### 信源矩阵

| # | 信源 | 覆盖类型 | 采集方式 | 时效 |
|---|------|---------|---------|------|
| 1 | **arXiv** (cs.AI, cs.LG, cs.CL) | 研究论文原始流 | `http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&max_results=50` | 日更 |
| 2 | **Hugging Face Daily Papers** | 社区筛选的研究热点 | `GET https://huggingface.co/api/daily_papers?limit=20` | 日更 |
| 3 | **Papers with Code** | 论文的实际影响力（GitHub stars + 引用） | `https://paperswithcode.com/api/v1/papers/?items_per_page=20` | 日更 |
| 4 | **Hacker News** | 科技社区注意力信号 | `https://hacker-news.firebaseio.com/v0/topstories.json` → 过滤 AI/LLM/ML 关键词 | 小时级 |
| 5 | **Reddit r/MachineLearning** | AI 社区热议话题 | `https://www.reddit.com/r/MachineLearning/hot.json?limit=25` | 小时级 |
| 6 | **Import AI 周刊** (Jack Clark) | 高质量人工策展 AI 新闻 | 邮件订阅，每周一封 | 周更 |
| 7 | **The Batch** (Andrew Ng) | 行业向 AI 周报 | 邮件订阅，每周一封 | 周更 |

信源 1~5 可通过脚本一键拉取；6~7 人肉做最后一道安全网。

### 为什么是这 7 个

- **arXiv**：最原始的研究信号，噪音最大但不会漏论文
- **HF Daily Papers**：社区已筛过一遍，专注"值得读的论文"
- **Papers with Code**：代码 + 引用双重验证，区分"被炒作的论文"和"真正好用的论文"
- **HN + Reddit**：社区注意力的风向标，很多重要事件在媒体报道前先在这里发酵
- **Import AI + The Batch**：最后的安全网——防止自动化漏掉政策/社会/文化层面的重要事件

### 采集脚本示例

```bash
# arXiv 最近 50 篇
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=50" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
    link = entry.find('{http://www.w3.org/2005/Atom}id').text
    published = entry.find('{http://www.w3.org/2005/Atom}published').text
    print(f'{published[:10]} | {title[:80]} | {link}')
"

# Hugging Face Daily Papers
curl -s "https://huggingface.co/api/daily_papers?limit=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data:
    p = item['paper']
    print(f\"{p['publishedAt'][:10]} | {p['title'][:80]} | upvotes={item.get('upvotes',0)}\")
"
```

---

### 1A. 发现后检查：6 分类维度覆盖自查

发现层输出的候选事件往往集中在 **能力突破** 和 **产品工具** 两个类别。以下 6 个分类必须在每次收集中逐一自查，确保无空白。

| 分类 | 定义 | 倾向出现的信源 | 典型遗漏信号 |
|------|------|-------------|-------------|
| `capability` — 能力突破 | 前沿模型发布、首次达到超人类水平、新范式改变技术路线 | arXiv, HF, Reddit, 行业报告 | —（最容易发现） |
| `product` — 产品工具 | AI 变成普通人能用的产品/工具，包括开源项目 | HN, GitHub trending, PH, 科技媒体 | 开源小团队爆火易漏；被模型发布信息淹没 |
| `commerce` — 商业产业 | 公司治理、估值市值、行业格局、关键人事、AI 裁员 | 财经媒体, 公司公告, 科技媒体 | 与技术新闻不同频 |
| `governance` — 治理监管 | 法律、监管、法院判例、行政命令 | 新闻, 法律媒体, Import AI | 早期信源不覆盖 |
| `safety` — 安全伦理 | 安全事故、伦理争议、吹哨人、深度伪造 | Import AI, 专业媒体, 安全社区 | 在技术信源中几乎不存在 |
| `society` — 社会文化 | 文化现象、就业危机（社会面）、公众认知时刻 | 主流媒体, HN/Reddit 热帖, Import AI | 在技术信源中几乎不存在；需要主动找 |

**检查方法**：候选列表出来后，按 6 个分类染色，高亮空白类别。对空白类别，在确认层执行定向 Brave 搜索补漏（见第 5 层）。

**频率**：每次收敛事件的批次（而非单事件）执行一次。

---

## 二、候选初筛

从发现层输出的原始信号到候选池，用 0-2 分快速给 5 个维度打分：

| 维度 | 0 分 | 1 分 | 2 分 |
|------|------|------|------|
| 可验证性 | 无原始来源 | 有二级来源 | 有原始来源（论文/公告/代码） |
| 新颖性 | 重复旧事 | 小幅增量 | 明确新节点 |
| 外溢影响 | 只在小圈层讨论 | 影响单一群体 | 跨研究/产业/政策/公众 |
| 持续性 | 短期热度 | 可能持续 | 已有后续采用或制度影响 |
| 来源质量 | 社区流言 | 可靠二级来源 | 原始来源 + 独立确认 |

阈值：
- **0-4 分**：不收录，保留观察
- **5-7 分**：进入候选池
- **8-10 分**：进入草稿，立即启动确认层

---

## 三、确认层：Brave Search 四层漏斗

针对每个候选池中的事件，执行四层搜索。每层产出映射到 v2 数据模型的不同字段。

### 第 1 层：事实确认

**目标**：锁定准确的时间、主体、参数。

```bash
brave search "事件名称 launch date release announcement 2024" -n 5 --content
brave search "事件名称 parameters model architecture paper" -n 5 --content
```

**产出** → 填充 `AIEvent`:

> 初筛评分（五维×0-2）写入 `data/screening_log.json`。确认层完成后，该 entry 的 `eventId` 回填为正式事件 ID，形成"候选→审核→发布"的可追溯链条。

| 搜索到的信息 | v2 字段 |
|-------------|---------|
| 准确日期 | `date`, `datePrecision` |
| 发布主体 | `claims[fact]` |
| 发生了什么 | `summary`、`claims[fact]` |
| 原始公告/论文 URL | `sources` (Tier 1) |

### 第 2 层：影响分析

**目标**：找到这个事件产生的可观测影响。

```bash
brave search "事件名称 impact effect consequence one year later" -n 10 --content
brave search "事件名称 economic disruption job market changed how" -n 5 --content
brave search "事件名称 adoption users enterprise deployment" -n 5 --content
```

**产出** → 填充 `ImpactAssessment[]`:

| 搜索到的信息 | v2 字段 |
|-------------|---------|
| 改变了什么能力 | `impacts[].dimension = capability_leap` |
| 就业/产业变化 | `impacts[].dimension = economic_disruption` |
| 使用门槛变化 | `impacts[].dimension = access_democratization` |
| 新增风险 | `impacts[].dimension = risk_creation` |
| 社会认知变化 | `impacts[].dimension = paradigm_shift` |
| 每个影响的严重度 | `impacts[].severity` (-3 ~ +3) |
| 受影响的群体 | `impacts[].affectedGroups` |
| 影响的时间尺度 | `impacts[].timeframe` |
| 支持影响的来源 | `impacts[].sourceIds` |

### 第 3 层：行业分析报告

**目标**：找到独立第三方的权威分析，提高证据等级。

```bash
brave search "事件名称 analysis report review Stanford AI Index McKinsey" -n 5 --content
brave search "事件名称 MIT Technology Review Ars Technica Nature Science" -n 5 --content
```

**产出** → 提升证据等级：

| 搜索到的信息 | 用途 |
|-------------|------|
| 独立分析文章 | 提升 `impacts[].evidenceGrade` (C → B → A) |
| 行业报告 | 作为 Tier 2 来源 |
| 专家评论 | 填充 `claims[].interpretation` |

### 第 4 层：争议与批评

**目标**：找到反方观点，评估是否标记争议。

```bash
brave search "事件名称 criticism controversy limitation risk danger" -n 5 --content
brave search "事件名称 copyright lawsuit safety concern ethical issue" -n 5 --content
```

**产出** → 填充：

| 搜索到的信息 | v2 字段 |
|-------------|---------|
| 存在权威反方来源 | `controversy = true` |
| 具体反方观点 | `claims[].claimType = limitation` |
| 安全/伦理风险 | `impacts[].dimension = risk_creation` |
| 争议导致共识度低 | `consensusLevel = debated` |

### 第 5 层：按分类定向深挖 + 社区热点信号

在批次收集中，对自查发现的空白分类执行定向搜索。这层搜索**不以单事件为起点**，而是以类别为起点，目的是发现之前被遗漏的事件。

#### 社区热点信号（补充发现层）

对于 `product` 和 `society` 分类，传统技术信源（arXiv、论文）容易遗漏。在年度 sweep 中额外搜索：

```bash
# 产品工具类 — 社区爆火信号
brave search "fastest growing open source AI project {year}" -n 10 --content
brave search "viral AI tool agent {year} GitHub trending" -n 10 --content
brave search "Hacker News top AI posts {year} breakthrough" -n 5 --content

# 社会文化类 — 概念流行信号
brave search "AI buzzword new term coined {year}" -n 10 --content
brave search "AI concept went viral mainstream {year}" -n 5 --content
brave search "AI cultural phenomenon meme trend {year}" -n 5 --content

# 商业产业类 — 公司/资本信号
brave search "AI company valuation IPO restructuring acquisition {year}" -n 10 --content
brave search "AI layoff裁员 company announced {year} citing automation" -n 10 --content
brave search "AI market cap milestone trillion valuation {year}" -n 5 --content
```

#### 分类定向搜索

```bash
# 治理监管类
brave search "AI regulation law bill passed {year}" -n 10 --content
brave search "EU AI Act enforcement implementation {year}" -n 5 --content
brave search "AI lawsuit filed court ruling {year}" -n 10 --content

# 安全伦理类
brave search "AI safety incident whistleblower accident {year}" -n 10 --content
brave search "AI deepfake nonconsensual ban block controversy {year}" -n 10 --content
brave search "AI ethics controversy lawsuit copyright {year}" -n 10 --content

# 能力突破类
brave search "AI first time human expert level benchmark milestone {year}" -n 10 --content
brave search "AI IMO gold mathematics science Nobel {year}" -n 5 --content
brave search "AI new architecture training paradigm paper breakthrough {year}" -n 10 --content
```

**产出**：从搜索结果中识别新候选事件，加入候选池，重新回到第 1-4 层的标准确认流程。

---

## 四、AI 辅助生成 JSON 草稿

确认层搜索完成后，将搜索结果交给 agent 生成完整的 v2 JSON。

**输入**：四层搜索的原始内容（标题、摘要、来源 URL）

**Agent 做的事**：
1. 从搜索内容中提取事实信息，填入 `title`、`summary`、`date`
2. 识别影响类型，生成 `ImpactAssessment[]`，初步评估 `severity` 和 `direction`
3. 将来源分类（primary/official/news/analysis），填入 `sources.json` 结构，事件里只存 `SourceRef`
4. 识别反方观点，决定 `controversy` 和 `claims[].claimType = limitation`
5. 翻译中英双语（`LocalizedText` 的 `en` 和 `zhHans`）
6. 计算 `impactIndex`（基于 dimensionScore + evidenceBonus + durabilityBonus + scopeBonus + controversyAdj）

**Agent 不做的**（留给人工）：
- 确定 `significance` (L1/L2/L3) —— 这是最重要的编辑判断
- 微调 `severity` —— agent 的评估可能有偏差
- 最终决定是否发布

---

## 五、人工审核清单

审核者收到 JSON 草稿后，逐项检查：

### 分类覆盖检查

- [ ] 当前批次覆盖了至少 **5 个以上不同分类**（model/capability/research/product/open_source/regulation/safety/social）
- [ ] 如果某个分类完全空白，确认是该期间确实没有该类别的重要事件（而非遗漏搜索）
- [ ] `category` 选择准确：选择"最能解释为什么被收录"的那个，而不是最容易的那个

### 来源检查

- [ ] 每个 L1 事件至少 1 个 Tier 1 来源（或 2 个独立 Tier 2）
- [ ] 每个 L2 事件至少 1 个 Tier 1 + 1 个独立 Tier 2/3
- [ ] 每个 L3 事件至少 1 个 Tier 1 + 2 个独立 Tier 2
- [ ] 所有来源 URL 可访问（非 404）

### 评分检查

- [ ] `significance` L1-L3 与同类事件一致
- [ ] `impactIndex` 在 0-10 之间，与同类事件的 relative magnitude 一致
- [ ] `severity` 做了拆分（正负影响分别写，不写成模糊的 0）
- [ ] `controversy = true` 的事件有 `claimType = limitation` 的反方主张
- [ ] `consensusLevel` 选择合理（broad / debated / emerging）

### 语言检查

- [ ] `en` 文案适合公开传播
- [ ] `zhHans` 文案已翻译完成

---

## 六、自动化方案

### 第一版：手动触发 + agent 执行

适合个人策展，每周一次：

1. 运行脚本拉取 5 个 API 信源 → 输出候选列表
2. 人工浏览 Import AI + The Batch 邮件 → 补充候选
3. **分类覆盖自查**：按 6 个分类染色候选列表，标记空白类别
4. 对空白类别，agent 执行**第 5 层定向搜索** → 补充遗漏候选
5. 对每个候选，agent 执行四层 Brave Search → 生成 JSON 草稿
6. 人工审核 → 提交到 `content/events/`
7. 运行 `npm run build:data` → 生成 `data/events.json`
8. 前端自动渲染

### 第二版（可选）：Scheduled Worker

如果需要更频繁的更新（如每天），可将步骤 1-3 部署为 Cloudflare Scheduled Worker：

```
Scheduled Worker (每天)
  → 拉取 5 个 API 信源
  → 初筛高分候选
  → 写入候选池（D1 或 content/candidates/）
  → 人工在后台界面筛选和确认
```

---

## 七、常见问题

### Q: 为什么不用 Google News / Bing API 等更多搜索引擎？

Brave Search 对历史事件和学术内容的索引质量足够好。多个搜索引擎不会显著提升覆盖率，只会增加重复结果和噪音。关键在于用对搜索场景——Brave 做深挖，API 信源做发现。

### Q: arXiv 每天几百篇论文，怎么筛？

两层过滤：
1. HF Daily Papers 已经人工筛过一轮——每天 10-20 篇精选
2. Papers with Code 的 GitHub stars 和引用数提供客观热度信号
3. 只有在以上两层被标记为"值得关注"的论文，才会进入 Brave Search 确认层

不会从 arXiv 原始流里人工筛选。

### Q: 发现层会不会漏掉重要的公司发布（如 OpenAI、Google）？

公司官方发布通常：
1. 会在 X/Twitter 上引爆 → HN/Reddit 马上跟上
2. 会被主流科技媒体报道 → Brave Search 能搜到
3. 会在 Import AI / The Batch 周报中被总结

三层保险。如果某个发布连这三层都完全没覆盖，那大概率不符合收录标准（"影响跨出 AI 圈"）。

### Q: 整个流程每周需要多少时间？

| 环节 | 耗时 |
|------|------|
| 脚本拉取 5 个 API 信源 | 自动 |
| 浏览 Import AI + The Batch | 10 分钟 |
| agent 对候选执行 Brave Search + 生成 JSON | 自动（每次 1-3 分钟） |
| 人工审核 | 10-20 分钟 |
| 构建 + 部署 | 自动 |

**合计**：每周 20-30 分钟人工时间。

---

*此文档与 DATA-MODEL.md v2.0 配套使用。
DATA-MODEL.md 定义"存什么"，本文档定义"怎么找到要存的内容"。*
