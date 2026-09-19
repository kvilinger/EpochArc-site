# 发布检查清单 v2.4

1. 依据 [EDITORIAL-STANDARD](../workflow/EDITORIAL-STANDARD.md) 和 [REVIEW-CONTRACT](../data/REVIEW-CONTRACT.md) 核对阶段、来源、评级路径、证据截止日与真实人工批准。新内容不能借历史标记绕过检查。
2. 公开事件引用只指向 published；Arc 的锚点和 relatedArcs 同样如此。方向至少两个 observed signals，均绑定公开事件与逐主张来源；screeningRunId 回指真实批次。
3. 运行 `npm run test:editorial`、`python3 scripts/validate_all.py`、`npm run build`、`npm run test:seo`。错误阻止发布；警告表示历史债务，不是事实健康证明。
4. 检查构建没有把 governance 下证据、审核、审批或校准文件复制到 dist；来源/响应中不含密钥和不必要个人信息。
5. 政策正式生效时，同步公开 Methods 对纳入条件、来源等级、L1–L3、影响分、共识与方向边界的说明；不能声称全部历史数据已按新规则复核。
6. 检查默认英文页面与 `/zh-hans/` 中文页面、自指 canonical、相互 hreflang、英文 x-default、og:url 与 sitemap 配对。
7. 本地检查双语文本、样式、移动端和关键交互。来源 URL 返回 200 不等于内容支持结论；结构测试也不能替代视觉检查。
8. 收集 Reader Pulse/反馈/分析数据时，检查隐私说明，只保留必要真实数据，不制造互动。
9. 核对 git diff；仅提交本次明确批准的路径。获得独立的发布授权后才 commit/push，部署后检查页面、路由、样式与预期版本。
