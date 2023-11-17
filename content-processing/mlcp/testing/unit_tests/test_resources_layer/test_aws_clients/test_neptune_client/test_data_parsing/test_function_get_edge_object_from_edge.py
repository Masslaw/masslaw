import unittest
from unittest.mock import MagicMock

from gremlin_python.structure.graph import Edge
from gremlin_python.structure.graph import Vertex

from resources_layer.aws_clients.neptune_client._data_parsing import get_edge_object_from_edge


class TestFunctionGetEdgeObjectFromEdge(unittest.TestCase):

    def test_valid_edge(self):
        edge = Edge(id=123, label="TestEdge", outV=Vertex(id=456, label="FromVertex"), inV=Vertex(id=789, label="ToVertex"))
        propertyA = MagicMock()
        propertyA.key = "keyA"
        propertyA.value = "valueA"
        propertyB = MagicMock()
        propertyB.key = "keyB"
        propertyB.value = "valueB"
        edge.properties = [propertyA, propertyB]

        neptune_edge = get_edge_object_from_edge(edge)

        self.assertEqual(neptune_edge.get_id(), 123)
        self.assertEqual(neptune_edge.get_label(), 'TestEdge')
        self.assertEqual(neptune_edge.get_from_node(), 456)
        self.assertEqual(neptune_edge.get_to_node(), 789)
        self.assertEqual(neptune_edge.get_properties(), {'keyA': 'valueA', 'keyB': 'valueB'})
