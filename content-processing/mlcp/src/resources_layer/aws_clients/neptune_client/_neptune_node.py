from typing import Dict

from gremlin_python.statics import long


class NeptuneNode:
    def __init__(self, label: str, properties: Dict, node_id: long | str = None):
        self._id = node_id
        self._label = label
        self._properties = properties

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_label(self):
        return self._label

    def set_label(self, value):
        self._label = value

    def get_properties(self):
        return self._properties

    def set_properties(self, value):
        self._properties = value
