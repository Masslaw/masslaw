import os

from execution_layer.actions._application_action import ApplicationAction
from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.database_sync import RecordDatabaseSyncManager
from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper import SpacyWrapper
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats
from logic_layer.remote_graph_database.neptune_manager import NeptuneDatabaseManager

class ExtractKnowledge(ApplicationAction):
    _required_params = ['files_data']

    _files_data = {}

    def _handle_arguments(self):
        self._files_data = self._get_param("files_data")

    def _execute(self):
        self.__extract_knowledge()

    def __extract_knowledge(self):
        logger.debug(f"Extracting knowledge from {common_formats.value(len(self._files_data))} files")
        for file_data in self._files_data:
            self.__process_file(file_data)

    @logger.process_function('Extracting knowledge from file')
    def __process_file(self, file_data):
        logger.debug(f"File data: {common_formats.value(file_data)}")
        file_name = file_data.get("file_name")
        languages = file_data.get("languages")
        neptune_endpoints = file_data.get("neptune_endpoints", {})
        neptune_read_endpoint_data = neptune_endpoints.get("read", {})
        neptune_write_endpoint_data = neptune_endpoints.get("write", {})
        knowledge_record_data = file_data.get("knowledge_record_data", {})

        if (not file_name) or (not languages) or (not neptune_read_endpoint_data) or (not neptune_write_endpoint_data):
            logger.warning(f"Skipping file due to missing data")
            return False

        extractor: KnowledgeExtractor = SpacyWrapper(languages)
        extractor.load_file(file_name)
        knowledge_record: KnowledgeRecord = extractor.get_record()

        graph_database_sync_manager = RecordDatabaseSyncManager(knowledge_record)

        neptune_database_manager = NeptuneDatabaseManager(
            neptune_read_connection_data=neptune_read_endpoint_data,
            neptune_write_connection_data=neptune_write_endpoint_data,
            subgraph_node_properties=knowledge_record_data.get("node_properties", {}),
            subgraph_edge_properties=knowledge_record_data.get("edge_properties", {}),
        )

        graph_database_sync_manager.sync_with_database(neptune_database_manager)

        return True

