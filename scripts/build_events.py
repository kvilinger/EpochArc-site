#!/usr/bin/env python3
"""Build data/events.json from content/events/*.json with full validation"""
import json, os, glob, sys, html
from impact_display import EMPTY as IMPACT_EMPTY, impact_index_label
from html_safety import http_url, script_json, claim_source_link, SOURCE_TYPE_LABELS

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
SOURCES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sources.json')

events = []
for f in sorted(glob.glob(os.path.join(EVENTS_DIR, '*.json'))):
    with open(f) as fh:
        event = json.load(fh)
        if event.get('status') == 'published':
            events.append(event)

# Load labels for validation
with open(LABELS_FILE) as fh:
    labels = json.load(fh)
with open(SOURCES_FILE) as fh:
    source_records = json.load(fh)
VALID_CATEGORIES = set(labels['category'].keys())
VALID_DIMENSIONS = set(labels['impactDimension'].keys())
VALID_TIMEFRAMES = set(labels['timeframe'].keys())
VALID_CONSENSUS = set(labels['consensus'].keys())
VALID_DIRECTIONS = {'positive', 'negative', 'mixed', 'neutral'}
VALID_CLAIM_TYPES = {'fact', 'impact', 'limitation', 'interpretation'}
VALID_EVIDENCE_GRADES = {'A', 'B', 'C', 'D'}
VALID_CHANGE_TYPES = {
    'created', 'source_added', 'score_changed', 'translation_changed',
    'forecast_resolved', 'correction', 'archived'
}
VALID_SOURCE_IDS = {source['id'] for source in source_records}

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
    for field in ['id','date','datePrecision','title','searchSummary','summary','narrative','categories','significance','impactIndex','impacts','claims','sources','editorial']:
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
            elif src['sourceId'] not in VALID_SOURCE_IDS:
                errors.append(f"{eid}.sources[{i}]: unknown sourceId '{src['sourceId']}'")
    
    # 9. LocalizedText for title, searchSummary, summary, narrative
    for field in ['title','searchSummary','summary','narrative']:
        val = e.get(field)
        if not isinstance(val, dict):
            errors.append(f"{eid}: '{field}' must be dict with 'en' and 'zhHans' keys")
        else:
            for lang in ['en','zhHans']:
                if lang not in val or not val[lang]:
                    errors.append(f"{eid}.{field}: missing '{lang}' translation")

    # 10. Claims
    claims = e.get('claims', [])
    if not isinstance(claims, list) or not claims:
        errors.append(f"{eid}: claims must be a non-empty array")
    else:
        claim_ids = set()
        for i, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"{eid}.claims[{i}]: must be an object")
                continue
            for field in ['id', 'text', 'claimType', 'evidenceGrade', 'sourceIds']:
                if field not in claim:
                    errors.append(f"{eid}.claims[{i}]: missing required field '{field}'")
            claim_id = claim.get('id')
            if not isinstance(claim_id, str) or not claim_id.strip():
                errors.append(f"{eid}.claims[{i}].id: must be a non-empty string")
            elif claim_id in claim_ids:
                errors.append(f"{eid}: duplicate claim ID '{claim_id}'")
            else:
                claim_ids.add(claim_id)
            claim_text = claim.get('text')
            if not isinstance(claim_text, dict):
                errors.append(f"{eid}.claims[{i}].text: must contain localized text")
            else:
                for lang in ['en', 'zhHans']:
                    if not isinstance(claim_text.get(lang), str) or not claim_text[lang].strip():
                        errors.append(f"{eid}.claims[{i}].text: missing '{lang}' translation")
            if claim.get('claimType') not in VALID_CLAIM_TYPES:
                errors.append(
                    f"{eid}.claims[{i}]: unknown claimType '{claim.get('claimType')}'. "
                    f"Valid: {sorted(VALID_CLAIM_TYPES)}"
                )
            if claim.get('evidenceGrade') not in VALID_EVIDENCE_GRADES:
                errors.append(
                    f"{eid}.claims[{i}]: invalid evidenceGrade '{claim.get('evidenceGrade')}'. "
                    f"Valid: {sorted(VALID_EVIDENCE_GRADES)}"
                )
            source_ids = claim.get('sourceIds')
            if not isinstance(source_ids, list):
                errors.append(f"{eid}.claims[{i}].sourceIds: must be an array")
            elif any(not isinstance(source_id, str) or not source_id.strip() for source_id in source_ids):
                errors.append(f"{eid}.claims[{i}].sourceIds: entries must be non-empty strings")
            elif not source_ids:
                errors.append(f"{eid}.claims[{i}].sourceIds: must contain at least one source")
            else:
                for source_id in source_ids:
                    if source_id not in VALID_SOURCE_IDS:
                        errors.append(
                            f"{eid}.claims[{i}].sourceIds: unknown sourceId '{source_id}'"
                        )

    # 11. Editorial metadata
    editorial = e.get('editorial')
    if not isinstance(editorial, dict):
        errors.append(f"{eid}: editorial must be an object")
    else:
        for field in ['createdAt', 'updatedAt']:
            if not isinstance(editorial.get(field), str) or not editorial[field].strip():
                errors.append(f"{eid}.editorial: missing or empty '{field}'")
        for field in ['reviewedAt', 'publishedAt', 'lastSourceCheckAt', 'curator', 'reviewer']:
            if field in editorial and (
                not isinstance(editorial[field], str) or not editorial[field].strip()
            ):
                errors.append(f"{eid}.editorial.{field}: must be a non-empty string")
        curator_note = editorial.get('curatorNote')
        if curator_note is not None:
            if not isinstance(curator_note, dict):
                errors.append(f"{eid}.editorial.curatorNote: must contain localized text")
            else:
                for lang in ['en', 'zhHans']:
                    if not isinstance(curator_note.get(lang), str) or not curator_note[lang].strip():
                        errors.append(f"{eid}.editorial.curatorNote: missing '{lang}' translation")
        change_log = editorial.get('changeLog')
        if change_log is not None:
            if not isinstance(change_log, list):
                errors.append(f"{eid}.editorial.changeLog: must be an array")
            else:
                for i, entry in enumerate(change_log):
                    if not isinstance(entry, dict):
                        errors.append(f"{eid}.editorial.changeLog[{i}]: must be an object")
                        continue
                    for field in ['date', 'changeType', 'summary']:
                        if not isinstance(entry.get(field), str) or not entry[field].strip():
                            errors.append(
                                f"{eid}.editorial.changeLog[{i}]: missing or empty '{field}'"
                            )
                    if entry.get('changeType') not in VALID_CHANGE_TYPES:
                        errors.append(
                            f"{eid}.editorial.changeLog[{i}]: invalid changeType "
                            f"'{entry.get('changeType')}'"
                        )

    # 12. Related events: source files may declare one side; targets must be valid.
    related_events = e.get('relatedEvents', [])
    if not isinstance(related_events, list):
        errors.append(f"{eid}.relatedEvents: must be an array")
    else:
        seen_related = set()
        for i, rel_id in enumerate(related_events):
            if not isinstance(rel_id, str) or not rel_id.strip():
                errors.append(f"{eid}.relatedEvents[{i}]: must be a non-empty string")
                continue
            if rel_id == eid:
                errors.append(f"{eid}.relatedEvents[{i}]: must not reference itself")
            if rel_id in seen_related:
                errors.append(f"{eid}.relatedEvents: duplicate event ID '{rel_id}'")
            else:
                seen_related.add(rel_id)
            if rel_id not in ids:
                errors.append(f"{eid}.relatedEvents[{i}]: unknown event ID '{rel_id}'")

# Report
if warnings:
    for w in warnings:
        print(f"⚠️  {w}")

if errors:
    for err in errors:
        print(f"❌ {err}")
    print(f"\nBuild FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)

# relatedEvents is logically undirected. Keep source files concise, but publish a
# symmetric graph so every consumer sees the same neighbors without reverse scans.
events_by_id_for_relations = {e['id']: e for e in events}
normalized_relation_count = 0
for e in events:
    e['relatedEvents'] = list(e.get('relatedEvents', []))
for e in events:
    for rel_id in list(e['relatedEvents']):
        reverse_relations = events_by_id_for_relations[rel_id]['relatedEvents']
        if e['id'] not in reverse_relations:
            reverse_relations.append(e['id'])
            normalized_relation_count += 1

with open(OUTPUT_FILE, 'w') as fh:
    json.dump(events, fh, ensure_ascii=False, indent=2)

print(
    f"✅ Built {OUTPUT_FILE} with {len(events)} events "
    f"({normalized_relation_count} reverse relations normalized, {len(warnings)} warnings)"
)

# ─────────────────── SSG 详情页静态生成 ───────────────────
import shutil
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_FILE = os.path.join(ROOT_DIR, 'templates', 'detail_template.html')
EVENTS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'events')
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
        copy_summary_en = e['summary']['en']
        copy_summary_zh = e['summary']['zhHans']
        copy_narrative_en = e['narrative']['en']
        copy_narrative_zh = e['narrative']['zhHans']
        copy_lead_en = e.get('searchSummary', {}).get('en') or copy_summary_en
        copy_lead_zh = e.get('searchSummary', {}).get('zhHans') or copy_summary_zh
        seo_desc_en = copy_lead_en
        
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
            
        # 2. 渲染 Sources HTML
        source_items = []
        source_index_by_id = {
            source_ref.get('sourceId'): index + 1
            for index, source_ref in enumerate(e.get('sources', []))
            if source_ref.get('sourceId')
        }
        for s_idx, source_ref in enumerate(e.get('sources', [])):
            src_id = source_ref.get('sourceId')
            src = sources_by_id.get(src_id, {'id': src_id, 'title': src_id, 'type': 'unknown', 'url': ''})
            
            src_type = src.get('type', 'unknown')
            type_en = SOURCE_TYPE_LABELS.get(src_type, SOURCE_TYPE_LABELS['unknown'])['en']
            type_zh = SOURCE_TYPE_LABELS.get(src_type, SOURCE_TYPE_LABELS['unknown'])['zhHans']
            
            source_url = http_url(src.get('url'))
            source_title = html_escape(src.get('title'))
            title_html = f'<a class="source-title source-title-link" href="{html_escape(source_url)}" target="_blank" rel="noopener noreferrer">{source_title}</a>' if source_url else f'<span class="source-title">{source_title}</span>'
            quote_html = f'<div class="source-quote">{html_escape(source_ref.get("quote"))}</div>' if source_ref.get('quote') else ''
            
            meta_en = html_escape(f'URL: {source_url}' if source_url else 'URL pending')
            meta_zh = html_escape(f'原文链接: {source_url}' if source_url else '待补原文链接')
            status_en = 'Source link' if source_url else 'URL pending'
            status_zh = '原文链接' if source_url else '待补原文链接'
            
            source_items.append(f'''
              <li class="source-card" id="source-{html_escape(src_id)}">
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
                    <span class="source-chip" data-zh="{status_zh}" data-en="{status_en}">{status_en}</span>
                  </div>
                </div>
              </li>
            ''')
            
        impacts_html = '\n'.join(impact_items)
        if not impact_items:
            impacts_html = f'<li class="impact-item" data-zh="{html_escape(IMPACT_EMPTY["zhHans"])}" data-en="{html_escape(IMPACT_EMPTY["en"])}">{html_escape(IMPACT_EMPTY["en"])}</li>'
        sources_html = '\n'.join(source_items)

        # 3. 渲染带证据绑定的关键结论
        claim_type_labels = {
            'fact': {'en': 'Fact', 'zhHans': '事实'},
            'impact': {'en': 'Impact', 'zhHans': '影响'},
            'limitation': {'en': 'Limitation', 'zhHans': '局限'},
            'interpretation': {'en': 'Interpretation', 'zhHans': '解读'},
        }
        claim_items = []
        for claim in e.get('claims', []):
            claim_type = claim.get('claimType', 'fact')
            claim_label = claim_type_labels.get(claim_type, claim_type_labels['fact'])
            source_links = []
            for source_id in claim.get('sourceIds', []):
                source = sources_by_id.get(source_id, {})
                source_number = source_index_by_id.get(source_id)
                source_links.append(claim_source_link(source, source_id, source_number))

            claim_items.append(f'''
              <li class="claim-card claim-{claim_type}">
                <div class="claim-head">
                  <span class="claim-type" data-zh="{html_escape(claim_label['zhHans'])}" data-en="{html_escape(claim_label['en'])}">{html_escape(claim_label['en'])}</span>
                  <span class="claim-grade">Grade {html_escape(claim.get('evidenceGrade', ''))}</span>
                </div>
                <p class="claim-text" data-zh="{html_escape(claim.get('text', {}).get('zhHans', ''))}" data-en="{html_escape(claim.get('text', {}).get('en', ''))}">{html_escape(claim.get('text', {}).get('en', ''))}</p>
                <div class="claim-sources">
                  <span data-zh="来源" data-en="Sources">Sources</span>
                  {''.join(source_links)}
                </div>
              </li>
            ''')
        claims_html = '\n'.join(claim_items)
            
        # 4. 计算关联关系
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
        related_data_json = script_json(related_data_dict, ensure_ascii=False)
        
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
                  <div class="related-card" onclick="navigateToEvent('{p.get('slug', p['id'])}')">
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
                  <div class="related-card" onclick="navigateToEvent('{s.get('slug', s['id'])}')">
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
                      <g class="svg-node" onclick="navigateToEvent('{p.get('slug', p['id'])}')" onmouseenter="highlightLink('link-{p['id']}-{eid}', true); showEventTooltip(event, '{p['id']}')" onmouseleave="highlightLink('link-{p['id']}-{eid}', false); hideEventTooltip()">
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
                      <g class="svg-node" onclick="navigateToEvent('{s.get('slug', s['id'])}')" onmouseenter="highlightLink('link-{eid}-{s['id']}', true); showEventTooltip(event, '{s['id']}')" onmouseleave="highlightLink('link-{eid}-{s['id']}', false); hideEventTooltip()">
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
              <section class="detail-block related-section" id="event-related" data-toc-section>
                <h2 data-zh="关联事件" data-en="Related Events">关联事件</h2>
                {precursors_html}
                {successors_html}
                {topology_html}
              </section>
            '''
            
        # 5. 生成多语言分类和共识字符串
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
        
        # 6. 替换占位符并写出物理文件
        schema_data = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": copy_title_en,
            "description": seo_desc_en,
            "articleBody": f"{copy_summary_en}\n\n{copy_narrative_en}",
            "datePublished": e['date'],
            "dateModified": e.get('editorial', {}).get('updatedAt', e['date']),
            "image": f"https://epoch-arc.com/assets/og/events/{e['slug']}.png",
            "articleSection": ', '.join(labels['category'].get(c, {}).get('en', c) for c in e.get('categories', [])),
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
            "mainEntityOfPage": f"https://epoch-arc.com/events/{e['slug']}/"
        }
        schema_json_ld = f'<script type="application/ld+json">\n{script_json(schema_data, ensure_ascii=False, indent=2)}\n</script>'

        page_html = template_content
        page_html = page_html.replace('{{SCHEMA_JSON_LD}}', schema_json_ld)
        page_html = page_html.replace('{{SEO_TITLE}}', html_escape(copy_title_en))
        page_html = page_html.replace('{{SEO_DESC}}', html_escape(seo_desc_en))
        page_html = page_html.replace('{{SLUG}}', e['slug'])
        page_html = page_html.replace('{{ID}}', eid)
        page_html = page_html.replace('{{DATE}}', e['date'])
        page_html = page_html.replace('{{TITLE_ZH}}', html_escape(copy_title_zh))
        page_html = page_html.replace('{{TITLE_EN}}', html_escape(copy_title_en))
        page_html = page_html.replace('{{PRIMARY_CAT}}', primary_cat)
        page_html = page_html.replace('{{PRIMARY_CAT_NAME}}', html_escape(primary_cat_name_en))
        page_html = page_html.replace('{{PRIMARY_CAT_NAME_ZH}}', html_escape(primary_cat_name_zh))
        page_html = page_html.replace('{{SECONDARY_CAT_HTML}}', secondary_cat_html)
        page_html = page_html.replace('{{LEAD_ZH}}', html_escape(copy_lead_zh))
        page_html = page_html.replace('{{LEAD_EN}}', html_escape(copy_lead_en))
        page_html = page_html.replace('{{SUMMARY_ZH}}', html_escape(copy_summary_zh))
        page_html = page_html.replace('{{SUMMARY_EN}}', html_escape(copy_summary_en))
        page_html = page_html.replace('{{NARRATIVE_ZH}}', html_escape(copy_narrative_zh))
        page_html = page_html.replace('{{NARRATIVE_EN}}', html_escape(copy_narrative_en))
        page_html = page_html.replace('{{CLAIMS}}', claims_html)
        page_html = page_html.replace('{{IMPACTS}}', impacts_html)
        page_html = page_html.replace('{{SIGNIFICANCE}}', str(e['significance']))
        page_html = page_html.replace('{{CATEGORIES}}', f'<span data-zh="{cats_zh}" data-en="{cats_en}">{cats_en}</span>')
        page_html = page_html.replace('{{CONSENSUS}}', f'<span data-zh="{con_zh}" data-en="{con_en}">{con_en}</span>')
        impact_label = f'<span data-zh="{html_escape(impact_index_label(e, "zhHans"))}" data-en="{html_escape(impact_index_label(e))}">{html_escape(impact_index_label(e))}</span>'
        page_html = page_html.replace('{{IMPACT_INDEX_LABEL}}', impact_label)
        page_html = page_html.replace('{{SOURCES}}', sources_html)
        related_toc = '<a href="#event-related" data-zh="关联事件" data-en="Related events">Related events</a>' if related_events_list else ''
        page_html = page_html.replace('{{RELATED_TOC_LINK}}', related_toc)
        page_html = page_html.replace('{{RELATED}}', related_section_html)
        page_html = page_html.replace('{{RELATED_DATA_JSON}}', related_data_json)
        
        # 写出到 events/{slug}/index.html
        event_dir = os.path.join(EVENTS_OUTPUT_DIR, e['slug'])
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

# ─────────────────── 精简摘要数据生成 (events_summary.json) ───────────────────
# Keep this tuple ordered so generated summary output stays deterministic across
# Python hash seeds.
FALLBACK_KEEP_KEYS = (
    'id', 'slug', 'title', 'date', 'datePrecision', 'searchSummary', 'summary',
    'categories', 'significance', 'impactIndex', 'consensusLevel', 'controversy', 'tags',
)

def trim_for_fallback(events):
    """生成首页首屏列表与全筛选器所需的精简事件摘要"""
    trimmed = []
    for e in events:
        entry = {}
        for key in FALLBACK_KEEP_KEYS:
            if key in e:
                entry[key] = e[key]
        entry['impactCount'] = len(e.get('impacts', []))
        entry['impactDimensions'] = list(dict.fromkeys(impact['dimension'] for impact in e.get('impacts', [])))
        trimmed.append(entry)
    return trimmed

import re

with open(os.path.join(ROOT_DIR, 'data', 'events.json'), 'r', encoding='utf-8') as fh:
    full_events_list = json.load(fh)

trimmed_events = trim_for_fallback(full_events_list)
trimmed_events_str = json.dumps(trimmed_events, ensure_ascii=False, default=str)
summary_path = os.path.join(ROOT_DIR, 'data', 'events_summary.json')
with open(summary_path, 'w', encoding='utf-8') as fh:
    fh.write(trimmed_events_str)
dist_data_dir = os.path.join(ROOT_DIR, 'dist', 'data')
if os.path.exists(dist_data_dir):
    with open(os.path.join(dist_data_dir, 'events_summary.json'), 'w', encoding='utf-8') as fh:
        fh.write(trimmed_events_str)
print(f"✅ Built {summary_path} ({len(trimmed_events)} slimmed event summaries)")

# ─────────────────── 旧事件 ID URL → canonical slug ───────────────────
REDIRECTS_FILE = os.path.join(ROOT_DIR, '_redirects')
REDIRECTS_BASE = (
    '# Host-level www → apex redirects must be configured with a Cloudflare\n'
    '# Single Redirect. Pages _redirects rules only match paths.\n\n'
    '# Canonical\n'
    '/index.html / 301'
)
REDIRECTS_START = '# BEGIN GENERATED EVENT ID REDIRECTS'
REDIRECTS_END = '# END GENERATED EVENT ID REDIRECTS'
FUNCTIONS_EVENT_ROUTES_FILE = os.path.join(
    ROOT_DIR, 'functions', 'event-routes.generated.js'
)

def generate_event_id_redirects(events):
    """Keep legacy ID-based event URLs working while canonical pages use slugs."""
    rules = []
    for event in sorted(events, key=lambda item: item['id']):
        event_id = event['id']
        slug = event.get('slug', event_id)
        if slug == event_id:
            continue
        for prefix in ('', '/zh-hans'):
            source = f'{prefix}/events/{event_id}'
            target = f'{prefix}/events/{slug}/'
            rules.extend([
                f'{source} {target} 301',
                f'{source}/ {target} 301',
                f'{source}/index.html {target} 301',
            ])

    generated = '\n'.join([REDIRECTS_START, *rules, REDIRECTS_END])
    content = f'{REDIRECTS_BASE}\n\n{generated}\n'
    with open(REDIRECTS_FILE, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f"✅ Generated {len(rules)} legacy event redirect rule(s)")

generate_event_id_redirects(events)

# ─────────────────── Pages middleware event route & direction ID map ───────────────────
def generate_event_route_map(events):
    """Generate the ID/slug lookup and valid direction IDs for Pages Functions."""
    routes = {}
    for event in sorted(events, key=lambda item: item['id']):
        event_id = event['id']
        slug = event.get('slug', event_id)
        routes[event_id] = slug
        routes[slug] = slug

    forecasts_path = os.path.join(ROOT_DIR, 'data', 'forecasts.json')
    forecast_ids = []
    if os.path.exists(forecasts_path):
        with open(forecasts_path, 'r', encoding='utf-8') as fh:
            forecast_ids = sorted({item['id'] for item in json.load(fh) if isinstance(item, dict) and item.get('id')})

    content = (
        '// Generated by scripts/build_events.py. Do not edit manually.\n'
        'export const EVENT_ROUTES = Object.freeze('
        f'{json.dumps(routes, ensure_ascii=False, sort_keys=True, indent=2)}'
        ');\n'
        'export const FORECAST_IDS = Object.freeze('
        f'{json.dumps(forecast_ids, ensure_ascii=False)}'
        ');\n'
    )
    with open(FUNCTIONS_EVENT_ROUTES_FILE, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f"✅ Generated Pages event route map with {len(routes)} aliases and {len(forecast_ids)} direction IDs")

generate_event_route_map(events)
