import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import remove_dir


class TestFunctionRemoveDir(unittest.TestCase):
    def test_function_remove_dir_on_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = os.path.join(temp_dir, 'test_dir')
            os.makedirs(directory)
            self.assertTrue(os.path.exists(directory))
            remove_dir(temp_dir)
            self.assertFalse(os.path.exists(temp_dir))

    def test_function_remove_dir_on_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, 'test_file.txt')
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write('test')
                self.assertTrue(os.path.isfile(temp_file_path))
                remove_dir(temp_file_path)
                self.assertFalse(os.path.isfile(temp_file_path))
