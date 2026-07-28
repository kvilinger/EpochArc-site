#!/usr/bin/env python3
"""Build the Possible Directions index and detail pages."""

import datetime
import json
import os
import re
import shutil
from html import escape


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'directions')
LIST_OUTPUT = os.path.join(ROOT_DIR, 'directions.html')
DIST_DIR = os.path.join(ROOT_DIR, 'dist')


def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as file_handle:
        return json.load(file_handle)


def load_template(filename):
    with open(os.path.join(TEMPLATE_DIR, filename), 'r', encoding='utf-8') as file_handle:
        return file_handle.read()


def clean(value):
    """Keep generated UI copy compatible with the site's punctuation rules."""
    return re.sub(r'\s*[—–‑]+\s*', ' - ', str(value or '')).strip()


def html(value):
    return escape(clean(value), quote=True)


def localized(record):
    if not isinstance(record, dict):
        return clean(record), clean(record)
    return clean(record.get('en', '')), clean(record.get('zhHans', record.get('zh', record.get('en', ''))))


def localized_element(tag, record, class_name='', attributes=''):
    en, zh = localized(record)
    class_attr = f' class="{class_name}"' if class_name else ''
    extra = f' {attributes}' if attributes else ''
    return f'<{tag}{class_attr}{extra} data-zh="{html(zh)}" data-en="{html(en)}">{html(en)}</{tag}>'


def label_pair(en, zh):
    return f'<span data-zh="{html(zh)}" data-en="{html(en)}">{html(en)}</span>'


TYPE_LABELS = {
    'capability': ('Capability', '能力'),
    'product': ('Product', '产品'),
    'science': ('Science', '科学'),
    'policy': ('Policy', '政策'),
    'safety': ('Safety', '安全'),
}

SIGNAL_KIND_LABELS = {
    'benchmark': ('Benchmark', '基准'),
    'deployment': ('Deployment', '部署'),
    'incident': ('Incident', '事件'),
    'infrastructure': ('Infrastructure', '基础设施'),
    'market': ('Market', '市场'),
    'product': ('Product', '产品'),
    'research': ('Research', '研究'),
    'workflow': ('Workflow', '工作流'),
}

CADENCE_LABELS = {
    'monthly': ('Monthly', '每月'),
    'quarterly': ('Quarterly', '每季度'),
    'semiannual': ('Twice yearly', '每半年'),
    'annual': ('Yearly', '每年'),
}

CONFIDENCE_LABELS = {
    'low': ('Low', '低'),
    'medium': ('Medium', '中'),
    'high': ('High', '高'),
}

EVIDENCE_STRENGTH_LABELS = {
    'low': ('Developing', '形成中'),
    'medium': ('Moderate', '中等'),
    'high': ('Strong', '较强'),
}


def pair_for(mapping, key):
    return mapping.get(key, (str(key).replace('_', ' ').title(), str(key)))


def expected_window(forecast):
    window = forecast.get('expectedWindow', {})
    start = clean(window.get('start', ''))
    end = clean(window.get('end', ''))
    return f'{start}-{end}' if end and end != start else start


def source_link(source, text=None):
    url = html(source.get('url', '#'))
    label = html(text or source.get('title', source.get('id', 'Source')))
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'


def build_list_rows(forecasts):
    rows = []
    for forecast in forecasts:
        slug = html(forecast['slug'])
        type_en, type_zh = pair_for(TYPE_LABELS, forecast.get('forecastType'))
        signals = forecast.get('signals', [])
        observed_count = sum(signal.get('status') == 'observed' for signal in signals)
        confidence = forecast.get('confidence', {})
        confidence_en, confidence_zh = pair_for(EVIDENCE_STRENGTH_LABELS, confidence.get('level'))
        evidence_grade = clean(confidence.get('evidenceGrade', ''))
        row = f'''
      <a class="direction-row-card" href="/directions/{slug}/">
        <div class="direction-row-main">
          <span class="direction-row-type" data-zh="{html(type_zh)}" data-en="{html(type_en)}">{html(type_en)}</span>
          {localized_element('h2', forecast.get('title', {}))}
          {localized_element('p', forecast.get('thesis', {}), 'direction-row-thesis')}
        </div>
        <div class="direction-row-metric">
          <span class="direction-row-mobile-label" data-zh="预期窗口" data-en="Expected window">Expected window</span>
          <strong>{html(expected_window(forecast))}</strong>
        </div>
        <div class="direction-row-metric">
          <span class="direction-row-mobile-label" data-zh="已观察信号" data-en="Observed signals">Observed signals</span>
          <strong>{observed_count}</strong>
        </div>
        <div class="direction-row-metric direction-row-evidence">
          <span class="direction-row-mobile-label" data-zh="证据强度" data-en="Evidence strength">Evidence strength</span>
          <strong data-zh="{html(evidence_grade)} 级 · {html(confidence_zh)}" data-en="Grade {html(evidence_grade)} · {html(confidence_en)}">Grade {html(evidence_grade)} · {html(confidence_en)}</strong>
        </div>
        <div class="direction-row-cta" data-zh="查看详情 →" data-en="View details →">View details →</div>
      </a>'''
        rows.append(row)
    return ''.join(rows)


def build_signal(signal, number, events_by_id, sources_by_id):
    kind = clean(signal.get('kind', 'signal')).replace('_', ' ')
    status = clean(signal.get('status', 'observed')).replace('_', ' ')
    kind_en, kind_zh = pair_for(SIGNAL_KIND_LABELS, kind)
    status_en = status.title()
    status_zh = '已观察' if status == 'observed' else status
    event_links = []
    for event_id in signal.get('eventIds', []):
        event = events_by_id.get(event_id)
        if event:
            title_en, title_zh = localized(event.get('title', {}))
            event_links.append(
                f'<a href="/events/{html(event.get("slug", event_id))}/" data-zh="{html(title_zh)}" data-en="{html(title_en)}">{html(title_en)}</a>'
            )
    source_items = []
    for source_id in signal.get('sourceIds', []):
        source = sources_by_id.get(source_id)
        if source:
            source_items.append(f'<li>{source_link(source)}</li>')

    related_html = ''
    if event_links:
        related_html = f'''
            <div class="signal-related-events">
              <span data-zh="相关事件" data-en="Related events">Related events</span>
              <div class="signal-event-links">{''.join(event_links)}</div>
            </div>'''

    source_details = ''
    if source_items:
        source_count = len(source_items)
        source_details = f'''
          <details class="signal-sources">
            <summary>
              <span class="source-count-label" data-zh="{source_count} 个来源" data-en="{source_count} sources">{source_count} sources</span>
              <span class="source-close-label" data-zh="收起来源" data-en="Hide sources">Hide sources</span>
            </summary>
            <ul>{''.join(source_items)}</ul>
          </details>'''

    return f'''
        <li class="signal-item">
          <div class="signal-marker">{number:02d}</div>
          <div class="signal-body">
            <div class="direction-signal-meta">
              <span data-zh="{html(status_zh)}" data-en="{html(status_en)}">{html(status_en)}</span>
              <span data-zh="{html(kind_zh)}" data-en="{html(kind_en)}">{html(kind_en)}</span>
            </div>
            {localized_element('h3', signal.get('label', {}))}
            {localized_element('p', signal.get('summary', {}))}
            {related_html}
          </div>
          {source_details}
        </li>'''


def build_source_registry(forecast, sources_by_id):
    ids = []
    for source_ref in forecast.get('sources', []):
        source_id = source_ref.get('sourceId')
        if source_id and source_id not in ids:
            ids.append(source_id)
    for signal in forecast.get('signals', []):
        for source_id in signal.get('sourceIds', []):
            if source_id not in ids:
                ids.append(source_id)
    for source_id in forecast.get('consensusBasis', {}).get('sourceIds', []):
        if source_id not in ids:
            ids.append(source_id)

    items = []
    for index, source_id in enumerate(ids, start=1):
        source = sources_by_id.get(source_id)
        if not source:
            continue
        items.append(f'''
          <li>
            <span class="direction-source-index">{index:02d}</span>
            <span class="direction-source-title">{html(source.get('title', source_id))}</span>
            {source_link(source, 'Open source')}
          </li>''')
    return ''.join(items)


def build_related_events(forecast, events_by_id):
    links = []
    for event_id in forecast.get('relatedEvents', []):
        event = events_by_id.get(event_id)
        if not event:
            continue
        en, zh = localized(event.get('title', {}))
        links.append(f'<a href="/events/{html(event.get("slug", event_id))}/" data-zh="{html(zh)}" data-en="{html(en)}">{html(en)}</a>')
    return ''.join(links)


def build_detail_content(forecast, events_by_id, sources_by_id):
    type_en, type_zh = pair_for(TYPE_LABELS, forecast.get('forecastType'))
    confidence = forecast.get('confidence', {})
    confidence_en, confidence_zh = pair_for(CONFIDENCE_LABELS, confidence.get('level'))
    signals = forecast.get('signals', [])
    observed_count = sum(signal.get('status') == 'observed' for signal in signals)
    source_ids = {
        source_ref.get('sourceId')
        for source_ref in forecast.get('sources', [])
        if source_ref.get('sourceId')
    }
    for signal in signals:
        source_ids.update(source_id for source_id in signal.get('sourceIds', []) if source_id)
    source_ids.update(source_id for source_id in forecast.get('consensusBasis', {}).get('sourceIds', []) if source_id)
    signal_html = ''.join(build_signal(signal, index, events_by_id, sources_by_id) for index, signal in enumerate(signals, start=1))
    rationale = forecast.get('rationale', {})
    consensus = forecast.get('consensusBasis', {})
    open_questions = ''.join(localized_element('li', question) for question in rationale.get('openQuestions', []))

    return f'''
    <header class="page-header direction-hero">
      <div class="direction-status-line">
        <span data-zh="观察中" data-en="Monitoring">Monitoring</span>
        <span data-zh="{html(type_zh)}" data-en="{html(type_en)}">{html(type_en)}</span>
      </div>
      {localized_element('h1', forecast.get('title', {}), 'page-title')}
      {localized_element('p', forecast.get('thesis', {}), 'page-lead direction-thesis')}
    </header>

    <div class="page-layout direction-detail-layout">
      <article class="page-main direction-main">
        <section class="direction-narrative-grid">
          <div class="direction-prose-block" id="direction-baseline" data-toc-section>
            <span class="direction-section-label" data-zh="当前基线" data-en="Current baseline">Current baseline</span>
            <h2 data-zh="已经成立的部分" data-en="What is already true">What is already true</h2>
            {localized_element('p', rationale.get('currentBaseline', {}))}
          </div>
          <div class="direction-prose-block" id="direction-judgment" data-toc-section>
            <span class="direction-section-label" data-zh="核心判断" data-en="Core judgment">Core judgment</span>
            <h2 data-zh="为何值得持续观察" data-en="Why this direction matters">Why this direction matters</h2>
            {localized_element('p', rationale.get('whyThisDirection', {}))}
          </div>
        </section>

        <section class="direction-evidence" id="direction-signals" data-toc-section>
          <header class="direction-evidence-head">
            <span class="direction-section-label" data-zh="证据轨迹" data-en="Evidence trail">Evidence trail</span>
            <h2 data-zh="已观察信号" data-en="Observed signals">Observed signals</h2>
            <p data-zh="每个信号都连接到站内历史事件和公开来源，后续评审会继续增加、修订或降级这些信号。" data-en="Each signal links back to historical events and public sources. Later reviews may add, revise, or downgrade it.">Each signal links back to historical events and public sources. Later reviews may add, revise, or downgrade it.</p>
          </header>
          <ol class="signal-track">{signal_html}</ol>
        </section>

        <section class="direction-review-grid">
          <div class="direction-counter" id="direction-counter" data-toc-section>
            <span class="direction-section-label" data-zh="反向条件" data-en="Counter-signal">Counter-signal</span>
            <h2 data-zh="什么会削弱这个方向" data-en="What would weaken this direction">What would weaken this direction</h2>
            {localized_element('p', rationale.get('counterSignal', {}))}
          </div>
          <div class="direction-consensus" id="direction-consensus" data-toc-section>
            <span class="direction-consensus-badge">{html(consensus.get('resolutionMode', 'monitor_only').replace('_', ' '))}</span>
            <span class="direction-section-label" data-zh="共识基础" data-en="Consensus basis">Consensus basis</span>
            <h2 data-zh="为什么只做持续监测" data-en="Why this remains monitored">Why this remains monitored</h2>
            {localized_element('p', consensus.get('summary', {}))}
          </div>
        </section>

        <section class="direction-questions" id="direction-questions" data-toc-section>
          <span class="direction-section-label" data-zh="待复核问题" data-en="Questions to review">Questions to review</span>
          <h2 data-zh="开放问题" data-en="Open questions">Open questions</h2>
          <ol class="direction-question-list">{open_questions}</ol>
        </section>

        <section class="direction-references">
          <div class="direction-reference-block" id="direction-related" data-toc-section>
            <span class="direction-section-label" data-zh="上下文" data-en="Context">Context</span>
            <h2 data-zh="相关事件" data-en="Related events">Related events</h2>
            <div class="direction-related-events">{build_related_events(forecast, events_by_id)}</div>
          </div>
          <div class="direction-reference-block" id="direction-sources" data-toc-section>
            <span class="direction-section-label" data-zh="证据目录" data-en="Evidence registry">Evidence registry</span>
            <h2 data-zh="公开来源" data-en="Public sources">Public sources</h2>
            <ul class="direction-source-list">{build_source_registry(forecast, sources_by_id)}</ul>
          </div>
        </section>
      </article>

      <aside class="page-rail direction-sidebar" aria-label="Direction overview">
        <section class="rail-card">
          <h2 class="rail-card-title" data-zh="方向概览" data-en="Direction overview">方向概览</h2>
          <dl class="rail-facts direction-meta">
            <div><dt data-zh="预计窗口" data-en="Expected window">Expected window</dt><dd>{html(expected_window(forecast))}</dd></div>
            <div><dt data-zh="信心 / 证据" data-en="Confidence / evidence">Confidence / evidence</dt><dd data-zh="{html(confidence_zh)} / {html(confidence.get('evidenceGrade', ''))} 级" data-en="{html(confidence_en)} / Grade {html(confidence.get('evidenceGrade', ''))}">{html(confidence_en)} / Grade {html(confidence.get('evidenceGrade', ''))}</dd></div>
            <div><dt data-zh="已观察信号" data-en="Observed signals">Observed signals</dt><dd>{observed_count}</dd></div>
            <div><dt data-zh="公开来源" data-en="Public sources">Public sources</dt><dd>{len(source_ids)}</dd></div>
            <div><dt data-zh="上次复核" data-en="Last reviewed">Last reviewed</dt><dd>{html(forecast.get('lastReviewedAt', ''))}</dd></div>
          </dl>
        </section>
        <section class="rail-card rail-toc-card">
          <h2 class="rail-card-title" data-zh="本页目录" data-en="On this page">本页目录</h2>
          <nav class="rail-link-list" data-page-toc aria-label="On this page">
            <a href="#direction-baseline" data-zh="当前基线" data-en="Current baseline">Current baseline</a>
            <a href="#direction-judgment" data-zh="核心判断" data-en="Core judgment">Core judgment</a>
            <a href="#direction-signals" data-zh="已观察信号" data-en="Observed signals">Observed signals</a>
            <a href="#direction-counter" data-zh="反向条件" data-en="Counter-signal">Counter-signal</a>
            <a href="#direction-consensus" data-zh="共识基础" data-en="Consensus basis">Consensus basis</a>
            <a href="#direction-questions" data-zh="开放问题" data-en="Open questions">Open questions</a>
            <a href="#direction-related" data-zh="相关事件" data-en="Related events">Related events</a>
            <a href="#direction-sources" data-zh="公开来源" data-en="Public sources">Public sources</a>
          </nav>
        </section>
        <section class="rail-card">
          <h2 class="rail-card-title" data-zh="评审说明" data-en="Review note">评审说明</h2>
          <p class="direction-rail-note" data-zh="方向只表示持续监测，不代表确定性预测。判断依据统一记录在方法与来源页。" data-en="Directions are monitored, not treated as certain predictions. The shared evaluation rules live on Methodology & Sources.">方向只表示持续监测，不代表确定性预测。判断依据统一记录在方法与来源页。</p>
          <a class="direction-inline-link" href="/methods/#possible-directions" data-zh="查看方法与来源 →" data-en="Read methodology and sources →">查看方法与来源 →</a>
        </section>
      </aside>
    </div>'''


def schema_for(forecast):
    title_en, _ = localized(forecast.get('title', {}))
    thesis_en, _ = localized(forecast.get('thesis', {}))
    payload = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title_en,
        'description': thesis_en,
        'datePublished': forecast.get('createdAt'),
        'dateModified': forecast.get('updatedAt'),
        'mainEntityOfPage': f'https://epoch-arc.com/directions/{forecast["slug"]}/',
        'author': {'@type': 'Organization', 'name': 'EpochArc editorial'},
        'publisher': {'@type': 'Organization', 'name': 'EpochArc'},
        'inLanguage': ['en', 'zh-Hans'],
    }
    encoded = json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')
    return f'<script type="application/ld+json">{encoded}</script>'


def write_pages():
    forecasts = load_json('forecasts.json')
    events = load_json('events.json')
    sources = load_json('sources.json')
    events_by_id = {event['id']: event for event in events}
    sources_by_id = {source['id']: source for source in sources}

    list_page = load_template('directions_list_template.html').replace('{{DIRECTION_ROWS}}', build_list_rows(forecasts))
    with open(LIST_OUTPUT, 'w', encoding='utf-8') as file_handle:
        file_handle.write(list_page)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    detail_template = load_template('direction_template.html')
    for forecast in forecasts:
        title_en, _ = localized(forecast.get('title', {}))
        thesis_en, _ = localized(forecast.get('thesis', {}))
        page = detail_template
        replacements = {
            '{{SEO_TITLE}}': html(title_en),
            '{{SEO_DESC}}': html(thesis_en),
            '{{SLUG}}': html(forecast['slug']),
            '{{SCHEMA_JSON_LD}}': schema_for(forecast),
            '{{DIRECTION_CONTENT}}': build_detail_content(forecast, events_by_id, sources_by_id),
        }
        for placeholder, value in replacements.items():
            page = page.replace(placeholder, value)
        output_path = os.path.join(OUTPUT_DIR, forecast['slug'])
        os.makedirs(output_path, exist_ok=True)
        with open(os.path.join(output_path, 'index.html'), 'w', encoding='utf-8') as file_handle:
            file_handle.write(page)

    if os.path.exists(DIST_DIR):
        shutil.copy2(LIST_OUTPUT, os.path.join(DIST_DIR, 'directions.html'))
        shutil.copytree(OUTPUT_DIR, os.path.join(DIST_DIR, 'directions'), dirs_exist_ok=True)

    print(f'✅ Generated Possible Directions index and {len(forecasts)} detail pages')
    append_to_sitemap(forecasts)


def append_to_sitemap(forecasts):
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        print('⚠️  sitemap.xml not found; skipping direction URLs')
        return
    with open(sitemap_path, 'r', encoding='utf-8') as file_handle:
        content = file_handle.read()
    today = datetime.date.today().isoformat()
    urls = [('https://epoch-arc.com/directions', today)]
    urls.extend((f'https://epoch-arc.com/directions/{forecast["slug"]}/', forecast.get('updatedAt', today)) for forecast in forecasts)
    additions = []
    for url, lastmod in urls:
        if f'<loc>{url}</loc>' not in content:
            additions.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>')
    if additions:
        content = content.replace('</urlset>', '\n'.join(additions) + '\n</urlset>')
        with open(sitemap_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)
    if os.path.exists(DIST_DIR):
        with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)
    print(f'✅ Sitemap contains {len(urls)} Possible Directions URL(s)')


if __name__ == '__main__':
    write_pages()
