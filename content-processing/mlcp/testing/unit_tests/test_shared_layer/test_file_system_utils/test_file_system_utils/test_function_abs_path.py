import os
import unittest

from shared_layer.file_system_utils._file_system_utils import abs_path


class TestFunctionAbsPath(unittest.TestCase):

    def setUp(self):
        self.original_cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_cwd)

    def test_relative_path(self):
        relative_path = "some_folder/some_file.txt"
        expected_path = os.path.join(os.getcwd(), "some_folder", "some_file.txt")
        self.assertEqual(abs_path(relative_path), expected_path)

    def test_absolute_path(self):
        absolute_path = "/some_folder/some_file.txt"
        self.assertEqual(abs_path(absolute_path), absolute_path)

    def test_current_directory(self):
        path = "./some_file.txt"
        expected_path = os.path.join(os.getcwd(), "some_file.txt")
        self.assertEqual(abs_path(path), expected_path)
