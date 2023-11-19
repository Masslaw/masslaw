from create_case.modules.dictionary_utils import dictionary_utils
from create_case.modules.lambda_base import lambda_constants
from create_case.modules.lambda_handler_template_http_invoked import HTTPInvokedLambdaFunctionHandler
from create_case.modules.masslaw_users_config import user_statuses
from create_case.modules.masslaw_users_objects import MasslawUserInstance
from create_case.modules.masslaw_users_status_management import MasslawUserStatusManager
from create_case.modules.masslaw_users_status_management import masslaw_users_status_management_exceptions


class AuthenticatedMasslawUserHttpInvokedLambdaFunction(HTTPInvokedLambdaFunctionHandler):
    def __init__(
            self,
            name=None,
            default_response_body=None,
            request_query_string_parameters_structure=None,
            request_body_structure=None,
            minimum_user_status_level=user_statuses.UserStatuses.GUEST
    ):
        HTTPInvokedLambdaFunctionHandler.__init__(
            self,
            name=name,
            default_response_body=default_response_body,
            request_query_string_parameters_structure=request_query_string_parameters_structure,
            request_body_structure=request_body_structure
        )
        self.__minimum_user_status_level = minimum_user_status_level

        self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.USER_STATUS], -1)

        self._access_token = ''
        self._caller_user_instance = None

        self._log(f'Calling an authenticated user http invoked lambda handler. \n'
                  f'Minimum allowed user status: {minimum_user_status_level}')

    def _load_request_headers(self):
        HTTPInvokedLambdaFunctionHandler._load_request_headers(self)
        access_token = dictionary_utils.get_from(self._request_headers, [lambda_constants.RequestHeaders.AUTHORIZATION], '')
        self._access_token = access_token.replace('Bearer ', '').replace(' ', '')

    def _handle_event(self):
        HTTPInvokedLambdaFunctionHandler._handle_event(self)
        self._caller_user_instance = MasslawUserInstance(access_token=self._access_token)
        self._status_manager = MasslawUserStatusManager(self._caller_user_instance)
        self._log(f'Caller user status: {self._status_manager.get_user_status()}')
        self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.USER_STATUS], self._status_manager.get_user_status())
        self._status_manager.assert_status(self.__minimum_user_status_level)

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_users_status_management_exceptions.MasslawUserStatusAssertFailed):
            self._log(f'User status assertion failed')
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.UNAUTHORIZED)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], lambda_constants.ResponseMessages.UNAUTHORIZED_REQUEST)
            return

        HTTPInvokedLambdaFunctionHandler._handle_exception(self, exception)
