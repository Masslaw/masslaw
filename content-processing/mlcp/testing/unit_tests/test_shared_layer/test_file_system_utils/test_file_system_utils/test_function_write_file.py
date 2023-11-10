import os
import tempfile
import unittest

from shared_layer.file_system_utils._file_system_utils import write_file


class TestFunctionWriteFile(unittest.TestCase):

    def setUp(self):
        self.file_path = tempfile.mktemp()

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_write_to_file(self):
        contents = "Sample test content"
        write_file(self.file_path, contents)

        with open(self.file_path, 'r') as f:
            read_contents = f.read()
        self.assertEqual(read_contents, contents)

    def test_overwrite_existing_file(self):
        initial_content = "Initial content"
        overwrite_content = "Overwritten content"
        with open(self.file_path, 'w') as f:
            f.write(initial_content)

        write_file(self.file_path, overwrite_content)

        with open(self.file_path, 'r') as f:
            read_contents = f.read()
        self.assertEqual(read_contents, overwrite_content)

    def test_write_empty_content(self):
        write_file(self.file_path, "")

        with open(self.file_path, 'r') as f:
            read_contents = f.read()
        self.assertEqual(read_contents, "")
