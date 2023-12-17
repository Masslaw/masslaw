from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record._record_compnents_matching._connection_matching import find_matching_connection_in_record
from logic_layer.knowledge_record.data_merging._connection_merging_logic import merge_connections
from logic_layer.knowledge_record.data_merging._entity_merging_logic import merge_entities
from logic_layer.knowledge_record._record_compnents_matching import entity_matching


def merge_entities_between_records(merge_to: KnowledgeRecord, to_merge: KnowledgeRecord):
    for entity_to_merge in to_merge.get_entities():
        matching_entity = entity_matching.find_matching_entity_in_record(entity_to_merge, merge_to)
        if matching_entity is None:
            merge_to.add_entities([entity_to_merge])
            continue
        merge_entities(matching_entity, entity_to_merge)
        entity_to_merge_ingoing_connections = to_merge.get_entity_ingoing_connections(entity_to_merge)
        entity_to_merge_outgoing_connections = to_merge.get_entity_outgoing_connections(entity_to_merge)
        for ingoing_connection in entity_to_merge_ingoing_connections:
            ingoing_connection.set_to_entity(matching_entity)
        for outgoing_connection in entity_to_merge_outgoing_connections:
            outgoing_connection.set_from_entity(matching_entity)
    merge_to.add_connections(to_merge.get_connections())


def merge_connections_in_record(record: KnowledgeRecord, bidirectional: bool = False, ignore_properties: bool = False):
    for connection in record.get_connections():
        matching_connection = find_matching_connection_in_record(connection, record, bidirectional, ignore_properties)
        if matching_connection is None:
            continue
        merge_connections(matching_connection, connection)

