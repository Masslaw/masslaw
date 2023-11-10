import unittest

import boto3
from moto import mock_s3

from logic_layer.remote_storage.s3_bucket_storage_manager._s3_bucket_storage_manager import S3BucketStorageManager


class TestS3BucketStorageManager(unittest.TestCase):

    @mock_s3
    def test_get_file_from_bucket(self):
        bucket_name = 'test-bucket'
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=bucket_name)

        file_content = "Test file content"
        file_key = "test.txt"
        s3.Object(bucket_name, file_key).put(Body=file_content)

        save_as_path = "/tmp/downloaded_test.txt"
        storage_manager = S3BucketStorageManager(bucket_name)
        storage_manager.get_file_from_bucket(file_key, save_as_path)

        with open(save_as_path, 'r') as f:
            self.assertEqual(f.read(), file_content)

    @mock_s3
    def test_save_file_to_bucket(self):
        bucket_name = 'test-bucket'
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=bucket_name)

        file_content = "Test file content for upload"
        saved_as_path = "/tmp/upload_test.txt"
        file_key = "upload_test.txt"

        with open(saved_as_path, 'w') as f:
            f.write(file_content)

        storage_manager = S3BucketStorageManager(bucket_name)
        storage_manager.save_file_to_bucket(file_key, saved_as_path)

        obj = s3.Object(bucket_name, file_key)
        self.assertEqual(obj.get()["Body"].read().decode(), file_content)
