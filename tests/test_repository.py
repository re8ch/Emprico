import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).parents[1]


class RepositoryTest(unittest.TestCase):
    def test_cases_have_empirical_shape(self):
        for path in (ROOT / "cases").glob("*.json"):
            data = json.loads(path.read_text())
            self.assertRegex(data["id"], r"^[a-z0-9-]+$")
            self.assertTrue(data["facts"])
            self.assertTrue(data["judgment"])
            self.assertTrue(data["rule"])
            self.assertTrue(data["evidence"])

    def test_json_files_parse(self):
        for path in ROOT.rglob("*.json"):
            json.loads(path.read_text())

    def test_actions_use_full_commit_sha(self):
        action = re.compile(r"uses:\s+[^\s]+@([^\s]+)")
        for path in (ROOT / ".github" / "workflows").glob("*.yml"):
            for ref in action.findall(path.read_text()):
                self.assertRegex(ref, r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
