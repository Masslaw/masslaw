import os
from lambda_src.components.masslaw_cases.management.masslaw_case_creation import *
from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *


class CreateCase(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'case_id': ''
            },
            request_body_structure={
                'case_data': {
                    'title': [str],
                    'description': [str]
                }
            }
        )

        self.__case_data = {}

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__case_data = self._request_body.get('case_data')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)

        new_case = create_a_new_case(creator_user_id=self._caller_user_instance.get_user_id(),
                                     case_creation_data=self.__case_data)

        new_case.save_data()

        self._set_response_attribute([EventKeys.BODY, 'case_id'], new_case.get_case_id())


handler = CreateCase()
