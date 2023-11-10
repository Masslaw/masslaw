import os
import tempfile
import time
import unittest

from shared_layer.file_system_utils._file_system_utils import get_modified_time


class TestFunctionGetModifiedTime(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_modified_time_existing_file(self):
        mtime = os.path.getmtime(self.file_path)
        self.assertEqual(get_modified_time(self.file_path), mtime)

    def test_get_modified_time_after_modification(self):
        time.sleep(1)  # Ensuring a noticeable difference in modification time
        with open(self.file_path, 'a') as f:
            f.write("\nAppended content")
        mtime = os.path.getmtime(self.file_path)
        self.assertEqual(get_modified_time(self.file_path), mtime)

    def test_get_modified_time_non_existent_file(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            get_modified_time(non_existent_path)

    def test_get_modified_time_directory(self):
        directory = tempfile.mkdtemp()
        mtime = os.path.getmtime(directory)
        self.assertEqual(get_modified_time(directory), mtime)
        os.rmdir(directory)
