import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_multiple_nodes_data_from_traversal


class TestFunctionGetMultipleNodesDataFromTraversal(unittest.TestCase):

    def test_valid_traversal_multiple_nodes(self):
        traversal = MagicMock()
        mock_results = [{'id': '123', 'label': 'NodeLabel1', 'properties': {'key1': 'value1', 'key2': 'value2'}},
                        {'id': '456', 'label': 'NodeLabel2', 'properties': {'key3': 'value3', 'key4': 'value4'}}]
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes_data = get_multiple_nodes_data_from_traversal(traversal)

        self.assertEqual(nodes_data, mock_results)

    def test_valid_traversal_single_node(self):
        traversal = MagicMock()
        mock_results = [{'id': '789', 'label': 'NodeLabel3', 'properties': {'key5': 'value5', 'key6': 'value6'}}]
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes_data = get_multiple_nodes_data_from_traversal(traversal)

        self.assertEqual(nodes_data, mock_results)

    def test_empty_traversal(self):
        traversal = MagicMock()
        mock_results = []
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = mock_results

        nodes_data = get_multiple_nodes_data_from_traversal(traversal)

        self.assertEqual(nodes_data, mock_results)
