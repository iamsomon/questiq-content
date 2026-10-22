import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

collector = module('collect_candidates')
content = module('content')

class CandidateTests(unittest.TestCase):
    def test_provenance_and_status_never_imply_factual_approval(self):
        rows = list(collector.parse('\n#Q What is a sample?\n^ One\nA One\nB Two\nC Three\nD Four\n', 'general'))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['sourceLine'], 2)
        self.assertEqual(row['sourceCorrectIndex'], 0)
        self.assertEqual(row['status'], 'unverified_source_candidate')
        self.assertIn('primary_fact_check', row['missing'])
        self.assertIn('ru_translation', row['missing'])
        self.assertNotIn('localizations', row)
        self.assertNotIn('humanApproved', row)
        self.assertEqual(row['license'], 'CC-BY-SA-4.0')

    def test_rejects_duplicate_choices_and_wrong_answer(self):
        for choices in ['A One\nB one!\nC Three\nD Four', 'A Zero\nB Two\nC Three\nD Four', 'A One\nB Two\nC Three']:
            self.assertEqual(list(collector.parse('#Q A sample question?\n^ One\n'+choices+'\n', 'general')), [])

    def test_ids_are_stable_and_html_is_decoded(self):
        text = '#Q What is &quot;one&quot;?\n^ One\nA One\nB Two\nC Three\nD Four\n'
        a = list(collector.parse(text, 'general'))[0]
        b = list(collector.parse(text, 'newest'))[0]
        self.assertEqual(a['candidateId'], b['candidateId'])
        self.assertEqual(a['questionEn'], 'What is "one"?')

    def test_programming_symbols_stay_distinct(self):
        for options in [('#', '//', '/*', '<!--'), ('=', '==', '!=', '<='), ('%', '/', '**', '==')]:
            normalized = [content.normalized(s) for s in options]
            self.assertTrue(all(normalized))
            self.assertEqual(len(set(normalized)), 4)

    def test_research_does_not_count_toward_playable_target(self):
        report = content.report()
        self.assertEqual(report['targetQuestions'], 10000)
        self.assertEqual(report['targetComplete'], all(r['remaining'] == 0 and not any(r['difficultyRemaining'].values()) for r in report['categories']))
        self.assertEqual(report['remainingQuestions'], sum(r['remaining'] for r in report['categories']))
        self.assertEqual(report['approvedQuestions'], sum(r['approved'] for r in report['categories']))

if __name__ == '__main__':
    unittest.main()
