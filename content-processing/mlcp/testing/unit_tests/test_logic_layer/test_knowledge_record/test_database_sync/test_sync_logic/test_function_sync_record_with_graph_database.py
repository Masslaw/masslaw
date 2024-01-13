import unittest
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import sync_record_with_graph_database
from logic_layer.knowledge_record.database_sync._sync_logic import MAX_NUMBER_OF_ENTITIES_SUBMITTED
from logic_layer.knowledge_record.database_sync._sync_logic import MAX_NUMBER_OF_CONNECTIONS_SUBMITTED
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncRecordWithGraphDatabase(unittest.TestCase):

    def test_sync_record_with_graph_database(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        record = KnowledgeRecord()
        _entities = [KnowledgeRecordEntity() for _ in range(3)]
        _connections = [KnowledgeRecordConnection(to_entity=KnowledgeRecordEntity(), from_entity=KnowledgeRecordEntity()) for _ in range(3)]

        record.set_entities(_entities)
        record.set_connections(_connections)

        def entity_mergeability_check_function(e1: KnowledgeRecordEntity, e2: KnowledgeRecordEntity):
            if e1.get_label() != e2.get_label(): return False
            if e1.get_properties().get('name', '') != e2.get_properties().get('name', ''): return False
            return True

        def connection_mergeability_check_function(e1: KnowledgeRecordConnection, e2: KnowledgeRecordConnection):
            if e1.get_label() != e2.get_label(): return False
            if e1.get_properties().get('name', '') != e2.get_properties().get('name', ''): return False
            return True

        merge_configuration = RecordMergingConfiguration(entity_mergeability_check_function, connection_mergeability_check_function)
        sync_record_with_graph_database(record, mock_graph_db_manager, merge_configuration)

    def test_with_a_large_number_of_entities(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        number_of_extra_entities = 100
        number_of_extra_connections = 1000

        record = KnowledgeRecord()
        _entities = [KnowledgeRecordEntity() for _ in range(MAX_NUMBER_OF_ENTITIES_SUBMITTED + number_of_extra_entities)]
        _connections = [KnowledgeRecordConnection(to_entity=KnowledgeRecordEntity(), from_entity=KnowledgeRecordEntity()) for _ in range(MAX_NUMBER_OF_CONNECTIONS_SUBMITTED + number_of_extra_connections)]

        record.set_entities(_entities)
        record.set_connections(_connections)

        merge_configuration = RecordMergingConfiguration()
        sync_record_with_graph_database(record, mock_graph_db_manager, merge_configuration)

        entity_deletion_call_args = mock_graph_db_manager.delete_nodes_if_exist.call_args_list[0]
        entity_ids_called_to_delete = entity_deletion_call_args[0][0]
        self.assertEqual(len(entity_ids_called_to_delete), number_of_extra_entities)

        connection_deletion_call_args = mock_graph_db_manager.delete_edges_if_exist.call_args_list[0]
        connection_ids_called_to_delete = connection_deletion_call_args[0][0]
        self.assertEqual(len(connection_ids_called_to_delete), number_of_extra_connections)
