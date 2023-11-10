import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import remove_file


class TestFunctionRemoveFile(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def test_remove_file_existing(self):
        self.assertTrue(os.path.isfile(self.file_path))
        remove_file(self.file_path)
        self.assertFalse(os.path.exists(self.file_path))

    def test_remove_file_non_existent(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            remove_file(non_existent_path)
