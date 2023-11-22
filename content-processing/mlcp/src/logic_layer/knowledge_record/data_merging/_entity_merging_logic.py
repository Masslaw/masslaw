from typing import Dict

from logic_layer.knowledge_record import KnowledgeRecordEntity

entity_property_specific_merging_functions = {'value': lambda name1, name2: max(name1, name2, key=len), }

entity_property_type_specific_merging_functions = {list: lambda list1, list2: list1 + list2, }


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
        if isinstance(entity1_value, dict):
            merge_function = merge_entity_properties
        else:
            merge_function = (entity_property_specific_merging_functions.get(property_name) or entity_property_type_specific_merging_functions.get(type(entity1_value)))
        merged_value = merge_function and merge_function(entity1_value, entity2_value) or entity2_value
        merged_properties[property_name] = merged_value
    return merged_properties
