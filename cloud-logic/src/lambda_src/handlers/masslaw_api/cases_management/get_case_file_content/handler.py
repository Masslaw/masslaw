from lambda_src.components.masslaw_cases.management.masslaw_case_storage_manager import *
from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *
from lambda_src.components.masslaw_cases.masslaw_data_instances.masslaw_case_instance import *


class GetCaseFileContent(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'download_urls': {}
            },
            request_query_string_parameters_structure={
                'case_id': [str],
                'file_id': [str],
                'content_paths': [str],
            }
        )

        self.__case_id = ''
        self.__file_id = ''
        self.__content_paths = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__file_id = self._request_query_string_params.get('file_id')
        self.__content_paths = self._request_query_string_params.get('content_paths').split("|")

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)

        user_id = self._caller_user_instance.get_user_id()

        case_instance = MasslawCaseInstance(self.__case_id)

        case_storage_manager = MasslawCaseStorageManager(case_instance=case_instance)

        urls = {}
        for content_path in self.__content_paths:
            urls[content_path] = case_storage_manager.get_case_file_download_url(user_id=user_id,
                                                                                 file_id=self.__file_id,
                                                                                 content_path=content_path)

        case_instance.save_data()

        self._set_response_attribute([EventKeys.BODY, 'download_urls'], urls)


handler = GetCaseFileContent()
