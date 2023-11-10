import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import get_nested_files


class TestFunctionGetNestedFiles(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        self.nested_dir_1 = os.path.join(self.temp_dir, "nested1")
        os.makedirs(self.nested_dir_1)
        self.nested_dir_2 = os.path.join(self.nested_dir_1, "nested2")
        os.makedirs(self.nested_dir_2)

        self.txt_file_1 = os.path.join(self.temp_dir, "file1.txt")
        with open(self.txt_file_1, 'w') as f:
            f.write("content")
        self.txt_file_2 = os.path.join(self.nested_dir_1, "file2.txt")
        with open(self.txt_file_2, 'w') as f:
            f.write("content")
        self.jpg_file = os.path.join(self.nested_dir_2, "image.jpg")
        with open(self.jpg_file, 'wb') as f:
            f.write(b"content")

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_get_nested_files_of_type_txt(self):
        result = get_nested_files(self.temp_dir, "txt")
        expected_files = [self.txt_file_1, self.txt_file_2]
        self.assertEqual(set(result), set(expected_files))

    def test_get_nested_files_of_type_jpg(self):
        result = get_nested_files(self.temp_dir, "jpg")
        expected_files = [self.jpg_file]
        self.assertEqual(set(result), set(expected_files))

    def test_get_nested_files_no_matching_type(self):
        result = get_nested_files(self.temp_dir, "png")
        self.assertEqual(result, [])
