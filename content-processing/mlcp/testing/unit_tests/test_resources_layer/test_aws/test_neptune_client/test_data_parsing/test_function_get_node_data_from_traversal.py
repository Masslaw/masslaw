import unittest
from unittest.mock import MagicMock

from resources_layer.aws.neptune_client._data_parsing import get_node_data_from_traversal


class TestFunctionGetNodeDataFromTraversal(unittest.TestCase):

    def test_valid_traversal(self):
        traversal = MagicMock()
        mock_result = {'id': '123', 'label': 'NodeLabel', 'properties': {'key1': 'value1', 'key2': 'value2'}}
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.next.return_value = mock_result

        node_data = get_node_data_from_traversal(traversal)

        self.assertEqual(node_data, mock_result)

    def test_empty_traversal(self):
        traversal = MagicMock()
        traversal.project.return_value.by.return_value.by.return_value.by.return_value.next.side_effect = StopIteration

        with self.assertRaises(StopIteration):
            get_node_data_from_traversal(traversal)
