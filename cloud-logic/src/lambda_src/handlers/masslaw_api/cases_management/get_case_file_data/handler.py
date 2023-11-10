from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *
from lambda_src.components.masslaw_cases.management.masslaw_case_data_collector import *


class GetCaseFileData(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'file_data': {}
            },
            request_query_string_parameters_structure={
                'case_id': [str],
                'file_id': [str],
            }
        )

        self.__case_id = ''
        self.__file_id = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__file_id = self._request_query_string_params.get('file_id')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)

        user_id = self._caller_user_instance.get_user_id()

        case_instance = MasslawCaseInstance(case_id=self.__case_id)

        case_data_collector = MasslawCaseDataCollector(case_instance=case_instance, access_user_id=user_id)

        file_data = case_data_collector.get_file_data(file_id=self.__file_id)

        self._set_response_attribute([EventKeys.BODY, 'file_data'], file_data)


handler = GetCaseFileData()
