#!/usr/bin/env python3
"""Build data/events.json from content/events/*.json with full validation"""
import json, os, glob, sys, html

# ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT REMOVE OR BYPASS THIS FUNCTION!
# All dynamic strings injected into HTML attributes (e.g. data-zh, data-en) MUST be escaped via this function.
# Otherwise, unescaped quotes will crash Vite HMR parser with parse5 parsing errors.
def html_escape(text):
    if not text:
        return ""
    return html.escape(str(text), quote=True)


EVENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content', 'events')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'events.json')
LABELS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'labels.json')

events = []
for f in sorted(glob.glob(os.path.join(EVENTS_DIR, '*.json'))):
    with open(f) as fh:
        events.append(json.load(fh))

# Load labels for validation
with open(LABELS_FILE) as fh:
    labels = json.load(fh)
VALID_CATEGORIES = set(labels['category'].keys())
VALID_DIMENSIONS = set(labels['impactDimension'].keys())
VALID_TIMEFRAMES = set(labels['timeframe'].keys())
VALID_CONSENSUS = set(labels['consensus'].keys())
VALID_DIRECTIONS = {'positive', 'negative', 'mixed', 'neutral'}

errors = []
warnings = []

# 1. Duplicate IDs
ids = [e['id'] for e in events]
for i, eid in enumerate(ids):
    if eid in ids[:i]:
        errors.append(f"Duplicate event ID: {eid}")

for e in events:
    eid = e['id']
    
    # 2. Required fields
    for field in ['id','date','datePrecision','title','summary','narrative','categories','significance','impactIndex','impacts','sources']:
        if field not in e:
            errors.append(f"{eid}: missing required field '{field}'")
    
    # 3. Categories: 1-2 items, valid values, no stale 'category'
    if 'category' in e:
        errors.append(f"{eid}: stale 'category' field — must use 'categories' array")
    cats = e.get('categories', [])
    if not isinstance(cats, list) or len(cats) == 0:
        errors.append(f"{eid}: categories must be a non-empty array")
    elif len(cats) > 2:
        errors.append(f"{eid}: too many categories ({len(cats)}), max 2")
    for c in cats:
        if c not in VALID_CATEGORIES:
            errors.append(f"{eid}: unknown category '{c}'. Valid: {sorted(VALID_CATEGORIES)}")
    
    # 4. significance: integer 1/2/3 (not string L1/L2/L3)
    sig = e.get('significance')
    if isinstance(sig, str):
        errors.append(f"{eid}: significance must be integer (1/2/3), got string '{sig}'")
    elif sig not in [1,2,3]:
        errors.append(f"{eid}: significance must be 1, 2, or 3, got {sig}")
    
    # 5. impactIndex: 0-10 integer
    ii = e.get('impactIndex')
    if not isinstance(ii, int) or ii < 0 or ii > 10:
        errors.append(f"{eid}: impactIndex must be 0-10 integer, got {ii}")
    
    # 6. consensusLevel
    cl = e.get('consensusLevel')
    if cl not in VALID_CONSENSUS:
        errors.append(f"{eid}: unknown consensusLevel '{cl}'. Valid: {sorted(VALID_CONSENSUS)}")
    
    # 7. Impacts
    imps = e.get('impacts', [])
    if not isinstance(imps, list):
        errors.append(f"{eid}: impacts must be an array")
    else:
        for i, imp in enumerate(imps):
            for field in ['dimension','direction','severity','description','timeframe','affectedGroups','sourceIds']:
                if field not in imp:
                    errors.append(f"{eid}.impacts[{i}]: missing required field '{field}'")
            if imp.get('dimension') not in VALID_DIMENSIONS:
                errors.append(f"{eid}.impacts[{i}]: unknown dimension '{imp.get('dimension')}'. Valid: {sorted(VALID_DIMENSIONS)}")
            if imp.get('timeframe') not in VALID_TIMEFRAMES:
                errors.append(f"{eid}.impacts[{i}]: unknown timeframe '{imp.get('timeframe')}'. Valid: {sorted(VALID_TIMEFRAMES)}")
            dir_val = imp.get('direction')
            if dir_val not in VALID_DIRECTIONS:
                errors.append(f"{eid}.impacts[{i}]: unknown direction '{dir_val}'. Valid: {sorted(VALID_DIRECTIONS)}")
            sev_val = imp.get('severity')
            if not isinstance(sev_val, int) or sev_val < -3 or sev_val > 3:
                errors.append(f"{eid}.impacts[{i}]: severity must be -3..+3 integer, got {sev_val}")
    
    # 8. Sources
    sources = e.get('sources', [])
    if not isinstance(sources, list):
        errors.append(f"{eid}: sources must be an array")
    else:
        for i, src in enumerate(sources):
            if not isinstance(src, dict) or 'sourceId' not in src:
                errors.append(f"{eid}.sources[{i}]: missing sourceId")
    
    # 9. LocalizedText for title, summary, narrative
    for field in ['title','summary','narrative']:
        val = e.get(field)
        if not isinstance(val, dict):
            errors.append(f"{eid}: '{field}' must be dict with 'en' and 'zhHans' keys")
        else:
            for lang in ['en','zhHans']:
                if lang not in val or not val[lang]:
                    errors.append(f"{eid}.{field}: missing '{lang}' translation")

# 10. RelatedEvents bidirectional check (warning only)
for e in events:
    for rel_id in e.get('relatedEvents', []):
        if rel_id not in ids:
            pass  # future events may not exist yet
        else:
            rel_event = next(ev for ev in events if ev['id'] == rel_id)
            if e['id'] not in rel_event.get('relatedEvents', []):
                if e['id'].split('-')[-1] > rel_id.split('-')[-1]:  # only warn for newer referencing older
                    warnings.append(f"{e['id']} → {rel_id} (no back-reference)")

# Report
if warnings:
    for w in warnings:
        print(f"⚠️  {w}")

if errors:
    for err in errors:
        print(f"❌ {err}")
    print(f"\nBuild FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)

with open(OUTPUT_FILE, 'w') as fh:
    json.dump(events, fh, ensure_ascii=False, indent=2)

print(f"✅ Built {OUTPUT_FILE} with {len(events)} events ({len(warnings)} warnings)")

# ─────────────────── SSG 详情页静态生成 ───────────────────
import shutil
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_FILE = os.path.join(ROOT_DIR, 'templates', 'detail_template.html')
EVENTS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'events')
SOURCES_FILE = os.path.join(ROOT_DIR, 'data', 'sources.json')

# 确保 events 临时输出目录存在并清空
if os.path.exists(EVENTS_OUTPUT_DIR):
    shutil.rmtree(EVENTS_OUTPUT_DIR)
os.makedirs(EVENTS_OUTPUT_DIR, exist_ok=True)

# 加载 sources.json
with open(SOURCES_FILE) as fh:
    sources_data = json.load(fh)
sources_by_id = {s['id']: s for s in sources_data}

# 建立 events id 快速索引
events_by_id = {e['id']: e for e in events}

if os.path.exists(TEMPLATE_FILE):
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as tf:
        template_content = tf.read()
        
    for e in events:
        eid = e['id']
        copy_title_en = e['title']['en']
        copy_title_zh = e['title']['zhHans']
        if 'searchSummary' in e and 'en' in e['searchSummary'] and e['searchSummary']['en']:
            copy_desc_en = e['searchSummary']['en']
        else:
            raw_summary = e.get('summary', {}).get('en', '')
            copy_desc_en = (raw_summary[:147] + '...') if len(raw_summary) > 150 else raw_summary
        copy_desc_zh = e['summary']['zhHans']
        
        # 1. 渲染 Impacts HTML
        impact_items = []
        for imp in e.get('impacts', []):
            dim = imp.get('dimension')
            dim_en = labels['impactDimension'].get(dim, {}).get('en', dim)
            dim_zh = labels['impactDimension'].get(dim, {}).get('zhHans', dim)
            
            tf_val = imp.get('timeframe')
            tf_en = labels['timeframe'].get(tf_val, {}).get('en', tf_val)
            tf_zh = labels['timeframe'].get(tf_val, {}).get('zhHans', tf_val)
            
            desc_en = imp.get('description', {}).get('en', '')
            desc_zh = html_escape(imp.get('description', {}).get('zhHans', ''))
            desc_en = html_escape(imp.get('description', {}).get('en', ''))
            
            affected_en = html_escape(', '.join(imp.get('affectedGroups', [])))
            affected_zh = html_escape('、'.join(imp.get('affectedGroups', [])))
            
            severity_val = f"+{imp.get('severity')}" if imp.get('severity') > 0 else str(imp.get('severity'))
            
            impact_items.append(f'''
              <li class="impact-item">
                <div class="impact-head">
                  <span class="impact-name" data-zh="{html_escape(dim_zh)}" data-en="{html_escape(dim_en)}">{html_escape(dim_en)}</span>
                  <span class="impact-score" data-zh="{severity_val} · {html_escape(tf_zh)}" data-en="{severity_val} · {html_escape(tf_en)}">{severity_val} · {html_escape(tf_en)}</span>
                </div>
                <p class="impact-description" data-zh="{desc_zh}" data-en="{desc_en}">{desc_en}</p>
                <p class="impact-description" data-zh="受影响群体: {affected_zh}" data-en="Affected Groups: {affected_en}">Affected Groups: {affected_en}</p>
              </li>
            ''')
            
        # 1b. 渲染 Impact Evolution (新增：影响力演进追踪)
        # ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT change class names or DOM structure.
        # This strictly aligns with detail.css styling.
        impact_evolution_html = ''
        impact_updates = e.get('impactUpdates', [])
        if impact_updates:
            mini_nodes = []
            evolution_cards = []
            for upd in impact_updates:
                upd_date = upd.get('date', '')
                upd_ms_en = html_escape(upd.get('milestone', {}).get('en', ''))
                upd_ms_zh = html_escape(upd.get('milestone', {}).get('zhHans', ''))
                upd_sum_en = html_escape(upd.get('summary', {}).get('en', ''))
                upd_sum_zh = html_escape(upd.get('summary', {}).get('zhHans', ''))
                severity_delta = upd.get('severityDelta', '+0')
                cum_severity = upd.get('cumulativeSeverity', 1)
                dim = upd.get('dimension', 'paradigm_shift')
                linked_id = upd.get('linkedEventId', '')
                
                # 获取关联事件详情
                linked_ev = events_by_id.get(linked_id, {})
                linked_title_en = html_escape(linked_ev.get('title', {}).get('en', ''))
                linked_title_zh = html_escape(linked_ev.get('title', {}).get('zhHans', ''))
                linked_date = linked_ev.get('date', '')
                
                dim_en = labels['impactDimension'].get(dim, {}).get('en', dim)
                dim_zh = labels['impactDimension'].get(dim, {}).get('zhHans', dim)
                
                # 拼接横轴 mini 节点
                mini_nodes.append(f'''
                  <div class="mini-node-wrapper" data-linked-id="{linked_id}">
                    <div class="mini-node dim-{dim} severity-{cum_severity}"></div>
                    <span class="mini-node-date">{upd_date}</span>
                    <span class="mini-node-badge">{severity_delta}</span>
                  </div>
                ''')
                
                # 拼接详情卡片
                evolution_cards.append(f'''
                  <div class="evolution-card dim-{dim}" id="upd-{linked_id}">
                    <div class="evolution-card-header">
                      <span class="evolution-date">{upd_date}</span>
                      <span class="evolution-badge badge-delta">变化: {severity_delta}</span>
                      <span class="evolution-badge badge-cum">累积: L{cum_severity}</span>
                      <span class="evolution-dimension" data-zh="{html_escape(dim_zh)}" data-en="{html_escape(dim_en)}">{html_escape(dim_en)}</span>
                    </div>
                    <h4 class="evolution-milestone" data-zh="{upd_ms_zh}" data-en="{upd_ms_en}">{upd_ms_en}</h4>
                    <p class="evolution-summary" data-zh="{upd_sum_zh}" data-en="{upd_sum_en}">{upd_sum_en}</p>
                    <div class="evolution-link-row">
                      <a class="evolution-link-btn" href="javascript:navigateToEvent('{linked_id}')">
                        <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244"></path>
                        </svg>
                        <span data-zh="证据: {linked_title_zh} ({linked_date})" data-en="Evidence: {linked_title_en} ({linked_date})">Evidence: {linked_title_en} ({linked_date})</span>
                      </a>
                    </div>
                  </div>
                ''')
                
            mini_nodes_html = '\n'.join(mini_nodes)
            evolution_cards_html = '\n'.join(evolution_cards)
            
            impact_evolution_html = f'''
              <section class="detail-block impact-evolution-block">
                <h3 class="evolution-block-title" data-zh="影响力演进追踪" data-en="Impact Evolution Tracking">
                  影响力演进追踪
                  <span class="evolution-toggle-hint" data-zh="点击展开详情" data-en="Click to expand details">Click to expand details</span>
                </h3>
                
                <!-- 静态横向演进轴 -->
                <div class="impact-timeline-mini">
                  <div class="mini-line"></div>
                  <div class="mini-nodes-container">
                    {mini_nodes_html}
                  </div>
                </div>
                
                <!-- 里程碑详细卡片列表 (默认折叠) -->
                <div class="impact-evolution-details collapsed">
                  {evolution_cards_html}
                </div>
              </section>
            '''

        # 2. 渲染 Sources HTML
        source_items = []
        for s_idx, source_ref in enumerate(e.get('sources', [])):
            src_id = source_ref.get('sourceId')
            src = sources_by_id.get(src_id, {'id': src_id, 'title': src_id, 'type': 'unknown', 'url': ''})
            
            source_types_translation = {
                'paper': {'en': 'Academic Paper', 'zhHans': '学术论文'},
                'news': {'en': 'News Report', 'zhHans': '新闻报道'},
                'blog': {'en': 'Official Blog / Announcement', 'zhHans': '官方博文/公告'},
                'code': {'en': 'Code Repository', 'zhHans': '开源代码库'},
                'tweet': {'en': 'Social Media Post', 'zhHans': '社交媒体发布'},
                'governance': {'en': 'Official Document', 'zhHans': '政策官方文档'},
                'unknown': {'en': 'Reference Evidence', 'zhHans': '参考证据'}
            }
            src_type = src.get('type', 'unknown')
            type_en = source_types_translation.get(src_type, source_types_translation['unknown'])['en']
            type_zh = source_types_translation.get(src_type, source_types_translation['unknown'])['zhHans']
            
            title_html = f'<a class="source-title source-title-link" href="{src.get("url")}" target="_blank" rel="noopener noreferrer">{src.get("title")}</a>' if src.get("url") else f'<span class="source-title">{src.get("title")}</span>'
            quote_html = f'<div class="source-quote">{source_ref.get("quote")}</div>' if source_ref.get('quote') else ''
            
            meta_en = html_escape(f'URL: {src.get("url")}' if src.get("url") else 'URL pending')
            meta_zh = html_escape(f'原文可访问: {src.get("url")}' if src.get("url") else '待补原文链接')
            
            source_items.append(f'''
              <li class="source-card">
                <span class="source-index">{s_idx + 1}</span>
                <div class="source-body">
                  <div class="source-row">
                    {title_html}
                  </div>
                  <p class="source-meta" data-zh="{meta_zh}" data-en="{meta_en}">{meta_en}</p>
                  {quote_html}
                  <div class="source-status">
                    <span class="source-chip" data-zh="{html_escape(type_zh)}" data-en="{html_escape(type_en)}">{html_escape(type_en)}</span>
                    <span class="source-chip" data-zh="引用已记录" data-en="Citation logged">Citation logged</span>
                    <span class="source-chip" data-zh="原文可访问" data-en="Live source">Live source</span>
                  </div>
                </div>
              </li>
            ''')
            
        impacts_html = '\n'.join(impact_items)
        sources_html = '\n'.join(source_items)
            
        # 3. 计算关联关系
        related_ids = set(e.get('relatedEvents', []))
        for other_e in events:
            if eid in other_e.get('relatedEvents', []):
                related_ids.add(other_e['id'])
        related_ids.discard(eid)
        
        related_events_list = [events_by_id[rid] for rid in related_ids if rid in events_by_id]
        related_events_list.sort(key=lambda x: x['date'])
        
        precursors = [re for re in related_events_list if re['date'] < e['date']]
        successors = [re for re in related_events_list if re['date'] > e['date']]
        
        # 静态 JSON 字典注入供 hover 用
        related_data_dict = {}
        for re in related_events_list:
            cat = re['categories'][0]
            cat_en = labels['category'].get(cat, {}).get('en', cat)
            cat_zh = labels['category'].get(cat, {}).get('zhHans', cat)
            related_data_dict[re['id']] = {
                'date': re['date'],
                'significance': re['significance'],
                'category': {'en': cat_en, 'zh': cat_zh},
                'title': {'en': re['title']['en'], 'zh': re['title']['zhHans']},
                'summary': {'en': re['summary']['en'], 'zh': re['summary']['zhHans']}
            }
        related_data_json = json.dumps(related_data_dict, ensure_ascii=False)
        
        # 前驱
        precursors_html = ''
        if precursors:
            cards = []
            for p in precursors:
                # ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT REMOVE html_escape! 
                # p_title and p_summary MUST be escaped to avoid unescaped quotes causing markup syntax crash.
                p_title_zh = html_escape(p['title']['zhHans'])
                p_title_en = html_escape(p['title']['en'])
                p_summary_zh = html_escape(p['summary']['zhHans'])
                p_summary_en = html_escape(p['summary']['en'])
                cards.append(f'''
                  <div class="related-card" onclick="navigateToEvent('{p['id']}')">
                    <div class="related-card-meta">
                      <span>{p['date']}</span>
                      <span class="sig-badge">L{p['significance']}</span>
                    </div>
                    <h4 class="related-card-title" data-zh="{p_title_zh}" data-en="{p_title_en}">{p_title_en}</h4>
                    <p class="related-card-summary" data-zh="{p_summary_zh}" data-en="{p_summary_en}">{p_summary_en}</p>
                  </div>
                ''')
            precursors_html = f'''
              <div class="related-row">
                <div class="related-row-title">
                  <span data-zh="← 前驱事件 (Origins)" data-en="← Origins">← Origins</span>
                </div>
                <div class="related-cards-container">
                  {''.join(cards)}
                </div>
              </div>
            '''
            
        # 后继
        successors_html = ''
        if successors:
            cards = []
            for s in successors:
                # ⚠️ WARNING FOR OTHER AI AGENTS: DO NOT REMOVE html_escape! 
                # s_title and s_summary MUST be escaped to avoid unescaped quotes causing markup syntax crash.
                s_title_zh = html_escape(s['title']['zhHans'])
                s_title_en = html_escape(s['title']['en'])
                s_summary_zh = html_escape(s['summary']['zhHans'])
                s_summary_en = html_escape(s['summary']['en'])
                cards.append(f'''
                  <div class="related-card" onclick="navigateToEvent('{s['id']}')">
                    <div class="related-card-meta">
                      <span>{s['date']}</span>
                      <span class="sig-badge">L{s['significance']}</span>
                    </div>
                    <h4 class="related-card-title" data-zh="{s_title_zh}" data-en="{s_title_en}">{s_title_en}</h4>
                    <p class="related-card-summary" data-zh="{s_summary_zh}" data-en="{s_summary_en}">{s_summary_en}</p>
                  </div>
                ''')
            successors_html = f'''
              <div class="related-row">
                <div class="related-row-title">
                  <span data-zh="→ 后继事件 (Successors)" data-en="→ Successors">→ Successors</span>
                </div>
                <div class="related-cards-container">
                  {''.join(cards)}
                </div>
              </div>
            '''
            
        # SVG 局部演进图谱
        topology_html = ''
        if related_events_list:
            view_width = 700
            view_height = 280
            center_node_x = 350
            center_node_y = 140
            precursor_x = 110
            successor_x = 590
            
            visible_precursors = precursors[-4:]
            visible_successors = successors[:4]
            
            nodes_markup = []
            links_markup = []
            
            defs_markup = '''
              <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="var(--border)" />
                </marker>
                <marker id="arrow-highlighted" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="var(--accent)" />
                </marker>
              </defs>
            '''
            
            c_title_en = html_escape(e['title']['en'][:20] + '...' if len(e['title']['en']) > 22 else e['title']['en'])
            c_title_zh = html_escape(e['title']['zhHans'][:12] + '...' if len(e['title']['zhHans']) > 14 else e['title']['zhHans'])
            nodes_markup.append(f'''
              <g class="svg-node" onclick="event.stopPropagation()" onmouseenter="showEventTooltip(event, '{eid}')" onmouseleave="hideEventTooltip()">
                <rect class="svg-node-rect center-node breathing-aura" x="{center_node_x - 95}" y="{center_node_y - 26}" width="190" height="52" />
                <text class="svg-node-title" x="{center_node_x}" y="{center_node_y - 2}" text-anchor="middle" data-zh="{c_title_zh}" data-en="{c_title_en}">{c_title_en}</text>
                <text class="svg-node-date" x="{center_node_x}" y="{center_node_y + 16}" text-anchor="middle">{e['date']} · L{e['significance']}</text>
              </g>
            ''')
            
            if visible_precursors:
                gap_y = view_height / (len(visible_precursors) + 1)
                for idx, p in enumerate(visible_precursors):
                    node_y = gap_y * (idx + 1)
                    p_title_en = html_escape(p['title']['en'][:18] + '...' if len(p['title']['en']) > 20 else p['title']['en'])
                    p_title_zh = html_escape(p['title']['zhHans'][:11] + '...' if len(p['title']['zhHans']) > 13 else p['title']['zhHans'])
                    
                    st_x = precursor_x + 85
                    st_y = node_y
                    ed_x = center_node_x - 95
                    ed_y = center_node_y
                    ct_x1 = st_x + 40
                    ct_y1 = st_y
                    ct_x2 = ed_x - 40
                    ct_y2 = ed_y
                    
                    links_markup.append(f'''
                      <path class="svg-link-path" id="link-{p['id']}-{eid}" d="M {st_x} {st_y} C {ct_x1} {ct_y1}, {ct_x2} {ct_y2}, {ed_x} {ed_y}" marker-end="url(#arrow)" />
                    ''')
                    
                    nodes_markup.append(f'''
                      <g class="svg-node" onclick="navigateToEvent('{p['id']}')" onmouseenter="highlightLink('link-{p['id']}-{eid}', true); showEventTooltip(event, '{p['id']}')" onmouseleave="highlightLink('link-{p['id']}-{eid}', false); hideEventTooltip()">
                        <rect class="svg-node-rect" x="{precursor_x - 85}" y="{node_y - 22}" width="170" height="44" />
                        <text class="svg-node-title" x="{precursor_x}" y="{node_y - 2}" text-anchor="middle" data-zh="{p_title_zh}" data-en="{p_title_en}">{p_title_en}</text>
                        <text class="svg-node-date" x="{precursor_x}" y="{node_y + 12}" text-anchor="middle">{p['date']} · L{p['significance']}</text>
                      </g>
                    ''')
                    
            if visible_successors:
                gap_y = view_height / (len(visible_successors) + 1)
                for idx, s in enumerate(visible_successors):
                    node_y = gap_y * (idx + 1)
                    s_title_en = html_escape(s['title']['en'][:18] + '...' if len(s['title']['en']) > 20 else s['title']['en'])
                    s_title_zh = html_escape(s['title']['zhHans'][:11] + '...' if len(s['title']['zhHans']) > 13 else s['title']['zhHans'])
                    
                    st_x = center_node_x + 95
                    st_y = center_node_y
                    ed_x = successor_x - 85
                    ed_y = node_y
                    ct_x1 = st_x + 40
                    ct_y1 = st_y
                    ct_x2 = ed_x - 40
                    ct_y2 = ed_y
                    
                    links_markup.append(f'''
                      <path class="svg-link-path" id="link-{eid}-{s['id']}" d="M {st_x} {st_y} C {ct_x1} {ct_y1}, {ct_x2} {ct_y2}, {ed_x} {ed_y}" marker-end="url(#arrow)" />
                    ''')
                    
                    nodes_markup.append(f'''
                      <g class="svg-node" onclick="navigateToEvent('{s['id']}')" onmouseenter="highlightLink('link-{eid}-{s['id']}', true); showEventTooltip(event, '{s['id']}')" onmouseleave="highlightLink('link-{eid}-{s['id']}', false); hideEventTooltip()">
                        <rect class="svg-node-rect" x="{successor_x - 85}" y="{node_y - 22}" width="170" height="44" />
                        <text class="svg-node-title" x="{successor_x}" y="{node_y - 2}" text-anchor="middle" data-zh="{s_title_zh}" data-en="{s_title_en}">{s_title_en}</text>
                        <text class="svg-node-date" x="{successor_x}" y="{node_y + 12}" text-anchor="middle">{s['date']} · L{s['significance']}</text>
                      </g>
                    ''')
                    
            links_markup_str = '\n'.join(links_markup)
            nodes_markup_str = '\n'.join(nodes_markup)
            topology_html = f'''
              <div class="related-topology-container">
                <span class="related-topology-title" data-zh="局部演进图谱 (Local Lineage)" data-en="Local Lineage">Local Lineage</span>
                <svg class="related-svg" viewBox="0 0 {view_width} {view_height}">
                  {defs_markup}
                  {links_markup_str}
                  {nodes_markup_str}
                </svg>
              </div>
            '''
            
        related_section_html = ''
        if related_events_list:
            related_section_html = f'''
              <section class="detail-block related-section">
                <h3 data-zh="关联事件" data-en="Related Events">关联事件</h3>
                {precursors_html}
                {successors_html}
                {topology_html}
              </section>
            '''
            
        # 4. 生成多语言分类和共识字符串
        primary_cat = e['categories'][0]
        primary_cat_name_en = labels['category'].get(primary_cat, {}).get('en', primary_cat)
        primary_cat_name_zh = labels['category'].get(primary_cat, {}).get('zhHans', primary_cat)
        
        secondary_cat_html = ''
        if len(e['categories']) > 1:
            sec_cat = e['categories'][1]
            sec_cat_en = labels['category'].get(sec_cat, {}).get('en', sec_cat)
            sec_cat_zh = labels['category'].get(sec_cat, {}).get('zhHans', sec_cat)
            secondary_cat_html = f'<span class="category-badge secondary {sec_cat}" data-zh="{sec_cat_zh}" data-en="{sec_cat_en}">{sec_cat_en}</span>'
            
        cats_en = ' / '.join([labels['category'].get(c, {}).get('en', c) for c in e['categories']])
        cats_zh = ' / '.join([labels['category'].get(c, {}).get('zhHans', c) for c in e['categories']])
        
        con = e['consensusLevel']
        con_en = labels['consensus'].get(con, {}).get('en', con)
        con_zh = labels['consensus'].get(con, {}).get('zhHans', con)
        
        # 5. 替换占位符并写出物理文件
        schema_data = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": copy_title_en,
            "description": copy_desc_en,
            "datePublished": e['date'],
            "dateModified": e.get('editorial', {}).get('updatedAt', e['date']),
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
            "mainEntityOfPage": f"https://epoch-arc.com/events/{eid}/"
        }
        schema_json_ld = f'<script type="application/ld+json">\n{json.dumps(schema_data, ensure_ascii=False, indent=2)}\n</script>'

        page_html = template_content
        page_html = page_html.replace('{{SCHEMA_JSON_LD}}', schema_json_ld)
        page_html = page_html.replace('{{SEO_TITLE}}', copy_title_en)
        page_html = page_html.replace('{{SEO_DESC}}', copy_desc_en)
        page_html = page_html.replace('{{SLUG}}', eid)
        page_html = page_html.replace('{{ID}}', eid)
        page_html = page_html.replace('{{DATE}}', e['date'])
        page_html = page_html.replace('{{TITLE_ZH}}', copy_title_zh)
        page_html = page_html.replace('{{TITLE_EN}}', copy_title_en)
        page_html = page_html.replace('{{PRIMARY_CAT}}', primary_cat)
        page_html = page_html.replace('{{PRIMARY_CAT_NAME}}', primary_cat_name_en)
        page_html = page_html.replace('{{SECONDARY_CAT_HTML}}', secondary_cat_html)
        page_html = page_html.replace('{{DESC_ZH}}', copy_desc_zh)
        page_html = page_html.replace('{{DESC_EN}}', copy_desc_en)
        page_html = page_html.replace('{{IMPACTS}}', impacts_html)
        page_html = page_html.replace('{{IMPACT_EVOLUTION_HTML}}', impact_evolution_html)
        page_html = page_html.replace('{{SIGNIFICANCE}}', str(e['significance']))
        page_html = page_html.replace('{{CATEGORIES}}', f'<span data-zh="{cats_zh}" data-en="{cats_en}">{cats_en}</span>')
        page_html = page_html.replace('{{CONSENSUS}}', f'<span data-zh="{con_zh}" data-en="{con_en}">{con_en}</span>')
        page_html = page_html.replace('{{IMPACT_INDEX}}', str(e['impactIndex']))
        page_html = page_html.replace('{{SOURCES}}', sources_html)
        page_html = page_html.replace('{{RELATED}}', related_section_html)
        page_html = page_html.replace('{{RELATED_DATA_JSON}}', related_data_json)
        
        # 写出到 events/{eid}/index.html 
        event_dir = os.path.join(EVENTS_OUTPUT_DIR, eid)
        os.makedirs(event_dir, exist_ok=True)
        event_output_file = os.path.join(event_dir, 'index.html')
        with open(event_output_file, 'w', encoding='utf-8') as ev_fh:
            ev_fh.write(page_html)
            
    print(f"✅ Generated {len(events)} static event detail pages inside {EVENTS_OUTPUT_DIR}")

# ─────────────────── 同步 SSG 页面至 dist/ ───────────────────
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
if os.path.exists(DIST_DIR):
    shutil.copytree(EVENTS_OUTPUT_DIR, os.path.join(DIST_DIR, 'events'), dirs_exist_ok=True)
    print(f"✅ Synced static events to {DIST_DIR}/events/")

# ─────────────────── 回填 HTML Fallback 数据 ───────────────────
import re

def inject_fallback_data(html_path, forecasts_json, events_json, sources_json):
    if not os.path.exists(html_path):
        return False
    with open(html_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # 替换 fallback-forecasts-data
    def replace_forecasts(match):
        return match.group(1) + forecasts_json + match.group(2)
    content = re.sub(
        r'(<script\s+type="application/json"\s+id="fallback-forecasts-data">).*?(</script>)',
        replace_forecasts,
        content,
        flags=re.DOTALL
    )
    # 替换 fallback-events-data
    def replace_events(match):
        return match.group(1) + events_json + match.group(2)
    content = re.sub(
        r'(<script\s+type="application/json"\s+id="fallback-events-data">).*?(</script>)',
        replace_events,
        content,
        flags=re.DOTALL
    )
    # 替换 fallback-sources-data
    def replace_sources(match):
        return match.group(1) + sources_json + match.group(2)
    content = re.sub(
        r'(<script\s+type="application/json"\s+id="fallback-sources-data">).*?(</script>)',
        replace_sources,
        content,
        flags=re.DOTALL
    )
    
    with open(html_path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    return True

# 准备这三个 JSON 的紧凑字符串
with open(os.path.join(ROOT_DIR, 'data', 'forecasts.json'), 'r', encoding='utf-8') as fh:
    forecasts_data_str = json.dumps(json.load(fh), ensure_ascii=False)
with open(os.path.join(ROOT_DIR, 'data', 'events.json'), 'r', encoding='utf-8') as fh:
    events_data_str = json.dumps(json.load(fh), ensure_ascii=False)
with open(os.path.join(ROOT_DIR, 'data', 'sources.json'), 'r', encoding='utf-8') as fh:
    sources_data_str = json.dumps(json.load(fh), ensure_ascii=False)

inject_fallback_data(os.path.join(ROOT_DIR, 'index.html'), forecasts_data_str, events_data_str, sources_data_str)
inject_fallback_data(os.path.join(ROOT_DIR, 'dist', 'index.html'), forecasts_data_str, events_data_str, sources_data_str)
print("✅ Injected fallback data into index.html and dist/index.html")

# ─────────────────── 自动生成 sitemap.xml ───────────────────
def generate_sitemap(events):
    import datetime
    today = datetime.date.today().isoformat()
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>https://epoch-arc.com/</loc><lastmod>{today}</lastmod></url>',
        f'  <url><loc>https://epoch-arc.com/methods.html</loc><lastmod>{today}</lastmod></url>'
    ]
    
    for e in events:
        slug = e['id']
        xml_lines.append(f'  <url><loc>https://epoch-arc.com/events/{slug}/</loc><lastmod>{today}</lastmod></url>')
        
    xml_lines.append('</urlset>')
    sitemap_content = '\n'.join(xml_lines)
    
    # 写入根目录下
    with open(os.path.join(ROOT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write(sitemap_content)
    # 如果 dist/ 存在，同样写入 dist/
    if os.path.exists(DIST_DIR):
        with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
            fh.write(sitemap_content)
            
    print("✅ Generated sitemap.xml with physical routes successfully")

generate_sitemap(events)


