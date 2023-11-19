import secrets

from delete_case_file_annotation.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from delete_case_file_annotation.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from delete_case_file_annotation.modules.masslaw_cases_config import access_config
from delete_case_file_annotation.modules.masslaw_cases_objects import MasslawCaseFileAnnotationInstance
from delete_case_file_annotation.modules.masslaw_cases_objects import MasslawCaseInstance


class MasslawCaseAnnotationUnauthorizedAccessException(Exception): pass


class MasslawCaseAnnotationsManager:

    def __init__(self, case_instance: MasslawCaseInstance):
        self.__case_instance = case_instance

        self.__case_user_access_manager = MasslawCaseUserAccessManager(self.__case_instance)

    def put_annotation(self, user_id, file_id, annotation_type, beginning_character, ending_character, annotation_text, annotated_text, color, annotation_id=None):
        if not annotation_id:
            while True:
                annotation_id = secrets.token_hex(16)
                case_annotation_instance = MasslawCaseFileAnnotationInstance(annotation_id)
                if not case_annotation_instance.is_valid(): break
        else:
            case_annotation_instance = MasslawCaseFileAnnotationInstance(annotation_id)
            if not case_annotation_instance.is_valid(): return

        if beginning_character > ending_character:
            (beginning_character, ending_character) = (ending_character, beginning_character)

        self.assert_user_annotation_access(case_annotation_instance, user_id, file_id)

        case_annotation_instance.set_data_property(['type'], annotation_type)
        case_annotation_instance.set_data_property(['creator'], user_id)
        case_annotation_instance.set_data_property(['file_id'], file_id)
        case_annotation_instance.set_data_property(['case_id'], self.__case_instance.get_case_id())
        case_annotation_instance.set_data_property(['from_char'], beginning_character)
        case_annotation_instance.set_data_property(['to_char'], ending_character)
        case_annotation_instance.set_data_property(['annotation_text'], annotation_text)
        case_annotation_instance.set_data_property(['annotated_text'], annotated_text)
        case_annotation_instance.set_data_property(['color'], color)

        case_annotation_instance.save_data()

    def delete_annotation(self, annotation_id, user_id=None):
        case_annotation_instance = MasslawCaseFileAnnotationInstance(annotation_id)

        if user_id:
            self.assert_user_annotation_access(case_annotation_instance, user_id)

        if not case_annotation_instance.is_valid(): return

        case_annotation_instance.delete()

    def assert_user_annotation_access(self, case_annotation_instance: MasslawCaseFileAnnotationInstance, user_id, file_id=None):
        file_id = file_id or case_annotation_instance.get_data_property(['file_id'])

        if case_annotation_instance.get_data_property(['creator'], user_id) != user_id:
            raise MasslawCaseAnnotationUnauthorizedAccessException('Attempting to edit an annotation that was created by another user')

        user_access_files = self.__case_user_access_manager.get_user_access_files(user_id)
        if file_id not in user_access_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException('Attempting to edit an annotation in a file the user has no access to')

        user_access_level = self.__case_user_access_manager.get_user_access_level_name(user_id)
        if user_access_level in (access_config.CaseAccessEntities.READER_CLIENT):
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException('Attempting to edit an annotation in a file the user has no write access to')
