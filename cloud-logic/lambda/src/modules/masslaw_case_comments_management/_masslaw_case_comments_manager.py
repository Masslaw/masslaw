import secrets

from src.modules.masslaw_case_comments_management._exceptions import MasslawCaseCommentUnauthorizedAccessException
from src.modules.masslaw_case_comments_management._exceptions import MasslawInvalidCommentException
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_objects import MasslawCaseCommentInstance
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class MasslawCaseCommentsManager:

    def __init__(self, case_instance: MasslawCaseInstance = None):
        self.__case_instance = case_instance
        self.__case_user_access_manager = MasslawCaseUserAccessManager(self.__case_instance)

    def put_comment(self, user_id, file_id, beginning_character, ending_character, beginning_page, ending_page, marked_text, color):
        while True:
            comment_id = secrets.token_hex(16)
            case_comment_instance = MasslawCaseCommentInstance(comment_id)
            if not case_comment_instance.is_valid(): break

        user_access_files = self.__case_user_access_manager.get_user_accessible_files(user_id)
        if file_id not in user_access_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException('Attempting to put an comment in a file the user has no access to')

        case_id = self.__case_instance.get_case_id()

        if beginning_character > ending_character: (beginning_character, ending_character) = (ending_character, beginning_character)
        if beginning_page > ending_page: (beginning_page, ending_page) = (ending_page, beginning_page)

        case_comment_instance.set_data_property(['owner'], user_id)
        case_comment_instance.set_data_property(['file_id'], file_id)
        case_comment_instance.set_data_property(['case_id'], case_id)
        case_comment_instance.set_data_property(['from_char'], beginning_character)
        case_comment_instance.set_data_property(['to_char'], ending_character)
        case_comment_instance.set_data_property(['from_page'], beginning_page)
        case_comment_instance.set_data_property(['to_page'], ending_page)
        case_comment_instance.set_data_property(['comment_text'], '')
        case_comment_instance.set_data_property(['marked_text'], marked_text)
        case_comment_instance.set_data_property(['color'], color)

        case_comment_instance.save_data()

        return case_comment_instance

    def update_comment(self, user_id, comment_id, comment_text=None, color=None):
        case_comment_instance = MasslawCaseCommentInstance(comment_id)
        if not case_comment_instance.is_valid(): raise MasslawInvalidCommentException('Attempting to update a non-existing comment')
        self.assert_user_comment_access(case_comment_instance, user_id, write=True)
        if comment_text: case_comment_instance.set_data_property(['comment_text'], comment_text)
        if color: case_comment_instance.set_data_property(['color'], color)
        case_comment_instance.save_data()

    def delete_comment(self, comment_id, user_id=None):
        case_comment_instance = MasslawCaseCommentInstance(comment_id)
        if user_id: self.assert_user_comment_access(case_comment_instance, user_id, write=True)
        if not case_comment_instance.is_valid(): return
        case_comment_instance.delete()

    def assert_user_comment_access(self, case_comment_instance: MasslawCaseCommentInstance, user_id, file_id=None, write=False):
        comment_file_id = case_comment_instance.get_data_property(['file_id'])
        if file_id and file_id != comment_file_id: raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException('Attempting to edit an comment in a file the user has no access to')
        owner = case_comment_instance.get_data_property(['owner'])
        if write and owner != user_id: raise MasslawCaseCommentUnauthorizedAccessException('Attempting to edit an comment that was created by another user')
        user_access_files = self.__case_user_access_manager.get_user_accessible_files(user_id)
        if comment_file_id not in user_access_files: raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException('Attempting to edit an comment in a file the user has no access to')
