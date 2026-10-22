import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_candidates import module

source = module('import_global_mmlu')
ROOT = Path(__file__).resolve().parents[1]


class GlobalMmluTests(unittest.TestCase):
    def sample(self):
        return dict(sample_id='subject/dev/0', subject='subject', subject_category='STEM', question='A question?',
                    option_a='One', option_b='Two', option_c='Three', option_d='Four', answer='B', is_annotated=True)

    def test_aligns_by_id_not_input_order(self):
        a = self.sample()
        b = dict(a, sample_id='subject/dev/1', question='Another question?')
        rows = list(source.align([a,b], [b,a], 'dev'))
        self.assertEqual([r['sourceId'] for r in rows], ['subject/dev/0','subject/dev/1'])
        self.assertEqual(rows[0]['sourceCorrectOptionId'], 'b')
        self.assertEqual(rows[0]['options'][1], {'id':'b','en':'Two','ru':'Two'})
        self.assertEqual(rows[0]['status'], 'imported_not_game_ready')
        self.assertIn('row-level human translation review is not established', rows[0]['translationProvenance'])
        self.assertNotIn('humanApproved', rows[0])

    def test_misaligned_answers_ids_and_subjects_fail(self):
        row = self.sample()
        for change in ({'answer':'C'}, {'subject':'other'}, {'sample_id':'missing'}):
            with self.assertRaises(ValueError):
                list(source.align([row], [dict(row, **change)], 'dev'))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            list(source.align([row,row], [row], 'dev'))

    def test_preserves_and_flags_bad_options_instead_of_silently_fixing(self):
        en, ru = self.sample(), self.sample()
        ru['option_d'] = ru['option_c']
        row = next(source.align([en], [ru], 'dev'))
        self.assertIn('ru_duplicate_options', row['riskFlags'])
        self.assertEqual(row['options'][3]['ru'], 'Three')
        ru['option_d'] = ''
        self.assertIn('ru_empty_option', next(source.align([en], [ru], 'dev'))['riskFlags'])

    def test_tampered_cache_rejected_without_loading_parquet(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            (cache/'ru-test.parquet').write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                source.read_source(cache,'ru','test')

    def test_saved_aligned_bank_hashes_counts_and_no_approvals(self):
        folder = ROOT/'imports/global-mmlu'
        path = folder/'questions-ru-en.jsonl'
        report = json.loads((folder/'report.json').read_text())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), report['sha256'])
        count, ids = 0, set()
        with path.open() as stream:
            for line in stream:
                r = json.loads(line)
                self.assertNotIn(r['id'], ids)
                ids.add(r['id']);count+=1
                self.assertEqual(r['status'], 'imported_not_game_ready')
                self.assertEqual(r['sourceCommit'], source.COMMIT)
                self.assertEqual(r['license'], 'Apache-2.0')
                self.assertEqual(len(r['options']), 4)
                self.assertEqual(set(r['questions']), {'ru','en'})
                self.assertIn(r['sourceCorrectOptionId'], 'abcd')
                self.assertIn('explanation_ru_en', r['missingForGame'])
                self.assertNotIn('humanApproved', r)
                self.assertNotIn('approved', r)
        self.assertEqual(count, 14327)
        self.assertEqual(report['sourcePairs'], count)
        self.assertEqual(len(report['subjects']), 57)
        self.assertEqual(report['gameReadyQuestionsAdded'], 0)
        self.assertFalse(report['humanTranslationReviewInferredFromAnnotations'])
