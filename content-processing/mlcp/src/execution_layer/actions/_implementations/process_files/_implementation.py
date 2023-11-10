import os

from execution_layer.actions._application_action import ApplicationAction
from logic_layer.file_processing import create_processor
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class ProcessFiles(ApplicationAction):
    _required_params = ['files_data']

    _files_data = {}

    def _handle_arguments(self):
        self._files_data = self._get_param("files_data")

    def _execute(self):
        self.__process_files()

    def __process_files(self):
        logger.debug(f"Processing {common_formats.value(len(self._files_data))} files")
        for file_data in self._files_data:
            self.__process_file(file_data)

    @logger.process_function('Processing file')
    def __process_file(self, file_data):
        logger.debug(f"File data: {common_formats.value(file_data)}")
        file_name = file_data.get("file_name")
        languages = file_data.get("languages")

        if (not file_name) or (not languages):
            logger.warning(f"Skipping file due to missing data")
            return False
        
        logger.info(f"Creating file processor")
        file_processor = create_processor(file_name, languages)
        logger.positive(f"Created file processor | type: {common_formats.value(file_processor.__class__.__name__)}")

        logger.info(f"Performing file processing...")
        file_processor.process()

        logger.info(f"Exporting processed data")
        file_processor.export_metadata(file_data.get("file_metadata_output_dir", "file_metadata"))
        file_processor.export_text(file_data.get("extracted_text_output_dir", "extracted_text"))
        file_processor.export_assets(file_data.get("assets_output_dir", "actioned_assets"))

        if os.environ.get('__mlcp_stage__', '') in ('debug', 'test'):
            logger.info(f"Exporting debug data")
            file_processor.export_debug_data(file_data.get("debug_data_dir", "debug_data"))

        return True
