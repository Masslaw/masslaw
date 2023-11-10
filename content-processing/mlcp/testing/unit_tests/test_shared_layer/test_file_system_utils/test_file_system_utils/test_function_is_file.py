import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import is_file


class TestFunctionIsFile(unittest.TestCase):

    def setUp(self):
        self.file_path = os.path.join(tempfile.mkdtemp(), 'test.txt')
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        os.remove(self.file_path)

    def test_is_file_true(self):
        self.assertTrue(is_file(self.file_path))

    def test_is_file_false_directory(self):
        dir_path = tempfile.mkdtemp()
        self.assertFalse(is_file(dir_path))
        os.rmdir(dir_path)

    def test_is_file_false_non_existent(self):
        non_existent_path = tempfile.mkdtemp()
        self.assertFalse(is_file(non_existent_path))
