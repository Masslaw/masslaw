import os
import subprocess
from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from shared_layer.mlcp_logger import logger
from shared_layer.file_system_utils import file_system_utils


class WordToPdf(FileConverter):
    supported_file_types = {"doc", "docx"}
    output_file_type = "pdf"

    @classmethod
    @logger.process_function("Converting a word file to PDF")
    def _do_convert(cls, doc_path: str, output_file_path: str):
        output_dir = file_system_utils.get_parent_dir(output_file_path)
        command = [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            output_dir,
            doc_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Error in converting a word file to PDF: {result.stderr.decode('utf-8')}")
        original_output_file = file_system_utils.get_file_name(doc_path) + ".pdf"
        original_output_path = file_system_utils.join_paths(output_dir, original_output_file)
        os.rename(original_output_path, output_file_path)
