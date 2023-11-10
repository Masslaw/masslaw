import os
import unittest

import boto3
from moto import mock_s3

from resources_layer.aws.s3_client import S3BucketManager


class TestClassS3BucketManager(unittest.TestCase):

    @mock_s3
    def test_get_file_from_bucket(self):
        bucket_name = 'test-bucket'
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=bucket_name)

        file_content = "Test file content"
        file_key = "test.txt"
        s3.Object(bucket_name, file_key).put(Body=file_content)

        save_as_path = "/tmp/downloaded_test.txt"
        bucket_manager = S3BucketManager(bucket_name, 'us-east-1')
        bucket_manager.get_file_from_bucket(file_key, save_as_path)

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

        bucket_manager = S3BucketManager(bucket_name, 'us-east-1')
        bucket_manager.save_file_to_bucket(file_key, saved_as_path)

        obj = s3.Object(bucket_name, file_key)
        self.assertEqual(obj.get()["Body"].read().decode(), file_content)

    @mock_s3
    def test_save_folder_to_bucket(self):
        bucket_name = 'test-bucket'
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=bucket_name)

        folder_path = "/tmp/upload_folder"
        file_key = "folder_key"
        os.makedirs(folder_path, exist_ok=True)

        file1_content = "Test file1"
        file1_path = os.path.join(folder_path, "file1.txt")
        with open(file1_path, 'w') as f:
            f.write(file1_content)

        file2_content = "Test file2"
        file2_path = os.path.join(folder_path, "file2.txt")
        with open(file2_path, 'w') as f:
            f.write(file2_content)

        bucket_manager = S3BucketManager(bucket_name, 'us-east-1')
        bucket_manager.save_file_to_bucket(file_key, folder_path)

        obj1 = s3.Object(bucket_name, os.path.join(file_key, "file1.txt"))
        self.assertEqual(obj1.get()["Body"].read().decode(), file1_content)

        obj2 = s3.Object(bucket_name, os.path.join(file_key, "file2.txt"))
        self.assertEqual(obj2.get()["Body"].read().decode(), file2_content)
