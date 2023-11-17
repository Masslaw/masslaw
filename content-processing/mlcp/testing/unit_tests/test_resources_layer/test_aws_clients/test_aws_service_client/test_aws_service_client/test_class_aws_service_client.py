import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import boto3

from resources_layer.aws_clients._aws_service_client._aws_service_client import AWSServiceClient


class TestClassAWSServiceClient(unittest.TestCase):

    def setUp(self):
        self.mock_boto3_session_patcher = patch('boto3.Session')
        self.mock_boto3_session_class = self.mock_boto3_session_patcher.start()
        self.mock_session_instance = MagicMock(spec=boto3.Session)
        self.mock_boto3_session_class.return_value = self.mock_session_instance
        self.mock_client = MagicMock()
        self.mock_resource = MagicMock()
        self.mock_session_instance.attach_mock(self.mock_client, 'client')
        self.mock_session_instance.attach_mock(self.mock_resource, 'resource')

    def tearDown(self):
        self.mock_boto3_session_patcher.stop()

    def test_initialization_with_session_keys(self):
        client = AWSServiceClient('s3', 'us-west-1', ('key', 'secret', 'token'))

        self.assertEqual(client._session_keys, ('key', 'secret', 'token'))
        self.assertEqual(client._service_name, 's3')
        self.assertEqual(client._region_name, 'us-west-1')

    @patch('os.environ', {"s3_access_key_id": "test_key", "s3_secret_access_key": "test_secret", "s3_session_token": "test_token"})
    def test_initialization_without_session_keys(self):
        client = AWSServiceClient('s3', 'us-west-1')

        self.assertEqual(client._session_keys, ('test_key', 'test_secret', 'test_token'))

    def test_start_session(self):
        _client = AWSServiceClient('s3', 'us-west-1', ('key', 'secret', 'token'))

        self.mock_boto3_session_class.assert_called_once_with(aws_access_key_id='key', aws_secret_access_key='secret',
            aws_session_token='token')
        self.mock_client.assert_called_once_with('s3', region_name='us-west-1')
        self.mock_resource.assert_called_once_with('s3', region_name='us-west-1')
