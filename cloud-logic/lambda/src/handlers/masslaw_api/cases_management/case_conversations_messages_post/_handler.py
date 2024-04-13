from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_conversation_action_handler import MasslawCaseManagementApiConversationActionHandler
from src.modules.masslaw_case_conversations import MasslawCaseConversationsManager
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.text_embeddings import generate_text_embeddings_suitable_for_masslaw_system


class PostCaseConversationMessage(MasslawCaseManagementApiConversationActionHandler):

    def __init__(self):
        MasslawCaseManagementApiConversationActionHandler.__init__(self, request_body_structure={'prompt': [str]}, default_response_body={'content': {}})

    def _load_request_body(self):
        MasslawCaseManagementApiConversationActionHandler._load_request_body(self)
        self._prompt = self._request_body.get('prompt', '')

    def _execute(self):
        MasslawCaseManagementApiConversationActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_conversations_manager = MasslawCaseConversationsManager(case_instance=self._case_instance)
        context = self._obtain_context_for_message()
        new_conversation_content = case_conversations_manager.send_message_to_conversation_as_user(user_id, self._conversation_id, self._prompt, context)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'content'], new_conversation_content)

    def _obtain_context_for_message(self):
        embeddings_vector = generate_text_embeddings_suitable_for_masslaw_system(self._prompt)
        user_id = self._caller_user_instance.get_user_id()
        case_user_access = MasslawCaseUserAccessManager(case_instance=self._case_instance)
        user_access_files = case_user_access.get_user_accessible_files(user_id)
        case_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, f'{self._case_id}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}')
        result = case_index_manager.execute_query({"query": {"bool": {"must": [{"knn": {"embedding": {"vector": embeddings_vector, "k": 10}}}, {"terms": {"file_id": user_access_files}}, ]}}, "sort": [{"_score": {"order": "desc"}}], "_source": ["name", "text", "file_id"]})
        self._log(f"Search result:\n{result}")
        context = ''
        for hit in result['hits']['hits']:
            file_id = hit['_source']['file_id']
            if file_id not in user_access_files: continue
            context += f"A paragraph from the file \"{hit['_source']['name']}\":\n\"{hit['_source']['text']}\""
        return context


def handler(event, context):
    handler_instance = PostCaseConversationMessage()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
