from abc import abstractmethod
from typing import List

import numpy as np

from logic_layer.text_extraction.optical_character_recognition import OcrExtractedElement
from shared_layer.concurrency_utils import run_process_batch
from shared_layer.memory_utils.controlled_data_loading import MemoryControlledDataLoadingManager
from shared_layer.memory_utils.controlled_data_loading.builtin_loaders import MemoryControlledOpenCVImageLoader
from shared_layer.mlcp_logger import logger


class OCRProcessor:

    def __init__(self, languages: List[str], image_directories: List[str] = None):
        self._languages = languages
        self.__image_directories = image_directories or []
        self.__text_data = []

    def set_image_directories(self, image_directories: List[str]):
        self.__image_directories = image_directories

    def get_extracted_text_data(self) -> List[List[OcrExtractedElement]]:
        return self.__text_data

    @logger.process_function("Extracting text data in images using ocr", max_memory_record=True)
    def perform_text_extraction(self, max_memory_usage=(2 ** 20)):
        image_loader = MemoryControlledOpenCVImageLoader()
        data_loading_manager = MemoryControlledDataLoadingManager(loader=image_loader,
            chunk_processing_function=self.__extract_text_in_loaded_chunk, max_memory_usage=max_memory_usage)
        data_loading_manager.load_and_process_data_chunks(load_inputs=self.__image_directories)

    def __extract_text_in_loaded_chunk(self, images: List[np.array]):
        text_data = self.__extract_text_in_images(images)
        self.__text_data.extend(text_data)

    def __extract_text_in_images(self, images: List[np.array]) -> List[List[OcrExtractedElement]]:
        text_data = run_process_batch(func=self._extract_text_in_image, batch_inputs=images)
        return text_data

    @abstractmethod
    def _extract_text_in_image(self, images: np.array) -> List[OcrExtractedElement]:
        pass
