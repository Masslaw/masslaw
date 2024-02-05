import mimetypes
import os

import botocore
from .._types import AWSSessionKeys
from .._aws_service_client import AWSServiceClient
from shared_layer.mlcp_logger import logger


class S3BucketManager(AWSServiceClient):
    def __init__(self, bucket_name: str, region_name: str, session_keys: AWSSessionKeys = None):
        super().__init__(service_name='s3', region_name=region_name, session_keys=session_keys, )
        self._bucket_name = bucket_name
        self._bucket = self._resource.Bucket(bucket_name)

    @logger.process_function("Getting A File From S3 Bucket")
    def get_file_from_bucket(self, file_key, save_as):
        logger.info(f"Downloading file from S3 File key: {file_key} Save as: {save_as}")
        self._client.download_file(self._bucket_name, file_key, save_as)

    @logger.process_function("Saving A File To S3 Bucket")
    def save_file_to_bucket(self, file_key, saved_as):
        logger.info(f"Uploading file to S3 File key: {file_key} Saved as: {saved_as}")
        _, file_type = os.path.splitext(saved_as)
        is_folder = not file_type
        if not is_folder:
            content_type = self._get_content_type_for_file(file_key)
            logger.debug(f"Content type: {content_type}")
            self._client.upload_file(saved_as, self._bucket_name, file_key, ExtraArgs={'ContentType': content_type})
        else:
            logger.debug(f"Folder detected, uploading files recursively")
            for entry in os.scandir(saved_as):
                entry_key = os.path.join(file_key, entry.name)
                self.save_file_to_bucket(entry_key, entry.path)

    @logger.process_function("Putting An Object To S3 Bucket")
    def put_object(self, key, body):
        logger.info(f"Putting object to S3 with key: {key}")
        self._bucket.put_object(Key=key, Body=body)

    @logger.process_function("Getting An Object From S3 Bucket")
    def get_object(self, key):
        logger.info(f"Getting object from S3 with key: {key}")
        try:
            obj = self._resource.Object(self._bucket_name, key).get()
            return (obj['Body'].read()).decode()
        except:
            return None

    def get_bucket_id(self):
        return self._bucket_name

    @logger.process_function("Creating A Bucket")
    def create_bucket(self, region=None, CORS=None):
        if self.check_exists(): return False
        logger.info(f"Creating bucket in S3 with name: {self._bucket_name}")
        if region is not None:
            self._client.create_bucket(Bucket=self._bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        else:
            self._client.create_bucket(Bucket=self._bucket_name)
        if CORS:
            logger.debug("Putting bucket CORS")
            self.put_bucket_cors(CORS)
        return True

    @logger.process_function("Starting A Multipart Upload")
    def start_multipart_upload(self, file_key, num_parts):
        logger.info(f"Starting multipart upload to S3 with file key: {file_key}")
        content_type = self._get_content_type_for_file(file_key)
        mp_upload = self._client.create_multipart_upload(
            Bucket=self._bucket_name,
            Key=file_key,
            ContentType=content_type
        )

        upload_urls = []
        upload_id = mp_upload['UploadId']
        for i in range(num_parts):
            upload_urls.append(self._client.generate_presigned_url(
                'upload_part',
                {
                    'Bucket': self._bucket_name,
                    'Key': file_key,
                    'PartNumber': i + 1,
                    'UploadId': upload_id,
                },
                ExpiresIn=10 * 60,
                HttpMethod='PUT'
            ))

        return {'upload_id': upload_id, 'upload_urls': upload_urls}

    @logger.process_function("Completing A Multipart Upload")
    def complete_multipart_upload(self, file_key, parts_list, upload_id):
        logger.info(f"Completing multipart upload to S3 with file key: {file_key}")
        self._client.complete_multipart_upload(
            Bucket=self._bucket_name,
            Key=file_key,
            MultipartUpload=parts_list,
            UploadId=upload_id,
        )

    @logger.process_function("Putting Bucket CORS")
    def put_bucket_cors(self, CORS):
        logger.info(f"Putting bucket CORS to S3 with CORS: {CORS}")
        self._client.put_bucket_cors(
            Bucket=self._bucket_name,
            CORSConfiguration=CORS
        )

    @logger.process_function("Putting Bucket Policy")
    def put_bucket_policy(self, policy):
        logger.info(f"Putting bucket policy to S3 with policy: {policy}")
        self._client.put_bucket_policy(Bucket=self._bucket_name, Policy=policy)

    @logger.process_function("Checking If Bucket Exists")
    def check_exists(self):
        try:
            self._client.head_bucket(Bucket=self._bucket_name)
            return True
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:  # private bucket
                return True
            elif error_code == 404:  # bucket does not exist
                return False

    @logger.process_function("Deleting A Bucket")
    def delete_bucket(self):
        self._bucket.delete()

    @logger.process_function("Getting Bucket Location")
    def get_bucket_location(self):
        try:
            response = self._client.get_bucket_location(Bucket=self._bucket_name)
            return response['LocationConstraint']
        except:
            return None

    @logger.process_function("Setting Bucket ACL")
    def set_bucket_acl(self, acl):
        self._bucket.Acl().put(ACL=acl)

    @logger.process_function("Getting Bucket ACL")
    def get_bucket_acl(self):
        try:
            response = self._client.get_bucket_acl(Bucket=self._bucket_name)
            return response['Grants']
        except:
            return None

    @logger.process_function("Setting Object ACL")
    def set_object_acl(self, key, acl):
        self._client.ObjectAcl(self._bucket_name, key).put(ACL=acl)

    @logger.process_function("Getting Object ACL")
    def get_object_acl(self, key):
        try:
            response = self._client.get_object_acl(Bucket=self._bucket_name, Key=key)
            return response['Grants']
        except:
            return None

    def list_buckets(self):
        return [bucket.name for bucket in self._client.buckets.all()]

    @logger.process_function("Deleting An Object")
    def delete_object(self, key):
        self._client.Object(self._bucket_name, key).delete()

    @logger.process_function("Deleting A Folder")
    def delete_folder(self, folder_name):
        logger.info(f"Deleting folder from S3 with key: {folder_name}")
        for obj in self._bucket.objects.filter(Prefix=folder_name): obj.delete()
        self._bucket.objects.filter(Prefix=folder_name).delete()

    @logger.process_function("Copying An Object")
    def copy_object(self, source_key, destination_key):
        copy_source = {
            'Bucket': self._bucket_name,
            'Key': source_key
        }
        self._bucket.copy(copy_source, destination_key)

    @logger.process_function("Listing Bucket Objects")
    def list_objects(self):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self._bucket.objects.all()
        ]

    @logger.process_function("Listing Bucket Objects With Prefix")
    def list_objects_with_prefix(self, prefix):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self._bucket.objects.filter(Prefix=prefix)
        ]

    @logger.process_function("Uploading A File")
    def upload_file(self, local_file_path, s3_key):
        logger.info(f"Uploading file to S3 with key: {s3_key} from: {local_file_path}")
        content_type = self._get_content_type_for_file(local_file_path)
        self._bucket.upload_file(local_file_path, s3_key, ExtraArgs={'ContentType': content_type})

    @logger.process_function("Downloading A File")
    def download_file(self, s3_key, local_file_path):
        logger.info(f"Downloading file from S3 with key: {s3_key} to: {local_file_path}")
        self._bucket.download_file(s3_key, local_file_path)

    @logger.process_function("Getting Object Presigned URL")
    def get_object_presigned_url(self, key, expiration=3600):
        logger.info(f"Getting presigned URL for S3 with key: {key}")
        return self._client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': key},
            ExpiresIn=expiration,
            HttpMethod='GET'
        )

    @logger.process_function("Getting Key For Unknown Type")
    def get_key_for_unknown_type(self, key):
        logger.info(f"Getting key for unknown type from S3 with key: {key}")
        response = self._client.list_objects_v2(Bucket=self._bucket_name, Prefix=key)
        for obj in response.get('Contents', []):
            if obj['Key'].startswith(key):
                return obj['Key']

    def _get_content_type_for_file(self, file_path) -> str:
        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or 'application/octet-stream'
