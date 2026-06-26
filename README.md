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
├── data/                   # 构建输出（前端消费）
│   ├── events.json         # 合并后的事件数据
│   ├── sources.json        # 来源独立表
│   ├── labels.json         # 枚举标签中英对照
│   ├── forecasts.json      # Possible Directions 数据
│   └── possible_directions_screening_log.json  # 方向筛选运行记录
│
├── scripts/
│   ├── build_events.py     # 合并 content/ → data/
│   └── migrate_categories.py  # v1→v2 分类迁移脚本（一次性）
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

1. 运行 [docs/workflow/WORKFLOW.md](docs/workflow/WORKFLOW.md) 中的多源发现 → 筛选候选 → 写入本地候选日志（格式可自定）
2. 通过候选的事件写 `content/events/{event-id}.json`（参考 [docs/data/DATA-MODEL.md](docs/data/DATA-MODEL.md) 附录示例）
3. 来源加入 `data/sources.json`
4. 运行 `python3 scripts/build_events.py` 构建 `data/events.json`
5. Possible Directions 的公开筛选结果维护在 `data/possible_directions_screening_log.json`
6. 前端自动读取（`fetch` 加载）

## 数据校验

```
python3 scripts/build_events.py  # 合并 + 基本校验
python3 scripts/validate_forecasts.py  # Possible Directions 数据校验
```

## 技术栈

- 纯静态 HTML/CSS/JS 前端（无框架依赖）
- 数据层：JSON 文件 + Python 构建脚本
- 搜索来源：Brave Search API
- 部署目标：Cloudflare Pages（见 [docs/product/PRODUCT-PLAN.md](docs/product/PRODUCT-PLAN.md)）
