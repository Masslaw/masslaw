from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class KnowledgeExtractionStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'knowledge_extraction', 'status'], 'InProgress')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['knnowledge_extraction_submission_failed'], 'true')

    def _successful_execution(self):
        self.__file_instance.save_data()


handler = KnowledgeExtractionStart()
