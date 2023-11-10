import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import rename_file


class TestFunctionRenameFile(unittest.TestCase):

    def setUp(self):
        self.src_file = tempfile.NamedTemporaryFile(delete=False)
        self.dst_path = tempfile.mktemp()

    def tearDown(self):
        if os.path.exists(self.src_file.name):
            os.remove(self.src_file.name)
        if os.path.exists(self.dst_path):
            os.remove(self.dst_path)

    def test_rename_file_valid(self):
        rename_file(self.src_file.name, self.dst_path)
        self.assertFalse(os.path.exists(self.src_file.name))
        self.assertTrue(os.path.exists(self.dst_path))

    def test_rename_to_existing_file(self):
        with open(self.dst_path, 'w') as f:
            f.write("Some content")
        rename_file(self.src_file.name, self.dst_path)
        self.assertFalse(os.path.exists(self.src_file.name))
        self.assertTrue(os.path.exists(self.dst_path))

    def test_rename_non_existent_file(self):
        non_existent_path = "/path/to/nonexistent/file"
        with self.assertRaises(FileNotFoundError):
            rename_file(non_existent_path, self.dst_path)
