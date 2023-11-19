from case_file_pipeline_fail.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from case_file_pipeline_fail.modules.masslaw_cases_objects import MasslawCaseFileInstance


class CaseFilePipelineFail(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'ProcessingFile', 'status'], 'Failed')
        self.__file_instance.set_data_property(['processing', 'in_progress'], 'false')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


handler = CaseFilePipelineFail()
