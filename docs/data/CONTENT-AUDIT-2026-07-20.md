# EpochArc 内容审计（2026-07-20）

## 结论

当前内容已通过 v2.3 **结构发布门禁**：93 个事件、271 个来源、4 条 Possible Directions、6 个 Arcs 均可解析，引用不存在悬空，状态、日期、枚举、来源最低数量和影响分可以复算。

这不等于全部内容已完成 v2.3 事实复核。统一校验仍保留 5 类迁移债务；其中证据等级和来源层级是发布质量风险最高的两类。

## 本轮已修复

1. 修复构建顺序：统一校验和所有生成器先运行，Vite 最后复制最终产物，避免 `dist/data/events.json` 等文件落后于源数据。
2. 补齐 `gemini-robotics-2025` 与 `alphaevolve-2025`，解除 Possible Directions 对不存在事件的引用。
3. 将新闻媒体误标为 Tier 1 的记录统一降为 Tier 2，并在校验器中禁止新闻类型进入 Tier 1。
4. 修复 `ai-winter-1987` 中 `mixed` 方向与有符号严重度冲突。
5. 修复来源标题中丢失的 `$1.25 trillion` 和 `$60 billion`。
6. 修复 CAIS Remote Labor Index 条目：失效 URL 改为当前官方页面；发布日期从 7 月 6 日改为 7 月 1 日；领先结果从 16.1% 改为官方当前页面的 15.8%；删除未经数据支持的“1-3 年内显著冲击”外推。
7. 修复 Inkling 条目：官方模型卡只列文本、图像、音频输入；视频属于预训练数据，不应写成发布模型的视频输入能力；同时删除 `2.8T/?? active` 占位符并降低新发布事件的共识表述。
8. 修复 Kimi K3 条目：区分 7 月 16 日的产品/API 访问与计划于 7 月 27 日提供的完整权重；不再把尚未可独立检查的权重写成已经完成的“最大开源模型发布”，并把厂商基准明确标成待独立复核。
9. 新增 `editorial.reviewProvenance`，把旧数据迁移与按 v2.3 完成的事实复核区分开，防止机械补字段冒充人工复核。
10. 独立来源改为按 publisher/域名去重，堵住“同一机构两条 URL 算两个独立来源”的漏洞；该规则发现并修复了 Grok 深度伪造事件仅靠同域 Wikipedia 支撑的问题，现改用 Ofcom 官方调查与 AP 独立报道，并纠正调查日期和国家封锁范围。

## 尚未清零的问题

### P0 — 211 条证据等级高于来源链可支持的上限

按 v2.3 规则反算后，旧事件中仍有 211 条 claim/impact 的 `evidenceGrade` 偏高：常见情况是单一一手来源标 A、单一二手来源标 B，或把 Wikipedia 与单篇报道组合标为 A。

这些条目目前以 `legacy_pre_v23` 保留并产生聚合警告；任何改为 `reviewProvenance: v2.3` 的事件都会因证据等级高估而校验失败。修复方式只能是补充独立来源或下调等级，不能机械维持原分。

### P0 — 57 个来源缺少 `accessedAt`

本轮对原 61 个缺失项做了 HTTP 可达性初筛，并修复了 CAIS 的硬 404；另对 OpenAI、Anthropic、Thinking Machines、Moonshot 等本轮实际阅读的官方页面补了访问日期。剩余 57 项即使 HTTP 可达，也尚未逐页核对“页面内容是否真的支持对应 claim”，因此没有伪造 `accessedAt`。

HTTP 401/403/429 或网络错误只表示自动访问受限，不等于来源失效；需要人工浏览或替代来源。

### P1 — 39 条 Wikipedia 仍标为 Tier 2

v2.3 默认把 Wikipedia 归为 Tier 3。若现在直接降级，会有 14 个已发布事件不再满足最低来源要求：

`ai-winter-1987`、`alphago-2016`、`character-ai-2022`、`dartmouth-1956`、`deep-blue-1997`、`google-deepmind-2014`、`gpt-2-safety-2019`、`gpt-image-2025`、`gpt3-2020`、`microsoft-tay-2016`、`nvidia-4-trillion-2025`、`perceptron-1958`、`siri-2011`、`transformer-2017`。

因此本轮没有直接降级并让公开时间线缺项；正确顺序是先为这 14 条补一手或独立 Tier 2，再完成降级。

### P1 — 87 个事件仍是旧规范复核状态

93 个事件中只有本轮逐项核验的 6 个事件标为 `reviewProvenance: v2.3`；其余 87 个明确标为 `legacy_pre_v23`。旧 `reviewer`/`reviewedAt` 的机械迁移不再被解释为已按新规范完成事实复核。

### P1 — 11 个近期事件使用 `broad` 共识标签

截至本审计日，近 90 天内仍有 11 个事件标为 `consensusLevel: broad`：`ai-layoffs-wave-2026`、`ai-model-price-war-2026`、`apple-siri-ai-wwdc-2026`、`claude-sonnet-5-launch-2026`、`deepseek-v4-2026`、`doubao-ai-companion-shutdown-2026`、`glm-52-open-source-2026`、`gpt-5-6-broad-launch-2026`、`illinois-ai-safety-law-2026`、`openai-jalapeno-chip-2026`、`sora-shutdown-2026`。

“事实已发生”不等于“主要影响解释已有广泛共识”。这些条目应逐项判断：若 `broad` 只描述事实，应改写标签定义或拆分；若覆盖影响判断，通常应先降为 `emerging` 或 `debated`。

### P1 — 68 条候选筛选记录缺少 `runId`

旧 `data/screening_log.json` 只有逐条 `screenedAt`，没有批次 ID，也无法回溯当次时间窗、通道状态、查询、失败与重试。因此无法证明“没有发现候选”究竟代表执行过覆盖搜索，还是某个通道没有运行。

历史批次信息不得事后臆造。新记录必须携带 `runId` 并回指完整批次记录。

## 外部核验依据

- [CAIS — A Significant Increase in Digital Labor Automation](https://safe.ai/blog/significant-increase-in-digital-labor-automation)
- [Thinking Machines Lab — Inkling announcement](https://thinkingmachines.ai/news/introducing-inkling/)
- [Thinking Machines Lab — Inkling model card](https://thinkingmachines.ai/model-card/inkling/)
- [Moonshot AI — Kimi K3 technical blog](https://www.kimi.com/blog/kimi-k3)
- [OpenAI — GPT-5.6 general availability](https://openai.com/index/gpt-5-6/)
- [Anthropic — Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)
- [Ofcom — investigation into X over Grok sexualised imagery](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-launches-investigation-into-x-over-grok-sexualised-imagery)
- [Associated Press — Malaysia and Indonesia block Grok](https://apnews.com/article/c7cb320327f259c4da35908e1269c225)

## 建议处理顺序

1. 先修 14 个依赖 Wikipedia Tier 2 的事件，完成来源替换和 Wikipedia 降级。
2. 再按事件逐个反算 211 条证据等级，优先 L3、争议事件和 2026 年近期事件。
3. 对 11 个近期 `broad` 标签做语义复核。
4. 逐页复核剩余 57 个来源并补 `accessedAt`；无法访问或不支持 claim 的来源直接替换。
5. 新一轮扫描开始前先建立带 `runId` 的批次记录，不回填虚构的历史运行数据。

## 复现命令

```bash
python3 scripts/validate_all.py
npm run build
```

结构校验通过只表示满足可机器验证的发布契约；最终事实可信度以 `reviewProvenance`、来源链和本审计债务是否清零为准。
