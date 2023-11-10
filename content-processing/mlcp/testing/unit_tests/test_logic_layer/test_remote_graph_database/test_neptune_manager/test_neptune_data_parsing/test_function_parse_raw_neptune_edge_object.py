import unittest

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database.neptune_manager._neptune_data_parsing import parse_raw_neptune_edge_object
from resources_layer.aws.neptune_client import NeptuneEdge


class TestFunctionParseRawNeptuneEdgeObject(unittest.TestCase):

    def test_parse_valid_neptune_edge_object(self):
        neptune_edge = NeptuneEdge(123, 'edgeLabel', 'fromNode', 'toNode', {'key': 'value'})
        result = parse_raw_neptune_edge_object(neptune_edge)

        self.assertIsInstance(result, GraphDatabaseEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel')
        self.assertEqual(result.get_from_node(), 'fromNode')
        self.assertEqual(result.get_to_node(), 'toNode')
        self.assertEqual(result.get_properties(), {'key': 'value'})

    def test_parse_edge_with_empty_properties(self):
        neptune_edge = NeptuneEdge(123, 'edgeLabel', 'fromNode', 'toNode', {})
        result = parse_raw_neptune_edge_object(neptune_edge)

        self.assertIsInstance(result, GraphDatabaseEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel')
        self.assertEqual(result.get_from_node(), 'fromNode')
        self.assertEqual(result.get_to_node(), 'toNode')
        self.assertEqual(result.get_properties(), {})

    def test_parse_edge_with_multiple_properties(self):
        properties = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        neptune_edge = NeptuneEdge(123, 'edgeLabel', 'fromNode', 'toNode', properties)
        result = parse_raw_neptune_edge_object(neptune_edge)

        self.assertIsInstance(result, GraphDatabaseEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel')
        self.assertEqual(result.get_from_node(), 'fromNode')
        self.assertEqual(result.get_to_node(), 'toNode')
        self.assertEqual(result.get_properties(), properties)
