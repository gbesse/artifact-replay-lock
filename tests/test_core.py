import tempfile,unittest,hashlib,os
from pathlib import Path
from artifact_replay_lock import run
class DomainTests(unittest.TestCase):
 def test_exact_bytes_and_mutation(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'a';p.write_bytes(b'first');d={'root':tmp,'files':[{'path':'a','expected_sha256':hashlib.sha256(b'first').hexdigest()}]};self.assertTrue(run(d)['all_expected_hashes_match']);p.write_bytes(b'changed');self.assertEqual(run(d)['files'][0]['state'],'mismatch')
 def test_capture_without_expectation_is_not_verified(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/'a').write_bytes(b'a');self.assertFalse(run({'root':tmp,'files':[{'path':'a'}]})['all_expected_hashes_match'])
 def test_traversal_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):run({'root':tmp,'files':[{'path':'../x'}]})
 def test_symlink_not_followed(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'a').write_bytes(b'a');(p/'link').symlink_to(p/'a');self.assertEqual(run({'root':tmp,'files':[{'path':'link'}]})['files'][0]['state'],'symlink_rejected')
 def test_missing_and_byte_budget_visible(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/'a').write_bytes(b'123');r=run({'root':tmp,'maximum_total_bytes':2,'files':[{'path':'a'},{'path':'missing'}]});self.assertEqual([x['state'] for x in r['files']],['byte_budget_exceeded','missing'])
