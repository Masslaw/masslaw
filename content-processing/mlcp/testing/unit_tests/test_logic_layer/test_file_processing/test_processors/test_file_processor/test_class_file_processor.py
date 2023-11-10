import os
import tempfile
import unittest

from logic_layer.file_processing._processors import FileProcessor


class TestClassFileProcessor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mocked_file_path = os.path.join(self.temp_dir, "mockedFile")
        with open(self.mocked_file_path, 'w') as f:
            f.write("Mocked content")

        self.processor = FileProcessor(self.mocked_file_path, ['en'])

    def tearDown(self):
        os.remove(self.mocked_file_path)
        os.rmdir(self.temp_dir)

    def test_set_file(self):
        new_mocked_file_path = os.path.join(self.temp_dir, "newMockedFile")
        with open(new_mocked_file_path, 'w') as f:
            f.write("New mocked content")

        self.processor.set_file(new_mocked_file_path)
        self.assertEqual(self.processor._file, new_mocked_file_path)

        os.remove(new_mocked_file_path)

    def test_process(self):
        self.processor.process()

    def test_export_metadata(self):
        self.processor.export_metadata()

    def test_export_text(self):
        self.processor.export_text()

    def test_export_assets(self):
        self.processor.export_assets()

    def test_export_debug_data(self):
        self.processor.export_debug_data()
