from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.record_merging._connection_merging_logic import merge_connections
from logic_layer.knowledge_record.record_merging._entity_merging_logic import merge_entities
from shared_layer.list_utils import list_utils
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


@logger.process_function("Knowledge Record Merging - Merging records")
def merge_records(merge_to: KnowledgeRecord, to_merge: KnowledgeRecord, entity_mergeability_check_function: callable = lambda entity1, entity2: False, connection_mergeability_check_function: callable = lambda connection1, connection2: False):
    logger.debug(f"Before merging:")
    logger.debug(f"record1 has {common_formats.value(len(merge_to.get_entities()))} entities and {common_formats.value(len(merge_to.get_connections()))} connections")
    logger.debug(f"record2 has {common_formats.value(len(to_merge.get_entities()))} entities and {common_formats.value(len(to_merge.get_connections()))} connections")
    logger.debug(f"together they have {common_formats.value(len(merge_to.get_entities()) + len(to_merge.get_entities()))} entities and {common_formats.value(len(merge_to.get_connections()) + len(to_merge.get_connections()))} connections in total")
    merge_to.add_entities(to_merge.get_entities())
    merge_to.add_connections(to_merge.get_connections())
    merge_entities_in_record(merge_to, entity_mergeability_check_function)
    merge_connections_in_record(merge_to, connection_mergeability_check_function)
    logger.debug(f"After merging:")
    logger.debug(f"the record has {common_formats.value(len(merge_to.get_entities()))} entities and {common_formats.value(len(merge_to.get_connections()))} connections")


@logger.process_function("Knowledge Record Merging - Merging entities in record")
def merge_entities_in_record(record: KnowledgeRecord, mergeability_check_function: callable = lambda e1, e2: False):
    record_entities = record.get_entities()
    logger.debug(f"Before merging: {common_formats.value(len(record_entities))} entities")
    list_utils.merge_mergeable(record_entities, mergeability_check_function, lambda e1, e2: do_merge_entities_in_record(record, e1, e2))
    logger.debug(f"After merging: {common_formats.value(len(record_entities))} entities")
    record.set_entities(record_entities)


def do_merge_entities_in_record(record: KnowledgeRecord, entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    merge_entities(entity1, entity2)
    entity2_ingoing_connections = record.get_entity_ingoing_connections(entity2)
    entity2_outgoing_connections = record.get_entity_outgoing_connections(entity2)
    for ingoing_connection in entity2_ingoing_connections:
        ingoing_connection.set_to_entity(entity1)
    for outgoing_connection in entity2_outgoing_connections:
        outgoing_connection.set_from_entity(entity1)
    return entity1


@logger.process_function("Knowledge Record Merging - Merging connections in record")
def merge_connections_in_record(record: KnowledgeRecord, connection_mergeability_check_function: callable = lambda c1, c2: False):
    record_connections = record.get_connections()
    logger.debug(f"Before merging: {common_formats.value(len(record_connections))} connections")
    list_utils.merge_mergeable(record_connections, connection_mergeability_check_function, lambda c1, c2: do_merge_connections_in_record(record, c1, c2))
    logger.debug(f"After merging: {common_formats.value(len(record_connections))} connections")
    record.set_connections(record_connections)


def do_merge_connections_in_record(record: KnowledgeRecord, connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    merge_connections(connection1, connection2)
    return connection1
