from src.modules.lambda_handler_template_masslaw_api_case_file_action_handler import MasslawCaseManagementApiFileActionHandler
from src.modules.masslaw_case_storage_management import MasslawCaseStorageManager


class DeleteCaseFile(MasslawCaseManagementApiFileActionHandler):

    def _execute(self):
        MasslawCaseManagementApiFileActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_storage_manager = MasslawCaseStorageManager(case_instance=self._case_instance)
        case_storage_manager.delete_file_as_user(file_id=self._file_id, user_id=user_id)
        self._case_instance.save_data()


def handler(event, context):
    handler_instance = DeleteCaseFile()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
