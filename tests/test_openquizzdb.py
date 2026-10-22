import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_candidates import module

collector = module('import_openquizzdb')
ROOT = Path(__file__).resolve().parents[1]


class OpenQuizzDbTests(unittest.TestCase):
    def sample(self):
        return {'rédacteur': 'Example author', 'thème': 'Example', 'quizz': {'en': {'débutant': [
            {'id': 1, 'question': 'A question?', 'propositions': ['One', 'Two', 'Three', 'Four'],
             'réponse': 'Two', 'anecdote': 'Original explanation.'}]}}}

    def test_handles_both_published_wrappers_without_changing_text(self):
        data = self.sample()
        expected = list(collector.records(data, 'openquizzdb_1', 'sourcehash'))
        data['quizz']['en'] = [data['quizz']['en']]
        self.assertEqual(expected, list(collector.records(data, 'openquizzdb_1', 'sourcehash')))
        row = expected[0]
        self.assertEqual(row['questionEn'], 'A question?')
        self.assertEqual(row['sourceCorrectIndex'], 1)
        self.assertEqual(row['explanationEn'], 'Original explanation.')
        self.assertIn('Example author', row['attribution'])
        self.assertEqual(row['status'], 'unverified_source_candidate')
        self.assertIn('primary_fact_check', row['missingForGame'])
        self.assertIn('ru_translation', row['missingForGame'])
        self.assertNotIn('approved', row)

    def test_rejects_ambiguous_choices_missing_answer_and_missing_explanation(self):
        for change in ({'propositions': ['One', ' one ', 'Three', 'Four']},
                       {'réponse': 'Absent'}, {'anecdote': ''}, {'propositions': ['One', 'Two']}):
            data = self.sample()
            data['quizz']['en']['débutant'][0].update(change)
            self.assertEqual(list(collector.records(data, 'openquizzdb_1', 'sha')), [])

    def test_fails_before_opening_tampered_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'input.tar.gz'
            path.write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                collector.import_archive(path, Path(tmp)/'out')
            self.assertFalse((Path(tmp)/'out').exists())

    def test_saved_bank_integrity_provenance_and_no_approvals(self):
        folder = ROOT/'imports/openquizzdb'
        report = json.loads((folder/'report.json').read_text())
        path = folder/'questions-en.jsonl'
        rows = [json.loads(s) for s in path.read_text().splitlines()]
        self.assertEqual(report['importedSourceRows'], 3291)
        self.assertEqual(report['sourceEnRows'], 3300)
        self.assertEqual(report['structurallyRejectedRows'], 9)
        self.assertEqual(len(report['rejectedFiles']), 26)
        self.assertEqual(len(report['fileReceipts']), 110)
        self.assertEqual(len(rows), 3291)
        self.assertEqual(len({r['id'] for r in rows}), 3291)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), report['sha256'])
        self.assertEqual(report['gameReadyQuestionsAdded'], 0)
        for row in rows:
            self.assertEqual(row['sourceCommit'], collector.COMMIT)
            self.assertTrue(row['sourceUrl'].startswith(collector.BASE+'/data/'))
            self.assertEqual(row['license'], 'CC-BY-SA-4.0')
            self.assertEqual(row['status'], 'unverified_source_candidate')
            self.assertTrue(row['attribution'])
            self.assertIn('editorial_acceptance', row['missingForGame'])
            self.assertNotIn('approved', row)
            self.assertNotIn('humanApproved', row)


if __name__ == '__main__':
    unittest.main()
