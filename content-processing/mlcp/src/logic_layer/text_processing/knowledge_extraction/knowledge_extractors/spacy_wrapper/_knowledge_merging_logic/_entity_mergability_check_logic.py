import itertools
import re

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._knowledge_merging_logic._merging_logic_config import REMOVABLE_EXPRESSIONS_BY_ENTITY_TYPE


def check_spacy_entities_mergeable(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    if _check_entity_ids(entity1, entity2): return True
    if _determine_date_time_typed_entities_mergeable(entity1, entity2): return True
    if _determine_entities_mergeable_by_title(entity1, entity2): return True
    return False


def _check_entity_ids(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity):
    return entity1.get_id() and entity2.get_id() and entity1.get_id() == entity2.get_id()


def _determine_date_time_typed_entities_mergeable(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity) -> bool:
    if not (entity1.get_label() in ("DATE", "TIME",) and entity2.get_label() in ("DATE", "TIME",)): return False
    entity1_datetime = entity1.get_properties().get("datetime", {})
    entity2_datetime = entity2.get_properties().get("datetime", {})
    if not entity1_datetime or not entity2_datetime: return False
    for key, value in entity1_datetime.items():
        if value != entity2_datetime.get(key, value): return False
    for key, value in entity2_datetime.items():
        if value != entity1_datetime.get(key, value): return False
    return True


def _determine_entities_mergeable_by_title(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity) -> bool:
    if entity1.get_label() != entity2.get_label(): return False
    if entity1.get_label() in ("DATE", "TIME", ): return False
    entity1_title = str(entity1.get_properties().get("title", '')).lower()
    entity2_title = str(entity2.get_properties().get("title", '')).lower()
    entity1_title = re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z]', ' ', entity1_title))
    entity2_title = re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z]', ' ', entity2_title))
    entity1_parts = set(entity1_title.split(' '))
    entity2_parts = set(entity2_title.split(' '))
    removable_expressions = REMOVABLE_EXPRESSIONS_BY_ENTITY_TYPE.get(entity1.get_label()) or REMOVABLE_EXPRESSIONS_BY_ENTITY_TYPE.get("-OTHER-")
    entity1_parts -= removable_expressions
    entity2_parts -= removable_expressions
    entity1_parts = {part for part in entity1_parts if len(part) > 1}
    entity2_parts = {part for part in entity2_parts if len(part) > 1}
    entity_parts_overlap = entity1_parts & entity2_parts
    if len(entity_parts_overlap) > (len(entity1_parts) + len(entity2_parts)) / 4: return True  # - more than half of the average of the lengths
    return False
