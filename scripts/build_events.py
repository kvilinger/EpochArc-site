#!/usr/bin/env python3
"""Build data/events.json from content/events/*.json"""
import json, os, glob

EVENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content', 'events')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'events.json')

events = []
for f in sorted(glob.glob(os.path.join(EVENTS_DIR, '*.json'))):
    with open(f) as fh:
        events.append(json.load(fh))

# Validate
ids = [e['id'] for e in events]
for i, eid in enumerate(ids):
    if eid in ids[:i]:
        raise SystemExit(f"Duplicate event ID: {eid}")

VALID_CATEGORIES = {'capability', 'product', 'commerce', 'governance', 'safety', 'society'}
for e in events:
    cats = e.get('categories', [])
    if not cats or len(cats) > 2:
        raise SystemExit(f"Invalid categories in {e['id']}: must have 1-2 categories, got {len(cats)}")
    for c in cats:
        if c not in VALID_CATEGORIES:
            raise SystemExit(f"Unknown category '{c}' in {e['id']}. Valid: {sorted(VALID_CATEGORIES)}")
    # Check for pre-migration category field
    if 'category' in e:
        raise SystemExit(f"Stale 'category' field in {e['id']} — must use 'categories' array")

# Check bidirectional relatedEvents
for e in events:
    for rel_id in e.get('relatedEvents', []):
        if rel_id not in ids:
            pass  # future events may not exist yet
        else:
            rel_event = next(ev for ev in events if ev['id'] == rel_id)
            if e['id'] not in rel_event.get('relatedEvents', []):
                print(f"Warning: {e['id']} → {rel_id}, but {rel_id} does not reference back")

with open(OUTPUT_FILE, 'w') as fh:
    json.dump(events, fh, ensure_ascii=False, indent=2)

print(f"Built {OUTPUT_FILE} with {len(events)} events")
