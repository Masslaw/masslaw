from src.modules.lambda_handler_template_step_functions_lambda_node import StepFunctionLambdaNodeHandler


class MasslawStepFunctionCaseFilePipelineNodeHandler(StepFunctionLambdaNodeHandler):
    def __init__(self, name=None, default_response=None, event_structure=None, ):
        StepFunctionLambdaNodeHandler.__init__(self, name=name, default_response=default_response, event_structure=event_structure)
        self._file_id = ''
        self._execution_stage = ''

    def _handle_event(self):
        StepFunctionLambdaNodeHandler._handle_event(self)
        self._file_id = self._get_request_event().get('file_id')
        self._execution_stage = self._get_request_event().get('stage', 'prod')

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['success'], 'false')
        StepFunctionLambdaNodeHandler._handle_exception(self, exception)
