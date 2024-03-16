from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class TextExtractionSuccess(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'text_extraction', 'status'], 'done')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'text_extraction', 'valid'], 'true')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


def handler(event, context):
    handler_instance = TextExtractionSuccess()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
