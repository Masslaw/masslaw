from typing import List
from typing import Dict


class KnowledgeRecordEntity:

    def __init__(self, entity_id: str = '', label: str = '', properties: Dict = None, unique_properties: List[str] = None):
        self._id = entity_id
        self._label = label
        self._properties = properties or {}
        self._unique_properties = unique_properties or []

    def get_id(self) -> str:
        return self._id

    def set_id(self, id: str):
        self._id = id

    def get_label(self) -> str:
        return self._label

    def set_label(self, label: str):
        self._label = label

    def get_properties(self) -> Dict:
        return self._properties.copy()

    def set_properties(self, properties: Dict):
        self._properties = properties.copy()

    def set_property_as_unique(self, property_key: str):
        self._unique_properties.append(property_key)

    def get_unique_properties(self) -> Dict:
        return {key: self._properties[key] for key in self._unique_properties}
