import os

import botocore
from .._types import AWSSessionKeys
from .._aws_service_client import AWSServiceClient


class S3BucketManager(AWSServiceClient):
    def __init__(self, bucket_name: str, region_name: str = 'us-east-1', session_keys: AWSSessionKeys = None):
        super().__init__(service_name='s3', region_name=region_name, session_keys=session_keys)
        self._bucket_name = bucket_name
        self._bucket = self._resource.Bucket(bucket_name)

    def get_file_from_bucket(self, file_key, save_as):
        self._client.download_file(self._bucket_name, file_key, save_as)

    def save_file_to_bucket(self, file_key, saved_as):
        _, file_type = os.path.splitext(saved_as)
        is_folder = not file_type
        if not is_folder:
            self._client.upload_file(saved_as, self._bucket_name, file_key)
        else:
            for entry in os.scandir(saved_as):
                entry_key = os.path.join(file_key, entry.name)
                self.save_file_to_bucket(entry_key, entry.path)

    def put_object(self, key, body):
        self._bucket.put_object(Key=key, Body=body)

    def get_object(self, key):
        try:
            obj = self._resource.Object(self._bucket_name, key).get()
            return (obj['Body'].read()).decode('utf-8')
        except:
            return None

    def get_bucket_id(self):
        return self._bucket_name

    def create_bucket(self, region=None, CORS=None):
        if self.check_exists(): return False
        if region is not None:
            self._client.create_bucket(Bucket=self._bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        else:
            self._client.create_bucket(Bucket=self._bucket_name)

        if CORS:
            self.put_bucket_cors(CORS)

        return True

    def start_multipart_upload(self, file_key, num_parts):
        mp_upload = self._client.create_multipart_upload(
            Bucket=self._bucket_name,
            Key=file_key,
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

    def complete_multipart_upload(self, file_key, parts_list, upload_id):
        self._client.complete_multipart_upload(
            Bucket=self._bucket_name,
            Key=file_key,
            MultipartUpload=parts_list,
            UploadId=upload_id,
        )

    def put_bucket_cors(self, CORS):
        self._client.put_bucket_cors(
            Bucket=self._bucket_name,
            CORSConfiguration=CORS
        )

    def put_bucket_policy(self, policy):
        self._client.put_bucket_policy(Bucket=self._bucket_name, Policy=policy)

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

    def delete_bucket(self):
        self._bucket.delete()

    def get_bucket_location(self):
        try:
            response = self._client.get_bucket_location(Bucket=self._bucket_name)
            return response['LocationConstraint']
        except:
            return None

    def set_bucket_acl(self, acl):
        self._bucket.Acl().put(ACL=acl)

    def get_bucket_acl(self):
        try:
            response = self._client.get_bucket_acl(Bucket=self._bucket_name)
            return response['Grants']
        except:
            return None

    def set_object_acl(self, key, acl):
        self._client.ObjectAcl(self._bucket_name, key).put(ACL=acl)

    def get_object_acl(self, key):
        try:
            response = self._client.get_object_acl(Bucket=self._bucket_name, Key=key)
            return response['Grants']
        except:
            return None

    def list_buckets(self):
        return [bucket.name for bucket in self._client.buckets.all()]

    def delete_object(self, key):
        self._client.Object(self._bucket_name, key).delete()

    def delete_folder(self, folder_name):
        for obj in self._bucket.objects.filter(Prefix=folder_name):
            obj.delete()
        self._bucket.objects.filter(Prefix=folder_name).delete()

    def copy_object(self, source_key, destination_key):
        copy_source = {
            'Bucket': self._bucket_name,
            'Key': source_key
        }
        self._bucket.copy(copy_source, destination_key)

    def list_objects(self):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self._bucket.objects.all()
        ]

    def list_objects_with_prefix(self, prefix):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self._bucket.objects.filter(Prefix=prefix)
        ]

    def upload_file(self, local_file_path, s3_key):
        self._bucket.upload_file(local_file_path, s3_key)

    def download_file(self, s3_key, local_file_path):
        self._bucket.download_file(s3_key, local_file_path)

    def get_object_presigned_url(self, key, expiration=3600):
        return self._client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': key},
            ExpiresIn=expiration,
            HttpMethod='GET'
        )

    def get_key_for_unknown_type(self, key):
        response = self._client.list_objects_v2(Bucket=self._bucket_name, Prefix=key)
        for obj in response.get('Contents', []):
            if obj['Key'].startswith(key):
                return obj['Key']
