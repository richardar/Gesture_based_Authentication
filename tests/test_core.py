import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import unittest

class ImportTests(unittest.TestCase):
    def test_import_modules(self):
        modules = ['app', 'facerecognition', 'gesturerecognition', 'gesturerecognitiontask']
        for m in modules:
            with self.subTest(module=m):
                __import__(m)

if __name__ == '__main__':
    unittest.main()
