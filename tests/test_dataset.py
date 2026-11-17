import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[1]


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class DatasetTest(unittest.TestCase):
    def test_recommendations_are_supported_and_auditable(self):
        path = ROOT / "data" / "recommendations" / "public-gitops-v0.1.jsonl"
        for record in load_jsonl(path):
            self.assertEqual(record["schema_version"], "0.1.0")
            self.assertTrue(record["context"]["facts"])
            for fact in record["context"]["facts"]:
                self.assertTrue(fact["claim"])
                self.assertTrue(fact["evidence"])
                self.assertTrue(all(url.startswith("https://") for url in fact["evidence"]))
            recommendation = record["recommendation"]
            self.assertTrue(recommendation["action"])
            self.assertTrue(recommendation["rationale"])
            self.assertGreaterEqual(recommendation["confidence"], 0)
            self.assertLessEqual(recommendation["confidence"], 1)
            self.assertTrue(record["provenance"]["case_ids"])

    def test_raw_records_default_to_training_ineligible(self):
        spec = importlib.util.spec_from_file_location("collector", ROOT / "scripts" / "collect_github_prs.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIn('"training_eligible": False', (ROOT / "scripts" / "collect_github_prs.py").read_text())

    def test_jsonl_has_unique_ids(self):
        records = []
        for path in (ROOT / "data").rglob("*.jsonl"):
            records.extend(load_jsonl(path))
        ids = [record.get("id", record.get("record_id")) for record in records]
        self.assertEqual(len(ids), len(set(ids)))

    def test_huggingface_publications_are_immutable(self):
        manifest = json.loads((ROOT / "datasets" / "huggingface.json").read_text())
        self.assertEqual(manifest["visibility"], "private")
        for publication in manifest["publications"]:
            self.assertRegex(publication["revision"], r"^[0-9a-f]{40}$")
            self.assertIn(publication["revision"], publication["revisionUrl"])
            for item in publication["files"]:
                self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
