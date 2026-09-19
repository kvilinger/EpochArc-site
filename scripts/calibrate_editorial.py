#!/usr/bin/env python3
"""Offline rule replay and comparison of independently produced model outputs.

No browsing, model calls, canonical writes, rating updates or approvals.
"""
import argparse
import itertools
import json
from pathlib import Path
from editorial_policy import load, digest, criteria_met

ROOT = Path(__file__).resolve().parent.parent


def evaluate(case, policy):
    """Evaluate a explicitly synthetic, adjudicated fact vector, not prose truth."""
    if case['kind'] == 'published_snapshot':
        return {'decision': 'review_required', 'significance': None}
    inputs = case['inputs']
    if inputs.get('coreFactVerified') is not True:
        return {'decision': 'hold', 'significance': None}
    categories = {policy['l2Rules'][r['ruleId']]['category'] for r in inputs['routes']
                  if criteria_met(r['ruleId'], r['values'], policy)}
    level = 2 if categories else 1
    l3 = policy['l3']
    if (len(categories) >= l3['minimumCategories']
            and inputs.get('observedDays', 0) >= l3['minimumObservedDays']
            and inputs.get('independentOrigins', 0) >= l3['minimumIndependentOrigins']
            and inputs.get('independentPublishers', 0) >= l3['minimumIndependentOrigins']
            and inputs.get('hasPrimary') is True and inputs.get('coreGradesAtLeastB') is True):
        level = 3
    return {'decision': inputs.get('identityDecision', 'new'), 'significance': level}


def replay(suite, policy):
    errors = []
    if suite['policyDigest'] != digest(policy):
        errors.append('policy changed: recalibrate and explicitly version the suite')
    for case in suite['cases']:
        actual = evaluate(case, policy)
        if actual != case['expected']:
            errors.append({'caseId': case['id'], 'expected': case['expected'], 'actual': actual})
    return {'mode': 'deterministic_rule_replay_not_model_agreement', 'caseCount': len(suite['cases']),
            'passed': len(suite['cases']) - sum(isinstance(e, dict) for e in errors), 'errors': errors}


def compare(suite, policy, outputs):
    if len(outputs) < 2:
        raise ValueError('need at least two independent output files')
    expected_ids = {c['id'] for c in suite['cases']}
    indexes, seen_sessions = [], set()
    for output in outputs:
        if output.get('suiteDigest') != digest(suite) or output.get('policyDigest') != digest(policy):
            raise ValueError('outputs must bind the same frozen suite and policy')
        if not output.get('model') or not output.get('sessionId') or output['sessionId'] in seen_sessions:
            raise ValueError('real model and distinct sessionId required; never fabricate runs')
        seen_sessions.add(output['sessionId'])
        rows = output['results']
        index = {r['caseId']: r for r in rows}
        if set(index) != expected_ids or len(index) != len(rows):
            raise ValueError('every case required exactly once; do not drop disagreements or abstentions')
        for r in rows:
            if r.get('decision') not in {'skip', 'hold', 'new', 'update', 'merge', 'review_required'}:
                raise ValueError('invalid decision')
            if r.get('significance') is not None and (type(r['significance']) is not int or r['significance'] not in {1, 2, 3}):
                raise ValueError('invalid significance')
            if r.get('impactIndex') is not None and (type(r['impactIndex']) is not int or not 0 <= r['impactIndex'] <= 10):
                raise ValueError('invalid impactIndex')
        indexes.append(index)
    pairs = []
    total = len(expected_ids)
    for a, b in itertools.combinations(range(len(outputs)), 2):
        left, right = indexes[a], indexes[b]
        # Null agreement is reported but cannot inflate significance or impact coverage.
        graded = [k for k in expected_ids if left[k]['significance'] is not None and right[k]['significance'] is not None]
        impacts = [k for k in expected_ids if left[k].get('impactIndex') is not None and right[k].get('impactIndex') is not None]
        disagreements = [k for k in expected_ids if any(left[k].get(f) != right[k].get(f) for f in ('decision', 'significance', 'impactIndex'))]
        ratio = lambda n, d: n / d if d else None
        pairs.append({'left': outputs[a]['sessionId'], 'right': outputs[b]['sessionId'],
                      'decisionAgreement': ratio(sum(left[k]['decision'] == right[k]['decision'] for k in expected_ids), total),
                      'significanceAgreement': ratio(sum(left[k]['significance'] == right[k]['significance'] for k in graded), len(graded)),
                      'significanceCoverage': ratio(len(graded), total),
                      'impactWithinOne': ratio(sum(abs(left[k]['impactIndex'] - right[k]['impactIndex']) <= 1 for k in impacts), len(impacts)),
                      'impactCoverage': ratio(len(impacts), total), 'disagreements': sorted(disagreements)})
    return {'mode': 'recorded_model_outputs_comparison', 'models': [x['model'] for x in outputs],
            'caseCount': total, 'pairs': pairs, 'certified': False,
            'note': 'Agreement is not accuracy. Independently adjudicate evidence/rule violations; no auto-certification or self-reported zero-violation acceptance.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare', nargs='+', type=Path)
    args = parser.parse_args()
    policy = load(ROOT / 'governance/policy.json')
    suite = load(ROOT / 'governance/calibration/cases.json')
    result = compare(suite, policy, [load(p) for p in args.compare]) if args.compare else replay(suite, policy)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get('errors') else 0


if __name__ == '__main__':
    raise SystemExit(main())
