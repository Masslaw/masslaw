import unittest
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record_compnents_matching._connection_matching import fetch_matching_connections_in_database
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.remote_graph_database import GraphDatabaseEdge


class TestFunctionFetchMatchingConnectionsInDatabase(unittest.TestCase):

    def test_fetch_matching_connections_in_database(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)
        mock_graph_db_manager.get_edges_by_properties.return_value = [GraphDatabaseEdge(edge_id='123', edge_label='test', properties={'test': 'test'}, from_node='123', to_node='123')]

        connections = fetch_matching_connections_in_database(graph_database_manager=mock_graph_db_manager,
            connection=KnowledgeRecordConnection(from_entity=KnowledgeRecordEntity(), to_entity=KnowledgeRecordEntity()), )

        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0].get_id(), '123')
        self.assertEqual(connections[0].get_label(), 'test')
        self.assertEqual(connections[0].get_properties(), {'test': 'test'})
