import os
from src.modules.aws_clients.neptune_client import NeptuneClient
from src.modules.aws_clients.neptune_client import NeptuneConnection
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_knowledge_management import MasslawCaseKnowledgeManager
from src.modules.neptune_endpoints import get_neptune_read_endpoint_for_stage
from src.modules.neptune_endpoints import get_neptune_write_endpoint_for_stage
from src.modules.neptune_endpoints._get_neptune_endpoints import get_neptune_protocol_for_stage
from src.modules.lambda_base import lambda_constants

_stage = os.environ.get('STAGE', 'prod')
neptune_read_endpoint = get_neptune_read_endpoint_for_stage(_stage)
neptune_write_endpoint = get_neptune_write_endpoint_for_stage(_stage)
neptune_connection_protocol = get_neptune_protocol_for_stage(_stage)
_neptune_client = NeptuneClient(read_connection=NeptuneConnection(connection_endpoint=neptune_read_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'),
                                write_connection=NeptuneConnection(connection_endpoint=neptune_write_endpoint, connection_port=8182, connection_protocol=neptune_connection_protocol, connection_type='gremlin'))


class GetCaseKnowledgeItemData(MasslawCaseManagementApiCaseActionHandler):

    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            default_response_body={'knowledge': {'entities': [],'connections': []}},
            request_path_parameters_structure={'item_id': [str], 'item_type': [str]},
        )
        self.__item_id = ''
        self.__item_type = ''

    def _load_request_path_params(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_path_params(self)
        self.__item_id = self._request_path_params.get('item_id')
        self.__item_type = self._request_path_params.get('item_type')

    def _execute(self):
        user_id = self._caller_user_instance.get_user_id()
        knowledge_manager = MasslawCaseKnowledgeManager(self._case_instance)
        case_knowledge = knowledge_manager.get_case_knowledge_item_data_as_user(self.__item_id, self.__item_type, user_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'knowledge'], case_knowledge)

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, ConnectionResetError): return
        MasslawCaseManagementApiCaseActionHandler._handle_exception(self, exception)


def handler(event, context):
    handler_instance = GetCaseKnowledgeItemData()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
