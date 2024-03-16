from src.modules.lambda_handler_template_masslaw_api_case_file_action_handler import MasslawCaseManagementApiFileActionHandler
from src.modules.masslaw_case_comments_management import MasslawCaseCommentsManager
from src.modules.masslaw_cases_objects import MasslawCaseInstance
from src.modules.lambda_base import lambda_constants


class PutCaseComment(MasslawCaseManagementApiFileActionHandler):
    def __init__(self):
        MasslawCaseManagementApiFileActionHandler.__init__(
            self, default_response_body={},
            request_body_structure={'marked_text': [str], 'from_char': [int, str], 'to_char': [int, str], 'from_page': [int, str], 'to_page': [int, str], 'color': [str]}
        )
        self.__marked_text = ''
        self.__from_char = -1
        self.__to_char = -1
        self.__from_page = -1
        self.__to_page = -1
        self.__color = ''

    def _load_request_body(self):
        MasslawCaseManagementApiFileActionHandler._load_request_body(self)
        self.__marked_text = self._request_body.get('marked_text')
        self.__from_char = self._request_body.get('from_char')
        self.__to_char = self._request_body.get('to_char')
        self.__from_page = self._request_body.get('from_page')
        self.__to_page = self._request_body.get('to_page')
        self.__color = self._request_body.get('color')

    def _execute(self):
        MasslawCaseManagementApiFileActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self._case_id)
        case_comments_manager = MasslawCaseCommentsManager(case_instance=case_instance)
        new_comment_instance = case_comments_manager.put_comment(
            user_id=user_id,
            file_id=self._file_id,
            beginning_character=self.__from_char,
            ending_character=self.__to_char,
            beginning_page=self.__from_page,
            ending_page=self.__to_page,
            marked_text=self.__marked_text,
            color=self.__color,
        )
        new_comment_data = new_comment_instance.get_data_copy() or {}
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'comment'], new_comment_data)


def handler(event, context):
    handler_instance = PutCaseComment()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
