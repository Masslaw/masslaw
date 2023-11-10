import unittest
from unittest.mock import Mock, patch
from typing import List
import numpy as np

from logic_layer.text_extraction.optical_character_recognition._ocr_processor import OCRProcessor


class TestOCRProcessor(unittest.TestCase):

    def setUp(self):
        self.languages = ["eng"]
        self.image_directories = ["path/to/images"]
        self.ocr_processor = OCRProcessor(languages=self.languages, image_directories=self.image_directories)

    def test_constructor(self):
        self.assertEqual(self.ocr_processor._languages, self.languages)
        self.assertIsNotNone(self.ocr_processor._OCRProcessor__image_directories)

    def test_set_image_directories(self):
        new_directories = ["new/path/to/images"]
        self.ocr_processor.set_image_directories(new_directories)
        self.assertEqual(self.ocr_processor._OCRProcessor__image_directories, new_directories)

    def test_get_extracted_text_data(self):
        self.ocr_processor._OCRProcessor__text_data = [["sample", "data"]]
        self.assertEqual(self.ocr_processor.get_extracted_text_data(), [["sample", "data"]])

    @patch('logic_layer.text_extraction.optical_character_recognition._ocr_processor.MemoryControlledDataLoadingManager')
    @patch('logic_layer.text_extraction.optical_character_recognition._ocr_processor.MemoryControlledOpenCVImageLoader')
    def test_perform_text_extraction(self, mock_image_loader, mock_data_manager):
        mock_manager_instance = mock_data_manager.return_value
        self.ocr_processor.perform_text_extraction(max_memory_usage=(2 ** 20))

        mock_data_manager.assert_called_once_with(loader=mock_image_loader.return_value, chunk_processing_function=self.ocr_processor._OCRProcessor__extract_text_in_loaded_chunk,
            max_memory_usage=(2 ** 20))

        mock_manager_instance.load_and_process_data_chunks.assert_called_once_with(load_inputs=self.image_directories)
