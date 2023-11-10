import json
from typing import IO

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record.data_exporting._assertions import assert_export_output_file
from logic_layer.knowledge_record.data_exporting._dictionary_export import connection_to_dictionary
from logic_layer.knowledge_record.data_exporting._dictionary_export import entity_to_dictionary
from logic_layer.knowledge_record.data_exporting._dictionary_export import record_to_dictionary


def export_entity_to_json_file(entity: KnowledgeRecordEntity, output_file: IO):
    assert_export_output_file(output_file, 'json', context='entity data json export')
    entity_data = entity_to_dictionary(entity)
    json.dump(entity_data, output_file, ensure_ascii=False)


def export_connection_to_json_file(connection: KnowledgeRecordConnection, output_file: IO):
    assert_export_output_file(output_file, 'json', context='connection data json export')
    connection_data = connection_to_dictionary(connection)
    json.dump(connection_data, output_file, ensure_ascii=False)


def export_record_to_json_file(record, output_file: IO):
    assert_export_output_file(output_file, 'json', context='record data json export')
    record_data = record_to_dictionary(record)
    json.dump(record_data, output_file, ensure_ascii=False)
