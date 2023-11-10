import unittest

from shared_layer.file_system_utils._file_system_utils import join_paths


class TestFunctionJoinPaths(unittest.TestCase):

    def test_join_paths(self):
        result = join_paths('absolute', 'path/to/', 'file.txt')
        self.assertEqual(result, 'absolute/path/to/file.txt')
