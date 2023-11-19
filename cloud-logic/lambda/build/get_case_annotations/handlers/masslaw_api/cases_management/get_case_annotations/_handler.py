from get_case_annotations.modules.lambda_base import lambda_constants
from get_case_annotations.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from get_case_annotations.modules.masslaw_case_data_collection import MasslawCaseDataCollector
from get_case_annotations.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from get_case_annotations.modules.masslaw_cases_objects import MasslawCaseInstance


class GetCaseAnnotations(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'annotations': []}, request_query_string_parameters_structure={'case_id': [str], })
        self.__case_id = ''
        self.__files = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        if _files := self._request_query_string_params.get('files', ''): self.__files = _files.split('|')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_data_collector = MasslawCaseDataCollector(case_instance=case_instance, access_user_id=user_id)
        case_user_access = MasslawCaseUserAccessManager(case_instance=case_instance)
        user_access_files = case_user_access.get_user_access_files(user_id)
        file_ids = list(set(self.__files or user_access_files) & set(user_access_files))
        case_file_annotations = [annotation_data for f_id in file_ids for annotation_data in case_data_collector.get_file_annotations(f_id)]
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'annotations'], case_file_annotations)


handler = GetCaseAnnotations()
