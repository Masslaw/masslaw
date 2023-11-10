import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import copy_files


class TestFunctionCopyFiles(unittest.TestCase):

    def setUp(self):
        self.src_dir = tempfile.mkdtemp()
        self.dst_dir = tempfile.mkdtemp()
        self.file_names = ["file1.txt", "file2.txt", "file3.txt"]

        for file_name in self.file_names:
            with open(os.path.join(self.src_dir, file_name), 'w') as f:
                f.write(f"content of {file_name}")

    def tearDown(self):
        for file_name in self.file_names:
            src_file = os.path.join(self.src_dir, file_name)
            if os.path.exists(src_file):
                os.remove(src_file)
        if os.path.exists(self.src_dir):
            os.rmdir(self.src_dir)
        for file_name in self.file_names:
            dst_file = os.path.join(self.dst_dir, file_name)
            if os.path.exists(dst_file):
                os.remove(dst_file)
        if os.path.exists(self.dst_dir):
            os.rmdir(self.dst_dir)

    def test_copy_files(self):
        copy_files(self.src_dir, self.dst_dir)
        for file_name in self.file_names:
            dst_file_path = os.path.join(self.dst_dir, file_name)
            self.assertTrue(os.path.exists(dst_file_path))
            with open(os.path.join(self.src_dir, file_name), 'r') as f1, open(dst_file_path, 'r') as f2:
                self.assertEqual(f1.read(), f2.read())

    def test_copy_files_from_empty_directory(self):
        empty_src_dir = tempfile.mkdtemp()
        copy_files(empty_src_dir, self.dst_dir)
        self.assertEqual(len(os.listdir(self.dst_dir)), 0)
        os.rmdir(empty_src_dir)

    def test_copy_files_to_existing_files(self):
        for file_name in self.file_names:
            with open(os.path.join(self.dst_dir, file_name), 'w') as f:
                f.write(f"old content of {file_name}")
        copy_files(self.src_dir, self.dst_dir)
        for file_name in self.file_names:
            with open(os.path.join(self.dst_dir, file_name), 'r') as f:
                self.assertEqual(f.read(), f"content of {file_name}")
