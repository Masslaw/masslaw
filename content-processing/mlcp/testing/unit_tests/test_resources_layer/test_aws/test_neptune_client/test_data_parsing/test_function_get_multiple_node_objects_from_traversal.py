import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_multiple_node_objects_from_traversal


class TestFunctionGetMultipleNodeObjectsFromTraversal(unittest.TestCase):

    def test_valid_traversal_multiple_nodes(self):
        traversal = MagicMock()
        mock_results = [
            {'id': '123', 'label': 'NodeLabel1', 'properties': {'key1': 'value1', 'key2': 'value2'}},
            {'id': '456', 'label': 'NodeLabel2', 'properties': {'key3': 'value3', 'key4': 'value4'}}
        ]
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes = get_multiple_node_objects_from_traversal(traversal)

        self.assertEqual(nodes[0].get_id(), 123)
        self.assertEqual(nodes[0].get_label(), 'NodeLabel1')
        self.assertEqual(nodes[0].get_properties(), {'key1': 'value1', 'key2': 'value2'})

        self.assertEqual(nodes[1].get_id(), 456)
        self.assertEqual(nodes[1].get_label(), 'NodeLabel2')
        self.assertEqual(nodes[1].get_properties(), {'key3': 'value3', 'key4': 'value4'})

    def test_valid_traversal_single_node(self):
        traversal = MagicMock()
        mock_results = [
            {'id': '789', 'label': 'NodeLabel3', 'properties': {'key5': 'value5', 'key6': 'value6'}}
        ]
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes = get_multiple_node_objects_from_traversal(traversal)

        self.assertEqual(nodes[0].get_id(), 789)
        self.assertEqual(nodes[0].get_label(), 'NodeLabel3')
        self.assertEqual(nodes[0].get_properties(), {'key5': 'value5', 'key6': 'value6'})

    def test_empty_traversal(self):
        traversal = MagicMock()
        mock_results = []
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes = get_multiple_node_objects_from_traversal(traversal)

        self.assertEqual(len(nodes), 0)
