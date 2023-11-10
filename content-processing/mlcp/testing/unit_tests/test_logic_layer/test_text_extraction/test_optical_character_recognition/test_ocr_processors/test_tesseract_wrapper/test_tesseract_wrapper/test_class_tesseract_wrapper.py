import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper import TesseractWrapper


class TestClassTesseractWrapper(unittest.TestCase):

    @patch('logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper._tesseract_wrapper.Image.fromarray')
    @patch('logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper._tesseract_wrapper.pytesseract.pytesseract.image_to_data')
    def test_ocr_text_extraction(self, mock_image_to_data: MagicMock(), mock_fromarray):
        mock_image_to_data.return_value = {
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

        tesseract = TesseractWrapper(languages=['eng'], image_directories=[])
        extracted_items = tesseract._extract_text_in_image([])

        mock_image_to_data.assert_called_once()
        self.assertEqual(extracted_items, [
            [
                [
                    [
                        ('Hello,', (100, 50, 130, 60))
                    ],
                    [
                        ('world!', (130, 80, 155, 90))
                    ]
                ]
            ],
            [
                [
                    [
                        ('Example', (100, 150, 130, 160))
                    ]
                ]
            ]
        ])
