from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class KnowledgeExtractionStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'knowledge_extraction', 'status'], 'in_progress')
        knowledge_extraction_job_id = submit_knowledge_extraction_job(self.__file_instance, stage=self._stage)
        assert knowledge_extraction_job_id
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'knowledge_extraction', 'job_id'], knowledge_extraction_job_id)
        self.__invalidate_next_steps()
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['knowledge_extraction_submission_failed'], 'true')
        MasslawStepFunctionCaseFilePipelineNodeHandler._handle_exception(self, exception)

    def _successful_execution(self):
        self.__file_instance.save_data()

    def __invalidate_next_steps(self):
        ...


handler = KnowledgeExtractionStart()
