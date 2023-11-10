import unittest
from unittest.mock import create_autospec
from unittest.mock import patch

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _sync_entity_with_graph_database
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncEntityWithGraphDatabase(unittest.TestCase):

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_entity_if_exists")
    def test_sync_entity_with_graph_database_with_merged(self, mock_get_and_merge_matching_entity_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _entity = KnowledgeRecordEntity()

        def mock_sync_entity_with_graph_database(graph_db_manager, entity):
            entity.set_id(str('123'))
            entity.set_properties({'test': 'test'})

        mock_get_and_merge_matching_entity_if_exists.side_effect = mock_sync_entity_with_graph_database

        _sync_entity_with_graph_database(mock_graph_db_manager, _entity)

        mock_graph_db_manager.load_properties_to_node.assert_any_call(node_id=str('123'), properties={'test': 'test'})

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_entity_if_exists")
    def test_sync_entity_with_graph_database_with_new(self, mock_get_and_merge_matching_entity_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _entity = KnowledgeRecordEntity()
        _entity.set_properties({'test': 'test'})

        def mock_sync_entity_with_graph_database(graph_db_manager, entity):
            entity.set_id(None)

        mock_get_and_merge_matching_entity_if_exists.side_effect = mock_sync_entity_with_graph_database

        _sync_entity_with_graph_database(mock_graph_db_manager, _entity)

        mock_graph_db_manager.set_node.assert_any_call(label=_entity.get_label(), properties={'test': 'test'})
