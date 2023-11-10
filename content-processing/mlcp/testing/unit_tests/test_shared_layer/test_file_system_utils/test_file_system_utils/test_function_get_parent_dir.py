import unittest

from shared_layer.file_system_utils._file_system_utils import get_parent_dir


class TestFunctionGetParentDir(unittest.TestCase):

    def test_get_parent_dir_absolute_path(self):
        path = "/home/user/documents/file.txt"
        expected = "/home/user/documents"
        self.assertEqual(get_parent_dir(path), expected)

    def test_get_parent_dir_relative_path(self):
        path = "documents/file.txt"
        expected = "documents"
        self.assertEqual(get_parent_dir(path), expected)

    def test_get_parent_dir_no_parent(self):
        path = "file.txt"
        expected = ""
        self.assertEqual(get_parent_dir(path), expected)

    def test_get_parent_dir_nested_path(self):
        path = "/home/user/documents/projects/project1/file.txt"
        expected = "/home/user/documents/projects/project1"
        self.assertEqual(get_parent_dir(path), expected)
