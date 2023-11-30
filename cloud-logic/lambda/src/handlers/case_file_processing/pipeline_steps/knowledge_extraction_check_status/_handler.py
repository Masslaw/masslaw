from src.modules.aws_clients.batch_client._batch_management import describe_jobs
from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


class KnowledgeExtractionCheckStatus(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        knowledge_extraction_job_ids = self.__file_instance.get_data_property(['processing', 'stage_metadata', 'knowledge_extraction', 'job_ids'], [])
        describe_jobs_response = describe_jobs(knowledge_extraction_job_ids)
        self._log(f"describe_jobs_response: {describe_jobs_response}")
        job_statuses = [job.get('status', '') for job in describe_jobs_response]
        self._log(f"job_statuses: {job_statuses}")
        if 'FAILED' in job_statuses:
            self.__file_instance.set_data_property(['processing', 'stage_information', 'knowledge_extraction', 'status'], 'failed')
        elif job_statuses.count('SUCCEEDED') == len(job_statuses):
            self.__file_instance.set_data_property(['processing', 'stage_information', 'knowledge_extraction', 'status'], 'succeeded')
        else:
            self.__file_instance.set_data_property(['processing', 'stage_information', 'knowledge_extraction', 'status'], 'in_progress')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())


handler = KnowledgeExtractionCheckStatus()
