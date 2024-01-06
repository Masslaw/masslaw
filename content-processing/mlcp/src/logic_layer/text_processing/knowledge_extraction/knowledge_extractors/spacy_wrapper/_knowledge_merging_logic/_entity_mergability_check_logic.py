from logic_layer.knowledge_record import KnowledgeRecordEntity


def check_spacy_entities_mergeable(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    if _check_entity_ids(entity1, entity2): return True
    if not _check_entity_labels(entity1, entity2): return False
    if _determine_person_typed_entities_mergeable(entity1, entity2): return True
    if _determine_date_time_typed_entities_mergeable(entity1, entity2): return True
    return False


def _check_entity_ids(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    return entity1.get_id() and entity2.get_id() and entity1.get_id() == entity2.get_id()


def _check_entity_labels(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    return entity1.get_label() == entity2.get_label()


def _determine_person_typed_entities_mergeable(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    if not (entity1.get_label() == "PERSON" and entity2.get_label() == "PERSON"): return False
    entity1_title = entity1.get_properties().get("title", '')
    entity2_title = entity2.get_properties().get("title", '')
    if len(set(entity1_title.split(' ')) & set(entity2_title.split(' '))) > 0: return True
    return False


def _determine_date_time_typed_entities_mergeable(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    if not (entity1.get_label() in ("DATE", "TIME",) and entity2.get_label() in ("DATE", "TIME",)): return False
    entity1_iso = entity1.get_properties().get("iso", '')
    entity2_iso = entity2.get_properties().get("iso", '')
    return entity1_iso == entity2_iso
