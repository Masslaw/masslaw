from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cases_objects import masslaw_cases_objects_exceptions


class MasslawCaseManagementApiFileActionHandler(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self, name=None, default_response_body=None, request_path_parameters_structure=None, request_query_string_parameters_structure=None, request_body_structure=None):
        request_path_parameters_structure = request_path_parameters_structure or {}
        request_path_parameters_structure = request_path_parameters_structure.update({'file_id': [str]})
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_path_parameters_structure=request_path_parameters_structure,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure,
        )
        self._file_id = ''
        self._file_instance = None

    def _load_request_path_params(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_path_params(self)
        self._file_id = self._request_path_params.get('file_id')
        self._file_instance = MasslawCaseFileInstance(self._file_id)

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        self.__assert_user_access_to_file()

    def __assert_user_access_to_file(self):
        user_id = self._caller_user_instance.get_user_id()
        case_user_access = MasslawCaseUserAccessManager(case_instance=self._case_instance)
        user_access_files = case_user_access.get_user_accessible_files(user_id)
        if self._file_id not in user_access_files: raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to set the description of a file which is not included in a user's case permissions")

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_cases_objects_exceptions.MasslawCaseFileDataUpdateException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'Invalid File Data: {exception}')
            return

        MasslawCaseManagementApiCaseActionHandler._handle_exception(self, exception)
