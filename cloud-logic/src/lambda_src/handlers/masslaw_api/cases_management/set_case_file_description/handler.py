from lambda_src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from lambda_src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from lambda_src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from lambda_src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from lambda_src.modules.masslaw_cases_objects import MasslawCaseInstance


class SetCaseFileDescription(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, request_query_string_parameters_structure={'case_id': [str], 'file_id': [str], }, request_body_structure={'value': [str], })
        self.__case_id = ''
        self.__file_id = ''
        self.__new_description = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__file_id = self._request_query_string_params.get('file_id')

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__new_description = self._request_body.get('value')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_user_access = MasslawCaseUserAccessManager(case_instance=case_instance)
        user_access_files = case_user_access.get_user_access_files(user_id)
        if self.__file_id not in user_access_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to set the description of a file which is not included in a user's case permissions")
        file_instance = MasslawCaseFileInstance(file_id=self.__file_id)
        file_instance.set_data_property(['description'], self.__new_description)
        file_instance.save_data()


handler = SetCaseFileDescription()
