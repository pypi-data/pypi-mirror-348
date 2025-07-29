import unittest
import pathlib
import os

class TestExamples(unittest.TestCase):
    def setUp(self):
        example_dir = pathlib.Path(__file__).parent.parent / "examples/"
        os.chdir(example_dir)

    def test_run_examples(self):
        print(pathlib.Path('.').absolute())
        for example in pathlib.Path('.').glob("*.py"):
            if example.name.startswith("run_") or example.name == "util.py":
                continue
            with self.subTest(example=example.name):
                exec(example.read_text())

if __name__ == "__main__":
    unittest.main()
