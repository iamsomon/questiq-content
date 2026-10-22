"""Source/credit preservation checks; these do not grant factual approval."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AdaptationProvenanceTests(unittest.TestCase):
    def test_selected_source_records_still_match_pinned_intake(self):
        mapping = json.loads((ROOT/'credits/global_mmlu_20261023.mapping.json').read_text())
        expected = {row['sourceId']: row for row in mapping}
        self.assertEqual(len(mapping), len(expected))
        found = set()
        with (ROOT/'imports/global-mmlu/questions-ru-en.jsonl').open() as source:
            for line in source:
                row = json.loads(line)
                if row['sourceId'] not in expected:
                    continue
                pin = expected[row['sourceId']]
                canonical = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
                self.assertEqual(hashlib.sha256(canonical).hexdigest(), pin['sourceRecordSha256'])
                self.assertEqual(row['sourceCommit'], pin['sourceCommit'])
                self.assertEqual(row['license'], pin['license'])
                found.add(row['sourceId'])
        self.assertEqual(found, set(expected))

    def test_delivered_adaptations_retain_credit_and_full_license_reference(self):
        mapping = json.loads((ROOT/'credits/global_mmlu_20261023.mapping.json').read_text())
        questions = {q['id']: q for p in (ROOT/'questions').glob('*.json') for q in json.loads(p.read_text())}
        credits = (ROOT/'credits/global_mmlu_20261023.md').read_text()
        license_text = (ROOT/'imports/global-mmlu/LICENSE-APACHE-2.0.txt').read_text().strip()
        self.assertIn(license_text, credits)
        self.assertIn('Dan Hendrycks', credits)
        for entry in mapping:
            q = questions[entry['questionId']]
            self.assertIn('f02ed01b9e205553ef37cbf4f1ed1514bb41bce1', q['sources'][0])
            self.assertTrue(q['sources'][0].endswith('#'+q['id'].replace('_', '-')))
            self.assertIn('LICENSE-APACHE-2.0.txt', q['sources'][-1])
            self.assertIn(entry['sourceId'], credits)
            for locale in ['ru', 'en']:
                self.assertIn('Global-MMLU', q['localizations'][locale]['explanation'])
                self.assertIn('Apache 2.0', q['localizations'][locale]['explanation'])


if __name__ == '__main__':
    unittest.main()
