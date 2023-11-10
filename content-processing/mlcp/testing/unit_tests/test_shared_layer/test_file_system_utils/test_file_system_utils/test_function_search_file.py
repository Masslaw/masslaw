import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import search_file


class TestFunctionSearchFile(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        self.content = "This is a test content with some unique_string."
        with open(self.file_path, 'w') as f:
            f.write(self.content)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_search_existing_string(self):
        self.assertTrue(search_file(self.file_path, "unique_string"))

    def test_search_non_existing_string(self):
        self.assertFalse(search_file(self.file_path, "non_existent_string"))

    def test_search_with_special_characters(self):
        special_content = "Special content with ^.*$[\\] patterns."
        special_file_path = tempfile.mktemp()
        with open(special_file_path, 'w') as f:
            f.write(special_content)

        self.assertTrue(search_file(special_file_path, "\\^\\.\\*\\$\\[\\\\\\]"))
        os.remove(special_file_path)

    def test_search_in_empty_file(self):
        empty_file_path = tempfile.mktemp()
        with open(empty_file_path, 'w') as f:
            pass
        self.assertFalse(search_file(empty_file_path, "any_string"))
        os.remove(empty_file_path)
