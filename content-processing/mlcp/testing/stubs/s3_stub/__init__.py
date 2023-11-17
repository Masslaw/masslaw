import boto3
import moto


class S3StubTestLoader:
    _client = None
    _moto_s3 = moto.mock_s3()

    _active = False

    def start_s3_stub(self):
        if self._active: return
        self._moto_s3.start()
        self._active = True

    def stop_s3_stub(self):
        if not self._active: return
        self._moto_s3.stop()
        self._active = False

    def create_client(self):
        self._client = boto3.client('s3')

    def create_bucket(self, bucket_name):
        self._client.create_bucket(Bucket=bucket_name)

    def upload_file(self, bucket_name, file_path, key):
        self._client.upload_file(file_path, bucket_name, key)

    def list_buckets(self):
        return self._client.list_buckets()

    def list_files(self, bucket_name):
        return self._client.list_objects(Bucket=bucket_name)
