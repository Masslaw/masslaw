import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import read_file


class TestFunctionReadFile(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        self.content = "Sample test content"
        with open(self.file_path, 'w') as f:
            f.write(self.content)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_read_existing_file(self):
        read_content = read_file(self.file_path)
        self.assertEqual(read_content, self.content)

    def test_read_non_existent_file(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            read_file(non_existent_path)

    def test_read_empty_file(self):
        empty_file_path = tempfile.mktemp()
        with open(empty_file_path, 'w') as f:
            pass
        read_content = read_file(empty_file_path)
        self.assertEqual(read_content, "")
        os.remove(empty_file_path)
