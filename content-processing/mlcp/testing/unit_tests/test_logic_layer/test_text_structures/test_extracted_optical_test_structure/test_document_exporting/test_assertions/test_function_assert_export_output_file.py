import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import assert_export_output_file
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileAccessException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException


class TestAssertExportOutputFileFunction(unittest.TestCase):

    def test_file_not_writable_raises_exception(self):
        with tempfile.NamedTemporaryFile('r') as test_file:
            with self.assertRaises(DocumentExportingOutputFileAccessException):
                assert_export_output_file(file=test_file, expected_type='json')

    def test_invalid_file_type_raises_exception(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as test_file:
            with self.assertRaises(DocumentExportingOutputFileTypeException):
                assert_export_output_file(file=test_file, expected_type='json')

    def test_valid_conditions_no_exception(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.json') as test_file:
            assert_export_output_file(file=test_file, expected_type='json')
