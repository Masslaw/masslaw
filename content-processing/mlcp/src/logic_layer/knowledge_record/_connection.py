from typing import Dict

from logic_layer.knowledge_record._entity import KnowledgeRecordEntity


class KnowledgeRecordConnection:

    def __init__(self, connection_id: str = '', label: str = '', from_entity: KnowledgeRecordEntity = None, to_entity: KnowledgeRecordEntity = None, properties: Dict = None):
        self._id = connection_id
        self._label = label
        self._from_entity = from_entity
        self._to_entity = to_entity
        self._properties = properties or {}

    def get_id(self) -> str:
        return self._id

    def set_id(self, connection_id: str):
        self._id = connection_id

    def get_label(self) -> str:
        return self._label

    def set_label(self, label: str):
        self._label = label

    def get_from_entity(self) -> KnowledgeRecordEntity:
        return self._from_entity

    def set_from_entity(self, from_entity: KnowledgeRecordEntity):
        self._from_entity = from_entity

    def get_to_entity(self) -> KnowledgeRecordEntity:
        return self._to_entity

    def set_to_entity(self, to_entity: KnowledgeRecordEntity):
        self._to_entity = to_entity

    def get_properties(self) -> Dict:
        return self._properties.copy()

    def set_properties(self, properties: Dict):
        self._properties = properties.copy()
