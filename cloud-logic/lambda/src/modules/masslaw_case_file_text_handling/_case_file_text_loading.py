from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.masslaw_cases_config import storage_config
import xml.etree.ElementTree as ET


cases_content_bucket_manager = S3BucketManager(storage_config.CASES_CONTENT_BUCKET_ID)


def load_case_file_text(file_id: str):
    file_text = cases_content_bucket_manager.get_object(f'{file_id}/client_exposed/extracted_text/plain_text.txt')
    return file_text


def load_case_file_text_structure(file_id: str) -> ET.Element:
    file_text_structure_text = cases_content_bucket_manager.get_object(f'{file_id}/client_exposed/extracted_text/text_structure.xml')
    root = ET.fromstring(file_text_structure_text)
    return root
