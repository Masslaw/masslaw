import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import copy_file


class TestFunctionCopyFile(unittest.TestCase):

    def setUp(self):
        self.src_path = tempfile.mktemp()
        with open(self.src_path, 'w') as f:
            f.write("test content")
        self.dst_path = tempfile.mktemp()

    def tearDown(self):
        if os.path.exists(self.src_path):
            os.remove(self.src_path)
        if os.path.exists(self.dst_path):
            os.remove(self.dst_path)

    def test_copy_file(self):
        self.assertTrue(os.path.isfile(self.src_path))
        self.assertFalse(os.path.exists(self.dst_path))
        copy_file(self.src_path, self.dst_path)
        self.assertTrue(os.path.isfile(self.dst_path))
        with open(self.src_path, 'r') as f1, open(self.dst_path, 'r') as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_copy_file_non_existent_src(self):
        non_existent_path = tempfile.mktemp()
        with self.assertRaises(FileNotFoundError):
            copy_file(non_existent_path, self.dst_path)

    def test_copy_file_to_existing_dst(self):
        with open(self.dst_path, 'w') as f:
            f.write("existing content")
        self.assertTrue(os.path.isfile(self.dst_path))
        copy_file(self.src_path, self.dst_path)
        with open(self.src_path, 'r') as f1, open(self.dst_path, 'r') as f2:
            self.assertEqual(f1.read(), f2.read())
