import unittest
from unittest.mock import Mock
from unittest.mock import patch

from logic_layer.text_extraction.optical_character_recognition import OcrExtractedElement
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.file_processing._processors._optical_shared._optical_document_extraction import OpticalDocumentExtractor


class TestClassOpticalDocumentExtractor(unittest.TestCase):

    def setUp(self):
        self.languages = ['eng']
        self.test_extractor = OpticalDocumentExtractor(languages=self.languages)

    @patch('logic_layer.file_processing._processors._optical_shared._optical_document_extraction.TesseractWrapper')
    def test_extract_data_using_ocr(self, mocked_tesseract_wrapper):
        image_directories = ['test_dir']
        mocked_ocr_data = [[Mock(spec=OcrExtractedElement)]]

        instance = mocked_tesseract_wrapper.return_value
        instance.get_extracted_text_data.return_value = mocked_ocr_data

        result = self.test_extractor._extract_data_using_ocr(image_directories)

        self.assertEqual(result, mocked_ocr_data)
        instance.set_image_directories.assert_called_with(image_directories=image_directories)
        instance.perform_text_extraction.assert_called_once()

    @patch('logic_layer.file_processing._processors._optical_shared._optical_document_extraction.OpticalTextDocumentBuilder')
    def test_build_text_document(self, mocked_document_builder):
        ocr_output_data = [[Mock(spec=OcrExtractedElement)]]
        mocked_document = Mock(spec=ExtractedOpticalTextDocument)

        instance = mocked_document_builder.return_value
        instance.build_document_structure_from_structured_ocr_output.return_value = mocked_document

        result = self.test_extractor._build_text_document(ocr_output_data)

        self.assertEqual(result, mocked_document)

    @patch('cv2.imread')
    @patch('logic_layer.file_processing._processors._optical_shared._optical_document_extraction.DocumentMetadataHandler')
    def test_put_image_sizes_in_document_metadata(self, mocked_document_metadata_handler, mocked_imread):
        extracted_text_document = Mock(spec=ExtractedOpticalTextDocument)

        mocked_image = Mock()
        mocked_image.shape = (100, 200, 3)
        mocked_imread.return_value = mocked_image

        metadata_handler_instance = mocked_document_metadata_handler.return_value

        self.test_extractor._put_image_sizes_in_document_metadata(extracted_text_document, ['test_dir'])

        mocked_imread.assert_called_once_with('test_dir')
        metadata_handler_instance.put_metadata_item.assert_called_once_with(['structure', 'image_sizes', '0'], 'image_size', {'n': 0, 'w': 200, 'h': 100})

    @patch.object(OpticalDocumentExtractor, '_extract_data_using_ocr')
    @patch.object(OpticalDocumentExtractor, '_build_text_document')
    @patch.object(OpticalDocumentExtractor, '_put_image_sizes_in_document_metadata')
    def test_extract_text_document(self, mocked_put_image_sizes, mocked_build_text_document, mocked_extract_data):
        image_directories = ['test_dir']
        mocked_document = Mock(spec=ExtractedOpticalTextDocument)

        mocked_extract_data.return_value = [[Mock(spec=OcrExtractedElement)]]
        mocked_build_text_document.return_value = mocked_document

        result = self.test_extractor.extract_text_document(image_directories)

        self.assertEqual(result, mocked_document)
        mocked_extract_data.assert_called_once_with(image_directories)
        mocked_build_text_document.assert_called_once()
        mocked_put_image_sizes.assert_called_once_with(mocked_document, image_directories)
