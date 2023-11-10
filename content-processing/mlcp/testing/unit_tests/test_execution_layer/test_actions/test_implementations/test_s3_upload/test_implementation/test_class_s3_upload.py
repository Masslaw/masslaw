import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import boto3
import moto

from execution_layer.actions._exceptions import ApplicationActionRequiredParamMissingException
from execution_layer.actions._implementations.s3_upload import S3Upload


class TestClassS3Upload(unittest.TestCase):

    def test_init_with_required_params(self):
        action = S3Upload(params={_key: 'value' for _key in S3Upload._required_params})

    def test_init_with_missing_required_params(self):
        with self.assertRaises(ApplicationActionRequiredParamMissingException):
            action = S3Upload()

    def test_handle_arguments(self):
        action = S3Upload(params={'bucket': 'bucket_name', 'files_data': ['some_file_data']})

        action._handle_arguments()

        self.assertEqual(action._bucket_name, 'bucket_name')
        self.assertEqual(action._files_data, ['some_file_data'])

    @patch('execution_layer.actions._implementations.s3_upload._implementation.S3Upload._S3Upload__handle_upload_file_data')
    def test_execution(self, mock_handle_upload_file_data):
        action = S3Upload(params={'bucket': 'bucket_name', 'files_data': ['some_file_data', 'some_another_file_data']})

        action._handle_arguments()
        action._execute()

        mock_handle_upload_file_data.assert_any_call('some_file_data')
        mock_handle_upload_file_data.assert_any_call('some_another_file_data')

    @moto.mock_s3
    def test_uploading_file_to_s3(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        bucket_name = 'my-test-bucket'
        conn.create_bucket(Bucket=bucket_name)

        test_file_content = 'This is a test file'
        test_file_key = 'test_key'
        test_file_name = os.path.join(tempfile.mkdtemp(), 'test_file.txt')
        with open(test_file_name, 'w') as f:
            f.write(test_file_content)
        test_file_data = {
            'key': test_file_key,
            'saved_as': test_file_name
        }

        action = S3Upload(params={'bucket': bucket_name, 'files_data': [test_file_data]})
        action._handle_arguments()
        action._S3Upload__handle_upload_file_data(file_data=test_file_data)

        body = (
            conn.Object(bucket_name, test_file_key)
            .get()['Body']
            .read()
            .decode('utf-8')
        )
        self.assertEqual(body, test_file_content)
