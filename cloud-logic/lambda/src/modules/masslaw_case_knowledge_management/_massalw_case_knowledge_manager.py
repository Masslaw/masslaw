import os
from concurrent.futures import ThreadPoolExecutor

from src.modules.aws_clients.neptune_client import NeptuneClient
from src.modules.aws_clients.neptune_client import NeptuneConnection
from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import storage_config
from src.modules.masslaw_cases_objects import MasslawCaseInstance
from src.modules.neptune_endpoints import get_neptune_read_endpoint_for_stage
from src.modules.neptune_endpoints import get_neptune_write_endpoint_for_stage
from src.modules.neptune_endpoints._get_neptune_endpoints import get_neptune_protocol_for_stage

stage = os.environ.get('STAGE', 'prod')
neptune_read_endpoint = get_neptune_read_endpoint_for_stage(stage)
neptune_write_endpoint = get_neptune_write_endpoint_for_stage(stage)
neptune_connection_protocol = get_neptune_protocol_for_stage(stage)

s3_bucket_manager = S3BucketManager(storage_config.CASES_KNOWLEDGE_BUCKET_ID)


class MasslawCaseKnowledgeManager:

    def __init__(self, case_instance: MasslawCaseInstance):
        self.__case_instance = case_instance

    def get_case_knowledge(self) -> dict:
        s3_knowledge_key = f'{self.__case_instance.get_case_id()}/knowledge.json'
        knowledge_data = s3_bucket_manager.get_object(s3_knowledge_key)
        if not knowledge_data: return {'connections': [], 'entities': []}
        knowledge = dictionary_utils.ensure_dict(knowledge_data)
        return knowledge

    def get_case_knowledge_as_user(self, user_id: str) -> dict:
        knowledge = self.get_case_knowledge()
        access_manager = MasslawCaseUserAccessManager(self.__case_instance)
        case_files = access_manager.get_user_accessible_files(user_id)
        self.clean_knowledge_data(knowledge, case_files)
        return knowledge

    def get_case_knowledge_item_data(self, knowledge_item_id: str, knowledge_item_type: str) -> dict:
        if knowledge_item_type not in ('node', 'edge',): raise ValueError(f'item_type must be one of: "node", "edge". Got: {knowledge_item_type}')
        if knowledge_item_type == 'node': return self.get_node_item_data(knowledge_item_id)
        if knowledge_item_type == 'edge': return self.get_edge_item_data(knowledge_item_id)

    def get_case_knowledge_item_data_as_user(self, knowledge_item_id: str, knowledge_item_type: str, user_id: str) -> dict:
        knowledge = self.get_case_knowledge_item_data(knowledge_item_id, knowledge_item_type)
        access_manager = MasslawCaseUserAccessManager(self.__case_instance)
        case_files = access_manager.get_user_accessible_files(user_id)
        self.clean_knowledge_data(knowledge, case_files)
        return knowledge

    def get_node_item_data(self, node_id: str) -> dict:
        self._create_neptune_client()
        response = {'entities': [], 'connections': []}
        with ThreadPoolExecutor() as executor:
            node_data_future = executor.submit(self._neptune_client.get_nodes_by_ids, [node_id])
            node_outgoing_connections_future = executor.submit(self._neptune_client.get_edges_by_nodes_connection, node_id, None)
            node_ingoing_connections_future = executor.submit(self._neptune_client.get_edges_by_nodes_connection, None, node_id)
            node_data = node_data_future.result()[0]
            node_outgoing_connections = node_outgoing_connections_future.result()
            node_ingoing_connections = node_ingoing_connections_future.result()
        if node_data is None: return response
        to_nodes_futures = []
        from_nodes_futures = []
        connected_nodes = []
        with ThreadPoolExecutor() as executor:
            for connection in node_outgoing_connections: to_nodes_futures.append(executor.submit(self._neptune_client.get_nodes_by_ids, [connection.get_to_node()]))
            for connection in node_ingoing_connections: from_nodes_futures.append(executor.submit(self._neptune_client.get_nodes_by_ids, [connection.get_from_node()]))
            for future in to_nodes_futures + from_nodes_futures: connected_nodes.append(future.result()[0])
        all_nodes_by_id = {node_data.get_id(): node_data}
        for connected_node in connected_nodes: all_nodes_by_id[connected_node.get_id()] = connected_node
        all_nodes = list(all_nodes_by_id.values())
        for node in all_nodes:
            response['entities'].append({'id': node.get_id(), 'label': node.get_label(), 'properties': node.get_properties()})
        for connection in node_outgoing_connections + node_ingoing_connections:
            response['connections'].append({'id': connection.get_id(), 'label': connection.get_label(), 'from': connection.get_from_node(), 'to': connection.get_to_node(), 'properties': connection.get_properties()})
        return response

    def get_edge_item_data(self, edge_id: str):
        self._create_neptune_client()
        edge_data = self._neptune_client.get_edges_by_ids([edge_id])[0]
        with ThreadPoolExecutor() as executor:
            from_node_future = executor.submit(self._neptune_client.get_nodes_by_ids, [edge_data.get_from_node()])
            to_node_future = executor.submit(self._neptune_client.get_nodes_by_ids, [edge_data.get_to_node()])
            from_node = from_node_future.result()[0]
            to_node = to_node_future.result()[0]
        response = {'entities': [{'id': from_node.get_id(), 'label': from_node.get_label(), 'properties': from_node.get_properties()}, {'id': to_node.get_id(), 'label': to_node.get_label(), 'properties': to_node.get_properties()}],
                    'connections': [{'id': edge_data.get_id(), 'label': edge_data.get_label(), 'from': edge_data.get_from_node(), 'to': edge_data.get_to_node(), 'properties': edge_data.get_properties()}]}
        return response

    def clean_knowledge_data(self, knowledge: dict, files: list[str]):
        clean_entities = []
        for entity in knowledge.get('entities', []):
            self._clean_knowledge_entity_data(entity, files)
            if not len(dictionary_utils.get_from(entity, ['properties', 'files', 'list'], [])): continue
            clean_entities.append(entity)
        clean_connections = []
        for connection in knowledge.get('connections', []):
            self._clean_knowledge_connection_data(connection, files)
            if not len(dictionary_utils.get_from(connection, ['properties', 'files', 'list'], [])): continue
            clean_connections.append(connection)
        knowledge['entities'] = clean_entities
        knowledge['connections'] = clean_connections

    def _clean_knowledge_entity_data(self, entity: dict, files: list[str]):
        entity_files = set(dictionary_utils.get_from(entity, ['properties', 'files', 'list'], []))
        dictionary_utils.set_at(entity, ['properties', 'files', 'list'], list(entity_files & set(files)))
        text_data = dictionary_utils.get_from(entity, ['properties', 'text'], {})
        text_data = dictionary_utils.select_keys(text_data, files)
        dictionary_utils.set_at(entity, ['properties', 'text'], text_data)

    def _clean_knowledge_connection_data(self, connection: dict, files: list[str]):
        connection_files = set(dictionary_utils.get_from(connection, ['properties', 'files', 'list'], []))
        dictionary_utils.set_at(connection, ['properties', 'files', 'list'], list(connection_files & set(files)))
        text_data = dictionary_utils.get_from(connection, ['properties', 'text'], {})
        text_data = dictionary_utils.select_keys(text_data, files)
        dictionary_utils.set_at(connection, ['properties', 'text'], text_data)

    def _create_neptune_client(self):
        self._neptune_client = NeptuneClient(read_connection=NeptuneConnection(connection_endpoint=neptune_read_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'),
                                             write_connection=NeptuneConnection(connection_endpoint=neptune_write_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'))
