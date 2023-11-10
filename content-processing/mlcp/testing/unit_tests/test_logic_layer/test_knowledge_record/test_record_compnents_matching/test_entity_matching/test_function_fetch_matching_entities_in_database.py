import unittest
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record_compnents_matching._entity_matching import fetch_matching_entities_in_database
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.remote_graph_database import GraphDatabaseNode


class TestFunctionFetchMatchingEntitiesInDatabase(unittest.TestCase):

    def test_fetch_matching_entities_in_database(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)
        mock_graph_db_manager.get_nodes_by_properties.return_value = [GraphDatabaseNode(node_id='123', label='test', properties={'test': 'test'})]

        entities = fetch_matching_entities_in_database(graph_database_manager=mock_graph_db_manager, entity=KnowledgeRecordEntity())

        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].get_id(), '123')
        self.assertEqual(entities[0].get_label(), 'test')
        self.assertEqual(entities[0].get_properties(), {'test': 'test'})
