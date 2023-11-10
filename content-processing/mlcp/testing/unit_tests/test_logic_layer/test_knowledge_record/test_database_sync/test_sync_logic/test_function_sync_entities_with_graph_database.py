import unittest
from unittest.mock import create_autospec
from unittest.mock import patch

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.database_sync._sync_logic import _sync_entities_with_graph_database
from logic_layer.remote_graph_database import GraphDatabaseManager


class TestSyncEntitiesWithGraphDatabase(unittest.TestCase):

    @patch("logic_layer.knowledge_record.database_sync._sync_logic._get_and_merge_matching_entity_if_exists")
    def test_sync_entities_with_graph_database(self, mock_get_and_merge_matching_entity_if_exists):
        mock_graph_db_manager = create_autospec(GraphDatabaseManager)

        _entities = [KnowledgeRecordEntity() for _ in range(3)]

        entity_id = 0

        def mock_sync_entity_with_graph_database(graph_db_manager, entity):
            nonlocal entity_id
            if entity_id % 2 == 0:
                entity.set_id(str(entity_id))
            entity_id += 1

        mock_get_and_merge_matching_entity_if_exists.side_effect = mock_sync_entity_with_graph_database

        _sync_entities_with_graph_database(mock_graph_db_manager, _entities)

        for i, entity in enumerate(_entities):
            if i % 2 == 0:
                mock_graph_db_manager.load_properties_to_node.assert_any_call(node_id=str(i), properties=entity.get_properties())
            else:
                mock_graph_db_manager.set_node.assert_any_call(label=entity.get_label(), properties=entity.get_properties())
