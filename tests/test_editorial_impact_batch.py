import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from report_impact_batch import inspect_batch, report
from validate_all import calculate_impact_index

class BatchImpactRisks(unittest.TestCase):
    def setUp(self):
        self.events={str(i):{'id':str(i),'significance':1,'impactIndex':0,'impacts':[]} for i in range(3)}
        self.run={'candidates':[{'eventId':str(i),'decision':'update','confirmation':{'impact':{'status':'not_found','finding':'No independent adoption measured.'}}} for i in range(3)]}
    def test_uniform_batch_warns_and_never_mutates_or_scores(self):
        before=copy.deepcopy((self.events,self.run));d=inspect_batch(self.run,self.events)
        self.assertIn('UNIFORM_EMPTY_IMPACTS_REVIEW_SOURCES',{f['code'] for f in d['flags']})
        self.assertIn('REPEATED_IMPACT_REASON_REVIEW_SOURCES',{f['code'] for f in d['flags']})
        self.assertEqual(before,(self.events,self.run));self.assertIn('not measured zero',d['notice'])
    def test_l1_nonzero_impact_uses_original_formula(self):
        e={'significance':1,'status':'draft','claims':[],'impacts':[{'dimension':'access_democratization','severity':1,'direction':'positive','affectedGroups':['developers'],'timeframe':'immediate','evidenceGrade':'B'}]}
        self.assertEqual(2,calculate_impact_index(e))
        e['impacts'][0]['severity']=-1;e['impacts'][0]['direction']='negative'
        self.assertEqual(2,calculate_impact_index(e))
    def test_found_unscored_warns_not_forced_score(self):
        self.run['candidates'][0]['confirmation']['impact']['status']='found'
        d=inspect_batch(self.run,self.events);self.assertIn('FOUND_BUT_UNSCORED_REQUIRES_DISPOSITION',{f['code'] for f in d['flags']})
    def test_nonuniform_not_flagged_uniform(self):
        self.events['0']['impacts']=[{}];self.events['0']['impactIndex']=1
        self.assertNotIn('UNIFORM_EMPTY_IMPACTS_REVIEW_SOURCES',{f['code'] for f in inspect_batch(self.run,self.events)['flags']})
    def test_duplicate_selected_rejected(self):
        self.run['candidates'].append(copy.deepcopy(self.run['candidates'][0]))
        with self.assertRaises(ValueError):inspect_batch(self.run,self.events)
    def test_missing_reason_and_null_impacts_not_silently_assessed(self):
        del self.run['candidates'][0]['confirmation']['impact']['finding']
        self.assertIn('MISSING_IMPACT_REASON',{f['code'] for f in inspect_batch(self.run,self.events)['flags']})
        self.events['0']['impacts']=None
        with self.assertRaises(ValueError):inspect_batch(self.run,self.events)
    def test_run_path_escape_rejected(self):
        with self.assertRaises(ValueError):report(ROOT,'../outside.json')
if __name__=='__main__':unittest.main()
