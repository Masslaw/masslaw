from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.lambda_base import lambda_constants


class PutNewCaseConversation(MasslawCaseManagementApiCaseActionHandler):

    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(self, request_body_structure={'name': [str]}, default_response_body={'conversation': {}})

    def _load_request_body(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_body(self)
        self._conversation_name = self._request_body.get('name', '')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(case_instance=self._case_instance)
        new_conversation_id, new_conversation_data = case_conversations_manager.start_conversation_as_user(user_id, self._conversation_name)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'id'], new_conversation_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'data'], new_conversation_data)


def handler(event, context):
    handler_instance = PutNewCaseConversation()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
