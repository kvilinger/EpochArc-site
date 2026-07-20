# EpochArc 产品与上线规划

**更新日期**：2026-07-20
**定位**：AI development roadmap, evidence index, and possible directions site.

---

## 1. 产品定位

EpochArc 不是新闻站、论文库或深度研究机构。第一版的核心价值是把 AI 发展的重要事实、来源证据、影响判断和可能方向整理成一条可筛选、可追溯、可更新的路线记录。

目标用户：

- 想快速理解 AI 发展脉络的普通读者。
- 需要有序追踪 AI 里程碑的产品、投资、研究和创作者人群。
- 希望看到未来方向和历史节点如何互相连接的长期关注者。

核心体验：

- 首页直接进入 Possible Directions 和时间轴，不做营销式 landing page。
- 每个节点可展开，看到摘要、影响评估、解读共识和来源。
- Possible Directions 必须来自事件化信号，不是空泛口号或闭门造车的完成标准。
- 方法页公开收录和评分规则，让读者知道本站如何判断。

---

## 2. 内容边界

收录重点：

- 改变 AI 技术路线、产品化路径、社会认知、监管议程或产业结构的事件。
- 可被来源验证的事实节点。
- 与已发生事件形成闭环、且仍值得持续观察的中期方向。

不追求：

- 每日新闻覆盖。
- 论文全量索引。
- 对每个事件都写长篇深度分析。
- 用本站投票结果替代事实证据。

---

## 3. 公开方法页策略

建议公开 `Methodology & Sources`，但只公开用户需要监督的方法，不公开内部抓取细节。

应公开：

- 收录标准。
- 来源分级。
- L1-L3 重要度定义。
- Impact Score 的基本含义。
- 共识度和争议标记定义。
- Possible Directions 的公开方法、共识搜索与限制说明。
- 修订、纠错和局限性说明。

不必公开：

- API key、抓取脚本、内部提示词。
- 未审核候选池。
- 个人内部备注。
- 可能涉及版权风险的全文缓存。

这样做的价值：

- 提升可信度。
- 降低读者对主观评分的疑虑。
- 方便未来被引用、合作或商业化。

---

## 4. 第一版技术架构

推荐第一版：

- **Cloudflare Pages**：托管静态前端、JSON 数据、预览部署、自定义域名。
- **Pages Functions**：处理轻量动态接口，例如投票、反馈、候选提交。
- **Cloudflare D1**：保存投票、反馈、候选提交、更新日志等结构化数据。
- **Cloudflare R2**：可选，用于保存来源快照索引、截图或未来归档附件。
- **Scheduled Worker**：可选，用于定时抓取候选信号，不直接自动发布。

不建议第一版把所有内容放进动态数据库。当前核心价值是策展质量，不是实时更新；文件化内容更容易人工 review、版本追踪和回滚。

### Pages 还是 Workers

| 方案 | 适合场景 | 推荐度 |
| --- | --- | --- |
| Cloudflare Pages | 静态站、JSON 数据、预览部署、Git 发布、少量 API | 第一版首选 |
| Workers + Static Assets | 动态 API 更重、边缘逻辑多、需要统一 Worker 入口 | 第二阶段可考虑 |
| Pages + 独立 Worker | 静态站独立，自动抓取/任务队列独立 | 推荐的渐进式方案 |

结论：**先用 Pages，上线更快；投票用 Pages Functions + D1；自动收集用独立 Scheduled Worker。**

---

## 5. 当前目录与权威来源

项目已经进入结构化内容生产阶段。编辑源与构建产物必须分离：

```txt
data/
  events.json
  forecasts.json
  sources.json
  schema/
    event.schema.json
    forecast.schema.json
    source.schema.json

content/
  events/
  arcs/

scripts/
  validate_all.py
  validate_forecasts.py
  build_events.py
  build_arcs.py

```

- `content/events/*.json` 与 `content/arcs/*.json` 是编辑源。
- `data/events.json` 是事件构建产物，不得手工编辑。
- `data/sources.json`、`data/forecasts.json`、筛选日志目前仍是受版本控制的编辑源。
- `data/arcs.json` 由 `content/arcs/*.json` 自动生成，只作为前端清单，不得手工登记。
- 结构和流程变更必须在同一个提交中同步更新规范、验证器、数据迁移和测试结果。

---

## 6. 更新流程

1. 自动或手动收集候选信号。
2. 写入 `data/screening_log.json`；同一候选 ID 只保留一条当前记录，历史变化写入记录内的 review history。
3. 人工筛选后生成 `content/events/*.json`，方向数据维护在 `data/forecasts.json`。
4. 运行 `python3 scripts/validate_all.py`：
   - 必填字段。
   - 来源 URL 不为空。
   - L2/L3 来源数量达标。
   - Claims 字段、证据等级和来源绑定完整。
   - Editorial 至少包含 `createdAt` 与 `updatedAt`。
   - Possible Directions 必须具备事件锚点、observed signals、counterSignal 与共识状态。
   - 多语言字段完整性。
5. 构建生成 `data/events.json`、`data/arcs.json` 和静态页面。
6. Cloudflare Pages 自动部署。
7. 每月检查断链和更新来源访问日期。

---

## 7. Possible Directions 与 Reader Pulse

Possible Directions 的完整数据来源、采纳标准、事件联动、读者交互和运营规则见 [FORECASTS-SPEC.md](FORECASTS-SPEC.md)。

核心原则：

- 首页模块对外命名为 `Possible Directions / 可能方向`，不是 `Predictions`；`Future Signals` 只保留在内部方法语境。
- 每条方向必须有事件化信号、反向约束、时间窗口，以及 `monitor_only` 或 `consensus_gated` 的公开状态。
- 用户投票命名为 `Reader Pulse / 读者预期`，只代表参与者预期，不作为事实证据。
- 不登录的第一版使用 localStorage + D1 `voter_hash` + rate limit 做软防刷。
- 同一用户对同一方向只有一个当前有效投票，但允许改投。
- 方向首先必须由时间轴事件支撑；只有未来出现外部共识基础时，才讨论是否进入公开裁定。

第一版可以先保留低摩擦投票，但不要把投票排序、投票比例或读者意见包装成预测概率。

---

## 8. 阶段路线

### 已完成：结构化内容生产

- `content/events/` 与 `content/arcs/` 已投入使用。
- 事件与 Arc 已由构建脚本生成公开数据和页面。
- Possible Directions 已采用事件化信号与 `monitor_only` 规则。
- 主要可索引页面已声明 Atom 自动发现，事件页使用独立的 1200 × 630 PNG 分享图。
- 英文页面使用默认路径，简体中文页面生成到 `/zh-hans/`；两种语言均有自指 canonical、双向 hreflang 和 sitemap 条目。

### 当前阶段：发布门禁与历史数据清理

- 统一数据校验入口并接入 `npm run build`。
- 清理旧来源字段、筛选日志枚举和缺失的编辑元数据。
- 修复方向与 Arc 的悬空引用。
- 建立持续的链接与事实复核报告。

### 后续阶段：动态能力

- Pages Functions + D1 投票。
- Feedback / submit candidate 表单。
- Scheduled Worker 生成候选池。
- 每月自动断链检查。

---

## 9. 视觉与交互规范

### 品牌

- 品牌名：EpochArc。
- 首页主标题：`What Comes Next?`
- 方向模块标题：`Possible Directions / 可能方向`
- 语气：克制、清晰、信息优先，不刻意宏大。

### 颜色

| Token | Value | Usage |
| --- | --- | --- |
| `--bg` | `oklch(98.5% 0.003 240)` | 页面背景 |
| `--surface` | `oklch(100% 0 0)` | 卡片和控件 |
| `--surface-hover` | `oklch(97% 0.004 240)` | hover 状态 |
| `--fg` | `oklch(15% 0.015 250)` | 主文字 |
| `--muted` | `oklch(52% 0.012 250)` | 辅助文字和元信息 |
| `--border` | `oklch(90.5% 0.006 250)` | 边框 |
| `--accent` | `oklch(58% 0.18 255)` | 进度、投票、重点状态 |

### 字体

- Display：`-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", "PingFang SC", sans-serif`
- Body：`-apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", "PingFang SC", sans-serif`
- Mono：`"JetBrains Mono", "IBM Plex Mono", Menlo, monospace`

### 布局

- 内容最大宽度：`960px`。
- 首页直接进入 Possible Directions 和时间轴，不做 landing page。
- 卡片圆角保持 8-12px，不使用过度胶囊化的大面积容器。
- 时间轴要保持时间、轴线、圆点和右侧节点的几何对齐。
- 详情内容在原节点内展开，不弹出独立大卡。

### 导航

- 页眉在首页和方法页保持一致：品牌 logo + `EpochArc` + 语言选择 + 深浅色切换。
- 多语言第一版只保留 `EN` 和 `中文`，语言切换必须在默认英文 URL 与 `/zh-hans/` 中文 URL 之间跳转。
- 页脚保留 RSS 与 `Methodology` 链接。

---

## 10. 最小上线清单

1. 补齐 L2/L3 事件的可点击来源 URL。
2. 每个 L3 事件至少有 2 个独立来源。
3. 每个 Possible Direction 都有事件化信号和来源链路。
4. 方法页公开来源分级、信号规则、`monitor_only` 逻辑和限制说明。
5. 数据校验脚本能在部署前阻断明显错误。
6. 投票如上线，必须有隐私说明和反刷策略。
7. 确认构建生成双语 `sitemap.xml`，并抽查两种语言页面的 canonical、hreflang 与 `og:url`。
8. 部署后做 Lighthouse、移动端截图、链接校验和来源链接检查。
