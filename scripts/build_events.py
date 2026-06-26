#!/usr/bin/env python3
"""Build data/events.json from content/events/*.json with full validation"""
import json, os, glob, sys

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
