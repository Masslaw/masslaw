from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.lambda_handler_template_step_functions_lambda_node_case_file_pipiline import MasslawStepFunctionCaseFilePipelineNodeHandler
from src.modules.masslaw_case_file_text_handling import load_case_file_text_structure
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.text_embeddings import generate_text_embeddings_suitable_for_masslaw_system

PARAGRAPH_MINIMUM_TEXT_LENGTH = 300


class SubmitToSearchIndex(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):
        self.__file_instance = MasslawCaseFileInstance(self._file_id)
        self.__file_instance.set_data_property(['processing', 'stage_information', 'text_indexing', 'status'], 'in_progress')
        self.__load_file_text()
        self.__submit_to_opensearch_index()
        self.__file_instance.set_data_property(['processing', 'stage_information', 'text_indexing', 'status'], 'done')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'text_indexing', 'valid'], 'true')
        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _handle_exception(self, exception: Exception):
        self.__file_instance.save_data()
        self._set_response_attribute(['search_index_submission_failed'], 'true')

    def _successful_execution(self):
        self.__file_instance.save_data()

    def __load_file_text(self):
        self.__file_text_structure = load_case_file_text_structure(self._file_id)

    def __submit_to_opensearch_index(self):
        case_id = self.__file_instance.get_data_property(['case_id'])
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.ensure_exists(opensearch_config.MASSLAW_CASE_TEXT_INDEX_CREATION_CONFIGURATION)
        self.__generate_documents_for_file_paragraphs()
        for idx, document in enumerate(self.__documents): case_search_index_manager.add_document(f'{self._file_id}-{idx}', document)

    def __generate_documents_for_file_paragraphs(self):
        document_general_data = {'text': '', 'file_id': self.__file_instance.get_data_property(['file_id']), 'name': self.__file_instance.get_data_property(['name']), 'case_id': self.__file_instance.get_data_property(['case_id'])}
        self.__documents = []
        current_document = {}
        for child in self.__file_text_structure.iter():
            if child.tag == 'pr':
                if len(current_document.get('text', '')) < PARAGRAPH_MINIMUM_TEXT_LENGTH: continue
                if index := current_document.get('par_idx', -1) >= 0:
                    embeddings_vector = generate_text_embeddings_suitable_for_masslaw_system(str(current_document['text']))
                    current_document['embedding'] = embeddings_vector
                    self.__documents.append(current_document)
                current_document = {"par_idx": index + 1, **document_general_data}
            if child.tag == 'wd': current_document['text'] = current_document.get('text', '') + ' '
            if child.tag == 'cr': current_document['text'] = current_document.get('text', '') + child.text
        embeddings_vector = generate_text_embeddings_suitable_for_masslaw_system(str(current_document['text']))
        current_document['embedding'] = embeddings_vector
        self.__documents.append(current_document)
        self._log(f'Generated the following paragraphs for the provided document: {self.__documents}')


def handler(event, context):
    handler_instance = SubmitToSearchIndex()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
