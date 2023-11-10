from typing import Dict
from typing import List

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity


class KnowledgeRecord:

    def __init__(self):
        self._entities: List[KnowledgeRecordEntity] = []
        self._connections: List[KnowledgeRecordConnection] = []

        self._outgoing_connections_by_entities = {}
        self._ingoing_connections_by_entities = {}

    def get_entities(self) -> List[KnowledgeRecordEntity]:
        return self._entities.copy()

    def set_entities(self, entities: List[KnowledgeRecordEntity]):
        self._entities = entities.copy()

    def add_entities(self, entities: KnowledgeRecordEntity|List[KnowledgeRecordEntity]):
        if not isinstance(entities, list): entities = [entities]
        self._entities.extend(entities)

    def get_connections(self) -> List[KnowledgeRecordConnection]:
        return self._connections.copy()

    def set_connections(self, connections: List[KnowledgeRecordConnection]):
        self._connections = connections.copy()
        self._outgoing_connections_by_entities = {}
        self._ingoing_connections_by_entities = {}
        for c in connections: self._map_connection_to_its_entities(c)

    def add_connections(self, connections: KnowledgeRecordConnection|List[KnowledgeRecordConnection]):
        if not isinstance(connections, list): connections = [connections]
        self._connections.extend(connections)
        for c in connections: self._map_connection_to_its_entities(c)

    def get_entity_outgoing_connections(self, entity: KnowledgeRecordEntity) -> List[KnowledgeRecordConnection]:
        return self._outgoing_connections_by_entities.get(entity.__hash__(), [])

    def get_entity_ingoing_connections(self, entity: KnowledgeRecordEntity) -> List[KnowledgeRecordConnection]:
        return self._ingoing_connections_by_entities.get(entity.__hash__(), [])

    def _map_connection_to_its_entities(self, connection: KnowledgeRecordConnection):
        from_entity = connection.get_from_entity()
        to_entity = connection.get_to_entity()
        self._outgoing_connections_by_entities[from_entity.__hash__()] = self.get_entity_outgoing_connections(from_entity) + [connection]
        self._ingoing_connections_by_entities[to_entity.__hash__()] = self.get_entity_ingoing_connections(to_entity) + [connection]
