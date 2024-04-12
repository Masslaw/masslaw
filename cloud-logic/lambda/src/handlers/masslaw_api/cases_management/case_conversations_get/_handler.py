from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.lambda_base import lambda_constants


class GetCaseConversations(MasslawCaseManagementApiCaseActionHandler):

    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(self, default_response_body={'conversations': {}})

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(case_instance=self._case_instance)
        case_conversations = case_conversations_manager.get_user_case_conversations(user_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'conversations'], case_conversations)


def handler(event, context):
    handler_instance = GetCaseConversations()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
