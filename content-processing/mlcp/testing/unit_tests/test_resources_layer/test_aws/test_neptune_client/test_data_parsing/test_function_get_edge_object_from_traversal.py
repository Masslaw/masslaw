import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_edge_object_from_traversal


class TestFunctionGetEdgeObjectFromTraversal(unittest.TestCase):

    def setUp(self):
        self.traversal = MagicMock()

    def test_valid_edge_object_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.next.return_value = {
            'id': '123', 'label': 'EdgeLabel', 'outV': '456',
            'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}
        }

        edge_object = get_edge_object_from_traversal(self.traversal)

        self.assertEqual(str(edge_object.get_id()), '123')
        self.assertEqual(edge_object.get_label(), 'EdgeLabel')
        self.assertEqual(str(edge_object.get_from_node()), '456')
        self.assertEqual(str(edge_object.get_to_node()), '789')
        self.assertEqual(edge_object.get_properties(), {'key1': 'value1', 'key2': 'value2'})

    def test_no_edge_object_from_traversal(self):
        self.traversal.project.return_value.by.return_value.by.return_value.by.return_value.by.return_value.by.return_value.next.side_effect = StopIteration

        with self.assertRaises(StopIteration):
            get_edge_object_from_traversal(self.traversal)
