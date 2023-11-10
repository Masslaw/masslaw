from ...lambda_base.lambda_function import *


class StepFunctionLambdaNodeHandler(LambdaFunction):

    def _handle_event(self):
        LambdaFunction._handle_event(self)
        self._set_response_attribute([], LambdaFunction._get_request_event(self))

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['exceptions', self.__class__.__name__],
                                     f'{exception} --- {traceback.format_exc()}')
        LambdaFunction._handle_exception(self, exception)
