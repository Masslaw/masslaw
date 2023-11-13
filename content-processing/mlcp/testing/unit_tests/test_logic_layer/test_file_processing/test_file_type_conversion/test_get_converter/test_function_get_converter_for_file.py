import shutil
import tempfile
import unittest

from logic_layer.file_processing._file_type_conversion import get_converter_for_file
from logic_layer.file_processing._file_type_conversion._to_pdf import PdfToPdf, ImageToPdf, WordToPdf


class TestFunctionGetConverterForFile(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        shutil.rmtree(self.tempdir.name)

    def _create_file_of_type(self, file_type):
        file = tempfile.NamedTemporaryFile(suffix=file_type, dir=self.tempdir.name, delete=False)
        with open(file.name, 'w') as f: f.write('test')
        return file.name

    def test_with_pdf(self):
        pdf_file = self._create_file_of_type(".pdf")
        converter = get_converter_for_file(pdf_file)
        self.assertEqual(converter, PdfToPdf)

    def test_with_images(self):
        png_file = self._create_file_of_type(".png")
        converter = get_converter_for_file(png_file)
        self.assertEqual(converter, ImageToPdf)
        png_file = self._create_file_of_type(".jpeg")
        converter = get_converter_for_file(png_file)
        self.assertEqual(converter, ImageToPdf)
        png_file = self._create_file_of_type(".tif")
        converter = get_converter_for_file(png_file)
        self.assertEqual(converter, ImageToPdf)
        png_file = self._create_file_of_type(".jpg")
        converter = get_converter_for_file(png_file)
        self.assertEqual(converter, ImageToPdf)

    def test_with_word_files(self):
        file = self._create_file_of_type(".doc")
        converter = get_converter_for_file(file)
        self.assertEqual(converter, WordToPdf)
        file = self._create_file_of_type(".docx")
        converter = get_converter_for_file(file)
        self.assertEqual(converter, WordToPdf)
