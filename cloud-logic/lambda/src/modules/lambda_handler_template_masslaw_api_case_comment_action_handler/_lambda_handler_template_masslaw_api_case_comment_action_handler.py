from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_file_action_handler import MasslawCaseManagementApiFileActionHandler
from src.modules.masslaw_cases_objects import MasslawCaseCommentInstance
from src.modules.masslaw_cases_objects import masslaw_cases_objects_exceptions


class MasslawCaseManagementApiCaseCommentActionHandler(MasslawCaseManagementApiFileActionHandler):
    def __init__(self, name=None, default_response_body=None, request_path_parameters_structure=None, request_query_string_parameters_structure=None, request_body_structure=None):
        request_path_parameters_structure = request_path_parameters_structure or {}
        request_path_parameters_structure = request_path_parameters_structure.update({'comment_id': [str]})
        MasslawCaseManagementApiFileActionHandler.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_path_parameters_structure=request_path_parameters_structure,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure,
        )
        self._comment_id = ''
        self._comment_instance = None

    def _load_request_path_params(self):
        MasslawCaseManagementApiFileActionHandler._load_request_path_params(self)
        self._comment_id = self._request_path_params.get('comment_id')
        self._comment_instance = MasslawCaseCommentInstance(self._comment_id)

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_cases_objects_exceptions.MasslawCaseCommentDataUpdateException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'Invalid Comment Data: {exception}')
            return

        MasslawCaseManagementApiFileActionHandler._handle_exception(self, exception)
