import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import is_dir


class TestFunctionIsDir(unittest.TestCase):

    def setUp(self):
        self.dir_path = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.dir_path)

    def test_is_dir_true(self):
        self.assertTrue(is_dir(self.dir_path))

    def test_is_dir_false_file(self):
        file_path = os.path.join(tempfile.mkdtemp(), 'test.txt')
        with open(file_path, 'w') as f:
            f.write("test content")
        self.assertFalse(is_dir(file_path))
        os.remove(file_path)

    def test_is_dir_false_non_existent(self):
        non_existent_path = 'some/arbitrary/non/existent/path'
        self.assertFalse(is_dir(non_existent_path))
