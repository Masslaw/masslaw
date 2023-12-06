import os

from src.modules.aws_clients.neptune_client import NeptuneClient
from src.modules.aws_clients.neptune_client import NeptuneConnection
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_storage_management import masslaw_case_storage_management_exceptions
from src.modules.neptune_endpoints import get_neptune_read_endpoint_for_stage
from src.modules.dictionary_utils import dictionary_utils


_stage = os.environ.get('STAGE', 'prod')
neptune_read_endpoint = get_neptune_read_endpoint_for_stage(_stage)
neptune_write_endpoint = get_neptune_read_endpoint_for_stage(_stage)
_neptune_client = NeptuneClient(
    read_connection=NeptuneConnection(
        connection_endpoint=neptune_read_endpoint,
        connection_port=8182,
        connection_protocol='wss',
        connection_type='gremlin'
    ),
    write_connection=NeptuneConnection(
        connection_endpoint=neptune_write_endpoint,
        connection_port=8182,
        connection_protocol='wss',
        connection_type='gremlin'
    )
)


class StartCaseFileUpload(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={
            'knowledge': {
                'entities': [],
                'connections': []
            }
        }, request_query_string_parameters_structure={
            'case_id': [str],
        }, request_body_structure={
            'entities': {
                'include_properties': [list, None],
                'label': [str, None],
                'query_properties': [dict, None]
            },
            'connections': {
                'include_properties': [list, None],
                'label': [str],
                'query_properties': [dict, None]
            }
        })
        self.__case_id = ''
        self.__entity_query_params = {}
        self.__connection_query_params = {}
        self._neptune_read_endpoint = ''
        self._neptune_write_endpoint = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__entity_query_params = self._request_body.get('entities', {})
        self.__connection_query_params = self._request_body.get('connections', {})

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        self.__get_entities()
        self.__get_connections()
        self.__build_response()

    def __get_entities(self):
        request_query_properties = self.__entity_query_params.get('query_properties', {})
        request_include_properties = self.__entity_query_params.get('include_properties', [])
        request_query_properties['case_id'] = self.__case_id
        request_label = self.__entity_query_params.get('label')
        neptune_nodes_response = _neptune_client.get_nodes_by_properties(request_query_properties, request_label)
        entities_response = []
        for neptune_node in neptune_nodes_response:
            entity_id = neptune_node.get_id()
            entity_label = neptune_node.get_label()
            entity_properties = neptune_node.get_properties()
            entity_properties = dictionary_utils.select_keys(entity_properties, request_include_properties)
            entities_response.append({
                'id': entity_id,
                'label': entity_label,
                'properties': entity_properties
            })
        self._entities_response = entities_response

    def __get_connections(self):
        request_query_properties = self.__connection_query_params.get('query_properties', {})
        request_include_properties = self.__connection_query_params.get('include_properties', [])
        request_query_properties['case_id'] = self.__case_id
        request_label = self.__connection_query_params.get('label')
        neptune_edges_response = _neptune_client.get_edges_by_properties(request_query_properties, request_label)
        connections_response = []
        for neptune_edge in neptune_edges_response:
            connection_id = neptune_edge.get_id()
            connection_from_node_id = neptune_edge.get_from_node()
            connection_to_node_id = neptune_edge.get_to_node()
            connection_label = neptune_edge.get_label()
            connection_properties = neptune_edge.get_properties()
            connection_properties = dictionary_utils.select_keys(connection_properties, request_include_properties)
            connections_response.append({
                'id': connection_id,
                'from_node_id': connection_from_node_id,
                'to_node_id': connection_to_node_id,
                'label': connection_label,
                'properties': connection_properties
            })
        self._connections_response = connections_response

    def __build_response(self):
        self._set_response_attribute(['knowledge', 'entities'], self._entities_response)
        self._set_response_attribute(['knowledge', 'connections'], self._connections_response)

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_case_storage_management_exceptions.MasslawFileTypeNotSupportedException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'{exception}')
            return


handler = StartCaseFileUpload()
