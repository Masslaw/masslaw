from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_knowledge_management import MasslawCaseKnowledgeManager


class GetCaseKnowledge(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(self, default_response_body={'knowledge': {'entities': [], 'connections': []}})

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        knowledge_manager = MasslawCaseKnowledgeManager(self._case_instance)
        case_knowledge = knowledge_manager.get_case_knowledge_as_user(user_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'knowledge'], case_knowledge)


def handler(event, context):
    handler_instance = GetCaseKnowledge()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
