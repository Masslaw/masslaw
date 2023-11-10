import unittest
from unittest.mock import create_autospec
from unittest.mock import patch

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _sync_connection_with_graph_database
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncConnectionWithGraphDatabase(unittest.TestCase):

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_connection_if_exists")
    def test_sync_connection_with_graph_database_with_merged(self, mock_get_and_merge_matching_connection_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _connection = KnowledgeRecordConnection()

        def mock_sync_connection_with_graph_database(graph_db_manager, connection):
            connection.set_id(str('123'))
            connection.set_properties({'test': 'test'})

        mock_get_and_merge_matching_connection_if_exists.side_effect = mock_sync_connection_with_graph_database

        _sync_connection_with_graph_database(mock_graph_db_manager, _connection)

        mock_graph_db_manager.load_properties_to_edge.assert_any_call(edge_id=str('123'), properties={'test': 'test'})

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_connection_if_exists")
    def test_sync_connection_with_graph_database_with_new(self, mock_get_and_merge_matching_connection_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _connection = KnowledgeRecordConnection(from_entity=KnowledgeRecordEntity(), to_entity=KnowledgeRecordEntity())
        _connection.set_properties({'test': 'test'})

        def mock_sync_connection_with_graph_database(graph_db_manager, connection):
            connection.set_id(None)

        mock_get_and_merge_matching_connection_if_exists.side_effect = mock_sync_connection_with_graph_database

        _sync_connection_with_graph_database(mock_graph_db_manager, _connection)

        mock_graph_db_manager.set_edge.assert_any_call(edge_label=_connection.get_label(), from_node='', to_node='', properties={'test': 'test'})
