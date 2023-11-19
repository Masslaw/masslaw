import json

from set_case_file_annotation.modules.dictionary_utils import dictionary_utils
from set_case_file_annotation.modules.lambda_base import LambdaHandler
from set_case_file_annotation.modules.lambda_base import lambda_base_exceptions
from set_case_file_annotation.modules.lambda_base import lambda_constants

HARD_CODED_RESPONSE_HEADERS = {lambda_constants.RequestHeaders.CONTENT_TYPE: lambda_constants.ContentTypes.APPLICATION_JSON, lambda_constants.RequestHeaders.ACCESS_CONTROL_ALLOW_ORIGIN: '*', }
DEFAULT_RESPONSE_BODY = {lambda_constants.EventKeys.RESPONSE_MESSAGE: "", lambda_constants.EventKeys.USER_STATUS: -1, }


class HTTPInvokedLambdaFunctionHandler(LambdaHandler):
    def __init__(self, name=None, default_response_body=None, request_query_string_parameters_structure=None, request_body_structure=None):
        LambdaHandler.__init__(self, name=name, default_response={lambda_constants.EventKeys.STATUS_CODE: lambda_constants.StatusCodes.OK, lambda_constants.EventKeys.HEADER_PARAMETERS: HARD_CODED_RESPONSE_HEADERS, lambda_constants.EventKeys.BODY: DEFAULT_RESPONSE_BODY, },
            event_structure={lambda_constants.EventKeys.QUERY_STRING_PARAMETERS: request_query_string_parameters_structure or {}, lambda_constants.EventKeys.BODY: request_body_structure or {}})

        self.__default_response_body = default_response_body or {}
        self._set_response_attribute([lambda_constants.EventKeys.BODY], self.__default_response_body)

        self._request_query_string_params = {}
        self._request_headers = {}
        self._request_body = {}

    def _prepare_final_response(self, response):
        response = LambdaHandler._prepare_final_response(self, response)

        if self._stage in ['dev']:
            response[lambda_constants.EventKeys.BODY]['error'] = str(self._execution_exception)

        response[lambda_constants.EventKeys.HEADER_PARAMETERS].update(HARD_CODED_RESPONSE_HEADERS)

        valid_body = DEFAULT_RESPONSE_BODY
        valid_body.update(self.__default_response_body)

        raw_response_body = dictionary_utils.ensure_dict(response.get(lambda_constants.EventKeys.BODY, {}))
        if isinstance(raw_response_body, dict):
            valid_body.update(raw_response_body)

        valid_body = dictionary_utils.ensure_serializable(valid_body)
        response[lambda_constants.EventKeys.BODY] = json.dumps(valid_body)

        return response

    def _handle_event(self):
        LambdaHandler._handle_event(self)
        self._load_request_query_string_params()
        self._load_request_headers()
        self._load_request_body()

    def _load_request_query_string_params(self):
        event = LambdaHandler._get_request_event(self)
        self._request_query_string_params = event.get(lambda_constants.EventKeys.QUERY_STRING_PARAMETERS) or {}

    def _load_request_headers(self):
        event = LambdaHandler._get_request_event(self)
        self._request_headers = event.get(lambda_constants.EventKeys.HEADER_PARAMETERS) or {}

    def _load_request_body(self):
        event = LambdaHandler._get_request_event(self)
        self._request_body = event.get(lambda_constants.EventKeys.BODY) or {}

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, lambda_base_exceptions.InvalidEventLambdaException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], lambda_constants.ResponseMessages.POORLY_PROVIDED_PARAMETERS)
            return

        self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.INTERNAL_SERVER_ERROR)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], lambda_constants.ResponseMessages.INTERNAL_SERVER_ERROR)

        LambdaHandler._handle_exception(self, exception)

    def _successful_execution(self):
        LambdaHandler._successful_execution(self)
        self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.OK)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], lambda_constants.ResponseMessages.OPERATION_EXECUTED_SUCCESSFULLY)
