#!/usr/bin/env python3
"""Read-only audit of live editorial sources. Prints JSON; never changes ratings."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from editorial_policy import load, digest

ROOT = Path(__file__).resolve().parent.parent


def audit(root=ROOT):
    events = [load(p) for p in sorted((root / 'content/events').glob('*.json'))]
    events = [e for e in events if e.get('status') == 'published']
    sources = {s['id']: s for s in load(root / 'data/sources.json')}
    entries = load(root / 'data/screening_log.json')['entries']
    matched = {e.get('eventId') for e in entries}
    results = []
    for e in events:
        ed = e['editorial']
        refs = {s['sourceId'] for s in e['sources']}
        flags = []
        if ed.get('reviewProvenance') != 'v2.4':
            flags.append('NO_V24_EVIDENCE_AND_RATING_REVIEW')
        if e['id'] not in matched:
            flags.append('NO_LEGACY_SCREENING_EVENT_LINK')
        if e['significance'] >= 2 and not ed.get('reviewRecord'):
            flags.append('NO_STRUCTURED_L2_L3_RATIONALE')
        if any(not sources[s].get('accessedAt') for s in refs):
            flags.append('SOURCE_ACCESS_DATE_MISSING')
        if any(sources[s].get('type') == 'encyclopedia' and sources[s]['tier'] < 3 for s in refs):
            flags.append('ENCYCLOPEDIA_TIER_DEBT')
        if any(not i.get('observedSince') for i in e['impacts']) and ed.get('reviewProvenance') != 'v2.4':
            flags.append('IMPACT_DURATION_NOT_OBSERVATION_DATED')
        results.append({
            'eventId': e['id'], 'digest': digest(e), 'significance': e['significance'],
            'impactIndex': e['impactIndex'], 'createdAt': ed['createdAt'],
            'publishedAt': ed.get('publishedAt'), 'updatedAt': ed['updatedAt'],
            'reviewPriority': 'P0' if e['significance'] == 3 else 'P1' if e['significance'] == 2 else 'P2',
            'disposition': 'retain_pending_evidence_review' if flags else 'contract_reviewed',
            'flags': flags,
        })
    results.sort(key=lambda r: (r['reviewPriority'], r['eventId']))
    return {
        'auditType': 'offline_contract_audit_not_fact_verification',
        'scope': 'canonical published events only; excludes all draft packages',
        'publishedEventCount': len(events),
        'significanceCounts': dict(sorted(Counter(e['significance'] for e in events).items())),
        'flagCounts': dict(sorted(Counter(f for r in results for f in r['flags']).items())),
        'sourceCount': len(sources),
        'sourceMissingAccessedAt': sum(not s.get('accessedAt') for s in sources.values()),
        'results': results,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
