import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_candidates import module

intake = module('import_parallel_qa')
content = module('content')
ROOT = Path(__file__).resolve().parents[1]


class ParallelQaTests(unittest.TestCase):
    def mkqa(self):
        return {'example_id': -12, 'queries': {'ru': 'Кто написал роман?', 'en': 'Who wrote the novel?'},
                'answers': {lang: [{'text': 'Name', 'aliases': ['Alias'], 'entity': 'Q1', 'type': 'entity'}]
                            for lang in ('ru', 'en')}}

    def rubq(self):
        return {'uid': 42, 'question_text': 'Кто написал роман?', 'question_eng': 'Who wrote the novel?',
                'answers': [{'label': 'Автор', 'value': 'Q1', 'type': 'uri', 'wd_names': {'ru': ['Автор']}}],
                'query': 'SELECT', 'question_uris': ['Q1'], 'question_props': ['P50'], 'tags': []}

    def test_preserves_mkqa_answers_without_approving(self):
        raw = self.mkqa()
        row = next(intake.mkqa_rows([raw], 'sha'))
        self.assertEqual(row['id'], 'mkqa_n12')
        self.assertEqual(row['answers'], raw['answers'])
        self.assertEqual(row['questions'], raw['queries'])
        self.assertEqual(row['license'], 'CC-BY-SA-3.0')
        self.assertEqual(row['status'], 'imported_not_game_ready')
        self.assertIn('four_options', row['missingForGame'])
        self.assertNotIn('humanApproved', row)

    def test_rejects_missing_locale(self):
        raw = self.mkqa()
        del raw['queries']['ru']
        with self.assertRaisesRegex(ValueError, 'missing parallel'):
            list(intake.mkqa_rows([raw], 'sha'))
        raw = self.rubq()
        raw['question_eng'] = ''
        with self.assertRaisesRegex(ValueError, 'missing parallel'):
            list(intake.rubq_rows([raw], 'dev', 'sha'))

    def test_unanswerable_multivalued_and_stale_source_flags(self):
        raw = self.mkqa()
        raw['queries']['en'] = 'When was the last time this happened?'
        raw['answers']['en'].append({'type': 'unanswerable', 'text': 'Other', 'entity': 'Q2'})
        row = next(intake.mkqa_rows([raw], 'sha'))
        self.assertTrue({'possibly_time_dependent_or_underspecified', 'source_has_no_short_answer',
                         'multiple_source_answers', 'entity_alignment_requires_review'} <= set(row['riskFlags']))

    def test_rubq_missing_english_answer_is_not_fabricated(self):
        row = next(intake.rubq_rows([self.rubq()], 'dev', 'sha'))
        self.assertEqual(row['answers']['en'][0]['aliases'], [])
        self.assertIn('localized_answer_label_missing', row['riskFlags'])
        self.assertEqual(row['translationProvenance']['en'], 'source_machine_translation')

    def test_duplicates_are_rejected_or_reported(self):
        row = next(intake.mkqa_rows([self.mkqa()], 'sha'))
        other = copy.deepcopy(row)
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'bank.jsonl'
            with self.assertRaisesRegex(ValueError, 'Duplicate source ID'):
                intake.write_bank([row, other], target)
            other['id'] += '_other'
            report = intake.write_bank([row, other], target)
            self.assertEqual(report['sourceRows'], 2)
            self.assertEqual(report['distinctNormalizedPairs'], 1)
            self.assertEqual(report['duplicatePairRows'], 1)
            self.assertEqual(report['gameReadyQuestionsAdded'], 0)

    def test_tampered_cached_source_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'mkqa.jsonl.gz'
            path.write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                intake.download(intake.MKQA_URL, path)

    def test_published_intake_integrity_and_separation(self):
        folder = ROOT/'imports/parallel-qa'
        report = json.loads((folder/'report.json').read_text())
        self.assertEqual(report['sourceRows'], 12910)
        self.assertFalse(report['countIsDistinctFacts'])
        self.assertEqual(report['gameReadyQuestionsAdded'], 0)
        for name, expected in [('mkqa', 10000), ('rubq', 2910)]:
            path = folder/f'{name}-ru-en.jsonl'
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(rows), expected)
            self.assertEqual(len({row['id'] for row in rows}), expected)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), report['sources'][name]['sha256'])
            for row in rows:
                self.assertEqual(row['status'], 'imported_not_game_ready')
                self.assertEqual(set(row['questions']), {'ru', 'en'})
                self.assertTrue(all(row['questions'].values()))
                self.assertEqual(row['license'], intake.LICENSES[name])
                self.assertTrue(row['attribution'])
                self.assertEqual(row['sourceSha256'], intake.SOURCE_HASHES[
                    'mkqa.jsonl.gz' if name == 'mkqa' else f"rubq-{row['sourceSplit']}.json"])
                self.assertIn('editorial_acceptance', row['missingForGame'])
                self.assertNotIn('approved', row)
                self.assertNotIn('humanApproved', row)
        playable = content.report()
        released = sum(len(json.loads(path.read_text())) for path in (ROOT/'questions').glob('*.json'))
        self.assertEqual(playable['approvedQuestions'], released)
        self.assertEqual(playable['remainingQuestions'], sum(row['remaining'] for row in playable['categories']))


if __name__ == '__main__':
    unittest.main()
