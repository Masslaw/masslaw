from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class CaseFilePipelineStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        if not self.__file_instance.is_valid():
            self._set_response_attribute(['invalid'], 'true')
            return
        if self._execution_stage in ('dev', 'test'):
            self.__file_instance.set_data_property(['processing'], None)  # reset the processing information of a file to have a full execution of the state machine (no skips)
        processing_in_progress = self.__file_instance.get_data_property(['processing', 'in_progress']) in ('true', True)
        if processing_in_progress:
            self._set_response_attribute(['invalid'], 'true')
            return
        self.__file_instance.set_data_property(['processing', 'stage_information', 'ProcessingFile', 'status'], 'InProgress')
        self.__file_instance.set_data_property(['processing', 'in_progress'], 'true')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


handler = CaseFilePipelineStart()
