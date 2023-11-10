import unittest

from shared_layer.file_system_utils._file_system_utils import split_path


class TestFunctionSplitPath(unittest.TestCase):

    def test_split_path_absolute(self):
        path = "/home/user/documents/file.txt"
        expected = ['/', 'home', 'user', 'documents', 'file.txt']
        self.assertEqual(split_path(path), expected)

    def test_split_path_relative(self):
        path = "documents/projects/file.txt"
        expected = ['documents', 'projects', 'file.txt']
        self.assertEqual(split_path(path), expected)

    def test_split_path_single_directory(self):
        path = "/home"
        expected = ['/', 'home']
        self.assertEqual(split_path(path), expected)

    def test_split_path_single_file(self):
        path = "file.txt"
        expected = ['file.txt']
        self.assertEqual(split_path(path), expected)

    def test_split_path_empty(self):
        path = ""
        expected = []
        self.assertEqual(split_path(path), expected)
