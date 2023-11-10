import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_next


class TestFunctionGetNext(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_get_next_without_existing_files(self):
        result = get_next(self.temp_dir, "test.txt")
        self.assertEqual(result, os.path.join(self.temp_dir, "1_test.txt"))

    def test_get_next_with_existing_files(self):
        for i in range(1, 5):
            with open(os.path.join(self.temp_dir, f"{i}_test.txt"), 'w') as f:
                f.write("dummy content")
        result = get_next(self.temp_dir, "test.txt")
        self.assertEqual(result, os.path.join(self.temp_dir, "5_test.txt"))

    def test_get_next_no_pattern(self):
        result = get_next(self.temp_dir)
        self.assertEqual(result, os.path.join(self.temp_dir, "1_"))
