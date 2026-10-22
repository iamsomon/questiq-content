import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('content',Path(__file__).resolve().parents[1]/'tools/content.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
class PipelineTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  for d in ['questions','drafts','reviews','catalog','dist']: (self.root/d).mkdir()
  shutil.copy2(c.ROOT/'catalog/categories.json',self.root/'catalog/categories.json')
  (self.root/'revoked.json').write_text('[]')
  self.items=json.loads((c.ROOT/'tests/fixtures/astronomy.json').read_text())[:10]
 def tearDown(self):self.tmp.cleanup()
 def save(self,stage='questions'):
  (self.root/stage/'astronomy.json').write_text(json.dumps(self.items))
 def approve(self):
  rows=[{'id':q['id'],'status':'approved','sha256':c.digest(q),'author':'fixture-author','factReviewer':'fixture-review','languageReviewer':'fixture-review','checkedAt':'2026-10-22','method':'agent_source_review','humanApproved':False,'sourceChecks':[{'url':q['sources'][0],'claim':'Disposable test fixture','location':'Test source'}]} for q in self.items]
  (self.root/'reviews/astronomy.json').write_text(json.dumps(rows))
 def test_unreviewed_question_cannot_publish(self):
  self.save()
  with self.assertRaisesRegex(ValueError,'no approval'):c.inventory(self.root)
 def test_changed_wording_invalidates_review(self):
  self.save();self.approve();c.inventory(self.root)
  self.items[0]['localizations']['en']['question']+=' Changed.';self.save()
  with self.assertRaisesRegex(ValueError,'stale review'):c.inventory(self.root)
 def test_build_is_reproducible_and_revisions_immutable(self):
  self.save();self.approve();a=c.build(self.root,'https://example.org/dist');b=c.build(self.root,'https://example.org/dist');self.assertEqual(a,b)
  self.items[0]['localizations']['en']['question']+=' Revised.';self.save();self.approve()
  with self.assertRaisesRegex(ValueError,'higher revision'):c.build(self.root,'https://example.org/dist')
  self.items[0]['revision']+=1;self.save();self.approve();self.assertNotEqual(a['version'],c.build(self.root,'https://example.org/dist')['version'])
 def test_revoked_ids_cannot_return(self):
  self.save();self.approve();(self.root/'revoked.json').write_text(json.dumps([self.items[0]['id']]))
  with self.assertRaisesRegex(ValueError,'revoked'):c.inventory(self.root)
 def test_duplicate_across_draft_and_release_denied(self):
  self.save();self.approve();self.save('drafts')
  with self.assertRaisesRegex(ValueError,'Duplicate ID'):c.inventory(self.root)
 def test_removed_published_id_requires_revocation(self):
  self.save();self.approve();c.build(self.root,'https://example.org/dist')
  removed=self.items.pop()['id'];self.save();self.approve()
  with self.assertRaisesRegex(ValueError,'explicit revocation'):c.build(self.root,'https://example.org/dist')
 def test_urgent_revocation_publishes_without_a_replacement_question(self):
  self.save();self.approve();c.build(self.root,'https://example.org/dist')
  removed=self.items.pop()['id'];self.save();self.approve()
  (self.root/'revoked.json').write_text(json.dumps([removed]))
  manifest=c.build(self.root,'https://example.org/dist')
  self.assertIn(removed,manifest['revokedIds']);self.assertEqual(manifest['packs'],[])
  self.assertEqual(c.report(self.root)['playableCategories'],0)
if __name__=='__main__':unittest.main()
