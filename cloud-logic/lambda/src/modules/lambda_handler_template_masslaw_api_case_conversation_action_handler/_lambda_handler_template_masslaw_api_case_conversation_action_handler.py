from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions


class MasslawCaseManagementApiConversationActionHandler(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self, name=None, default_response_body=None, request_path_parameters_structure=None, request_query_string_parameters_structure=None, request_body_structure=None):
        request_path_parameters_structure = request_path_parameters_structure or {}
        request_path_parameters_structure = request_path_parameters_structure.update({'conversation_id': [str]})
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_path_parameters_structure=request_path_parameters_structure,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure,
        )
        self._conversation_id = ''

    def _load_request_path_params(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_path_params(self)
        self._conversation_id = self._request_path_params.get('conversation_id', '')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        self.__assert_user_access_to_conversation()

    def __assert_user_access_to_conversation(self):
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(self._case_instance)
        conversation_data = case_conversations_manager.get_conversation_data(user_id, self._conversation_id)
        if not conversation_data: raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to access a conversation that does not exist or that the user does not have access to. Conversation ID: {self._conversation_id}")
