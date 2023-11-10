import unittest


from logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper._output_parsing import get_entry_path_from_tesseract_output


class TestFunctionGetEntryPathFromTessearctOutput(unittest.TestCase):

    def test_normal(self):
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

        self.assertEqual(get_entry_path_from_tesseract_output(tesseract_output, 0), (0, 0, 0, 0))
        self.assertEqual(get_entry_path_from_tesseract_output(tesseract_output, 1), (0, 0, 1, 0))
        self.assertEqual(get_entry_path_from_tesseract_output(tesseract_output, 2), (1, 0, 0, 0))

    def test_test_out_of_range(self):

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

        with self.assertRaises(IndexError):
            get_entry_path_from_tesseract_output(tesseract_output, 3)
