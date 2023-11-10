from lambda_src.components.S3_manager.bucket_manager import *
from lambda_src.components.masslaw_case_file_processing_pipeline_manager.lambda_templates.masslaw_step_functions_case_file_pipeline_node_handler import *
from lambda_src.components.masslaw_cases.config.opensearch_config import *
from lambda_src.components.masslaw_cases.management.masslaw_case_file_text_utils import load_case_file_text
from lambda_src.components.masslaw_cases.masslaw_data_instances.masslaw_case_file_instance import *
from lambda_src.components.opensearch_manager.index_manager import *


class SubmitToSearchIndex(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):

        self.__file_instance = MasslawCaseFileInstance(self._file_id)

        self.__file_instance.set_data_property(['processing', 'stage_information', 'TextIndexing', 'status'], 'InProgress')
        
        self.__load_file_text()
        self.__submit_to_opensearch_index()

        self.__file_instance.set_data_property(['processing', 'stage_information', 'TextIndexing', 'status'], 'Done')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextIndexing', 'valid'], 'true')

        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self.__file_instance.save_data()
        self._set_response_attribute(['search_index_submission_failed'], 'true')

    def _successful_execution(self):
        self.__file_instance.save_data()

    def __load_file_text(self):
        self.__file_text = load_case_file_text(self._file_id)

    def __submit_to_opensearch_index(self):
        case_id = self.__file_instance.get_data_property(['case_id'])
        open_search_index_name = f'{case_id}{MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.ensure_exists()
        case_search_index_manager.add_document(self._file_id, self.__get_file_submit_document())

    def __get_file_submit_document(self):
        document = {
            'text': self.__file_text,
            'file_id': self.__file_instance.get_data_property(['file_id']),
            'name': self.__file_instance.get_data_property(['name']),
            'type': self.__file_instance.get_data_property(['type']),
            'languages': self.__file_instance.get_data_property(['languages']),
            'case_id': self.__file_instance.get_data_property(['case_id']),
        }
        return document


handler = SubmitToSearchIndex()
