from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._data_merging._connection_merging_logic import merge_connections
from logic_layer.knowledge_record._data_merging._entity_merging_logic import merge_entities
from logic_layer.knowledge_record._data_merging._record_merging_logic import merge_records
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity


class EntityMerger:

    def __init__(self, target_entity: KnowledgeRecordEntity):
        self._target_entity = target_entity

    def merge_data_from_another_entity(self, another_entity: KnowledgeRecordEntity):
        merge_entities(merge_to=self._target_entity, to_merge=another_entity)


class ConnectionMerger:

    def __init__(self, target_connection: KnowledgeRecordConnection):
        self._target_connection = target_connection

    def merge_data_from_another_connection(self, another_connection: KnowledgeRecordConnection):
        merge_connections(merge_to=self._target_connection, to_merge=another_connection)


class RecordMerger:

    def __init__(self, target_record: KnowledgeRecord):
        self._target_record = target_record

    def merge_data_from_another_record(self, another_record: KnowledgeRecord):
        merge_records(merget_to=self._target_record, to_merge=another_record)
