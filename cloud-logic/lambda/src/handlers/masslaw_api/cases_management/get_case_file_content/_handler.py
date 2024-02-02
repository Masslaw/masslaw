from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_storage_management import MasslawCaseStorageManager
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class GetCaseFileContent(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'download_urls': {}}, request_query_string_parameters_structure={'case_id': [str], 'file_id': [str], 'content_paths': [str], })
        self.__case_id = ''
        self.__file_id = ''
        self.__content_paths = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
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
        with ThreadPoolExecutor(max_workers=100) as executor:
            submissions: Dict[str, Future] = {}
            for content_path in self.__content_paths:
                submissions[content_path] = executor.submit(case_storage_manager.get_case_file_download_url, user_id, self.__file_id, content_path)
                self._log(f"Submitted {content_path}")
            for content_path, submission in submissions.items():
                urls[content_path] = submission.result()
                self._log(f"Got {content_path} --> {urls[content_path]}")
        case_instance.save_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'download_urls'], urls)


def handler(event, context):
    handler_instance = GetCaseFileContent()
    return handler_instance.call_handler(event, context)
