from typing import IO

from service.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileAccessException
from service.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException
from service.file_system_utils import file_system_utils


def assert_export_output_file(file: IO, expected_type: str, context: str = None):
    if not file.writable():
        raise DocumentExportingOutputFileAccessException(required_access='write')

    file_type = file_system_utils.get_file_type(file.name).replace('.', '')
    expected_type = expected_type.replace('.', '')
    if expected_type != file_type:
        raise DocumentExportingOutputFileTypeException(provided_type=file_type, required_type=expected_type, context=context)
