import unittest

from shared_layer.file_system_utils._file_system_utils import get_relative_path


class TestFunctionGetRelativePath(unittest.TestCase):

    def test_get_relative_path_in_same_directory(self):
        base_path = "/home/user/documents"
        path = "/home/user/documents/sample.txt"
        expected_relative_path = "sample.txt"
        self.assertEqual(get_relative_path(path, base_path), expected_relative_path)

    def test_get_relative_path_in_subdirectory(self):
        base_path = "/home/user/documents"
        path = "/home/user/documents/subdir/sample.txt"
        expected_relative_path = "subdir/sample.txt"
        self.assertEqual(get_relative_path(path, base_path), expected_relative_path)

    def test_get_relative_path_in_parent_directory(self):
        base_path = "/home/user/documents/subdir"
        path = "/home/user/documents/sample.txt"
        expected_relative_path = "../sample.txt"
        self.assertEqual(get_relative_path(path, base_path), expected_relative_path)

    def test_get_relative_path_for_the_same_path(self):
        base_path = "/home/user/documents/sample.txt"
        path = "/home/user/documents/sample.txt"
        expected_relative_path = "."
        self.assertEqual(get_relative_path(path, base_path), expected_relative_path)
