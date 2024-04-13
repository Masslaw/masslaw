from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked import HTTPInvokedLambdaFunctionHandler
from src.modules.masslaw_users_config import opensearch_config


class SearchUsers(HTTPInvokedLambdaFunctionHandler):
    def __init__(self):
        HTTPInvokedLambdaFunctionHandler.__init__(
            self, 
            default_response_body={'results': []}, 
            request_query_string_parameters_structure={'search_query': [str]}
        )
        self.__search_query = ''

    def _load_request_query_string_params(self):
        HTTPInvokedLambdaFunctionHandler._load_request_query_string_params(self)
        self.__search_query = self._request_query_string_params.get('search_query')

    def _execute(self):
        HTTPInvokedLambdaFunctionHandler._execute(self)
        payload = self.construct_query_payload()
        users_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_USERS_OPENSEARCH_ENDPOINT, opensearch_config.MASSLAW_USERS_OPENSEARCH_INDEX_NAME)
        users_index_manager.ensure_exists({})
        result = users_index_manager.execute_query(payload)
        self._log(f"Search result:\n{result}")
        result_items = [hit.get('_source', {})|{'score': hit.get('_score', 0)} for hit in result['hits']['hits']]
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'results'], result_items)

    def construct_query_payload(self) -> dict:
        return {
            "query": {
                "multi_match": {
                    "query": self.__search_query,
                    "fields": ["email", "first_name", "last_name"],
                    "fuzziness" : "AUTO",
                }
            },
            "sort": [
                {"_score": {"order": "desc"}}
            ],
            "_source": ["User_ID", "email", "first_name", "last_name"],
        }


def handler(event, context):
    handler_instance = SearchUsers()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
