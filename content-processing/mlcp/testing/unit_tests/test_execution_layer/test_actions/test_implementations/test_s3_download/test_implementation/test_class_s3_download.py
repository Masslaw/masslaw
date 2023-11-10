import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import boto3
import moto

from execution_layer.actions._exceptions import ApplicationActionRequiredParamMissingException
from execution_layer.actions._implementations.s3_download import S3Download


class TestClassS3Download(unittest.TestCase):

    def test_init_with_required_params(self):
        action = S3Download(params={_key: 'value' for _key in S3Download._required_params})

    def test_init_with_missing_required_params(self):
        with self.assertRaises(ApplicationActionRequiredParamMissingException):
            action = S3Download()

    def test_handle_arguments(self):
        action = S3Download(params={'bucket': 'bucket_name', 'files_data': ['some_file_data']})

        action._handle_arguments()

        self.assertEqual(action._bucket_name, 'bucket_name')
        self.assertEqual(action._files_data, ['some_file_data'])

    @patch('execution_layer.actions._implementations.s3_download._implementation.S3Download._S3Download__handle_download_file_data')
    def test_execution(self, mock_handle_download_file_data):
        action = S3Download(params={'bucket': 'bucket_name', 'files_data': ['some_file_data', 'some_another_file_data']})

        action._handle_arguments()
        action._execute()

        mock_handle_download_file_data.assert_any_call('some_file_data')
        mock_handle_download_file_data.assert_any_call('some_another_file_data')

    @moto.mock_s3
    def test_downloading_file_from_s3(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        bucket_name = 'my-test-bucket'
        conn.create_bucket(Bucket=bucket_name)

        test_file_content = 'This is a test file content'
        test_file_key = 'test_file_key'
        conn.Object(bucket_name, test_file_key).put(Body=test_file_content)

        with tempfile.TemporaryDirectory() as temp_dir:
            test_save_as = os.path.join(temp_dir, 'downloaded_file.txt')
            test_file_data = {
                'key': test_file_key,
                'save_as': test_save_as
            }

            action = S3Download(params={'bucket': bucket_name, 'files_data': [test_file_data]})
            action._handle_arguments()
            action._execute()

            self.assertTrue(os.path.exists(test_save_as))

            with open(test_save_as, 'r') as file:
                downloaded_content = file.read()
            self.assertEqual(downloaded_content, test_file_content)
