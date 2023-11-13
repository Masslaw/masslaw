import shutil
import tempfile
import unittest
from unittest.mock import Mock

from logic_layer.file_processing._file_type_conversion._converter import FileConverter

class TestClassFileConverter(unittest.TestCase):

    def setUp(self):
        converter_class = FileConverter
        converter_class.supported_file_types = {"type1", "type2"}
        converter_class.output_file_type = "type3"
        self.converter = converter_class()
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        shutil.rmtree(self.tempdir.name)

    def _create_file_of_type(self, file_type):
        file = tempfile.NamedTemporaryFile(suffix=file_type, dir=self.tempdir.name, delete=False)
        with open(file.name, 'w') as f: f.write('test')
        return file.name

    def test_convert_supported_file_type(self):
        file = self._create_file_of_type(".type1")
        self.converter.convert(file, self.tempdir.name)

    def test_convert_non_supported_file_type(self):
        file = self._create_file_of_type(".type3")
        with self.assertRaises(ValueError):
            self.converter.convert(file, self.tempdir.name)


