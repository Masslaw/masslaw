from src.modules.dictionary_utils import dictionary_utils
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_config import access_config
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class SetCaseData(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, request_query_string_parameters_structure={'case_id': [str], }, request_body_structure={'new_data': [dict]})
        self.__case_id = ''
        self.__new_data = {}

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id', '')

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__new_data = self._request_body.get('new_data', {})

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_user_access = MasslawCaseUserAccessManager(case_instance=case_instance)
        user_access_level = case_user_access.get_user_access_level_name(user_id)
        if user_access_level not in (access_config.CaseAccessEntities.OWNER_CLIENT, access_config.CaseAccessEntities.MANAGER_CLIENT):
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt to change the data of a case is made by an unauthorized user.")
        update_object = self.__build_update_object()
        case_instance.update_data(update_object, create_new_keys=False)
        case_instance.save_data()

    def __build_update_object(self):
        update_object = self.__new_data.copy()
        if new_title := dictionary_utils.get_from(self.__new_data, ['title']):
            dictionary_utils.set_at(update_object, ['information', 'title'], new_title)
        if new_description := dictionary_utils.get_from(self.__new_data, ['description']):
            dictionary_utils.set_at(update_object, ['information', 'description'], new_description)
        return update_object


handler = SetCaseData()
