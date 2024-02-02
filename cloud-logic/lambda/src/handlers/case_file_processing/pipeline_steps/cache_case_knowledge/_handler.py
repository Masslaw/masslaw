import json
import os
from concurrent.futures import ThreadPoolExecutor

from src.modules.aws_clients.neptune_client import NeptuneClient
from src.modules.aws_clients.neptune_client import NeptuneConnection
from src.modules.aws_clients.neptune_client import NeptuneEdge
from src.modules.aws_clients.neptune_client import NeptuneNode
from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_config._storage_config import CASES_CONTENT_BUCKET_ID
from src.modules.neptune_endpoints import get_neptune_read_endpoint_for_stage
from src.modules.neptune_endpoints import get_neptune_write_endpoint_for_stage
from src.modules.neptune_endpoints._get_neptune_endpoints import get_neptune_protocol_for_stage

_stage = os.environ.get('STAGE', 'prod')
neptune_read_endpoint = get_neptune_read_endpoint_for_stage(_stage)
neptune_write_endpoint = get_neptune_write_endpoint_for_stage(_stage)
neptune_connection_protocol = get_neptune_protocol_for_stage(_stage)
_neptune_client = NeptuneClient(read_connection=NeptuneConnection(connection_endpoint=neptune_read_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'),
    write_connection=NeptuneConnection(connection_endpoint=neptune_write_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'))

_s3_bucket_manager = S3BucketManager(CASES_CONTENT_BUCKET_ID)

CACHED_NODE_PROPERTIES = ['title', 'datetime']
CACHED_EDGE_PROPERTIES = ['strength']


class CacheCaseKnowledge(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self._file_data = self._get_request_event().get('file_data', {})
        self._set_response_attribute(['file_data'], self._file_data)
        self.__case_id = self._file_data.get('case_id', '')
        self._files_sorted_data = {}
        self.__get_entities()
        self.__get_connections()
        self.__save_to_s3()

    def __get_entities(self):
        request_query_properties = {'case_id': self.__case_id}
        neptune_nodes_response = _neptune_client.get_nodes_by_properties(request_query_properties)
        entities_response = []
        for neptune_node in neptune_nodes_response:
            if not self.__validate_node(neptune_node):
                continue
            entity_id = neptune_node.get_id()
            entity_label = neptune_node.get_label()
            entity_properties = neptune_node.get_properties()
            files = entity_properties.get('files', {}).get('list', [])
            if not files:
                continue
            selected_entity_properties = dictionary_utils.select_keys(entity_properties, CACHED_NODE_PROPERTIES)
            entity_data = {
                'id': entity_id,
                'label': entity_label,
                'properties': selected_entity_properties
            }
            for file_id in files:
                if file_id not in self._files_sorted_data:
                    self._files_sorted_data[file_id] = {
                        'entities': [],
                        'connections': []
                    }
                self._files_sorted_data[file_id]['entities'].append(entity_data)
        self._entities_data = entities_response

    def __validate_node(self, neptune_node: NeptuneNode) -> bool:
        if neptune_node.get_properties().get('case_id', '') != self.__case_id:
            return False
        return True

    def __get_connections(self):
        request_query_properties = {'case_id': self.__case_id}
        neptune_edges_response = _neptune_client.get_edges_by_properties(request_query_properties)
        connections_response = []
        for neptune_edge in neptune_edges_response:
            if not self.__validate_edge(neptune_edge):
                continue
            connection_id = neptune_edge.get_id()
            connection_label = neptune_edge.get_label()
            connection_properties = neptune_edge.get_properties()
            files = connection_properties.get('files', {}).get('list', [])
            if not files:
                continue
            selected_connection_properties = dictionary_utils.select_keys(connection_properties, CACHED_EDGE_PROPERTIES)
            connection_data = {
                'id': connection_id,
                'label': connection_label,
                'from': neptune_edge.get_from_node(),
                'to': neptune_edge.get_to_node(),
                'properties': selected_connection_properties
            }
            for file_id in files:
                if file_id not in self._files_sorted_data:
                    self._files_sorted_data[file_id] = {
                        'entities': [],
                        'connections': []
                    }
                self._files_sorted_data[file_id]['connections'].append(connection_data)
        self._connections_data = connections_response

    def __validate_edge(self, neptune_edge: NeptuneEdge) -> bool:
        if neptune_edge.get_properties().get('case_id', '') != self.__case_id:
            return False
        return True

    def __save_to_s3(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            for file_id in list(self._files_sorted_data.keys()):
                executor.submit(self.__save_upload_data_to_s3_in_json_format, file_id)

    def __save_upload_data_to_s3_in_json_format(self, file_id):
        s3_file_key = f'{file_id}/client_exposed/extracted_knowledge/knowledge.json'
        s3_file_data = self._files_sorted_data.get(file_id, {})
        json_data = json.dumps(s3_file_data)
        encoded_json_data = json_data.encode('utf-8')
        self._log(f'Uploading {encoded_json_data} to {s3_file_key}')
        _s3_bucket_manager.put_object(key=s3_file_key, body=encoded_json_data)
        self._log("Finished uploading")


def handler(event, context):
    handler_instance = CacheCaseKnowledge()
    return handler_instance.call_handler(event, context)
