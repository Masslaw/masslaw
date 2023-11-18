from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_case_file_text_handling import load_case_file_text
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance


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
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.ensure_exists()
        case_search_index_manager.add_document(self._file_id, self.__get_file_submit_document())

    def __get_file_submit_document(self):
        document = {'text': self.__file_text, 'file_id': self.__file_instance.get_data_property(['file_id']), 'name': self.__file_instance.get_data_property(['name']), 'type': self.__file_instance.get_data_property(['type']), 'languages': self.__file_instance.get_data_property(['languages']),
                    'case_id': self.__file_instance.get_data_property(['case_id']), }
        return document


handler = SubmitToSearchIndex()
