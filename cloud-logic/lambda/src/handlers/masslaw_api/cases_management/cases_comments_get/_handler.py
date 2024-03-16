from src.modules.lambda_handler_template_masslaw_api_case_comment_action_handler import MasslawCaseManagementApiCaseCommentActionHandler
from src.modules.masslaw_case_comments_management import MasslawCaseCommentsManager
from src.modules.masslaw_case_data_collection import MasslawCaseDataCollector
from src.modules.lambda_base import lambda_constants


class GetCaseComment(MasslawCaseManagementApiCaseCommentActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseCommentActionHandler.__init__(self, default_response_body={'comment': {}})

    def _execute(self):
        MasslawCaseManagementApiCaseCommentActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_comments_manager = MasslawCaseCommentsManager(case_instance=self._case_instance)
        case_comments_manager.assert_user_comment_access(self._comment_instance, user_id)
        data_collector = MasslawCaseDataCollector(case_instance=self._case_instance, access_user_id=user_id)
        comment_data = data_collector.get_case_comment_data(comment_id=self._comment_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'comment'], comment_data)


def handler(event, context):
    handler_instance = GetCaseComment()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
