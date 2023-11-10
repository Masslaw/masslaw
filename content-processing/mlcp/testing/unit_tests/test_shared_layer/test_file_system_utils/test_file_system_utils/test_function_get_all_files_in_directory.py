import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_all_files_in_directory


class TestFunctionGetAllFilesInDirectory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        self.sub_dir = os.path.join(self.temp_dir, "subdir")
        os.makedirs(self.sub_dir)

        self.file_1 = os.path.join(self.temp_dir, "file1.txt")
        with open(self.file_1, 'w') as f:
            f.write("content")

        self.file_2 = os.path.join(self.sub_dir, "file2.txt")
        with open(self.file_2, 'w') as f:
            f.write("content")

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_valid_directory(self):
        result = get_all_files_in_directory(self.temp_dir)
        expected_files = [self.file_1, self.file_2]
        self.assertEqual(set(result), set(expected_files))

    def test_nonexistent_directory(self):
        nonexistent_dir = os.path.join(self.temp_dir, "nonexistent")
        result = get_all_files_in_directory(nonexistent_dir)
        self.assertEqual(result, [])

    def test_directory_is_a_file(self):
        result = get_all_files_in_directory(self.file_1)
        self.assertEqual(result, [self.file_1])
