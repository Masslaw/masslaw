from typing import List

from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.aws_clients.open_search_client import OpensearchQuery
from src.modules.aws_clients.open_search_client import OpensearchQuerySortOrder
from src.modules.aws_clients.open_search_client import opensearch_inner_queries
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class SearchCaseFiles(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'results': []}, request_query_string_parameters_structure={'case_id': [str], 'search_query': [str], 'files': [str, None], 'highlight_padding': [str, int, None], })
        self.__case_id = ''
        self.__search_query = ''
        self.__highlight_padding = 0
        self.__files = None

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''
        self.__search_query = ''
        self.__highlight_padding = 0
        self.__files = None

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__search_query = self._request_query_string_params.get('search_query')
        self.__highlight_padding = self._request_query_string_params.get('highlight_padding', 100)
        if isinstance(self.__highlight_padding, str): self.__highlight_padding = int(self.__highlight_padding)
        if _files := self._request_query_string_params.get('files', ''): self.__files = _files.split('|')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(self.__case_id)
        case_user_access = MasslawCaseUserAccessManager(case_instance=case_instance)
        user_access_files = case_user_access.get_user_access_files(user_id)
        search_files = list(set(self.__files or user_access_files) & set(user_access_files))
        query = self.construct_query(search_files)
        case_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, f'{self.__case_id}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}')
        result = case_index_manager.execute_query(query)
        self._log(f"Search result:\n{result}")
        result_items = []
        for hit in result['hits']['hits']:
            file_id = hit['_source']['file_id']
            if file_id not in user_access_files: continue
            result_items.append({'file_id': file_id, 'file_name': hit['_source']['name'], 'text_highlights': hit['highlight']['text']})
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'results'], result_items)

    def construct_query(self, search_files: List[str]) -> OpensearchQuery:
        query = OpensearchQuery()
        query.set_inner_query(opensearch_inner_queries.OpensearchMatchInnerQuery('text', self.__search_query))
        query.add_sorting('_score', OpensearchQuerySortOrder.desc)
        query.include_source_fields(['file_id', 'name'])
        query.set_documents(search_files)
        query.enable_highlight('text', self.__highlight_padding)
        return query


def handler(event, context):
    handler_instance = SearchCaseFiles()
    return handler_instance.call_handler(event, context)
