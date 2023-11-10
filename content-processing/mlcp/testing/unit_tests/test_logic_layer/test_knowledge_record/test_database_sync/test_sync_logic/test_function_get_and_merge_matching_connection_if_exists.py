import unittest
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _get_and_merge_matching_connection_if_exists
from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.remote_graph_database import GraphDatabaseNode


class TestFunctionGetAndMergeMatchingConnectionIfExists(unittest.TestCase):

    def test_with_found_connection(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        returned_edge = create_autospec(GraphDatabaseEdge)
        returned_edge.get_id.return_value = '123'
        returned_edge.get_properties.return_value = {'test': 'test'}
        returned_edge.get_label.return_value = 'label'
        returned_edge.get_from_node.return_value = GraphDatabaseNode(node_id='abc', label='label', properties={})
        returned_edge.get_to_node.return_value = GraphDatabaseNode(node_id='100', label='label', properties={})

        mock_graph_db_manager.get_edges_by_properties.return_value = [returned_edge]

        connection = KnowledgeRecordConnection(from_entity=KnowledgeRecordEntity(), to_entity=KnowledgeRecordEntity())

        _get_and_merge_matching_connection_if_exists(mock_graph_db_manager, connection)

        self.assertEqual(connection.get_id(), '123')
        self.assertEqual(connection.get_properties(), {'test': 'test'})
        self.assertEqual(connection.get_label(), 'label')

    def test_with_non_found(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        mock_graph_db_manager.get_edges_by_properties.return_value = []

        connection = KnowledgeRecordConnection(from_entity=KnowledgeRecordEntity(), to_entity=KnowledgeRecordEntity(), properties={'test': 'test'})

        _get_and_merge_matching_connection_if_exists(mock_graph_db_manager, connection)

        self.assertEqual(connection.get_id(), '')
        self.assertEqual(connection.get_properties(), {'test': 'test'})
        self.assertEqual(connection.get_label(), '')
