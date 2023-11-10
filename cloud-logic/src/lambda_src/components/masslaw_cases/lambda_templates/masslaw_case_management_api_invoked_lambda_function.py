from ...masslaw_cases.management.masslaw_case_user_access_manager import MasslawCaseUnauthorizedUserActionException
from ...masslaw_cases.masslaw_data_instances.masslaw_case_instance import *
from ...masslaw_users.lambda_templates.authenticated_masslaw_user_http_invoked_lambda_function import *
from ...masslaw_users.config.user_statuses import *


class MasslawCaseManagementApiInvokedLambdaFunction(AuthenticatedMasslawUserHttpInvokedLambdaFunction):
    def __init__(
            self,
            name=None,
            default_response_body=None,
            request_query_string_parameters_structure=None,
            request_body_structure=None
    ):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure,
            minimum_user_status_level=UserStatuses.FULLY_APPROVED
        )

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, MasslawCaseDataUpdateException):
            self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.BAD_REQUEST)
            self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE],
                                         f'Invalid Case Data: {exception}')
            return

        if isinstance(exception, MasslawCaseUnauthorizedUserActionException):
            self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.UNAUTHORIZED)
            self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE],
                                         ResponseMessages.UNAUTHORIZED_REQUEST)
            return

        AuthenticatedMasslawUserHttpInvokedLambdaFunction._handle_exception(self, exception)
