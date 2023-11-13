from typing import List

import cv2

from logic_layer.text_extraction.optical_character_recognition import OcrExtractedElement
from logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper import TesseractWrapper
from logic_layer.text_extraction.optical_character_recognition.text_document_building import OpticalTextDocumentBuilder
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_metadata import DocumentMetadataHandler
from logic_layer.file_processing._processors.pdf_processor._config import extracted_optical_text_structure_hierarchy_formation
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class OpticalDocumentExtractor:

    def __init__(self, languages: List[str]):
        logger.info(f'Created an OpticalDocumentExtractor instance with languages: {common_formats.value(languages)}')
        self._languages = languages

    @logger.process_function('Extracting text document')
    def extract_text_document(self, image_directories: List[str]) -> ExtractedOpticalTextDocument:
        logger.info(f'Extracting text document from {common_formats.value(len(image_directories))} images')
        ocr_output_data = self._extract_data_using_ocr(image_directories)
        extracted_text_document = self._build_text_document(ocr_output_data)
        self._put_image_sizes_in_document_metadata(extracted_text_document, image_directories)
        return extracted_text_document

    @logger.process_function('Extracting text document using OCR')
    def _extract_data_using_ocr(self, image_directories) -> List[List[OcrExtractedElement]]:
        text_extractor = TesseractWrapper(languages=self._languages)
        text_extractor.set_image_directories(image_directories=image_directories)
        text_extractor.perform_text_extraction()
        ocr_output_data = text_extractor.get_extracted_text_data()
        return ocr_output_data

    @logger.process_function('Building text document from OCR output')
    def _build_text_document(self, ocr_output_data) -> ExtractedOpticalTextDocument:
        ocr_document_builder = OpticalTextDocumentBuilder(hierarchy_formation=extracted_optical_text_structure_hierarchy_formation)
        extracted_text_document = ocr_document_builder.build_document_structure_from_structured_ocr_output(ocr_output_data)
        return extracted_text_document

    @logger.process_function('Putting image sizes in document metadata')
    def _put_image_sizes_in_document_metadata(self, extracted_text_document, image_directories):
        metadata_handler = DocumentMetadataHandler(extracted_text_document)
        for image_num, image_directory in enumerate(image_directories):
            _image = cv2.imread(image_directory)
            image_size = _image.shape[:2]
            logger.debug(f'Image number: {common_formats.value(image_num)} size: {common_formats.value(image_size)}')
            metadata_handler.put_metadata_item(['structure', 'image_sizes', str(image_num)], 'image_size', {'n': image_num, 'w': image_size[1], 'h': image_size[0], })
