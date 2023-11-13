import inspect
from typing import List

from logic_layer.file_processing._exceptions import FileTypeNotSupportedException
from logic_layer.file_processing._file_type_conversion import get_converter_for_file
from logic_layer.file_processing._processors import FileProcessor
from shared_layer.file_system_utils import file_system_utils
from shared_layer.file_system_utils import file_system_utils_assertions
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


def convert_file_to_a_processable_file(file_path: str, output_directory: str) -> str:
    file_converter = get_converter_for_file(file_path)
    if not file_converter:
        raise FileTypeNotSupportedException(file_path)
    output_file = file_converter.convert(file_path, output_directory)
    return output_file


def create_processor(file_path: str, languages: List[str]) -> FileProcessor:
    file_system_utils_assertions.assert_directory_exists(file_path)
    file_type = file_system_utils.get_file_type(file_path)
    logger.info(F'Creating processor for file {common_formats.value(file_path)} of type {common_formats.value(file_type)}')
    if file_type.lower().replace(".", "") in ("pdf",):
        from ._processors.pdf_processor import PdfProcessor
        return PdfProcessor(file=file_path, languages=languages)
    else:
        raise FileTypeNotSupportedException(file_path)
