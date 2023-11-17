from resources_layer.aws_clients.s3_client import S3BucketManager


class S3BucketStorageManager:
    """
    This class is nothing but a wrapper for S3BucketManager.
    Configured to operate specifically in us-east-1 region.
    """

    def __init__(self, bucket_name: str):
        self._bucket_manager = S3BucketManager(bucket_name=bucket_name, region_name='us-east-1')

    def get_file_from_bucket(self, file_key: str, save_as: str):
        return self._bucket_manager.get_file_from_bucket(file_key=file_key, save_as=save_as)

    def save_file_to_bucket(self, file_key: str, saved_as: str):
        return self._bucket_manager.save_file_to_bucket(file_key=file_key, saved_as=saved_as)
