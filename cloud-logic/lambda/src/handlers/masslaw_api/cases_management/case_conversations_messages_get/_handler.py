from src.modules.lambda_handler_template_masslaw_api_case_conversation_action_handler import MasslawCaseManagementApiConversationActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.lambda_base import lambda_constants


class GetCaseConversationContent(MasslawCaseManagementApiConversationActionHandler):

    def __init__(self):
        MasslawCaseManagementApiConversationActionHandler.__init__(self, default_response_body={'content': {}})

    def _execute(self):
        MasslawCaseManagementApiConversationActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(case_instance=self._case_instance)
        conversation_content = case_conversations_manager.get_conversation_content(user_id, self._conversation_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'content'], conversation_content)


def handler(event, context):
    handler_instance = GetCaseConversationContent()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
