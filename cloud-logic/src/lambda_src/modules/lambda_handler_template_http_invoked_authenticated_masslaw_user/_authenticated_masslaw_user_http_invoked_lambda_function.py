from src.lambda_src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline._http_invoked_lambda_function_handler import *
from lambda_src.modules.masslaw_users_objects.management.masslaw_user_status_manager import *
from lambda_src.modules.masslaw_users_objects._masslaw_user_instance import *
from src.lambda_src.modules.lambda_base._consts import *
from ...util import json_utils


class AuthenticatedMasslawUserHttpInvokedLambdaFunction(HTTPInvokedLambdaFunctionHandler):
    def __init__(
            self,
            name=None,
            default_response_body=None,
            request_query_string_parameters_structure=None,
            request_body_structure=None,
            minimum_user_status_level=UserStatuses.GUEST
    ):
        HTTPInvokedLambdaFunctionHandler.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure
        )
        self.__minimum_user_status_level = minimum_user_status_level

        self._set_response_attribute([EventKeys.BODY, EventKeys.USER_STATUS], -1)

        self._access_token = ''
        self._caller_user_instance = None

        self._log(f'Calling an authenticated user http invoked lambda handler. \n'
                  f'Minimum allowed user status: {minimum_user_status_level}')

    def _load_request_headers(self):
        HTTPInvokedLambdaFunctionHandler._load_request_headers(self)
        access_token = json_utils.get_from(self._request_headers, [RequestHeaders.AUTHORIZATION], '')
        self._access_token = access_token.replace('Bearer ', '').replace(' ', '')

    def _handle_event(self):
        HTTPInvokedLambdaFunctionHandler._handle_event(self)
        self._caller_user_instance = MasslawUserInstance(access_token=self._access_token)
        self._status_manager = MasslawUserStatusManager(self._caller_user_instance)
        self._log(f'Caller user status: {self._status_manager.get_user_status()}')
        self._set_response_attribute([EventKeys.BODY, EventKeys.USER_STATUS], self._status_manager.get_user_status())
        self._status_manager.assert_status(self.__minimum_user_status_level)

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, MasslawUserStatusAssertFailed):
            self._log(f'User status assertion failed')
            self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.UNAUTHORIZED)
            self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE], ResponseMessages.UNAUTHORIZED_REQUEST)
            return

        HTTPInvokedLambdaFunctionHandler._handle_exception(self, exception)
