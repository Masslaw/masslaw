from typing import Dict


class GraphDatabaseNode:
    def __init__(self, node_id: str, label: str, properties: Dict):
        self._id = node_id
        self._label = label
        self._properties = properties

    def get_properties(self):
        return self._properties

    def set_properties(self, properties):
        self._properties = properties

    def get_id(self):
        return self._id

    def set_id(self, node_id):
        self._id = node_id

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label
