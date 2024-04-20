from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_objects import MasslawCaseInstance
from src.modules.masslaw_cases_objects import masslaw_cases_objects_exceptions
from src.modules.masslaw_users_config import user_statuses
from src.modules.masslaw_cases_config import access_config


class MasslawCaseManagementApiCaseActionHandler(AuthenticatedMasslawUserHttpInvokedLambdaFunction):
    def __init__(self, name=None, default_response_body=None, request_path_parameters_structure=None, request_query_string_parameters_structure=None, request_body_structure=None):
        request_path_parameters_structure = request_path_parameters_structure or {}
        request_path_parameters_structure = request_path_parameters_structure.update({'case_id': [str]})
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_path_parameters_structure=request_path_parameters_structure,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure,
            minimum_user_status_level=user_statuses.UserStatuses.FULLY_APPROVED
        )
        self._case_id = ''
        self._case_instance = None

    def _load_request_path_params(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._load_request_path_params(self)
        self._case_id = self._request_path_params.get('case_id')
        self._case_instance = MasslawCaseInstance(self._case_id)

    def _execute(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._execute(self)
        self.__assert_user_access_to_case()

    def __assert_user_access_to_case(self):
        user_id = self._caller_user_instance.get_user_id()
        self._log(f'asserting case access for user {user_id} to case {self._case_id}')
        case_user_access = MasslawCaseUserAccessManager(case_instance=self._case_instance)
        user_access_level = case_user_access.get_user_access_level_name(user_id)
        self._log(f'user {user_id} has access level {user_access_level} to case {self._case_id}')
        if user_access_level == access_config.CaseAccessEntities.EXTERNAL_CLIENT: raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to perform an action on a case which is not included in a user's case permissions")

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_cases_objects_exceptions.MasslawCaseDataUpdateException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'Invalid Case Data: {exception}')
            return

        if isinstance(exception, masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.UNAUTHORIZED)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], lambda_constants.ResponseMessages.UNAUTHORIZED_REQUEST)
            return

        AuthenticatedMasslawUserHttpInvokedLambdaFunction._handle_exception(self, exception)
