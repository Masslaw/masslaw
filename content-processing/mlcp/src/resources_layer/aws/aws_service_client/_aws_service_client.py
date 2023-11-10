import os

import boto3

from resources_layer.aws._config import service_access_key_id_suffix
from resources_layer.aws._config import service_secret_access_key_suffix
from resources_layer.aws._config import service_session_token_suffix
from resources_layer.aws._types import AWSSessionKeys


class AWSServiceClient:
    def __init__(self, service_name, region_name, session_keys: AWSSessionKeys = None):
        self._service_name = service_name
        self._region_name = region_name
        self._session_keys = session_keys
        if not self._session_keys: self._load_environment_session_keys()
        self._start_session()

    def _start_session(self):
        self._session = boto3.Session(aws_access_key_id=self._session_keys[0], aws_secret_access_key=self._session_keys[1], aws_session_token=self._session_keys[2])
        self._client = self._session.client(self._service_name, region_name=self._region_name)
        self._resource = self._session.resource(self._service_name, region_name=self._region_name)

    def _load_environment_session_keys(self):
        access_key_id = os.environ.get(f"{self._service_name}{service_access_key_id_suffix}", '')
        access_key_secret = os.environ.get(f"{self._service_name}{service_secret_access_key_suffix}", '')
        session_token = os.environ.get(f"{self._service_name}{service_session_token_suffix}", '')
        self._session_keys = (access_key_id, access_key_secret, session_token)
