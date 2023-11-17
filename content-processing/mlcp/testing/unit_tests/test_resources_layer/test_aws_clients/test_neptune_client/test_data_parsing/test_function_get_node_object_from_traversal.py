import unittest
from unittest.mock import MagicMock

from resources_layer.aws_clients.neptune_client._data_parsing import get_node_object_from_traversal


class TestFunctionGetNodeObjectFromTraversal(unittest.TestCase):

    def test_valid_traversal(self):
        traversal = MagicMock()
        mock_result = {'id': '123', 'label': 'NodeLabel', 'properties': {'key1': 'value1', 'key2': 'value2'}}
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.next.return_value = mock_result

        node = get_node_object_from_traversal(traversal)

        self.assertEqual(node.get_id(), 123)
        self.assertEqual(node.get_label(), 'NodeLabel')
        self.assertEqual(node.get_properties(), {'key1': 'value1', 'key2': 'value2'})

    def test_empty_traversal(self):
        traversal = MagicMock()
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.next.side_effect = StopIteration

        with self.assertRaises(StopIteration):
            get_node_object_from_traversal(traversal)
