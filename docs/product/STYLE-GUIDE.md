# EpochArc 文案风格指南

## 标题规范

### 核心原则：一个标题只说一件事

标题不是摘要。标题的任务是让读者**想点进来**，摘要的任务是告诉读者**里面有什么**。两者分开写，不要塞进一句话里。

### 禁止句式

**禁用：逗号+分词解释意义**

这是最常见的句式陷阱。解释意义是摘要的工作，不是标题的工作。

- 不要写：`Meta releases LLaMA, triggering the open-weight LLM revolution`
- 不要写：`OpenAI launches ChatGPT, bringing AI to 100 million users in two months`
- 不要写：`Auto-GPT goes viral, giving mainstream developers their first taste of autonomous AI agents`

**禁用："From X to Y" 模板**

专题子标题尤其容易掉进这个坑。

- 不要写：`AI Safety: From Tay to ASL-3`
- 不要写：`AI in Science: From Games to Nobel Prizes`

### 推荐策略（四种交替使用）

每类标题至少切换使用以下四种策略中的两种，相邻标题不得使用同一种策略。

#### 1. 具体数字法

用一个可量化的细节代替抽象判断。

- `ChatGPT hits 100M users in 60 days — faster than any product in history`
- `DeepSeek R1 costs $5.9M to train — Nvidia loses $593B in one day`
- `92,000 tech workers laid off in AI's first measurable job displacement wave`

#### 2. 破折号冲击法

用破折号引出**意料之外**的后果，而不是预期中的意义。

- `LLaMA weights leak on 4chan — and the open-source AI revolution begins`
- `AlphaGo beats Lee Sedol — with a move no human would make`
- `Siri launches on iPhone 4S — millions of ordinary people meet AI for the first time`

#### 3. 引语/圈内梗法

用原话、昵称、社区术语做 hook。

- `OpenAI says GPT-2 is 'too dangerous to release'`
- `'Vibe coding' enters the developer vocabulary — programming becomes intent`
- `'Attention Is All You Need' — the Transformer architecture is born`

#### 4. 直陈事实法

干净的事实本身就足够有力，不需要修饰。

- `IBM Deep Blue defeats world chess champion Garry Kasparov`
- `EU approves the world's first comprehensive AI law`
- `Scarlett Johansson challenges OpenAI over voice that sounds 'eerily similar' to hers`

### 专题标题规范

专题的 main title 和 subtitle 分开承担不同职责：

- **Main title**: 8 个词以内，制造好奇心（可以是问题、反直觉判断、具体画面）
- **Subtitle**: 解释 what + why，但不能重复 main title 已传达的信息

正确示范：

```
Title:    The Fork
Subtitle: How open-weight and proprietary models split the AI industry in two

Title:    When AI Goes Wrong
Subtitle: A decade of safety failures, from a racist chatbot to government export bans
```

错误示范（main title 和 subtitle 说同一件事）：

```
Title:    AI Safety: From Tay to ASL-3
Subtitle: How AI safety evolved from a chatbot incident to frontier frameworks
```

### 中文标题

中文标题按同一套原则独立写作（不是英文的翻译）。特别利用汉语特点：

- 可省略主语：`上线 16 小时，学会种族歧视`
- 用短句：`一条推文引发的安全危机`
- 避免"的"字堆砌

---

## 预测文案

预测文案避免断言：

- 避免：`will definitely`、`inevitable`、`the end of`、`solved`
- 推荐：`may`、`could`、`is likely to`、`under current assumptions`、`would count as achieved if`

每年 L2/L3 逻辑校验：如果现在回顾去年写的预测，是离谱了还是印证了？只保留经得起时间的语句。

---

## 争议

争议不是削弱内容，而是提升可信度。对于安全、版权、就业、AGI、监管等内容，应主动呈现反方或限制条件：

- `controversy = true` 时，必须至少有一条 `claimType = limitation`。
- 每个 L3 事件至少收录一条反方来源（若有公开反方观点）。

---

## 中英对照

所有公开内容必须同时提供 `en` 和 `zhHans`。AI 辅助翻译后需人工核对：

- 英文为准（内容从事实和来源产生，英文最接近原始信息）。
- 中文不应逐字直译，应保持可读性和自然语感。
- 避免中式英语（Chinglish）和英式中文（过度欧化句式）。

---

## 整体语调

- 描述性而非宣传性：用 "达到 1 亿用户" 而非 "轰动全球"。
- 开放而非封闭：用 "被广泛认为" 而非 "毫无疑问"。
- 承认不确定性：用 "截至当前证据" 而非 "事实证明"。
