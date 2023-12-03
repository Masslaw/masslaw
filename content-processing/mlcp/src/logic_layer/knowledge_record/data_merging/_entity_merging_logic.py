from typing import Dict

from logic_layer.knowledge_record import KnowledgeRecordEntity
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger
from shared_layer.list_utils import list_utils


def _title_merging_function(value1: str, value2: str) -> str:
    return max(value1, value2, key=len)


def _list_merging_function(list1: list, list2: list) -> list:
    lst = list1 + list2
    list_utils.remove_duplicates(lst)
    return lst


entity_property_specific_merging_functions = {
    'title': _title_merging_function,
}

entity_property_type_specific_merging_functions = {
    list: _list_merging_function,
}


def merge_entities(merge_to: KnowledgeRecordEntity, to_merge: KnowledgeRecordEntity):
    merged_properties = merge_entity_properties(merge_to.get_properties(), to_merge.get_properties())
    merge_to.set_id(to_merge.get_id())
    merge_to.set_label(to_merge.get_label())
    merge_to.set_properties(merged_properties)


def merge_entity_properties(entity1_properties: Dict, entity2_properties: Dict) -> Dict:
    merged_properties = {}
    total_keys = list(set(list(entity1_properties.keys()) + list(entity2_properties.keys())))
    for property_name in total_keys:
        entity1_value = entity1_properties.get(property_name)
        entity2_value = entity2_properties.get(property_name)
        if entity1_value is None:
            merged_properties[property_name] = entity2_value
            continue
        if entity2_value is None:
            merged_properties[property_name] = entity1_value
            continue
        entity1_type = type(entity1_value)
        entity2_type = type(entity2_value)
        if entity1_type != entity2_type:
            logger.warn(f"Entity property {common_formats.value(property_name)} has different types in the two entities: {common_formats.value(entity1_type)} and {common_formats.value(entity2_type)} respectively. The value from the second entity will be used.")
            merged_properties[property_name] = entity2_value
            continue
        value_type = entity1_type
        if value_type == dict:
            merge_function = merge_entity_properties
        else:
            merge_function = (entity_property_specific_merging_functions.get(property_name) or entity_property_type_specific_merging_functions.get(value_type))
        merged_value = merge_function and merge_function(entity1_value, entity2_value) or entity2_value
        merged_properties[property_name] = merged_value
    return merged_properties
