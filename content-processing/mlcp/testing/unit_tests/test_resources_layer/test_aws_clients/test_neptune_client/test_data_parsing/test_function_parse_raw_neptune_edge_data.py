import unittest

from resources_layer.aws_clients.neptune_client._data_parsing import parse_raw_neptune_edge_data


class TestFunctionParseRawNeptuneEdgeData(unittest.TestCase):

    def test_valid_edge_data(self):
        raw_data = {'id': '123', 'label': 'EdgeLabel', 'outV': '456', 'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}}

        edge = parse_raw_neptune_edge_data(raw_data)

        self.assertEqual(edge.get_id(), 123)
        self.assertEqual(edge.get_label(), 'EdgeLabel')
        self.assertEqual(edge.get_from_node(), 456)
        self.assertEqual(edge.get_to_node(), 789)
        self.assertEqual(edge.get_properties(), {'key1': 'value1', 'key2': 'value2'})

    def test_missing_edge_id(self):
        raw_data = {'label': 'EdgeLabel', 'outV': '456', 'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}}

        with self.assertRaises(KeyError):
            parse_raw_neptune_edge_data(raw_data)

    def test_missing_edge_label(self):
        raw_data = {'id': '123', 'outV': '456', 'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}}

        with self.assertRaises(KeyError):
            parse_raw_neptune_edge_data(raw_data)

    def test_missing_from_node(self):
        raw_data = {'id': '123', 'label': 'EdgeLabel', 'inV': '789', 'properties': {'key1': 'value1', 'key2': 'value2'}}

        with self.assertRaises(KeyError):
            parse_raw_neptune_edge_data(raw_data)

    def test_missing_to_node(self):
        raw_data = {'id': '123', 'label': 'EdgeLabel', 'outV': '456', 'properties': {'key1': 'value1', 'key2': 'value2'}}

        with self.assertRaises(KeyError):
            parse_raw_neptune_edge_data(raw_data)

    def test_missing_properties(self):
        raw_data = {'id': '123', 'label': 'EdgeLabel', 'outV': '456', 'inV': '789'}

        edge = parse_raw_neptune_edge_data(raw_data)
        self.assertEqual(edge.get_properties(), {})
