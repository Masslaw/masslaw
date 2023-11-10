import os

from resources_layer.aws._types import AWSSessionKeys
from resources_layer.aws.aws_service_client import AWSServiceClient
from shared_layer.file_system_utils import file_system_utils


class S3BucketManager(AWSServiceClient):
    def __init__(self, bucket_name: str, region_name: str, session_keys: AWSSessionKeys = None):
        super().__init__(service_name='s3', region_name=region_name, session_keys=session_keys, )
        self._bucket_name = bucket_name

    def get_file_from_bucket(self, file_key, save_as):
        self._client.download_file(self._bucket_name, file_key, save_as)

    def save_file_to_bucket(self, file_key, saved_as):
        is_folder = not file_system_utils.get_file_type(saved_as)
        if not is_folder:
            self._client.upload_file(saved_as, self._bucket_name, file_key)
        else:
            for entry in os.scandir(saved_as):
                entry_key = os.path.join(file_key, entry.name)
                self.save_file_to_bucket(entry_key, entry.path)
