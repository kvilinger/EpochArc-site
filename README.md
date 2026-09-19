# EpochArc — AI Milestones, Evidence, and Possible Directions

EpochArc 是一个双语 AI 发展时间轴网站，记录 1950 年至今的 AI 里程碑、来源证据及可能方向。核心受众是普通大众和长期关注者，目标是把零散信息整理成一条能回溯、能筛选、能持续更新的路线记录。

**数据驱动，非断言。** 每一节点都附有来源证据、影响维度评分和编辑可追溯记录。

## 项目结构

```
EpochArc-site/
├── index.html              # 主时间轴前端
├── methods.html            # 方法论公开页
├── 404.html                # 错误页面
│
├── content/events/*.json   # 事件编辑源文件（按事件拆分）
├── content/arcs/*.json     # Arc 编辑源文件
├── data/                   # 构建输出（前端消费）
│   ├── events.json         # 合并后的事件数据
│   ├── sources.json        # 来源独立表
│   ├── labels.json         # 枚举标签中英对照
│   ├── forecasts.json      # Possible Directions 数据
│   ├── screening_log.json  # 候选事件筛选记录
│   └── possible_directions_screening_log.json  # 方向筛选运行记录
│
├── scripts/
│   ├── validate_all.py     # 全部公开内容的统一发布门禁
│   ├── build_events.py     # 合并事件并生成静态详情页
│   ├── build_arcs.py       # 生成 Arc 清单与详情页
│   ├── build_directions.py # 生成 Possible Directions 页面
│   ├── build_feed.py       # 生成 Atom 订阅源
│   ├── build_og_images.mjs # 生成事件社交分享图
│   ├── build_localized_pages.py # 生成英文默认页、/zh-hans/ 镜像与双语 sitemap
│   └── migrate_v23.py      # v2.3 数据契约迁移脚本（一次性）
│
├── docs/                   # 规范文档
│   ├── README.md           # 文档索引
│   ├── data/               # 数据模型、评分、方向筛选
│   ├── workflow/           # 内容收集、确认、发布流程
│   ├── product/            # 产品规划、模块规范、上线清单
│   └── skills/             # Codex/agent 使用说明
│
└── assets/                 # 静态资源
```

## 数据更新流程

v2.4 规则入口：[EDITORIAL-STANDARD](docs/workflow/EDITORIAL-STANDARD.md)，执行步骤：[WORKFLOW](docs/workflow/WORKFLOW.md)。

1. 定范围与证据截止日 → 多源发现 → 去重/初筛；新批次写 `governance/runs/`，data 下旧筛选日志冻结。
2. 逐主张确认 → 依据变化路径提出分类、等级与影响 → 独立复核；记录于 `governance/reviews/`。
3. 编辑事件/Arc/来源/方向源文件；不手改生成输出。
4. 精确版本经真实人工批准后运行统一校验、测试、构建；获明确发布授权才推送。
5. 方向关联真实 run 的 directionDecisions 与共识搜索；默认 monitor_only。

字段与证据契约见 [REVIEW-CONTRACT](docs/data/REVIEW-CONTRACT.md)，冻结校准材料见 [CALIBRATION](docs/workflow/CALIBRATION.md)。

当前迁移债务与内容复核结果见 [docs/data/CONTENT-AUDIT-2026-07-20.md](docs/data/CONTENT-AUDIT-2026-07-20.md)。`Validation PASSED` 表示契约通过，不等同于所有旧事件已完成事实复核。v2.4 使用精确历史指纹保留未变旧记录，改变后的内容不能通过历史标记绕过门禁；应同时检查审计、reviewProvenance 和警告。

## 数据校验

```
npm run test:editorial           # 编辑契约正反例 + 冻结校准重放
python3 scripts/validate_all.py  # 统一门禁；通过不等于事实审核通过
python3 scripts/calibrate_editorial.py # 离线规则重放，不是跨模型实测
python3 scripts/build_events.py # 生成数据/页面及双向关系；不代替统一门禁
```

## 技术栈

- 纯静态 HTML/CSS/JS 前端（无框架依赖）
- 数据层：JSON 文件 + Python 构建脚本
- SEO 语言架构：英文使用默认路径，简体中文使用 `/zh-hans/`；构建时生成双向 hreflang、独立 canonical 与双语 sitemap
- 搜索来源：Brave Search API
- 部署目标：Cloudflare Pages（见 [docs/product/PRODUCT-PLAN.md](docs/product/PRODUCT-PLAN.md)）
