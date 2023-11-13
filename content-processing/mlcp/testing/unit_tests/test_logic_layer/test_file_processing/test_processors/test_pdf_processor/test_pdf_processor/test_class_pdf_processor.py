import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, Mock, MagicMock

import numpy as np

from logic_layer.file_processing._processors.pdf_processor._pdf_processor import PdfProcessor
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument, \
    OpticalStructureHierarchyLevel
from shared_layer.file_system_utils._exceptions import InvalidPathOrDirectory
from shared_layer.memory_utils.storage_cached_image import StorageCachedImage


class TestClassPdfProcessor(unittest.TestCase):

    def setUp(self):
        self.pdf_directory = tempfile.TemporaryDirectory()
        self.pdf_file = os.path.join(self.pdf_directory.name, "test_pdf.pdf")

        with open(self.pdf_file, 'w') as f:
            f.write('Dummy PDF content')

        self.languages = ['eng']
        self.test_processor = PdfProcessor(file=self.pdf_file, languages=self.languages)

        self.page_image_data = np.array([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]])
        self.page_image_cached_image = StorageCachedImage()
        self.page_image_cached_image.set_image(self.page_image_data)

        self.pdf_loader_patcher = patch('logic_layer.file_processing._processors.pdf_processor._pdf_file_loader.PdfFileLoader.get_page_images', return_value=[self.page_image_cached_image])
        self.pdf_loader_patcher.start()

        self.pdfinfo_from_path_patcher = patch('logic_layer.file_processing._processors.pdf_processor._pdf_file_loader.pdfinfo_from_path')
        self.pdfinfo_from_path = self.pdfinfo_from_path_patcher.start()
        self.pdfinfo_from_path.return_value = {'Pages': 1}

    def tearDown(self):
        self.pdf_loader_patcher.stop()
        self.pdfinfo_from_path_patcher.stop()
        shutil.rmtree(self.pdf_directory.name)

    def test_init(self):
        test_processor = PdfProcessor(file=self.pdf_file, languages=self.languages)

    def test_with_no_real_pdf(self):
        with self.assertRaises(InvalidPathOrDirectory):
            PdfProcessor(file="test_pdf.pdf", languages=self.languages)

    def test_process(self):
        image_directories = ["image_dir1", "image_dir2"]

        with patch('logic_layer.file_processing._processors.pdf_processor._pdf_processor.PdfFileLoader.get_page_images_as_directories', return_value=image_directories):
            with patch('logic_layer.file_processing._processors.pdf_processor._pdf_processor.PdfFileLoader.extract_existing_optical_text_document') as mock_extract_existing_optical_text_document:
                with patch('logic_layer.file_processing._processors.pdf_processor._pdf_processor.PdfFileLoader.create_page_images_with_no_text_elements') as mock_create_page_images_with_no_text_elements:
                    with patch('logic_layer.file_processing._processors.pdf_processor._pdf_processor.PdfFileLoader.get_optical_text_document') as mock_get_optical_text_document:
                        with patch('logic_layer.file_processing._processors.pdf_processor._pdf_processor.OpticalDocumentExtractor') as mock_extracted_document_extraction:
                            extracted_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])
                            existing_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])
                            mock_extracted_document_extraction.return_value.extract_text_document.return_value = extracted_document
                            mock_get_optical_text_document.return_value = existing_document
                            mock_extract_existing_optical_text_document.side_effect = lambda: ...
                            mock_create_page_images_with_no_text_elements.return_value = []

                            self.test_processor._process()

                            merged_document = extracted_document
                            merged_document.get_structure_root().set_children(merged_document.get_structure_root().get_children() + existing_document.get_structure_root().get_children())

                            self.assertEqual(self.test_processor._extracted_text_document, merged_document)

    def test_export_text(self):
        output_dir = tempfile.TemporaryDirectory().name

        self.test_processor._extracted_text_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])

        self.test_processor._export_text(output_dir=output_dir)

        self.assertSetEqual(set(os.listdir(output_dir)), {'text_structure.xml', 'plain_text.txt'})
        shutil.rmtree(output_dir)

    def test_export_assets(self):
        output_dir = tempfile.TemporaryDirectory().name

        self.test_processor._extracted_text_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.WORD])

        with patch('logic_layer.file_processing._processors.pdf_processor._pdf_file_loader.pypdf') as mock_pypdf:
            mock_pypdf.PdfReader.return_value = MagicMock()
            mock_pypdf.PdfWriter.return_value = MagicMock()
            mock_pypdf.PdfWriter.return_value.add_page = MagicMock()
            mock_pypdf.PdfWriter.return_value.write.return_value = lambda f: f.write("hi")

            self.test_processor._export_assets(output_dir=output_dir)

        self.assertSetEqual(set(os.listdir(output_dir)), {'page_0.pdf', 'page_0.png', 'display.html'})
        shutil.rmtree(output_dir)
