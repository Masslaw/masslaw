from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_data_collection import MasslawCaseDataCollector


class GetCaseData(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(self, default_response_body={'case_data': {}})

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_data_collector = MasslawCaseDataCollector(case_instance=self._case_instance, access_user_id=user_id)
        case_data = case_data_collector.get_case_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'case_data'], case_data)


def handler(event, context):
    handler_instance = GetCaseData()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
