from src.modules.lambda_handler_template_masslaw_api_case_conversation_action_handler import MasslawCaseManagementApiConversationActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.lambda_base import lambda_constants


class PostCaseConversationMessage(MasslawCaseManagementApiConversationActionHandler):

    def __init__(self):
        MasslawCaseManagementApiConversationActionHandler.__init__(self, request_body_structure={'prompt': [str]}, default_response_body={'content': {}})

    def _load_request_body(self):
        MasslawCaseManagementApiConversationActionHandler._load_request_body(self)
        self._prompt = self._request_body.get('prompt', '')

    def _execute(self):
        MasslawCaseManagementApiConversationActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(case_instance=self._case_instance)
        new_conversation_content = case_conversations_manager.send_message_to_conversation_as_user(user_id, self._conversation_id, self._prompt)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'content'], new_conversation_content)


def handler(event, context):
    handler_instance = PostCaseConversationMessage()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
