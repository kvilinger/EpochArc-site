# EpochArc 编辑执行入口 v2.4

本文件是导航，不定义第二套规则。

## 必读顺序

1. [EDITORIAL-STANDARD](../workflow/EDITORIAL-STANDARD.md)：规则、边界、未知处理和权限。
2. [WORKFLOW](../workflow/WORKFLOW.md)：阶段执行步骤。
3. [DATA-MODEL](../data/DATA-MODEL.md) 与 [REVIEW-CONTRACT](../data/REVIEW-CONTRACT.md)：公开字段与私有证据/批准结构。
4. [CALIBRATION](../workflow/CALIBRATION.md)：冻结案例、提示词和一致性测量。
5. 对应模块的语言、Arc 或方向规范；它们不能覆盖证据与批准门槛。

## 执行检查

- 先对齐范围、是否允许写源数据、是否允许发布；检查工作区。
- Discover → Screen → Confirm → Edit → Review → 人工批准 → Publish，不能跳过。
- 新批次写 governance/runs；旧 data 下筛选日志冻结。
- full 记录全部核心渠道和六类覆盖；快照不是日期窗覆盖，故障/缺口如实记录。
- 初筛总分只决定核实优先级；评级从变化路径及证据决定。
- 未知写 null，不捏造数值、来源访问、人工批准、模型评审或反方意见。
- 分类按动作；日期按真实动作阶段；可用、采用、融资完成、监管生效分别核实。
- 影响指数只用已观察后果、固定受众 ID、可复算观察期。
- 中英文共用事实台账，允许自然表达差异，不允许新增或强化事实。
- 已发布数据不因新规则自动降级。精确旧指纹仅允许历史债务继续存在，不供新改动绕过。

## 入口命令

```bash
npm run test:editorial
python3 scripts/validate_all.py
python3 scripts/audit_editorial.py
npm run build
npm run test:seo
```

测试只说明契约行为，不代替事实审核。构建后检查生成 diff 和页面；无明确授权不得 commit/push。只暂存本次相关文件。

## 编辑源

- 事件：content/events/*.json
- Arc：content/arcs/*.json
- 来源：data/sources.json
- 方向：data/forecasts.json
- 标签：data/labels.json
- 参数：governance/policy.json

不得手工修改 data/events.json、data/arcs.json 或生成页面。不要把 governance/evidence、review、approval 复制到公开静态目录。

## 历史回溯

使用 backfill 批次并说明范围，不强行伪造历史社交渠道覆盖。仍需事实/影响/分析/反方确认和同样的评级标准。后来的真实证据可用于回顾评级，但必须注明截止日，不冒充当时已知。
