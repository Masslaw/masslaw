from src.modules.masslaw_cloud_configurations import get_configuration_value
from src.modules.masslaw_cloud_configurations import configuration_keys

neptune_endpoints = get_configuration_value(configuration_keys.MASSLAW_KNOWLEDGE_NEPTUNE_ENDPOINTS)


def get_neptune_read_endpoint_for_stage(stage) -> str:
    return neptune_endpoints.get(stage, {}).get('read', '')


def get_neptune_write_endpoint_for_stage(stage) -> str:
    return neptune_endpoints.get(stage, {}).get('write', '')


def get_neptune_protocol_for_stage(stage) -> str:
    return neptune_endpoints.get(stage, {}).get('protocol', 'ws')
