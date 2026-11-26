#!/usr/bin/env python3
"""Read-only batch risk report, NOT a fact review, score setter, or publication gate.

Usage: python3 -B scripts/report_impact_batch.py governance/runs/<run>.json
Warnings ask for source-specific inspection; they never prove missing impacts.
"""
import json
from collections import Counter
from pathlib import Path
import sys
from editorial_policy import safe_file

ROOT = Path(__file__).resolve().parent.parent

def inspect_batch(run, events):
    if not isinstance(run, dict) or not isinstance(run.get('candidates'), list):
        raise ValueError('run candidates must be an array')
    rows, flags, ids = [], [], set()
    for c in run['candidates']:
        if not isinstance(c, dict):
            raise ValueError('candidate must be object')
        if c.get('decision') not in {'new', 'update', 'merge'}:
            continue
        eid = c.get('eventId')
        if not isinstance(eid, str) or not eid or eid in ids or eid not in events:
            raise ValueError('selected event missing/duplicate/unknown')
        ids.add(eid)
        e = events[eid]
        if not isinstance(e.get('impacts'), list):
            raise ValueError('impacts must be an array; unknown is not an empty assessment')
        layer = c.get('confirmation', {}).get('impact', {})
        if not isinstance(layer, dict):
            raise ValueError('impact confirmation must be object')
        finding = layer.get('finding')
        if not isinstance(finding, str) or not finding.strip():
            flags.append({'code': 'MISSING_IMPACT_REASON', 'eventId': eid})
            finding = ''
        rows.append({'id': eid, 'significance': e.get('significance'),
                     'impactIndex': e.get('impactIndex'), 'impactCount': len(e['impacts']),
                     'impactConfirmationStatus': layer.get('status'),
                     'finding': finding})
        if not e['impacts'] and layer.get('status') == 'found':
            flags.append({'code': 'FOUND_BUT_UNSCORED_REQUIRES_DISPOSITION', 'eventId': eid})
        if not e['impacts'] and 'independent' in finding.lower() and any(x in finding.lower() for x in ('adoption', 'external change', 'attributable use')):
            flags.append({'code': 'CHECK_ADOPTION_NOT_USED_AS_UNIVERSAL_IMPACT_REQUIREMENT', 'eventId': eid})
    if len(rows) >= 3 and all(r['impactCount'] == 0 and r['impactIndex'] == 0 for r in rows):
        flags.append({'code': 'UNIFORM_EMPTY_IMPACTS_REVIEW_SOURCES', 'count': len(rows)})
    counts = Counter(' '.join(r['finding'].split()) for r in rows if r['finding'])
    for finding, count in counts.items():
        if count >= 3:
            flags.append({'code': 'REPEATED_IMPACT_REASON_REVIEW_SOURCES', 'count': count, 'finding': finding})
    return {'mode': 'READ_ONLY_RISK_REPORT_NOT_FACT_REVIEW_OR_GATE',
            'notice': 'Empty impacts means no scored entries, not measured zero. Flags do not prescribe a score or prove an error; inspect complete sources and record each candidate outcome.',
            'selectedCount': len(rows), 'unscoredCount': sum(x['impactCount'] == 0 for x in rows),
            'rows': rows, 'flags': flags}

def report(root, relative):
    path = safe_file(root, relative, 'governance/runs')
    if path is None:
        raise ValueError('run must be an existing file under governance/runs')
    events = {}
    for p in sorted((root/'content/events').glob('*.json')):
        e = json.loads(p.read_text())
        if not isinstance(e, dict) or not isinstance(e.get('id'), str) or not e['id'] or e['id'] in events:
            raise ValueError('invalid or duplicate event id')
        events[e['id']] = e
    return inspect_batch(json.loads(path.read_text()), events)

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('provide exactly one governance/runs/<run>.json path')
        print(json.dumps(report(ROOT, sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({'mode':'REPORT_FAILED_NOT_APPROVAL','error':str(exc)}, ensure_ascii=False))
        sys.exit(1)
