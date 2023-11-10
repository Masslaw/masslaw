import os.path
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import make_dir


class TestFunctionMakeDir(unittest.TestCase):

    def setUp(self):
        self.dir_path = tempfile.mktemp()

    def tearDown(self):
        if os.path.exists(self.dir_path):
            os.rmdir(self.dir_path)

    def test_make_dir_new(self):
        self.assertFalse(os.path.exists(self.dir_path))
        make_dir(self.dir_path)
        self.assertTrue(os.path.isdir(self.dir_path))

    def test_make_dir_existing_with_override(self):
        os.makedirs(self.dir_path)
        self.assertTrue(os.path.isdir(self.dir_path))
        make_dir(self.dir_path, override=True)
        self.assertTrue(os.path.isdir(self.dir_path))

    def test_make_dir_existing_without_override(self):
        os.makedirs(self.dir_path)
        self.assertTrue(os.path.isdir(self.dir_path))
        make_dir(self.dir_path, override=False)
        self.assertTrue(os.path.isdir(self.dir_path))
