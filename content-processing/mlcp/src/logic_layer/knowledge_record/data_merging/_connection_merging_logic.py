from typing import Dict

from logic_layer.knowledge_record import KnowledgeRecordConnection
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger
from shared_layer.list_utils import list_utils

connection_property_specific_merging_functions = {'value': lambda v1, v2: max(v1, v2, key=len), 'strength': lambda v1, v2: v1 + v2, }

connection_property_type_specific_merging_functions = {list: lambda list1, list2: list_utils.remove_duplicates(list1 + list2), }


@logger.process_function('Merging knowledge record connections')
def merge_connections(merge_to: KnowledgeRecordConnection, to_merge: KnowledgeRecordConnection):
    merged_properties = merge_connection_properties(merge_to.get_properties(), to_merge.get_properties())
    merge_to.set_id(to_merge.get_id())
    merge_to.set_label(to_merge.get_label())
    merge_to.set_properties(merged_properties)


@logger.process_function('Merging knowledge record connection properties')
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
        connection1_type = type(connection1_value)
        connection2_type = type(connection2_value)
        if connection1_type != connection2_type:
            logger.warn(f"Connection property {common_formats.value(property_name)} has different types in the two connections: {common_formats.value(connection1_type)} and {common_formats.value(connection2_type)} respectively. The value from the second connection will be used.")
            merged_properties[property_name] = connection2_value
            continue
        value_type = connection1_type
        if value_type == dict:
            merge_function = merge_connection_properties
        else:
            merge_function = (connection_property_specific_merging_functions.get(property_name) or connection_property_type_specific_merging_functions.get(value_type))
        merged_value = merge_function and merge_function(connection1_value, connection2_value) or connection2_value
        merged_properties[property_name] = merged_value

    return merged_properties
