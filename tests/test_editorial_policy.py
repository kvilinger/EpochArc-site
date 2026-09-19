"""Synthetic contracts only. No fixture is a real event, review or human approval."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import editorial_policy as ep
import validate_all as core


def save(root, relative, data):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def localized(value):
    return {'en': value, 'zhHans': '合成测试：' + value}


class Contracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.policy = ep.load(ROOT / 'governance/policy.json')
        save(self.root, 'governance/policy.json', self.policy)
        rules = self.root / self.policy['rulesDocument']
        rules.parent.mkdir(parents=True)
        rules.write_bytes((ROOT / self.policy['rulesDocument']).read_bytes())
        raw = 'SYNTHETIC TEST ONLY. Company released software. Two unaffiliated organizations use a new production workflow. Independent investigators verified the deployments.'
        path = self.root / 'governance/evidence/test.txt'
        path.parent.mkdir(parents=True)
        path.write_text(raw)
        self.sha = hashlib.sha256(raw.encode()).hexdigest()
        self.sources = {
            'p': {'id': 'p', 'title': 'Synthetic primary', 'url': 'https://example.com/p', 'tier': 1, 'type': 'official', 'independence': 'primary_actor', 'publisherId': 'company', 'originId': 'company-record', 'publishedAt': '2026-01-01', 'accessedAt': '2026-09-18'},
            'i': {'id': 'i', 'title': 'Synthetic investigation', 'url': 'https://example.org/i', 'tier': 2, 'type': 'news', 'independence': 'independent', 'publisherId': 'investigator', 'originId': 'fieldwork', 'publishedAt': '2026-07-01', 'accessedAt': '2026-09-18'},
        }
        self.run = {'policyVersion': '2.4', 'runId': 'synthetic-run', 'kind': 'full', 'windowStart': '2026-01-01', 'windowEnd': '2026-09-18', 'evidenceCutoff': '2026-09-18', 'timezone': 'UTC', 'baselineCommit': 'a' * 40, 'operator': 'test-producer', 'model': 'synthetic-model', 'promptVersion': 'test-v1',
                    'channels': [{'id': cid, 'status': 'complete', 'windowCovered': True, 'coverageNote': 'Synthetic bounded fixture', 'attempts': [{'query': 'synthetic query', 'executedAt': '2026-09-18T00:00:00Z', 'artifact': 'governance/evidence/test.txt', 'sha256': self.sha, 'resultCount': 1}]} for cid in self.policy['coreChannels']],
                    'categoryCoverage': [{'category': c, 'status': 'complete', 'finding': 'synthetic fixture only'} for c in self.policy['categories']],
                    'candidates': [{'candidateId': 'c', 'eventId': 'test-event', 'scores': {k: 2 for k in self.policy['screeningFields']}, 'scoreReasons': {k: 'Synthetic evidence' for k in self.policy['screeningFields']}, 'total': 10, 'priority': 'confirm', 'decision': 'new', 'reason': 'New synthetic action', 'discoveryUrls': ['https://example.com/p'], 'confirmation': {k: {'status': 'found' if k in {'fact', 'impact'} else 'not_found', 'query': 'synthetic ' + k, 'finding': 'Synthetic finding', 'evidenceIds': ['ef'] if k == 'fact' else ['ei'] if k == 'impact' else []} for k in ['fact', 'impact', 'analysis', 'controversy']}}]}
        self.record = {'id': 'test-event', 'slug': 'test-event', 'title': localized('Software release'), 'searchSummary': localized('A production workflow.'), 'summary': localized('The company released software.'), 'narrative': localized('A bounded synthetic event for tests.'), 'date': '2026-01-01', 'datePrecision': 'day', 'categories': ['product'], 'status': 'published', 'significance': 2, 'impactIndex': 4, 'consensusLevel': 'emerging', 'controversy': False,
                       'sources': [{'sourceId': 'p', 'supports': ['fact', 'impact']}, {'sourceId': 'i', 'supports': ['impact']}],
                       'claims': [{'id': 'fact', 'claimType': 'fact', 'text': localized('Company released software.'), 'evidenceGrade': 'B', 'sourceIds': ['p']}, {'id': 'impact', 'claimType': 'impact', 'text': localized('Two independent deployments'), 'evidenceGrade': 'A', 'sourceIds': ['p', 'i']}],
                       'impacts': [{'dimension': 'access_democratization', 'severity': 2, 'direction': 'positive', 'description': localized('New workflow in production'), 'affectedGroups': ['developers', 'businesses'], 'timeframe': 'medium', 'evidenceGrade': 'A', 'sourceIds': ['p', 'i']}], 'relatedEvents': [],
                       'editorial': {'createdAt': '2026-09-18', 'updatedAt': '2026-09-18', 'reviewedAt': '2026-09-18', 'lastSourceCheckAt': '2026-09-18', 'publishedAt': '2026-09-18', 'curator': 'test-producer', 'reviewer': 'test-reviewer', 'reviewProvenance': 'v2.4', 'reviewRecord': 'governance/reviews/test.json', 'changeLog': [{'date': '2026-09-18', 'changeType': 'created', 'summary': 'SYNTHETIC fixture, not a real review.'}]}}
        self.events = {'test-event': self.record, 'example-a': {'id': 'example-a', 'status': 'published'}, 'example-b': {'id': 'example-b', 'status': 'published'}}
        evidence = []
        for eid, sid, claim, relation, mode, quote in [('ef', 'p', 'fact', 'primary', 'direct', 'Company released software.'), ('ep', 'p', 'impact', 'primary', 'direct', 'Two unaffiliated organizations use a new production workflow.'), ('ei', 'i', 'impact', 'independent', 'independent_verification', 'Independent investigators verified the deployments.')]:
            evidence.append({'id': eid, 'sourceId': sid, 'claimId': claim, 'url': self.sources[sid]['url'], 'originId': self.sources[sid]['originId'], 'accessedAt': '2026-09-18', 'relationship': relation, 'verification': mode, 'quote': quote, 'locator': 'Synthetic test paragraph', 'artifact': 'governance/evidence/test.txt', 'sha256': self.sha})
        self.review = {'policyVersion': '2.4', 'kind': 'event', 'subjectId': 'test-event', 'evidenceCutoff': '2026-09-18', 'preparedBy': 'test-producer', 'model': 'synthetic-model', 'reviewedBy': 'test-reviewer', 'reviewMethod': 'independent_model', 'producerSessionId': 'session-1', 'reviewerSessionId': 'session-2', 'reviewerModel': 'synthetic-review-model', 'limitations': ['SYNTHETIC, no factual assertion or human action'], 'languageReview': {'factsAligned': True, 'notes': 'Synthetic fixture'}, 'evidence': evidence, 'runId': 'synthetic-run', 'candidateId': 'c', 'coreFactClaimIds': ['fact'],
                       'identity': {'seriesId': 'test-series', 'action': 'release', 'stage': 'available', 'dateBasis': 'Synthetic primary dated record', 'deduplicationReason': 'Different action from comparison records', 'comparedEventIds': ['example-a'], 'decision': 'new'},
                       'classification': {'primary': 'product', 'reason': 'The action changes workflow'},
                       'significance': {'rationale': 'Observed workflow change', 'whyNotHigher': 'Insufficient duration and categories for L3', 'whyNotLower': 'Meets production workflow route', 'comparisonEventIds': ['example-a', 'example-b'], 'routes': [{'ruleId': 'L2-PRODUCT', 'criteria': {'new_workflow': {'value': True, 'rationale': 'A measured change', 'evidenceIds': ['ei']}, 'unaffiliated_production_organizations': {'value': 2, 'entityIds': ['org-a', 'org-b'], 'rationale': 'Two independent controls', 'evidenceIds': ['ei']}}}]},
                       'impactBasis': [{'dimension': 'access_democratization', 'observation': 'observed', 'evidenceIds': ['ep', 'ei'], 'observedSince': '2026-01-01', 'observedUntil': '2026-07-01', 'baseline': 'Old workflow', 'outcome': 'New workflow', 'materialChange': True}], 'consensus': {'level': 'emerging', 'reason': 'Limited evidence', 'evidenceIds': []}, 'dispute': {'exists': False, 'reason': 'None documented in synthetic fixture', 'evidenceIds': []}}
        self.baseline = {'events': {k: {'digest': ep.digest(v), 'slug': k, 'status': 'published'} for k, v in self.events.items() if k != 'test-event'}, 'arcs': {}, 'directions': {}, 'sources': {}, 'legacyLogs': {}}
        save(self.root, 'governance/legacy-baseline.json', self.baseline)
        self.sync()

    def sync(self, approve=True):
        self.record['impactIndex'] = core.calculate_impact_index(self.record)
        self.review['policyDigest'] = ep.digest(self.policy)
        self.review['subjectDigest'] = ep.digest(self.record)
        self.review['inputsDigest'] = ep.review_inputs('event', self.record, self.sources, self.events)
        self.review['runDigest'] = ep.digest(self.run)
        save(self.root, 'governance/runs/test.json', self.run)
        save(self.root, 'governance/reviews/test.json', self.review)
        if approve:
            approval = {'subjectId': self.record['id'], 'subjectDigest': ep.digest(self.record), 'reviewDigest': ep.digest(self.review), 'policyDigest': ep.digest(self.policy), 'decision': 'approve', 'actorType': 'human', 'actor': 'SYNTHETIC-NOT-A-PERSON', 'approvedAt': '2026-09-18', 'confirmationRef': 'synthetic-test-only'}
            save(self.root, 'governance/approvals/' + ep.digest(self.record) + '.json', approval)

    def review_errors(self):
        self.sync()
        return ep.validate_review(self.root, 'event', self.record, self.review, self.policy, self.sources, self.events, {self.run['runId']: self.run})

    def policy_errors(self):
        return ep.validate_policy(self.root, self.events, self.sources, [], [])[0]

    def assertRejected(self, errors, fragment):
        self.assertTrue(errors, fragment)
        self.assertIn(fragment, '\n'.join(errors))

    def test_positive_l2_end_to_end(self):
        self.assertEqual([], ep.validate_run(self.run, self.policy))
        self.assertEqual([], self.review_errors())
        self.assertEqual([], self.policy_errors())

    def test_core_and_policy_accept_same_valid_record(self):
        save(self.root, 'content/events/test-event.json', self.record)
        core.errors.clear(); core.warnings.clear()
        with patch.object(core, 'EVENT_GLOB', str(self.root / 'content/events/*.json')):
            core.validate_events(self.sources)
        self.assertEqual([], core.errors)
        self.assertEqual([], self.policy_errors())

    def test_valid_l1_no_observed_impact(self):
        self.record['significance'] = 1
        self.record['impacts'] = []
        self.review['impactBasis'] = []
        criterion = self.review['significance']['routes'][0]['criteria']['unaffiliated_production_organizations']
        criterion.update(value=None, evidenceIds=[], rationale='Not measured')
        self.assertEqual([], self.review_errors())
        self.assertEqual(0, self.record['impactIndex'])

    def test_missing_screening_link(self):
        self.review['candidateId'] = 'missing'
        self.assertRejected(self.review_errors(), 'matching selected candidate')

    def test_full_run_cannot_omit_channels(self):
        self.run['channels'] = self.run['channels'][:1]
        self.assertRejected(ep.validate_run(self.run, self.policy), 'every core channel')

    def test_targeted_run_can_use_one_channel(self):
        self.run.update(kind='targeted', scopeReason='Single-event recheck')
        self.run['channels'] = self.run['channels'][:1]
        self.assertEqual([], ep.validate_run(self.run, self.policy))

    def test_partial_run_is_honest_not_failure(self):
        c = self.run['channels'][0]
        c.update(status='partial', windowCovered=False, reason='Only latest snapshot', retryResult='No historical endpoint available')
        self.assertEqual([], ep.validate_run(self.run, self.policy))

    def test_snapshot_is_not_complete_window(self):
        self.run['channels'][0]['windowCovered'] = False
        self.assertRejected(ep.validate_run(self.run, self.policy), 'window coverage')

    def test_found_confirmation_needs_evidence(self):
        self.run['candidates'][0]['confirmation']['fact']['evidenceIds'] = []
        self.assertRejected(ep.validate_run(self.run, self.policy), 'found layer')

    def test_boolean_score_is_not_integer(self):
        self.run['candidates'][0]['scores']['novelty'] = True
        self.assertRejected(ep.validate_run(self.run, self.policy), 'integer dimensions')

    def test_unknown_l2_condition_not_satisfied(self):
        self.review['significance']['routes'][0]['criteria']['new_workflow'].update(value=None, evidenceIds=[])
        self.assertRejected(self.review_errors(), 'satisfied milestone route')

    def test_same_company_entities_not_counted_twice(self):
        self.review['significance']['routes'][0]['criteria']['unaffiliated_production_organizations']['entityIds'] = ['a', 'a']
        self.assertRejected(self.review_errors(), 'distinct entityIds')

    def test_unknown_rule(self):
        self.review['significance']['routes'][0]['ruleId'] = 'L2-FAMOUS-BRAND'
        self.assertRejected(self.review_errors(), 'unknown significance rule')

    def test_no_routes_not_valid_l1_shortcut(self):
        self.record['significance'] = 1
        self.review['significance']['routes'] = []
        self.assertRejected(self.review_errors(), 'at least one relevant')

    def test_l3_one_category_rejected(self):
        self.record['significance'] = 3
        self.assertRejected(self.review_errors(), 'distinct milestone categories')

    def test_future_observation_not_counted(self):
        self.review['impactBasis'][0]['observedUntil'] = '2027-01-01'
        self.assertRejected(self.review_errors(), 'impact observed dates')

    def test_forecast_does_not_contribute_index(self):
        self.review['impactBasis'][0]['observation'] = 'expected'
        self.assertRejected(self.review_errors(), 'unobserved impacts')

    def test_timeframe_derived_not_selected(self):
        self.record['impacts'][0]['timeframe'] = 'long'
        self.assertRejected(self.review_errors(), 'timeframe must derive')

    def test_synonyms_cannot_inflate_scope(self):
        self.record['impacts'][0]['affectedGroups'] = ['developers', 'coders', 'programmers']
        self.assertRejected(self.review_errors(), 'canonical audience IDs')

    def test_severity_three_needs_breadth(self):
        self.record['impacts'][0].update(severity=3, affectedGroups=['developers'])
        self.assertRejected(self.review_errors(), 'severity 3 breadth')

    def test_missing_metadata(self):
        for key in ['curator', 'changeLog', 'lastSourceCheckAt', 'publishedAt']:
            with self.subTest(key=key):
                value = self.record['editorial'].pop(key)
                self.assertRejected(self.review_errors(), key)
                self.record['editorial'][key] = value

    def test_missing_source_access(self):
        del self.sources['p']['accessedAt']
        self.sync()
        self.assertRejected(self.policy_errors(), 'accessedAt')

    def test_same_session_not_independent_review(self):
        self.review['reviewerSessionId'] = self.review['producerSessionId']
        self.assertRejected(self.review_errors(), 'distinct session')

    def test_self_review_not_enough_l2(self):
        self.review['reviewMethod'] = 'self_review'
        self.assertRejected(self.review_errors(), 'self-review only')

    def test_quote_must_be_in_artifact(self):
        self.review['evidence'][0]['quote'] = 'Invented statement'
        self.assertRejected(self.review_errors(), 'quote absent')

    def test_artifact_change_invalidates_evidence(self):
        (self.root / 'governance/evidence/test.txt').write_text('changed')
        self.assertRejected(self.review_errors(), 'artifact hash')

    def test_path_escape_rejected(self):
        self.review['evidence'][0]['artifact'] = '../../outside.txt'
        self.assertRejected(self.review_errors(), 'outside governance/evidence')

    def test_stale_subject_review(self):
        self.record['title']['en'] = 'Different title'
        self.assertRejected(self.policy_errors(), 'stale review digest')

    def test_stale_dependency_review(self):
        self.sources['i']['originId'] = 'different-origin'
        self.assertRejected(self.policy_errors(), 'inputsDigest')

    def test_stale_run_review(self):
        self.run['operator'] = 'changed-operator'
        save(self.root, 'governance/runs/test.json', self.run)
        self.assertRejected(self.policy_errors(), 'runDigest')

    def test_stale_review_approval(self):
        self.review['limitations'].append('New limit')
        save(self.root, 'governance/reviews/test.json', self.review)
        self.assertRejected(self.policy_errors(), 'explicit human approval')

    def test_policy_change_invalidates_approval(self):
        self.policy['revision'] = '2.4.1'
        save(self.root, 'governance/policy.json', self.policy)
        self.assertRejected(self.policy_errors(), 'explicit human approval')

    def test_rule_text_change_invalidates_policy(self):
        (self.root / self.policy['rulesDocument']).write_text('Changed semantics without a policy revision')
        self.assertRejected(self.policy_errors(), 'rule text changed')

    def test_missing_human_approval(self):
        for p in (self.root / 'governance/approvals').glob('*.json'):
            p.unlink()
        self.assertRejected(self.policy_errors(), 'explicit human approval')

    def test_legacy_flag_cannot_bypass(self):
        self.record['editorial']['reviewProvenance'] = 'legacy_pre_v23'
        self.assertRejected(self.policy_errors(), 'legacy flags cannot bypass')

    def test_frozen_legacy_record_allowed(self):
        self.record['editorial']['reviewProvenance'] = 'legacy_pre_v23'
        self.baseline['events']['test-event'] = {'digest': ep.digest(self.record), 'slug': 'test-event', 'publishedAt': '2026-09-18', 'status': 'published'}
        self.baseline['sources'] = {k: ep.digest(v) for k, v in self.sources.items()}
        save(self.root, 'governance/legacy-baseline.json', self.baseline)
        self.assertEqual([], self.policy_errors())
        self.record['significance'] = 3
        self.assertRejected(self.policy_errors(), 'legacy flags cannot bypass')

    def test_first_publication_date_immutable(self):
        self.baseline['events']['test-event'] = {'digest': 'old', 'slug': 'test-event', 'publishedAt': '2026-08-01', 'status': 'published'}
        save(self.root, 'governance/legacy-baseline.json', self.baseline)
        self.assertRejected(self.policy_errors(), 'publishedAt is immutable')

    def test_deleted_public_record_blocked(self):
        del self.events['example-a']
        self.assertRejected(self.policy_errors(), 'cannot disappear')

    def test_unpublished_comparison_rejected(self):
        self.events['example-a']['status'] = 'draft'
        self.assertRejected(self.review_errors(), 'published comparable')

    def test_syndicated_origin_not_independent_verification(self):
        self.review['evidence'][2]['originId'] = 'company-record'
        self.assertRejected(self.review_errors(), 'syndicated or Tier 4')

    def test_only_community_evidence_is_d(self):
        self.sources['i'].update(tier=4, type='community')
        self.assertEqual('D', ep.evidence_ceiling([self.review['evidence'][2]], self.sources))
        self.assertEqual('D', core.maximum_supported_evidence_grade(['i'], self.sources))
        self.assertRejected(self.review_errors(), 'syndicated or Tier 4')

    def test_no_independent_performance_validation_no_a(self):
        self.review['evidence'][2]['verification'] = 'reported'
        self.assertEqual('B', ep.evidence_ceiling(self.review['evidence'][1:], self.sources))
        self.assertRejected(self.review_errors(), 'grade exceeds')

    def test_malformed_contracts_fail_closed(self):
        for field, value in [('channels', None), ('candidates', [None]), ('categoryCoverage', [None])]:
            with self.subTest(field=field):
                run = copy.deepcopy(self.run); run[field] = value
                self.assertTrue(ep.validate_run(run, self.policy))
        for field in ['evidence', 'significance', 'impactBasis']:
            review = copy.deepcopy(self.review); review[field] = None
            self.assertTrue(ep.validate_review(self.root, 'event', self.record, review, self.policy, self.sources, self.events, {self.run['runId']: self.run}))

    def test_deterministic_timeframe_boundaries(self):
        from datetime import date, timedelta
        for n, expected in [(0, 'immediate'), (29, 'immediate'), (30, 'short'), (179, 'short'), (180, 'medium'), (364, 'medium'), (365, 'long')]:
            end = (date(2020, 1, 1) + timedelta(days=n)).isoformat()
            self.assertEqual(expected, ep.derive_timeframe('2020-01-01', end, self.policy))

    def test_every_l2_rule_numeric_and_unknown_boundaries(self):
        for rule_id, rule in self.policy['l2Rules'].items():
            with self.subTest(rule=rule_id):
                values = dict(rule['criteria'])
                self.assertTrue(ep.criteria_met(rule_id, values, self.policy))
                for key, threshold in rule['criteria'].items():
                    below = dict(values); below[key] = False if type(threshold) is bool else threshold - 1
                    self.assertFalse(ep.criteria_met(rule_id, below, self.policy))
                    unknown = dict(values); unknown[key] = None
                    self.assertFalse(ep.criteria_met(rule_id, unknown, self.policy))

    def test_duplicate_impact_does_not_increase_score(self):
        before = core.calculate_impact_index(self.record)
        self.record['impacts'].append(copy.deepcopy(self.record['impacts'][0]))
        self.assertEqual(before, core.calculate_impact_index(self.record))

    def test_core_rejects_published_to_draft_reference(self):
        save(self.root, 'content/events/test-event.json', {**self.record, 'relatedEvents': ['draft-node']})
        draft = copy.deepcopy(self.record); draft.update(id='draft-node', slug='draft-node', status='draft')
        save(self.root, 'content/events/draft-node.json', draft)
        core.errors.clear(); core.warnings.clear()
        with patch.object(core, 'EVENT_GLOB', str(self.root / 'content/events/*.json')):
            core.validate_events(self.sources)
        self.assertRejected(core.errors, 'references unpublished')

    def test_positive_l3_and_minimum_duration_boundary(self):
        self.record.update(significance=3, date='2025-01-01')
        self.review['significance'].update(observedSince='2025-01-01', observedUntil='2026-01-01')
        self.review['significance']['routes'].append({'ruleId': 'L2-METHOD', 'criteria': {
            'new_method_or_framework': {'value': True, 'rationale': 'Synthetic method', 'evidenceIds': ['ei']},
            'independent_follow_on_works': {'value': 2, 'entityIds': ['team-a', 'team-b'], 'rationale': 'Independent use', 'evidenceIds': ['ei']}}})
        for sid in ['j', 'k']:
            self.sources[sid] = {**self.sources['i'], 'id': sid, 'url': 'https://example.net/' + sid, 'publisherId': sid, 'originId': sid}
            self.record['sources'].append({'sourceId': sid, 'supports': ['impact']})
            self.record['claims'][1]['sourceIds'].append(sid)
            self.review['evidence'].append({**self.review['evidence'][2], 'id': 'e' + sid, 'sourceId': sid, 'url': self.sources[sid]['url'], 'originId': sid})
        self.assertEqual([], self.review_errors())
        self.review['significance']['observedUntil'] = '2025-12-31'
        self.assertRejected(self.review_errors(), 'observed persistence')
        self.review['significance']['observedUntil'] = '2026-01-01'
        for item in self.review['evidence']:
            if item['relationship'] == 'independent':
                item['originId'] = 'same-fieldwork'
        self.assertRejected(self.review_errors(), 'L3 independent evidence minimum')

    def test_direction_positive_and_unknown_screening_run(self):
        for sid in ['p', 'i']:
            self.sources[sid]['independence'] = 'independent'
        self.events['example-a']['sources'] = [{'sourceId': 'p'}]
        self.events['example-b']['sources'] = [{'sourceId': 'i'}]
        direction = {'id': 'test-direction', 'relatedEvents': ['example-a', 'example-b'],
                     'sources': [{'sourceId': 'p'}, {'sourceId': 'i'}],
                     'editorial': {**self.record['editorial'], 'screeningRunId': self.run['runId']}}
        self.run['directionDecisions'] = [{'id': direction['id'], 'decision': 'publish', 'reason': 'Synthetic direction'}]
        review = {**self.review, 'kind': 'direction', 'subjectId': direction['id'],
                  'subjectDigest': ep.digest(direction), 'inputsDigest': ep.review_inputs('direction', direction, self.sources, self.events),
                  'runDigest': ep.digest(self.run), 'eventIds': ['example-a', 'example-b'],
                  'changeReason': 'Synthetic change', 'counterEvidence': 'Synthetic constraint',
                  'screeningDecision': 'publish', 'consensusSearch': 'No standard found in synthetic data', 'independentSourceIds': ['p', 'i'],
                  'evidence': [{**x, 'relationship': 'independent', 'verification': 'reported'} for x in self.review['evidence']]}
        args = (self.root, 'direction', direction, review, self.policy, self.sources, self.events, {self.run['runId']: self.run})
        self.assertEqual([], ep.validate_review(*args))
        for item in review['evidence']:
            item['originId'] = 'one-report'
        self.assertRejected(ep.validate_review(*args), 'two independent origins')
        direction['editorial']['screeningRunId'] = 'nonexistent'
        self.assertRejected(ep.validate_review(*args), 'screeningRunId must resolve')

    def test_direction_hold_not_publication(self):
        direction = {'id': 'd', 'relatedEvents': ['example-a', 'example-b'], 'sources': self.record['sources'], 'editorial': self.record['editorial']}
        review = {**self.review, 'kind': 'direction', 'subjectId': 'd', 'screeningDecision': 'hold'}
        errors = ep.validate_review(self.root, 'direction', direction, review, self.policy, self.sources, self.events, {})
        self.assertRejected(errors, 'requires publish decision')

    def test_arc_dependency_and_unpublished_anchor(self):
        self.events['example-a']['sources'] = self.record['sources']
        arc = {'id': 'arc', 'chapters': [{'anchorEvents': ['example-a', 'example-b']}], 'editorial': self.record['editorial']}
        review = {**self.review, 'kind': 'arc', 'subjectId': 'arc', 'subjectDigest': ep.digest(arc),
                  'inputsDigest': ep.review_inputs('arc', arc, self.sources, self.events), 'eventIds': ['example-a', 'example-b'],
                  'changeReason': 'Synthetic argument', 'counterEvidence': 'Synthetic alternative interpretation'}
        args = (self.root, 'arc', arc, review, self.policy, self.sources, self.events, {})
        self.assertEqual([], ep.validate_review(*args))
        self.sources['i']['title'] = 'Changed dependency'
        self.assertRejected(ep.validate_review(*args), 'inputsDigest')
        self.events['example-a']['status'] = 'draft'
        self.assertRejected(ep.validate_review(*args), 'references unpublished')

    def test_neutral_is_not_mixed(self):
        self.record['impacts'][0].update(severity=0, direction='neutral')
        self.assertRejected(self.review_errors(), 'neutral cannot conceal mixed')

    def test_core_rejects_boolean_level_and_impossible_date(self):
        invalid = copy.deepcopy(self.record)
        invalid.update(significance=True, date='2026-02-30', impactIndex=True)
        save(self.root, 'content/events/test-event.json', invalid)
        core.errors.clear(); core.warnings.clear()
        with patch.object(core, 'EVENT_GLOB', str(self.root / 'content/events/*.json')):
            core.validate_events(self.sources)
        for fragment in ['significance must', 'invalid calendar date', 'impactIndex must']:
            self.assertRejected(core.errors, fragment)

    def test_publication_needs_human_not_ai_actor(self):
        path = self.root / 'governance/approvals' / (ep.digest(self.record) + '.json')
        approval = ep.load(path); approval['actorType'] = 'ai'
        save(self.root, str(path.relative_to(self.root)), approval)
        self.assertRejected(self.policy_errors(), 'explicit human approval')

    def test_synthetic_impact_anchors(self):
        base = copy.deepcopy(self.record)
        base['impacts'][0].update(severity=1, timeframe='immediate', affectedGroups=['developers'], evidenceGrade='B')
        self.assertEqual(2, core.calculate_impact_index(base))
        base['impacts'][0]['severity'] = -1
        self.assertEqual(2, core.calculate_impact_index(base))
        maximum = copy.deepcopy(self.record)
        maximum['impacts'] = [{**base['impacts'][0], 'dimension': d, 'severity': 3, 'evidenceGrade': 'A', 'timeframe': 'long', 'affectedGroups': ['developers', 'researchers', 'businesses', 'workers']} for d in sorted(core.IMPACT_DIMENSIONS)]
        self.assertEqual(9, core.calculate_impact_index(maximum))


class ExistingStructureBoundaries(unittest.TestCase):
    """Mutate in-memory copies only; no canonical or external draft package writes."""
    def setUp(self):
        self.events = {e['id']: e for e in (ep.load(p) for p in (ROOT / 'content/events').glob('*.json'))}
        self.sources = {s['id']: s for s in ep.load(ROOT / 'data/sources.json')}
        self.forecasts = ep.load(ROOT / 'data/forecasts.json')
        core.errors.clear(); core.warnings.clear()

    def test_direction_confidence_enum(self):
        self.forecasts[0]['confidence']['level'] = 'certain'
        with patch.object(core, 'load_json', return_value=self.forecasts):
            core.validate_forecasts(self.events, self.sources)
        self.assertTrue(any('confidence requires' in e for e in core.errors))

    def test_consensus_gated_requires_external_sources(self):
        self.forecasts[0]['consensusBasis'].update(resolutionMode='consensus_gated', basisType='regulatory_standard', sourceIds=[])
        with patch.object(core, 'load_json', return_value=self.forecasts):
            core.validate_forecasts(self.events, self.sources)
        self.assertTrue(any('requires external sources' in e for e in core.errors))

    def test_monitor_only_cannot_have_private_achievement_threshold(self):
        self.forecasts[0]['consensusBasis']['resolutionMode'] = 'monitor_only'
        self.forecasts[0]['achievedWhen'] = 'synthetic private threshold'
        with patch.object(core, 'load_json', return_value=self.forecasts):
            core.validate_forecasts(self.events, self.sources)
        self.assertTrue(any('private resolution thresholds' in e for e in core.errors))

    def test_public_arc_cannot_link_unpublished_arc(self):
        arcs = [ep.load(p) for p in (ROOT / 'content/arcs').glob('*.json')]
        arcs[0]['relatedArcs'] = [arcs[1]['id']]
        arcs[1]['status'] = 'draft'
        mapping = {str(i): a for i, a in enumerate(arcs)}
        with patch.object(core.glob, 'glob', return_value=list(mapping)), patch.object(core, 'load_json', side_effect=lambda p: mapping[p]):
            core.validate_arcs(self.events)
        self.assertTrue(any('references unpublished arc' in e for e in core.errors))


class Calibration(unittest.TestCase):
    def setUp(self):
        import calibrate_editorial
        self.cal = calibrate_editorial
        self.policy = ep.load(ROOT / 'governance/policy.json')
        self.suite = ep.load(ROOT / 'governance/calibration/cases.json')

    def test_frozen_cases_and_counterfactual_replay(self):
        result = self.cal.replay(self.suite, self.policy)
        self.assertEqual([], result['errors'])
        snapshots = [c for c in self.suite['cases'] if c['kind'] == 'published_snapshot']
        self.assertEqual(16, len(snapshots))
        for case in snapshots:
            snapshot = ep.load(ROOT / case['snapshot'])
            self.assertEqual(case['snapshotDigest'], ep.digest(snapshot))
            self.assertEqual('published', snapshot['event']['status'])
            self.assertEqual('review_required', case['expected']['decision'])
            self.assertIsNone(case['expected']['significance'])

    def test_comparison_cannot_hide_missing_cases_or_duplicate_sessions(self):
        one = {'model': 'synthetic-a', 'sessionId': 'one', 'policyDigest': ep.digest(self.policy), 'suiteDigest': ep.digest(self.suite), 'results': [{'caseId': c['id'], **c['expected'], 'impactIndex': None} for c in self.suite['cases']]}
        two = copy.deepcopy(one); two.update(model='synthetic-b', sessionId='two')
        result = self.cal.compare(self.suite, self.policy, [one, two])
        self.assertFalse(result['certified'])
        self.assertIsNone(result['pairs'][0]['impactWithinOne'])
        self.assertEqual(0, result['pairs'][0]['impactCoverage'])
        two['results'].pop()
        with self.assertRaises(ValueError):
            self.cal.compare(self.suite, self.policy, [one, two])
        with self.assertRaises(ValueError):
            self.cal.compare(self.suite, self.policy, [one, one])

    def test_nulls_cannot_inflate_rating_agreement(self):
        one = {'model': 'synthetic-a', 'sessionId': 'one', 'policyDigest': ep.digest(self.policy), 'suiteDigest': ep.digest(self.suite), 'results': [{'caseId': c['id'], 'decision': 'hold', 'significance': None, 'impactIndex': None} for c in self.suite['cases']]}
        two = copy.deepcopy(one); two.update(model='synthetic-b', sessionId='two')
        pair = self.cal.compare(self.suite, self.policy, [one, two])['pairs'][0]
        self.assertIsNone(pair['significanceAgreement'])
        self.assertEqual(0, pair['significanceCoverage'])


if __name__ == '__main__':
    unittest.main()
