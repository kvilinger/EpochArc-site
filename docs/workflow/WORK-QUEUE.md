# 当前工作清单与接手状态

最后核对：**2026-11-27 UTC**。维护者：当前协调 Agent；任务 owner 另记。

这是当前待办的唯一索引，不是编辑规则、自动调度器或发布授权。规则见 [EDITORIAL-STANDARD](EDITORIAL-STANDARD.md)，执行见 [WORKFLOW](WORKFLOW.md)，认领规则见 [根目录 AGENTS.md](../../AGENTS.md)。旧批次中的 status/progress/README 只是当时快照；冲突时核对 Git、实际批准及发布报告，不能按文件名猜测。

## 接手先核对

- 本机正式目录 `/Users/gang/Projects/Project/EpochArc-site` 的 `main` **已与远端 `origin/main` 完全同步**（父提交 `925d2322da6d077cab0bae112e8eacd231621cd1` 为 EA-005 13 条增量发布，最新提交合并 P0 前端止血修复与构建生成物去跟踪）；此前本机基于 `bf0b2ca4` 的全部未提交草稿已无损归档至本地分支 `archive/local-wip-20261127`，EA-009 实验门禁单独保存在分支 `exp/impact-audit-gate-20261124`。
- 构建派生文件（`data/events.json`、`data/events_summary.json`、`data/arcs.json`、`arcs/`、`arcs.html`、`rss.xml`、`sitemap.xml`、`_redirects`、`functions/event-routes.generated.js`）及 `index.html` 内联大体积冗余 JSON 已移出 Git 跟踪，统一由 `npm run build`（及 Cloudflare Pages 构建阶段）动态生成，运行构建不再污染 `git status`。
- 2026-11-20 的 20 条及 2026-11-27 的 EA-005 13 条均已获精确批准、推送并核实上线；AMD 收购完成未发布。不要重复执行历史发布脚本。
- 2026-11-19 美联航单项已经发布，提交 `bc06942fc3c0d52e04720540ef10072d98e97060`。
- 到其他机器或新会话后先核对实际 HEAD、UTC、工作树和权限。不得把 2026-11-20 当作“全部渠道已扫描至该日”：该次主要处理既有草稿，定向搜索有覆盖局限。

### 证据位置与可移植性

正式仓库内可直接追溯：

- 20 条发布提交：`bf0b2ca47d67df44d13bf645e32913fb49bb95b2`。
- 单次真实批准：[one-pass20-exact-approval-context.json](../../governance/evidence/2026-11-20/human/one-pass20-exact-approval-context.json)；每条批准见 `governance/approvals/`。
- 生产 run：[remaining19](../../governance/runs/targeted-remaining19-20261120.json)、[Meta/LVMH](../../governance/runs/targeted-next-two-20261120-r3.json)；它们是历史审计记录，不是可认领工作。

完整未发布材料和模型输入/原始输出在仓库外，本机路径如下；**克隆正式仓库不会自动获得它们**：

```text
工作区根 W = /Users/gang/pi-cwd-20260526/epocharc-workspace
批次根 B = W/active/2026-11-09-to-2026-11-17-restart
发布准备 P = B/publication-prep
统一发布包 U = P/one-pass-remaining-20261120/published-candidate
```

上面 W/B/P/U 是本文缩写，不是已设置的环境变量。已上线核验报告：`U/release_report_20261120_ALL21.json`、`U/public-live-verification.json`。统一批准请求文件 SHA-256：`424fd11b0305a54182555086f47adc66d57d420992965d869f11db686f92c7cd`。

外部目录不可用时，把依赖该材料的任务标记 blocked 并请求交接包；不能补造来源、模型结果或批准，也不能仅凭历史日志重跑带绝对路径的写入/发布脚本。

## 当前任务卡

状态与认领字段定义见文末。优先顺序不是执行授权。

### EA-007：20 条零分问题排查与修复（当前优先）

- status：`in_progress`
- 最新授权：2026-11-26 用户要求先排查并修复近期零分问题，再分析完善流程；不再先做政策迁移工程。不含提交、推送或部署
- 本轮 owner / claimedAtUTC：pi-session:019f7eb3-bd32-7de0-b812-96efddac7723 / 2026-11-26T12:04:07Z
- 本轮产物：外部 workspace 下 `score-repair-20261126-r2/RESULTS_20.md`、`RESULTS_20.json`、`proposal-final.json`。初次 `score-repair-20261126/` 因误把 severity +1 当作指数 1 的断言失败而未完成，保留失败现场；按原公式实际为 2，r2 已修正
- 2026-11-26 结果：确认批量预填空影响和统一 impact:not_found 有执行漏洞；Carbon、Decisions API 准备限定访问影响修正 0→2（severity +1、B、developers、immediate），L1 不变。7 条缺证据、6 条需身份/日期处理、5 条存档未支持可计分后果，不把剩余 18 条认证为零。两条本轮直接复读，其他 18 条沿用前轮全文审计，不是新的全网核查
- 两条最终精确包：DeepSeek 独立会话 `01a217d4-a7f0-72d3-82a6-426c5939072a`、`deepseek/deepseek-flash`、stopReason=stop，均 ACCEPT_LIMITED；也限定接受流程只读提示。大包前次调用超时无最终消息，不计通过；重试原 JSON 少一处括号，原文保留、派生解析只修格式并留痕。最终输入 SHA `67aab335597b3eeb95367e60020db9bcffad3fe4a976b65749a021f4919946ea`
- 已做流程补漏：新增 `scripts/report_impact_batch.py` 和 7 项测试，更新手工影响检查清单；撤下未批准强制审计门禁并标注实验草案。现行 policy、规则正文、基线、源评分、历史 run 和批准均不变；正式内容校验 0 错误/6 旧警告，编辑测试 92 通过
- 已发布（覆盖此前提案未批准状态）：用户实际回复 `f3e81f2f`「上线吧」批准两条 0→2 和流程补漏；真实审批上下文在 `governance/evidence/2026-11-26/human/two-score-repair-approval.json`。干净发布工作树中完整构建通过、71 项生产编辑测试/8 项 SEO 测试通过；22 路径白名单提交并推送 `aee3fd5f3b907a153b9edc9494683b630a3e01f0`。2026-11-26T14:30:42Z 公网 238 条完整数据及摘要与构建版精确一致，两条的四个双语页均显示 2/10、L1，其余 236 条未改；sitemap 504 路由核实。未发布旧 UI-only 包、政策迁移或其余 18 条的猜分
- 发布报告：外部 workspace 下 `score-release-20261126/release-report.json`、`production-verification.json`。首次公网仍旧分，后续 curl TLS 连接失败；正常 HTTPS 浏览器验证随后通过，未关闭 TLS 校验。原未提交草稿保留，正式目录尚未快进到已上线提交。下一步只处理 7 条补证和 6 条身份/日期缺口，5 条暂无可计分后果；两条已上线不再重复发布
- owner / claimedAtUTC：此前执行影响审计的会话 / 2026-11-24（具体执行和模型会话见外部调用记录；不冒填更精确的认领时间）
- baseCommit：`bf0b2ca47d67df44d13bf645e32913fb49bb95b2`；用户既有未提交 Agent 文档需保留
- workspace：`/Users/gang/pi-cwd-20260526/epocharc-workspace/active/2026-11-24-impact-process-audit/`
- 已完成：执行层修复候选及隔离构建；20 条影响初审；16 条再裁决并经 DeepSeek V4.1 Flash 独立跨模型复核。2026-11-25 有限定向补证：4 项可准备草稿、6 身份待处理、5 缺证据、1 暂无支持改分；不是精确生产版批准
- 前轮历史 nextAction（已由本轮两条修分提案推进）：Apple、Wallet HOLD；Carbon、Decisions API 曾因是否需外部接收者而有分歧。本轮按现行 EVID/IMP 和完整原文进行有限判断，形成两条非生产版本；不因模型多数票改政策。6 项身份仍需完整去重，不凭词面检索断言无重复
- 阻断：未重新采集完整当前日期窗；DeepSeek 与另一独立模型对两项可用性影响的证据解释未一致，不能把外部用户实际使用强加成政策一律要求；语义、因果及审计执行仍需核实。新审核门禁及展示修复尚未提交/部署
- 产物：`IMPACT_AUDIT_REPORT_20.md`、`IMPACT_ADJUDICATION_16.md`、`FOLLOWUP_CROSS_MODEL_20261125.md`、`identity-dedup-20261125.json`、`deepseek41-review/summary.json`、`score-path-four-deepseek-r2/review.json`；路径均相对上述 workspace。旧 Gemini 调用 provider 不存在，失败已留痕，不计通过
- permission：当前 20 条公开内容及分数未修改；任何内容变更仍需独立复核和针对最终精确版本的人工批准。工程改动与内容修订不得借旧批准自动发布
- acceptance：分别记录代码评审/工程发布，以及内容修订的逐项证据、复核、批准与部署；不因本次报告宣称 20 条全为零或全应加分

### EA-001：接手基线检查

- status：`ready`
- owner：未认领
- claimedAtUTC：未认领
- baseCommit：认领时填写实际 HEAD，不预填历史值
- workspace：当前仓库；不得在只读检查中修改源数据
- scope：本地只读检查工作树、内容基线、已发布 20 条与 AMD 缺席情况；确认后续任务材料是否可用
- permission：默认仅本地只读；写认领记录需用户已授权执行/认领任务。联网、模型调用、build、源数据修改、commit/push 均不包含
- nextAction：读取根目录 AGENTS.md；比较实际 HEAD 与本清单，向用户报告可接手项；若用户未分派任务，不继续内容生产
- acceptance：报告实际 UTC/HEAD/工作树、材料缺失与权限边界；不能把本地核对称作重新确认线上状态
- artifacts：在接手回复或获授权的交接记录中留痕；无须新建生产 run

### EA-002：AMD 新交割与旧公告联动

- status：`needs_scope`
- owner / claimedAtUTC：未认领 / 未认领
- baseCommit / workspace：执行前核对 / 待确认后设独立隔离目录
- scope：拟同时复核 `amd-world-labs-close-2026` 新稿和 `amd-world-labs-acquisition-2026` 旧条目的时态修正；本轮尚未授权
- permission：不能沿用 20 条发布批准；旧条目修改必须重新复核并获精确批准
- blocker：旧公开文本用现在时写交易尚未完成；新交割稿若单独发布会冲突。此前用户明确 AMD 暂缓
- nextAction：询问是否允许“新旧两条联动修订”；未同意前保持两者原状
- artifacts：`P/amd-dependency-audit-20261119.json`；`P/one-pass-remaining-20261120/drafts/r2/amd-world-labs-close-2026.json`
- acceptance：获准后核对全部旧主张/影响/依赖，保留旧 id/slug/date/publishedAt；准备联动精确提案，独立复核后统一申请批准；未批准不得发布

### EA-003：Cursor 既有事件纠错

- status：`needs_scope`
- owner / claimedAtUTC：未认领 / 未认领
- baseCommit / workspace：执行前核对 / 待确认
- scope：拟核对 `cursor-claude-code-extension-compromise-2026` 的凭据范围表述与后续公司披露，不自动调整旧评级/影响
- blocker：已有草案/限定审查不等于完整变更后生产复核；不在此前 20 条批准范围
- nextAction：先确认允许处理旧公开事件；获准后重读原始证据与新披露，检查引用依赖
- artifacts：`B/improvement/bundle/published_dependency_audit_20261119.json`；`P/drafts/update_proposals/cursor-claude-code-extension-compromise-2026.json`
- acceptance：按 endpoint 风险与历史训练轨迹 API 凭据暴露区分主张，完整双语/v2.4 复核并就精确新版本申请批准

### EA-004：OpenAI 学术研究者旧事件证据缺口

- status：`blocked`
- owner / claimedAtUTC：未认领 / 未认领
- baseCommit / workspace：执行前核对 / 待确认
- scope：历史节点 `openai-academic-researchers-2026` 的旧主张及影响依赖复核；新扩容计划不能反证旧实际采用
- blocker：2026-11-19 历史一手原文读取返回 403；转载不构成独立采用证据。本次未重新请求，不能断言目前仍为 403
- nextAction：先确认旧事件复核范围及可用合法来源；不绕过访问限制，不静默降低已有影响分
- artifacts：`B/improvement/bundle/published_dependency_audit_20261119.json` 中 academicResearchers
- acceptance：找到足以核对旧主张/影响的证据或明确保留缺口；旧公开修改另获复核和批准

### EA-005：增量发现与未覆盖日期窗（2026-11-17 至 2026-11-26 UTC）

- status：`done`
- owner / claimedAtUTC：antigravity-eb6ae22d / 2026-11-26T15:07:00Z
- baseCommit / workspace：发现基线 `bf0b2ca47d67df44d13bf645e32913fb49bb95b2`，发布父提交 `aee3fd5f3b907a153b9edc9494683b630a3e01f0` / `/Users/gang/pi-cwd-20260526/epocharc-workspace/active/2026-11-17-to-2026-11-26-discover/`
- scope：2026-11-17 至 2026-11-26 UTC 全部 14 条 `confirm` 候选（Anthropic IPO 11/18 定价、11/19 挂牌与 11/20 交割合并为 1 条，共 **13 条事件**，2 条 L2 + 11 条 L1，新增 38 条 `ea005-*` 来源）
- 复核与精确批准：
  - 独立只读子会话 `0b5e4807-71c6-4d64-a6a7-325fbe77af19`（`independent_model`，同模型家族非跨模型实验）：第一轮 `REVISE_REQUIRED`（7 项阻断全部修复）→ 第二轮 `ACCEPT_LIMITED` → 发布态 `reviewed -> published` 零正文改动核验延续 `ACCEPT_LIMITED`；
  - 人工批准：用户于 `2026-11-27T07:23:25Z`（“继续”）与 `2026-11-27T07:23:43Z`（“批准”）明确同意精确审批请求清单 `EA005_EXACT_APPROVAL_REQUEST_13.json`（SHA-256 `b266b7be70312e642bcd27a3bd811fc8e99c8dcbfffe9f58180b0b85d41b6b06`）并授权发布；审批上下文记录在 `governance/evidence/2026-11-27/human/ea005-13-exact-approval-context.json`（SHA-256 `e910bfa66c300a80cabe7e25808a06a238772583ea1b7e7707ef55c242f5e804`），13 份 `governance/approvals/<subjectDigest>.json` 已随提交入库。
- 已发布并公网核验（勿重复发布）：
  - 在干净发布工作树 `release-20261127/site/` 基于 `origin/main`（`aee3fd5f`）白名单合入，未触动本机正式目录未提交草稿；
  - 校验与构建：`test:editorial` 71/71、`validate_all.py` 0 errors（251 事件、732 来源、4 方向、6 主线）、`report_impact_batch.py` `flags: []`、`npm run build`（265 EN + 265 `/zh-hans/` 页、530 sitemap URL）、`test:seo` 8/8 全部通过；
  - 推送提交：**`925d2322da6d077cab0bae112e8eacd231621cd1`**（`2026-11-27T07:29:46Z` 推送至 `origin/main`）；
  - 公网核验（`2026-11-27T07:32:34Z`，严格 HTTPS TLS）：`https://epoch-arc.com/data/events.json`（251 条，SHA-256 精确一致）、`events_summary.json`（251 条，SHA-256 精确一致）、`sitemap.xml`（530 条路由含全部 26 个新增双语 URL）、`rss.xml`（251 条，SHA-256 精确一致）、全部 26 个新增双语事件页（26/26 HTTP 200 且标题与 canonical 精确匹配）、`/governance/policy.json` 返回 404（未暴露治理材料）。
- blocker：无
- nextAction：无（本批次已结案；勿重复发布；下一次增量发现请从 `2026-11-26` 后半日起算）
- artifacts：`release-20261127/release-report.json`、`release-20261127/production-verification.json`、`EA005_BATCH_SUMMARY.md`、`EA005_EXACT_APPROVAL_REQUEST_13.json`、`DISCOVERY_SCREEN_REPORT.md`、`impact-triage/IMPACT_TRIAGE_13.json`（均位于上述隔离工作区）；生产记录见远端提交 `925d2322` 下 `governance/runs/latest-data-full-2026-11-26.json`、`governance/reviews/ea005-20261126/`、`governance/approvals/` 与 `governance/evidence/2026-11-26/`、`2026-11-27/`
- acceptance：已分别记录准备完成、白名单推送与公网全量核验，满足结案条件

### EA-006：旧批次暂缓与窗口外候选

- status：`needs_scope`
- owner / claimedAtUTC：未认领 / 未认领
- baseCommit / workspace：执行前核对 / 待确认
- scope：Inkling 2 Small 的下载/公告日期证据，儿童安全工具、医疗代理、纽约安全中心等核心来源缺口，以及窗口外历史补录提案
- blocker：这些不是已发布 20 条的遗漏发布项；不能凭模型限定接受追认生产合格，补录也不等于获准扩大窗口
- nextAction：请用户选择补证或 backfill 范围；对照现有公开数据去重，检查时间与来源变化后再核实
- artifacts：`P/publication_readiness_report.json`、`P/supported-subset-20261119-r3/status.json`（历史快照）；`B/improvement/bundle/proposed_backfill_queue.json`
- acceptance：逐项接受/暂缓/排除及原因明确，不替历史缺口填造来源；合格项依旧走完整复核与精确批准

### EA-008：前端 P0 止血修复、空影响展示与工作树/生成物收敛

- status：`done`
- owner / claimedAtUTC：antigravity-eb6ae22d / 2026-11-27T15:24:00Z
- baseCommit / workspace：`925d2322da6d077cab0bae112e8eacd231621cd1` / `/Users/gang/Projects/Project/EpochArc-site`
- 已完成（2026-11-27 用户明确授权“1、2修复吧”，不含任何公开事件内容、评分、政策或基线改动）：
  - **工作树脑裂清理**：将本机原 `bf0b2ca4` 上的未提交改动完整归档至本地分支 `archive/local-wip-20261127`，将 EA-009 实验门禁隔离至 `exp/impact-audit-gate-20261124`，`main` 快进对齐 `origin/main`；
  - **构建派生文件去跟踪与 HTML 瘦身**：`data/events.json`、`data/events_summary.json`、`data/arcs.json`、`arcs/`、`arcs.html`、`rss.xml`、`sitemap.xml`、`_redirects`、`functions/event-routes.generated.js` 移出 Git 跟踪并加入 `.gitignore`，移除 `index.html` 内联 650+ KB 重复 fallback JSON（`dist/index.html` 由 688 KB 降至 16 KB）；
  - **前端与边缘接口止血修复**：`events_summary.json` 补齐 `consensusLevel`、`impactCount`、`impactDimensions`、`controversy`、`tags`，修复首页“影响维度”筛选 JS 崩溃与“共识度”筛选恒为 0 Bug；空影响事件统一展示为“尚无已记录影响 / No impacts recorded”（不再显示 `0/10`）；更新首页 6 分类 Tooltip 与完整 `SOURCE_TYPE_LABELS`；来源 URL/脚本内嵌转义加固；`init()` 解除 `/api/reader-pulse` 首屏阻塞，且 `GET /api/reader-pulse` 不再向未投票访客下发 Cookie、`POST` 增加 `FORECAST_IDS` 白名单与 UUID 校验；
  - **校验通过**：模拟全新克隆全量构建通过，`test:editorial` 75/75、`test:impact-ui` 6/6、`test:seo` 10/10、`validate_all.py` 0 errors（251 事件、732 来源、4 方向、6 主线），构建后 `git status` 零脏文件。
- nextAction：无（已结案上线）

### EA-009：影响审计门禁的政策迁移（暂停，不是当前修分前置条件）

- status：`blocked`
- 2026-11-26 范围收敛：按用户要求暂停版本化政策原型扩展，优先 EA-007。旧 HOLD 保留；不得把完成迁移作为排查评分问题的前置要求
- owner / claimedAtUTC：当前影响专项审计会话 / 2026-11-25；未记录更精确认领时刻
- baseCommit：`bf0b2ca47d67df44d13bf645e32913fb49bb95b2`
- workspace：`/Users/gang/pi-cwd-20260526/epocharc-workspace/active/2026-11-24-impact-process-audit/`
- 已完成：DeepSeek V4.1 Flash 对现有门禁给出 HOLD；隔离模拟显示仅改 policy revision 就有 166 条错误，涉及 81 个事件及 2 个 Arc 的复核与批准。已生成 83 项原有摘要绑定清单，并通过机械一致性核查；这不验证人类身份或事实
- 阻断：现有草案对 L1 独立复核、批准摘要、额外历史兼容名单新增强制要求，与当前 v2.4 权威规则和契约的关系尚未经负责人决定。现有代码没有多政策历史解析器；不能把审计快照冒充已有 GOV-03 基线
- 用户已同意按 A→B **准备**：先冻结 v2.4 并将审计作为非阻断诊断，再设计版本化迁移；尚未批准具体政策条款、历史适用清单或任何上线。隔离副本中的 v2.4 主校验通过（6 条既有警告）、64 项政策测试与 17 项审计单测通过；5 项路由实验测试覆盖 83 条旧复核和部分篡改。诊断将 238 条列为 UNASSESSED，不代表零影响或事实审计结论
- 路由实验仅用同一工作树生成内存状态，不能验证状态本身的真实性；当前政策摘要是假数据，无版本化政策快照或完整生产集成。独立 DeepSeek 对原型给出 HOLD，指出认证清单/防降级、旧批准真实性、依赖覆盖、影子报告重复 ID 与旧 review 校验等风险；模型只看冻结输入，并未自行重跑测试
- nextAction：处理独立审查发现，先构造可信不可变状态及恶意变造测试，再验证完整版本路由、旧 run、165 条既有基线例外和证据文件；明确先于披露但持续的影响、受阻来源及审批确认机制。形成政策提案和上线范围并重新独立复核后，再请求精确批准
- 产物：`policy-migration-simulation/report.json`、`policy-migration-design/review.json`、`policy-migration-design/affected-binding-inventory.json`、`policy-migration-prototype/site/`、`policy-migration-prototype/independent-review/review.json`；清单 SHA-256 `5da9a6b209e46e292a8ef8fca201e6a57ebfe4ed91029f08f74a420d8bb89fea`
- permission：以上均为隔离诊断，非政策或例外批准；不得重建 `governance/legacy-baseline.json`、改写历史 run 或伪造批准。UI 单项包见 EA-008，不含该强制门禁

## 已完成事项（勿重复发布）

| 项目 | 状态 | 验收定位 |
|---|---|---|
| 美联航单项 | done | 提交 `bc06942fc3c0d52e04720540ef10072d98e97060`；`P/solo-united-20261119-r3/published-candidate/release_report_20261119_united.json` |
| 统一 20 条，AMD 暂缓 | done | 提交 `bf0b2ca47d67df44d13bf645e32913fb49bb95b2`；`U/release_report_20261120_ALL21.json` 记载 20 条公开数据及 40 双语路由核验 |
| EA-005 增量 13 条（2026-11-17..26） | done | 提交 `925d2322da6d077cab0bae112e8eacd231621cd1`；`W/active/2026-11-17-to-2026-11-26-discover/release-20261127/release-report.json` 与 `production-verification.json` 记载 251 条公开数据与 26 新增双语页核验 |
| EA-008 前端 P0 止血与工作树/生成物收敛 | done | 本机 `main` 已对齐远端并完成生成物去跟踪、首页筛选修复、空影响展示、HTML 瘦身与公网核验 |

这些是已有发布记录，不是本次重新请求公开站点的结果；之后若怀疑漂移，另做明确的线上核验。

## 更新约定

状态只使用：`ready`、`needs_scope`、`blocked`、`in_progress`、`awaiting_review`、`awaiting_approval`、`done`。这是任务状态，不是事件的 draft/reviewed/published，也不是 run 的 skip/hold/new。

- 获得任务授权后按 AGENTS.md 认领；补实际 `owner/claimedAtUTC/baseCommit/workspace`，禁止臆造会话或日期。
- 未获范围/权限确认的卡保持 needs_scope；受阻卡写清阻断和解锁条件，不能为了显示进度改为 ready。
- 每次停止/交接时同步 status、nextAction、产物与实际验证结果。补充的批准只对其精确对象有效。
- 完成阶段性工作但未发布，用 awaiting_review/awaiting_approval，而不是 done。若任务仅为只读诊断，交付诊断即可 done，不要求发布。
- 并行由协调者串行维护本清单；没有原子锁/自动抢占机制。正在进行的任务不可无确认接管。
- 新提交后记录实际提交；公开上线需要独立核验。旧报告留作历史，不改写原始审批/模型记录；入口状态应明确指向后来有效的完成记录。
