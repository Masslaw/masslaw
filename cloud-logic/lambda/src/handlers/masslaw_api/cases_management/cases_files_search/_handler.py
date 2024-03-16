from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import opensearch_config


class SearchCaseFiles(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self, 
            default_response_body={'results': []}, 
            request_query_string_parameters_structure={'search_query': [str], 'files': [str, None], 'highlight_padding': [str, int, None], }
        )
        self.__search_query = ''
        self.__highlight_padding = 0
        self.__files = None

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_query_string_params(self)
        self.__search_query = self._request_query_string_params.get('search_query')
        self.__highlight_padding = self._request_query_string_params.get('highlight_padding', 100)
        if isinstance(self.__highlight_padding, str): self.__highlight_padding = int(self.__highlight_padding)
        if _files := self._request_query_string_params.get('files', ''): self.__files = _files.split('&')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_user_access = MasslawCaseUserAccessManager(case_instance=self._case_instance)
        user_access_files = case_user_access.get_user_access_files(user_id)
        self.__search_files = list(set(self.__files or user_access_files) & set(user_access_files))
        payload = self.construct_query_payload()
        case_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, f'{self._case_id}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}')
        result = case_index_manager.execute_query(payload)
        self._log(f"Search result:\n{result}")
        result_items = []
        for hit in result['hits']['hits']:
            file_id = hit['_source']['file_id']
            if file_id not in user_access_files: continue
            result_items.append({
                'file_id': file_id,
                'file_name': hit['_source']['name'],
                'text_highlights': hit['highlight']['text'],
                'score': hit['_score']
            })
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'results'], result_items)

    def construct_query_payload(self) -> dict:
        field = "text"
        return {
            "query": {
                "bool": {
                    "must": [{
                        "match_phrase": {
                            field: {
                                "query": self.__search_query,
                                "slop": "1"
                            }
                        }
                    },
                        {
                            "terms": {
                                "_id": self.__search_files
                            }
                        }
                    ]
                }

            },
            "sort": [
                {"_score": {"order": "desc"}}
            ],
            "_source": ["file_id", "name"],
            "highlight": {
                "fields": {
                    field: {
                        "number_of_fragments": 0,
                        "fragment_size": self.__highlight_padding
                    }
                },
                "pre_tags": ["<search_result>"],
                "post_tags": ["</search_result>"]
            },
        }


def handler(event, context):
    handler_instance = SearchCaseFiles()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
