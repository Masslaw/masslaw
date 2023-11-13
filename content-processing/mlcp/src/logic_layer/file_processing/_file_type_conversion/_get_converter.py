from typing import Type, List

from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from logic_layer.file_processing._file_type_conversion._to_pdf import DocxToPdf
from logic_layer.file_processing._file_type_conversion._to_pdf import ImageToPdf
from logic_layer.file_processing._file_type_conversion._to_pdf import PdfToPdf
from shared_layer.file_system_utils import file_system_utils


__all_converters: List[Type[FileConverter]] = [
    PdfToPdf,
    ImageToPdf,
    DocxToPdf,
]


def get_converter_for_file(file_path: str) -> Type[FileConverter] | None:
    file_type = file_system_utils.get_file_type(file_path).replace(".", "")
    for converter in __all_converters:
        if file_type not in converter.supported_file_types: continue
        return converter
