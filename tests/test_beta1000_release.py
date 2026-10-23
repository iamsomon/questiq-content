"""Keep the reviewed beta selection and earlier published facts intact."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


class Beta1000ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.questions={q['id']:q for p in (ROOT/'questions').glob('*.json') for q in json.loads(p.read_text())}
        self.revoked=set(json.loads((ROOT/'revoked.json').read_text()))

    def test_prior_published_questions_are_preserved_or_explicitly_corrected(self):
        baseline=json.loads((ROOT/'authoring/beta1000.baseline.json').read_text())['questions']
        self.assertEqual(len(baseline),310)
        for qid,entry in baseline.items():
            if qid in self.revoked: continue
            q=self.questions[qid]
            if q['revision']==1:
                self.assertEqual(digest(q),entry['sha256'],qid)

    def test_only_the_recorded_selection_has_catalog_review_and_clean_labels(self):
        decisions=json.loads((ROOT/'authoring/beta1000.reviewed-selection.json').read_text())
        evidence=json.loads((ROOT/'authoring/beta1000.evidence.json').read_text())
        self.assertEqual(len(decisions),690)
        self.assertEqual(set(decisions),set(evidence))
        self.assertEqual(len({e['sourceRecordSha256'] for e in evidence.values()}),690)
        for qid,decision in decisions.items():
            e=evidence[qid]
            self.assertEqual(digest(e['sourceRecord']),e['sourceRecordSha256'])
            self.assertEqual(decision['sourceRecordSha256'],e['sourceRecordSha256'])
            if qid in self.revoked: continue
            q=self.questions[qid]
            if q['revision']==1:self.assertEqual(digest(q),decision['sha256'],qid)
            for o in q['options']:
                self.assertNotIn('сша',o['ru'])
                self.assertNotIn('оаэ',o['ru'])
                self.assertNotIn('Kyrgystani',o['en'])
                if q['categoryId']=='literature':
                    self.assertFalse(re.search(r'\d{4}',o['en']),qid)


if __name__=='__main__':unittest.main()
