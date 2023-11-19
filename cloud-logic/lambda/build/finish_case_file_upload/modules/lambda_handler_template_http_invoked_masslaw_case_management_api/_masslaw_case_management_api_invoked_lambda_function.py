from finish_case_file_upload.modules.lambda_base import lambda_constants
from finish_case_file_upload.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction
from finish_case_file_upload.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from finish_case_file_upload.modules.masslaw_cases_objects import masslaw_cases_objects_exceptions
from finish_case_file_upload.modules.masslaw_users_config import user_statuses


class MasslawCaseManagementApiInvokedLambdaFunction(AuthenticatedMasslawUserHttpInvokedLambdaFunction):
    def __init__(self, name=None, default_response_body=None, request_query_string_parameters_structure=None, request_body_structure=None):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(self, name=name, default_response_body=default_response_body, request_query_string_parameters_structure=request_query_string_parameters_structure, request_body_structure=request_body_structure,
            minimum_user_status_level=user_statuses.UserStatuses.FULLY_APPROVED)

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
