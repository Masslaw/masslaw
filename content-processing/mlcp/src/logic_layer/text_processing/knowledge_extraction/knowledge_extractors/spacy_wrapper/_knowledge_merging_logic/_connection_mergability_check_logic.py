from logic_layer.knowledge_record import KnowledgeRecordConnection


def check_spacy_connections_mergeable(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    if _check_connection_ids(connection1, connection2): return True
    if not _check_connection_labels(connection1, connection2): return False
    if _determine_same_direction_connections_mergeable(connection1, connection2): return True
    if _determine_opposite_direction_connections_mergeable(connection1, connection2): return True
    return False


def _check_connection_ids(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    return connection1.get_id() == connection2.get_id()


def _check_connection_labels(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    return connection1.get_label() == connection2.get_label()


def _determine_same_direction_connections_mergeable(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    return connection1.get_from_entity() == connection2.get_from_entity() and connection1.get_to_entity() == connection2.get_to_entity()


def _determine_opposite_direction_connections_mergeable(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection):
    return connection1.get_from_entity() == connection2.get_to_entity() and connection1.get_to_entity() == connection2.get_from_entity()
