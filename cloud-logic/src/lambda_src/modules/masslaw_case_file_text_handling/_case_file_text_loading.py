from src.lambda_src.modules.masslaw_cases_config._storage_config import *
from ...S3_manager.bucket_manager import *


def load_case_file_text(file_id: str):
    cases_content_bucket_manager = S3BucketManager(CASES_CONTENT_BUCKET_ID)
    file_text = cases_content_bucket_manager.get_object(f'{file_id}/client_exposed/extracted_text/plain_text.txt')
    return file_text
