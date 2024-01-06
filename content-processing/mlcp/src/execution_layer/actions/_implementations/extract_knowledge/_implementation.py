from execution_layer.actions._application_action import ApplicationAction
from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.database_sync import RecordDatabaseSyncManager
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.remote_graph_database.neptune_manager import NeptuneDatabaseManager
from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper import SpacyWrapper
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


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
            logger.warn(f"Skipping file due to missing data")
            return False

        merging_configuration = RecordMergingConfiguration()
        extractor: KnowledgeExtractor = SpacyWrapper(languages)
        extractor.load_file(file_name)
        knowledge_record: KnowledgeRecord = extractor.get_record()

        logger.debug(f"{common_formats.value(str(len(knowledge_record.get_entities())))} entities have been extracted.")
        logger.debug(f"{common_formats.value(str(len(knowledge_record.get_entities())))} connections have been extracted.")

        knowledge_record.batch_update_entity_properties(knowledge_record_data.get("node_properties", {}))
        knowledge_record.batch_update_connection_properties(knowledge_record_data.get("edge_properties", {}))

        file_id = knowledge_record_data.get("file_id")
        if file_id: self.prefrom_custom_knowledge_items_properties_manipulation_for_file(knowledge_record, file_id)

        logger.info(f"Proceeding to sync extracted knowledge with neptune database")
        graph_database_sync_manager = RecordDatabaseSyncManager(knowledge_record, merging_configuration)

        neptune_database_manager = NeptuneDatabaseManager(
            neptune_read_connection_data=neptune_read_endpoint_data,
            neptune_write_connection_data=neptune_write_endpoint_data,
            subgraph_node_properties=knowledge_record_data.get("subgraph_node_properties", {}),
            subgraph_edge_properties=knowledge_record_data.get("subgraph_edge_properties", {}),
        )

        graph_database_sync_manager.sync_with_database(neptune_database_manager)

        return True

    @logger.process_function('Performing custom knowledge items properties manipulation for file')
    def prefrom_custom_knowledge_items_properties_manipulation_for_file(self, knowledge_record: KnowledgeRecord, file_id: str):
        for entity in knowledge_record.get_entities():
            entity_properties = entity.get_properties()
            information_items = entity_properties.get("information_items", [])
            entity_properties['information_items'] = {
                file_id: information_items
            }
            entity.set_properties(entity_properties)
        for connection in knowledge_record.get_connections():
            connection_properties = connection.get_properties()
            evidence = connection_properties.get("evidence", [])
            connection_properties['evidence'] = {
                file_id: evidence
            }
            connection.set_properties(connection_properties)
