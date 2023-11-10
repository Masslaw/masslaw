import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_accessed_time


class TestFunctionGetAccessedTime(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_accessed_time_existing_file(self):
        atime = os.path.getatime(self.file_path)
        self.assertEqual(get_accessed_time(self.file_path), atime)

    def test_get_accessed_time_after_access(self):
        with open(self.file_path, 'r') as f:
            _ = f.read()
        atime = os.path.getatime(self.file_path)
        self.assertEqual(get_accessed_time(self.file_path), atime)

    def test_get_accessed_time_non_existent_file(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            get_accessed_time(non_existent_path)

    def test_get_accessed_time_directory(self):
        directory = tempfile.mkdtemp()
        atime = os.path.getatime(directory)
        self.assertEqual(get_accessed_time(directory), atime)
        os.rmdir(directory)
