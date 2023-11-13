import shutil
import tempfile
import unittest
from unittest.mock import patch

from logic_layer.file_processing import create_processor
from logic_layer.file_processing._exceptions import FileTypeNotSupportedException
from shared_layer.file_system_utils._exceptions import InvalidPathOrDirectory


class TestFunctionCreateProcessor(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()

        _patcher = patch('logic_layer.file_processing._processors.pdf_processor.PdfProcessor')
        self.mock_pdf_processor = _patcher.start()

        self.pdf_processor_patcher = patch('logic_layer.file_processing._processors.pdf_processor.PdfProcessor')
        self.pdf_processor_class = self.pdf_processor_patcher.start()

    def tearDown(self):
        self.pdf_processor_patcher.stop()
        shutil.rmtree(self.tempdir.name)

    def _create_file_of_type(self, file_type):
        file = tempfile.NamedTemporaryFile(suffix=file_type, dir=self.tempdir.name, delete=False)
        with open(file.name, 'w') as f: f.write('test')
        return file.name

    def test_create_processor_on_non_existent_file(self):
        with self.assertRaises(InvalidPathOrDirectory):
            create_processor('non_existent_file.pdf', ['en'])

    def test_create_processor_on_unknown_file(self):
        file = self._create_file_of_type('.unknown')
        with self.assertRaises(FileTypeNotSupportedException):
            create_processor(file, ['en'])

    def test_create_processor_on_file_with_no_extension(self):
        file = self._create_file_of_type('')
        with self.assertRaises(FileTypeNotSupportedException):
            create_processor(file, ['en'])

    def test_create_processor_on_pdf_file(self):
        for file_type in ('.pdf', '.PDF'):
            file = self._create_file_of_type(file_type)
            processor = create_processor(file, ['en'])
            self.pdf_processor_class.assert_called_once_with(file=file, languages=['en'])
            self.assertEqual(processor, self.pdf_processor_class.return_value)
            self.pdf_processor_class.reset_mock()
