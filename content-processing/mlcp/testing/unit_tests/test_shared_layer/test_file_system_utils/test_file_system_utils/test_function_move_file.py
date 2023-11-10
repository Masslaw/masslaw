import os
import shutil
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import move_file


class TestFunctionMoveFile(unittest.TestCase):

    def setUp(self):
        self.src_file = tempfile.NamedTemporaryFile(delete=False)
        self.dst_path = tempfile.mktemp()

    def tearDown(self):
        if os.path.exists(self.src_file.name):
            shutil.rmtree(self.src_file.name, ignore_errors=True)
        if os.path.exists(self.dst_path):
            shutil.rmtree(self.dst_path, ignore_errors=True)

    def test_move_file_valid(self):
        move_file(self.src_file.name, self.dst_path)
        self.assertFalse(os.path.exists(self.src_file.name))
        self.assertTrue(os.path.exists(self.dst_path))

    def test_move_to_existing_file(self):
        with open(self.dst_path, 'w') as f:
            f.write("Some content")
        move_file(self.src_file.name, self.dst_path)
        self.assertFalse(os.path.exists(self.src_file.name))
        self.assertTrue(os.path.exists(self.dst_path))

    def test_move_non_existent_file(self):
        non_existent_path = "/path/to/nonexistent/file"
        with self.assertRaises(FileNotFoundError):
            move_file(non_existent_path, self.dst_path)

    def test_move_file_to_existing_directory(self):
        os.makedirs(self.dst_path)
        dst_file_path = os.path.join(self.dst_path, os.path.basename(self.src_file.name))
        move_file(self.src_file.name, self.dst_path)
        self.assertFalse(os.path.exists(self.src_file.name))
        self.assertTrue(os.path.exists(dst_file_path))
