import boto3
import botocore.exceptions
from botocore.config import Config


class S3BucketManager:
    def __init__(self, bucket_name, access_key_id=None, secret_access_key=None, session_key=None):
        self.__bucket_name = bucket_name
        self.__s3_client = boto3.client('s3',
                                        region_name='us-east-1',
                                        config=Config(signature_version='s3v4'),
                                        aws_access_key_id=access_key_id,
                                        aws_secret_access_key=secret_access_key,
                                        aws_session_token=session_key)
        self.__s3_resource = boto3.resource('s3',
                                            aws_access_key_id=access_key_id,
                                            aws_secret_access_key=secret_access_key,
                                            aws_session_token=session_key)
        self.__bucket = self.__s3_resource.Bucket(bucket_name)

    def get_bucket_id(self):
        return self.__bucket_name

    def create_bucket(self, region=None, CORS=None):
        if self.check_exists(): return False
        if region is not None:
            self.__s3_client.create_bucket(Bucket=self.__bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        else:
            self.__s3_client.create_bucket(Bucket=self.__bucket_name)

        if CORS:
            self.put_bucket_cors(CORS)

        return True

    def start_multipart_upload(self, file_key, num_parts):
        mp_upload = self.__s3_client.create_multipart_upload(
            Bucket=self.__bucket_name,
            Key=file_key,
        )

        upload_urls = []

        upload_id = mp_upload['UploadId']

        for i in range(num_parts):
            upload_urls.append(self.__s3_client.generate_presigned_url(
                'upload_part',
                {
                    'Bucket': self.__bucket_name,
                    'Key': file_key,
                    'PartNumber': i + 1,
                    'UploadId': upload_id,
                },
                ExpiresIn=10 * 60,
                HttpMethod='PUT'
            ))

        return {'upload_id': upload_id, 'upload_urls': upload_urls}

    def complete_multipart_upload(self, file_key, parts_list, upload_id):
        self.__s3_client.complete_multipart_upload(
            Bucket=self.__bucket_name,
            Key=file_key,
            MultipartUpload=parts_list,
            UploadId=upload_id,
        )

    def put_bucket_cors(self, CORS):
        self.__s3_client.put_bucket_cors(
            Bucket=self.__bucket_name,
            CORSConfiguration=CORS
        )

    def put_bucket_policy(self, policy):
        self.__s3_client.put_bucket_policy(Bucket=self.__bucket_name, Policy=policy)

    def check_exists(self):
        try:
            self.__s3_client.head_bucket(Bucket=self.__bucket_name)
            return True
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:  # private bucket
                return True
            elif error_code == 404:  # bucket does not exist
                return False

    def delete_bucket(self):
        self.__bucket.delete()

    def get_bucket_location(self):
        try:
            response = self.__s3_client.get_bucket_location(Bucket=self.__bucket_name)
            return response['LocationConstraint']
        except:
            return None

    def set_bucket_acl(self, acl):
        self.__bucket.Acl().put(ACL=acl)

    def get_bucket_acl(self):
        try:
            response = self.__s3_client.get_bucket_acl(Bucket=self.__bucket_name)
            return response['Grants']
        except:
            return None

    def set_object_acl(self, key, acl):
        self.__s3_client.ObjectAcl(self.__bucket_name, key).put(ACL=acl)

    def get_object_acl(self, key):
        try:
            response = self.__s3_client.get_object_acl(Bucket=self.__bucket_name, Key=key)
            return response['Grants']
        except:
            return None

    def list_buckets(self):
        return [bucket.name for bucket in self.__s3_client.buckets.all()]

    def put_object(self, key, body):
        self.__bucket.put_object(Key=key, Body=body)

    def get_object(self, key):
        try:
            obj = self.__s3_resource.Object(self.__bucket_name, key).get()
            return (obj['Body'].read()).decode()
        except:
            return None

    def delete_object(self, key):
        self.__s3_client.Object(self.__bucket_name, key).delete()

    def delete_folder(self, folder_name):
        for obj in self.__bucket.objects.filter(Prefix=folder_name):
            obj.delete()
        self.__bucket.objects.filter(Prefix=folder_name).delete()

    def copy_object(self, source_key, destination_key):
        copy_source = {
            'Bucket': self.__bucket_name,
            'Key': source_key
        }
        self.__bucket.copy(copy_source, destination_key)

    def list_objects(self):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self.__bucket.objects.all()
        ]

    def list_objects_with_prefix(self, prefix):
        return [
            {
                'Key': obj.key,
                'Size': obj.size,
                'LastModified': obj.last_modified
            }
            for obj in self.__bucket.objects.filter(Prefix=prefix)
        ]

    def upload_file(self, local_file_path, s3_key):
        self.__bucket.upload_file(local_file_path, s3_key)

    def download_file(self, s3_key, local_file_path):
        self.__bucket.download_file(s3_key, local_file_path)

    def get_object_presigned_url(self, key, expiration=3600):
        return self.__s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.__bucket_name, 'Key': key},
            ExpiresIn=expiration,
            HttpMethod='GET'
        )

    def get_key_for_unknown_type(self, key):
        response = self.__s3_client.list_objects_v2(Bucket=self.__bucket_name, Prefix=key)
        for obj in response.get('Contents', []):
            if obj['Key'].startswith(key):
                return obj['Key']
