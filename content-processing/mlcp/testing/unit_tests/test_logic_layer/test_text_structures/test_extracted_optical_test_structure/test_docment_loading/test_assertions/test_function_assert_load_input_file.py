import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._assertions import assert_load_input_file
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._exceptions import DocumentLoadingInputFileTypeException


class TestAssertLoadInputFileFunction(unittest.TestCase):

    def test_invalid_file_type_raises_exception(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as test_file:
            with self.assertRaises(DocumentLoadingInputFileTypeException):
                assert_load_input_file(file=test_file, expected_type='json')

    def test_valid_conditions_no_exception(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.json') as test_file:
            assert_load_input_file(file=test_file, expected_type='json')
