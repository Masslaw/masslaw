from lambda_src.components.masslaw_case_file_processing_pipeline_manager.lambda_templates.masslaw_step_functions_case_file_pipeline_node_handler import *
from lambda_src.components.masslaw_case_file_processing_pipeline_manager.actions.submit_text_extraction_job import *


class TextExtractionStart(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):

        self.__file_instance = MasslawCaseFileInstance(self._file_id)

        self.__file_instance.set_data_property(['processing', 'stage_information', 'TextExtraction', 'status'], 'InProgress')

        text_extraction_job_id = submit_text_extraction_job(self.__file_instance, stage=self._stage)
        assert text_extraction_job_id

        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextExtraction', 'job_id'], text_extraction_job_id)
        self.__invalidate_next_steps()

        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self._set_response_attribute(['text_extraction_submission_failed'], 'true')
        MasslawStepFunctionCaseFilePipelineNodeHandler._handle_exception(self, exception)

    def _successful_execution(self):
        self.__file_instance.save_data()

    def __invalidate_next_steps(self):
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextIndexing', 'valid'], 'false')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextProcessing', 'valid'], 'false')


handler = TextExtractionStart()
