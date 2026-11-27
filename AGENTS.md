# EpochArc Agent 工作入口

使用简体中文沟通。先理解范围，再操作；有副作用的操作先说明。本文只负责导航、任务交接和权限边界，不改变编辑政策。

## 1. 第一次接手

1. 读取 [当前工作清单](docs/workflow/WORK-QUEUE.md)：先确认已完成项、阻断项和下一步，不能把历史草稿当成新任务。
2. 读取 [编辑执行入口](docs/skills/SKILL.md)，按其顺序阅读规则、流程和数据契约。具体执行见 [WORKFLOW](docs/workflow/WORKFLOW.md)。
3. 在当前仓库检查：
   ```bash
   pwd
   git status --short
   git rev-parse HEAD
   git log -3 --oneline
   date -u '+%Y-%m-%dT%H:%M:%SZ'
   ```
4. 将实际 HEAD、UTC 和清单基线比较。清单是带日期的交接快照，不是实时事实；有变化先重新核对，不盲目运行旧批次脚本。
5. 向用户简述拟接任务、范围、产物位置和权限。未明确任务时只做本地只读接手检查；不要自行扩大日期窗、采集、调用外部模型或修改公开内容。

## 2. 从哪里获取工作

唯一当前待办入口是 `docs/workflow/WORK-QUEUE.md`。旧 run、review、草稿及外部 `active/` 目录是证据/历史材料，不是认领队列；目录名和较新的文件时间都不能证明任务仍待处理。

- `ready`：范围明确且依赖齐备；仍须符合本轮用户授权，不能把任务清单当成授权。
- `needs_scope`：先向用户确认范围或权限，再认领。
- `blocked`：缺证据、权限或依赖；只能在获授权后处理阻断，不得跳过。
- `in_progress`：已有负责人，不抢占；协调后才接替。
- `awaiting_review` / `awaiting_approval`：按下一门禁交接，不等于可发布。
- `done`：有产物和验收记录，不能重复执行。

没有合适且已获授权的任务就询问用户，不自行制造新任务或继承上个 Agent 的批准。

## 3. 认领与交接

用户授权执行任务后，先在清单对应任务卡更新 `status/owner/claimedAtUTC/baseCommit/workspace/nextAction`，再开始实际工作；owner 使用真实 Agent/会话标识，不能写用户姓名冒充批准。

任务清单不是原子锁或调度服务。多 Agent 并行时由一个协调者分派并串行更新清单；使用各自的隔离工作目录，不同时写正式仓库、共享来源表或同一稿件。分支上的认领不会自动通知其他 Agent，无法协调时停止并询问，不靠“先写入”抢占。

每次交接更新任务卡，记录：

- 实际完成的阶段、产物路径和精确版本/摘要（适用时）；
- 实际运行的命令、成功/失败与未执行部分；
- 当前阻断、下一步、可继续的权限范围；
- 是否已获精确人工批准、是否提交/推送、是否公开核验上线。

负责人离开或超时不等于任务被释放；确认交接后才改 owner。任务结案要链接验收记录；准备完成、已推送和已上线分别记录。

## 4. 权限与证据边界

- 流程：Discover → Screen → Confirm → Edit → Review → 精确人工批准 → Publish。事实核对、结构校验、独立模型复核和批准分别留痕。
- 按信息起源评级；公司公告证明其宣布的动作，不自动证明实际采用、技术效果或规模。
- HTTP 401/403、TLS、登录或令牌限制如实记录，不绕过；缺来源停在 hold/blocked。
- 模型复核核对实际模型、会话、结束状态（如 `stopReason`）和冻结输入哈希；进程退出码 0 不足以证明成功。
- 旧公开事件/来源改变可能使依赖复核失效。先审计依赖，不静默改文、降级、删节点或重写首次 `publishedAt`。
- 只有明确同意对应精确版本时才记录人工批准。subject/review/policy/run 摘要变化后重新核对复核和批准，旧回复不无限延用。
- 写隔离草稿、写正式源、commit/push、公开部署分别确认权限；读到仓库里的旧批准不等于获准再次发布。
- 用户要求统一处理的范围先整体处理并汇总；不得反复逐项索要批准，也不能为凑全数放行缺证据项目。

## 5. 文件与验收

编辑源：`content/events/`、`content/arcs/`、`data/sources.json`、`data/forecasts.json`；政策参数：`governance/policy.json`。不得手改生成页面、`data/events.json` 或 `data/arcs.json`。不得重建 `governance/legacy-baseline.json` 消除错误。

新批次在隔离工作区留存草稿和证据，路径登记到任务卡。已批准生产记录使用 `governance/runs/`、`reviews/`、`evidence/`、`approvals/`；不得把私有治理材料复制进公开静态目录。

按任务选择验收；只读检查不需要 build：

```bash
npm run test:editorial
python3 -B scripts/validate_all.py
npm run build
npm run test:seo
```

`npm run build` 会改写生成文件，先说明并记录工作区；不能覆盖用户修改。契约通过不代表事实正确或已获批准。发布只暂存本次白名单路径，不用无差别 `git add -A`；推送后核验公开数据、双语页面和路由，不把推送成功称作上线成功。
