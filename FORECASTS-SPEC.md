# Future Signals 模块规范

**更新日期**：2026-06-24  
**模块定位**：列出有证据支撑、可被未来裁定的 AI 发展可能性，而不是宣称本站能够预测未来。

---

## 1. 命名与产品定位

首页模块不建议继续叫 `Forward-Looking Predictions`。这个名字太像本站在给确定性预言，但当前产品更像在组织“可能方向”和“可观察信号”。

推荐名称：

- 英文：**Future Signals**
- 中文：**未来信号**

含义：

- `Future`：面向尚未完成的 AI 发展方向。
- `Signals`：每条内容必须来自证据、趋势、约束和反向信号。
- 不承诺确定性，只要求可追踪、可讨论、可裁定。

内部数据可以继续使用 `forecast` 命名，但产品文案应避免给用户“官方预测”的错觉。对外更准确的解释是：**evidence-backed future directions**。

---

## 2. 未来方向从哪里来

未来方向不应来自单一专家观点、社交媒体热度或个人直觉。建议使用“信号篮子”方法做 horizon scanning。

### 2.1 信号篮子

| 信号篮子 | 观察内容 | 典型来源 |
| --- | --- | --- |
| 技术能力 | 新模型能力、评测跃迁、可复现实验、第三方评测 | model cards、technical reports、arXiv、OpenReview、METR、ARC Evals、Papers with Code |
| 产品采用 | 用户规模、企业部署、API 使用、价格变化、工作流替代 | 公司公告、财报、开发者文档、客户案例、可靠媒体 |
| 基础设施 | GPU/ASIC 供给、推理成本、数据中心、电力、开源工具链 | 芯片公司报告、云厂商公告、行业报告、供应链报道 |
| 资本产业 | 融资、并购、收入披露、战略合作、供应链变化 | 财报、SEC 文件、投资机构报告、可靠财经媒体 |
| 政策安全 | 法规、标准、诉讼、监管处罚、安全评测、事故报告 | 官方法规、法院文件、监管机构、标准组织、安全报告 |
| 社会行为 | 劳动力、教育、创作、媒体、公众使用习惯 | OECD、ILO、Stanford AI Index、学术论文、调查报告 |
| 反向信号 | 技术瓶颈、成本瓶颈、监管阻力、采用失败、评测失真 | 反方论文、事故复盘、独立测评、监管文件、行业失败案例 |

### 2.2 候选来源

候选来源分为三层：

1. **发现层**：帮助发现方向，但不能直接支撑发布。
   - Hacker News、Reddit、社交讨论、newsletter、专家博客。
2. **证据层**：支持方向是否值得纳入。
   - 模型卡、论文、benchmark、第三方评测、监管文件、财报、机构报告。
3. **裁定层**：未来用于判断是否达成。
   - 独立 benchmark、审计报告、公开技术报告、法规/法院文件、可复核产品部署。

---

## 3. 是否采纳一个方向

### 3.1 最低准入标准

一条 Future Signal 必须同时满足：

1. **明确命题**  
   能写成一句可理解的未来可能性，而不是泛泛趋势。

2. **时间窗口**  
   必须有 `expectedWindow.start` 和 `expectedWindow.end`。不要只写单一年份。

3. **至少两个支持信号**  
   来自至少两个不同信号篮子，且不能全部来自同一家公司或同一作者。

4. **至少一个反向信号**  
   必须记录约束、失败可能、争议或反方观点。

5. **可裁定标准**  
   必须有 `achievedWhen` 和 `notAchievedWhen`。

6. **相关性**  
   方向应能影响 AI 技术路线、产品化、产业结构、政策安全或社会行为中的至少一项。

### 3.2 采纳评分

候选方向进入公开模块前，建议按 0-2 分打分：

| 维度 | 0 分 | 1 分 | 2 分 |
| --- | --- | --- | --- |
| Evidence | 来源薄弱或单一 | 有可靠来源 | 多个独立可靠来源 |
| Plausibility | 机制不清 | 有合理路径 | 技术/产业/政策路径清晰 |
| Relevance | 影响有限 | 影响一个群体 | 影响多个领域或群体 |
| Resolvability | 难以裁定 | 可部分裁定 | 有明确达成/未达成标准 |
| Timeframe | 时间模糊 | 有宽泛窗口 | 有合理窗口和复核节奏 |
| Counter-signal | 无反方 | 有简单限制 | 有具体反向证据或失败路径 |

建议阈值：

- 0-6：不公开，留在候选池。
- 7-9：继续观察，补来源。
- 10-12：可公开为 Future Signal。

### 3.3 量化、定性与共识

采用混合标准：

- **能量化就量化**：benchmark、采用率、成本、部署数量、法规生效日期。
- **不能量化也要可裁定**：使用独立审计、持续时间、公开可复核材料、权威来源交叉确认。
- **广泛共识不能单独作为达成标准**：共识可以提高可信度，但不能替代可观察证据。
- **投票不是证据**：用户投票只能代表读者预期，不影响方向是否采纳或是否达成。

---

## 4. 达成标准怎么定义

每条 Future Signal 都要有：

- `achievedWhen`：什么算达成。
- `notAchievedWhen`：什么不算达成。
- `measurementSources`：未来裁定时优先看的来源。
- `minimumDuration`：能力或采用是否需要持续一段时间。
- `adjudicationNotes`：边界情况如何处理。

推荐格式：

```md
Achieved when:
The capability appears in at least two independent evaluations or real-world deployments, is available beyond a closed demo, and remains observable for at least 90 days.

Not achieved when:
The claim depends on a private demo, cherry-picked examples, a single benchmark, hidden human handoff, or unverifiable statements.
```

### 4.1 裁定状态

| 状态 | 含义 | 页面处理 |
| --- | --- | --- |
| `active` | 仍在观察 | 留在 Future Signals |
| `resolved_true` | 达成 | 转为已裁定状态，并生成/关联时间轴事件 |
| `resolved_false` | 未达成 | 留档并展示原因，不删除 |
| `partially_resolved` | 部分达成 | 展示哪些条件达成、哪些未达成 |
| `superseded` | 被更准确的新方向替代 | 归档并链接新条目 |
| `retracted` | 原方向有明显错误 | 标记撤回，保留修订说明 |

---

## 5. 达成后如何处理

达成不是把卡片删掉，而是进入“历史闭环”。

处理流程：

1. 更新 Future Signal 状态为 `resolved_true`。
2. 写一条 resolution note，说明哪些证据触发了裁定。
3. 如果影响达到 L1-L3 时间轴标准，新增或关联一个 `AIEvent`。
4. 在 Future Signal 卡片上显示：
   - resolved date
   - outcome
   - linked event
   - original thesis
5. 保留用户投票结果，作为“当时读者如何预期”的历史记录。
6. 后续如果出现反证，用 `correction` 或 `partially_resolved` 更新，不直接覆盖历史。

这会让模块形成一个长期价值：不仅展示未来可能性，也展示过去的预测/方向判断是如何被现实验证或推翻的。

---

## 6. 运营节奏

建议节奏：

- 每周：扫描候选信号。
- 每月：更新已公开 Future Signals 的来源和反向信号。
- 每季度：复核时间窗口、达成标准和是否需要归档/替换。
- 触发式：当出现重大模型发布、法规、第三方评测、事故或产业部署时立即复核。

每次更新应记录：

- 变化摘要。
- 新增来源。
- 评分变化。
- 是否影响达成标准。

---

## 7. 投票的产品逻辑

### 7.1 投票目的

投票不是为了决定真相，也不是为了替代专业判断。它的产品目的有三个：

1. 给用户轻量参与感。
2. 记录读者对未来方向的预期。
3. 在未来裁定后形成“当时大家怎么看”的历史层。

因此投票模块应命名为类似：

- `Reader Pulse`
- `Audience Expectation`
- 中文：`读者预期`

不要叫 `Community Verdict`，因为它不是裁决。

### 7.2 投票问题

每张卡建议问：

> Do you expect this to happen within the stated window?

选项：

- `Likely`
- `Unlikely`
- `Unsure`

中文：

- `可能`
- `不太可能`
- `不确定`

这比单个“投一票”更清楚，也避免所有票都变成“点赞”。

### 7.3 是否允许多投和改投

建议：

- 同一用户对同一方向只有一个当前有效投票。
- 允许改投，因为未来信息会变化。
- 改投后更新当前票，也可额外记录历史投票事件用于趋势分析。
- 页面显示当前分布，不显示“投票排名”。

不建议：

- 允许无限重复累加。
- 用投票数决定卡片排序。
- 把投票比例包装成预测概率。

---

## 8. 无登录防刷设计

第一版不登录是可以的，但要承认它只能做“软防刷”，不能做到强身份。

### 8.1 第一阶段：低摩擦方案

前端：

- `localStorage` 保存用户对每个 direction 的当前选择。
- 用户可改投，但不会重复累加。

后端：

- D1 保存当前投票。
- 使用服务器端 salt 对 IP、User-Agent、forecast id 做 HMAC，生成 `voter_hash`。
- 不保存明文 IP。
- D1 对 `(forecast_id, voter_hash)` 做唯一约束。
- 修改投票时 `upsert`，不新增重复当前票。

Cloudflare：

- 对投票接口做基础 rate limit。
- 出现异常时启用 Turnstile。

### 8.2 第二阶段：可信度增强

如果投票变成核心功能，再考虑：

- 邮箱 magic link。
- GitHub / Google OAuth。
- passkey。
- 用户声誉或长期校准分。

但第一版不建议上登录。它会增加阻力，而投票目前不是核心证据。

### 8.3 D1 表建议

当前票：

```sql
CREATE TABLE forecast_votes_current (
  forecast_id TEXT NOT NULL,
  voter_hash TEXT NOT NULL,
  vote TEXT NOT NULL CHECK (vote IN ('likely', 'unlikely', 'unsure')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (forecast_id, voter_hash)
);
```

可选历史：

```sql
CREATE TABLE forecast_vote_events (
  id TEXT PRIMARY KEY,
  forecast_id TEXT NOT NULL,
  voter_hash TEXT NOT NULL,
  vote TEXT NOT NULL CHECK (vote IN ('likely', 'unlikely', 'unsure')),
  created_at TEXT NOT NULL
);
```

聚合可以实时查询，也可以定时写入缓存表：

```sql
CREATE TABLE forecast_vote_totals (
  forecast_id TEXT PRIMARY KEY,
  likely INTEGER NOT NULL DEFAULT 0,
  unlikely INTEGER NOT NULL DEFAULT 0,
  unsure INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL
);
```

---

## 9. 与时间轴的关系

Future Signals 不应是完全独立的“猜猜玩”。它应该和时间轴形成闭环：

```txt
historical events -> signals -> future direction -> resolution -> historical event
```

产品规则：

- 每条 Future Signal 至少关联 1 条历史事件或 1 类来源信号。
- 卡片详情中展示 `Related Milestones`。
- 达成后，如果影响足够大，转化为时间轴事件。
- 未达成或被替代时，保留为归档记录。

投票可以提供参与感，但模块的核心价值仍应是“证据组织 + 未来裁定”。

---

## 10. 首页产品改动建议

保持当前克制风格，不需要做大改。

### 10.1 标题

将模块标题从：

- `Forward-Looking Predictions`
- `前瞻预测`

改为：

- `Future Signals`
- `未来信号`

### 10.2 卡片信息层级

每张卡建议展示：

1. 标题。
2. 一句话命题。
3. 时间窗口，例如 `2027-2029`。
4. 状态：`Active` / `Resolved` / `Superseded`。
5. 证据等级或信号强度：`Evidence B` / `Signal strength 8/12`。
6. 读者预期三选一。

卡片不要塞满解释，详细的达成标准和来源在展开层或详情页。

### 10.3 投票 UI

当前单按钮 `Vote` 容易被理解成点赞。建议改成紧凑三段式：

```txt
Likely | Unlikely | Unsure
```

投票后显示：

```txt
Reader Pulse: 62% likely · 24% unlikely · 14% unsure
```

文案必须避免：

- `probability`
- `community says`
- `forecast accuracy`

除非未来真的做校准和身份系统。

### 10.4 卡片状态

建议加小状态标签：

- `Active`
- `Resolved`
- `Watching`
- `Needs evidence`

这会让用户知道它不是普通投票卡，而是一个持续运营的方向条目。

---

## 11. 数据字段补充建议

当前 `data/forecasts.json` 已有基本结构。后续建议补：

```ts
sourceSignalScore: number;       // 0-12，按采纳评分生成
publicLabel: 'future_signal';    // 对外模块类型
statusReason?: LocalizedText;
resolvedAt?: string;
resolutionEventId?: string;
reviewCadence: 'monthly' | 'quarterly' | 'triggered';
lastReviewedAt: string;
nextReviewAt?: string;
```

投票字段建议从单一总数升级为三项分布：

```ts
votes: {
  likely: number;
  unlikely: number;
  unsure: number;
  updatedAt: string;
}
```

---

## 12. 结论

Future Signals 应该是 EpochArc 的第二条主线：时间轴回答“已经发生了什么”，Future Signals 回答“哪些未来方向值得持续观察，以及现实最终如何裁定它们”。

它可以有一点参与感，但不能沦为纯投票娱乐。真正的产品价值来自：来源标准、反向信号、达成标准、定期复核，以及达成后与时间轴闭环。
