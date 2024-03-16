from src.handlers.case_file_processing.pipeline_steps.text_extraction_start._submit_text_extraction_job import submit_text_extraction_job
from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class TextExtractionStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'text_extraction', 'status'], 'in_progress')
        text_extraction_job_ids = submit_text_extraction_job(self.__file_instance, stage=self._stage)
        assert not any([job_id is None for job_id in text_extraction_job_ids])
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'text_extraction', 'job_ids'], text_extraction_job_ids)
        self.__invalidate_next_steps()
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['text_extraction_submission_failed'], 'true')
        MasslawStepFunctionCaseFilePipelineNodeHandler._handle_exception(self, exception)

    def _successful_execution(self):
        self.__file_instance.save_data()

    def __invalidate_next_steps(self):
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'text_indexing', 'valid'], 'false')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'knowledge_extraction', 'valid'], 'false')


def handler(event, context):
    handler_instance = TextExtractionStart()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
