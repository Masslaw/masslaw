import unittest

from shared_layer.file_system_utils._file_system_utils import get_file_type


class TestFunctionGetFileType(unittest.TestCase):

    def test_get_file_type(self):
        result = get_file_type('path/to/file.txt')
        self.assertEqual(result, '.txt')

    def test_get_file_type_no_extension(self):
        result = get_file_type('path/to/file')
        self.assertEqual(result, '')

    def test_get_file_type_multiple_extensions(self):
        self.assertEqual(get_file_type('path/to/file.tar.gz'), '.gz')
