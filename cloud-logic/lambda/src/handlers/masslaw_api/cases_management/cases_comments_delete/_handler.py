from src.modules.lambda_handler_template_masslaw_api_case_comment_action_handler import MasslawCaseManagementApiCaseCommentActionHandler
from src.modules.masslaw_case_comments_management import MasslawCaseCommentsManager


class DeleteCaseComment(MasslawCaseManagementApiCaseCommentActionHandler):

    def _execute(self):
        MasslawCaseManagementApiCaseCommentActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_comments_manager = MasslawCaseCommentsManager(case_instance=self._case_instance)
        case_comments_manager.delete_comment(self._comment_id, user_id)


def handler(event, context):
    handler_instance = DeleteCaseComment()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
