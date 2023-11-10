import unittest

from logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper._output_parsing import put_entry_in_entry_structure


class TestFunctionPutEntryInEntryStructure(unittest.TestCase):

    def test_valid(self):
        tesseract_output = {
            'block_num': [1, 1, 2],
            'par_num': [1, 1, 1],
            'line_num': [1, 2, 1],
            'word_num': [1, 1, 1],
            'left': [100, 130, 100],
            'top': [50, 80, 150],
            'width': [30, 25, 30],
            'height': [10, 10, 10],
            'conf': [90, 85, 92],
            'text': ['Hello,', 'world!', 'Example']
        }
