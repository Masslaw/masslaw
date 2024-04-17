import http.client
import json

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from src.modules.aws_clients.open_search_client._exceptions import OpenSearchRequestFailedException


class OpenSearchIndexManager:
    def __init__(self, endpoint_url, index_name, region='us-east-1'):
        self.endpoint_url = endpoint_url.replace('https://', '')
        self.region = region
        self.index_name = index_name
        self.session = boto3.Session()

    def ensure_exists(self, creation_configuration: dict = None):
        try:
            if not self.index_exists(): self.create_index(creation_configuration or {})
        except OpenSearchRequestFailedException:
            pass

    def index_exists(self):
        try:
            self.__execute_request('HEAD', self.index_name)
            return True
        except OpenSearchRequestFailedException:
            return False

    def create_index(self, creation_configuration: dict = None):
        self.__execute_request('PUT', self.index_name, creation_configuration or {})

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

    def execute_query(self, payload):
        response = self.__execute_request('POST', self.index_name + "/_search", payload)
        return json.loads(response.read())

    def __execute_request(self, method, path, payload=None):
        request = self.__sign_request(method, path, payload)
        conn = http.client.HTTPSConnection(self.endpoint_url)
        conn.request(method, request.url, body=request.body, headers=request.headers)  # Change 'request.path' to 'request.url'
        response = conn.getresponse()
        if response.status >= 400: raise OpenSearchRequestFailedException(f'Status: {response.status}, Reason: {response.reason}, Info: {response.read()}')
        return response

    def __sign_request(self, method, path, payload=None):
        service = 'es'
        credentials = self.session.get_credentials()
        headers = {'Host': self.endpoint_url, 'Content-Type': 'application/json'}
        request = AWSRequest(method=method, url=f"https://{self.endpoint_url}/{path}", data=json.dumps(payload or {}), headers=headers)
        SigV4Auth(credentials, service, self.region).add_auth(request)
        return request.prepare()
