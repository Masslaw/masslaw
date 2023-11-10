from abc import abstractmethod
from typing import List

from shared_layer.file_system_utils import file_system_utils
from shared_layer.file_system_utils import file_system_utils_assertions
from shared_layer.mlcp_logger import logger


class FileProcessor:
    _file: str
    _file_type: str
    _languages: List[str]

    def __init__(self, file: str, languages: List[str]):
        self.set_file(file)
        self._languages = languages

    def set_file(self, file_dir: str):
        file_system_utils_assertions.assert_directory_exists(file_dir)
        self._file = file_dir
        self._file_type = file_system_utils.get_file_type(self._file)

    @logger.process_function("Processing file")
    def process(self):
        self._process()

    @abstractmethod
    def _process(self):
        pass

    @logger.process_function("Exporting file metadata")
    def export_metadata(self, output_dir=""):
        self._export_metadata(output_dir=output_dir)

    @abstractmethod
    def _export_metadata(self, output_dir=""):
        pass

    @logger.process_function("Exporting file text")
    def export_text(self, output_dir=""):
        self._export_text(output_dir=output_dir)

    @abstractmethod
    def _export_text(self, output_dir=""):
        pass

    @logger.process_function("Exporting file assets")
    def export_assets(self, output_dir=""):
        self._export_assets(output_dir=output_dir)

    @abstractmethod
    def _export_assets(self, output_dir=""):
        pass

    @logger.process_function("Exporting file debug data")
    def export_debug_data(self, output_dir=""):
        self._export_debug_data(output_dir=output_dir)

    @abstractmethod
    def _export_debug_data(self, output_dir=""):
        pass
