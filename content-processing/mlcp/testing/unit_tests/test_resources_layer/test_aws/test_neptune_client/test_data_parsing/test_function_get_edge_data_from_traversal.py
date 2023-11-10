import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_edge_data_from_traversal


class TestFunctionGetEdgeDataFromTraversal(unittest.TestCase):

    def setUp(self):
        self.traversal = MagicMock()

    def test_valid_edge_data_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.next.return_value = {
            'id': '123', 'label': 'EdgeLabel', 'outV': '456',
            'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}
        }

        edge_data = get_edge_data_from_traversal(self.traversal)

        self.assertEqual(edge_data['id'], '123')
        self.assertEqual(edge_data['label'], 'EdgeLabel')
        self.assertEqual(edge_data['outV'], '456')
        self.assertEqual(edge_data['inV'], '789')
        self.assertEqual(edge_data['properties'], {'key1': 'value1', 'key2': 'value2'})

    def test_empty_edge_data_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.next.return_value = {}

        edge_data = get_edge_data_from_traversal(self.traversal)

        self.assertEqual(edge_data, {})

    def test_no_edge_data_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.next.side_effect = StopIteration

        with self.assertRaises(StopIteration):
            get_edge_data_from_traversal(self.traversal)
