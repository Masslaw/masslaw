from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import logger


class PdfToPdf(FileConverter):
    supported_file_types = {"pdf"}
    output_file_type = "pdf"

    @classmethod
    @logger.process_function("Converting a PDF file to pdf")
    def _do_convert(cls, file_path: str, output_file_path: str):
        file_system_utils.copy_file(file_path, output_file_path)
