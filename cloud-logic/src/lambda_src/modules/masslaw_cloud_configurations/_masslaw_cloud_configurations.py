from lambda_src.components.masslaw_cloud_configurations.config.names import *
from lambda_src.components.util.dynamodb_data_holder import *


def get_configuration_value(key: str):
    value_item = DynamodbDataHolder(GLOBAL_VALUES_DYNAMODB_TABLE_NAME, key)
    if not value_item.is_valid(): return None
    return value_item.get_data_property("value")
