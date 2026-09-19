# EpochArc 编辑执行流程 v2.4

规则权威：[EDITORIAL-STANDARD](EDITORIAL-STANDARD.md)。参数：[policy.json](../../governance/policy.json)。本文只描述执行方法，不另设评分标准。

## 1. 开始前

1. 确认范围：完整扫查 full、定向复核 targeted、历史回溯 backfill；明确是否允许写 canonical、是否允许发布。
2. 检查工作区，记录 Git 完整 SHA、UTC 日期窗、证据截止日、操作者、模型和提示词版本。
3. 新 run 写 `governance/runs/{runId}.json`。旧 `data/screening_log.json`、`data/possible_directions_screening_log.json` 是冻结的历史日志，不追加新格式。
4. `content/events`、`content/arcs`、`data/sources.json`、`data/forecasts.json` 是编辑源；不要手改生成页面或生成清单。

## 2. Discover：发现

full 必须记录全部核心通道及六类覆盖。状态以本轮结果为准，文档中不再写永久“可用/停刊”。

| 通道 ID | 采集入口 | 日期窗注意事项 |
|---|---|---|
| hf-papers | `https://huggingface.co/api/daily_papers?limit=20` | 仅为当前快照；回溯需按日/分页或辅助搜索，缺失指标写 unknown |
| hacker-news | Firebase topstories + item API | top 30 不代表整周；用有日期范围的历史检索补充并记录局限 |
| reddit-search | Brave 或平台可用后端 | 保存查询/日期过滤、URL 和结果；索引不等于完整平台覆盖 |
| x-search | 同上 | 不从标题推断互动量，不保证实时索引 |
| import-ai | `python3 scripts/check_mail.py import-ai --limit N --max-chars 0` | N 覆盖所需期数，确认正文未截断 |
| the-batch | `python3 scripts/check_mail.py the-batch --limit N --max-chars 0` | 同上 |

Gmail 使用 IMAP + macOS Keychain `epocharc-gmail-app-password`；先用 `python3 scripts/check_mail.py test` 检查连接。凭据不入库，失效如实记录。不得为了让通道“成功”改写返回结果。

对 capability/product/commerce/governance/safety/society 逐一检查，必要时定向搜索补漏。分类没有结果是允许的，不分配收录配额。通用搜索补充，而不是伪装已完成其他通道。

保存最小必要原始响应到 `governance/evidence/`，注明实际请求时间、查询、结果数、sha256。去除凭据和不必要个人信息；涉及受限内容，只保留合法可留存的摘录及存档定位。

## 3. Screen：去重和初筛

- 为实际评估过的候选分配唯一 candidateId；保存发现 URL、五维评分与逐维理由。
- 使用 SCREEN-02 得出核实优先级，不由初筛决定 L 等级。
- 检索相同主体/动作/阶段的旧事件，列入 identity.comparedEventIds。
- 记录最终工作决定 skip / hold / new / update / merge。pool 是优先级，不是事件状态；confirm 也不等于 reviewed。
- 提前处理低优先级候选须说明理由；保留 skip/hold，不能只存最终胜出者。

## 4. Confirm：四层事实搜索

| 层 | 要回答 | 允许结果 |
|---|---|---|
| fact | 谁在何时做了什么？处于什么阶段？ | found / not_found / blocked |
| impact | 哪些后果已经发生？ | 同上；未找到不等于“没有影响” |
| analysis | 有什么独立验证、分析及可比基线？ | 同上；报道不自动升 A |
| controversy | 有无反证、争议、复测失败或范围限制？ | 同上；未找到不能证明不存在 |

每层保存 query/finding/evidenceIds。found 必须有证据引用。每条摘录同时绑定公开 claim 与来源，材料缺失则停在 hold，不填假 accessedAt。不同 URL 先去重到 publisherId/originId，再判断独立性。

## 5. Edit：基于冻结证据形成判断

依次完成身份/日期 → 分类 → claim 证据链 → 相关 L2 路径 → L3 条件 → observed impacts → 共识/争议 → 双语。

- 用 `null + 缺什么证据` 表达未知，不能用 false 偷换成反证。
- 填最接近的至少两个已发布对照案例；比较证据结构，不抄旧分数。
- 已上线事件缺证据时，只提出复核缺口；未经复核和批准不降级。
- AI 可以提出等级、severity 和文案建议；人工负责最终接受。禁止把“AI 不做评分”作为省略评级依据的理由。
- review 结构和批准绑定见 [REVIEW-CONTRACT](../data/REVIEW-CONTRACT.md)。

## 6. Review：先复核再批准

L2/L3 需要独立模型会话或真实人工复核；同模型不同会话可以做独立复核，但不能叫跨模型实验。记录生产/评审 sessionId、实际模型、评审方法、限制和双语事实一致检查。

复核原文是否支持结论、来源是否真正独立、观察期是否实际测得、组织计数是否无关联。这些不是文件哈希能证明的。分歧先定位证据，再处理规则解释；无法解决的停在 reviewed 之前。

审批文件位于 `governance/approvals/{subjectDigest}.json`。只在收到明确确认后记录 actorType=human、确认消息引用及精确 subject/review/policy digest；代码不得自动生成批准。

## 7. 本地验收与发布

```bash
npm run test:editorial
python3 scripts/validate_all.py
npm run build
npm run test:seo
```

此外检查中英文页面渲染、来源链接、日期/等级展示和重要交互。结构通过不是事实审核通过，也不是视觉检查通过。

本地 build 会改写部分受跟踪的生成文件：先保存工作区清单，只恢复确由本轮构建产生且不打算提交的输出，不覆盖用户改动。

获得明确发布授权后，只暂存本次批准涉及的路径，核对 diff，再 commit/push。不要使用无差别 `git add -A`。部署后检查 HTTP 状态、canonical/语言链接、页面样式及预期数据。

## 8. Arc 与方向

- Arc 以公开事件为事实锚点，额外解释有证据/反例；按 [ARC-MODEL](../arcs/ARC-MODEL.md) 写作。
- 方向从事件和 observed signals 聚合；新 run 另存 directionDecisions，关联 screeningRunId，执行共识搜索。
- 改变引用事件或来源会使依赖复核失效；应明确检查受影响 Arc/方向，不复制旧审批。
- 定期/触发式复核记录新信息和保留意见；没有实际复核，不更新 reviewedAt/lastSourceCheckAt。

## 9. 不允许的捷径

没有发现渠道≠没有事件；初筛高分≠L2；厂商跑分≠独立复现；融资大≠结构变化；年头久≠持续观察；校验通过≠事实正确；负责人姓名≠负责人批准；新规则≠自动重评级历史数据。
