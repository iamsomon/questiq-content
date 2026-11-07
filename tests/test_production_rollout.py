"""A client with the previous manifest can finish its in-flight download."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).parent))
import test_pipeline as pipeline
c = pipeline.c


class ProductionRolloutTests(unittest.TestCase):
    setUp = pipeline.PipelineTests.setUp
    tearDown = pipeline.PipelineTests.tearDown
    save = pipeline.PipelineTests.save
    approve = pipeline.PipelineTests.approve
    def test_old_manifest_file_survives_without_reentering_active_catalog(self):
        self.save(); self.approve()
        first=c.build(self.root,'https://example.org/dist')
        entry=first['packs'][0]; name=entry['url'].split('/')[-1]
        payload=(self.root/'dist/packs'/name).read_bytes()
        (self.root/'catalog/retained-packs.json').write_text(json.dumps({
            'schemaVersion':1,'packs':[{'file':name,'sha256':hashlib.sha256(payload).hexdigest(),'size':len(payload)}]}))
        self.items[0]['localizations']['en']['question']+=' Revised.'
        self.items[0]['revision']+=1
        self.save(); self.approve()
        second=c.build(self.root,'https://example.org/dist')
        self.assertNotEqual(first['version'],second['version'])
        self.assertEqual((self.root/'dist/packs'/name).read_bytes(),payload)
        self.assertNotIn(entry['url'],[p['url'] for p in second['packs']])
        self.assertEqual(c.report(self.root)['approvedQuestions'],10)
        self.assertEqual(second,c.build(self.root,'https://example.org/dist'))

    def test_retention_cannot_pin_path_traversal_or_incorrect_bytes(self):
        self.save();self.approve()
        (self.root/'catalog/retained-packs.json').write_text(json.dumps({'schemaVersion':1,'packs':[{'file':'../questions.json'}]}))
        with self.assertRaisesRegex(ValueError,'Unsafe retained'):
            c.build(self.root,'https://example.org/dist')
        m=c.load(self.root/'catalog/retained-packs.json')
        m['packs'][0]={'file':'astronomy-0000000000000000.json','sha256':'0'*64,'size':1}
        (self.root/'dist/packs/astronomy-0000000000000000.json').write_bytes(b'x')
        (self.root/'catalog/retained-packs.json').write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,'Invalid retained'):
            c.build(self.root,'https://example.org/dist')

if __name__=='__main__': unittest.main()
