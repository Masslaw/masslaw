import os.path

import boto3

from service.extracted_optical_text_structure.document_loading import DocumentLoader

cases_content_bucket = "masslaw-cases-content"


def load_masslaw_file(file_id: str, access_key_id: str, secret_access_key: str, file_download_directory: str, data_out: dict):
    file_structure_s3_key = f'{file_id}/client_exposed/extracted_text/text_structure.xml'
    boto3_session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    s3_client = boto3_session.client('s3')

    file_structure_data_path = os.path.join(file_download_directory, 'text_structure.xml')
    s3_client.download_file(cases_content_bucket, file_structure_s3_key, file_structure_data_path)

    data_out['file_structure_data_path'] = file_structure_data_path

    with open(file_structure_data_path, 'r') as f:
        optical_text_document = DocumentLoader().load_xml(f)

    data_out['optical_text_document'] = optical_text_document

    document_page_sizes = optical_text_document.get_metadata()

    print(document_page_sizes)
