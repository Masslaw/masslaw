from typing import Dict

from logic_layer.knowledge_record import KnowledgeRecordConnection

connection_property_specific_merging_functions = {'value': lambda v1, v2: max(v1, v2, key=len), 'strength': lambda v1, v2: v1 + v2, }

connection_property_type_specific_merging_functions = {list: lambda list1, list2: list1 + list2, }


def merge_connections(merge_to: KnowledgeRecordConnection, to_merge: KnowledgeRecordConnection):
    merged_properties = merge_connection_properties(merge_to.get_properties(), to_merge.get_properties())
    merge_to.set_id(to_merge.get_id())
    merge_to.set_label(to_merge.get_label())
    merge_to.set_properties(merged_properties)


def merge_connection_properties(connection1_properties: Dict, connection2_properties: Dict) -> Dict:
    merged_properties = {}
    total_keys = list(set(list(connection1_properties.keys()) + list(connection2_properties.keys())))
    for property_name in total_keys:
        connection1_value = connection1_properties.get(property_name)
        connection2_value = connection2_properties.get(property_name)
        if connection1_value is None:
            merged_properties[property_name] = connection2_value
            continue
        if connection2_value is None:
            merged_properties[property_name] = connection1_value
            continue
        if isinstance(connection1_value, dict):
            merge_function = merge_connection_properties
        else:
            merge_function = (connection_property_specific_merging_functions.get(property_name) or connection_property_type_specific_merging_functions.get(type(connection1_value)))
        merged_value = merge_function and merge_function(connection1_value, connection2_value) or connection2_value
        merged_properties[property_name] = merged_value

    return merged_properties
