from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.masslaw_cases_config import storage_config


def load_case_file_text(file_id: str):
    cases_content_bucket_manager = S3BucketManager(storage_config.CASES_CONTENT_BUCKET_ID)
    file_text = cases_content_bucket_manager.get_object(f'{file_id}/client_exposed/extracted_text/plain_text.txt')
    return file_text
