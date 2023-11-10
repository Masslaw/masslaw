import unittest
from unittest.mock import Mock, create_autospec
from unittest.mock import patch

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import sync_record_with_graph_database
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncRecordWithGraphDatabase(unittest.TestCase):

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_entity_if_exists")
    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_connection_if_exists")
    def test_sync_record_with_graph_database(self, mock_get_and_merge_matching_connection_if_exists, mock_get_and_merge_matching_entity_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        record = KnowledgeRecord()
        _entities = [KnowledgeRecordEntity() for _ in range(3)]
        _connections = [KnowledgeRecordConnection(to_entity=KnowledgeRecordEntity(), from_entity=KnowledgeRecordEntity()) for _ in range(3)]

        record.set_entities(_entities)
        record.set_connections(_connections)

        entity_id = 0
        def mock_sync_entity_with_graph_database(graph_db_manager, entity):
            nonlocal entity_id
            if entity_id % 2 == 0:
                entity.set_id(str(entity_id))
            entity_id += 1
        mock_get_and_merge_matching_entity_if_exists.side_effect = mock_sync_entity_with_graph_database

        connection_id = 0
        def mock_sync_connection_with_graph_database(graph_db_manager, connection):
            nonlocal connection_id
            if connection_id % 2 == 0:
                connection.set_id(str(connection_id))
            connection_id += 1
        mock_get_and_merge_matching_connection_if_exists.side_effect = mock_sync_connection_with_graph_database

        sync_record_with_graph_database(mock_graph_db_manager, record)

        for i, entity in enumerate(_entities):
            if i % 2 == 0:
                mock_graph_db_manager.load_properties_to_node.assert_any_call(node_id=str(i), properties=entity.get_properties())
            else:
                mock_graph_db_manager.set_node.assert_any_call(label=entity.get_label(), properties=entity.get_properties())

        for i, connection in enumerate(_connections):
            if i % 2 == 0:
                mock_graph_db_manager.load_properties_to_edge.assert_any_call(edge_id=str(i), properties=connection.get_properties())
            else:
                mock_graph_db_manager.set_edge.assert_any_call(edge_label=connection.get_label(), from_node=connection.get_from_entity().get_id(),
                    to_node=connection.get_to_entity().get_id(), properties=connection.get_properties(), )
