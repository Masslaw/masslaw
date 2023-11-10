from typing import IO

from logic_layer.knowledge_record.data_exporting._exceptions import KnowledgeRecordExportingOutputFileAccessException
from logic_layer.knowledge_record.data_exporting._exceptions import KnowledgeRecordExportingOutputFileTypeException
from shared_layer.file_system_utils import file_system_utils


def assert_export_output_file(file: IO, expected_type: str, context: str = None):
    file_open_mode = file.mode
    if 'w' not in file_open_mode:
        raise KnowledgeRecordExportingOutputFileAccessException(required_access='write')

    file_type = file_system_utils.get_file_type(file.name).replace('.', '')
    expected_type = expected_type.replace('.', '')
    if expected_type != file_type:
        raise KnowledgeRecordExportingOutputFileTypeException(provided_type=file_type, required_type=expected_type, context=context)
