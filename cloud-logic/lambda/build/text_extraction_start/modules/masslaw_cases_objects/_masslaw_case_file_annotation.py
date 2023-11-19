import time

from text_extraction_start.modules.aws_clients.open_search_client import OpenSearchIndexManager
from text_extraction_start.modules.masslaw_cases_config import annotations_config
from text_extraction_start.modules.masslaw_cases_config import opensearch_config
from text_extraction_start.modules.masslaw_cases_objects import MasslawCaseFileInstance
from text_extraction_start.modules.masslaw_cases_objects._exceptions import MasslawCaseFileAnnotationDataUpdateException
from text_extraction_start.modules.remote_data_management_dynamodb import DynamodbDataHolder


class MasslawCaseFileAnnotationInstance(DynamodbDataHolder):
    def __init__(self, annotation_id: str):
        DynamodbDataHolder.__init__(self, "MasslawFileAnnotations", annotation_id)

    def get_file_id(self):
        return DynamodbDataHolder.get_item_id(self)

    def save_data(self):
        self.update_last_updated_time()
        if 'annotated_text' in self._updated_attributes:
            self.__update_opensearch_document()
        self.__ensure_self_in_file()
        DynamodbDataHolder.save_data(self)

    def update_last_updated_time(self):
        self.set_data_property(['last_modified'], str(int(time.time())))

    def _assert_valid_data(self):
        DynamodbDataHolder._assert_valid_data(self)

        type = self.get_data_property(['type'], '')
        if type not in ['highlight', 'sticky_note']:
            raise MasslawCaseFileAnnotationDataUpdateException('invalid type')

        creator = self.get_data_property(['creator'], '')
        if len(creator) < 1:
            raise MasslawCaseFileAnnotationDataUpdateException('invalid creator')

        file_id = self.get_data_property(['file_id'], '')
        if len(file_id) < 1:
            raise MasslawCaseFileAnnotationDataUpdateException('invalid file id')
        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        if not case_file_instance.is_valid():
            raise MasslawCaseFileAnnotationDataUpdateException('invalid file id')

        from_char = int(self.get_data_property(['from_char'], -1))
        to_char = int(self.get_data_property(['to_char'], -1))
        if not to_char >= from_char > -1:
            raise MasslawCaseFileAnnotationDataUpdateException('invalid char range')
        if abs(to_char - from_char) > annotations_config.ANNOTATION_LENGTH_HARD_LIMIT:
            raise MasslawCaseFileAnnotationDataUpdateException(F'invalid annotated text length. Passed the hard limit of {annotations_config.ANNOTATION_LENGTH_HARD_LIMIT} characters')

        text = self.get_data_property(['text'], '')
        if len(text) > annotations_config.ANNOTATION_TEXT_LENGTH_HARD_LIMIT:
            raise MasslawCaseFileAnnotationDataUpdateException(F'invalid annotation text length. Passed the hard limit of {annotations_config.ANNOTATION_TEXT_LENGTH_HARD_LIMIT} characters')

        color = self.get_data_property(['color'], '')
        if (color[0] != '#') or (len(color) != 7):
            raise MasslawCaseFileAnnotationDataUpdateException('invalid color provided. Please use hex formatted '
                                                               'color codes. example: #f6f6f6')

    def __update_opensearch_document(self):
        annotated_text = self.get_data_property(['annotated_text'])
        file_id = self.get_data_property(['file_id'])
        case_id = self.get_data_property(['case_id'])
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_ANNOTATIONS_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.ensure_exists()
        case_search_index_manager.add_document(self.get_item_id(), {
                'text': self.get_data_property(['text']),
                'annotated_text': annotated_text,
                'file_id': file_id,
                'case_id': case_id,
                'type': self.get_data_property(['type']),
            })

    def __ensure_self_in_file(self):
        annotation_id = self.get_item_id()
        file_id = self.get_data_property(['file_id'], '')
        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        case_file_annotations = case_file_instance.get_data_property(['annotations'], [])
        if not annotation_id in case_file_annotations:
            case_file_annotations.append(annotation_id)
        case_file_instance.set_data_property(['annotations'], case_file_annotations)
        case_file_instance.save_data()

    def delete(self):
        case_id = self.get_data_property(['case_id'])
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_ANNOTATIONS_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.remove_document(self.get_item_id())

        annotation_id = self.get_item_id()
        file_id = self.get_data_property(['file_id'], '')
        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        case_file_annotations = case_file_instance.get_data_property(['annotations'], [])
        if annotation_id in case_file_annotations:
            case_file_annotations.remove(annotation_id)
        case_file_instance.set_data_property(['annotations'], case_file_annotations)
        case_file_instance.save_data()
