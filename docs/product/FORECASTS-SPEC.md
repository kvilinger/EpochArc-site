# Possible Directions 产品规范

**更新日期**：2026-06-25  
**模块定位**：把时间轴中已经出现的现实信号组织成值得持续观察的方向，而不是对未来下判决。

关联文档：
- 方向筛选与方法：[../data/POSSIBLE-DIRECTIONS-SCREENING.md](../data/POSSIBLE-DIRECTIONS-SCREENING.md)
- 数据模型：[../data/DATA-MODEL.md](../data/DATA-MODEL.md)

---

## 1. 命名与用户心智

首页对外名称：

- 英文：**Possible Directions**
- 中文：**可能方向**

内部方法论名称仍可保留 `Future Signals`，但公开页面不宜使用 `Predictions`、`Forecasts` 或“达成率”式语言。

用户应该理解为：

> 这是一个基于已发生事件的观察模块，不是一个自封权威的未来裁定模块。

---

## 2. 模块回答什么问题

时间轴回答：

> 已经发生了什么？

Possible Directions 回答：

> 从这些事件往前看，哪些变化路径已经显露出来，值得继续跟踪？

它不回答：

- 哪条方向一定会赢
- 哪条方向已经被本站正式宣布实现
- 读者投票哪条票多就更真实

---

## 3. 卡片内容结构

每张方向卡只展示四类信息：

1. **Current baseline**  
   当前已经发生到什么程度。
2. **Why this direction**  
   为什么这些事件与信号合起来值得单独观察。
3. **Observed signals**  
   已经出现的现实信号，每条都必须绑定时间轴事件和来源。
4. **Open questions / constraints**  
   当前仍未解决的问题、限制和不确定性。

默认不展示：

- 自定义 `achievedWhen`
- 自定义 `notAchievedWhen`
- “2/5 已满足”式完成度
- 私设持续天数门槛

---

## 4. 信号展示规则

### 4.1 信号是什么

信号不是“未来待完成的 checklist”。

信号是：

> 已经在现实世界中发生、并且能回指到时间轴事件的前兆。

### 4.2 每条信号如何展示

前端应显示：

- signal label
- 简短 summary
- 至少 1 条 linked event

可以显示：

- 对应来源数量
- linked event 的日期与标题

不应显示：

- `met / open`
- `pending`
- `未满足`
- 模块内部自定的完成进度

### 4.3 顶部计数

顶部计数改为：

- `3 linked signals`
- `2 observed signals`

不再使用：

- `3/5 signals met`
- `2/5 已满足`

---

## 5. 事件联动要求

Possible Directions 不是独立漂浮模块，必须与时间轴形成闭环。

最低要求：

- 每条方向至少关联 2 条时间轴事件
- 每条信号至少关联 1 条时间轴事件
- 点击展开后，用户能看出信号从哪些事件推导而来

推荐前端行为：

- 在信号下方显示相关事件标题
- 点击事件标题可跳到或筛到下方时间轴
- 如果一个方向引用了报告或评测框架，也应同时关联至少 1 条具体事件，而不是只挂报告

---

## 6. 裁定与共识状态

### 6.1 默认：`monitor_only`

当前公开方向默认是 `monitor_only`。

页面只表达：

- 这是一个值得观察的方向
- 这些信号已经出现
- 这些问题还没解决

页面不表达：

- 本站已经定义了它的公开达成标准
- 本站有权给它下最终结论

### 6.2 何时允许公开裁定

只有当存在公开的外部共识基础时，方向才可以切换到 `consensus_gated`。

允许的基础类型：

- `regulatory_standard`
- `benchmark_norm`
- `market_consensus`

如果方向进入 `consensus_gated`，页面可以额外显示：

- 共识来自哪些外部来源
- 本站采用的公开口径是什么

即便如此，也应避免把页面做成“判卷式打分板”。

---

## 7. Reader Pulse 交互

### 7.1 1.0 版本定位

1.0 的读者动作仍然是轻量选择：

> Which direction feels most likely to deepen next?

中文可表达为：

> 你更想持续追踪哪个方向？

这更符合模块本质：参与观察，不是假装投票决定真相。

### 7.2 存储

- 当前浏览器只保留一个选择
- 使用 `localStorage`
- 允许改选

### 7.3 不展示全站票数

1.0 不显示：

- 排名
- 票数比例
- 社区共识条

因为这会把方向模块误读成“群众预测市场”。

---

## 8. 展开态布局要求

展开态必须满足：

- 占据整行
- 不把其他方向散落在上下
- 不制造巨大的空白盒子
- 信息优先，而不是解释性文案堆叠

建议结构：

- 左侧：标题、简述、当前基线、为什么值得看
- 右侧：observed signals
- 底部：选择 / 收起操作

如果有 `monitor_only` 状态提示，应保持克制，不单独占据大面积空间。

---

## 9. 数据与页面的对应关系

前端必须按以下映射渲染：

| 数据字段 | 页面用途 |
| --- | --- |
| `title` | 卡片标题 |
| `description` | 卡片简述 |
| `rationale.currentBaseline` | 当前基线 |
| `rationale.whyThisDirection` | 为什么值得看 |
| `rationale.counterSignal` | 当前限制 |
| `rationale.openQuestions` | 开放问题 |
| `signals` | 已观察信号 |
| `signals[].eventIds` | 信号关联的时间轴事件 |
| `consensusBasis` | 是否只观察，或是否已有外部共识基础 |

页面不再依赖：

- `signalChecklist`
- `achievedWhen`
- `notAchievedWhen`
- `minimumDuration`

---

## 10. 当前版本的产品结论

在现阶段，Possible Directions 的价值不在于宣布“谁已经实现”，而在于：

1. 让用户看到时间轴中的哪些事件正在连成线。
2. 把这些线组织成更聚焦的观察主题。
3. 让后续新增事件可以持续挂回这些主题。
4. 在外部共识出现之前，保持方法上的克制。

一句话：

> Possible Directions 是时间轴的前视镜，不是它的判决书。
