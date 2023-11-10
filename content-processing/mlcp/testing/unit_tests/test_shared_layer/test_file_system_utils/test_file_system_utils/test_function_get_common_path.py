import unittest

from shared_layer.file_system_utils._file_system_utils import get_common_path


class TestFunctionGetCommonPath(unittest.TestCase):

    def test_common_path_for_identical_paths(self):
        path_1 = "/home/user/documents/sample.txt"
        path_2 = "/home/user/documents/sample.txt"
        expected_common_path = path_1
        self.assertEqual(get_common_path(path_1, path_2), expected_common_path)

    def test_common_path_for_subdirectory(self):
        path_1 = "/home/user/documents"
        path_2 = "/home/user/documents/subdir/sample.txt"
        expected_common_path = path_1
        self.assertEqual(get_common_path(path_1, path_2), expected_common_path)

    def test_common_path_for_different_directories(self):
        path_1 = "/home/user/documents"
        path_2 = "/home/user/music"
        expected_common_path = "/home/user"
        self.assertEqual(get_common_path(path_1, path_2), expected_common_path)

    def test_common_path_for_completely_different_paths(self):
        path_1 = "/home/user/documents"
        path_2 = "/var/log"
        expected_common_path = "/"
        self.assertEqual(get_common_path(path_1, path_2), expected_common_path)
