import unittest
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import sync_record_with_graph_database
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
