from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_data_collection import MasslawCaseDataCollector
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class GetCaseData(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'case_data': {}}, request_query_string_parameters_structure={'case_id': [str], })
        self.__case_id = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_data_collector = MasslawCaseDataCollector(case_instance=case_instance, access_user_id=user_id)
        case_data = case_data_collector.get_case_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'case_data'], case_data)


def handler(event, context):
    handler_instance = GetCaseData()
    return handler_instance.call_handler(event, context)
