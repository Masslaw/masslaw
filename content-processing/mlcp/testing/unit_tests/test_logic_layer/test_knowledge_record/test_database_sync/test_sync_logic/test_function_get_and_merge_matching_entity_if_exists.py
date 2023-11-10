import unittest
from unittest.mock import Mock
from unittest.mock import create_autospec

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _get_and_merge_matching_entity_if_exists
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.remote_graph_database import GraphDatabaseNode


class TestFunctionGetAndMergeMatchingEntityIfExists(unittest.TestCase):

    def test_with_found_entity(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        returned_node = create_autospec(GraphDatabaseNode)
        returned_node.get_id.return_value = '123'
        returned_node.get_properties.return_value = {'test': 'test'}
        returned_node.get_label.return_value = 'label'

        mock_graph_db_manager.get_nodes_by_properties.return_value = [returned_node]

        entity = KnowledgeRecordEntity()

        _get_and_merge_matching_entity_if_exists(mock_graph_db_manager, entity)

        self.assertEqual(entity.get_id(), '123')
        self.assertEqual(entity.get_properties(), {'test': 'test'})
        self.assertEqual(entity.get_label(), 'label')

    def test_with_non_found(self):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        mock_graph_db_manager.get_nodes_by_properties.return_value = []

        entity = KnowledgeRecordEntity()
        entity.set_properties({'test': 'test'})

        _get_and_merge_matching_entity_if_exists(mock_graph_db_manager, entity)

        self.assertEqual(entity.get_id(), '')
        self.assertEqual(entity.get_properties(), {'test': 'test'})
        self.assertEqual(entity.get_label(), '')
