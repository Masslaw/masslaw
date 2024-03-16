from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class CaseFilePipelineStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        if not self.__file_instance.is_valid():
            self._set_response_attribute(['invalid'], 'true')
            return
        rerun_processing = self._get_request_event().get('force_rerun', 'false')
        if rerun_processing in ("true", True):
            self.__file_instance.set_data_property(['processing'], None)  # reset the processing information of a file to have a full execution of the state machine (no skips)
        processing_in_progress = self.__file_instance.get_data_property(['processing', 'in_progress']) in ('true', True)
        if processing_in_progress:
            self._set_response_attribute(['invalid'], 'true')
            return
        self.__file_instance.set_data_property(['processing', 'stage_information', 'processing_file', 'status'], 'in_progress')
        self.__file_instance.set_data_property(['processing', 'in_progress'], 'true')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


def handler(event, context):
    handler_instance = CaseFilePipelineStart()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
