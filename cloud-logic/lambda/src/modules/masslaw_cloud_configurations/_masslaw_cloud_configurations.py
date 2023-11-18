from src.modules.masslaw_cloud_configurations._config import GLOBAL_VALUES_DYNAMODB_TABLE_NAME
from src.modules.remote_data_management_dynamodb import DynamodbDataHolder


def get_configuration_value(key: str):
    value_item = DynamodbDataHolder(GLOBAL_VALUES_DYNAMODB_TABLE_NAME, key)
    if not value_item.is_valid(): return None
    return value_item.get_data_property("value")
