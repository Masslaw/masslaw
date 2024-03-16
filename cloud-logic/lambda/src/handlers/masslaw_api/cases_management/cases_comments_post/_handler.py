from src.modules.lambda_handler_template_masslaw_api_case_comment_action_handler import MasslawCaseManagementApiCaseCommentActionHandler
from src.modules.masslaw_case_comments_management import MasslawCaseCommentsManager


class GetCaseComment(MasslawCaseManagementApiCaseCommentActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseCommentActionHandler.__init__(self, request_body_structure={'comment_text': [str, None], 'color': [str, None]})
        self.__comment_text = None
        self.__color = None

    def _load_request_body(self):
        MasslawCaseManagementApiCaseCommentActionHandler._load_request_body(self)
        self.__comment_text = self._request_body.get('comment_text')
        self.__color = self._request_body.get('color')

    def _execute(self):
        MasslawCaseManagementApiCaseCommentActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_comments_manager = MasslawCaseCommentsManager(case_instance=self._case_instance)
        self._log(f"waaa {self._comment_instance.get_data_property([])}")
        case_comments_manager.update_comment(user_id, self._comment_id, comment_text=self.__comment_text, color=self.__color)


def handler(event, context):
    handler_instance = GetCaseComment()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
