from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_creation import create_a_new_case


class CreateCase(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'case_id': ''}, request_body_structure={'case_data': {'title': [str], 'description': [str]}})
        self.__case_data = {}

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_data = {}

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__case_data = self._request_body.get('case_data')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        new_case = create_a_new_case(creator_user_id=self._caller_user_instance.get_user_id(), case_creation_data=self.__case_data)
        new_case.save_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'case_id'], new_case.get_case_id())


def handler(event, context):
    handler_instance = CreateCase()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
