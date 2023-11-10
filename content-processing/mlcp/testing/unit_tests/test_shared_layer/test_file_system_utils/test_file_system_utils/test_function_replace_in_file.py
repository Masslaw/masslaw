import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import replace_in_file


class TestFunctionReplaceInFile(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()
        self.content = "This is a test content with some placeholder."
        with open(self.file_path, 'w') as f:
            f.write(self.content)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_replace_existing_string(self):
        replace_in_file(self.file_path, "placeholder", "unique_string")

        with open(self.file_path, 'r') as f:
            updated_content = f.read()

        self.assertIn("unique_string", updated_content)
        self.assertNotIn("placeholder", updated_content)

    def test_replace_non_existing_string(self):
        original_content = self.content[:]
        replace_in_file(self.file_path, "non_existent_string", "some_string")

        with open(self.file_path, 'r') as f:
            updated_content = f.read()

        self.assertEqual(original_content, updated_content)

    def test_replace_with_special_characters(self):
        special_content = "Special content with ^.*$[\\] patterns."
        special_file_path = tempfile.mktemp()
        with open(special_file_path, 'w') as f:
            f.write(special_content)

        replace_in_file(special_file_path, "\\^\\.\\*\\$\\[\\\\\\]", "REPLACED")

        with open(special_file_path, 'r') as f:
            updated_content = f.read()

        self.assertIn("REPLACED", updated_content)
        os.remove(special_file_path)
