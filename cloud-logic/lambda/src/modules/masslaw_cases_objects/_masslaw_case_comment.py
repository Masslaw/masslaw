import time

from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.masslaw_cases_config import comments_config
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cases_objects._exceptions import MasslawCaseCommentDataUpdateException
from src.modules.remote_data_management_dynamodb import DynamodbDataHolder


class MasslawCaseCommentInstance(DynamodbDataHolder):
    def __init__(self, comment_id: str):
        DynamodbDataHolder.__init__(self, "MasslawCaseComments", comment_id)

    def get_file_id(self):
        return DynamodbDataHolder.get_item_id(self)

    def save_data(self):
        self.update_last_updated_time()
        if {'marked_text', 'comment_text'} & set(self._updated_attributes):
            self.__update_opensearch_document()
        self.__ensure_self_in_file()
        DynamodbDataHolder.save_data(self)

    def update_last_updated_time(self):
        self.set_data_property(['last_modified'], str(int(time.time())))

    def _assert_valid_data(self):
        DynamodbDataHolder._assert_valid_data(self)

        owner = self.get_data_property(['owner'], '')
        if len(owner) < 1: raise MasslawCaseCommentDataUpdateException('invalid owner')

        file_id = self.get_data_property(['file_id'], '')
        if len(file_id) < 1: raise MasslawCaseCommentDataUpdateException('invalid file id')

        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        if not case_file_instance.is_valid(): raise MasslawCaseCommentDataUpdateException('invalid file id')

        from_char = int(self.get_data_property(['from_char'], 0))
        to_char = int(self.get_data_property(['to_char'], 0))
        if not to_char >= from_char > -1: raise MasslawCaseCommentDataUpdateException('invalid char range')

        from_page = int(self.get_data_property(['from_page'], 0))
        to_page = int(self.get_data_property(['to_page'], 0))
        if not to_page >= from_page > -1: raise MasslawCaseCommentDataUpdateException('invalid page indices')

        comment_text = self.get_data_property(['comment_text'], '')
        if len(comment_text) > comments_config.COMMENT_TEXT_LENGTH_HARD_LIMIT:
            raise MasslawCaseCommentDataUpdateException(F'invalid comment text length. Passed the hard limit of {comments_config.COMMENT_TEXT_LENGTH_HARD_LIMIT} characters')

        marked_text = self.get_data_property(['marked_text'], '')
        if len(marked_text) > comments_config.COMMENT_MARKING_LENGTH_HARD_LIMIT:
            raise MasslawCaseCommentDataUpdateException(F'invalid comment marking length. Passed the hard limit of {comments_config.COMMENT_MARKING_LENGTH_HARD_LIMIT} characters')

        color = self.get_data_property(['color'], '')
        if (color[0] != '#') or (len(color) != 7):
            raise MasslawCaseCommentDataUpdateException('invalid color provided. Please use hex formatted color codes. example: #f6f6f6')

    def __update_opensearch_document(self):
        comment_id = self.get_item_id()
        comment_text = self.get_data_property(['comment_text'])
        marked_text = self.get_data_property(['marked_text'])
        file_id = self.get_data_property(['file_id'])
        case_id = self.get_data_property(['case_id'])
        owner = self.get_data_property(['comments'])
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_COMMENTS_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.ensure_exists()
        case_search_index_manager.add_document(comment_id, {
            'id': comment_id,
            'comment_text': comment_text,
            'marked_text': marked_text,
            'file_id': file_id,
            'case_id': case_id,
            'owner': owner
        })

    def __ensure_self_in_file(self):
        comment_id = self.get_item_id()
        file_id = self.get_data_property(['file_id'], '')
        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        case_file_comments = case_file_instance.get_data_property(['comments'], [])
        if not comment_id in case_file_comments: case_file_comments.append(comment_id)
        case_file_instance.set_data_property(['comments'], case_file_comments)
        case_file_instance.save_data()

    def delete(self):
        case_id = self.get_data_property(['case_id'])
        open_search_index_name = f'{case_id}{opensearch_config.MASSLAW_CASE_COMMENTS_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.remove_document(self.get_item_id())
        comment_id = self.get_item_id()
        file_id = self.get_data_property(['file_id'], '')
        case_file_instance = MasslawCaseFileInstance(file_id=file_id)
        case_file_comments = case_file_instance.get_data_property(['comments'], [])
        if comment_id in case_file_comments: case_file_comments.remove(comment_id)
        case_file_instance.set_data_property(['comments'], case_file_comments)
        case_file_instance.save_data()
