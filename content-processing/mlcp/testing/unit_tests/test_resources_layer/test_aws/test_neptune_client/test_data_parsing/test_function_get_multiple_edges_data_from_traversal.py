import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_multiple_edges_data_from_traversal


class TestFunctionGetMultipleEdgesDataFromTraversal(unittest.TestCase):

    def setUp(self):
        self.traversal = MagicMock()

    def test_valid_multiple_edge_data_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = [
            {'id': '123', 'label': 'EdgeLabel1', 'outV': '456', 'inV': '789', 'properties': {'key1': 'value1'}},
            {'id': '234', 'label': 'EdgeLabel2', 'outV': '890', 'inV': '901', 'properties': {'key2': 'value2'}}]

        edge_data_list = get_multiple_edges_data_from_traversal(self.traversal)

        self.assertEqual(len(edge_data_list), 2)
        self.assertEqual(edge_data_list[0]['id'], '123')
        self.assertEqual(edge_data_list[0]['label'], 'EdgeLabel1')
        self.assertEqual(edge_data_list[1]['id'], '234')
        self.assertEqual(edge_data_list[1]['label'], 'EdgeLabel2')

    def test_empty_multiple_edge_data_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.to_list.return_value = []

        edge_data_list = get_multiple_edges_data_from_traversal(self.traversal)

        self.assertEqual(len(edge_data_list), 0)
