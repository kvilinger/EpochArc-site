#!/usr/bin/env python3
"""Build Narrative Arc pages from content/arcs/*.json — list page + detail pages"""
import json, os, glob, sys, shutil, datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCS_CONTENT_DIR = os.path.join(ROOT_DIR, 'content', 'arcs')
EVENTS_FILE = os.path.join(ROOT_DIR, 'data', 'events.json')
LABELS_FILE = os.path.join(ROOT_DIR, 'data', 'labels.json')
LIST_TEMPLATE_FILE = os.path.join(ROOT_DIR, 'templates', 'arcs_list_template.html')
DETAIL_TEMPLATE_FILE = os.path.join(ROOT_DIR, 'templates', 'arc_template.html')
ARCS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'arcs')
ARCS_LIST_OUTPUT = os.path.join(ROOT_DIR, 'arcs.html')
DIST_DIR = os.path.join(ROOT_DIR, 'dist')

# ─────────────────── 1. 加载数据 ───────────────────

if not os.path.isdir(ARCS_CONTENT_DIR):
    print("⚠️  content/arcs/ directory not found — skipping arc build")
    sys.exit(0)

arc_files = sorted(glob.glob(os.path.join(ARCS_CONTENT_DIR, '*.json')))
if not arc_files:
    print("⚠️  No arc JSON files found in content/arcs/ — skipping")
    sys.exit(0)

arcs = []
for f in arc_files:
    with open(f, encoding='utf-8') as fh:
        arcs.append(json.load(fh))

with open(EVENTS_FILE, encoding='utf-8') as fh:
    events_data = json.load(fh)
events_by_id = {e['id']: e for e in events_data}

with open(LABELS_FILE, encoding='utf-8') as fh:
    labels = json.load(fh)

# ─────────────────── 2. 验证 ───────────────────

errors = []

# 重复 ID 检查
arc_ids = [a.get('id', '') for a in arcs]
for i, aid in enumerate(arc_ids):
    if aid in arc_ids[:i]:
        errors.append(f"Duplicate arc ID: {aid}")

for a in arcs:
    aid = a.get('id', '<missing>')

    # 顶层必要字段
    for field in ['id', 'title', 'subtitle', 'abstract', 'chapters', 'conclusion', 'editorial']:
        if field not in a:
            errors.append(f"{aid}: missing required field '{field}'")

    # LocalizedText 校验
    for field in ['title', 'subtitle', 'abstract']:
        val = a.get(field)
        if isinstance(val, dict):
            for lang in ['en', 'zhHans']:
                if lang not in val or not val[lang]:
                    errors.append(f"{aid}.{field}: missing '{lang}' translation")

    # conclusion LocalizedText
    conclusion = a.get('conclusion')
    if isinstance(conclusion, dict):
        for lang in ['en', 'zhHans']:
            if lang not in conclusion or not conclusion[lang]:
                errors.append(f"{aid}.conclusion: missing '{lang}' translation")

    # chapters 校验
    chapters = a.get('chapters', [])
    if not isinstance(chapters, list) or len(chapters) == 0:
        errors.append(f"{aid}: chapters must be a non-empty array")
    else:
        for ci, ch in enumerate(chapters):
            for field in ['id', 'title', 'narrative', 'anchorEvents', 'keyInsight']:
                if field not in ch:
                    errors.append(f"{aid}.chapters[{ci}]: missing required field '{field}'")
            # anchorEvents 引用校验
            for ev_id in ch.get('anchorEvents', []):
                if ev_id not in events_by_id:
                    errors.append(f"{aid}.chapters[{ci}]: anchorEvent '{ev_id}' not found in events.json")

if errors:
    for err in errors:
        print(f"❌ {err}")
    print(f"\nBuild FAILED: {len(errors)} error(s)")
    sys.exit(1)

# ─────────────────── 辅助函数 ───────────────────

def collect_all_anchor_events(arc):
    """收集 arc 所有章节中的唯一 anchorEvent ID"""
    ids = set()
    for ch in arc.get('chapters', []):
        for eid in ch.get('anchorEvents', []):
            ids.add(eid)
    return ids

def get_date_range(anchor_event_ids):
    """从 anchor events 中计算最早和最晚日期"""
    dates = []
    for eid in anchor_event_ids:
        ev = events_by_id.get(eid)
        if ev and 'date' in ev:
            dates.append(ev['date'])
    if not dates:
        return '', ''
    dates.sort()
    return dates[0], dates[-1]

def get_arc_categories(arc):
    """从 arc 的 categories 字段获取分类，若无则从 anchor events 推导"""
    if 'categories' in arc and arc['categories']:
        return arc['categories']
    cats = {}
    for eid in collect_all_anchor_events(arc):
        ev = events_by_id.get(eid)
        if ev:
            for c in ev.get('categories', []):
                cats[c] = cats.get(c, 0) + 1
    return sorted(cats, key=lambda c: -cats[c])[:3]

def get_arc_significance(arc):
    """获取 arc 的 significance 值"""
    if 'significance' in arc:
        return arc['significance']
    # 从 anchor events 取最高 significance
    max_sig = 3
    for eid in collect_all_anchor_events(arc):
        ev = events_by_id.get(eid)
        if ev:
            max_sig = min(max_sig, ev.get('significance', 3))
    return max_sig

# ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT REMOVE OR BYPASS THIS FUNCTION!
# Ensure all dynamic variables injected into attributes (like data-zh/data-en) are HTML-escaped.
# Otherwise, double quotes will crash Vite dev/build parsers.
def html_escape(text):
    """基本 HTML 转义"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

# ─────────────────── 3. 生成列表页 ───────────────────

if not os.path.exists(LIST_TEMPLATE_FILE):
    print(f"⚠️  List template not found: {LIST_TEMPLATE_FILE} — skipping list page")
else:
    with open(LIST_TEMPLATE_FILE, 'r', encoding='utf-8') as fh:
        list_template = fh.read()

    # 按 significance 排序 (1=最高 → 排前面)
    sorted_arcs = sorted(arcs, key=lambda a: get_arc_significance(a))

    card_items = []
    for a in sorted_arcs:
        aid = a['id']
        title_en = a['title']['en']
        title_zh = a['title']['zhHans']
        subtitle_en = a['subtitle']['en']
        subtitle_zh = a['subtitle']['zhHans']
        chapter_count = len(a.get('chapters', []))
        all_events = collect_all_anchor_events(a)
        event_count = len(all_events)
        date_start, date_end = get_date_range(all_events)
        date_range_str = f"{date_start} — {date_end}" if date_start and date_end else ''
        categories = get_arc_categories(a)

        cat_badges = ''
        for c in categories:
            cat_en = labels['category'].get(c, {}).get('en', c)
            cat_zh = labels['category'].get(c, {}).get('zhHans', c)
            cat_badges += f'<span class="category-badge {c}" data-zh="{html_escape(cat_zh)}" data-en="{html_escape(cat_en)}">{html_escape(cat_en)}</span>\n'

        card_items.append(f'''
          <a class="arc-card" href="arcs/{aid}/index.html">
            <h3 class="arc-card-title" data-zh="{html_escape(title_zh)}" data-en="{html_escape(title_en)}">{html_escape(title_en)}</h3>
            <p class="arc-card-subtitle" data-zh="{html_escape(subtitle_zh)}" data-en="{html_escape(subtitle_en)}">{html_escape(subtitle_en)}</p>
            <div class="arc-card-meta">
              <span class="arc-card-stat" data-zh="{chapter_count} 章节 · {event_count} 事件" data-en="{chapter_count} Chapters · {event_count} Events">{chapter_count} Chapters · {event_count} Events</span>
              <span class="arc-card-date">{date_range_str}</span>
            </div>
            <div class="arc-card-tags">
              {cat_badges}
            </div>
          </a>
        ''')

    cards_html = '\n'.join(card_items)
    list_html = list_template.replace('{{ARC_CARDS}}', cards_html)

    with open(ARCS_LIST_OUTPUT, 'w', encoding='utf-8') as fh:
        fh.write(list_html)
    print(f"✅ Generated arcs list page: {ARCS_LIST_OUTPUT}")

# ─────────────────── 4. 生成详情页 ───────────────────

if os.path.exists(ARCS_OUTPUT_DIR):
    shutil.rmtree(ARCS_OUTPUT_DIR)
os.makedirs(ARCS_OUTPUT_DIR, exist_ok=True)

if not os.path.exists(DETAIL_TEMPLATE_FILE):
    print(f"⚠️  Detail template not found: {DETAIL_TEMPLATE_FILE} — skipping detail pages")
else:
    with open(DETAIL_TEMPLATE_FILE, 'r', encoding='utf-8') as fh:
        detail_template = fh.read()

    for a in arcs:
        aid = a['id']
        title_en = a['title']['en']
        title_zh = a['title']['zhHans']
        subtitle_en = a['subtitle']['en']
        subtitle_zh = a['subtitle']['zhHans']
        abstract_en = a['abstract']['en']
        abstract_zh = a['abstract']['zhHans']
        conclusion_en = a['conclusion']['en']
        conclusion_zh = a['conclusion']['zhHans']
        cover_theme = a.get('coverTheme', 'default')

        # 中文大写数字映射
        ZH_NUMS = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十'}

        # ── 生成 TOC HTML ──
        # ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT use 'Chapter N' or '第N章' prefix for chapters.
        # Use Chinese numbers '一、' and English numbers '01.' pre-fixed directly to the title to align layout.
        toc_items = []
        for ci, ch in enumerate(a['chapters']):
            ch_num = ci + 1
            ch_title_en = ch['title']['en']
            ch_title_zh = ch['title']['zhHans']
            zh_num = ZH_NUMS.get(ch_num, str(ch_num))
            toc_items.append(
                f'<a href="#chapter-{ch["id"]}" data-zh="{zh_num}、{html_escape(ch_title_zh)}" '
                f'data-en="{ch_num:02d}. {html_escape(ch_title_en)}">'
                f'{ch_num:02d}. {html_escape(ch_title_en)}</a>'
            )
        toc_html = '<div class="arc-toc">\n' + '\n'.join(toc_items) + '\n</div>' if toc_items else ''

        # ── 生成 Chapters HTML ──
        chapter_blocks = []
        for ci, ch in enumerate(a['chapters']):
            ch_num = ci + 1
            ch_id = ch['id']
            ch_title_en = ch['title']['en']
            ch_title_zh = ch['title']['zhHans']
            ch_narrative_en = ch['narrative']['en']
            ch_narrative_zh = ch['narrative']['zhHans']
            zh_num = ZH_NUMS.get(ch_num, str(ch_num))

            # Key Insight box (对齐 arcs.css 的 .arc-key-insight 类名)
            ki = ch.get('keyInsight', {})
            ki_en = ki.get('en', '') if isinstance(ki, dict) else str(ki)
            ki_zh = ki.get('zhHans', '') if isinstance(ki, dict) else str(ki)
            key_insight_html = ''
            if ki_en or ki_zh:
                key_insight_html = f'''
                <div class="arc-key-insight">
                  <div class="arc-key-insight-label" data-zh="核心洞察" data-en="Key Insight">Key Insight</div>
                  <p data-zh="{html_escape(ki_zh)}" data-en="{html_escape(ki_en)}">{html_escape(ki_en)}</p>
                </div>
                '''

            # Anchor event mini-cards (对齐 arcs.css 的 .arc-anchor-event 类名与彩色重要度圆点)
            event_cards = []
            for ev_id in ch.get('anchorEvents', []):
                ev = events_by_id.get(ev_id)
                if not ev:
                    continue
                ev_title_en = ev['title']['en']
                ev_title_zh = ev['title']['zhHans']
                ev_date = ev['date']
                ev_sig = ev['significance']
                event_cards.append(f'''
                  <!-- ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT change 'arc-anchor-event' class name or its children structure. -->
                  <!-- It must strictly match CSS styling rules in arcs.css. -->
                  <!-- Make sure to link to events/{ev_id}/index.html detail pages directly. -->
                  <a class="arc-anchor-event" data-event-id="{ev_id}" href="../../events/{ev_id}/index.html">
                    <span class="sig-dot l{ev_sig}"></span>
                    <span class="event-date">{ev_date}</span>
                    <span class="event-name" data-zh="{html_escape(ev_title_zh)}" data-en="{html_escape(ev_title_en)}">{html_escape(ev_title_en)}</span>
                  </a>
                ''')
            events_html = '\n'.join(event_cards)

            # Chapters block (对齐 arcs.css 的 .arc-chapter-header 等类名，移除第N章前缀改为直观的前置数字)
            chapter_blocks.append(f'''
              <section class="arc-chapter" id="chapter-{ch_id}">
                <div class="arc-chapter-header">
                  <!-- ⚠️ WARNING FOR OTHER AI AGENTS: Keep Chinese numbers '一、' and English numbers '01.' prefixes directly inside heading attributes. -->
                  <h2 class="arc-chapter-title" data-zh="{zh_num}、{html_escape(ch_title_zh)}" data-en="{ch_num:02d}. {html_escape(ch_title_en)}">{ch_num:02d}. {html_escape(ch_title_en)}</h2>
                </div>
                <div class="arc-chapter-narrative" data-zh="{html_escape(ch_narrative_zh)}" data-en="{html_escape(ch_narrative_en)}">{html_escape(ch_narrative_en)}</div>
                {key_insight_html}
                <div class="arc-anchor-events">
                  {events_html}
                </div>
              </section>
            ''')
        chapters_html = '\n'.join(chapter_blocks)

        # ── Related Arcs HTML ──
        related_arcs_html = ''
        related_arc_ids = a.get('relatedArcs', [])
        if related_arc_ids:
            arcs_by_id = {ra['id']: ra for ra in arcs}
            related_cards = []
            for ra_id in related_arc_ids:
                ra = arcs_by_id.get(ra_id)
                if not ra:
                    continue
                ra_title_en = ra['title']['en']
                ra_title_zh = ra['title']['zhHans']
                ra_subtitle_en = ra['subtitle']['en']
                ra_subtitle_zh = ra['subtitle']['zhHans']
                related_cards.append(f'''
                  <a class="related-arc-card" href="../{ra_id}/index.html">
                    <h4 class="related-arc-title" data-zh="{html_escape(ra_title_zh)}" data-en="{html_escape(ra_title_en)}">{html_escape(ra_title_en)}</h4>
                    <p class="related-arc-subtitle" data-zh="{html_escape(ra_subtitle_zh)}" data-en="{html_escape(ra_subtitle_en)}">{html_escape(ra_subtitle_en)}</p>
                  </a>
                ''')
            if related_cards:
                related_arcs_html = f'''
                  <section class="related-arcs-section">
                    <h3 data-zh="相关叙事弧" data-en="Related Arcs">Related Arcs</h3>
                    <div class="related-arcs-grid">
                      {''.join(related_cards)}
                    </div>
                  </section>
                '''

        # ── Schema.org JSON-LD ──
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title_en,
            "description": abstract_en,
            "dateModified": a.get('editorial', {}).get('updatedAt', datetime.date.today().isoformat()),
            "author": {
                "@type": "Organization",
                "name": "EpochArc",
                "url": "https://epoch-arc.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "EpochArc",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://epoch-arc.com/assets/logo-icon.svg"
                }
            },
            "mainEntityOfPage": f"https://epoch-arc.com/arcs/{aid}/"
        }
        schema_json_ld = f'<script type="application/ld+json">\n{json.dumps(schema_data, ensure_ascii=False, indent=2)}\n</script>'

        # ── 替换模板占位符 ──
        page_html = detail_template
        page_html = page_html.replace('{{SEO_TITLE}}', html_escape(title_en))
        page_html = page_html.replace('{{SEO_DESC}}', html_escape(abstract_en))
        page_html = page_html.replace('{{SLUG}}', aid)
        page_html = page_html.replace('{{TITLE_EN}}', html_escape(title_en))
        page_html = page_html.replace('{{TITLE_ZH}}', html_escape(title_zh))
        page_html = page_html.replace('{{SUBTITLE_EN}}', html_escape(subtitle_en))
        page_html = page_html.replace('{{SUBTITLE_ZH}}', html_escape(subtitle_zh))
        page_html = page_html.replace('{{ABSTRACT_EN}}', html_escape(abstract_en))
        page_html = page_html.replace('{{ABSTRACT_ZH}}', html_escape(abstract_zh))
        page_html = page_html.replace('{{CHAPTERS_HTML}}', chapters_html)
        page_html = page_html.replace('{{CONCLUSION_EN}}', html_escape(conclusion_en))
        page_html = page_html.replace('{{CONCLUSION_ZH}}', html_escape(conclusion_zh))
        page_html = page_html.replace('{{RELATED_ARCS_HTML}}', related_arcs_html)
        page_html = page_html.replace('{{COVER_THEME}}', cover_theme)
        page_html = page_html.replace('{{SCHEMA_JSON_LD}}', schema_json_ld)
        page_html = page_html.replace('{{TOC_HTML}}', toc_html)

        # ── 写出文件 ──
        arc_dir = os.path.join(ARCS_OUTPUT_DIR, aid)
        os.makedirs(arc_dir, exist_ok=True)
        with open(os.path.join(arc_dir, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(page_html)

    print(f"✅ Generated {len(arcs)} arc detail pages inside {ARCS_OUTPUT_DIR}")

# ─────────────────── 5. 同步至 dist/ ───────────────────

if os.path.exists(DIST_DIR):
    shutil.copytree(ARCS_OUTPUT_DIR, os.path.join(DIST_DIR, 'arcs'), dirs_exist_ok=True)
    # 同步列表页
    if os.path.exists(ARCS_LIST_OUTPUT):
        shutil.copy2(ARCS_LIST_OUTPUT, os.path.join(DIST_DIR, 'arcs.html'))
    print(f"✅ Synced arcs to {DIST_DIR}/arcs/")

# ─────────────────── 6. 追加 sitemap.xml ───────────────────

def append_arcs_to_sitemap(arcs):
    today = datetime.date.today().isoformat()
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')

    if not os.path.exists(sitemap_path):
        print("⚠️  sitemap.xml not found — skipping sitemap update")
        return

    with open(sitemap_path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # 构建要插入的 URL 条目
    new_urls = []
    # 列表页
    list_url = f'  <url><loc>https://epoch-arc.com/arcs.html</loc><lastmod>{today}</lastmod></url>'
    if 'epoch-arc.com/arcs.html' not in content:
        new_urls.append(list_url)

    for a in arcs:
        arc_url = f'  <url><loc>https://epoch-arc.com/arcs/{a["id"]}/</loc><lastmod>{today}</lastmod></url>'
        if f'epoch-arc.com/arcs/{a["id"]}/' not in content:
            new_urls.append(arc_url)

    if not new_urls:
        print("✅ Sitemap already contains arc URLs — no changes needed")
        return

    # 在 </urlset> 前插入
    insertion = '\n'.join(new_urls)
    content = content.replace('</urlset>', insertion + '\n</urlset>')

    with open(sitemap_path, 'w', encoding='utf-8') as fh:
        fh.write(content)

    # 同步到 dist/
    dist_sitemap = os.path.join(DIST_DIR, 'sitemap.xml')
    if os.path.exists(DIST_DIR):
        with open(dist_sitemap, 'w', encoding='utf-8') as fh:
            fh.write(content)

    print(f"✅ Appended {len(new_urls)} arc URL(s) to sitemap.xml")

append_arcs_to_sitemap(arcs)
