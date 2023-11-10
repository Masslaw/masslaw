import unittest

from shared_layer.file_system_utils._file_system_utils import get_file_name


class TestFunctionGetFileName(unittest.TestCase):

    def test_get_file_name(self):
        result = get_file_name('path/to/file.txt')
        self.assertEqual(result, 'file')

    def test_get_file_name_no_extension(self):
        result = get_file_name('path/to/file')
        self.assertEqual(result, 'file')

    def test_get_file_name_multiple_extensions(self):
        result = get_file_name('path/to/file.tar.gz')
        self.assertEqual(result, 'file.tar')

    def test_get_file_name_remove_extension(self):
        result = get_file_name('path/to/file.txt', remove_extention=True)
        self.assertEqual(result, 'file')

    def test_get_file_name_remove_extension_no_extension(self):
        result = get_file_name('path/to/file', remove_extention=True)
        self.assertEqual(result, 'file')

    def test_get_file_name_remove_extension_multiple_extensions(self):
        result = get_file_name('path/to/file.tar.gz', remove_extention=True)
        self.assertEqual(result, 'file.tar')
