from typing import IO

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._exceptions import DocumentLoadingInputFileTypeException
from shared_layer.file_system_utils import file_system_utils


def assert_load_input_file(file: IO, expected_type: str, context: str = None):
    file_type = file_system_utils.get_file_type(file.name).replace('.', '')
    expected_type = expected_type.replace('.', '')
    if expected_type != file_type:
        raise DocumentLoadingInputFileTypeException(provided_type=file_type, required_type=expected_type, context=context)
