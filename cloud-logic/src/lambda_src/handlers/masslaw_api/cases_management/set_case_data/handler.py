from lambda_src.components.masslaw_cases.config.access_config import CaseAccessEntities
from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import \
    MasslawCaseManagementApiInvokedLambdaFunction
from lambda_src.components.masslaw_cases.management.masslaw_case_user_access_manager import \
    MasslawCaseUserAccessManager, MasslawCaseUnauthorizedUserActionException
from lambda_src.components.masslaw_cases.masslaw_data_instances.masslaw_case_instance import MasslawCaseInstance
from lambda_src.components.util import json_utils


class SetCaseData(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            request_query_string_parameters_structure={
                'case_id': [str],
            },
            request_body_structure={
                'new_data': [dict]
            }
        )

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

        if user_access_level not in (CaseAccessEntities.OWNER_CLIENT, CaseAccessEntities.MANAGER_CLIENT):
            raise MasslawCaseUnauthorizedUserActionException(
                f"An attempt to change the data of a case is made by an unauthorized user.")

        update_object = self.__build_update_object()

        case_instance.update_data(update_object, create_new_keys=False)

        case_instance.save_data()

    def __build_update_object(self):
        update_object = self.__new_data.copy()
        if new_title := json_utils.get_from(self.__new_data, ['title']):
            update_object = json_utils.set_at(update_object, ['information', 'title'], new_title)
        if new_description := json_utils.get_from(self.__new_data, ['description']):
            update_object = json_utils.set_at(update_object, ['information', 'description'], new_description)
        return update_object



handler = SetCaseData()
