# EpochArc 专题叙事标准

**版本**：v0.1
**更新日期**：2026-06-30
**适用范围**：专题叙事（Arcs）的内容结构、叙事标准、模板与编辑规范。

---

## 1. 什么是专题叙事？

专题叙事（Arc）是将时间轴上散落的 AI 里程碑串联为一条可阅读的叙事线。它不是新闻报道，不是维基百科，也不是技术综述。

一个合格的 arc 必须具备：

| 属性 | 含义 |
| --- | --- |
| **有论点** | 整条线支持一个明确的判断，不是说"发生了什么"，而是"为什么这很重要 / 哪里出了问题 / 我们误解了什么" |
| **有张力** | 每个章节包含冲突、选择、未解问题——不是平铺直叙 |
| **有立场** | 编辑者必须做出判断。安全的选择 = 没有价值 |
| **可反驳** | 如果读者找不到可以不同意的地方，说明写得不够锋利 |

### 1.1 专题叙事 ≠

- Wikipedia 条目：平铺事实、不表态
- AI 论文 survey：罗列工作、分类归档
- 新闻深度报道：围绕单一事件展开
- 博客个人感悟：缺乏结构化论证

Arc 是上述的杂交体：有调查报道的判断力、有 essay 的论点、有 survey 的结构、有时间轴的可视化锚点。

---

## 2. 四大叙事原型

每个 arc 必须归入（或明显接近）以下四种原型之一：

### 2.1 技术演进线 (Technical Evolution)

追踪一项核心技术从起源到现状的演变。

**适用场景**：Transformer、扩散模型、RL、神经渲染……

**结构特点**：
- 时间跨度大（5-15 年）
- 关键节点清晰（论文 → 突破 → 产品化 → 产业影响）
- 每章一个"为什么这一步在当时是正确的选择"

**代表选题**：Transformer Empire（本文档的首个示例）

**关键判定**：读者读完应该理解技术路线背后的决策逻辑，不仅是结果。

### 2.2 主题线索 (Thematic Thread)

跟随一个主题（安全、监管、开源、劳动力冲击）跨越不同技术/事件。

**适用场景**：AI 监管史、开源与闭源之争、AI 裁员潮……

**结构特点**：
- 时间跨度可长可短
- 事件来源分散（不同技术、不同公司）
- 每章一个"在这个领域，格局怎样变了"

**代表选题**：AI 监管的前世今生、大模型开源运动

**关键判定**：读者读完应该对一个跨领域问题形成系统性认知。

### 2.3 社会断层 (Societal Shift)

AI 如何改变了普通人生活、工作、社会结构。

**适用场景**：AI 对编程的改变、AI 在创意行业的渗透、AI 与教育……

**结构特点**：
- 以人群视角切入（不是技术视角）
- 依赖"社会信号"事件（不是能力突破事件）
- 可以包含具体人物故事或行业截面

**代表选题**：AI 时代的程序员、被 AI 改变的课堂

**关键判定**：不搞 AI 的人也能读懂，并感到"这和我有关"。

### 2.4 对比/岔路 (Fork & Friction)

两条竞争路线、两个互相矛盾的叙事、或者一个关键决策时刻。

**适用场景**：Encoder vs Decoder、Scaling vs Efficiency、开源 vs 闭源……

**结构特点**：
- 天生有张力——每个章节展示对立面
- 不预设"正确"答案——呈现证据后给出编辑判断
- 通常以"今天我们知道结果了，但当时可不是这样"开场

**代表选题**：BERT vs GPT 的岔路、Scaling Laws 的胜利与局限

**关键判定**：读者读完应该理解"当时的选择为什么不是显而易见的"。

---

## 3. 结构要求

### 3.1 章节

| 字段 | 要求 |
| --- | --- |
| 章节数 | 3-6 章 |
| 每章论点 | 必须有每章一句可反驳的 thesis |
| 锚点事件 | 每章 2-5 个，必须回指已发布的时间轴事件 |
| 核心洞察 | 每章必须有一条 Key Insight（一句话总结） |

### 3.2 长度

| 元素 | 正文长度（英文，建议） | 中文 |
| --- | --- | --- |
| Subtitle | 10-15 词 | 12-18 字 |
| Abstract | 40-60 词 | 70-100 字 |
| 每章 narrative | 100-200 词 | 180-350 字 |
| 每章 Key Insight | 6-12 词 | 10-20 字 |
| Conclusion | 60-100 词 | 100-180 字 |

### 3.3 元数据

- 起始、结束日期（从锚点事件中取最早和最晚）
- 覆盖事件数量
- 覆盖分类标签（从锚点事件中汇总）
- 作者/策展人

---

## 4. 叙事声音标准

这是本规范最核心的部分。**如果一句话在维基百科上也成立，删掉重写。**

### 4.0 中文独立写作原则（防止翻译腔）

**中文不是英文的翻译。中文是并行创作。**

这是 arc 写作中最容易被忽视的一条：英文和中文必须从同一套大纲出发独立写作。先写英文再翻译成中文，无论如何都会留下翻译腔。正确的做法是：

```
大纲（outline + key claims）
├── English: write from outline, ensure humanizer patterns clean
└── 中文：从同一套大纲写出中文。不能看英文文本。
```

#### 翻译腔自检清单

写完后对照以下项目逐条检查。命中任何一项就说明这段需要重写：

| # | 检测项 | 翻译腔标志 | 示范（差） | 示范（好） |
|---|--------|-----------|-----------|-----------|
| 1 | **的密度** | 连续两个以上的 "的" 出现在一句话里 | "Transformer 的并行化的最大优势是" | "Transformer 最大的优势是并行" |
| 2 | **句首镜像** | 中文句首跟英文句首一一对应（时间、地点、主语） | "2017 年，八个 Google 研究员决定终结 RNN" | "2017 年，Google 八个研究员做了一个决定" |
| 3 | **主语惯性** | 每句都有明确主语，全是 SVO 结构 | "Transformer 靠一个简单的优势赢了" | "赢在哪儿？并行。" |
| 4 | **抽象主语** | "这"、"那"、"它" 开头作主语 | "这等于承认了预训练的收益在递减" | "预训练的收益在递减。这句话不是猜测，是 o1 的分数单。" |
| 5 | **是...的** | "是 X 的 Y" 或 "是...的" 作结 | "Transformer 是靠让 GPU 满负荷运转取胜的" | "Transformer 赢在让 GPU 满负荷运转。" |
| 6 | **长前置定语** | 动宾短语做定语塞在名词前面 | "你花在 GPU 上的钱有一大半是买它闲着" | "GPU 的钱有一大半花在等待上。"（但更好的是拆成短句） |
| 7 | **被动语态** | "被" 字句过多 | "循环结构被彻底删掉了" | "循环结构，删掉。整个删掉。" |
| 8 | **抽象名词作谓语** | "是...的产物"、"体现了..."、"展示了..." | "这体现了对齐能力的价值" | "对齐能力本身变成了产品的护城河。" |
| 9 | **书面连接词** | "然而"、"因此"、"此外"、"与此同时" | "然而，顺序依赖还在" | "但顺序依赖还在。Transformer 把它拿掉了。" |
| 10 | **节奏单调** | 所有句子长度接近，没有长短交替 | 连续 5 句同样长度 | 短句、碎片句、长句交替 |

#### 中文的天然优势

中文写作应该利用而不是对抗汉语特点：

- **主谓可以省略**："不是一点点改，而是彻底删掉"（无主语句）
- **动词优先**："决定终结 RNN" 比 "做了一个终结 RNN 的决定" 好十倍
- **四字格**："顺藤摸瓜"、"连根拔起" → 不要每处都用，但关键判断点用一下很提气
- **把字句**：天然主动、有力。"把循环结构删掉" 比 "删掉了循环结构" 更有力
- **句末语气词**：在合适的地方用 "了"、"的"、"吧" 制造口语感
- **节奏对仗**："Google 赢了基准测试。OpenAI 赢了市场。" → 对称、利落

#### 两段式工作流

```
第一步（并行创作）：
  大纲 → 英文（humanizer 检测）
  大纲 → 中文（独立写，不看英文）

第二步（交叉自检）：
  1. 中文跑翻译腔 10 项清单
  2. 中文跑 khazix-writer 四层检测（L1 标点/L2 风格/L3 内容/L4 活人感）
  3. 对照英文检查事实一致（但不检查句式）
```

只有事实必须一致。句式、节奏、结构、例子选择可以完全不同。

### 4.1 英语叙事声音标准（English Voice）

### 4.1 必须遵守

| 规则 | 坏例子 | 好例子 |
| --- | --- | --- |
| **每章以论点开头** | "In 2014, Bahdanau et al. introduced the attention mechanism..." | "The 2014 attention paper didn't solve AI. It solved a GPU utilization problem." |
| **包含反直觉判断** | "Transformer scaled well due to parallelization." | "Transformer didn't beat RNNs on quality. It beat them on hardware economics." |
| **承认不确定性** | "This shows scaling works." | "Scaling worked for seven years. Whether it works another seven is an open bet." |
| **使用具体比较** | "GPT-4 scored well on benchmarks." | "GPT-4's bar exam score (90th percentile) meant the model could pass the bar but couldn't argue a case." |
| **选择立场** | "The implications are significant." | "If this trend continues, the market will consolidate around three players." |
| **结束于开放问题** | "Future work remains." | "The data wall is real. The question is whether synthetic data plugs the gap." |

### 4.2 禁止

- ❌ "This demonstrates that..." / "This shows that..."（编辑不需要声明自己在展示什么——读者能看出来）
- ❌ "It is important to note that..."（如果重要就说为什么，不要注释重要性）
- ❌ 被动语态作秀（"was validated by" → "proved"）
- ❌ 两段之间纯时间过渡（"In 2023, ... In 2024, ..." —— 除非时间本身是论点）
- ❌ 结语中虚无缥缈的展望（"The future remains unwritten" —— 这等于什么都没说）

### 4.3 力度分级

| 确信度 | 用词 | 示例 |
| --- | --- | --- |
| 高（有充分证据） | 直接陈述 | "This was the wrong call." |
| 中（有迹象但非定论） | 问题形式 | "Was this really necessary?" |
| 低（推测） | 明确标记 | "The data here is thin, but the pattern suggests..." |

不要在不确定时装确定，也不要在确定时模糊。

---

## 5. 模板结构

每个 arc 目录是自包含的静态页面：

```
arcs/{slug}/
  index.html    ← 完整页面
```

HTML 结构必须包含：

```
<!doctype html>
<html lang="zh-CN">
<head>
  <title>... · EpochArc</title>
  <meta name="description" content="..." />
  <meta property="og:title" content="..." />
  <meta property="og:description" content="..." />
  <meta property="og:type" content="article" />
  <link rel="icon" href="../../assets/logo-icon.svg" />
  <link rel="stylesheet" href="../../src/css/arcs.css" />
  <script type="application/ld+json">{Article Schema}</script>
</head>
<body>
  <!-- Top Nav -->
  <header class="topnav">...</header>

  <main class="arc-detail-container">
    <!-- Back Link -->
    <a href="../../arcs.html" class="back-link">...</a>

    <!-- Hero -->
    <div class="arc-hero">...</div>

    <!-- TOC -->
    <div class="arc-toc">...</div>

    <!-- Abstract -->
    <div class="arc-abstract">...</div>

    <!-- Chapters -->
    <section class="arc-chapter" id="chapter-xxx">
      <div class="arc-chapter-header">...</div>
      <div class="arc-chapter-narrative" data-zh="" data-en="">...</div>
      <div class="arc-key-insight">...</div>
      <div class="arc-anchor-events">...</div>
    </section>

    <!-- Conclusion -->
    <div class="arc-conclusion">...</div>

    <!-- Related Arcs -->
    <div class="arc-related">...</div>
  </main>

  <footer>...</footer>
  <script type="module" src="../../src/js/arcs.js"></script>
</body>
</html>
```

---

## 6. 发布前检查清单

### 结构完整

- [ ] 章节数在 3-6 之间
- [ ] 每章至少 2 个锚点事件
- [ ] 所有锚点事件链接存在（`../../events/{eventId}/index.html`）
- [ ] TOC 链接匹配章节 ID
- [ ] Abstract 存在且简洁
- [ ] Conclusion 存在且**有具体立场**

### 叙事质量

- [ ] 每章的第一句话是一个可反驳的论点（不是一个事实陈述）
- [ ] 至少有一处承认不确定性或反方证据
- [ ] 没有 Wikipedia 风格的平铺叙述
- [ ] 结语不写空洞展望
- [ ] 全文无 AI 生成腔（"This arc documents..." / "It is worth noting..."）

### 双语

- [ ] 所有 `data-zh` 和 `data-en` 均已填写
- [ ] 中文翻译不是英文的逐字硬译
- [ ] Arc 标题和 subtitle 两者均为独立撰写的双语版本（不是直译）

### 页面

- [ ] 所有资源路径正确（`../../src/` 可用）
- [ ] `data/arcs.json` 中已注册该 arc
- [ ] `arcs.html` 中已添加卡片

---

## 7. 选题标准

不是任何事件集合都够格成为 arc。选题通过以下三道门槛：

### 门槛一：有清晰的论点

候选选题必须能用一句话回答："这个 arc 想说服读者相信什么？"

| ✅ 可接受 | ❌ 不可接受 |
| --- | --- |
| "Transformer 的并行化设计使其成为 AI 产业的硬件基础设施层" | "讲一下 Transformer 的故事" |
| "AI 监管的发展方向是从放任到收紧，但每次收紧都源于一次安全事故" | "整理 AI 监管相关事件" |
| "开源与闭源的竞争格局在 2025 年发生了根本性逆转" | "看看开源和闭源的对比" |

### 门槛二：论点是可反驳的

不是显而易见的常识。如果大多数人已经同意，说明论点太平庸。

### 门槛三：有足够的事件密度

- 最少 5 个不重复锚点事件
- 时间跨度至少覆盖 3 年（同一个时间点的集合适合做"深度阅读"而不是 arc）
- 事件分布不能全部集中在同一年或同一个月

---

## 8. 与 DATA-MODEL 的关系

Arc **不定义新的事件字段**。所有锚点事件必须来自 `data/events.json`。

Arc 的叙事文本是独立创作，不存储为事件字段。事件 JSON 中的 `narrative` 字段保留给事件的独立背景描述。Arc 的章节叙事可以引用事件中的事实，但必须包含编辑判断（即事件 JSON 的 `narrative` 是客观背景，arc 是主观叙事）。

Arc 的 Key Insight 可以与事件的 `significance` 或 `impactIndex` 不同。因为 arc 的叙事线有自己的编辑判断，不一定等于事件的个体评分。

**跨 arc 一致性**：同一个事件出现在不同 arc 中可以有不同解读。这是允许的——arc 的叙事线是独立作品。

---

## 9. 版本记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v0.1 | 2026-06-30 | 初始版本 |
