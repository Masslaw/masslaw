import unittest
from unittest.mock import create_autospec
from unittest.mock import patch

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _sync_connections_with_graph_database
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncConnectionsWithGraphDatabase(unittest.TestCase):

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_connection_if_exists")
    def test_sync_connections_with_graph_database(self, mock_get_and_merge_matching_connection_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _connections = [KnowledgeRecordConnection(to_entity=KnowledgeRecordEntity(), from_entity=KnowledgeRecordEntity()) for _ in range(3)]

        connection_id = 0

        def mock_sync_connection_with_graph_database(graph_db_manager, connection):
            nonlocal connection_id
            if connection_id % 2 == 0:
                connection.set_id(str(connection_id))
            connection_id += 1

        mock_get_and_merge_matching_connection_if_exists.side_effect = mock_sync_connection_with_graph_database

        _sync_connections_with_graph_database(mock_graph_db_manager, _connections)

        for i, connection in enumerate(_connections):
            if i % 2 == 0:
                mock_graph_db_manager.load_properties_to_edge.assert_any_call(edge_id=str(i), properties=connection.get_properties())
            else:
                mock_graph_db_manager.set_edge.assert_any_call(edge_label=connection.get_label(), from_node=connection.get_from_entity().get_id(), to_node=connection.get_to_entity().get_id(),
                    properties=connection.get_properties(), )
