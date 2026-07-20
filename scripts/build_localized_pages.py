#!/usr/bin/env python3
"""Generate static English and Simplified Chinese pages with SEO annotations."""

from __future__ import annotations

import html
import json
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BASE_URL = "https://epoch-arc.com"


@dataclass(frozen=True)
class PageSpec:
    source: Path
    route: str
    title_en: str
    title_zh: str
    description_en: str
    description_zh: str
    last_modified: str

    @property
    def english_url(self) -> str:
        return f"{BASE_URL}{self.route}"

    @property
    def chinese_route(self) -> str:
        if self.route == "/":
            return "/zh-hans/"
        localized_route = f"/zh-hans{self.route}"
        return localized_route if localized_route.endswith("/") else f"{localized_route}/"

    @property
    def chinese_url(self) -> str:
        return f"{BASE_URL}{self.chinese_route}"

    @property
    def chinese_output(self) -> Path:
        if self.route == "/":
            return DIST / "zh-hans" / "index.html"
        clean_route = self.route.strip("/")
        return DIST / "zh-hans" / clean_route / "index.html"


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def localized(value, language: str) -> str:
    if isinstance(value, dict):
        key = "zhHans" if language == "zh-Hans" else "en"
        return str(value.get(key) or value.get("en") or value.get("zhHans") or "")
    return str(value or "")


def clean_description(value: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip(" ,.;，。；") + "…"


def page_specs() -> list[PageSpec]:
    today = date.today().isoformat()
    events = load_json(ROOT / "data" / "events.json")
    arcs = load_json(ROOT / "data" / "arcs.json")
    directions = load_json(ROOT / "data" / "forecasts.json")

    specs = [
        PageSpec(
            DIST / "index.html",
            "/",
            "EpochArc · AI Timeline: Key Milestones from 1950 to Today",
            "EpochArc · AI 时间轴：1950 至今的重要里程碑",
            f"Explore {len(events)} curated AI milestones with evidence, impact analysis, narrative arcs, and possible directions.",
            f"浏览 {len(events)} 个经过策展的 AI 里程碑，以及对应来源、影响分析、专题叙事与可能方向。",
            today,
        ),
        PageSpec(
            DIST / "methods.html",
            "/methods",
            "Methodology & Sources · EpochArc",
            "方法与来源 · EpochArc",
            "How EpochArc curates AI milestones, evaluates evidence, scores impact, and reviews possible directions.",
            "了解 EpochArc 如何筛选 AI 里程碑、评估来源证据、计算影响指数并复核可能方向。",
            today,
        ),
        PageSpec(
            DIST / "arcs.html",
            "/arcs",
            "Narrative Arcs · EpochArc",
            "专题叙事 · EpochArc",
            "Threading scattered AI milestones into readable narrative arcs that reveal longer-term technological change.",
            "将散落的 AI 里程碑串联为可阅读的叙事线，追踪技术演进的深层脉络。",
            today,
        ),
        PageSpec(
            DIST / "directions.html",
            "/directions",
            "Possible Directions · EpochArc",
            "可能方向 · EpochArc",
            "Evidence-led directions EpochArc is monitoring across AI capabilities, products, science, and deployment.",
            "EpochArc 基于已发布事件与公开证据，持续复核 AI 能力、产品、科学与部署方向。",
            today,
        ),
    ]

    for event in events:
        slug = event["slug"]
        title_en = localized(event.get("title"), "en")
        title_zh = localized(event.get("title"), "zh-Hans")
        summary = event.get("searchSummary") or event.get("summary") or {}
        specs.append(
            PageSpec(
                DIST / "events" / slug / "index.html",
                f"/events/{slug}/",
                f"{title_en} · EpochArc",
                f"{title_zh} · EpochArc",
                clean_description(localized(summary, "en")),
                clean_description(localized(summary, "zh-Hans")),
                event.get("editorial", {}).get("updatedAt") or event.get("date") or today,
            )
        )

    for arc in arcs:
        slug = arc["slug"]
        title_en = localized(arc.get("title"), "en")
        title_zh = localized(arc.get("title"), "zh-Hans")
        specs.append(
            PageSpec(
                DIST / "arcs" / slug / "index.html",
                f"/arcs/{slug}/",
                f"{title_en} · EpochArc",
                f"{title_zh} · EpochArc",
                clean_description(localized(arc.get("subtitle"), "en")),
                clean_description(localized(arc.get("subtitle"), "zh-Hans")),
                arc.get("updatedAt") or today,
            )
        )

    for direction in directions:
        slug = direction["slug"]
        title_en = localized(direction.get("title"), "en")
        title_zh = localized(direction.get("title"), "zh-Hans")
        specs.append(
            PageSpec(
                DIST / "directions" / slug / "index.html",
                f"/directions/{slug}/",
                f"{title_en} · EpochArc",
                f"{title_zh} · EpochArc",
                clean_description(localized(direction.get("description"), "en")),
                clean_description(localized(direction.get("description"), "zh-Hans")),
                direction.get("editorial", {}).get("updatedAt") or direction.get("updatedAt") or today,
            )
        )

    return specs


LOCALIZABLE_ELEMENT = re.compile(
    r"<(?P<tag>[A-Za-z][\w:-]*)(?P<attrs>[^<>]*\bdata-(?:en|zh)=\"[^\"]*\"[^<>]*)>"
    r"(?P<text>[^<]*)</(?P=tag)>",
    re.DOTALL,
)


def localize_visible_text(markup: str, language: str) -> str:
    attribute = "data-zh" if language == "zh-Hans" else "data-en"

    def replace(match: re.Match) -> str:
        value_match = re.search(rf'\b{attribute}="([^"]*)"', match.group("attrs"))
        if not value_match:
            return match.group(0)
        value = html.unescape(value_match.group(1))
        return (
            f'<{match.group("tag")}{match.group("attrs")}>'
            f'{html.escape(value, quote=False)}'
            f'</{match.group("tag")}>'
        )

    return LOCALIZABLE_ELEMENT.sub(replace, markup)


def replace_head_value(markup: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, markup, count=1, flags=re.IGNORECASE)
    if count:
        return updated
    return markup.replace("</head>", f"  {replacement}\n</head>", 1)


def set_meta(markup: str, attribute: str, key: str, value: str) -> str:
    escaped = html.escape(value, quote=True)
    pattern = (
        rf'<meta\b(?=[^>]*\b{re.escape(attribute)}="{re.escape(key)}")'
        rf'[^>]*\bcontent="[^"]*"[^>]*>'
    )
    replacement = f'<meta {attribute}="{key}" content="{escaped}" />'
    return replace_head_value(markup, pattern, replacement)


def set_page_links(markup: str, canonical: str, english_url: str, chinese_url: str) -> str:
    markup = re.sub(
        r'\s*<link\b(?=[^>]*\brel="alternate")(?=[^>]*\bhreflang="[^"]+")[^>]*>\s*',
        "\n",
        markup,
        flags=re.IGNORECASE,
    )
    canonical_tag = f'<link rel="canonical" href="{html.escape(canonical, quote=True)}" />'
    alternates = (
        f'{canonical_tag}\n'
        f'  <link rel="alternate" hreflang="en" href="{english_url}" />\n'
        f'  <link rel="alternate" hreflang="zh-Hans" href="{chinese_url}" />\n'
        f'  <link rel="alternate" hreflang="x-default" href="{english_url}" />'
    )
    pattern = r'<link\b(?=[^>]*\brel="canonical")[^>]*>'
    return replace_head_value(markup, pattern, alternates)


def normalize_resource_urls(markup: str) -> str:
    def replace(match: re.Match) -> str:
        attribute, quote, value = match.groups()
        if value.startswith(("http://", "https://", "//", "data:", "#")):
            return match.group(0)
        normalized = re.sub(r"^(?:\.\.?/)+", "", value)
        if normalized.startswith(("assets/", "src/", "data/")):
            value = f"/{normalized}"
        return f"{attribute}={quote}{value}{quote}"

    return re.sub(r'\b(href|src)=("|\')([^"\']+)(?:\2)', replace, markup)


def chinese_internal_links(markup: str) -> str:
    excluded = ("/assets/", "/src/", "/data/", "/rss.xml", "/sitemap.xml", "/robots.txt", "/zh-hans")

    def replace(match: re.Match) -> str:
        quote, value = match.groups()
        if not value.startswith("/") or value.startswith(excluded):
            return match.group(0)
        localized_href = "/zh-hans/" if value == "/" else f"/zh-hans{value}"
        if localized_href in ("/zh-hans/methods", "/zh-hans/arcs", "/zh-hans/directions"):
            localized_href += "/"
        return f"href={quote}{localized_href}{quote}"

    return re.sub(r'\bhref=("|\')([^"\']+)(?:\1)', replace, markup)


def localized_site_url(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https") or parsed.netloc != "epoch-arc.com":
        return value
    if parsed.path.startswith(("/assets/", "/src/", "/data/", "/rss.xml", "/zh-hans/")):
        return value
    path = "/zh-hans/" if parsed.path == "/" else f"/zh-hans{parsed.path}"
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def rewrite_json_ld(markup: str, language: str, title: str, description: str) -> str:
    pattern = re.compile(
        r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
        re.IGNORECASE | re.DOTALL,
    )

    def replace(match: re.Match) -> str:
        try:
            payload = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)

        def visit(value):
            if isinstance(value, dict):
                return {key: visit(item) for key, item in value.items()}
            if isinstance(value, list):
                return [visit(item) for item in value]
            if language == "zh-Hans" and isinstance(value, str):
                return localized_site_url(value)
            return value

        payload = visit(payload)
        if isinstance(payload, dict):
            if "headline" in payload:
                payload["headline"] = title.removesuffix(" · EpochArc")
            elif payload.get("@type") in ("Article", "WebPage") and "name" in payload:
                payload["name"] = title.removesuffix(" · EpochArc")
            if "description" in payload:
                payload["description"] = description
            payload["inLanguage"] = language
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).replace("</", "<\\/")
        return f"{match.group(1)}\n{encoded}\n{match.group(3)}"

    return pattern.sub(replace, markup)


def language_routing_script(language: str) -> str:
    return f'''  <script id="static-language-routing">
    (() => {{
      const language = {json.dumps(language)};
      const isChinese = language === 'zh-Hans';
      try {{ localStorage.setItem('epocharc-lang', language); }} catch (_) {{}}

      window.localizedSitePath = (path) => {{
        if (!isChinese || !path || !path.startsWith('/') || path.startsWith('/zh-hans')) return path;
        if (path === '/') return '/zh-hans/';
        const localized = `/zh-hans${{path}}`;
        return ['/zh-hans/methods', '/zh-hans/arcs', '/zh-hans/directions'].includes(localized)
          ? `${{localized}}/`
          : localized;
      }};

      const excluded = ['/assets/', '/src/', '/data/', '/rss.xml', '/sitemap.xml', '/robots.txt', '/zh-hans'];
      const localizeAnchor = (anchor) => {{
        if (!isChinese) return;
        const href = anchor.getAttribute('href');
        if (!href || !href.startsWith('/') || excluded.some((prefix) => href.startsWith(prefix))) return;
        anchor.setAttribute('href', window.localizedSitePath(href));
      }};
      const localizeTree = (root) => {{
        if (root.matches?.('a[href]')) localizeAnchor(root);
        root.querySelectorAll?.('a[href]').forEach(localizeAnchor);
      }};

      document.addEventListener('change', (event) => {{
        const select = event.target.closest?.('.language-select');
        if (!select) return;
        const alternate = document.querySelector(`link[rel="alternate"][hreflang="${{select.value}}"]`);
        if (!alternate) return;
        const target = new URL(alternate.href);
        if (['localhost', '127.0.0.1'].includes(window.location.hostname)) {{
          target.protocol = window.location.protocol;
          target.host = window.location.host;
        }}
        target.search = window.location.search;
        target.hash = window.location.hash;
        window.location.assign(target.href);
      }}, true);

      document.addEventListener('DOMContentLoaded', () => {{
        localizeTree(document.body);
        if (isChinese) {{
          new MutationObserver((mutations) => {{
            mutations.forEach((mutation) => mutation.addedNodes.forEach((node) => {{
              if (node.nodeType === Node.ELEMENT_NODE) localizeTree(node);
            }}));
          }}).observe(document.body, {{ childList: true, subtree: true }});
        }}
      }});
    }})();
  </script>'''


def localize_page(spec: PageSpec, language: str) -> str:
    markup = spec.source.read_text(encoding="utf-8")
    markup = re.sub(
        r'\s*<script\s+id="static-language-routing">.*?</script>\s*',
        "\n",
        markup,
        flags=re.IGNORECASE | re.DOTALL,
    )
    title = spec.title_zh if language == "zh-Hans" else spec.title_en
    description = spec.description_zh if language == "zh-Hans" else spec.description_en
    canonical = spec.chinese_url if language == "zh-Hans" else spec.english_url

    markup = re.sub(r'<html\b[^>]*\blang="[^"]*"', f'<html lang="{language}"', markup, count=1, flags=re.IGNORECASE)
    markup = localize_visible_text(markup, language)
    markup = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", markup, count=1, flags=re.IGNORECASE | re.DOTALL)
    markup = set_meta(markup, "name", "description", description)
    markup = set_meta(markup, "property", "og:title", title)
    markup = set_meta(markup, "property", "og:description", description)
    markup = set_meta(markup, "property", "og:url", canonical)
    markup = set_meta(markup, "property", "og:locale", "zh_CN" if language == "zh-Hans" else "en_US")
    markup = set_meta(markup, "property", "og:locale:alternate", "en_US" if language == "zh-Hans" else "zh_CN")
    markup = set_meta(markup, "name", "twitter:title", title)
    markup = set_meta(markup, "name", "twitter:description", description)
    markup = set_page_links(markup, canonical, spec.english_url, spec.chinese_url)
    markup = normalize_resource_urls(markup)
    if language == "zh-Hans":
        markup = chinese_internal_links(markup)
    markup = rewrite_json_ld(markup, language, title, description)
    markup = markup.replace("</head>", f"{language_routing_script(language)}\n</head>", 1)
    return markup


def write_sitemap(specs: list[PageSpec]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for spec in specs:
        for current_url in (spec.english_url, spec.chinese_url):
            lines.extend(
                [
                    "  <url>",
                    f"    <loc>{xml_escape(current_url)}</loc>",
                    f"    <lastmod>{xml_escape(spec.last_modified)}</lastmod>",
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{xml_escape(spec.english_url)}" />',
                    f'    <xhtml:link rel="alternate" hreflang="zh-Hans" href="{xml_escape(spec.chinese_url)}" />',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xml_escape(spec.english_url)}" />',
                    "  </url>",
                ]
            )
    lines.append("</urlset>")
    sitemap = "\n".join(lines) + "\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def validate_output(specs: list[PageSpec]) -> None:
    issues = []
    for spec in specs:
        variants = (
            (spec.source, "en", spec.english_url),
            (spec.chinese_output, "zh-Hans", spec.chinese_url),
        )
        for output, language, canonical in variants:
            if not output.exists():
                issues.append(f"{output.relative_to(ROOT)}: missing output")
                continue
            markup = output.read_text(encoding="utf-8")
            required = (
                f'<html lang="{language}"',
                f'<link rel="canonical" href="{canonical}"',
                f'<link rel="alternate" hreflang="en" href="{spec.english_url}"',
                f'<link rel="alternate" hreflang="zh-Hans" href="{spec.chinese_url}"',
                f'<link rel="alternate" hreflang="x-default" href="{spec.english_url}"',
                f'<meta property="og:url" content="{canonical}"',
                '<script id="static-language-routing">',
            )
            for value in required:
                if value not in markup:
                    issues.append(f"{output.relative_to(ROOT)}: missing {value}")
            if markup.count('<script id="static-language-routing">') != 1:
                issues.append(f"{output.relative_to(ROOT)}: language routing script is not unique")
            if language == "zh-Hans" and re.search(
                r'\b(?:href|src)=["\'](?:\.\.?/)+(?:assets|src|data)/', markup
            ):
                issues.append(f"{output.relative_to(ROOT)}: contains a relative resource URL")

    sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
    if sitemap.count("<loc>") != len(specs) * 2:
        issues.append("dist/sitemap.xml: URL count does not match localized page count")
    if sitemap.count('hreflang="en"') != len(specs) * 2:
        issues.append("dist/sitemap.xml: English alternate count is incomplete")
    if sitemap.count('hreflang="zh-Hans"') != len(specs) * 2:
        issues.append("dist/sitemap.xml: Chinese alternate count is incomplete")
    if issues:
        raise SystemExit("Localized page validation failed:\n" + "\n".join(issues))


def main() -> None:
    if not DIST.exists():
        raise SystemExit("dist/ does not exist; run Vite build first")
    specs = page_specs()
    missing = [str(spec.source.relative_to(ROOT)) for spec in specs if not spec.source.exists()]
    if missing:
        raise SystemExit("Missing indexable page(s):\n" + "\n".join(missing))

    for spec in specs:
        english_markup = localize_page(spec, "en")
        chinese_markup = localize_page(spec, "zh-Hans")
        spec.source.write_text(english_markup, encoding="utf-8")
        spec.chinese_output.parent.mkdir(parents=True, exist_ok=True)
        spec.chinese_output.write_text(chinese_markup, encoding="utf-8")

    write_sitemap(specs)
    validate_output(specs)
    print(f"✅ Localized {len(specs)} English page(s) and {len(specs)} /zh-hans/ page(s)")
    print(f"✅ Generated bilingual sitemap with {len(specs) * 2} URL entries")


if __name__ == "__main__":
    main()
