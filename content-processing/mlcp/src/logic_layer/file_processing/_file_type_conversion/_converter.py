from abc import abstractmethod
from typing import Set

from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import logger


class FileConverter:
    supported_file_types: Set[str] = []
    output_file_type: str = ""

    @classmethod
    @logger.process_function("Converting an file")
    def convert(cls, file_path: str, output_directory: str) -> str:
        if file_system_utils.get_file_type(file_path).replace(".", "") not in cls.supported_file_types:
            raise ValueError("Provided file type is not supported by this converter")
        file_system_utils.clear_directory(output_directory)
        output_file_path = file_system_utils.join_paths(output_directory, f"{cls.output_file_type}.{cls.output_file_type}")
        cls._do_convert(file_path, output_file_path)
        return output_file_path

    @classmethod
    @abstractmethod
    def _do_convert(cls, file_path: str, output_file_path: str):
        pass
