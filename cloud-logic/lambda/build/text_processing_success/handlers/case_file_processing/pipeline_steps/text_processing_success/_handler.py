from text_processing_success.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from text_processing_success.modules.masslaw_cases_objects import MasslawCaseFileInstance


class TextProcessingSuccess(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'TextProcessing', 'status'], 'Done')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextProcessing', 'valid'], 'true')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


handler = TextProcessingSuccess()
