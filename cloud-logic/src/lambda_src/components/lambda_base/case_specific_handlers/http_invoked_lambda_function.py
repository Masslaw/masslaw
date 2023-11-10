import json
from ...lambda_base.lambda_function import *
from ...networking.networking_consts import *

HARD_CODED_RESPONSE_HEADERS = {
    RequestHeaders.CONTENT_TYPE: ContentTypes.APPLICATION_JSON,
    RequestHeaders.ACCESS_CONTROL_ALLOW_ORIGIN: '*',
}
DEFAULT_RESPONSE_BODY = {
    EventKeys.RESPONSE_MESSAGE: "",
    EventKeys.USER_STATUS: -1,
}


class HTTPInvokedLambdaFunction(LambdaFunction):
    def __init__(
            self,
            name=None,
            default_response_body=None,
            request_query_string_parameters_structure=None,
            request_body_structure=None
    ):
        LambdaFunction.__init__(
            self,
            name=name,
            default_response={
                EventKeys.STATUS_CODE: StatusCodes.OK,
                EventKeys.HEADER_PARAMETERS: HARD_CODED_RESPONSE_HEADERS,
                EventKeys.BODY: DEFAULT_RESPONSE_BODY,
            },
            event_structure={
                EventKeys.QUERY_STRING_PARAMETERS: request_query_string_parameters_structure or {},
                EventKeys.BODY: request_body_structure or {}
            }
        )

        self.__default_response_body = default_response_body or {}
        self._set_response_attribute([EventKeys.BODY], self.__default_response_body)

        self._request_query_string_params = {}
        self._request_headers = {}
        self._request_body = {}

    def _prepare_final_response(self, response):
        response = LambdaFunction._prepare_final_response(self, response)

        if self._stage in ['dev']:
            response[EventKeys.BODY]['error'] = str(self._execution_exception)

        response[EventKeys.HEADER_PARAMETERS].update(HARD_CODED_RESPONSE_HEADERS)

        valid_body = DEFAULT_RESPONSE_BODY
        valid_body.update(self.__default_response_body)

        raw_response_body = json_utils.ensure_dict(response.get(EventKeys.BODY, {}))
        if isinstance(raw_response_body, dict):
            valid_body.update(raw_response_body)

        valid_body = json_utils.ensure_serializable(valid_body)
        response[EventKeys.BODY] = json.dumps(valid_body)

        return response

    def _handle_event(self):
        LambdaFunction._handle_event(self)
        self._load_request_query_string_params()
        self._load_request_headers()
        self._load_request_body()

    def _load_request_query_string_params(self):
        event = LambdaFunction._get_request_event(self)
        self._request_query_string_params = event.get(EventKeys.QUERY_STRING_PARAMETERS) or {}

    def _load_request_headers(self):
        event = LambdaFunction._get_request_event(self)
        self._request_headers = event.get(EventKeys.HEADER_PARAMETERS) or {}

    def _load_request_body(self):
        event = LambdaFunction._get_request_event(self)
        self._request_body = event.get(EventKeys.BODY) or {}

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, InvalidEventLambdaException):
            self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.BAD_REQUEST)
            self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE], ResponseMessages.POORLY_PROVIDED_PARAMETERS)
            return

        self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.INTERNAL_SERVER_ERROR)
        self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE], ResponseMessages.INTERNAL_SERVER_ERROR)

        LambdaFunction._handle_exception(self, exception)

    def _successful_execution(self):
        LambdaFunction._successful_execution(self)
        self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.OK)
        self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE],
                                     ResponseMessages.OPERATION_EXECUTED_SUCCESSFULLY)
