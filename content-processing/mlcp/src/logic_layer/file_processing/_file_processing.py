from typing import List

from logic_layer.file_processing._exceptions import NoProcessorForFileException
from logic_layer.file_processing._processors import FileProcessor
from shared_layer.file_system_utils import file_system_utils
from shared_layer.file_system_utils import file_system_utils_assertions
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


def create_processor(file: str, languages: List[str]) -> FileProcessor:
    file_system_utils_assertions.assert_directory_exists(file)
    file_type = file_system_utils.get_file_type(file)
    logger.info(F'Creating processor for file {common_formats.value(file)} of type {common_formats.value(file_type)}')
    if file_type.lower() in (".pdf",):
        from ._processors.pdf_processor import PdfProcessor
        return PdfProcessor(file=file, languages=languages)
    elif file_type in (".bmp", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".jpeg", ".jpg", ".jpe", ".jp2", ".tiff", ".tif", ".png", ".exr", ".hdr", ".pic", ".webp"):
        from ._processors.image_processor import ImageProcessor
        return ImageProcessor(file=file, languages=languages)
    else:
        raise NoProcessorForFileException(file)
