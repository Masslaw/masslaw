from typing import Dict

from logic_layer.knowledge_record.data_loading._exceptions import ConnectionDictionaryDataPropertyMissing
from logic_layer.knowledge_record.data_loading._exceptions import EntityDictionaryDataPropertyMissing
from logic_layer.knowledge_record.data_loading._exceptions import RecordDictionaryDataPropertyMissing


def assert_entity_dictionary_data_record(data: Dict):
    for key in ['id', 'label', 'properties']:
        if key not in data:
            raise EntityDictionaryDataPropertyMissing(key)


def assert_connection_dictionary_data_record(data: Dict):
    for key in ['id', 'label', 'from_entity_id', 'to_entity_id', 'properties']:
        if key not in data:
            raise ConnectionDictionaryDataPropertyMissing(key)


def assert_record_dictionary_data_record(data: Dict):
    for key in ['id', 'label', 'entities', 'connections']:
        if key not in data:
            raise RecordDictionaryDataPropertyMissing(key)
