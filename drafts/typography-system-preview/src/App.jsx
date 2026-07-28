import { useState } from "react";

const copy = {
  zh: {
    navArcs: "专题",
    navDirections: "方向",
    language: "EN",
    themeLight: "浅色",
    themeDark: "深色",
    back: "返回可能方向",
    pageKicker: "持续监测的研究方向",
    pageTitle: "AI 软件团队",
    pageLead:
      "软件开发正在从一次性的 AI 辅助，走向越来越像团队协作的多智能体闭环。",
    sectionKicker: "证据轨迹",
    sectionTitle: "已观察信号",
    sectionLead:
      "每个信号都连接到站内历史事件和公开来源，后续评审会继续增加、修订或降级这些信号。",
    observed: "已观察",
    related: "相关事件",
    sources: (count) => `${count} 个来源`,
    closeSources: "收起来源",
    counterKicker: "反向条件",
    counterTitle: "什么会削弱这个方向",
    counterBody:
      "代码库上下文理解仍不可靠，验证成本仍然较高，安全和责任归属问题尚未解决，多步 AI 工作流尚无法获得完整信任。",
    railTitle: "方向概览",
    railWindow: "预期窗口",
    railEvidence: "信心 / 证据",
    railEvidenceValue: "中等 / B 级",
    railSignals: "已观察信号",
    railSources: "公开来源",
    railReviewed: "最近复核",
    noteTitle: "排版样例",
    noteBody:
      "本页面只验证全站文字层级、阅读宽度和内容节奏，不代表方向内容已经改版。",
  },
  en: {
    navArcs: "Arcs",
    navDirections: "Directions",
    language: "中文",
    themeLight: "Light",
    themeDark: "Dark",
    back: "Back to Possible Directions",
    pageKicker: "Continuously monitored research direction",
    pageTitle: "AI Software Teams",
    pageLead:
      "Software development is moving from one-off AI assistance toward coordinated, multi-agent workflows that increasingly resemble teams.",
    sectionKicker: "Evidence trail",
    sectionTitle: "Observed signals",
    sectionLead:
      "Every signal links to a historical event and public sources. Later reviews may add, revise, or downgrade the evidence.",
    observed: "Observed",
    related: "Related events",
    sources: (count) => `${count} sources`,
    closeSources: "Hide sources",
    counterKicker: "Counter-condition",
    counterTitle: "What would weaken this direction",
    counterBody:
      "Repository context remains unreliable, verification is still costly, accountability and security are unresolved, and multi-step AI workflows have not yet earned complete trust.",
    railTitle: "Direction overview",
    railWindow: "Expected window",
    railEvidence: "Confidence / evidence",
    railEvidenceValue: "Medium / Grade B",
    railSignals: "Observed signals",
    railSources: "Public sources",
    railReviewed: "Last reviewed",
    noteTitle: "Typography preview",
    noteBody:
      "This page validates hierarchy, reading measure, and content rhythm only. It does not replace the live direction page.",
  },
};

const signals = [
  {
    type: { zh: "产品", en: "Product" },
    title: {
      zh: "AI 结对编程已成为主流开发环境的标准功能。",
      en: "AI pair programming has become a standard feature of mainstream development environments.",
    },
    body: {
      zh: "GitHub Copilot 全面上线，标志着 AI 生成代码从实验演示进入了开发者工具的标准配置。",
      en: "GitHub Copilot’s general availability marked the transition of AI-generated code from research demo to standard developer tooling.",
    },
    events: {
      zh: ["GitHub Copilot 正式发布，AI 结对编程进入所有主流 IDE"],
      en: ["GitHub Copilot launches generally, putting AI pair programming in every major IDE"],
    },
    sources: [
      {
        label: "GitHub Copilot",
        href: "https://github.com/features/copilot",
      },
      {
        label: "McKinsey · The state of AI",
        href: "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
      },
    ],
  },
  {
    type: { zh: "工作流", en: "Workflow" },
    title: {
      zh: "越来越多的开发者通过 LLM 描述和引导代码，而非逐行手写。",
      en: "More developers describe and steer code through LLMs instead of writing every line by hand.",
    },
    body: {
      zh: "“vibe coding” 被确认为一种开发行为模式，说明 AI 介导的软件创建已经足够普及，可以被命名和系统化研究了。",
      en: "The emergence of “vibe coding” as a recognized term shows that AI-mediated software creation is widespread enough to name and study.",
    },
    events: {
      zh: ["“Vibe coding” 一词诞生，概括了 AI 辅助编程的新范式"],
      en: ["“Vibe coding” is coined, capturing a new paradigm of AI-assisted programming"],
    },
    sources: [
      {
        label: "Andrej Karpathy · original post",
        href: "https://x.com/karpathy/status/1886192184808149383",
      },
      {
        label: "Collins Dictionary · Vibe coding",
        href: "https://www.collinsdictionary.com/dictionary/english/vibe-coding",
      },
      {
        label: "Simon Willison · Vibe coding",
        href: "https://simonwillison.net/2025/Feb/6/andrej-karpathy/",
      },
    ],
  },
  {
    type: { zh: "事件", en: "Incident" },
    title: {
      zh: "编程智能体已展示出多步自主执行和后台持续运行的能力。",
      en: "Coding agents have demonstrated multi-step autonomy and persistent background execution.",
    },
    body: {
      zh: "Claude Code 泄露事件表明前沿编程产品已在试验持续运行的背景智能体。Fable 5 在 KernelBench-Mega 上自主开发出 CUDA 内核，完成了完整的系统级编程流程。",
      en: "The Claude Code leak revealed experiments with persistent background agents. Fable 5 autonomously developed a CUDA kernel and completed a full systems-programming workflow.",
    },
    events: {
      zh: [
        "Claude Code 源代码通过 npm 泄露，秘密智能体特性曝光",
        "Claude Fable 5 写出首个 AI 编写的 CUDA 超级内核",
      ],
      en: [
        "Claude Code source code leaks via npm, exposing background-agent features",
        "Claude Fable 5 writes the first AI-authored CUDA megakernel",
      ],
    },
    sources: [
      {
        label: "The Hacker News · Claude Code leak",
        href: "https://thehackernews.com/",
      },
      {
        label: "CNBC · Anthropic internal source",
        href: "https://www.cnbc.com/",
      },
      {
        label: "Stanford HAI · AI Index",
        href: "https://hai.stanford.edu/ai-index",
      },
      {
        label: "Import AI · GPU kernels",
        href: "https://importai.substack.com/",
      },
      {
        label: "KernelBench-Mega leaderboard",
        href: "https://github.com/ScalingIntelligence/KernelBench",
      },
    ],
  },
];

function SignalRow({ signal, index, language }) {
  const [expanded, setExpanded] = useState(false);
  const t = copy[language];

  return (
    <li className="signal-row">
      <span className="signal-marker" aria-hidden="true">
        {String(index + 1).padStart(2, "0")}
      </span>
      <div className="signal-content">
        <p className="signal-meta">
          <span>{t.observed}</span>
          <span>{signal.type[language]}</span>
        </p>
        <h3>{signal.title[language]}</h3>
        <p className="signal-description">{signal.body[language]}</p>
        <div className="related-events">
          <span>{t.related}</span>
          <ul>
            {signal.events[language].map((event) => (
              <li key={event}>{event}</li>
            ))}
          </ul>
        </div>
        <ul className="source-list" id={`sources-${index + 1}`} hidden={!expanded}>
          {signal.sources.map((source) => (
            <li key={source.href}>
              <a href={source.href} target="_blank" rel="noreferrer">
                {source.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      <button
        className="source-toggle"
        type="button"
        aria-expanded={expanded}
        aria-controls={`sources-${index + 1}`}
        onClick={() => setExpanded((value) => !value)}
      >
        {expanded ? t.closeSources : t.sources(signal.sources.length)}
      </button>
    </li>
  );
}

export function App() {
  const [language, setLanguage] = useState("zh");
  const [theme, setTheme] = useState("light");
  const t = copy[language];

  return (
    <div className="app" data-theme={theme} lang={language === "zh" ? "zh-Hans" : "en"}>
      <header className="topnav">
        <div className="topnav-inner">
          <a className="brand" href="https://epoch-arc.com/" aria-label="EpochArc">
            <img src="/assets/logo-icon.svg" alt="" />
            <span>EpochArc</span>
          </a>
          <nav className="topnav-actions" aria-label="Primary navigation">
            <a href="https://epoch-arc.com/arcs/">{t.navArcs}</a>
            <a className="is-current" href="https://epoch-arc.com/directions/">
              {t.navDirections}
            </a>
            <button type="button" onClick={() => setLanguage(language === "zh" ? "en" : "zh")}>
              {t.language}
            </button>
            <button
              type="button"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            >
              {theme === "light" ? t.themeDark : t.themeLight}
            </button>
          </nav>
        </div>
      </header>

      <main className="site-page">
        <a className="page-back" href="https://epoch-arc.com/directions/">
          {t.back}
        </a>

        <div className="page-layout">
          <article className="direction-main">
            <header className="page-header">
              <p className="overline page-kicker">{t.pageKicker}</p>
              <h1>{t.pageTitle}</h1>
              <p className="page-lead">{t.pageLead}</p>
            </header>

            <section className="evidence-section" aria-labelledby="evidence-title">
              <header className="section-header">
                <p className="overline">{t.sectionKicker}</p>
                <h2 id="evidence-title">{t.sectionTitle}</h2>
                <p>{t.sectionLead}</p>
              </header>

              <ol className="signal-ledger">
                {signals.map((signal, index) => (
                  <SignalRow
                    key={signal.title.en}
                    signal={signal}
                    index={index}
                    language={language}
                  />
                ))}
              </ol>
            </section>

            <section className="counter-section" aria-labelledby="counter-title">
              <p className="overline">{t.counterKicker}</p>
              <h2 id="counter-title">{t.counterTitle}</h2>
              <p>{t.counterBody}</p>
            </section>
          </article>

          <aside className="page-rail" aria-label={t.railTitle}>
            <section className="rail-card">
              <h2>{t.railTitle}</h2>
              <dl>
                <div>
                  <dt>{t.railWindow}</dt>
                  <dd>2027–2030</dd>
                </div>
                <div>
                  <dt>{t.railEvidence}</dt>
                  <dd>{t.railEvidenceValue}</dd>
                </div>
                <div>
                  <dt>{t.railSignals}</dt>
                  <dd>3</dd>
                </div>
                <div>
                  <dt>{t.railSources}</dt>
                  <dd>10</dd>
                </div>
                <div>
                  <dt>{t.railReviewed}</dt>
                  <dd>2026-07-09</dd>
                </div>
              </dl>
            </section>
            <section className="rail-card rail-note">
              <h2>{t.noteTitle}</h2>
              <p>{t.noteBody}</p>
            </section>
          </aside>
        </div>
      </main>

      <footer className="footer">
        <div>
          <span>© 2026 EpochArc</span>
          <span>Typography system preview</span>
        </div>
      </footer>
    </div>
  );
}
