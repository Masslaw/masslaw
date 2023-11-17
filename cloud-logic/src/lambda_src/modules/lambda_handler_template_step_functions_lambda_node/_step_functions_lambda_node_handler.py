import traceback

from lambda_src.modules.lambda_base import LambdaHandler


class StepFunctionLambdaNodeHandler(LambdaHandler):

    def _handle_event(self):
        LambdaHandler._handle_event(self)
        self._set_response_attribute([], LambdaHandler._get_request_event(self))

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['exceptions', self.__class__.__name__], f'{exception} --- {traceback.format_exc()}')
        LambdaHandler._handle_exception(self, exception)
