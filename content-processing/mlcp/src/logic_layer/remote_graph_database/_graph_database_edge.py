from typing import Dict


class GraphDatabaseEdge:
    def __init__(self, edge_label: str, from_node: str, to_node: str, properties: Dict, edge_id: str = None):
        self._id = edge_id
        self._label = edge_label
        self._from_node = from_node
        self._to_node = to_node
        self._properties = properties

    def get_from_node(self):
        return self._from_node

    def set_from_node(self, value):
        self._from_node = value

    def get_to_node(self):
        return self._to_node

    def set_to_node(self, value):
        self._to_node = value

    def get_properties(self):
        return self._properties

    def set_properties(self, value):
        self._properties = value

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_label(self):
        return self._label

    def set_label(self, value):
        self._label = value
