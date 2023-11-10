import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_size


class TestFunctionGetSize(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        with open(self.file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_size_existing_file(self):
        size = os.path.getsize(self.file_path)
        self.assertEqual(get_size(self.file_path), size)

    def test_get_size_non_existent_file(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            get_size(non_existent_path)
