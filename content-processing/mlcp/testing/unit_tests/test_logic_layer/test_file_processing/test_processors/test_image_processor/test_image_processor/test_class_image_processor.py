import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument, \
    OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.file_processing._processors.image_processor._image_processor import ImageProcessor
from shared_layer.file_system_utils._exceptions import InvalidPathOrDirectory


class TestClassImageProcessor(unittest.TestCase):

    def setUp(self):
        self.image_directory = tempfile.TemporaryDirectory()
        self.image_file = os.path.join(self.image_directory.name, "test_image.png")
        self.image_data = np.array([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]])
        cv2.imwrite(self.image_file, self.image_data)
        self.languages = ['eng']
        self.test_processor = ImageProcessor(file=self.image_file, languages=self.languages)

    def tearDown(self):
        shutil.rmtree(self.image_directory.name)

    @patch('logic_layer.file_processing._processors.image_processor._image_processor.StorageCachedImage')
    @patch('cv2.imread')
    def test_init(self, mocked_imread, mocked_storage_cached_data):
        test_processor = ImageProcessor(file=self.image_file, languages=self.languages)
        mocked_storage_cached_data.return_value.set_image.assert_called_once()
        mocked_imread.assert_called_once_with(self.image_file)

    def test_with_no_real_image(self):
        with self.assertRaises(InvalidPathOrDirectory):
            ImageProcessor(file="test_image.png", languages=self.languages)

    @patch('logic_layer.file_processing._processors.image_processor._image_processor.OpticalDocumentExtractor')
    def test_process(self, mocked_optical_document_extractor):
        extracted_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])
        mocked_optical_document_extractor.return_value.extract_text_document.return_value = extracted_document

        self.test_processor._process()

        self.assertEqual(self.test_processor._extracted_text_document, extracted_document)
        mocked_optical_document_extractor.return_value.extract_text_document.assert_called_once()

    def test_export_text(self):
        output_dir = tempfile.TemporaryDirectory().name

        self.test_processor._extracted_text_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])

        self.test_processor._export_text(output_dir=output_dir)

        self.assertSetEqual(set(os.listdir(output_dir)), {'text_structure.xml', 'plain_text.txt'})
        shutil.rmtree(output_dir)

    def test_export_assets(self):
        output_dir = tempfile.TemporaryDirectory().name

        self.test_processor._extracted_text_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])

        self.test_processor._export_assets(output_dir=output_dir)

        self.assertSetEqual(set(os.listdir(output_dir)), {'image_0.png', 'text_layer.html'})
        shutil.rmtree(output_dir)
