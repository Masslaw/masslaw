from lambda_src.components.masslaw_cases.management.masslaw_case_storage_manager import MasslawCaseStorageManager
from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *


class DeleteCaseFile(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
            },
            request_query_string_parameters_structure={
                'case_id': [str],
                'file_id': [str],
            }
        )

        self.__case_id: str = ''
        self.__file_id: str = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__file_id = self._request_query_string_params.get('file_id')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)

        user_id = self._caller_user_instance.get_user_id()

        case_instance = MasslawCaseInstance(case_id=self.__case_id)

        case_storage_manager = MasslawCaseStorageManager(case_instance=case_instance)

        case_storage_manager.delete_file_as_user(file_id=self.__file_id, user_id=user_id)

        case_instance.save_data()


handler = DeleteCaseFile()
