import os
import shutil
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import clear_directory


class TestFunctionClearDirectory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_clear_existing_directory(self):
        sub_dir = os.path.join(self.temp_dir, 'existing_directory')
        os.makedirs(sub_dir)
        self.assertTrue(os.path.exists(sub_dir))

        clear_directory(sub_dir)
        self.assertTrue(os.path.exists(sub_dir))

    def test_clear_nonexistent_directory(self):
        non_existent_dir = os.path.join(self.temp_dir, 'non_existent_directory')
        self.assertFalse(os.path.exists(non_existent_dir))

        clear_directory(non_existent_dir)
        self.assertTrue(os.path.exists(non_existent_dir))
