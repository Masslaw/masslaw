import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_created_time


class TestFunctionGetCreatedTime(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_created_time_existing_file(self):
        ctime = os.path.getctime(self.file_path)
        self.assertEqual(get_created_time(self.file_path), ctime)

    def test_get_created_time_non_existent_file(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            get_created_time(non_existent_path)

    def test_get_created_time_directory(self):
        directory = tempfile.mkdtemp()
        ctime = os.path.getctime(directory)
        self.assertEqual(get_created_time(directory), ctime)
        os.rmdir(directory)
