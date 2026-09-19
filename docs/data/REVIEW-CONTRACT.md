# v2.4 编辑证据与审批契约

规则语义见 [EDITORIAL-STANDARD](../workflow/EDITORIAL-STANDARD.md)。公开数据结构沿用 DATA-MODEL；新增审计材料放在 `governance/`，不复制到公开 data 目录。不为旧数据补造审核。

## 文件组织

| 路径 | 用途 |
|---|---|
| governance/policy.json | 版本化参数，不是公开方向的实现标准 |
| governance/legacy-baseline.json | 一次性历史内容指纹；禁止重新生成以绕过门禁 |
| governance/runs/*.json | 新批次，包含发现/筛选及方向决定 |
| governance/evidence/* | 实际采集的文本/响应摘录，可分子目录 |
| governance/reviews/*.json | 针对精确编辑版本的复核记录 |
| governance/approvals/*.json | 真实人工批准的引用，不由构建生成 |
| governance/calibration/ | 非发布用冻结案例与测试变体 |
| governance/audits/ | 历史债务和结构审计，不是事实审核证书 |

JSON 对象摘要：UTF-8、ensure_ascii=False、sort_keys=True、separators=(',', ':') 后 SHA-256。文件摘要是原始字节 SHA-256。使用 `scripts/editorial_policy.digest`，不得拿 Git blob SHA 替代。

## Run

必填：`policyVersion`（字符串 2.4）、`runId`、`kind`（full/targeted/backfill）、`windowStart`、`windowEnd`、`evidenceCutoff`（均 YYYY-MM-DD）、`timezone`（UTC）、`baselineCommit`（40 位 SHA）、`operator`、`model`、`promptVersion`、`channels`、`categoryCoverage`、`candidates`。

- 非 full 要 `scopeReason`；full 要全部核心通道和六类覆盖。
- channel：`id/status/coverageNote/attempts`；非 complete 要 reason；partial/unavailable 要 retryResult；complete 要 windowCovered=true，且实际覆盖须由评审检查。
- attempt：`query/executedAt/artifact/sha256/resultCount`。时间为带时区 ISO 时间戳；文件限 governance/evidence 下。
- categoryCoverage：每项 `category/status/finding`。
- candidate：`candidateId/discoveryUrls/scores/scoreReasons/total/priority/decision/reason`。五个评分字段和五个理由字段必须完全匹配 policy。
- priority=skip/pool/confirm；decision=skip/hold/new/update/merge。最后三个要求 eventId 和 confirmation；优先级不足时补 priorityOverrideReason。
- confirmation：恰好 fact/impact/analysis/controversy，各含 `status/query/finding/evidenceIds`。found 不得为空；not_found/blocked 可空。
- directionDecisions（方向更新时）：每项 `id/decision/reason`，公开对象必须恰有一个 publish 决定。

## Source / 公开 editorial

新建或修改 Source 增加 `publisherId/originId/accessedAt`。originId 是主要信息起源，不能把转载 URL 自身当作独立起源。

v2.4 已审核/发布对象的 editorial 必填：

- `createdAt/updatedAt/reviewedAt/lastSourceCheckAt`（实际行为日期）。
- `curator/reviewer`（真实操作者，可是明确的 AI 会话标识，不等于人类批准）。
- `reviewProvenance: v2.4`、`reviewRecord`（governance/reviews 下的相对路径）。
- `changeLog` 非空：date/changeType/summary。
- 公开内容 `publishedAt` 保持首次记录日期。方向还需 `screeningRunId`。

新建 candidate/draft 只需基础数据结构，不要求编造复核/批准；reviewed 开始强制本契约。已有公开记录改变或归档不能退回 draft 来逃避审核。

## Review 公共字段

`policyVersion/policyDigest/kind/subjectId/subjectDigest/inputsDigest/evidenceCutoff/preparedBy/model/reviewedBy/reviewMethod/limitations/languageReview/evidence`。

policyDigest 绑定当前 policy 全对象；policy.rulesDigest 绑定规则总表的原始文件字节。因此规则正文改变也会使审核与批准失效，不能只沿用版本号。

- kind=event/arc/direction。
- inputsDigest=`review_inputs(kind, record, sources, events)`：绑定公开来源及 Arc/方向的锚点事件；依赖变更后旧复核失效。
- reviewMethod=independent_model/human/self_review。L2/L3 不允许仅 self_review。
- independent_model 还需不同的 producerSessionId/reviewerSessionId 和 reviewerModel。不同 actor 字符串不等于已真正独立，必须保存实际会话凭据供人工追溯。
- limitations 为非空字符串数组，哪怕只是明确“离线校验不能确认语义”。
- languageReview：factsAligned=true、notes，表示完成了实际的双语事实核对，不是机器自动测得。

### evidence 每项

`id/sourceId/claimId/url/originId/accessedAt/relationship/verification/quote/locator/artifact/sha256`。

- quote 是逐字文本，必须出现在留存文本中；截图/PDF 先形成可定位的文本摘录，并保存页码/章节定位。
- relationship=primary/independent/interested/unknown；verification=direct/independent_verification/reported/context。
- 每个事件 claim 都有证据，摘录 sourceIds 必须与 claim.sourceIds 相等；所有评审来源都应在公开 sources 引用中。
- 同一来源对不同 claim 的独立关系、验证对象可能不同，要分别记录。
- 访问和来源发布日期不晚于 evidenceCutoff。不能事后看了新材料却声称使用旧截止日。
- Arc 的 claimId 为稳定的章节/论点标识；来源可来自自身 sources 或锚点公开事件。方向的 signal 使用对应 signal.id 为 claimId，并匹配 sourceIds；基线/限制另设稳定标识。机器不验证这些文本的语义。

## Event 专属字段

- `runId/candidateId/runDigest`：匹配一个 selected candidate；截止日一致。
- `coreFactClaimIds`：明确节点身份所依赖的核心事实 claim；非空，均为 fact 且证据等级至少 B，不能用一个无关事实掩盖主事实不足。
- identity：`seriesId/action/stage/dateBasis/deduplicationReason/comparedEventIds/decision`。decision 与候选一致。
- classification：`primary/reason`；有次分类时 `secondaryClaimId` 指向确实不同的主张。
- significance：`rationale/whyNotHigher/whyNotLower/comparisonEventIds/routes`；至少两个其他已发布对照事件。
- route：`ruleId/criteria`。criteria 键集合与 policy 完全相同。
- criterion finding：`value/rationale/evidenceIds`。未知 value=null，可无证据；已知值需证据。布尔/计数不能混用。
- 组织/群体/后续工作计数：`entityIds` 数量必须等于 value；ID 指无关联控制主体/研究团队，而非同机构不同项目。人工验证独立性。
- observed_days：`observedSince/observedUntil`，由日期差复算。
- verified_active_users：`metric` 为 DAU/WAU/MAU、`measuredAt`；引用材料还须解释测量或估算方法。
- L3 significance 增加 `observedSince/observedUntil`，实证持续期达到配置，独立验证数量达标。
- L2 无一手资料时 `primaryUnavailableReason`；不能免除核心事实 B 级和路径验证。
- impactBasis 与 impacts **逐项同序**，各含 `dimension/observation/evidenceIds/observedSince/observedUntil/baseline/outcome/materialChange`；observation 只允许 observed。没有观察影响的 L1 两数组均空、impactIndex=0。
- consensus：`level/reason/evidenceIds`；broad 至少两组独立支持主要影响。
- dispute：`exists/reason/evidenceIds`；争议为真时有证据及 limitation claim。

## Arc / Direction 专属字段

两者都需要 `changeReason/counterEvidence/eventIds`；eventIds 恰好覆盖全部公开锚点。

方向另有 `screeningDecision: publish/consensusSearch/independentSourceIds/runId/runDigest`，关联 run.directionDecisions 及 editorial.screeningRunId。独立来源要有摘录支持且起源和控制主体均达到门槛。其余信号/共识/生命周期约束沿用正式 schema。

## Approval

路径：`governance/approvals/{subjectDigest}.json`。

必填：`subjectId/subjectDigest/reviewDigest/policyDigest/decision/actorType/actor/approvedAt/confirmationRef`。

- decision=approve，actorType=human；日期不早于 reviewedAt。
- reviewDigest 绑定 review 全对象，policyDigest 绑定 policy 全对象。审核内容或规则改变，旧批准不再生效。
- confirmationRef 指向实际确认消息或工单；程序不认证其真实性，项目负责人必须核对。
- 文件内不能写秘钥、会话 token 或不必要的个人信息。
- 归档已发布事件同样需要批准。旧基线未变的记录不要求追造历史批准。

## 可执行样例

完整合格与不合格样例由 `tests/test_editorial_policy.py` 在临时目录创建，均为明确的合成测试材料，不作为真实审核或批准入库。运行 `npm run test:editorial` 检查契约。禁止把测试证据/测试人工身份复制成生产审核。
