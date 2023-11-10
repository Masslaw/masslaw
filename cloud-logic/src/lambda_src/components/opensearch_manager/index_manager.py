import http.client
import json
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


class OpenSearchRequestFailedException(Exception): pass
class OpenSearchInvalidQueryTypeException(ValueError): pass


class OpenSearchIndexManager:
    def __init__(self, endpoint_url, index_name, region='us-east-1'):
        self.endpoint_url = endpoint_url.replace('https://', '')
        self.region = region
        self.index_name = index_name
        self.session = boto3.Session()

    def ensure_exists(self):
        if not self.index_exists():
            self.create_index()

    def index_exists(self):
        try:
            self.__execute_request('HEAD', self.index_name)
            return True
        except OpenSearchRequestFailedException:
            return False

    def create_index(self):
        self.__execute_request('PUT', self.index_name)

    def add_document(self, document_id, document):
        url = self.index_name + f'/_doc/{document_id}'
        response = self.__execute_request('PUT', url, document)
        return json.loads(response.read())

    def get_document(self, document_id):
        try:
            url = self.index_name + f'/{document_id}'
            response = self.__execute_request('GET', url)
            return json.loads(response.read())
        except: return None

    def remove_document(self, document_id):
        if not self.index_exists(): return
        if not self.get_document(document_id): return
        url = self.index_name + f'/{document_id}'
        response = self.__execute_request('DELETE', url)
        return json.loads(response.read())

    def query(
            self,
            field,
            query,
            query_type="match",
            fuzziness="AUTO",
            include_source_fields=None,
            include_highlight=True,
            highlight_padding=50,
            entire_text_highlight=False,
            sort=None,
            documents=None,
    ):
        if query_type == "match":
            inner_query = {"match": {field: {"query": query, "fuzziness": fuzziness}}}
        elif query_type == "term":
            inner_query = {"term": {field: query}}
        elif query_type == "prefix":
            inner_query = {"prefix": {field: query}}
        elif query_type == "wildcard":
            inner_query = {"wildcard": {field: query}}
        else:
            raise OpenSearchInvalidQueryTypeException(f"Unsupported query_type: {query_type}")

        payload = {"query": {"bool": {"must": [inner_query]}}}

        if documents:
            payload["query"]["bool"]["must"].append({"terms": {"_id": documents}})

        if include_source_fields:
            payload["_source"] = include_source_fields

        if include_highlight:
            padding = 1000000 if entire_text_highlight else highlight_padding
            fragment_count = 0 if entire_text_highlight else 5  # 5 being the default fragment count.
            payload['highlight'] = {
                "fields": {
                    field: {
                        "fragment_size": padding,
                        "number_of_fragments": fragment_count
                    }
                },
                "pre_tags": ["<search_result>"],
                "post_tags": ["</search_result>"]
            }

        if sort:
            payload["sort"] = [{_sort_field: {"order": _sort_order}} for _sort_field, _sort_order in sort.items()]

        return self.__execute_query(payload)

    def __execute_query(self, payload):
        response = self.__execute_request('POST', self.index_name + "/_search", payload)
        return json.loads(response.read())

    def __execute_request(self, method, path, payload=None):
        request = self.__sign_request(method, path, payload)
        conn = http.client.HTTPSConnection(self.endpoint_url)
        conn.request(method, request.url, body=request.body,
                     headers=request.headers)  # Change 'request.path' to 'request.url'
        response = conn.getresponse()
        if response.status >= 400:
            raise OpenSearchRequestFailedException(
                f'Status: {response.status}, Reason: {response.reason}, Info: {response.read()}')
        return response

    def __sign_request(self, method, path, payload=None):
        service = 'es'
        credentials = self.session.get_credentials()
        headers = {'Host': self.endpoint_url, 'Content-Type': 'application/json'}
        request = AWSRequest(method=method, url=f"https://{self.endpoint_url}/{path}", data=json.dumps(payload or {}),
            headers=headers)
        SigV4Auth(credentials, service, self.region).add_auth(request)
        return request.prepare()
