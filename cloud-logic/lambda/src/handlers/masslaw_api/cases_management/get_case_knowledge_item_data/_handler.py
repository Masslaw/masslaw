import os
from concurrent.futures import ThreadPoolExecutor

from src.modules.aws_clients.neptune_client import NeptuneClient
from src.modules.aws_clients.neptune_client import NeptuneConnection
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.neptune_endpoints import get_neptune_read_endpoint_for_stage
from src.modules.neptune_endpoints import get_neptune_write_endpoint_for_stage
from src.modules.neptune_endpoints._get_neptune_endpoints import get_neptune_protocol_for_stage

_stage = os.environ.get('STAGE', 'prod')
neptune_read_endpoint = get_neptune_read_endpoint_for_stage(_stage)
neptune_write_endpoint = get_neptune_write_endpoint_for_stage(_stage)
neptune_connection_protocol = get_neptune_protocol_for_stage(_stage)
_neptune_client = NeptuneClient(read_connection=NeptuneConnection(connection_endpoint=neptune_read_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'),
                                write_connection=NeptuneConnection(connection_endpoint=neptune_write_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'))


class GetCaseKnowledgeItemData(MasslawCaseManagementApiInvokedLambdaFunction):

    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={
            'knowledge': {
                'entities': [],
                'connections': []
            }
        }, request_query_string_parameters_structure={
            'case_id': [str],
            'item_id': [str, int],
            'item_type': [str]
        })
        self.__case_id = ''
        self.__item_id = ''
        self.__item_type = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''
        self.__item_id = ''
        self.__item_type = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__item_id = self._request_query_string_params.get('item_id')
        self.__item_type = self._request_query_string_params.get('item_type')

    def _execute(self):
        if self.__item_type not in ('node', 'edge',):
            raise ValueError(f'item_type must be one of: "node", "edge". Got: {self.__item_type}')
        if self.__item_type == 'node':
            self._set_response_attribute(['body', 'knowledge'], self.__handle_node())
            return
        if self.__item_type == 'edge':
            self._set_response_attribute(['body', 'knowledge'], self.__handle_edge())
            return

    def __handle_node(self):
        with ThreadPoolExecutor() as executor:
            node_data_future = executor.submit(_neptune_client.get_node_by_id, self.__item_id)
            node_outgoing_connections_future = executor.submit(_neptune_client.get_edges_by_nodes_connection, self.__item_id, None)
            node_ingoing_connections_future = executor.submit(_neptune_client.get_edges_by_nodes_connection, None, self.__item_id)

            node_data = node_data_future.result()
            node_outgoing_connections = node_outgoing_connections_future.result()
            node_ingoing_connections = node_ingoing_connections_future.result()

        response = {
            'entities': [],
            'connections': []
        }

        with ThreadPoolExecutor() as executor:
            to_nodes_futures = []
            for connection in node_outgoing_connections:
                to_nodes_futures.append(executor.submit(_neptune_client.get_node_by_id, connection.get_to_node()))
            from_nodes_futures = []
            for connection in node_ingoing_connections:
                from_nodes_futures.append(executor.submit(_neptune_client.get_node_by_id, connection.get_from_node()))
            connected_nodes = []
            for future in to_nodes_futures + from_nodes_futures:
                connected_nodes.append(future.result())

        all_nodes_by_id = {
            node_data.get_id(): node_data
        }
        for connected_node in connected_nodes:
            all_nodes_by_id[connected_node.get_id()] = connected_node
        all_nodes = list(all_nodes_by_id.values())

        for node in all_nodes:
            response['entities'].append({
                'id': node.get_id(),
                'label': node.get_label(),
                'properties': node.get_properties()
            })
        for connection in node_outgoing_connections + node_ingoing_connections:
            response['connections'].append({
                'id': connection.get_id(),
                'label': connection.get_label(),
                'from': connection.get_from_node(),
                'to': connection.get_to_node(),
                'properties': connection.get_properties()
            })
        return response

    def __handle_edge(self):
        edge_data = _neptune_client.get_edge_by_id(self.__item_id)
        with ThreadPoolExecutor() as executor:
            from_node_future = executor.submit(_neptune_client.get_node_by_id, edge_data.get_from_node())
            to_node_future = executor.submit(_neptune_client.get_node_by_id, edge_data.get_to_node())
            from_node = from_node_future.result()
            to_node = to_node_future.result()

        response = {
            'entities': [{
                'id': from_node.get_id(),
                'label': from_node.get_label(),
                'properties': from_node.get_properties()
            }, {
                'id': to_node.get_id(),
                'label': to_node.get_label(),
                'properties': to_node.get_properties()
            }],
            'connections': [{
                'id': edge_data.get_id(),
                'label': edge_data.get_label(),
                'from': edge_data.get_from_node(),
                'to': edge_data.get_to_node(),
                'properties': edge_data.get_properties()
            }]
        }
        return response

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, ConnectionResetError): return
        MasslawCaseManagementApiInvokedLambdaFunction._handle_exception(self, exception)


handler = GetCaseKnowledgeItemData()
